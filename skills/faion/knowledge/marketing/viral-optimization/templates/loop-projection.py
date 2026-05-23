# loop_projection.py — naive viral loop compounding model
# Shows whether assumed K + cycle time yields self-sustaining growth over a period

def project(starting_users: int, K: float, cycle_days: int, days: int) -> float:
    """
    K: viral coefficient (invites_per_user * conversion_rate) per cycle.
    Returns estimated total user count after `days` assuming no churn.
    """
    cycles = days / cycle_days
    if K >= 1:
        # Exponential growth
        return starting_users * (K ** cycles)
    # Geometric series sum (decaying contribution)
    total = starting_users * (1 - K ** (cycles + 1)) / (1 - K)
    return total


if __name__ == "__main__":
    print(f"{'K':>6}  {'cycle':>7}  {'180d users':>12}")
    print("-" * 30)
    for K in (0.05, 0.10, 0.20, 0.30, 0.50, 0.70, 1.00):
        n = project(1000, K, cycle_days=14, days=180)
        print(f"{K:>6.2f}  {'14d':>7}  {n:>12,.0f}")
