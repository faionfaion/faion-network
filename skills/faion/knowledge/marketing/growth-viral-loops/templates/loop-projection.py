# loop_projection.py — viral loop compounding model
# Shows whether assumed K + cycle time yields self-sustaining user growth

def project(starting_users: int, K: float, cycle_days: int, days: int) -> float:
    """
    K: viral coefficient per cycle (invites_per_user * conversion_rate).
    Returns estimated cumulative user count after `days` (naive model, assumes no churn).
    K >= 1 is exponential; K < 1 is geometric series (decaying contribution).
    """
    cycles = days / cycle_days
    if K >= 1:
        return starting_users * (K ** cycles)
    return starting_users * (1 - K ** (cycles + 1)) / (1 - K)


if __name__ == "__main__":
    print(f"{'K':>6}  {'cycle':>6}  {'90d':>10}  {'180d':>10}  {'365d':>10}")
    print("-" * 50)
    for K in (0.05, 0.10, 0.20, 0.30, 0.50, 0.70, 1.00):
        n90 = project(1000, K, cycle_days=14, days=90)
        n180 = project(1000, K, cycle_days=14, days=180)
        n365 = project(1000, K, cycle_days=14, days=365)
        print(f"{K:>6.2f}  {'14d':>6}  {n90:>10,.0f}  {n180:>10,.0f}  {n365:>10,.0f}")
    print("\nNote: model ignores churn; actual compounding is lower.")
    print("Category benchmarks: consumer K=0.10-0.30; B2B SaaS K=0.05-0.20")
