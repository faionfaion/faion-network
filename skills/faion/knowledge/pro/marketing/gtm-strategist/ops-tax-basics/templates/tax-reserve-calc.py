"""
Monthly tax-reserve calculator for US solopreneurs.

Inputs:
  revenue       -- total gross revenue this month
  deductible    -- deductible business expenses this month
  effective_rate -- estimated combined tax rate (default 0.30)

Output:
  dict with net_profit, reserve_usd, se_tax_estimate, note

IMPORTANT: output is a recommendation only. Never auto-sweep funds.
"""


def monthly_reserve(
    revenue: float, deductible: float, effective_rate: float = 0.30
) -> dict:
    net_profit = revenue - deductible
    if net_profit <= 0:
        return {"reserve_usd": 0, "note": "no profit; no reserve needed"}
    reserve = round(net_profit * effective_rate, 2)
    # SE tax on ~92.35% of net profit at 15.3%
    se_tax_estimate = round(net_profit * 0.9235 * 0.153, 2)
    return {
        "net_profit": round(net_profit, 2),
        "reserve_usd": reserve,
        "se_tax_estimate": se_tax_estimate,
        "note": (
            "Transfer reserve_usd to dedicated tax savings account. "
            "Do NOT auto-execute — human approval required."
        ),
    }


# Example usage:
# monthly_reserve(revenue=15000, deductible=3000)
# {'net_profit': 12000, 'reserve_usd': 3600, 'se_tax_estimate': 1692.33, ...}
