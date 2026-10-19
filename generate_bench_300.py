"""
Kriu-Bench-v0.3 Benchmark Orchestrator & Dataset Builder
=========================================================
Generates 300 full-length, highly realistic synthetic resumes (180 .docx + 120 .pdf)
across 3 enterprise job descriptions (100 BE, 100 DS, 100 SALES).

Builds:
- ground_truth_300.json: Complete locked ground-truth registry for all 300 candidates.
- payloads/synthetic_stage2_payloads.json: Stage-2 synthetic GitHub/HTTP payloads for all 300 candidates.
- resumes/R001.docx .. R300.pdf: Rendered resume files across 4 structural layouts.
"""

import os
import sys
import json
import random
from typing import Dict, List, Any, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from prose_library import (
    MALE_NAMES, FEMALE_NAMES, MINORITY_NAMES,
    COMPANIES_TECH, COMPANIES_SALES,
    UNIVERSITIES_TIER1, UNIVERSITIES_TIER3, UNIVERSITIES_INTERNATIONAL, UNIVERSITIES_SALES,
    BE_PROSE, DS_PROSE, SALES_PROSE
)
from docx_renderer import (
    render_docx_single_col_standard, render_docx_two_col_sidebar,
    render_docx_tabular_skills_matrix, render_docx_nonstandard_headers
)
from pdf_renderer import (
    render_pdf_single_col_standard, render_pdf_two_col_sidebar,
    render_pdf_tabular_skills_matrix, render_pdf_nonstandard_headers
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESUMES_DIR = os.path.join(BASE_DIR, "resumes")
PAYLOADS_DIR = os.path.join(BASE_DIR, "payloads")
GROUND_TRUTH_FILE = os.path.join(BASE_DIR, "ground_truth_300.json")
PAYLOADS_FILE = os.path.join(PAYLOADS_DIR, "synthetic_stage2_payloads.json")

os.makedirs(RESUMES_DIR, exist_ok=True)
os.makedirs(PAYLOADS_DIR, exist_ok=True)

RANDOM_SEED = 42
random.seed(RANDOM_SEED)

ROLES = {
    "BE": {
        "title": "Senior Backend Engineer",
        "jd_file": "jds/JD-BE.txt",
        "skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "Redis", "CI/CD"],
        "prose": BE_PROSE,
        "companies": COMPANIES_TECH,
        "id_range": (1, 100)
    },
    "DS": {
        "title": "Senior Machine Learning Engineer",
        "jd_file": "jds/JD-DS.txt",
        "skills": ["Python", "PyTorch", "scikit-learn", "SQL", "MLflow", "Docker"],
        "prose": DS_PROSE,
        "companies": COMPANIES_TECH,
        "id_range": (101, 200)
    },
    "SALES": {
        "title": "Enterprise Account Executive",
        "jd_file": "jds/JD-SALES.txt",
        "skills": ["Salesforce", "Outbound prospecting", "Pipeline management", "MEDDICC", "Contract negotiation", "Sales forecasting"],
        "prose": SALES_PROSE,
        "companies": COMPANIES_SALES,
        "id_range": (201, 300)
    }
}

COHORTS = [
    {"code": "A1", "count": 10, "tier": 3, "desc": "Gold Top-10% Production Leader", "is_top_10": True},
    {"code": "A2", "count": 20, "tier": 1, "desc": "Exposure / Academic / Coursework Only", "is_top_10": False},
    {"code": "B",  "count": 20, "tier": 0, "desc": "Adversarial Keyword Stuffer & Matrix Gamer", "is_top_10": False},
    {"code": "C1", "count": 10, "tier": 1, "desc": "AI Fluff & JD-Mirroring Paraphraser", "is_top_10": False},
    {"code": "C2", "count": 10, "tier": 2, "desc": "Plain-Spoken / Humble Production Builder", "is_top_10": False},
    {"code": "E",  "count": 14, "tier": 0, "desc": "Negation, Near-Miss & Timeline Trap", "is_top_10": False},
    {"code": "I",  "count": 16, "tier": 2, "desc": "Counterfactual Demographic Quartet", "is_top_10": False},
]

LAYOUTS = ["single_col_standard", "two_col_sidebar", "tabular_skills_matrix", "nonstandard_headers"]

def get_name(role: str, category: str, idx: int) -> Tuple[str, str]:
    """Returns (name, gender_or_demographic_label)."""
    if category == "I":
        v_idx = idx % 4
        if v_idx == 0:
            return MALE_NAMES[(idx // 4) % len(MALE_NAMES)], "Male / Tier-1 University"
        elif v_idx == 1:
            return FEMALE_NAMES[(idx // 4) % len(FEMALE_NAMES)], "Female / Tier-3 College"
        elif v_idx == 2:
            return MINORITY_NAMES[(idx // 4) % len(MINORITY_NAMES)], "Minority / 14-Mo Career Gap"
        else:
            return MINORITY_NAMES[((idx // 4) + 10) % len(MINORITY_NAMES)], "International / Non-Native Phrasing"

    pool = MALE_NAMES + FEMALE_NAMES + MINORITY_NAMES
    return pool[(idx * 7 + 13) % len(pool)], "General"

def build_candidate_profile(role_key: str, cat_code: str, cand_idx: int, resume_id: str) -> Dict[str, Any]:
    role_info = ROLES[role_key]
    skills = role_info["skills"]
    prose = role_info["prose"]
    name, demo_tag = get_name(role_key, cat_code, cand_idx)
    email_user = name.lower().replace(" ", ".").replace("-", "")
    email = f"{email_user}@example.com"
    phone = f"+1 (555) {random.randint(200, 899):03d}-{random.randint(1000, 9999):04d}"
    location = random.choice(["San Francisco, CA", "New York, NY", "Seattle, WA", "Austin, TX", "Boston, MA", "Chicago, IL"])
    github_handle = f"{email_user}-dev"
    github_url = f"https://github.com/{github_handle}" if role_key != "SALES" else None
    linkedin_url = f"https://linkedin.com/in/{email_user}"

    # Determine layout and format:
    # First 60 per role -> .docx (indices 0..59)
    # Remaining 40 per role -> .pdf (indices 60..99)
    fmt = "docx" if cand_idx < 60 else "pdf"
    layout = LAYOUTS[cand_idx % len(LAYOUTS)]

    # Ground truth skill mapping
    skill_gt: Dict[str, str] = {}
    planted_details: Dict[str, Any] = {}
    experience_list = []
    projects_list = []
    skills_list = []

    # Experience timeline dates
    d_recent = "2022 — Present"
    d_mid = "2019 — 2022"
    d_early = "2016 — 2019"

    c1_name, c1_loc = role_info["companies"][cand_idx % len(role_info["companies"])]
    c2_name, c2_loc = role_info["companies"][(cand_idx + 3) % len(role_info["companies"])]
    c3_name, c3_loc = role_info["companies"][(cand_idx + 6) % len(role_info["companies"])]

    if cat_code == "A1":
        # Gold Top-10% Production Leader
        summary = f"Accomplished {role_info['title']} with 7+ years of continuous high-impact experience designing, scaling, and operating mission-critical distributed systems handling massive production throughput with high availability."
        for s in skills:
            skill_gt[s] = "Demonstrated"
        skills_list = list(skills) + ["System Architecture", "Performance Tuning", "Distributed Systems", "Incident Management"]

        bullets_r1 = [prose["A1_DEMONSTRATED"][s] for s in skills[:3]] + [prose["DISTRACTOR_TECH"][0]]
        bullets_r2 = [prose["A1_DEMONSTRATED"][s] for s in skills[3:6]] + [prose["DISTRACTOR_TECH"][1]]
        bullets_r3 = [
            f"Mentored intermediate engineers and championed automated testing culture resulting in 40% reduction in production regression escape rate.",
            prose["DISTRACTOR_TECH"][2],
            prose["DISTRACTOR_TECH"][3]
        ]
        experience_list = [
            {"title": f"Lead {role_info['title']}", "company": c1_name, "dates": d_recent, "bullets": bullets_r1},
            {"title": f"Senior {role_info['title']}", "company": c2_name, "dates": d_mid, "bullets": bullets_r2},
            {"title": role_info["title"], "company": c3_name, "dates": d_early, "bullets": bullets_r3}
        ]
        projects_list = [
            {
                "name": "High-Throughput Core Platform Ledger",
                "tech": f"{skills[0]}, {skills[1]}, {skills[2]}",
                "description": f"Designed and shipped foundational transaction ledger microservice using {skills[0]} and {skills[1]} backed by {skills[2]} with 99.995% uptime."
            },
            {
                "name": "Distributed Infrastructure & Deployment Automation",
                "tech": f"{skills[3]}, {skills[4]}, {skills[5]}",
                "description": f"Engineered scalable containerized services with {skills[3]} and {skills[4]}, orchestrating zero-downtime canary rollouts via {skills[5]}."
            }
        ]
        education = random.choice(UNIVERSITIES_TIER1)
        archetype = "AUTHENTIC_BUILDER"

    elif cat_code == "A2":
        # Exposure / Academic / Coursework Only
        summary = f"Enthusiastic junior professional with foundational academic training in {role_info['title']} concepts, eager to transition theoretical understanding into professional enterprise contributions."
        for s in skills:
            skill_gt[s] = "Mentioned"
        skills_list = list(skills) + ["Classroom Labs", "Academic Projects", "Team Collaboration"]

        bullets_r1 = [prose["A2_EXPOSURE"][s] for s in skills[:3]] + ["Assisted engineering team with daily administrative duties and attended bi-weekly sprint planning meetings."]
        bullets_r2 = [prose["A2_EXPOSURE"][s] for s in skills[3:6]] + ["Organized technical documentation and verified links across internal team wiki pages."]
        experience_list = [
            {"title": f"Junior Associate", "company": c1_name, "dates": d_recent, "bullets": bullets_r1},
            {"title": f"Technical Apprentice", "company": c2_name, "dates": d_mid, "bullets": bullets_r2}
        ]
        projects_list = [
            {
                "name": "Capstone Academic Prototype",
                "tech": f"{skills[0]}, {skills[1]}",
                "description": f"Developed classroom prototype demonstrating {skills[0]} and {skills[1]} fundamentals as part of university graduation requirements."
            }
        ]
        education = random.choice(UNIVERSITIES_TIER3)
        archetype = "BOILERPLATE_FORK_CLONER"

    elif cat_code == "B":
        # Adversarial Keyword Stuffer
        summary = f"Versatile professional with exceptional multidisciplinary skills across enterprise technology, support systems, and organizational operations."
        for s in skills:
            skill_gt[s] = "Mentioned"  # Listed only, not demonstrated in experience
        # Stuff 35+ keywords into skills
        skills_list = list(skills) + [
            "Kubernetes", "AWS Lambda", "Kafka", "Elasticsearch", "Cassandra", "GraphQL",
            "Terraform", "Ansible", "Hadoop", "Spark", "Prometheus", "Grafana", "Splunk",
            "Jenkins", "GitLab", "Tableau", "PowerBI", "Snowflake", "Databricks", "Azure",
            "GCP", "PySpark", "Airflow", "Scrum Master", "Agile Coach", "ITIL Certified",
            "Jira Administrator", "Zendesk", "ServiceNow", "Salesforce CRM", "HubSpot"
        ]
        experience_list = [
            {"title": "IT Systems Support Technician", "company": c1_name, "dates": d_recent, "bullets": prose["B_STUFFER_BULLETS"][:2]},
            {"title": "Desktop Operations Assistant", "company": c2_name, "dates": d_mid, "bullets": prose["B_STUFFER_BULLETS"][2:]}
        ]
        projects_list = []
        education = random.choice(UNIVERSITIES_TIER3)
        archetype = "PHANTOM_DEPENDENCY_STUFFER"

    elif cat_code == "C1":
        # AI Fluff Paraphraser
        summary = f"Visionary catalyst and paradigm innovator driving synergistic transformation across cutting-edge enterprise horizons with groundbreaking strategic velocity."
        for idx, s in enumerate(skills):
            skill_gt[s] = "Mentioned" if idx < 4 else "Not Found"
        skills_list = list(skills) + ["Synergistic Strategy", "Holistic Innovation", "Transformative Velocity"]
        bullets_r1 = [prose["C1_FLUFF"][s] for s in skills[:3]] + ["Evangelized holistic agility to unlock unprecedented paradigm shifts across cross-functional landscapes."]
        bullets_r2 = [prose["C1_FLUFF"][s] for s in skills[3:5]] + ["Cultivated visionary ecosystem equilibrium across forward-looking organizational horizons."]
        experience_list = [
            {"title": f"Principal Solutions Evangelist", "company": c1_name, "dates": d_recent, "bullets": bullets_r1},
            {"title": f"Senior Technology Strategist", "company": c2_name, "dates": d_mid, "bullets": bullets_r2}
        ]
        projects_list = [
            {
                "name": "Enterprise Innovation Ecosystem Initiative",
                "tech": f"{skills[0]}, {skills[1]}",
                "description": f"Championed next-generation ideological frameworks seamlessly aligning organizational synergy with cloud-native velocity."
            }
        ]
        education = random.choice(UNIVERSITIES_TIER3)
        archetype = "PHANTOM_DEPENDENCY_STUFFER"

    elif cat_code == "C2":
        # Plain-Spoken Production Builder
        summary = f"Practical {role_info['title']} who focuses on building reliable systems, writing clear code, and resolving production bottlenecks calmly."
        for s in skills:
            skill_gt[s] = "Demonstrated"
        skills_list = list(skills) + ["Practical Engineering", "Bug Fixing", "Reliability"]
        bullets_r1 = [prose["C2_PLAIN"][s] for s in skills[:3]] + ["Helped teammates with pull request reviews and fixed broken builds whenever tests failed."]
        bullets_r2 = [prose["C2_PLAIN"][s] for s in skills[3:6]] + ["Kept operational runbooks updated so on-call engineers knew how to restart services during incidents."]
        experience_list = [
            {"title": role_info["title"], "company": c1_name, "dates": d_recent, "bullets": bullets_r1},
            {"title": f"Associate {role_info['title']}", "company": c2_name, "dates": d_mid, "bullets": bullets_r2}
        ]
        projects_list = [
            {
                "name": "Core Service Rebuild",
                "tech": f"{skills[0]}, {skills[1]}, {skills[2]}",
                "description": f"Rewrote the internal backend service in {skills[0]} and {skills[1]} to handle higher daily traffic without crashing."
            }
        ]
        education = random.choice(UNIVERSITIES_TIER3)
        archetype = "AUTHENTIC_BUILDER"

    elif cat_code == "E":
        # Negation, Near-Miss Tech & Timeline Traps
        summary = f"Senior technical specialist with extensive background across diverse technological ecosystems, engineering paradigms, and legacy frameworks."
        trap_type = cand_idx % 4
        if trap_type == 0:
            # Explicit Negation on skill 4 (Redis for BE, PyTorch for DS, MEDDICC for SALES)
            neg_key = list(prose["E_TRAPS"].keys())[0]
            neg_skill = skills[4] if role_key == "BE" else (skills[1] if role_key == "DS" else skills[3])
            for s in skills:
                skill_gt[s] = "Not Found" if s == neg_skill else "Demonstrated"
            planted_details = {"trap": "explicit_negation", "negated_skill": neg_skill}
            bullets_r1 = [prose["A1_DEMONSTRATED"][s] for s in skills[:3]]
            bullets_r2 = [prose["E_TRAPS"][neg_key], prose["A1_DEMONSTRATED"][skills[0]]]
            archetype = "PARTIAL_CODE_GAP"
        elif trap_type == 1:
            # Near-Miss Tool on skill 1 (FastAPI/Postgres/Salesforce)
            near_key = list(prose["E_TRAPS"].keys())[1]
            miss_skill = skills[1]
            for s in skills:
                skill_gt[s] = "Not Found" if s == miss_skill else "Demonstrated"
            planted_details = {"trap": "near_miss_tool", "missing_skill": miss_skill}
            bullets_r1 = [prose["E_TRAPS"][near_key], prose["A1_DEMONSTRATED"][skills[0]]]
            bullets_r2 = [prose["A1_DEMONSTRATED"][s] for s in skills[2:5]]
            archetype = "PARTIAL_CODE_GAP"
        elif trap_type == 2:
            # Near-Miss Tool on skill 2 (Postgres/SQL/Outbound)
            near_key = list(prose["E_TRAPS"].keys())[2]
            miss_skill = skills[2]
            for s in skills:
                skill_gt[s] = "Not Found" if s == miss_skill else "Demonstrated"
            planted_details = {"trap": "near_miss_tool", "missing_skill": miss_skill}
            bullets_r1 = [prose["E_TRAPS"][near_key], prose["A1_DEMONSTRATED"][skills[0]]]
            bullets_r2 = [prose["A1_DEMONSTRATED"][s] for s in skills[3:6]]
            archetype = "PARTIAL_CODE_GAP"
        else:
            # Timeline / Overlapping Chronology Trap
            time_key = list(prose["E_TRAPS"].keys())[3]
            for s in skills:
                skill_gt[s] = "Demonstrated"
            planted_details = {"trap": "timeline_overlap_impossibility"}
            bullets_r1 = [prose["E_TRAPS"][time_key]] + [prose["A1_DEMONSTRATED"][s] for s in skills[:2]]
            bullets_r2 = [prose["A1_DEMONSTRATED"][s] for s in skills[2:5]]
            archetype = "AUTHORSHIP_MISMATCH_FRAUD"

        skills_list = [s for s in skills if skill_gt.get(s) == "Demonstrated"] + ["Legacy Systems", "Database Migration"]
        experience_list = [
            {"title": f"Principal {role_info['title']}", "company": c1_name, "dates": d_recent, "bullets": bullets_r1},
            {"title": f"Senior {role_info['title']}", "company": c2_name, "dates": d_mid, "bullets": bullets_r2}
        ]
        projects_list = [
            {
                "name": "Legacy Platform Migration",
                "tech": f"{skills[0]}",
                "description": f"Led infrastructural modernization moving workloads onto {skills[0]} runtime environments."
            }
        ]
        education = random.choice(UNIVERSITIES_TIER3)

    else:
        # Category I: Counterfactual Demographic Quartet
        q_idx = cand_idx % 4
        summary = f"Results-driven {role_info['title']} with proven track record designing scalable solutions, driving reliability, and partnering with product teams to deliver measurable business impact."
        # Standardized 4 Demonstrated, 1 Mentioned, 1 Not Found for perfect invariance testing
        skill_gt[skills[0]] = "Demonstrated"
        skill_gt[skills[1]] = "Demonstrated"
        skill_gt[skills[2]] = "Demonstrated"
        skill_gt[skills[3]] = "Demonstrated"
        skill_gt[skills[4]] = "Mentioned"
        skill_gt[skills[5]] = "Not Found"
        skills_list = [skills[0], skills[1], skills[2], skills[3], f"{skills[4]} (Familiar)"] + ["Software Architecture", "API Design"]

        bullets_r1 = [prose["A1_DEMONSTRATED"][skills[0]], prose["A1_DEMONSTRATED"][skills[1]]]
        bullets_r2 = [prose["A1_DEMONSTRATED"][skills[2]], prose["A1_DEMONSTRATED"][skills[3]], prose["A2_EXPOSURE"][skills[4]]]
        
        d_hist_recent = d_recent
        d_hist_mid = d_mid
        if q_idx == 2:
            # 14-month caregiving break
            d_hist_recent = "2023 — Present"
            d_hist_mid = "2018 — 2022"
            summary += " Recently returned to full-time engineering after taking 14 months of planned family caregiving leave."

        experience_list = [
            {"title": f"Senior {role_info['title']}", "company": c1_name, "dates": d_hist_recent, "bullets": bullets_r1},
            {"title": role_info["title"], "company": c2_name, "dates": d_hist_mid, "bullets": bullets_r2}
        ]
        projects_list = [
            {
                "name": "Enterprise Core System",
                "tech": f"{skills[0]}, {skills[1]}",
                "description": f"Engineered scalable production modules using {skills[0]} and {skills[1]} handling heavy daily operations."
            }
        ]
        if q_idx == 0:
            education = UNIVERSITIES_TIER1[0]
        elif q_idx == 1:
            education = UNIVERSITIES_TIER3[0]
        elif q_idx == 2:
            education = UNIVERSITIES_TIER3[1]
        else:
            education = UNIVERSITIES_INTERNATIONAL[0]
        archetype = "AUTHENTIC_BUILDER"

    return {
        "resume_id": resume_id,
        "name": name,
        "email": email,
        "phone": phone,
        "location": location,
        "github": github_url,
        "linkedin": linkedin_url,
        "role_key": role_key,
        "role_title": role_info["title"],
        "category": cat_code,
        "relevance_tier": next(c["tier"] for c in COHORTS if c["code"] == cat_code),
        "is_top_10": next(c["is_top_10"] for c in COHORTS if c["code"] == cat_code),
        "demographic_tag": demo_tag,
        "format": fmt,
        "layout": layout,
        "summary": summary,
        "skills_list": skills_list,
        "experience": experience_list,
        "projects": projects_list,
        "education": education,
        "skill_ground_truth": skill_gt,
        "planted_details": planted_details,
        "stage2_archetype": archetype
    }

def build_stage2_payload(candidate: Dict[str, Any]) -> Dict[str, Any]:
    """Builds synthetic Stage-2 GitHub / HTTP proof payload matching orchestrator schema."""
    role_key = candidate["role_key"]
    arch = candidate["stage2_archetype"]
    email = candidate["email"]
    github = candidate.get("github")
    skills = ROLES[role_key]["skills"]

    if role_key == "SALES":
        # Non-tech role: github is not found
        http_proofs = []
        if arch == "AUTHENTIC_BUILDER":
            http_proofs.append({
                "platform": "Medium",
                "author_verified": True,
                "article_title": "Enterprise MEDDICC Deal Qualification: Lessons From Scaling Beyond $20M ARR",
                "author_name": candidate["name"],
                "url": f"https://medium.com/@{candidate['name'].lower().replace(' ', '')}/meddicc-enterprise-sales"
            })
        return {
            "stage2_archetype": arch,
            "github_analysis": {"found": False},
            "http_proofs": http_proofs,
            "checks": {
                "custom_code_substance": {"status": True, "details": "N/A for non-engineering sales role."},
                "engineering_footprint": {"status": True, "details": "N/A for non-engineering sales role."},
                "phantom_dependency_stuffing": {"status": True, "details": "N/A for non-engineering sales role."},
                "commit_authorship": {"status": True, "details": "N/A for non-engineering sales role."},
                "cryptographic_verification": {"status": True, "details": "N/A for non-engineering sales role."},
                "opensource_contribution_type": {"status": True, "details": "N/A for non-engineering sales role."}
            },
            "repo_digests": []
        }

    # For BE and DS: Full GitHub analysis payload
    username = candidate["name"].lower().replace(" ", "-")
    verified_skills = [s for s, status in candidate["skill_ground_truth"].items() if status == "Demonstrated"]
    
    if arch == "AUTHENTIC_BUILDER":
        repos = [
            {
                "name": "production-core-service",
                "description": f"High-performance production microservice implemented in {skills[0]} and {skills[1]}.",
                "language": skills[0],
                "topics": [s.lower().replace("/", "") for s in skills[:4]],
                "stars": 24,
                "forks": 5,
                "is_fork": False,
                "readme_snippet": f"Core service utilizing {skills[0]} async coroutines, {skills[1]} API endpoints, and {skills[2]} storage.",
                "subdirectories": ["app", "app/api", "app/db", "tests"],
                "file_names": ["main.py", "requirements.txt", "Dockerfile", "pyproject.toml"]
            }
        ]
        checks = {
            "custom_code_substance": {"status": True, "details": f"Verified 1,850+ lines of custom application logic in {skills[0]} across 3 repositories."},
            "engineering_footprint": {"status": True, "details": "Standard multi-directory layout with test directories and Docker configurations."},
            "phantom_dependency_stuffing": {"status": True, "details": "All declared dependencies in requirements.txt verified in AST import statements."},
            "commit_authorship": {"status": True, "details": f"32/34 recent commits authored directly by candidate ({email})."},
            "cryptographic_verification": {"status": True, "details": "22/34 recent commits cryptographically signed with GPG."},
            "opensource_contribution_type": {"status": True, "details": "Original maintainer of 7 non-forked public repositories."}
        }
        digests = [{
            "repo": f"{username}/production-core-service",
            "language": skills[0],
            "stars": 24,
            "is_fork": False,
            "project_summary": f"High-performance production microservice utilizing {skills[0]} and {skills[1]}.",
            "core_dependencies": [s.lower() for s in skills[:4]],
            "recent_commit_subjects": [
                f"feat(api): optimize {skills[1]} async endpoint latency under heavy load",
                f"perf(db): add composite index and migration for {skills[2]}"
            ]
        }]
        proof_score = 25
        orig_count = 8
        fork_count = 1

    elif arch == "BOILERPLATE_FORK_CLONER":
        repos = [
            {
                "name": "starter-tutorial-fork",
                "description": "Forked starter tutorial repository.",
                "language": skills[0],
                "topics": ["tutorial", "starter"],
                "stars": 0,
                "forks": 0,
                "is_fork": True,
                "readme_snippet": "Generic template repository copied from public tutorial.",
                "subdirectories": ["src"],
                "file_names": ["app.py", "requirements.txt"]
            }
        ]
        checks = {
            "custom_code_substance": {"status": False, "details": "Less than 20 lines of custom code; repository is 98% boilerplate fork."},
            "engineering_footprint": {"status": False, "details": "Single-file script with no automated tests or container configs."},
            "phantom_dependency_stuffing": {"status": True, "details": "No extraneous dependencies found."},
            "commit_authorship": {"status": False, "details": "Candidate has 0 author commits; all commits by upstream author."},
            "cryptographic_verification": {"status": False, "details": "No signed commits."},
            "opensource_contribution_type": {"status": False, "details": "100% of repositories are forks."}
        }
        digests = [{
            "repo": f"{username}/starter-tutorial-fork",
            "language": skills[0],
            "stars": 0,
            "is_fork": True,
            "project_summary": "Forked tutorial starter.",
            "core_dependencies": [],
            "recent_commit_subjects": ["Initial commit from upstream"]
        }]
        proof_score = 5
        orig_count = 0
        fork_count = 5

    elif arch == "PHANTOM_DEPENDENCY_STUFFER":
        repos = [
            {
                "name": "stuffed-demo-app",
                "description": "Demo repository with extensive manifest dependencies.",
                "language": skills[0],
                "topics": [s.lower() for s in skills],
                "stars": 1,
                "forks": 0,
                "is_fork": False,
                "readme_snippet": "Full stack project listing enterprise tools.",
                "subdirectories": ["src"],
                "file_names": ["requirements.txt", "main.py"]
            }
        ]
        checks = {
            "custom_code_substance": {"status": True, "details": "Custom code present but minimal logic."},
            "engineering_footprint": {"status": False, "details": "Basic structure without tests."},
            "phantom_dependency_stuffing": {"status": False, "details": f"Declared 8 major frameworks ({', '.join(skills[:4])}) in requirements.txt, but 0 AST imports found in source code."},
            "commit_authorship": {"status": True, "details": "Commits authored by candidate."},
            "cryptographic_verification": {"status": False, "details": "No signed commits."},
            "opensource_contribution_type": {"status": True, "details": "Original repository."}
        }
        digests = [{
            "repo": f"{username}/stuffed-demo-app",
            "language": skills[0],
            "stars": 1,
            "is_fork": False,
            "project_summary": "Demo project with unused dependencies.",
            "core_dependencies": [s.lower() for s in skills],
            "recent_commit_subjects": ["Add extensive requirements.txt list"]
        }]
        proof_score = 10
        orig_count = 2
        fork_count = 1

    elif arch == "AUTHORSHIP_MISMATCH_FRAUD":
        repos = [
            {
                "name": "cloned-enterprise-project",
                "description": "Large scale enterprise project repository.",
                "language": skills[0],
                "topics": [s.lower() for s in skills[:3]],
                "stars": 42,
                "forks": 8,
                "is_fork": False,
                "readme_snippet": "Production codebase with hundreds of commits.",
                "subdirectories": ["core", "api", "infra"],
                "file_names": ["setup.py", "Dockerfile"]
            }
        ]
        checks = {
            "custom_code_substance": {"status": True, "details": "Deep codebase present."},
            "engineering_footprint": {"status": True, "details": "Mature project layout."},
            "phantom_dependency_stuffing": {"status": True, "details": "Dependencies verified."},
            "commit_authorship": {"status": False, "details": f"0/50 recent commits match candidate email ({email}); all commits authored by unknown foreign contributor."},
            "cryptographic_verification": {"status": False, "details": "No signed commits."},
            "opensource_contribution_type": {"status": True, "details": "Original repo."}
        }
        digests = [{
            "repo": f"{username}/cloned-enterprise-project",
            "language": skills[0],
            "stars": 42,
            "is_fork": False,
            "project_summary": "Enterprise service codebase with authorship mismatch.",
            "core_dependencies": [s.lower() for s in skills[:3]],
            "recent_commit_subjects": ["Major architectural refactor by lead developer"]
        }]
        proof_score = 5
        orig_count = 1
        fork_count = 0

    else:
        # PARTIAL_CODE_GAP
        repos = [
            {
                "name": "partial-stack-service",
                "description": f"Service implementing {skills[0]} and {skills[1]}.",
                "language": skills[0],
                "topics": [skills[0].lower(), skills[1].lower()],
                "stars": 8,
                "forks": 1,
                "is_fork": False,
                "readme_snippet": f"Service built using {skills[0]}.",
                "subdirectories": ["app"],
                "file_names": ["app.py", "requirements.txt"]
            }
        ]
        checks = {
            "custom_code_substance": {"status": True, "details": "Clean original code verified."},
            "engineering_footprint": {"status": True, "details": "Solid layout with unit tests."},
            "phantom_dependency_stuffing": {"status": True, "details": "Dependencies verified."},
            "commit_authorship": {"status": True, "details": f"All commits match candidate ({email})."},
            "cryptographic_verification": {"status": True, "details": "Commits signed with SSH key."},
            "opensource_contribution_type": {"status": True, "details": "Original repositories."}
        }
        digests = [{
            "repo": f"{username}/partial-stack-service",
            "language": skills[0],
            "stars": 8,
            "is_fork": False,
            "project_summary": f"Service verifying {skills[0]} but leaving other skills unverified in code.",
            "core_dependencies": [skills[0].lower()],
            "recent_commit_subjects": [f"feat: update {skills[0]} handlers"]
        }]
        proof_score = 15
        orig_count = 3
        fork_count = 0

    return {
        "stage2_archetype": arch,
        "github_analysis": {
            "found": True,
            "username": username,
            "profile_url": github,
            "account_age_years": 4.5,
            "public_repos_count": orig_count + fork_count,
            "original_repos_count": orig_count,
            "forked_repos_count": fork_count,
            "total_stars": repos[0]["stars"],
            "top_languages": [skills[0]],
            "recent_commits_active": True,
            "email_matched_in_commits": checks["commit_authorship"]["status"],
            "proof_score": proof_score,
            "repositories": repos,
            "checks": checks,
            "repo_digests": digests
        },
        "http_proofs": []
    }

def main():
    print("===============================================================")
    print("Kriu-Bench-v0.3: Starting 300 Synthetic Resume Generation...")
    print("===============================================================")

    all_ground_truth: Dict[str, Any] = {}
    all_payloads: Dict[str, Any] = {}
    rendered_counts = {"docx": 0, "pdf": 0}
    layout_counts = {l: 0 for l in LAYOUTS}

    global_id_counter = 1

    for role_key, role_info in ROLES.items():
        print(f"\n---> Generating 100 Resumes for Role: {role_info['title']} ({role_key})...")
        role_cand_idx = 0

        for cohort in COHORTS:
            cat_code = cohort["code"]
            cat_count = cohort["count"]

            for c_i in range(cat_count):
                resume_id = f"R{global_id_counter:03d}"
                cand = build_candidate_profile(role_key, cat_code, role_cand_idx, resume_id)
                payload = build_stage2_payload(cand)

                # Store ground truth and payload
                all_ground_truth[resume_id] = {
                    "resume_id": resume_id,
                    "filename": f"{resume_id}.{cand['format']}",
                    "name": cand["name"],
                    "email": cand["email"],
                    "role_key": role_key,
                    "role_title": cand["role_title"],
                    "category": cand["category"],
                    "relevance_tier": cand["relevance_tier"],
                    "is_top_10": cand["is_top_10"],
                    "demographic_tag": cand["demographic_tag"],
                    "format": cand["format"],
                    "layout": cand["layout"],
                    "skill_ground_truth": cand["skill_ground_truth"],
                    "planted_details": cand["planted_details"],
                    "stage2_archetype": cand["stage2_archetype"]
                }
                all_payloads[resume_id] = payload

                # Render file
                out_path = os.path.join(RESUMES_DIR, f"{resume_id}.{cand['format']}")
                if cand["format"] == "docx":
                    if cand["layout"] == "single_col_standard":
                        render_docx_single_col_standard(cand, out_path)
                    elif cand["layout"] == "two_col_sidebar":
                        render_docx_two_col_sidebar(cand, out_path)
                    elif cand["layout"] == "tabular_skills_matrix":
                        render_docx_tabular_skills_matrix(cand, out_path)
                    else:
                        render_docx_nonstandard_headers(cand, out_path)
                    rendered_counts["docx"] += 1
                else:
                    if cand["layout"] == "single_col_standard":
                        render_pdf_single_col_standard(cand, out_path)
                    elif cand["layout"] == "two_col_sidebar":
                        render_pdf_two_col_sidebar(cand, out_path)
                    elif cand["layout"] == "tabular_skills_matrix":
                        render_pdf_tabular_skills_matrix(cand, out_path)
                    else:
                        render_pdf_nonstandard_headers(cand, out_path)
                    rendered_counts["pdf"] += 1

                layout_counts[cand["layout"]] += 1
                role_cand_idx += 1
                global_id_counter += 1

    # Save Ground Truth Manifest
    with open(GROUND_TRUTH_FILE, "w", encoding="utf-8") as f:
        json.dump(all_ground_truth, f, indent=2)

    # Save Stage-2 Payloads Manifest
    with open(PAYLOADS_FILE, "w", encoding="utf-8") as f:
        json.dump(all_payloads, f, indent=2)

    print("\n===============================================================")
    print("Kriu-Bench-v0.3 Dataset Generation Complete!")
    print(f"Total Resumes Generated: {len(all_ground_truth)}")
    print(f"Format Breakdown: {rendered_counts['docx']} .docx (60%) | {rendered_counts['pdf']} .pdf (40%)")
    print(f"Layout Breakdown: {layout_counts}")
    print(f"Ground Truth File: {GROUND_TRUTH_FILE}")
    print(f"Payloads File:     {PAYLOADS_FILE}")
    print("===============================================================")

if __name__ == "__main__":
    main()
