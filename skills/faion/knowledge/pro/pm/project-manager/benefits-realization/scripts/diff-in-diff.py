#!/usr/bin/env python3
"""diff-in-diff.py — quick difference-in-differences for benefit attribution.

Estimates the Average Treatment Effect on the Treated (ATT) via OLS with
two-way fixed effects (unit and period). The treated:post coefficient = ATT.

CSV columns required: y (outcome), treated (0/1), post (0/1), period, unit

Usage:
    python diff-in-diff.py data.csv

Requirements: pandas, statsmodels
    pip install pandas statsmodels
"""
import sys
import pandas as pd
import statsmodels.formula.api as smf


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("Usage: diff-in-diff.py <data.csv>")

    df = pd.read_csv(sys.argv[1])
    required = {"y", "treated", "post", "period", "unit"}
    missing = required - set(df.columns)
    if missing:
        sys.exit(f"Missing columns: {missing}")

    model = smf.ols(
        "y ~ treated * post + C(period) + C(unit)",
        data=df,
    ).fit()

    print("Difference-in-Differences Results")
    print("=" * 50)
    print(model.summary().tables[1])
    print()

    if "treated:post" in model.params:
        att = model.params["treated:post"]
        ci = model.conf_int().loc["treated:post"]
        print(f"ATT (benefit attributable to intervention): {att:.4f}")
        print(f"95% CI: [{ci[0]:.4f}, {ci[1]:.4f}]")
    else:
        print("Note: treated:post interaction not found — check column values.")


if __name__ == "__main__":
    main()
