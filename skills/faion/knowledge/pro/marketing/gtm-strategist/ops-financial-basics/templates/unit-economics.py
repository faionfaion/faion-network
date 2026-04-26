"""
Unit-economics snapshot for SaaS / subscription products.

Inputs:
  arpu                -- average revenue per user per month ($)
  monthly_churn_rate  -- monthly churn as decimal (e.g. 0.05 for 5%)
  ad_spend            -- total marketing spend this period ($)
  new_customers       -- new customers acquired this period
  gross_margin        -- gross margin as decimal (e.g. 0.75 for 75%)

Output:
  dict with ltv, cac, ltv_cac, payback_months, healthy flag, and any alerts

NOTE: suppress this report below 100 paid customers (high noise floor).
Use Decimal arithmetic for all currency — float rounding compounds in aggregations.
"""

from decimal import Decimal


def unit_economics(
    arpu: float,
    monthly_churn_rate: float,
    ad_spend: float,
    new_customers: int,
    gross_margin: float,
) -> dict:
    if monthly_churn_rate <= 0 or new_customers <= 0:
        return {"error": "invalid inputs: churn_rate and new_customers must be positive"}

    arpu_d = Decimal(str(arpu))
    churn_d = Decimal(str(monthly_churn_rate))
    spend_d = Decimal(str(ad_spend))
    margin_d = Decimal(str(gross_margin))

    ltv = arpu_d / churn_d
    cac = spend_d / Decimal(new_customers)
    payback = cac / (arpu_d * margin_d) if arpu_d * margin_d > 0 else None

    alerts = []
    ltv_cac = ltv / cac if cac > 0 else None
    if ltv_cac and ltv_cac < 3:
        alerts.append("LTV:CAC < 3 — acquisition engine efficiency concern")
    if payback and payback > 12:
        alerts.append("Payback > 12 months — cash-flow risk")
    if gross_margin < 0.70:
        alerts.append("Gross margin < 70% — investigate COGS structure for SaaS")

    return {
        "ltv": float(round(ltv, 2)),
        "cac": float(round(cac, 2)),
        "ltv_cac": float(round(ltv_cac, 2)) if ltv_cac else None,
        "payback_months": float(round(payback, 1)) if payback else None,
        "gross_margin_pct": float(round(margin_d * 100, 1)),
        "healthy": len(alerts) == 0,
        "alerts": alerts,
    }


# Example:
# unit_economics(arpu=50, monthly_churn_rate=0.05,
#                ad_spend=5000, new_customers=50, gross_margin=0.75)
