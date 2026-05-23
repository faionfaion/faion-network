def k_factor(invites_sent: int, signups_from_invites: int, active_referrers: int) -> dict:
    """
    Compute K-factor from referral event data.

    Args:
        invites_sent: Total invite events in the period
        signups_from_invites: Users who signed up via a referral link
        active_referrers: Users who sent at least one invite

    Returns:
        dict with keys: k, i (invites/referrer), c (conversion rate)
    """
    if active_referrers == 0:
        return {"k": 0, "i": 0, "c": 0}
    i = invites_sent / active_referrers
    c = signups_from_invites / max(invites_sent, 1)
    return {"k": round(i * c, 3), "i": round(i, 2), "c": round(c, 3)}


# Usage from agent:
# result = k_factor(invites_sent=4200, signups_from_invites=630, active_referrers=850)
# -> {"k": 0.741, "i": 4.94, "c": 0.15}  — near-viral

# NOTE: Do not report K computed on fewer than 500 invites; noise dominates at small samples.
# NOTE: Reward fulfillment must use unique (referrer_id, referee_id, event) key — never retry naked.
