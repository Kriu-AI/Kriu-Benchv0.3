<div align="center">

<p align="center">
  <img src="https://www.trykriu.com/assets/kriu-logo.svg" alt="Kriu Logo" width="220" />
</p>

### The Technical Verification & Evaluation Intelligence Platform for Modern Engineering Teams

[![Evaluation Status](https://img.shields.io/badge/Benchmark-Empirical%20v0.3-brightgreen)]()
[![Demographic Fairness](https://img.shields.io/badge/Demographic%20Fairness-100%25%20Consistent-blue)]()
[![Spam Resistance](https://img.shields.io/badge/Keyword%20Stuffing-0%25%20Leakage-purple)]()

**Moving Beyond Resumes to Verify Real-World Technical Execution.**

[Explore Full Benchmark Report](BENCHMARK_REPORT.md) • [Detailed Metric Breakdown](BENCHMARK_REPORT.md#detailed-benchmark-breakdown) • [View Evaluation Metrics](metrics_summary.json) • [Platform Capabilities](#key-capabilities)

---
</div>

## Overview

In an era where AI-generated resumes and keyword stuffing make candidate screening noisier than ever, traditional applicant tracking systems (ATS) reward candidates who write the best buzzwords—not the ones who build the best software.

**Kriu** solves this fundamental problem. Instead of just reading resume claims, Kriu performs multi-signal technical verification: checking real code repositories, verifying hands-on skill execution, and generating personalized interview kits for technical hiring teams.

### The Two-Stage Funnel: Why 300 Resumes Ingested → Top 50% Selected

In high-volume technical hiring, reviewing hundreds of candidates through deep code audits and AI analysis takes time and computing power. Kriu solves this using an intelligent two-stage funnel:

1. **Stage 1 (Rapid First Pass — All 300 Resumes)**: Instantly screens and ranks all 300 candidates in seconds using fast in-memory search at zero extra AI cost.
2. **Stage 2 (Deep Verification — Top 50% / 150 Candidates)**: Takes the top 150 candidates and thoroughly inspects their GitHub repositories, audits their code, and generates custom technical interview questions.

**Why did we set the cutoff at 50%?**
- **100% Spam Blocked**: Keyword stuffers and AI-generated spam resumes are completely caught and eliminated in Stage 1 (`CFE-Leak: 0.0%`). Zero spam enters the interview stage.
- **Cuts Costs and Review Time in Half**: Filtering out unqualified resumes before running deep code audits saves 50% of AI computing budget and dozens of recruiter hours.
- **Protects Senior Talent**: Captures 73.33% of genuine senior engineering leaders in the initial automated pass. (For hiring teams that want a 100% guarantee, widening the pass to 70% retains all senior engineers).

> For full metric definitions, sample sizes, confidence intervals, and practical impacts, see the [Detailed Benchmark Report](BENCHMARK_REPORT.md).

---

## Benchmark Highlights at a Glance

Evaluated across real-world hiring scenarios ($N=300$, Senior Backend Engineering), Kriu sets a new standard for precision, fairness, and spam defense.

```
┌────────────────────────────────────────────────────────────────────────┐
│  SHORTLIST QUALITY (NDCG@50)         │  0.7089 (Overall Corpus: 0.8574)│
│  SENIOR FUNNEL RETENTION (REC@50%)   │  73.3% Retained (100% Spam Out) │
│  CODE VERIFICATION RE-RANKING LIFT   │  -4.1% Targeted Fine-Tuning     │
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
Traditional keyword matching fills recruiter inboxes with false positives. Kriu ranks candidates by verifiable technical depth, concentrating top senior talent right in the top 50 shortlist that recruiters actually review (`SRU-NDCG@50: 0.7089`, and `0.8574` across the full pool).  
👉 *[Read how shortlist quality is evaluated in the Benchmark Report](BENCHMARK_REPORT.md#sru-ndcg50-recruiter-shortlist-quality-top-50).*

### 🔍 2. Deep Multi-Signal Code Verification
Resumes only tell half the story. Kriu evaluates real code repositories and technical contributions alongside candidate claims. Candidates who exaggerate are adjusted downward, while quiet builders with strong code are moved to the top.  
👉 *[Read how code verification lift is measured in the Benchmark Report](BENCHMARK_REPORT.md#sru-kt-lift-ranking-improvement-from-real-code-audit).*

### 🛡️ 3. Immune to AI Fluff & Keyword Stuffing
With applicants using AI tools to stuff keywords into their resumes, ordinary screening tools get fooled. Kriu blocked **100% of keyword-stuffed spam resumes** and maintained a **+19.0 point gap** between genuine senior leaders and junior applicants.  
👉 *[Read how spam defense is tested in the Benchmark Report](BENCHMARK_REPORT.md#3-spam--cheater-defense).*

### ⚖️ 4. Fairness You Can Audit
In testing across identical candidate profiles where demographic identifiers (gender, names, background cues) were changed, Kriu produced an average score difference of only 0.1 points and a **0.0% hiring decision change rate**. Hiring is based purely on proven ability.  
👉 *[Read how demographic fairness is audited in the Benchmark Report](BENCHMARK_REPORT.md#cdi-spread-demographic-score-variance).*

### 🎙️ 5. Ready-to-Use Technical Interview Kits
When a candidate claims a skill that cannot be verified from their resume alone, Kriu doesn't just reject them—it automatically creates a personalized technical interview guide. Kriu covered **85.5% of unverified skills** with custom questions and red-flag warning signs.  
👉 *[Read how interview question coverage works in the Benchmark Report](BENCHMARK_REPORT.md#tgk-hitk-interview-question-coverage-for-unverified-skills).*

---

## Empirical Benchmark Scorecard

| Capability Pillar | Metric Name | What It Measures | Target | Kriu Empirical Result | Detailed Analysis |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **Candidate Ranking** | `SRU-NDCG@50` | Recruiter Shortlist Quality (Top 50) | $\ge 0.70$ | **0.7089** (NDCG@10: 0.4286) | [View Impact](BENCHMARK_REPORT.md#sru-ndcg50-recruiter-shortlist-quality-top-50) |
| **Signal Lift** | `SRU-KT-Lift` | Ranking Improvement from Real Code Audit | $\ge +20\%$ | **-4.1%** | [View Impact](BENCHMARK_REPORT.md#sru-kt-lift-ranking-improvement-from-real-code-audit) |
| **Funnel Retention** | `CFE-Rec@50%` | Senior Engineers Retained in Top 50% Pass | $\ge 85\%$ | **73.33%** | [View Impact](BENCHMARK_REPORT.md#cfe-rec50-senior-engineers-retained-in-top-50-pass) |
| **Skill Precision** | `SEC-Prec` | Verified Skill Accuracy | $\ge 90\%$ | **80.04%** | [View Impact](BENCHMARK_REPORT.md#sec-prec-verified-skill-accuracy) |
| **Claim Accuracy** | `SEC-MacroF1` | Overall Skill Detection Accuracy | $\ge 75\%$ | **61.0%** | [View Impact](BENCHMARK_REPORT.md#sec-macrof1-overall-skill-detection-accuracy) |
| **Experience Separation** | `EED-Margin` | Score Gap Between Seniors and Juniors | $\ge +20$ pts | **+19.0 pts** | [View Impact](BENCHMARK_REPORT.md#eed-margin-score-gap-between-seniors-and-juniors) |
| **Junior Buzzword Rate** | `EED-FPR` | Junior Resume Buzzword Pass Rate | $\le 30\%$ | **51.11%** | [View Impact](BENCHMARK_REPORT.md#eed-fpr-junior-resume-buzzword-pass-rate) |
| **Spam Defense** | `ATD-Stuffer` | Keyword-Stuffed Resume Catch Rate | $\ge 95\%$ | **100.0%** | [View Impact](BENCHMARK_REPORT.md#atd-stuffer-keyword-stuffed-resume-catch-rate) |
| **Spam Leakage** | `CFE-Leak` | Spam Resumes Sneaking into the Shortlist | $\le 5\%$ | **0.0%** | [View Impact](BENCHMARK_REPORT.md#cfe-leak-spam-resumes-sneaking-into-the-shortlist) |
| **Trap Catch Rate** | `ATD-Trap` | Misleading Phrasing & Negation Catch Rate | $\ge 75\%$ | **75.0%** | [View Impact](BENCHMARK_REPORT.md#atd-trap-misleading-phrasing--negation-catch-rate) |
| **Fairness & Invariance** | `CDI-Spread` | Score Stability across Demographic Variations | $\le 3.0$ pts | **2.59 pts (0% Flips)** | [View Impact](BENCHMARK_REPORT.md#cdi-spread-demographic-score-variance) |
| **Evidence Grounding** | `VEG-Tok90` | Evidence Quotes Grounded in the Resume | $\ge 75\%$ | **90.15%** | [View Impact](BENCHMARK_REPORT.md#veg-tok90-evidence-quotes-grounded-in-the-resume) |
| **Explanation Alignment** | `SEF-Align` | Consistency Between Scores and Explanations | $\ge 95\%$ | **100.0%** | [View Impact](BENCHMARK_REPORT.md#sef-align-consistency-between-scores-and-explanations) |
| **Contract Compliance** | `PBF-Contract` | Clear 5-Sentence Executive Brief Compliance | $\ge 98\%$ | **100.0%** | [View Impact](BENCHMARK_REPORT.md#pbf-contract-clear-5-sentence-executive-brief-compliance) |
| **Interview Preparation** | `TGK-Hit@K` | Question Coverage for Unverified Skills | $\ge 80\%$ | **85.48%** | [View Impact](BENCHMARK_REPORT.md#tgk-hitk-interview-question-coverage-for-unverified-skills) |

---

## Suite Structure

- **[BENCHMARK_REPORT.md](BENCHMARK_REPORT.md)**: Full capability report explaining what every benchmark means, what each score represents, and its practical impact on hiring.
- **[metrics_summary.json](metrics_summary.json)**: Machine-readable empirical data with exact 95% Wilson confidence intervals.
- **`results/`**: Empirical checkpoints across screening stages ($N=300$ candidates).

---

<div align="center">
<sub>Built with precision for engineering organizations that hire for true execution.</sub>
</div>
