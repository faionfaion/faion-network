"""
gtm_feasibility.py

Unit-economics check for a proposed GTM sales motion.
Validates whether ACV, CAC, and gross margin support the chosen motion.

Usage:
    result = gtm_motion_feasibility(
        motion="self-serve",
        acv_usd=1200,
        gross_margin=0.80,
        estimated_cac=300,
        churn_monthly=0.03,
    )
    # result: {"ok": True, "ltv": 3200.0, "payback_months": 3.1, "issues": []}
"""


def gtm_motion_feasibility(
    motion: str,
    acv_usd: float,
    gross_margin: float,
    estimated_cac: float,
    churn_monthly: float,
) -> dict:
    """Check if a GTM motion is feasible given unit economics."""
    ltv = (acv_usd / 12) * gross_margin / max(churn_monthly, 1e-6)
    monthly_gp = (acv_usd / 12) * gross_margin
    payback_months = estimated_cac / max(monthly_gp, 1e-6)

    rules = {
        "self-serve":   {"max_payback": 6,  "min_acv": 60,    "max_acv": 5_000},
        "sales-assist": {"max_payback": 12, "min_acv": 1_200, "max_acv": 30_000},
        "enterprise":   {"max_payback": 18, "min_acv": 25_000, "max_acv": 1e9},
    }

    r = rules.get(motion)
    if not r:
        return {"ok": False, "reason": f"unknown motion '{motion}'"}

    issues = []
    if payback_months > r["max_payback"]:
        issues.append(
            f"payback {payback_months:.1f}mo > {r['max_payback']}mo max for {motion}"
        )
    if not (r["min_acv"] <= acv_usd <= r["max_acv"]):
        issues.append(
            f"ACV ${acv_usd} outside [{r['min_acv']}, {r['max_acv']}] for {motion}"
        )

    return {
        "ok": len(issues) == 0,
        "ltv": round(ltv, 2),
        "payback_months": round(payback_months, 1),
        "issues": issues,
    }
