def simulate(initial: int, k: float, cycle_days: int, days: int) -> int:
    """
    Simulate user growth via viral loop over N days.

    Args:
        initial:     Starting user count
        k:           Viral coefficient (K = i x c)
        cycle_days:  Average days from signup to successful invite conversion
        days:        Total simulation window in days

    Returns:
        Total users at end of simulation
    """
    cycles = days // cycle_days
    users = initial
    for _ in range(cycles):
        users = users + int(users * k)
    return users


# Example: compare loop choices over 30 days, starting with 1,000 users
# WOM    (K=0.4, 7d cycle):  simulate(1000, 0.4, 7, 30) -> ~3,800
# Incentivized (K=0.8, 7d):  simulate(1000, 0.8, 7, 30) -> ~10,500
# Inherent (K=1.2, 3d cycle): simulate(1000, 1.2, 3, 30) -> ~74,000
