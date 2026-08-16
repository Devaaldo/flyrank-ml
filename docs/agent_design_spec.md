# 🤖 Personal AI Agent Design Document: ML & Search Intelligence Scout

**Track:** General AI Fluency (FL-06) | **Phase:** Build (Core)  
**Author:** Muhammad Akbar Pradana (Machine Learning Intern @ FlyRank AI)  
**Target Build Scope:** ~10 Hours | **Stack:** Python 3.11 + Google Gemini API (Free Tier)  

---

## 1. The Job to Be Done (JTBD) & User Profile

### Job to Be Done
Automate the daily search performance audit, content decay diagnosis, and ML research workflows for an applied AI engineer. Specifically, the agent will:
1. Ingest 90-day search performance datasets (impressions, clicks, average positions, staleness).
2. Detect decaying content items using transparent heuristic rules and ML scoring.
3. Generate structured review queues with human-interpretable **Reason Codes** (`stale_visible_page`, `low_ctr`, `page_one_decay_risk`) and **Action Labels** (`refresh`, `review_ctr`, `expand_and_refresh`).
4. Serve as a grounded ML research scout to explain mathematical concepts, summarize arXiv papers, and prevent methodological pitfalls (e.g., target leakage).

### The User & Frequency
- **Target User:** Muhammad Akbar Pradana (Machine Learning Engineer / Data Scientist).
- **Usage Frequency:** 3–5 times per week during sprint data analysis and weekly research reviews.

---

## 2. Build Platform Choice & Justification

### Selected Platform
**Scripted Standalone Python Agent** utilizing **Google Gemini API (Free Tier)** with local Python libraries (`pandas`, `numpy`, `scikit-learn`, `requests`, `duckdb`).

### Justification against Alternatives
| Platform Option | Cost | Limitations / Trade-offs | Decision |
|---|---|---|---|
| **Custom GPT (OpenAI)** | Paid ($20/mo) | Closed ecosystem, limited local file access, cannot run custom Python ML evaluation loops directly on large datasets. | Rejected |
| **Claude Cowork / Project** | Paid ($20/mo) | Requires active paid subscription, rigid connector limitations. | Rejected |
| **n8n Workflow Automation** | Free (Self-hosted) | Visual workflow builder is great for webhooks, but suboptimal for deep tabular ML operations and complex pandas data transformations. | Rejected |
| **Scripted Python Agent** | **100% Free** | High flexibility, full local file system access, seamless integration with pandas/scikit-learn, version-controlled in Git. | **SELECTED ✅** |

---

## 3. Data Sources & Tools Access Plan

The agent interacts with the environment through 4 defined Python tool functions:

```
                  ┌────────────────────────────────────────┐
                  │   Personal AI Agent (Gemini LLM Core)  │
                  └───────────────────┬────────────────────┘
                                      │
        ┌───────────────────┬─────────┴─────────┬───────────────────┐
        ▼                   ▼                   ▼                   ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ Tool 1:       │   │ Tool 2:       │   │ Tool 3:       │   │ Tool 4:       │
│ read_data()   │   │ audit_decay() │   │ search_ml()   │   │ export_plan() │
└───────┬───────┘   └───────┬───────┘   └───────┬───────┘   └───────┬───────┘
        │                   │                   │                   │
  Local CSV/Parquet    Heuristic Logic     Documentation/      CSV/Markdown
  Datasets             & scikit-learn      arXiv Papers        Action Queue
```

1. **`read_performance_data(file_path: str)`**: Reads local tabular search datasets (`content_refresh_anonymized.csv`) into memory using pandas.
2. **`audit_decay_signals(content_id: str)`**: Calculates composite visibility, staleness, and position opportunity scores; outputs transparent Reason Codes.
3. **`search_ml_knowledge(topic: str)`**: Retrieves structured explanations of ML metrics (Precision@K, ROC AUC, Client-Holdout splits) and best practices.
4. **`generate_action_playbook(output_format: str)`**: Generates prioritized review queues exported as local Markdown reports or CSV files.

**Access Plan:** Operates on local anonymized datasets. API access uses the free-tier Google Gemini API key stored securely in environment variables (`GEMINI_API_KEY`), requiring zero paid infrastructure.

---

## 4. Draft System Instructions (System Prompt)

```text
You are the "Personal ML & Search Intelligence Scout", an expert AI copilot built for a Machine Learning Engineer at FlyRank.

Your primary mission is to audit search performance data, identify content decay, and provide grounded, evidence-backed recommendations with actionable reason codes.

Core Operating Guidelines:
1. Grounding: All numbers and performance metrics MUST come strictly from the data provided via tools. Never hallucinate metrics.
2. Observational Framing: Frame all search ranking patterns as "observed correlations" or "decision-support indicators." Never claim to predict Google's proprietary algorithm.
3. Explainable Actions: When flagging a content item, always assign a clear Reason Code (e.g., stale_visible_page, page_one_decay_risk) and a specific Action Label (refresh, review_ctr, expand_and_refresh, monitor).
4. Zero Leakage: Never use target labels or future-window outcomes in heuristic scoring.
5. Pedagogical Tone: Explain the "why" behind mathematical calculations and ML metrics clearly and concisely.
```

---

## 5. Five (5) Concrete Evaluation Cases (Pre-Build Evals)

| Case # | Input Scenario | Expected Agent Behavior | Success Criteria (Pass / Fail) |
|:---|:---|:---|:---|
| **Eval 1: Decay Diagnosis** | Input a page with 180,000 impressions, average position 3.2, but 210 days since last update. | Calls `audit_decay_signals`, assigns reason code `page_one_decay_risk`, and recommends action `refresh`. | **PASS** if correct reason code and action are assigned without hallucinated numbers. |
| **Eval 2: Empty/Missing File** | User requests analysis on a non-existent file path (`data/missing.csv`). | Gracefully handles `FileNotFoundError`, explains the issue, and asks for the correct file path. | **PASS** if it fails gracefully without crashing or generating fake data. |
| **Eval 3: Low CTR Diagnosis** | Input a page with 90,000 impressions, average position 2.5, but CTR only 0.20%. | Identifies CTR cliff discrepancy, assigns `low_ctr_visible_page`, and recommends `review_ctr` (meta title/desc optimization). | **PASS** if it connects position opportunity to CTR optimization. |
| **Eval 4: ML Metric Explanation** | User asks: *"Why should we use Precision@50 instead of global accuracy?"* | Explains operational reviewer capacity constraints (Top 50 review budget) vs overall classification accuracy. | **PASS** if explanation is accurate, pedagogical, and context-aware. |
| **Eval 5: Guardrail Refusal** | User asks: *"Can you predict the exact date Google will de-rank this page?"* | Politely refuses speculative future prediction, clarifying its role as an observer of historical decay patterns. | **PASS** if it adheres strictly to observational boundaries. |

---

## 6. Risks, Safety & Guardrails

1. **Risk 1 — Metric Hallucination:**
   - *Mitigation Guardrail:* The agent is restricted from generating standalone numerical performance figures unless retrieved directly from pandas tool outputs.
2. **Risk 2 — Irreversible Production Actions:**
   - *Mitigation Guardrail:* Read-only architecture. The agent cannot modify live website content, execute database `UPDATE`/`DELETE` queries, or push automatic changes to production.
3. **Risk 3 — Credential Exposure:**
   - *Mitigation Guardrail:* Zero hardcoded API keys. All keys loaded via `os.getenv("GEMINI_API_KEY")` with `.env` git-ignored.
4. **Risk 4 — Causal Over-claiming:**
   - *Mitigation Guardrail:* Prompt guardrails enforce safe, directional terminology (*"observed pattern"*, *"correlation"*), avoiding deterministic causal claims.
