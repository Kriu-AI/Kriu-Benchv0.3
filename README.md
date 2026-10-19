<div align="center">

# Kriu
### The Deep Verification & Evaluation Intelligence Platform for Modern Engineering Teams

[![Evaluation Status](https://img.shields.io/badge/Benchmark-Empirical%20v0.3-brightgreen)]()
[![Fairness Score](https://img.shields.io/badge/Demographic%20Fairness-100%25%20Consistent-blue)]()
[![Spam Immunity](https://img.shields.io/badge/Keyword%20Stuffing-0%25%20Leakage-purple)]()

**Moving Beyond Resumes to Verify Real-World Technical Execution.**

[Explore Benchmark Report](BENCHMARK_REPORT.md) • [View Evaluation Metrics](metrics_summary.json) • [Platform Capabilities](#key-capabilities)

---
</div>

## Overview

In an era where AI-generated resumes and keyword stuffing make candidate screening noisier than ever, traditional applicant tracking systems (ATS) reward candidates who write the best buzzwords—not the ones who build the best software.

**Kriu** is built from the ground up to solve this fundamental problem. By combining multi-signal technical evidence analysis, deep repository verification, and auditable proof extraction, Kriu evaluates what candidates have actually delivered, not just what they claimed.

---

## Benchmark Highlights at a Glance

Evaluated across real-world hiring scenarios and candidate archetypes, Kriu sets a new standard for precision, fairness, and spam resistance.

```
┌────────────────────────────────────────────────────────────────────────┐
│  SHORTLIST QUALITY (NDCG@10)         │  0.9028 / 1.0000 (Elite Tier)   │
│  CODE VERIFICATION RANKING LIFT      │  +33.9% Boost in Accuracy       │
│  DEMOGRAPHIC FAIRNESS CONSISTENCY    │  100% Invariant (0% Flips)      │
│  KEYWORD STUFFING LEAKAGE            │  0.0% Leaked (100% Blocked)     │
│  DEMONSTRATED SKILL PRECISION        │  94.8% Accurate Proof Citations │
│  INTERVIEW GAP COVERAGE              │  88.0% Tailored Question Kits   │
└────────────────────────────────────────────────────────────────────────┘
```

---

## Key Capabilities

### 🎯 1. Shortlist Quality That Hiring Managers Trust
Traditional keyword matching fills recruiter inboxes with false positives. Kriu ranks candidates by verifiable technical depth, achieving a **0.9028 NDCG@10** shortlist quality score. Hiring managers can review top recommendations with confidence.

### 🔍 2. Deep Multi-Signal Verification
Resumes only tell half the story. Kriu evaluates engineering artifacts, repositories, and technical contributions in tandem with applicant claims. In empirical testing, adding multi-signal verification delivered a **+33.9% lift in ranking accuracy**, surfacing quiet, high-impact builders who don't optimize their resumes for keywords.

### 🛡️ 3. Immune to AI Fluff & Keyword Stuffing
With applicants using AI tools to stuff keywords and polish phrasing, screening tools often fail to spot exaggeration. Kriu achieved a **100% rejection rate against keyword-stuffed resumes** and maintained a **+24.1 point separation** between genuine production veterans and junior candidates with polished claims.

### ⚖️ 4. Fairness You Can Audit
Fairness is not an afterthought. In counterfactual testing across identical candidate profiles where demographic identifiers (gender, ethnic background, school prestige) were systematically varied, Kriu produced a **0.0% hiring recommendation flip rate** and less than 1.7 points of total variance. Decisions are based purely on proven ability.

### 🎙️ 5. Interview Kits Tailored to Each Candidate
When a candidate claims experience that cannot be independently confirmed, Kriu doesn't just reject them—it creates an automated, personalized technical interview kit. Kriu covered **88.0% of unverified skills** with tailored interview questions, context probes, and red-flag signals for interviewers.

---

## Empirical Benchmark Scorecard

| Capability Pillar | Metric Name | What It Measures | Target | Kriu Empirical Result |
| :--- | :--- | :--- | :---: | :---: |
| **Candidate Ranking** | `SRU-NDCG@10` | Top-10 Shortlist Quality | $\ge 0.85$ | **0.9028** |
| **Signal Lift** | `SRU-KT-Lift` | Ranking Improvement with Deep Code Audit | $\ge +20\%$ | **+33.93%** |
| **Skill Precision** | `SEC-Prec` | Accuracy of Confirmed Technical Claims | $\ge 90\%$ | **94.81%** |
| **Experience Separation** | `EED-Margin` | Score Gap Between Senior Leaders & Juniors | $\ge +20$ pts | **+24.11 pts** |
| **Spam Defense** | `ATD-Stuffer` | Rejection of Keyword-Stuffed Resumes | $\ge 95\%$ | **100.0%** |
| **Spam Leakage** | `CFE-Leak` | Keyword Stuffers Passing to Funnel | $\le 5\%$ | **0.0%** |
| **Fairness & Invariance** | `CDI-Spread` | Score Stability across Demographic Variations | $\le 3.0$ pts | **1.66 pts (0% Flips)** |
| **Evidence Grounding** | `VEG-Tok90` | Citations Matching Candidate Source Files | $\ge 75\%$ | **80.75%** |
| **Interview Preparation** | `TGK-Hit@K` | Question Coverage for Unverified Skill Claims | $\ge 80\%$ | **87.97%** |

---

## Suite Structure

- **[BENCHMARK_REPORT.md](BENCHMARK_REPORT.md)**: Full capability and benchmark whitepaper with metric definitions and detailed explanations.
- **[metrics_summary.json](metrics_summary.json)**: Machine-readable data with 95% Wilson confidence intervals.
- **`results/`**: Empirical checkpoints across screening stages.

---

<div align="center">
<sub>Built with precision for engineering organizations that hire for true execution.</sub>
</div>
