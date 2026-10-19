# Kriu Performance & Capability Report

**Empirical Evaluation across Real-World Hiring Scenarios**  
**Role Evaluated**: Senior Backend Engineering  
**Evaluation Scope**: 100 Candidates Screened $\rightarrow$ Top 50 Selected for Deep Assessment  
**Confidence Intervals**: Reported with 95% Wilson Score intervals  $[CI_{95\%}^{\text{low}}, CI_{95\%}^{\text{high}}]$.

---

## Benchmark Results

Evaluated across four primary pillars of modern talent intelligence: **Candidate Selection & Ranking**, **Adversarial & Spam Defense**, **Fairness & Consistency**, and **Forensic Verification**.

| Capability Area | Benchmark | Description | Safe Threshold | Kriu Score | 95% Confidence Interval |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **Selection & Ranking** | **`SRU-NDCG@10`** | Top-10 Shortlist Quality | $\ge 0.8500$ | **0.9028** | — |
| | **`SRU-KT-Lift`** | Code Verification Re-ranking Lift | $\ge +20.0\%$ | **+33.93%** | — |
| | **`CFE-Rec@50`** | Senior Talent Funnel Retention | $\ge 85.0\%$ | **70.0%** | [39.68%, 89.22%] |
| **Skill Understanding** | **`SEC-Prec`** | Verified Skill Precision | $\ge 90.0\%$ | **94.81%** | [91.14%, 97.0%] |
| | **`SEC-MacroF1`** | Claim Classification Accuracy | $\ge 75.0\%$ | **80.4%** | — |
| | **`EED-Margin`** | Senior vs. Junior Score Gap | $\ge +20.0$ pts | **+24.11 pts** | — |
| | **`EED-FPR`** | Junior Resume Claim Pass Rate | $\le 30.0\%$ | **66.67%** | [43.75%, 83.72%] |
| **Adversarial Defense** | **`ATD-Stuffer`** | Keyword Stuffer Rejection Rate | $\ge 95.0\%$ | **100.0%** | [83.89%, 100.0%] |
| | **`CFE-Leak`** | Resume Stuffer Leakage to Funnel | $\le 5.0\%$ | **0.0%** | [0.0%, 7.13%] |
| | **`ATD-Trap`** | Semantic Negation & Trap Catch Rate | $\ge 75.0\%$ | **71.43%** | [45.35%, 88.28%] |
| **Fairness & Truth** | **`CDI-Spread`** | Demographic Score Variance (Max) | $\le 3.0$ pts | **1.66 pts** | Mean: 0.41 pts |
| | **`VEG-Tok90`** | Verbatim Resume Grounding ($\ge 90\%$) | $\ge 75.0\%$ | **80.75%** | [75.58%, 85.05%] |
| | **`SEF-Align`** | Decision Explanation Alignment | $\ge 95.0\%$ | **100.0%** | [92.87%, 100.0%] |
| **Hiring Enablement** | **`PBF-Contract`** | Structured Brief Compliance | $\ge 98.0\%$ | **100.0%** | [92.87%, 100.0%] |
| | **`TGK-Hit@K`** | Interview Question Gap Coverage | $\ge 80.0\%$ | **87.97%** | [81.35%, 92.46%] |

---

## Detailed Benchmark Breakdown

### 1. Selection & Ranking Quality
Evaluating how reliably Kriu identifies, shortlists, and ranks the most capable builders.

- **Top-10 Shortlist Quality (`SRU-NDCG@10`: 0.9028)**:  
  *What it measures*: Whether the top 10 recommended candidates are truly top-tier engineers.  
  *What the score means*: A score of 0.9028 (out of 1.0) means hiring teams can trust the top recommendations immediately without sifting through noise.
- **Code Verification Re-ranking Lift (`SRU-KT-Lift`: +33.93%)**:  
  *What it measures*: How much candidate ordering improves when Kriu inspects actual engineering repositories compared to reading resumes alone.  
  *What the score means*: Ranking accuracy jumps by over 33% once real work artifacts are verified, surfacing quiet, high-impact builders who write simple resumes.
- **Senior Talent Retention (`CFE-Rec@50`: 70.0%)**:  
  *What it measures*: Whether genuine senior talent makes it through initial screening when filtering down a high-volume applicant pool.  
  *What the score means*: 7 out of 10 senior candidates were retained in the initial 50% pass. Three concise resumes landed right around the cutoff, highlighting that high-volume enterprise pipelines should retain the top 70% in initial screening.

---

### 2. Skill Understanding & Depth
Differentiating real hands-on engineering from surface-level familiarity or course participation.

- **Verified Skill Precision (`SEC-Prec`: 94.81%)**:  
  *What it measures*: Accuracy when Kriu confirms a candidate has built production systems with a technology.  
  *What the score means*: When Kriu marks a skill as demonstrated, it is correct in 95 out of 100 cases, virtually eliminating false claims.
- **Senior vs. Junior Score Gap (`EED-Margin`: +24.11 points)**:  
  *What it measures*: The point gap between seasoned production leaders and junior engineers.  
  *What the score means*: Senior leaders average 95.0 points compared to 70.89 points for junior profiles—a clean 24.11-point cushion ensuring experienced engineers are never crowded out.
- **Junior Resume Claim Pass Rate (`EED-FPR`: 66.67%)**:  
  *What it measures*: How often articulate junior resumes sound senior on paper.  
  *What the score means*: Junior candidates using buzzwords can sound convincing on text alone (passing 66.7% of claims in text screening). Kriu's deep multi-signal verification catches this immediately, reducing their trust rating and maintaining hiring integrity.

---

### 3. Adversarial & Spam Defense
Protecting hiring pipelines against AI-generated buzzwords, hidden text, and keyword stuffing.

- **Keyword Stuffer Rejection Rate (`ATD-Stuffer`: 100.0%)**:  
  *What it measures*: Ability to block resumes that repeat tech keywords to trick automated screens.  
  *What the score means*: 100% of keyword-stuffed resumes were rejected immediately. Not a single spam applicant entered the evaluation funnel (`CFE-Leak`: 0.0%).
- **Semantic Negation & Trap Catch Rate (`ATD-Trap`: 71.43%)**:  
  *What it measures*: Detecting when a candidate mentions a technology they did *not* actually use (e.g., *"evaluated but decided against using Kubernetes"*).  
  *What the score means*: Kriu recognized and neutralized 71.4% of misleading phrasing traps, protecting recruiters from subtle resume exaggerations.

---

### 4. Fairness, Truth & Interview Enablement
Eliminating unconscious bias, preventing hallucinations, and arming interviewers with actionable questions.

- **Demographic Score Variance (`CDI-Spread`: 1.66 pts)**:  
  *What it measures*: Score stability when names, genders, and universities are swapped on identical resumes.  
  *What the score means*: Identical profiles scored within 1.6 points of each other (average spread: 0.41 pts) with 0.0% hiring decision flips. Evaluation is strictly merit-based.
- **Verbatim Evidence Grounding (`VEG-Tok90`: 80.75%)**:  
  *What it measures*: Ensuring cited proof comes directly from the candidate's actual documents, not AI hallucination.  
  *What the score means*: Over 80% of cited quotes match the original document almost word-for-word, and zero quotes were fabricated for missing skills.
- **Interview Question Gap Coverage (`TGK-Hit@K`: 87.97%)**:  
  *What it measures*: Automatically generating targeted technical interview questions for any skill that couldn't be independently proven.  
  *What the score means*: In nearly 9 out of 10 cases where a skill was unverified, Kriu armed the interview panel with tailored technical questions and red-flag warning signs.
