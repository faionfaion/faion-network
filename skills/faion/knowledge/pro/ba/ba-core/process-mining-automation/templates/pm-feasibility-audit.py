#!/usr/bin/env python3
# pm-feasibility-audit.py — audit a CSV event log for process mining readiness.
# Usage: python pm-feasibility-audit.py log.csv
# Output: JSON with ready flag, stats, and recommended algorithm.
import sys
import json
import pandas as pd

df = pd.read_csv(sys.argv[1])
required = {"case_id", "activity", "timestamp"}
missing = required - set(df.columns)
if missing:
    print(json.dumps({"ready": False, "missing_columns": sorted(missing)}))
    sys.exit(1)

df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
ts_bad = int(df["timestamp"].isna().sum())
case_n = int(df["case_id"].nunique())
act_n = int(df["activity"].nunique())
events_per_case = df.groupby("case_id").size()
median_events = float(events_per_case.median())
trace = df.sort_values(["case_id", "timestamp"]).groupby("case_id")["activity"].apply(tuple)
variants = trace.value_counts()
variant_n = int(variants.size)
top10_share = float(variants.head(10).sum() / variants.sum())

verdict = (
    case_n >= 200
    and act_n >= 3
    and act_n <= 200
    and median_events >= 3
    and ts_bad / len(df) < 0.02
)

recommended = (
    "alpha" if act_n < 15 and variant_n < 30
    else "inductive-infrequent" if variant_n > 100
    else "heuristic"
)

print(json.dumps({
    "ready": verdict,
    "cases": case_n,
    "activities": act_n,
    "variants": variant_n,
    "median_events_per_case": median_events,
    "top10_variant_coverage": round(top10_share, 3),
    "bad_timestamps": ts_bad,
    "recommended_algorithm": recommended,
    "notes": {
        "alpha": "Suitable for clean logs with few activities and variants. Cannot handle loops or noise.",
        "heuristic": "Handles noise and loops but loses formal soundness guarantees.",
        "inductive-infrequent": "Guarantees soundness; trades fitness for precision on high-variant logs.",
    }.get(recommended, ""),
}, indent=2))
