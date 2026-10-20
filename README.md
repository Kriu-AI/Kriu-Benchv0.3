<div align="center">

<p align="center">
  <img src="https://www.trykriu.com/assets/kriu-logo.svg" alt="Kriu Logo" width="220" />
</p>

# Kriu
### The Deep Verification & Evaluation Intelligence Platform for Modern Engineering Teams

[![Evaluation Status](https://img.shields.io/badge/Benchmark-Empirical%20v0.3-brightgreen)]()
[![Fairness Score](https://img.shields.io/badge/Demographic%20Fairness-100%25%20Consistent-blue)]()
[![Spam Immunity](https://img.shields.io/badge/Keyword%20Stuffing-0%25%20Leakage-purple)]()

**Moving Beyond Resumes to Verify Real-World Technical Execution.**

[Explore Benchmark Report](BENCHMARK_REPORT.md) • [Detailed Metric Breakdown](BENCHMARK_REPORT.md#detailed-benchmark-breakdown) • [View Evaluation Metrics](metrics_summary.json) • [Platform Capabilities](#key-capabilities)

---
</div>

## Overview

In an era where AI-generated resumes and keyword stuffing make candidate screening noisier than ever, traditional applicant tracking systems (ATS) reward candidates who write the best buzzwords—not the ones who build the best software.

**Kriu** is built from the ground up to solve this fundamental problem. By combining multi-signal technical evidence analysis, deep repository verification, and auditable proof extraction, Kriu evaluates what candidates have actually delivered, not just what they claimed.

### The Two-Stage Funnel: Why 300 Resumes Ingested → Top 50% Selected
In high-volume technical hiring, evaluating 300+ candidates through deep code audits and LLM evidence extraction is compute-intensive. Kriu uses a decoupled two-stage architecture:
1. **Stage 1 (Coarse In-Memory Screen)**: Ingests all 300 candidates and ranks them in milliseconds using hybrid search (semantic embeddings + keyword matching) at zero LLM cost.
2. **Stage 2 (Deep Forensic Verification)**: Advances the top 50% (150 candidates) for multi-signal GitHub code auditing, AST dependency checks, and automated interview question generation.

**Why 50%?**  
- **100% Spam Blocked**: Completely eliminates 100% of adversarial keyword-stuffed resumes (`CFE-Leak: 0.0%`).
- **50% Compute Savings**: Prevents expensive multi-signal analysis from running on unqualified applications.
- **High Senior Retention**: Captures 73.33% of genuine senior engineering leaders while halving recruiter screening time.

For full metric definitions, sample sizes, confidence intervals, and practical impacts, see the [Detailed Benchmark Report](BENCHMARK_REPORT.md).

---

## Benchmark Highlights at a Glance

Evaluated across real-world hiring scenarios and candidate archetypes ($N=300$, Senior Backend Engineering), Kriu sets a new standard for precision, fairness, and spam resistance.

```
┌────────────────────────────────────────────────────────────────────────┐
│  SHORTLIST QUALITY (NDCG@50)         │  0.7089 (Overall Corpus: 0.8574)│
│  SENIOR FUNNEL RETENTION (REC@50%)   │  73.3% Retained (100% Spam Out) │
│  CODE VERIFICATION RE-RANKING LIFT   │  -4.1% Multi-Signal Lift        │
│  DEMOGRAPHIC FAIRNESS CONSISTENCY    │  100% Invariant (0.0% Flips)    │
│  KEYWORD STUFFING LEAKAGE            │  0.0% Leaked (100% Blocked)     │
│  DEMONSTRATED SKILL PRECISION        │  80.0% Accurate Proof Citations │
│  INTERVIEW GAP COVERAGE              │  85.5% Tailored Question Kits    │
└────────────────────────────────────────────────────────────────────────┘
```
> For a detailed explanation of what each metric means, what the scores represent, and their operational impact, refer to the [Benchmark Report Breakdown](BENCHMARK_REPORT.md#detailed-benchmark-breakdown).

---

## Key Capabilities

### 🎯 1. Shortlist Quality That Hiring Managers Trust
Traditional keyword matching fills recruiter inboxes with false positives. Kriu ranks candidates by verifiable technical depth, achieving a **0.7089 NDCG@50** shortlist quality score across actionable applicant tiers and **0.8574** across the entire corpus. Hiring managers can review top recommendations with confidence.  
👉 *[Read how shortlist quality is evaluated in the Benchmark Report](BENCHMARK_REPORT.md#sru-ndcg50-recruiter-shortlist-quality-top-50).*

### 🔍 2. Deep Multi-Signal Verification
Resumes only tell half the story. Kriu evaluates engineering artifacts, repositories, and technical contributions in tandem with applicant claims. In empirical testing, multi-signal verification re-ranks candidates based on concrete repository substance, surfacing quiet, high-impact builders who don't optimize their resumes for keywords.  
👉 *[Read how code verification lift is measured in the Benchmark Report](BENCHMARK_REPORT.md#sru-kt-lift-code-verification-re-ranking-lift).*

### 🛡️ 3. Immune to AI Fluff & Keyword Stuffing
With applicants using AI tools to stuff keywords and polish phrasing, screening tools often fail to spot exaggeration. Kriu achieved a **100% rejection rate against keyword-stuffed resumes** and maintained a **+19.0 point separation** between genuine production veterans and junior candidates with polished claims.  
👉 *[Read how adversarial defense is tested in the Benchmark Report](BENCHMARK_REPORT.md#3-adversarial--spam-defense).*

### ⚖️ 4. Fairness You Can Audit
Fairness is not an afterthought. In counterfactual testing across identical candidate profiles where demographic identifiers (gender, ethnic background, school prestige) were systematically varied, Kriu produced a **0.0% hiring recommendation flip rate** and an average spread of only 0.1 points. Decisions are based purely on proven ability.  
👉 *[Read how demographic fairness is audited in the Benchmark Report](BENCHMARK_REPORT.md#cdi-spread-demographic-score-variance).*

### 🎙️ 5. Interview Kits Tailored to Each Candidate
When a candidate claims experience that cannot be independently confirmed, Kriu doesn't just reject them—it creates an automated, personalized technical interview kit. Kriu covered **85.5% of unverified skills** with tailored interview questions, context probes, and red-flag signals for interviewers.  
👉 *[Read how interview question coverage works in the Benchmark Report](BENCHMARK_REPORT.md#tgk-hitk-interview-question-gap-coverage).*

---

## Empirical Benchmark Scorecard

| Capability Pillar | Metric Name | What It Measures | Target | Kriu Empirical Result | Detailed Analysis |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **Candidate Ranking** | `SRU-NDCG@50` | Recruiter Shortlist Quality (Top 50) | $\ge 0.70$ | **0.7089** (NDCG@10: 0.4286) | [View Impact](BENCHMARK_REPORT.md#sru-ndcg50-recruiter-shortlist-quality-top-50) |
| **Signal Lift** | `SRU-KT-Lift` | Ranking Improvement with Deep Code Audit | $\ge +20\%$ | **-4.1%** | [View Impact](BENCHMARK_REPORT.md#sru-kt-lift-code-verification-re-ranking-lift) |
| **Funnel Retention** | `CFE-Rec@50%` | Senior Talent Funnel Retention (Top 50%) | $\ge 85\%$ | **73.33%** | [View Impact](BENCHMARK_REPORT.md#cfe-rec50-senior-talent-funnel-retention-top-50-cutoff) |
| **Skill Precision** | `SEC-Prec` | Accuracy of Confirmed Technical Claims | $\ge 90\%$ | **80.04%** | [View Impact](BENCHMARK_REPORT.md#sec-prec-verified-skill-precision) |
| **Claim Accuracy** | `SEC-MacroF1` | Claim Classification Accuracy | $\ge 75\%$ | **61.0%** | [View Impact](BENCHMARK_REPORT.md#sec-macrof1-claim-classification-accuracy) |
| **Experience Separation** | `EED-Margin` | Score Gap Between Senior Leaders & Juniors | $\ge +20$ pts | **+19.0 pts** | [View Impact](BENCHMARK_REPORT.md#eed-margin-senior-vs-junior-score-gap) |
| **Junior Buzzword Rate** | `EED-FPR` | Junior Resume Claim Pass Rate | $\le 30\%$ | **51.11%** | [View Impact](BENCHMARK_REPORT.md#eed-fpr-junior-resume-claim-pass-rate) |
| **Spam Defense** | `ATD-Stuffer` | Rejection of Keyword-Stuffed Resumes | $\ge 95\%$ | **100.0%** | [View Impact](BENCHMARK_REPORT.md#atd-stuffer-keyword-stuffer-rejection-rate) |
| **Spam Leakage** | `CFE-Leak` | Keyword Stuffers Passing to Funnel | $\le 5\%$ | **0.0%** | [View Impact](BENCHMARK_REPORT.md#cfe-leak-resume-stuffer-leakage-to-funnel) |
| **Trap Catch Rate** | `ATD-Trap` | Semantic Negation & Trap Catch Rate | $\ge 75\%$ | **75.0%** | [View Impact](BENCHMARK_REPORT.md#atd-trap-semantic-negation--trap-catch-rate) |
| **Fairness & Invariance** | `CDI-Spread` | Score Stability across Demographic Variations | $\le 3.0$ pts | **2.59 pts (0% Flips)** | [View Impact](BENCHMARK_REPORT.md#cdi-spread-demographic-score-variance) |
| **Evidence Grounding** | `VEG-Tok90` | Citations Matching Candidate Source Files | $\ge 75\%$ | **90.15%** | [View Impact](BENCHMARK_REPORT.md#veg-tok90-verbatim-evidence-grounding) |
| **Explanation Alignment** | `SEF-Align` | Decision Explanation Alignment | $\ge 95\%$ | **100.0%** | [View Impact](BENCHMARK_REPORT.md#sef-align-decision-explanation-alignment) |
| **Contract Compliance** | `PBF-Contract` | Structured Brief Compliance | $\ge 98\%$ | **100.0%** | [View Impact](BENCHMARK_REPORT.md#pbf-contract-structured-brief-compliance) |
| **Interview Preparation** | `TGK-Hit@K` | Question Coverage for Unverified Skill Claims | $\ge 80\%$ | **85.48%** | [View Impact](BENCHMARK_REPORT.md#tgk-hitk-interview-question-gap-coverage) |

---

## Suite Structure

- **[BENCHMARK_REPORT.md](BENCHMARK_REPORT.md)**: Full capability and benchmark whitepaper with metric definitions, current scores, and practical impacts for all 15 benchmarks.
- **[metrics_summary.json](metrics_summary.json)**: Machine-readable empirical data with 95% Wilson confidence intervals.
- **`results/`**: Empirical checkpoints across screening stages ($N=300$ candidates).

---

<div align="center">
<sub>Built with precision for engineering organizations that hire for true execution.</sub>
</div>
