#!/usr/bin/env python3
"""
Van Westendorp Price Sensitivity Meter.
Input (stdin): CSV with columns: too_cheap, cheap, expensive, too_expensive
  (each row is one respondent's answers as dollar amounts)
Output (stdout): JSON with Optimal Price Point (OPP) and Indifference Price Point (IDP).
Requires: pandas (pip install pandas)
Usage: cat survey.csv | python3 van-westendorp.py
Note: Minimum N=30 respondents for statistically meaningful results.
"""
import json
import sys
import pandas as pd

df = pd.read_csv(sys.stdin)
n = len(df)

if n < 30:
    print(json.dumps({"error": f"N={n} is below minimum of 30; results are not statistically meaningful"}))
    sys.exit(1)

prices = sorted(set(df.values.ravel()))

def cumulative(col, operator):
    return [sum(operator(df[col], p)) / n for p in prices]

# Cumulative distributions
too_cheap_pct = cumulative("too_cheap", lambda c, p: c >= p)   # "not cheap enough" rises right
cheap_pct = cumulative("cheap", lambda c, p: c >= p)
expensive_pct = cumulative("expensive", lambda c, p: c <= p)
too_expensive_pct = cumulative("too_expensive", lambda c, p: c <= p)

def crossing_point(a, b):
    """Return the price where series a crosses series b."""
    for i in range(1, len(prices)):
        if (a[i - 1] - b[i - 1]) * (a[i] - b[i]) <= 0:
            return prices[i]
    return None

opp = crossing_point(too_cheap_pct, too_expensive_pct)
idp = crossing_point(cheap_pct, expensive_pct)

print(json.dumps({
    "n_respondents": n,
    "optimal_price_point_opp": opp,
    "indifference_price_point_idp": idp,
    "note": "OPP = intersection of too-cheap and too-expensive curves; IDP = acceptable-range midpoint",
}))
