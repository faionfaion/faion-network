"""
Pull active MRR from Stripe and calculate runway.
Requires: STRIPE_SECRET_KEY, MONTHLY_EXPENSES, CASH_BALANCE environment variables.

Usage:
  STRIPE_SECRET_KEY=sk_... MONTHLY_EXPENSES=5000 CASH_BALANCE=30000 python stripe-runway.py
"""
import os

import stripe

stripe.api_key = os.environ["STRIPE_SECRET_KEY"]

# Sum active monthly subscription MRR
subs = stripe.Subscription.list(status="active", limit=100)
mrr = 0.0
for s in subs.auto_paging_iter():
    items = s["items"]["data"]
    if not items:
        continue
    price = items[0]["price"]
    if price.get("recurring", {}).get("interval") == "month":
        mrr += price["unit_amount"] / 100
    elif price.get("recurring", {}).get("interval") == "year":
        mrr += price["unit_amount"] / 100 / 12

monthly_expenses = float(os.environ.get("MONTHLY_EXPENSES", "0"))
cash = float(os.environ.get("CASH_BALANCE", "0"))

net = mrr - monthly_expenses
runway = cash / monthly_expenses if monthly_expenses > 0 else float("inf")

print(f"MRR: ${mrr:,.0f}")
print(f"Monthly expenses: ${monthly_expenses:,.0f}")
print(f"Net monthly: ${net:+,.0f}")
print(f"Cash balance: ${cash:,.0f}")
print(f"Runway: {runway:.1f} months")

if runway < 3:
    print("WARNING: runway below 3 months — review expense cuts immediately")
elif runway < 6:
    print("CAUTION: runway below 6 months — review reinvestment allocation")
else:
    print("Runway OK")
