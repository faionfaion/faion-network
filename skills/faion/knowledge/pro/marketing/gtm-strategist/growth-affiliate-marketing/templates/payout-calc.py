"""
payout.py — Compute monthly affiliate payout with refund holdback.

Input:  affiliate_id (str), charges (list of dicts with keys: id, affiliate_id,
        amount (int cents), created (datetime)), refunds (list of dicts with
        keys: charge_id)
Output: payout amount in dollars (float), rounded to 2 decimal places
"""
from datetime import datetime, timedelta


def monthly_payout(
    affiliate_id: str,
    charges: list[dict],
    refunds: list[dict],
    commission_rate: float = 0.30,
    holdback_days: int = 30,
) -> float:
    """Return the payable commission for affiliate_id after applying holdback."""
    cutoff = datetime.utcnow() - timedelta(days=holdback_days)
    eligible = [
        c for c in charges
        if c["affiliate_id"] == affiliate_id and c["created"] <= cutoff
    ]
    refunded_ids = {r["charge_id"] for r in refunds}
    eligible = [c for c in eligible if c["id"] not in refunded_ids]
    gross_dollars = sum(c["amount"] for c in eligible) / 100  # cents → dollars
    return round(gross_dollars * commission_rate, 2)
