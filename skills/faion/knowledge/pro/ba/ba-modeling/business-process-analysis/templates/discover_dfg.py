#!/usr/bin/env python3
"""
discover_dfg.py — Discover a directly-follows graph from an event log CSV.

Outputs:
  out/dfg.svg          Directly-follows graph (frequency variant)
  out/stats.csv        Per-activity frequency and count

Usage:
  python discover_dfg.py events.csv --case-col case_id --act-col activity --ts-col timestamp
"""
import argparse, os
import pandas as pd
import pm4py
from pm4py.algo.discovery.dfg import algorithm as dfg_algo
from pm4py.visualization.dfg import visualizer as dfg_vis

p = argparse.ArgumentParser()
p.add_argument("csv")
p.add_argument("--case-col", default="case_id")
p.add_argument("--act-col", default="activity")
p.add_argument("--ts-col", default="timestamp")
p.add_argument("--out", default="out")
a = p.parse_args()

os.makedirs(a.out, exist_ok=True)
df = pd.read_csv(a.csv, parse_dates=[a.ts_col])
log = pm4py.format_dataframe(
    df, case_id=a.case_col, activity_key=a.act_col, timestamp_key=a.ts_col
)
dfg = dfg_algo.apply(log)
gviz = dfg_vis.apply(dfg, log=log, variant=dfg_vis.Variants.FREQUENCY)
dfg_vis.save(gviz, f"{a.out}/dfg.svg")

stats = (
    df.groupby(a.act_col)
      .agg(count=(a.case_col, "size"))
      .sort_values("count", ascending=False)
)
stats.to_csv(f"{a.out}/stats.csv")
print(f"Wrote {a.out}/dfg.svg and {a.out}/stats.csv")
print("Compare DFG against manually-built process map. Discrepancies = undiscovered workarounds.")
