# purpose: PQL scoring model: weighted sum of activation + collaboration + usage signals
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~400-1000 tokens when loaded as context

"""Signal-weighted PQL scoring function.

Input: dict of boolean signals from user event data (aggregated, no PII).
Output: score and band (nurture / self_serve / sales).

Run weekly; output to user_pql table for sales routing.
Recalibrate thresholds monthly against actual close rates.
"""

SIGNALS: dict[str, tuple[int, str]] = {
    "weekly_actions_gte_100": (3, "high"),
    "invited_members_gte_5":  (3, "high"),
    "tried_gated_feature":    (3, "high"),
    "hours_in_product_gte_10": (2, "medium"),
    "integrations_gte_3":     (2, "medium"),
    "exported_or_shared":     (2, "medium"),
}


def score(user_events: dict[str, bool]) -> dict:
    """Return PQL score and routing band for a user's event summary."""
    total = sum(w for k, (w, _) in SIGNALS.items() if user_events.get(k))
    if total < 6:
        band = "nurture"
    elif total < 9:
        band = "self_serve"
    else:
        band = "sales"
    return {"score": total, "band": band}
