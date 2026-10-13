# Capstone Report: Content Refresh Prioritization Under Multi-Tenant Search Volatility

- **Author:** Muhammad Akbar Pradana
- **Lane:** Content Refresh Prioritization & Search Decay
- **Repo:** https://github.com/Devaaldo/flyrank-ml
- **Deployed Paper:** https://devaaldo.github.io/flyrank-ml/
- **Date:** October 2026

---

## 0. Abstract

In enterprise search engine optimization (SEO), editorial teams operate under strict weekly review constraints (~50 URLs per sprint), requiring automated prioritization to triage decaying content before search visibility is irreversibly lost. Using the FlyRank multi-tenant search dataset (30,000 active web pages spanning 32 client domains with trailing 90-day Search Console and GA4 metrics), we evaluate content decay dynamics and model generalization. We benchmark transparent heuristic rules against shallow decision trees, Random Forest ensembles, and L2-regularized Logistic Regression evaluated strictly under a grouped **Client-Holdout validation scheme** (25 training clients vs. 7 completely unseen test clients) to prevent multi-tenant domain memorization. While Random Forest models achieved a deceptively high 94.0% Precision@50 under naive random splits, their performance collapsed by 48.0 percentage points to 46.0% on unseen domains; in contrast, L2-regularized Logistic Regression maintained strong generalization, delivering **76.0% Precision@50** (a 1.8× lift over the 42.0% heuristic baseline). We translate these calibrated scores into an operational Content Action Playbook featuring diagnostic Reason Codes, a 3-tier human governance protocol, and an exposure-weighted priority queue protecting 7,382 median impressions per flagged article.

---

## 1. Problem framing

Enterprise web operations manage tens of thousands of published articles, but editorial teams have capacity to thoroughly audit and rewrite only ~30 to 50 comprehensive articles per weekly sprint. Unchecked decay on Google Page 1 represents an asymmetric business risk. The primary unit of analysis is the individual web page (`content_id`), mapped to an operational priority queue evaluated at **Precision@50**. Why does machine learning help? Hand-crafted rules fail to capture non-linear interactions between search position, impression consistency, and click-through rates across diverse client domains.

---

## 2. Data safety & Leakage Defense

- **Dataset:** FlyRank active modeling dataset (`content_refresh_anonymized.csv`), 30,000 rows × 44 columns across 32 clients.
- **Quarantined Columns:** `trend_direction` and `trend_pct` were strictly excluded from training features (X) because the target label is derived directly from them.
- **Pseudonymous Isolation:** Entity IDs (`content_id`, `client_id`) were used exclusively for grouped cross-validation splits, never as model features.
- **Transformations:** Traffic metrics (`impressions_90d`, `clicks_90d`, `sessions_90d`) were normalized using $\log(1 + x)$. `avg_position = 0` was handled as unranked rather than rank zero.
- **Public Safety:** Confirmed zero client names, URLs, or raw queries appear in the report or repository.

---

## 3. Baseline

Our transparent heuristic rule baseline (developed in Week 4) combines percentile-ranked visibility, staleness, and Page 1 status:
$$\text{Baseline Score} = 0.40 \times \text{rank}(\text{impr}) + 0.35 \times \text{rank}(\text{staleness}) + 0.25 \times (\text{pos\_norm} \times \text{visibility})$$
On the held-out test partition (N_test = 3,419, base rate = 52.4%), this baseline achieves **Precision@50 = 42.0%** and **Precision@100 = 50.0%** (ROC-AUC = 0.600).

---

## 4. Model / analysis

We evaluated three models against the baseline on the exact same client-holdout split:
1. **L2-Regularized Logistic Regression (Champion):** **76.0% Precision@50** (ROC-AUC 0.658, PR-AUC 0.660). Monotonic constraints prevent cross-feature tenant memorization.
2. **Decision Tree (`max_depth=5`):** **70.0% Precision@50** (ROC-AUC 0.654). Transparent IF-THEN rules.
3. **Random Forest (200 trees, depth 10):** **46.0% Precision@50** (ROC-AUC 0.664, Recall 0.772). Severely memorized training domain scale baselines.

---

## 5. Validation Design & Limitations

- **Validation:** 25 clients for training, 7 unseen clients for testing (client-holdout grouped split).
- **Limitations & Methodological Disclosures:**
  1. *Observational only:* No causal claims without randomized A/B intervention.
  2. *Seasonality confounding:* Rolling 90-day window does not isolate annual seasonal spikes.
  3. *Domain age requirement:* Requires at least 180 days of search history.
  4. *Label proxy & co-occurrence:* `is_declining_label` is derived from `trend_direction` (last 30d vs prior 30d), which overlaps within the same 90-day aggregate snapshot. Full warehouse deployment requires strict point-in-time temporal partitioning.
  5. *Divergence from starter reference pipeline:* In FlyRank's unscaled starter baseline, Random Forest scored ~0.68–0.74 P@50 while unregularized Logistic Regression scored ~0.40. In our production lane, this inverted (LR 76.0% vs. RF 46.0%) because our pipeline introduced log-transformed traffic counts, StandardScaler normalization, and strict client-holdout evaluation. Linear monotonic weights transferred cleanly across unseen tenants, whereas unconstrained tree ensembles partitioned on raw volume scales and overfit to training domains.

---

## 6. Ranked Recommendations (The Playbook)

We operationalized inferences into a dual-ranking Content Action Playbook:
- **Pure Model Ranking:** P@50 = 76.0%, median impressions = 1,684.
- **Exposure-Weighted Ranking:** Priority Score = P(decay) * log(1 + impr_90d), lifting median impressions to **7,382** (P@50 = 54.0%).
- **Prescribed Interventions:**
  - `Urgent Refresh & Title Defense` (64%): Page 1 assets at acute risk of dropping off.
  - `Optimize Snippet & Meta Tags` (22%): Striking-distance pages (Pos 11–20) with CTR < 0.5%.
  - `Routine Editorial Review` (14%): General decay cases.
- **3-Tier Human Governance:** Tier 1 (Positions 1–5) requires SEO Director sign-off.
- **No-Go List:** Strictly forbids unsupervised generative AI overwriting and programmatic URL deletions.

---

## 7. Artifacts & Figures

- `docs/figures/action_mix.png`: Editorial action distribution across top 50 queue.
- `docs/figures/priority_vs_position.png`: Priority score concentration by search position tier.
- `work/outputs/action_queue_top50.csv`: Ranked triage queue.
- `work/outputs/playbook_summary.json`: Machine-readable validation receipts.

---

## 8. Reproducibility

- **Repository:** https://github.com/Devaaldo/flyrank-ml
- **Capstone Notebook:** `work/notebooks/capstone.ipynb` (reproducibility seed: `42`).
- **Pipeline:** Run end-to-end via `python scripts/run_all.py`.

---

## 9. Acknowledgments & Data Credit

Built on the FlyRank ML Internship dataset, hosted and provided by [FlyRank AI](https://flyrank.ai). We thank the FlyRank engineering mentorship team for providing access to real-world search telemetry and establishing rigorous benchmarks for applied machine learning.
---

## 10. Showcase, Demo Outline & Shareable Cuts (ML-12)

### 1. 5-Minute Technical Demo Outline
1. **Minute 0:00 - 1:00 (The Problem):** Demonstrate the editorial bottleneck: enterprise sites with 30k+ pages and capacity for only ~50 reviews per week. Page 1 decay loses traffic fast.
2. **Minute 1:00 - 2:15 (The Pitfall of Complex Models):** Show how a Random Forest model looks superhuman (94% Precision@50) on a random split, but collapses by 48 points to 46% on unseen clients due to multi-tenant scale memorization.
3. **Minute 2:15 - 3:30 (The Monotonic Solution):** Present the L2-regularized Logistic Regression model delivering 76.0% Precision@50 on unseen domains (1.8x lift over heuristics).
4. **Minute 3:30 - 4:15 (The Playbook in Action):** Walk through the exposure-weighted queue protecting 7,382 median impressions per flagged article.
5. **Minute 4:15 - 5:00 (Governance & Boundaries):** Detail the 3-tier review protocol and explicit No-Go automation rules.

### 2. Social-Post Cut (LinkedIn / Technical Community)
> Why did a simple Logistic Regression model beat an advanced Random Forest by 30 percentage points (a 1.65x relative lift) in production SEO ranking?
>
> During my Machine Learning internship at FlyRank AI, we tackled content decay across 30,000 active pages and 32 enterprise domains. When evaluating model prioritization, Random Forest achieved an eye-popping 94% Precision@50 under a random split. But under a rigorous Client-Holdout split (evaluating strictly on unseen client domains), the tree ensemble collapsed to 46%, severely overfitting to domain-specific traffic scale.
>
> By contrast, monotonic L2-regularized Logistic Regression held strong at 76.0% Precision@50 (vs. 42% rule baseline). We combined this into an operational Content Action Playbook with transparent reason codes and human-in-the-loop governance. Full research paper: https://devaaldo.github.io/flyrank-ml/

### 3. Employer-Facing 3-Sentence Summary
> 1. Built an end-to-end Machine Learning prioritization pipeline on the FlyRank multi-tenant search dataset (30,000 active pages across 32 enterprise domains) to triage decaying content under strict editorial bandwidth constraints (~50 URLs/sprint).
> 2. Identified and diagnosed a 48-percentage-point cross-domain generalization gap in complex tree ensembles, deploying a monotonic regularized model achieving 76.0% Precision@50 on held-out client organizations.
> 3. Operationalized model inferences into an exposure-weighted Content Action Playbook protecting 7,382 median search impressions per review item with 3-tier human governance, reproducible code, and public deployment.
