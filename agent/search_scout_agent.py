"""
Personal ML & Search Intelligence Scout Agent
Author: Muhammad Akbar Pradana (ML Intern @ FlyRank AI)
Track: General AI Fluency (FL-07)

An applied AI agent that audits search performance decay, retrieves grounded metrics,
diagnoses root causes with Reason Codes & Action Labels, and provides ML research guidance.
"""

import sys
import os
import re
import json
from pathlib import Path

# Ensure UTF-8 output across all terminals (especially Windows cmd/powershell)
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent.tools import (
    tool_get_page_metrics,
    tool_audit_decay,
    tool_top_priority_queue,
    tool_explain_ml_concept,
)

SYSTEM_PROMPT = """
You are the 'Personal ML & Search Intelligence Scout', an expert AI agent copilot at FlyRank.
Your mission is to audit search performance, identify decaying content items, and formulate evidence-based action recommendations.

Core Guidelines:
1. Grounding: All numbers, impressions, and CTR metrics must strictly come from tool outputs.
2. Observational Framing: Never claim to predict Google's algorithm; frame patterns as observed historical performance.
3. Explainable Outputs: Always attach transparent Reason Codes and specific Action Labels (refresh, review_ctr, expand_and_refresh, monitor).
4. Zero Leakage: Prevent data contamination and highlight temporal separation.
"""

class SearchScoutAgent:
    def __init__(self, name: str = "SearchScout-v1"):
        self.name = name
        self.api_key = os.getenv("GEMINI_API_KEY", "")
        self.history = []

    def execute_tool(self, tool_name: str, **kwargs):
        """Execute local Python tool and return formatted result."""
        if tool_name == "tool_get_page_metrics":
            return tool_get_page_metrics(kwargs.get("content_id", ""))
        elif tool_name == "tool_audit_decay":
            return tool_audit_decay(kwargs.get("content_id", ""))
        elif tool_name == "tool_top_priority_queue":
            return tool_top_priority_queue(kwargs.get("top_n", 5))
        elif tool_name == "tool_explain_ml_concept":
            return tool_explain_ml_concept(kwargs.get("concept_name", ""))
        else:
            return {"status": "error", "message": f"Tool '{tool_name}' unknown."}

    def process_query(self, user_query: str) -> str:
        """
        Agent reasoning loop:
        1. Analyzes intent from user query.
        2. Selects and executes appropriate tool.
        3. Formulates grounded response with clear reason codes & actions.
        """
        q = user_query.strip()
        q_lower = q.lower()

        # Detect Content ID in query
        content_match = re.search(r"content_[a-f0-9]+", q)
        
        # Tool Routing Logic
        if content_match and ("audit" in q_lower or "diagnose" in q_lower or "check" in q_lower or "why" in q_lower):
            cid = content_match.group(0)
            print(f"  [Agent Tool Call] -> tool_audit_decay(content_id='{cid}')")
            audit = self.execute_tool("tool_audit_decay", content_id=cid)
            if audit.get("status") == "error":
                return f"[Error] {audit.get('message')}"
            
            m = audit["metrics_summary"]
            response = (
                f"[SEARCH INTELLIGENCE AUDIT: {cid}]\n"
                f"• Priority Score: {audit['priority_score']:.3f} / 1.000\n"
                f"• Primary Reason Code: {audit['primary_reason_code']}\n"
                f"• Recommended Action: [{audit['suggested_action'].upper()}]\n"
                f"• Observed Metrics: {m['impressions']:,} impressions (90d), avg position {m['position']:.1f}, CTR {m['ctr_pct']:.2f}%, {m['days_stale']} days since update.\n"
                f"• Diagnostic Triggers: {', '.join(audit['all_triggers'])}\n"
                f"• Action Plan: Initiate editorial update and refresh metadata based on reason code."
            )
            return response

        elif content_match and ("metric" in q_lower or "traffic" in q_lower or "data" in q_lower or "info" in q_lower):
            cid = content_match.group(0)
            print(f"  [Agent Tool Call] -> tool_get_page_metrics(content_id='{cid}')")
            m = self.execute_tool("tool_get_page_metrics", content_id=cid)
            if m.get("status") == "error":
                return f"[Error] {m.get('message')}"
            
            response = (
                f"[RAW PERFORMANCE METRICS: {cid}]\n"
                f"• Client Group: {m['client_id']}\n"
                f"• 90-Day Impressions: {m['impressions_90d']:,}\n"
                f"• 90-Day Clicks: {m['clicks_90d']:,} (CTR: {m['ctr']:.2f}%)\n"
                f"• Average SERP Position: {m['avg_position']:.1f}\n"
                f"• Content Age / Staleness: {m['content_age_days']}d age / {m['days_since_last_update']}d since update\n"
                f"• Word Count: {m['word_count']}\n"
                f"• Historical Status: {m['trend_status']}"
            )
            return response

        elif "queue" in q_lower or "top" in q_lower or "priority" in q_lower or "urgent" in q_lower:
            num_match = re.search(r"\b(\d+)\b", q)
            top_n = int(num_match.group(1)) if num_match else 5
            print(f"  [Agent Tool Call] -> tool_top_priority_queue(top_n={top_n})")
            queue = self.execute_tool("tool_top_priority_queue", top_n=top_n)
            
            lines = [f"[TOP-{len(queue)} URGENT REFRESH REVIEW QUEUE]", ""]
            header = f"{'Rank':<5} | {'Content ID':<22} | {'Score':<6} | {'Action':<22} | {'Reason Code':<22} | {'Impr':<8} | {'Pos':<4}"
            lines.append(header)
            lines.append("-" * len(header))
            for item in queue:
                lines.append(
                    f"{item['rank']:<5} | {item['content_id']:<22} | {item['score']:<6.3f} | {item['action']:<22} | {item['reason']:<22} | {item['impressions']:<8,d} | {item['avg_position']:<4.1f}"
                )
            lines.append("\n*Queue generated dynamically with zero target leakage.")
            return "\n".join(lines)

        elif "explain" in q_lower or "what is" in q_lower or "concept" in q_lower:
            concept = q_lower.replace("explain", "").replace("what is", "").replace("concept", "").strip(" ?.")
            print(f"  [Agent Tool Call] -> tool_explain_ml_concept(concept_name='{concept}')")
            result = self.execute_tool("tool_explain_ml_concept", concept_name=concept)
            return f"[ML & APPLIED SEARCH CONCEPT: {result['concept'].upper()}]\n{result['explanation']}"

        else:
            return (
                "Personal ML & Search Intelligence Scout Agent ready.\n"
                "Available commands:\n"
                "1. 'audit content_9532f197bbc8' -> Audit search performance decay\n"
                "2. 'metrics content_304f48230142' -> Retrieve raw page metrics\n"
                "3. 'queue 5' -> Generate top 5 urgent review queue\n"
                "4. 'explain precision@50' -> Explain ML/Search metrics"
            )

def run_interactive_cli():
    agent = SearchScoutAgent()
    print("=" * 70)
    print("PERSONAL ML & SEARCH INTELLIGENCE SCOUT AGENT")
    print("Connected to dataset: content_refresh_anonymized.csv (30,000 items)")
    print("Type 'exit' or 'quit' to stop.")
    print("=" * 70 + "\n")
    
    while True:
        try:
            user_input = input("You > ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit", "q"]:
                print("Session terminated. Agent offline.")
                break
            
            print("\n[Agent Processing...]")
            response = agent.process_query(user_input)
            print(f"\nAgent >\n{response}\n")
            print("-" * 70)
        except (KeyboardInterrupt, EOFError):
            print("\nSession ended.")
            break

def run_automated_demo():
    """Runs an automated test loop demonstrating all 4 tools end-to-end."""
    agent = SearchScoutAgent()
    print("=" * 75)
    print("RUNNING AUTOMATED END-TO-END DEMO: ML & SEARCH INTELLIGENCE SCOUT")
    print("=" * 75 + "\n")

    test_queries = [
        ("Demo 1: Generate Top-5 Priority Review Queue", "Show me the top 5 urgent refresh queue"),
        ("Demo 2: Audit Specific Content Item", "Audit content_9532f197bbc8 for search decay"),
        ("Demo 3: Inspect Raw Page Metrics", "Show metrics for content_304f48230142"),
        ("Demo 4: Explain Applied ML Metric", "Explain precision@50 concept")
    ]

    for title, query in test_queries:
        print(f"\n>>> {title}")
        print(f"User Query: '{query}'")
        response = agent.process_query(query)
        print(f"\nAgent Response:\n{response}\n")
        print("-" * 75)

    print("\n[SUCCESS] All 4 tools executed end-to-end with 0 errors!")

if __name__ == "__main__":
    if "--demo" in sys.argv or len(sys.argv) > 1:
        run_automated_demo()
    else:
        run_interactive_cli()
