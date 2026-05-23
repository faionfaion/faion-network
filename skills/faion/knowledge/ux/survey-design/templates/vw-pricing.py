# vw-pricing.py — Van Westendorp Price Sensitivity Meter analysis
# Input: responses.csv with columns: too_cheap, cheap, expensive, too_expensive
# Output: prints PMC, PME, OPP, IPP price points
# Usage: python vw-pricing.py responses.csv
# Requires: pip install pandas numpy

import sys

import numpy as np
import pandas as pd

df = pd.read_csv(sys.argv[1])
required = ["too_cheap", "cheap", "expensive", "too_expensive"]
missing = [c for c in required if c not in df.columns]
if missing:
    raise ValueError(f"Missing columns: {missing}")

all_prices = df[required].values.flatten()
prices = np.linspace(all_prices.min(), all_prices.max(), 200)


def cum_pct(col: str, ascending: bool) -> list[float]:
    """Cumulative % of respondents above or below each price point."""
    vals = df[col].dropna().values
    if ascending:
        return [(vals <= p).mean() for p in prices]
    else:
        return [(vals >= p).mean() for p in prices]


# Curves
too_cheap_curve = cum_pct("too_cheap", ascending=False)   # % saying "too cheap" at >= price
cheap_curve = cum_pct("cheap", ascending=False)            # % saying "acceptable cheap" at >= price
expensive_curve = cum_pct("expensive", ascending=True)     # % saying "expensive" at <= price
too_expensive_curve = cum_pct("too_expensive", ascending=True)  # % saying "too expensive" at <= price


def crossover(a: list[float], b: list[float]) -> float:
    """Price at which two curves cross (minimum absolute difference)."""
    diff = np.abs(np.array(a) - np.array(b))
    return float(prices[np.argmin(diff)])


pmc = crossover(too_cheap_curve, expensive_curve)
pme = crossover(cheap_curve, too_expensive_curve)
opp = crossover(too_cheap_curve, too_expensive_curve)
ipp = crossover(cheap_curve, expensive_curve)

print(f"N respondents: {len(df)}")
print(f"Point of Marginal Cheapness (PMC) — lower bound: ${pmc:.2f}")
print(f"Point of Marginal Expensiveness (PME) — upper bound: ${pme:.2f}")
print(f"Optimal Price Point (OPP) — minimum resistance: ${opp:.2f}")
print(f"Indifference Price Point (IPP) — expected price: ${ipp:.2f}")
print(f"Acceptable range: ${pmc:.2f} – ${pme:.2f}")
