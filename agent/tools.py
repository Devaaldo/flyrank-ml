"""
Tools module for the Personal ML & Search Intelligence Scout Agent.
Interfaces with local search performance datasets and domain heuristic rules.
"""

from pathlib import Path
import numpy as np
import pandas as pd

# Resolve dataset path dynamically
DATA_PATH = Path("data/raw/content_refresh_anonymized.csv")
if not DATA_PATH.exists():
    DATA_PATH = Path("../data/raw/content_refresh_anonymized.csv")
if not DATA_PATH.exists():
    DATA_PATH = Path("../../data/raw/content_refresh_anonymized.csv")

def _load_data() -> pd.DataFrame:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found at {DATA_PATH}. Please ensure content_refresh_anonymized.csv is present.")
    df = pd.read_csv(DATA_PATH)
    df["is_declining_label"] = (df["trend_direction"] == "down").astype(int)
    return df

def tool_get_page_metrics(content_id: str) -> dict:
    """
    Retrieve real 90-day search performance metrics for a specific content item.
    """
    df = _load_data()
    row = df[df["content_id"] == content_id.strip()]
    if row.empty:
        return {"status": "error", "message": f"Content ID '{content_id}' not found in dataset."}
    
    r = row.iloc[0]
    return {
        "status": "success",
        "content_id": str(r["content_id"]),
        "client_id": str(r["client_id"]),
        "impressions_90d": int(r["impressions_90d"]) if pd.notnull(r["impressions_90d"]) else 0,
        "clicks_90d": int(r["clicks_90d"]) if pd.notnull(r["clicks_90d"]) else 0,
        "avg_position": float(r["avg_position"]) if pd.notnull(r["avg_position"]) else 0.0,
        "ctr": float(r["ctr"]) if pd.notnull(r["ctr"]) else 0.0,
        "days_since_last_update": int(r["days_since_last_update"]) if pd.notnull(r["days_since_last_update"]) else 0,
        "content_age_days": int(r["content_age_days"]) if pd.notnull(r["content_age_days"]) else 0,
        "word_count": int(r["word_count"]) if pd.notnull(r["word_count"]) and r["word_count"] > 0 else "Unknown/Thin",
        "trend_status": "Observed Decline" if r["is_declining_label"] == 1 else "Observed Stable/Growth"
    }

def tool_audit_decay(content_id: str) -> dict:
    """
    Audit an item for search performance decay, diagnose root cause, and assign Reason Code & Action Label.
    """
    metrics = tool_get_page_metrics(content_id)
    if metrics.get("status") == "error":
        return metrics
    
    impr = metrics["impressions_90d"]
    pos = metrics["avg_position"]
    ctr = metrics["ctr"]
    stale = metrics["days_since_last_update"]
    age = metrics["content_age_days"]
    word_count = metrics["word_count"] if isinstance(metrics["word_count"], int) else 0

    reasons = []
    actions = []

    # Heuristic diagnostic rules
    if stale >= 180 and impr >= 500:
        reasons.append("stale_visible_page")
        actions.append("refresh")
    
    if 0 < pos <= 10 and age >= 180:
        reasons.append("page_one_decay_risk")
        actions.append("refresh")

    if impr >= 500 and 0 < pos <= 20 and ctr < 0.5:
        reasons.append("low_ctr_visible_page")
        actions.append("refresh_and_review_ctr")

    if 0 < word_count < 1200 and impr >= 250:
        reasons.append("thin_visible_page")
        actions.append("expand_and_refresh")

    if not reasons:
        reasons.append("general_refresh_review")
        actions.append("monitor")

    primary_reason = reasons[0]
    primary_action = actions[0]

    # Calculate transparent priority score
    visibility_score = min(1.0, np.log1p(impr) / np.log1p(100000))
    freshness_score = min(1.0, stale / 365.0)
    pos_score = (1.0 - (min(50.0, max(1.0, pos)) / 50.0)) if pos > 0 else 0.0

    priority_score = round(0.40 * visibility_score + 0.35 * freshness_score + 0.25 * pos_score, 3)

    return {
        "status": "success",
        "content_id": content_id,
        "priority_score": priority_score,
        "primary_reason_code": primary_reason,
        "suggested_action": primary_action,
        "all_triggers": reasons,
        "metrics_summary": {
            "impressions": impr,
            "position": pos,
            "ctr_pct": ctr,
            "days_stale": stale
        }
    }

def tool_top_priority_queue(top_n: int = 5) -> list[dict]:
    """
    Generate the top-N urgent content refresh queue from the active dataset.
    """
    df = _load_data()
    top_n = max(1, min(20, top_n))
    
    # Calculate scores on the fly
    vis = df["impressions_90d"].rank(pct=True).fillna(0)
    fresh = df["days_since_last_update"].rank(pct=True).fillna(0)
    pos_clean = df["avg_position"].clip(lower=1, upper=50)
    pos_norm = 1.0 - ((pos_clean - 1) / 49.0)
    has_pos = (df["avg_position"] > 0).astype(int)
    pos_score = pos_norm * vis * has_pos

    df["calc_score"] = (0.40 * vis + 0.35 * fresh + 0.25 * pos_score).round(3)
    sorted_df = df.sort_values("calc_score", ascending=False).head(top_n)

    queue = []
    for rank, (_, row) in enumerate(sorted_df.iterrows(), start=1):
        audit = tool_audit_decay(row["content_id"])
        queue.append({
            "rank": rank,
            "content_id": row["content_id"],
            "score": float(row["calc_score"]),
            "action": audit.get("suggested_action", "refresh"),
            "reason": audit.get("primary_reason_code", "general_review"),
            "impressions": int(row["impressions_90d"]),
            "avg_position": float(row["avg_position"]),
            "status": "Declining" if row["is_declining_label"] == 1 else "Stable"
        })
    return queue

def tool_explain_ml_concept(concept_name: str) -> dict:
    """
    Provides grounded knowledge base definitions for key ML and search intelligence concepts.
    """
    knowledge = {
        "precision@k": (
            "Precision@K measures the proportion of positive targets (e.g., truly declining content) "
            "within the Top-K items recommended by a ranking model. For instance, Precision@50 evaluates "
            "the accuracy of the top 50 prioritized pages, matching the real weekly capacity of an editorial review team."
        ),
        "target_leakage": (
            "Target leakage occurs when information from the future outcome or prediction target "
            "(such as 'trend_direction' or 'trend_pct') is mistakenly included as an input feature during model training, "
            "artificially inflating training accuracy while failing in production."
        ),
        "client_holdout_split": (
            "A validation split strategy where ~20% of unique client organizations are entirely held out in the test set. "
            "This ensures the model is evaluated on unseen domains, testing true cross-client generalization without organizational leakage."
        ),
        "baseline_heuristics": (
            "A transparent, rule-based scoring method without machine-learned weights. It acts as an explainable, "
            "production-safe benchmark that subsequent ML models must statistically outperform."
        )
    }
    
    query = concept_name.lower().strip().replace(" ", "_")
    for key, val in knowledge.items():
        if query in key or key in query:
            return {"concept": key, "explanation": val}
            
    return {
        "concept": concept_name,
        "explanation": f"Concept '{concept_name}' is tracked in the FlyRank ML framework as an applied search intelligence component."
    }
