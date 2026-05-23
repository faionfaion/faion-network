"""__faion_header__
purpose: Compute community health metrics from a Discord/Circle/Slack export.
consumes: platform activity CSV/JSON export
produces: JSON health-score dict (DAU/MAU, post rate, churn-risk members)
depends-on: AGENTS.md Task Routing (score_community_health → haiku)
token-budget-impact: ~500 tokens
"""

"""
Score community health from a Discord, Circle, or Slack activity export.

Input:  List of member activity records (from platform analytics export or API)
Output: Health score dict with DAU/MAU, post rate, churn risk members

Field requirements:
    member_id          str   unique member identifier
    posts_30d          int   number of posts in last 30 days
    replies_30d        int   number of replies in last 30 days
    last_active_days_ago  int  days since last activity (0 = today)
"""

from typing import TypedDict


class MemberActivity(TypedDict):
    member_id: str
    posts_30d: int
    replies_30d: int
    last_active_days_ago: int


def health_score(members: list[MemberActivity]) -> dict:
    """
    Compute community health metrics.

    Returns:
        health_score:       0-100 composite score (DAU/MAU * 50 + post_rate * 50)
        dau_mau:            ratio of active members (active = within 30 days)
        post_rate:          ratio of members who posted at least once in 30 days
        churn_risk_count:   members inactive 14+ days with zero posts
        churn_risk_members: list of churn-risk member IDs (first 10)

    Targets:
        health_score >= 50  → healthy
        dau_mau >= 0.20     → acceptable, >= 0.40 → great
        post_rate >= 0.10   → acceptable, >= 0.25 → great
    """
    total = len(members)
    if total == 0:
        return {"error": "no members provided"}

    active = sum(1 for m in members if m["last_active_days_ago"] <= 30)
    posters = sum(1 for m in members if m["posts_30d"] > 0)
    dau_mau = active / total
    post_rate = posters / total
    score = (dau_mau * 0.5 + post_rate * 0.5) * 100

    churn_risk = [
        m for m in members
        if m["last_active_days_ago"] > 14 and m["posts_30d"] == 0
    ]

    return {
        "health_score": round(score, 1),
        "dau_mau": round(dau_mau, 2),
        "post_rate": round(post_rate, 2),
        "churn_risk_count": len(churn_risk),
        "churn_risk_members": [m["member_id"] for m in churn_risk[:10]],
    }


# Usage example:
# members = [
#     {"member_id": "u1", "posts_30d": 3, "replies_30d": 5, "last_active_days_ago": 2},
#     {"member_id": "u2", "posts_30d": 0, "replies_30d": 0, "last_active_days_ago": 20},
# ]
# print(health_score(members))
