# 3-to-5 Minute Live Demo Script: Search Intelligence Scout Agent

- **Track:** General AI Fluency (FL-09)
- **Presenter:** Muhammad Akbar Pradana
- **Target Video Duration:** 3 to 5 minutes
- **Format:** Screen capture of active terminal running `python agent/search_scout_agent.py --demo` (no slide decks)

---

## Video Run-Down & Narration Plan

### Minute 0:00 - 0:45: The Problem & The Job to Be Done
- **Visual:** Terminal window in Visual Studio Code / Windows Terminal. Show repository structure with `agent/search_scout_agent.py`.
- **Narration:**
  > "Hello everyone. My name is Muhammad Akbar Pradana. During my internship at FlyRank, I worked on the search ranking intelligence problem. 
  > 
  > In enterprise digital publishing, companies often manage 30,000 or more live articles. But human content teams only have the bandwidth to review around 50 articles per sprint. 
  > 
  > To solve this operational bottleneck, I built this Personal Search Intelligence Scout Agent. Its job is to audit our 30,000-row search performance dataset, diagnose decaying content items, and generate actionable triage queues with transparent Reason Codes."

### Minute 0:45 - 2:00: Live End-to-End Execution
- **Visual:** Run `python agent/search_scout_agent.py --demo` in the terminal. Watch the 4 live outputs generate in real time.
- **Narration:**
  > "Let us run the automated live demo right now in the terminal.
  > 
  > First, the agent executes `tool_top_priority_queue(top_n=5)`. Notice the output: it dynamically ranks the most critical URLs using our non-leaking formula. Each row receives an explicit Reason Code, such as `page_one_decay_risk` or `low_ctr_visible_page`, plus a concrete action recommendation like `refresh` or `review_ctr`.
  > 
  > Second, in Demo 2, we query a specific article: `content_9532f197bbc8`. The agent calls `tool_audit_decay`. It inspects 309,000 impressions, average position 2.0, and 104 days since update, immediately flagging it for a metadata and content refresh."

### Minute 2:00 - 3:00: Key Design Decision (Transparency)
- **Visual:** Highlight `agent/tools.py` in the editor, showing the separation between tool logic and prompt orchestration.
- **Narration:**
  > "I want to highlight one key engineering decision I made during this build: **Strict Deterministic Grounding**.
  > 
  > Many AI agent demos allow a large language model to hallucinate numbers or invent traffic metrics. In my design, the LLM is never allowed to produce standalone numbers. All metric lookups, priority formulas, and decay thresholds are computed deterministically inside Python using Pandas. The reasoning engine only structures the explanation and handles intent routing. If a metric cannot be verified from the data file, the agent refuses to invent one."

### Minute 3:00 - 3:50: One Honest Limitation (On Camera)
- **Visual:** Scroll to the limitations section in `agent/README.md`.
- **Narration:**
  > "Now, to be completely transparent about one real limitation of this current build:
  > 
  > The agent currently operates on a static cross-sectional CSV export rather than a streaming live Google Search Console API. Because of this static window, the model cannot separate seasonal traffic drops from structural decay. For instance, a holiday gift guide might appear to decay simply because the season ended. In our production roadmap, this requires rolling time-partitioned DuckDB joins across the full 79-million-row warehouse."

### Minute 3:50 - 4:15: Conclusion & Reproducibility
- **Visual:** Show `https://github.com/Devaaldo/flyrank-ml` and `agent/README.md`.
- **Narration:**
  > "The complete agent code, tool functions, and reproducible evaluation benchmarks are open source in my GitHub repository under the `agent/` folder. Thank you for watching."
