"""
Kriu-Bench-v0.3 Local In-Process Benchmark Runner
==================================================
Runs Phase 1 and Phase 2 evaluations locally in-process without remote network calls.
Handles single-key Groq Free Tier limits (~15s rate-limit pacing, token tracking,
automatic Retry-After backoff, and per-resume atomic disk checkpointing).

Non-invasively injects synthetic GitHub & HTTP proof payloads without editing any core files.

Modes:
- Phase 1: Ingests all 100 resumes per role, runs RSSE parsing + HybridRetriever Top-10% coarse filter,
           and runs Stage-1 LLM Evidence Judge evaluations.
- Phase 2: Ingests Phase 1 checkpoints + synthetic Stage-2 payloads, executes GitHub code matching,
           SignalOrchestrator heuristics + checks, and OutcomeEngine synthesis (proof_brief, grill kit, recruiter_decision).
"""

import os
import sys
import json
import time
import math
import asyncio
import logging
import argparse
from typing import Dict, List, Any, Optional
from datetime import datetime

# Add root workspace to sys.path
WORKSPACE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if WORKSPACE_DIR not in sys.path:
    sys.path.insert(0, WORKSPACE_DIR)

from dotenv import load_dotenv
load_dotenv(os.path.join(WORKSPACE_DIR, ".env"))

# Import core Kriu modules locally in-process
from resume_parsing import ResumeParser, HybridRetriever
from jd_skill_extraction import JDExtractor
from evidence_engine import EvidenceAnalyzer, build_score_explanation
from models import SkillEvaluation, RankedResume, RankingResult
import signals.orchestrator as orch_module
import signals.dev_footprint as dev_module
import signals.http_proof as http_module
from signals.dev_footprint import match_skills_against_repos
from evidence_engine import map_to_evidence_level
from outcome_engine import generate_aaas_outcome

def generate_instant_verdict(job_description: str, verified_skills: List[str], partial_skills: List[str], 
                            missing_skills: List[str], all_skills: List[str]) -> str:
    clean_verified = [s.split(" | ")[0].strip() for s in verified_skills if s.strip()]
    clean_partial = [s.split(" | ")[0].strip() for s in partial_skills if s.strip()]
    clean_missing = [s.split(" | ")[0].strip() for s in missing_skills if s.strip()]

    if len(clean_verified) >= 2:
        s1 = f"Demonstrates verified hands-on implementation in {', '.join(clean_verified[:2])} across technical projects and work experience."
    elif clean_verified:
        s1 = f"Demonstrates practical capability in {clean_verified[0]} with foundational context in related technical areas."
    elif clean_partial:
        s1 = f"Shows foundational exposure to {', '.join(clean_partial[:2])} primarily in academic or skills listing contexts."
    else:
        s1 = "Shows general exposure to technical environments but lacks concrete production implementation evidence."

    if clean_missing:
        s2 = f"Screening recommended to probe practical proficiency in {', '.join(clean_missing[:2])}."
    elif clean_partial:
        s2 = f"Opportunity to evaluate real-world depth of {', '.join(clean_partial[:2])} during technical screening."
    else:
        s2 = "Meets all primary technical competency requirements without notable gaps."

    return f"{s1} {s2}"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("Kriu-Bench-v0.3")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESUMES_DIR = os.path.join(BASE_DIR, "resumes")
JDS_DIR = os.path.join(BASE_DIR, "jds")
GROUND_TRUTH_FILE = os.path.join(BASE_DIR, "ground_truth_300.json")
PAYLOADS_FILE = os.path.join(BASE_DIR, "payloads", "synthetic_stage2_payloads.json")
RESULTS_DIR = os.path.join(BASE_DIR, "results")
PHASE1_DIR = os.path.join(RESULTS_DIR, "phase1")
PHASE2_DIR = os.path.join(RESULTS_DIR, "phase2")

os.makedirs(PHASE1_DIR, exist_ok=True)
os.makedirs(PHASE2_DIR, exist_ok=True)

# -------------------------------------------------------------
# GROQ RATE-LIMIT PACER FOR FREE TIER (openai/gpt-oss-20b)
# Limits: 30 RPM, 8,000 TPM, 200,000 TPD
# -------------------------------------------------------------
class GroqRateLimitPacer:
    """Enforces dynamic pacing, token accounting, and checkpointing for Groq API."""
    def __init__(self, min_gap_seconds: float = 5.0, max_daily_tokens: int = 195000):
        self.min_gap_seconds = min_gap_seconds
        self.max_daily_tokens = max_daily_tokens
        self.last_call_time = 0.0
        self.cumulative_tokens = 0
        self.call_count = 0

    def pace_before_call(self, estimated_tokens: int = 1400):
        """Sleeps if necessary to stay safely under 8,000 TPM limit."""
        now = time.time()
        elapsed = now - self.last_call_time
        if elapsed < self.min_gap_seconds:
            sleep_needed = self.min_gap_seconds - elapsed
            logger.info(f"[RateLimitPacer] Pacing {sleep_needed:.1f}s to respect Groq TPM limit (<8,000 TPM)...")
            time.sleep(sleep_needed)

        # Check daily ceiling
        if self.cumulative_tokens + estimated_tokens > self.max_daily_tokens:
            logger.warning(f"[RateLimitPacer] Approaching daily token budget ({self.cumulative_tokens}/{self.max_daily_tokens} tokens). Checkpoint saved. Run can resume tomorrow.")
            raise RuntimeError("GROQ_DAILY_TOKEN_LIMIT_REACHED")

    def record_call(self, tokens_used: int = 1400):
        self.last_call_time = time.time()
        self.cumulative_tokens += tokens_used
        self.call_count += 1
        logger.info(f"[RateLimitPacer] Call #{self.call_count} recorded. Session tokens: ~{self.cumulative_tokens}/{self.max_daily_tokens}")

pacer = GroqRateLimitPacer(min_gap_seconds=5.0)

# -------------------------------------------------------------
# NON-INVASIVE MONKEYPATCHING FOR SYNTHETIC STAGE-2 INJECTION
# -------------------------------------------------------------
_CURRENT_SYNTHETIC_PAYLOAD: Optional[Dict[str, Any]] = None

async def patched_analyze_github_profile(*args, **kwargs):
    """In-process mock that returns the assigned candidate's synthetic GitHub analysis."""
    global _CURRENT_SYNTHETIC_PAYLOAD
    if _CURRENT_SYNTHETIC_PAYLOAD and "github_analysis" in _CURRENT_SYNTHETIC_PAYLOAD:
        return _CURRENT_SYNTHETIC_PAYLOAD["github_analysis"]
    return {"found": False}

async def patched_verify_proof_urls(*args, **kwargs):
    """In-process mock that returns the assigned candidate's synthetic HTTP proofs."""
    global _CURRENT_SYNTHETIC_PAYLOAD
    if _CURRENT_SYNTHETIC_PAYLOAD and "http_proofs" in _CURRENT_SYNTHETIC_PAYLOAD:
        return _CURRENT_SYNTHETIC_PAYLOAD["http_proofs"]
    return []

# Apply monkeypatches to avoid modifying signals/orchestrator.py
orch_module.analyze_github_profile = patched_analyze_github_profile
orch_module.verify_proof_urls = patched_verify_proof_urls
dev_module.analyze_github_profile = patched_analyze_github_profile
http_module.verify_proof_urls = patched_verify_proof_urls

# -------------------------------------------------------------
# BENCHMARK EVALUATOR
# -------------------------------------------------------------
class BenchmarkRunner:
    def __init__(self):
        with open(GROUND_TRUTH_FILE, "r", encoding="utf-8") as f:
            self.ground_truth = json.load(f)

        with open(PAYLOADS_FILE, "r", encoding="utf-8") as f:
            self.payloads = json.load(f)

        from sentence_transformers import SentenceTransformer
        logger.info("Loading shared SentenceTransformer weights (loaded ONCE into memory)...")
        self.shared_encoder = SentenceTransformer("all-MiniLM-L6-v2")

        self.parser = ResumeParser()
        self.retriever = HybridRetriever(encoder=self.shared_encoder)
        self.jd_extractor = JDExtractor()
        self.evidence_analyzer = EvidenceAnalyzer(encoder=self.shared_encoder)
        self.orchestrator = orch_module.SignalOrchestrator()

        # Pre-load JDs
        self.jds = {
            "BE": self._load_file(os.path.join(JDS_DIR, "JD-BE.txt")),
            "DS": self._load_file(os.path.join(JDS_DIR, "JD-DS.txt")),
            "SALES": self._load_file(os.path.join(JDS_DIR, "JD-SALES.txt"))
        }

        # Canonical skills
        self.canonical_skills = {
            "BE": [
                {"skill": "Python", "aliases": []},
                {"skill": "FastAPI", "aliases": []},
                {"skill": "PostgreSQL", "aliases": []},
                {"skill": "Docker", "aliases": []},
                {"skill": "Redis", "aliases": []},
                {"skill": "CI/CD", "aliases": []}
            ],
            "DS": [
                {"skill": "Python", "aliases": []},
                {"skill": "PyTorch", "aliases": []},
                {"skill": "scikit-learn", "aliases": ["sklearn"]},
                {"skill": "SQL", "aliases": []},
                {"skill": "MLflow", "aliases": []},
                {"skill": "Docker", "aliases": []}
            ],
            "SALES": [
                {"skill": "Salesforce", "aliases": ["Salesforce CRM"]},
                {"skill": "Outbound prospecting", "aliases": ["Outbound"]},
                {"skill": "Pipeline management", "aliases": []},
                {"skill": "MEDDICC", "aliases": ["MEDDPICC"]},
                {"skill": "Contract negotiation", "aliases": []},
                {"skill": "Sales forecasting", "aliases": ["Forecasting"]}
            ]
        }

    def _load_file(self, path: str) -> str:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def parse_all_resumes_for_role(self, role_key: str) -> List[Dict[str, Any]]:
        """Parses all 100 resumes for a role with RSSE and prepares corpus texts."""
        role_resumes = []
        for r_id, meta in self.ground_truth.items():
            if meta["role_key"] != role_key:
                continue
            fname = meta["filename"]
            fpath = os.path.join(RESUMES_DIR, fname)
            with open(fpath, "rb") as f:
                content = f.read()
            raw_text, sections = self.parser.parse_and_segment(content, fname)
            hybrid_text = self.parser.get_hybrid_search_text(sections)
            role_resumes.append({
                "resume_id": r_id,
                "filename": fname,
                "raw_text": raw_text,
                "sections": sections,
                "hybrid_text": hybrid_text,
                "file_bytes": content,
                "meta": meta
            })
        logger.info(f"Loaded and parsed {len(role_resumes)} resumes for {role_key}.")
        return role_resumes

    def run_stage1_coarse_filter(self, role_key: str, role_resumes: List[Dict[str, Any]], filter_ratio: float = 0.50) -> Dict[str, Any]:
        """
        Runs HybridRetriever (BM25 + Semantic Search) across all N ingested resumes
        and filters to the Top n = ceil(filter_ratio * N) (e.g. Top 50 for N=100 when filter_ratio=0.50).
        """
        jd_text = self.jds[role_key]
        must_have = self.canonical_skills[role_key]
        skills_str = " ".join(s["skill"] for s in must_have)
        query = f"{jd_text} {skills_str}"
        corpus = [r["hybrid_text"] for r in role_resumes]

        n_count = math.ceil(filter_ratio * len(role_resumes))
        logger.info(f"Executing Stage-1 HybridRetriever coarse filter for {role_key}: Ingested N={len(role_resumes)} -> Filtering Top n={n_count} (ratio: {filter_ratio*100:.0f}%)...")

        top_picks = self.retriever.compute_hybrid_score(
            query,
            corpus,
            top_k=n_count,
            bm25_top_k=min(60, len(role_resumes)),
            alpha=0.75
        )

        # Audit top picks
        top_indices = [p["index"] for p in top_picks]
        top_candidates = [role_resumes[idx] for idx in top_indices]

        gold_retrieved = sum(1 for c in top_candidates if c["meta"]["is_top_10"])
        stuffers_leaked = sum(1 for c in top_candidates if c["meta"]["category"] == "B")

        filter_stats = {
            "role_key": role_key,
            "filter_ratio": filter_ratio,
            "total_ingested": len(role_resumes),
            "top_n_filtered": n_count,
            "gold_candidates_in_top_n": gold_retrieved,
            "gold_recall_pct": round((gold_retrieved / 10) * 100, 1),
            "stuffers_leaked_count": stuffers_leaked,
            "stuffers_leakage_pct": round((stuffers_leaked / n_count) * 100, 1),
            "top_picks_metadata": [
                {
                    "rank": idx + 1,
                    "resume_id": c["resume_id"],
                    "category": c["meta"]["category"],
                    "is_top_10_gold": c["meta"]["is_top_10"],
                    "hybrid_score": top_picks[idx]["score"]
                }
                for idx, c in enumerate(top_candidates)
            ]
        }
        logger.info(f"Stage-1 Coarse Filter Result for {role_key}: Gold Recall@{int(filter_ratio*100)}% = {filter_stats['gold_recall_pct']}% ({gold_retrieved}/10) | Stuffer Leakage = {filter_stats['stuffers_leakage_pct']}% ({stuffers_leaked}/{n_count})")
        return filter_stats

    def evaluate_single_resume_stage1(self, resume_item: Dict[str, Any], role_key: str) -> Dict[str, Any]:
        """Evaluates a single resume under Stage-1 LLM Evidence Judge with checkpointing."""
        r_id = resume_item["resume_id"]
        ckpt_path = os.path.join(PHASE1_DIR, f"{r_id}.json")
        if os.path.exists(ckpt_path):
            with open(ckpt_path, "r", encoding="utf-8") as f:
                return json.load(f)

        must_have = self.canonical_skills[role_key]
        jd_text = self.jds[role_key]
        sections = resume_item["sections"]

        # Run EvidenceAnalyzer with rate-limit pacing and 429 backoff retry
        evals_raw = None
        for attempt in range(5):
            try:
                pacer.pace_before_call()
                evals_raw = self.evidence_analyzer.evaluate_skills_batch(
                    candidates_sections=[sections],
                    skills=must_have,
                    candidate_filenames=[resume_item["filename"]]
                )[0]
                pacer.record_call()
                break
            except Exception as e:
                err_str = str(e)
                if "429" in err_str or "rate_limit" in err_str.lower():
                    backoff = 20 * (attempt + 1)
                    logger.warning(f"[RateLimit 429] Backoff {backoff}s before retry {attempt+1}/5 for {r_id}...")
                    time.sleep(backoff)
                else:
                    logger.error(f"Error evaluating {r_id}: {e}")
                    raise e

        evaluations = []
        score_tally = 0.0
        calibrated_tally = 0.0

        for s_idx, skill in enumerate(must_have):
            item = evals_raw[s_idx]
            ev_level = item.get("evidence_level", "Not Found")
            status = item.get("status", "Missing")
            calibrated = float(item.get("calibrated_score", 0.0))
            best_chunk = (item.get("best_evidence_text", "") or "").strip()

            evaluations.append({
                "skill": skill["skill"],
                "evidence_level": ev_level,
                "status": status,
                "calibrated_score": calibrated,
                "confidence_score": float(item.get("confidence_score", 0.0)),
                "evidence_chunk": best_chunk,
                "consistency_check": item.get("consistency_check"),
                "component_scores": item.get("component_scores", {})
            })

            calibrated_tally += calibrated
            if ev_level in ("Code-Verified", "Resume-Demonstrated") or status == "Verified Professional":
                score_tally += 1.0
            elif ev_level == "Resume-Mentioned" or status == "Academic/Partial":
                score_tally += 0.5

        eff_tally = calibrated_tally if calibrated_tally > 0 else score_tally
        eval_score = round((eff_tally / len(must_have)) * 100, 2)

        # Build Score Explanation & Instant AI Verdict (0 extra tokens)
        score_explanation = build_score_explanation(
            [SkillEvaluation(
                skill=e["skill"], evidence_level=e["evidence_level"], calibrated_score=e["calibrated_score"],
                component_scores=e["component_scores"], status=e["status"], confidence_score=e["confidence_score"]
            ) for e in evaluations],
            len(must_have)
        )
        ai_verdict = generate_instant_verdict(
            jd_text,
            [e["skill"] for e in evaluations if e["evidence_level"] in ("Resume-Demonstrated", "Code-Verified")],
            [e["skill"] for e in evaluations if e["evidence_level"] == "Resume-Mentioned"],
            [e["skill"] for e in evaluations if e["evidence_level"] == "Not Found"],
            [s["skill"] for s in must_have]
        )

        result_data = {
            "resume_id": r_id,
            "filename": resume_item["filename"],
            "role_key": role_key,
            "category": resume_item["meta"]["category"],
            "relevance_tier": resume_item["meta"]["relevance_tier"],
            "is_top_10": resume_item["meta"]["is_top_10"],
            "evaluation_score": eval_score,
            "evaluations": evaluations,
            "score_explanation": score_explanation.model_dump() if hasattr(score_explanation, "model_dump") else (score_explanation.dict() if hasattr(score_explanation, "dict") else str(score_explanation)),
            "ai_verdict": ai_verdict,
            "timestamp": datetime.now().isoformat()
        }

        with open(ckpt_path, "w", encoding="utf-8") as f:
            json.dump(result_data, f, indent=2)

        return result_data

    async def evaluate_single_resume_stage2(self, resume_item: Dict[str, Any], stage1_record: Dict[str, Any], role_key: str) -> Dict[str, Any]:
        """Combines Stage 1 + Stage 2 with synthetic GitHub / HTTP payload injection."""
        global _CURRENT_SYNTHETIC_PAYLOAD
        r_id = resume_item["resume_id"]
        ckpt_path = os.path.join(PHASE2_DIR, f"{r_id}.json")
        if os.path.exists(ckpt_path):
            with open(ckpt_path, "r", encoding="utf-8") as f:
                return json.load(f)

        payload = self.payloads[r_id]
        _CURRENT_SYNTHETIC_PAYLOAD = payload

        must_have = self.canonical_skills[role_key]
        jd_text = self.jds[role_key]
        raw_text = resume_item["raw_text"]
        file_bytes = resume_item["file_bytes"]

        # Run Stage-2 Signals (with synthetic payload monkeypatch active)
        stage2_signals = await self.orchestrator.run_stage2_signals(
            resume_text=raw_text,
            file_bytes=file_bytes,
            filename=resume_item["filename"],
            explicit_email=resume_item["meta"]["email"],
            explicit_github=resume_item["meta"].get("github"),
            consent_given=True,
            job_description=jd_text,
            must_have_skills=must_have
        )

        # Match skills against repositories
        github_data = payload.get("github_analysis")
        per_skill_code_ev, code_ev_score, ev_gaps = match_skills_against_repos(
            must_have_skills=must_have,
            github_data=github_data
        )

        # Upgrade evaluations with Code-Verified status
        stage2_evals = []
        for idx, s1_ev in enumerate(stage1_record["evaluations"]):
            ev_copy = dict(s1_ev)
            if idx < len(per_skill_code_ev):
                c_status = per_skill_code_ev[idx]["code_evidence_status"]
                ev_copy["code_evidence_status"] = c_status
                ev_copy["repo_evidence_snippet"] = per_skill_code_ev[idx]["repo_evidence_snippet"]

                # If demonstrated on resume and verified in code -> upgrade to Code-Verified
                if ev_copy["evidence_level"] in ("Resume-Demonstrated", "Verified Professional") and c_status == "CODE_VERIFIED":
                    ev_copy["evidence_level"] = "Code-Verified"
                    ev_copy["is_independently_verified"] = True
                    ev_copy["calibrated_score"] = min(1.0, ev_copy["calibrated_score"] + 0.10)

            stage2_evals.append(ev_copy)

        # Combined Stage 1 + 2 evaluation score
        calibrated_tally = sum(e["calibrated_score"] for e in stage2_evals)
        final_stage2_score = round((calibrated_tally / len(must_have)) * 100, 2)

        # Determine Recruiter Decision based on trust and evidence
        trust_score = stage2_signals.get("trust_score", 60)
        trust_level = stage2_signals.get("trust_level", "MODERATE_TRUST")
        risk_flags = stage2_signals.get("risk_flags", [])

        if any("0/50 recent commits match candidate email" in rf or "authorship" in rf.lower() for rf in risk_flags):
            recruiter_decision = "REJECT_FRAUD_RISK"
        elif any("Declared" in rf and "0 AST imports" in rf for rf in risk_flags):
            recruiter_decision = "TECHNICAL_GRILL_REQUIRED"
        elif final_stage2_score >= 80 and trust_score >= 80 and code_ev_score >= 70:
            recruiter_decision = "FAST_TRACK_HIRE"
        elif final_stage2_score < 45 or trust_score < 40:
            recruiter_decision = "REJECT_FRAUD_RISK" if trust_score < 40 else "REJECT_MISMATCH"
        else:
            recruiter_decision = "TECHNICAL_GRILL_REQUIRED"

        # Generate targeted grill questions for unverified gaps or failed checks
        grill_kit = []
        if ev_gaps:
            for gap in ev_gaps[:3]:
                grill_kit.append({
                    "targeted_area": f"{gap} Deep Architecture",
                    "context_probe": f"Candidate demonstrated {gap} on resume but no code evidence was identified in repositories.",
                    "interview_question": f"Can you walk us through how you handled production failure modes, concurrency, and scaling when deploying {gap}?",
                    "ideal_response_criteria": f"Concrete description of architectural trade-offs and monitoring for {gap}.",
                    "red_flag_warning_signals": "Generic tutorial answers without production specifics."
                })
        elif not grill_kit:
            grill_kit.append({
                "targeted_area": f"{must_have[0]['skill']} Architecture",
                "context_probe": "General deep-dive on core platform architecture.",
                "interview_question": f"Walk us through your most complex production bug in {must_have[0]['skill']}.",
                "ideal_response_criteria": "Clear root cause identification and blameless remediation.",
                "red_flag_warning_signals": "Defensiveness or lack of technical depth."
            })

        # Generate 5-sentence proof brief
        repos_summary = f"{github_data.get('public_repos_count', 0)} public repositories" if github_data.get("found") else "external verified sources"
        proof_brief = (
            f"Candidate profile was audited across {repos_summary} and public credentials. "
            f"Technical evidence verification established a Code Evidence Score of {code_ev_score}/100 across required competencies. "
            f"Independent forensic telemetry calculated a Trust Score of {trust_score}/100 with status {trust_level}. "
            f"Identified evidence gaps were flagged in {len(ev_gaps)} required areas for targeted technical probe. "
            f"Recommended recruiter action is {recruiter_decision} based on composite Stage-1 and Stage-2 findings."
        )

        stage2_record = {
            "resume_id": r_id,
            "filename": resume_item["filename"],
            "role_key": role_key,
            "category": resume_item["meta"]["category"],
            "relevance_tier": resume_item["meta"]["relevance_tier"],
            "is_top_10": resume_item["meta"]["is_top_10"],
            "stage1_evaluation_score": stage1_record["evaluation_score"],
            "stage2_evaluation_score": final_stage2_score,
            "trust_score": trust_score,
            "trust_level": trust_level,
            "code_evidence_score": code_ev_score,
            "recruiter_decision": recruiter_decision,
            "evaluations": stage2_evals,
            "evidence_gaps": ev_gaps,
            "proof_brief": proof_brief,
            "technical_grill_kit": grill_kit,
            "checks": stage2_signals.get("checks", {}),
            "timestamp": datetime.now().isoformat()
        }

        with open(ckpt_path, "w", encoding="utf-8") as f:
            json.dump(stage2_record, f, indent=2)

        return stage2_record

def main():
    parser = argparse.ArgumentParser(description="Kriu-Bench-v0.3 Local Runner")
    parser.add_argument("--phase", type=str, choices=["1", "2", "all"], default="all", help="Evaluation phase")
    parser.add_argument("--roles", type=str, default="BE", help="Comma-separated roles to evaluate (default 'BE' for first job description only)")
    parser.add_argument("--limit-per-role", type=int, default=100, help="Max candidates per role to evaluate")
    parser.add_argument("--filter-ratio", type=float, default=0.50, help="Cutoff fraction for coarse filter (default 0.50 for Top 50%)")
    parser.add_argument("--all-resumes", action="store_true", help="Evaluate all 100 resumes per role instead of just the top-filtered picks")
    parser.add_argument("--top-filter-only", action="store_true", help="Run only the coarse filter evaluation (0 Groq tokens)")
    args = parser.parse_args()

    active_roles = [r.strip() for r in args.roles.split(",") if r.strip()]
    runner = BenchmarkRunner()

    print("===============================================================")
    print(f"Kriu-Bench-v0.3 Local In-Process Runner (Roles: {active_roles}, Phase: {args.phase}, Filter: Top {int(args.filter_ratio*100)}%)")
    print("===============================================================")

    # Step 1: Stage-1 Coarse Filter Funnel (100% Local Embeddings, 0 Groq tokens)
    filter_funnel_path = os.path.join(RESULTS_DIR, "stage1_filter_funnel.json")
    filter_results = {}
    if os.path.exists(filter_funnel_path):
        try:
            with open(filter_funnel_path, "r", encoding="utf-8") as f:
                filter_results = json.load(f)
        except Exception:
            filter_results = {}

    parsed_resumes_by_role = {}
    top_candidates_by_role = {}

    for role_key in active_roles:
        resumes = runner.parse_all_resumes_for_role(role_key)
        parsed_resumes_by_role[role_key] = resumes
        filter_stats = runner.run_stage1_coarse_filter(role_key, resumes, filter_ratio=args.filter_ratio)
        filter_results[role_key] = filter_stats

        # Collect top filtered resumes
        top_ids = [item["resume_id"] for item in filter_stats["top_picks_metadata"]]
        resume_map = {r["resume_id"]: r for r in resumes}
        top_candidates_by_role[role_key] = [resume_map[r_id] for r_id in top_ids if r_id in resume_map]

    # Save coarse filter results
    with open(filter_funnel_path, "w", encoding="utf-8") as f:
        json.dump(filter_results, f, indent=2)

    if args.top_filter_only:
        print(f"\nStage-1 Top-{int(args.filter_ratio*100)}% Filter Evaluation Complete (Results saved to results/stage1_filter_funnel.json)")
        return

    # Choose candidate set
    eval_candidates = parsed_resumes_by_role if args.all_resumes else top_candidates_by_role

    # Step 2: Phase 1 LLM Evidence Judge Evaluation
    if args.phase in ("1", "all"):
        print(f"\n---> Running Phase 1 (Stage-1 LLM Evidence Judge) on {'all' if args.all_resumes else f'Top {int(args.filter_ratio*100)}%'} candidates for {active_roles}...")
        for role_key in active_roles:
            resumes = eval_candidates[role_key][:args.limit_per_role]
            for idx, r_item in enumerate(resumes):
                r_id = r_item["resume_id"]
                ckpt_file = os.path.join(PHASE1_DIR, f"{r_id}.json")
                if os.path.exists(ckpt_file):
                    continue
                try:
                    runner.evaluate_single_resume_stage1(r_item, role_key)
                    logger.info(f"Phase 1 [{role_key}] {idx+1}/{len(resumes)} evaluated: {r_id}")
                except RuntimeError as re:
                    if str(re) == "GROQ_DAILY_TOKEN_LIMIT_REACHED":
                        logger.warning("Groq daily token limit reached. Halting Phase 1 gracefully.")
                        break
                    raise

    # Step 3: Phase 2 Stage-1 + Stage-2 Evaluation (with Synthetic Payloads)
    if args.phase in ("2", "all"):
        print(f"\n---> Running Phase 2 (Stage-1 + Stage-2 Combined with Synthetic Payloads) for {active_roles}...")
        for role_key in active_roles:
            resumes = eval_candidates[role_key][:args.limit_per_role]
            for idx, r_item in enumerate(resumes):
                r_id = r_item["resume_id"]
                p1_file = os.path.join(PHASE1_DIR, f"{r_id}.json")
                if not os.path.exists(p1_file):
                    # Need Phase 1 evaluated first
                    runner.evaluate_single_resume_stage1(r_item, role_key)

                with open(p1_file, "r", encoding="utf-8") as f:
                    s1_record = json.load(f)

                ckpt_file = os.path.join(PHASE2_DIR, f"{r_id}.json")
                if os.path.exists(ckpt_file):
                    continue

                asyncio.run(runner.evaluate_single_resume_stage2(r_item, s1_record, role_key))
                logger.info(f"Phase 2 [{role_key}] {idx+1}/{len(resumes)} evaluated: {r_id}")

    print("\n===============================================================")
    print("Local Benchmark Evaluation Complete!")
    print(f"Phase 1 checkpoints: {len(os.listdir(PHASE1_DIR))} files in {PHASE1_DIR}")
    print(f"Phase 2 checkpoints: {len(os.listdir(PHASE2_DIR))} files in {PHASE2_DIR}")
    print("===============================================================")

if __name__ == "__main__":
    main()
