# 🎙️ Explain It Like You Built It: ReAct Tool Calling & Anti-Hallucination

**Assignment:** Week 6 — Explain It Like You Built It  
**Track:** General AI Fluency | **Phase:** Build+  
**Author:** Muhammad Akbar Pradana (Machine Learning Intern @ FlyRank AI)  
**System Analyzed:** Personal ML & Search Intelligence Scout Agent (`agent/search_scout_agent.py` & `agent/tools.py`)  

---

## 1. What Part of the Build I Am Explaining
When building the **Personal ML & Search Intelligence Scout Agent** in Week 5 (FL-07), the mechanism I found most critical and interesting is the **ReAct (Reasoning + Acting) Tool Calling Loop** that allows a Language Model to query private tabular datasets without hallucinating numbers.

---

## 2. The Core Problem: Why Standard Chatbots Fail in Data Science
If you prompt a standard conversational LLM (like vanilla ChatGPT) with:
> *"What are the 90-day search impressions and SERP rank for content_9532f197bbc8?"*

The model will usually fabricate plausible-sounding, fake numbers. Because the model has no direct connection to private company datasets, its generative objective forces it to predict the most statistically probable sequence of tokens rather than factual truth.

---

## 3. How We Solved It: The 3-Step ReAct Tool Calling Architecture

In our implementation, we decoupled **natural language comprehension** from **factual data retrieval**:

```text
[1. User Command] ──► "Audit content_9532f197bbc8 for search decay"
                              │
                              ▼
[2. Intent Parser] ──► Extracts Entity ('content_9532f197bbc8') & Intent ('audit')
                              │
                              ▼
[3. Tool Dispatcher] ──► Executes local Python function: tool_audit_decay()
                              │
                              ▼
[4. Data Retrieval] ──► Opens 'content_refresh_anonymized.csv', computes heuristic scores
                              │
                              ▼
[5. Grounded Synthesis] ──► Outputs exact numbers (309k imp, pos 2.0) + Reason Code [page_one_decay_risk]
```

### Step 1: Entity & Intent Parsing (Reasoning)
When a user submits a query, regex and intent classification routers parse the request to determine:
1. Target content identifier (e.g., `content_[a-f0-9]+`).
2. Action intent (`audit`, `metrics`, `queue`, or `explain`).

### Step 2: Tool Execution (Acting)
Instead of guessing, the agent triggers a deterministic Python function:
- `tool_audit_decay(content_id="content_9532f197bbc8")`
- The function reads our 30,000-row pandas DataFrame, retrieves exact historical metrics (309,192 impressions, average position 2.0, 104 days stale), and computes the transparent priority score (`0.740`).

### Step 3: Structured Rationale & Guardrails (Observation)
The Python tool returns structured JSON back to the agent, which formats the response using predefined business logic:
- **Reason Code:** `page_one_decay_risk`
- **Action Label:** `[REFRESH]`
- **Data Grounding:** 100% of reported figures match the underlying dataset with zero hallucination.

---

## 4. Key Takeaways & Lessons Learned
1. **Separation of Concerns:** LLMs are superior at natural language parsing and summarization, but Python functions are superior at arithmetic, indexing, and tabular filtering.
2. **Human-in-the-Loop Ownership:** By writing custom tools with explicit error handling (e.g., handling `avg_position == 0` missing values and Windows UTF-8 terminal encoding), we ensure the system is production-safe and fully explainable.
