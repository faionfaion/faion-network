"""
clg_health.py — compute DAU/MAU ratio and top-contributor digest.

Wire into Discord.py / Slack Bolt event stream.
Emit results to weekly report; surface alerts for any metric
that dropped more than 20% week-over-week.

Input: list of event dicts with keys: user_id (str), ts (datetime, UTC).
"""
from collections import Counter
from datetime import datetime, timedelta, timezone


def compute_health(events: list[dict]) -> dict:
    """
    Args:
        events: list of {"user_id": str, "ts": datetime (UTC)}

    Returns:
        dict with dau, wau, mau, dau_mau_ratio, top_contributors.
    """
    now = datetime.now(timezone.utc)
    d1 = now - timedelta(days=1)
    d7 = now - timedelta(days=7)
    d30 = now - timedelta(days=30)

    dau = {e["user_id"] for e in events if e["ts"] >= d1}
    wau = {e["user_id"] for e in events if e["ts"] >= d7}
    mau = {e["user_id"] for e in events if e["ts"] >= d30}

    contributors = Counter(e["user_id"] for e in events if e["ts"] >= d7)
    top = contributors.most_common(10)

    return {
        "dau": len(dau),
        "wau": len(wau),
        "mau": len(mau),
        # README target: 0.73 for Discord-native communities; 0.30 as floor.
        "dau_mau_ratio": round(len(dau) / max(len(mau), 1), 2),
        "top_contributors": top,
    }
