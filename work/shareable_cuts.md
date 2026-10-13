# Tell the Story (ML-12) — Demo Script & Shareable Cuts

- **Author:** Muhammad Akbar Pradana
- **Track:** Machine Learning (ML-12)
- **Deployed Paper:** https://devaaldo.github.io/flyrank-ml/
- **Repository:** https://github.com/Devaaldo/flyrank-ml

---

## 1. Five-Minute Technical Demo Script (Week-8 Showcase Ready)

### Minute 0:00 - 1:00 (The Business Bottleneck)
"Good morning everyone. In modern digital publishing and enterprise SEO, companies manage portfolios of 30,000+ published URLs. But human editorial teams can realistically audit and rewrite only about 50 articles per weekly sprint. When high-performing articles on Google Page 1 decay, companies suffer severe organic traffic and revenue loss. The operational challenge we solved is: how do we accurately surface the 50 most urgent decay risks every week without drowning editors in false alarms?"

### Minute 1:00 - 2:15 (The Pitfall of Complex Tree Ensembles)
"Our natural engineering instinct was to train complex models like Random Forest. When we evaluated Random Forest using standard random cross-validation, it scored a seemingly incredible 94% Precision@50. But in multi-tenant publishing, random splitting is a trap: pages from the same client share domain authority, so the tree splits merely memorized client identities. When we evaluated under a strict Client-Holdout split (testing on 7 client domains the model had never seen), Random Forest collapsed by 48 points down to 46% precision, performing worse than the 52% base rate."

### Minute 2:15 - 3:30 (The Monotonic Solution)
"To fix this, we enforced monotonic regularization using an L2-regularized Logistic Regression model. Why? Because the physics of content decay are monotonic: holding all else equal, older content with slipping visibility increases decay risk across every tenant. On the exact same unseen test clients, Logistic Regression delivered 76.0% Precision@50: correctly identifying 38 out of 50 decaying URLs and beating the heuristic rule baseline (42%) by 1.8x."

### Minute 3:30 - 4:15 (The Action Playbook & Exposure Weighting)
"A model score alone doesn't help an editor. We translated these calibrated scores into an operational Content Action Playbook with two key breakthroughs:
First, exposure weighting: by combining decay probability with log impressions, we lifted median protected visibility to 7,382 impressions per review URL.
Second, diagnostic action archetypes: 64% of items were classified as Page 1 Title Defense, 22% as Striking Distance CTR Snippet Optimization (requiring just 15 minutes of work per URL), and 14% as Routine Review."

### Minute 4:15 - 5:00 (Human Governance & Boundaries)
"Finally, we implemented strict operational boundaries: Tier 1 high-stakes pages in positions 1 to 5 require SEO Director sign-off, and we enforce an explicit No-Go list that strictly forbids unsupervised LLM rewrites or automated URL deletions. The entire pipeline, research paper, and receipts are fully open-source and live at devaaldo.github.io/flyrank-ml. Thank you."

---

## 2. Social-Post Cut (LinkedIn / Technical Community)

Why did a simple Logistic Regression model beat an advanced Random Forest by 30 percentage points (a 1.65x relative lift) in production SEO ranking?

During my Machine Learning internship at FlyRank AI, we tackled content decay across 30,000 active web pages and 32 enterprise domains. When evaluating model prioritization, Random Forest achieved an eye-popping 94% Precision@50 under a naive random split. But under a rigorous Client-Holdout split (evaluating strictly on unseen client domains), the tree ensemble collapsed to 46%, heavily overfitting to tenant-specific scale baselines.

By contrast, monotonic L2-regularized Logistic Regression held strong at 76.0% Precision@50 (vs. 42% rule baseline). We combined this into an operational Content Action Playbook with transparent reason codes and human-in-the-loop governance, protecting 7,382 median impressions per flagged piece.

Full research paper, interactive figures, and reproducible code: https://devaaldo.github.io/flyrank-ml/

---

## 3. Employer-Facing Three-Sentence Summary

1. **What I Built:** Built an end-to-end Machine Learning prioritization pipeline on the FlyRank multi-tenant search dataset (30,000 active pages across 32 enterprise domains) to triage decaying content under strict weekly editorial bandwidth constraints (~50 URLs/sprint).
2. **What the Data Showed:** Identified and diagnosed a 48-percentage-point cross-domain generalization gap in complex tree ensembles, deploying a monotonic regularized model achieving 76.0% Precision@50 on held-out client organizations.
3. **Operational Impact:** Operationalized model inferences into an exposure-weighted Content Action Playbook protecting 7,382 median search impressions per review item with 3-tier human governance, reproducible code, and public deployment.
