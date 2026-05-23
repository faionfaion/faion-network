#!/usr/bin/env python3
"""
purpose: Reference script computing calibration score against prior forecasts.
consumes: see content/02-output-contract.xml inputs for predictive-analytics-pm
produces: report
depends-on: content/01-core-rules.xml + content/02-output-contract.xml
token-budget-impact: ~200-1000 tokens when loaded as context
"""


"""calibration.py — check predicted-probability calibration on a holdout set.

Usage: python calibration.py holdout.parquet
Input parquet columns: y_true (0/1 int), y_prob (float 0..1)
Output: Brier score, calibration table, pass/fail (threshold: Brier < 0.20).
Exit 0 = calibration OK, exit 1 = fails threshold.
"""
from __future__ import annotations
import json
import sys

import pandas as pd
from sklearn.calibration import calibration_curve


def main(path: str) -> int:
    df = pd.read_parquet(path)  # cols: y_true (0/1), y_prob (0..1)
    prob_true, prob_pred = calibration_curve(
        df["y_true"], df["y_prob"], n_bins=10
    )
    brier = float(((df["y_prob"] - df["y_true"]) ** 2).mean())
    out = {
        "brier": brier,
        "calibration_table": list(
            zip(map(float, prob_pred), map(float, prob_true))
        ),
        "ok": brier < 0.20,  # threshold; tune per project
    }
    print(json.dumps(out, indent=2))
    if not out["ok"]:
        print(f"FAIL: Brier score {brier:.3f} exceeds threshold 0.20", file=sys.stderr)
    return 0 if out["ok"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
