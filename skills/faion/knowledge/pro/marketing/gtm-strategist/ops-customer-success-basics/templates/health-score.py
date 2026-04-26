"""
Minimal customer health score.

Components (max 100 points):
  usage     -- weekly login frequency (max 40)
  adoption  -- fraction of core features used (max 30)
  sentiment -- NPS or satisfaction proxy (max 20)
  billing   -- no failed payment (max 10)

Output:
  dict with score (0-100), band (green/yellow/red), and components

NOTE: re-calibrate thresholds after every significant product release.
"""


def health_score(account: dict) -> dict:
    """
    account dict keys:
      weekly_logins      -- int: logins in last 7 days
      features_used      -- int: distinct core features used in last 30 days
      total_core_features -- int: number of core features in product
      nps                -- int: last NPS score (-100 to 100), or None
      payment_failed     -- bool: True if most recent payment failed
    """
    # Usage: scale weekly_logins to target of 5 logins/week = max score
    usage = min(account.get("weekly_logins", 0) / 5.0, 1.0) * 40

    # Adoption: fraction of core features used
    total = account.get("total_core_features", 8)
    adoption = min(account.get("features_used", 0) / max(total, 1), 1.0) * 30

    # Sentiment: NPS -100..100 → 0..20
    nps = account.get("nps")
    if nps is not None:
        sentiment = ((nps + 100) / 200.0) * 20
    else:
        sentiment = 10.0  # neutral when no data

    # Billing: full points if no failed payment
    billing_ok = 0 if account.get("payment_failed") else 10

    score = usage + adoption + sentiment + billing_ok

    if score >= 75:
        band = "green"
    elif score >= 50:
        band = "yellow"
    else:
        band = "red"

    return {
        "score": round(score, 1),
        "band": band,
        "components": {
            "usage": round(usage, 1),
            "adoption": round(adoption, 1),
            "sentiment": round(sentiment, 1),
            "billing": billing_ok,
        },
    }


# Example:
# health_score({
#     "weekly_logins": 3,
#     "features_used": 5,
#     "total_core_features": 8,
#     "nps": 40,
#     "payment_failed": False,
# })
# {'score': 72.5, 'band': 'yellow', ...}
