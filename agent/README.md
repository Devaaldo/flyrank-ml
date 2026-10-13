# Personal ML & Search Intelligence Scout Agent

An applied AI tool-using agent built to triage enterprise content decay, calculate search opportunity scores, and automate search performance audits without hallucinated numbers.

- **Author:** Muhammad Akbar Pradana
- **Track:** General AI Fluency (FL-09 / Capstone Showcase)
- **Affiliation:** FlyRank AI Internship
- **Codebase:** `agent/search_scout_agent.py` and `agent/tools.py`

---

## 1. What It Does and For Whom

Digital marketing and SEO editorial teams manage portfolios with tens of thousands of published URLs, but human editors can only review roughly 50 pages during a weekly sprint. This agent acts as a dedicated triage co-pilot for a Machine Learning Engineer or Senior SEO Director.

Instead of asking a general language model to guess recommendations, this agent interfaces directly with a 30,000-row enterprise search dataset. It runs deterministic Python tools to identify high-traffic pages slipping down search results, categorizes each risk using transparent Reason Codes, and exports prioritized action queues.

---

## 2. Architecture Sketch

The agent follows an inspect-first ReAct tool loop. The reasoning layer interprets user intent and executes Python tools against local datasets, returning strictly verified data back to the prompt:

```text
[User Natural Query] 
        |
        v
[Agent Intent Classifier & ReAct Loop]
        |
        +---> Tool 1: tool_top_priority_queue(top_n=5)
        |       |--> Scans 30,000 rows, applies non-leaking priority formula
        |       +--> Returns ranked markdown table with Reason Codes
        |
        +---> Tool 2: tool_audit_decay(content_id)
        |       |--> Evaluates 90-day impressions, SERP position, and staleness
        |       +--> Diagnoses Page 1 decay vs striking-distance CTR loss
        |
        +---> Tool 3: tool_get_page_metrics(content_id)
        |       +--> Extracts ground-truth metrics from dataset
        |
        +---> Tool 4: tool_explain_ml_concept(concept_name)
                +--> Retrieves grounded definitions from local ML knowledge base
```

---

## 3. Setup and Installation

Follow these steps to run the agent in a clean environment:

### Prerequisites
- Python 3.10 or 3.11 installed
- Git installed

### Step-by-Step Setup
```bash
# 1. Clone the repository
git clone https://github.com/Devaaldo/flyrank-ml.git
cd flyrank-ml

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install required dependencies
pip install pandas numpy scikit-learn requests

# 4. Verify data file location
# Ensure data/raw/content_refresh_anonymized.csv exists in the repo root.
```

---

## 4. Usage Examples

### Automated Self-Check / Demo Run
To run all four core capabilities sequentially without human intervention:
```bash
python agent/search_scout_agent.py --demo
```

### Interactive CLI Mode
To run the interactive conversational agent:
```bash
python agent/search_scout_agent.py
```

### Sample Queries to Try in CLI
- `Show me the top 5 urgent refresh queue`
- `Audit content_9532f197bbc8 for search decay`
- `Show metrics for content_304f48230142`
- `Explain precision@50 concept`
- `exit` (to quit)

---

## 5. Evaluation Results (v2 Evals)

Five real evaluation scenarios were tested against the implementation:

| Eval Scenario | Test Input | Observed Agent Output | Result |
|---|---|---|---|
| **Eval 1: Decay Diagnosis** | "Audit content_9532f197bbc8" | Diagnosed score 0.740, assigned reason code `page_one_decay_risk`, recommended `[REFRESH]`. Matched raw data (309,192 impressions, pos 2.0). | **PASS** |
| **Eval 2: Missing File Handling** | Non-existent path or ID | Path resolution hierarchy searches `data/raw/` then fallback parent directories. Returns clean error without crashing. | **PASS** |
| **Eval 3: Low CTR Diagnosis** | Page with pos <= 10 and CTR < 1.0% | Correctly identified `low_ctr_visible_page`, recommended metadata and snippet review. | **PASS** |
| **Eval 4: Concept Explanation** | "Explain precision@50" | Returned grounded explanation mapped to the FlyRank capacity-constrained evaluation setup. | **PASS** |
| **Eval 5: Guardrail & Refusal** | Speculative ranking question | Agent confines its response to historical observational data and refuses causal ranking guarantees. | **PASS** |

---

## 6. Known Limitations

1. **Static Dataset Snapshot:** The tool currently operates on local cross-sectional CSV exports rather than streaming live Google Search Console API feeds.
2. **Heuristic Rule Ceiling:** The priority scoring tool uses weighted heuristic formulas. While calibrated against the L2 Logistic Regression findings (76% Precision@50), it does not run live online retraining.
3. **Keyword-Grounded Intent Routing:** Simple user queries are parsed through pattern matching and deterministic function dispatch before falling back to cloud LLM generation. This prioritizes speed and reproducibility over open-ended small talk.

---

## 7. Transparency Diligence (Human-in-the-Loop Disclosure)

In accordance with the General AI Fluency framework guidelines:

- **What AI Generated:** I used Claude to help scaffold initial agent boilerplate, write regular expression routing patterns, and convert analytical markdown notes into docstrings.
- **What I Validated and Wrote Myself:**
  - Designed the 4-tool taxonomy and decided the exact input/output data contracts.
  - Implemented the hierarchical fallback path resolution to prevent runtime failures across different operating systems.
  - Tested the terminal encoding guard on Windows (`sys.stdout.reconfigure`) after raw emoji outputs produced character encoding errors in cp1252.
  - Verified every single numerical value returned by the agent against direct Pandas queries on `data/raw/content_refresh_anonymized.csv`.
