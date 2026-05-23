# purpose: Compute ZOPA from reserves + render summary
# consumes: my_reserve, their_reserve
# produces: ZOPA report
# depends-on: stdlib only
# token-budget-impact: 0 (runs locally)

def zopa(my_walk_away: float, their_walk_away: float, i_am_buyer: bool = True):
    """
    Compute the Zone of Possible Agreement (ZOPA).

    Args:
        my_walk_away:     the worst deal I will accept
        their_walk_away:  the worst deal they will accept (estimated)
        i_am_buyer:       True if I am buying (my_walk_away is a max price),
                          False if I am selling (my_walk_away is a min price)

    Returns:
        (low, high) tuple if ZOPA exists, None if no deal is possible.

    Notes:
        - If None is returned, creative options or BATNA improvement are needed
          before entering negotiation.
        - Values are monetary but the function works for any numeric scale.
    """
    if i_am_buyer:
        low = their_walk_away   # seller's minimum
        high = my_walk_away     # buyer's maximum
    else:
        low = my_walk_away      # seller's minimum
        high = their_walk_away  # buyer's maximum

    if low <= high:
        return (low, high)
    return None  # no ZOPA — negotiation cannot close at current positions


# Usage examples:
#
# Salary negotiation (I am the candidate = seller of labor):
# result = zopa(my_walk_away=80_000, their_walk_away=105_000, i_am_buyer=False)
# print(result)  # (80000, 105000) — deal possible, aim for top of range
#
# Vendor purchase (I am the buyer):
# result = zopa(my_walk_away=50_000, their_walk_away=45_000, i_am_buyer=True)
# print(result)  # (45000, 50000) — deal possible
#
# result = zopa(my_walk_away=40_000, their_walk_away=60_000, i_am_buyer=True)
# print(result)  # None — no overlap, need creative options
