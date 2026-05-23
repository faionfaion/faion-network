"""
US federal quarterly estimated tax calculator — safe-harbor method.

Computes the quarterly payment target using both:
  (1) Safe-harbor: 100% of prior-year tax (110% if prior AGI > $150K)
  (2) Current-year estimate: current YTD profit annualized x ~30% blended rate

Output: higher of the two amounts (safe-harbor protects against underpayment penalty)

IMPORTANT: This is a planning tool only. For actual filings, consult a CPA.
Rates, brackets, and thresholds change annually — verify against current IRS Pub 505.

Usage:
    result = quarterly_estimate(
        prior_year_tax=24000,
        prior_year_agi=145000,
        current_ytd_profit=80000,
        ytd_quarter=2,
        paid_prior_quarters=6000,
    )
    print(result)
"""


def quarterly_estimate(
    prior_year_tax: float,
    prior_year_agi: float,
    current_ytd_profit: float,
    ytd_quarter: int,
    paid_prior_quarters: float = 0.0,
) -> dict:
    # Safe-harbor method
    multiplier = 1.10 if prior_year_agi > 150_000 else 1.00
    safe_harbor_annual = prior_year_tax * multiplier
    safe_harbor_q = safe_harbor_annual / 4

    # Current-year method: annualize YTD profit, apply blended ~30% rate
    # Blended rate accounts for SE tax (15.3%) + estimated income tax
    annualized_profit = current_ytd_profit * (4 / ytd_quarter)
    current_year_annual = annualized_profit * 0.30
    current_year_q = current_year_annual / 4

    # Use the higher of the two to ensure safe harbor is met
    target_q = max(safe_harbor_q, current_year_q)

    # Subtract what was already paid in prior quarters of this year
    this_quarter_payment = max(0.0, target_q - paid_prior_quarters / ytd_quarter)

    return {
        "safe_harbor_annual": round(safe_harbor_annual, 2),
        "safe_harbor_quarterly": round(safe_harbor_q, 2),
        "current_year_annual_estimate": round(current_year_annual, 2),
        "current_year_quarterly": round(current_year_q, 2),
        "recommended_quarterly": round(target_q, 2),
        "this_quarter_payment": round(this_quarter_payment, 2),
        "note": (
            "110% safe-harbor applies (prior AGI > $150K)"
            if prior_year_agi > 150_000
            else "100% safe-harbor applies"
        ),
    }


if __name__ == "__main__":
    example = quarterly_estimate(
        prior_year_tax=24_000,
        prior_year_agi=145_000,
        current_ytd_profit=80_000,
        ytd_quarter=2,
        paid_prior_quarters=6_000,
    )
    for k, v in example.items():
        print(f"{k}: {v}")
