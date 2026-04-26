"""
at_risk.py — classify trial users by at-risk behavioral signals.

Input: trial_user dict from a warehouse mart_trial_users table.
Output: list of flag strings (empty = not at risk).

Flags map to Customer.io segments for targeted rescue campaigns.
All four flags require AND conditions — never OR. Validate trigger
logic before wiring to campaign platform.
"""


def at_risk(u: dict) -> list[str]:
    """
    Args:
        u: dict with keys:
            days_since_login       : int
            onboarding_complete    : bool
            features_used          : int  (distinct feature types used)
            team_invites_sent      : int
            is_team_product        : bool

    Returns:
        List of flag strings. Empty list = not at risk.
    """
    flags = []
    if u["days_since_login"] >= 3:
        flags.append("inactive_3d")
    if not u["onboarding_complete"]:
        flags.append("stuck_onboarding")
    if u["features_used"] <= 1:
        flags.append("low_breadth")
    if u["is_team_product"] and u["team_invites_sent"] == 0:
        flags.append("solo_in_team_product")
    return flags


# Route flags to specific Customer.io segments via API tags.
# Example campaign mapping:
#   inactive_3d         → "Did you get stuck?" email
#   stuck_onboarding    → Offer 1:1 setup call
#   low_breadth         → Feature education email
#   solo_in_team_product → Team-value social proof email
