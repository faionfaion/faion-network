#!/usr/bin/env bash
# stage-suggest.sh — first-pass lifecycle stage classification from MRR CSV
# Input:  CSV with columns: product_id,quarter,mrr_usd,churn_pct,gross_margin_pct
# Output: TSV: product_id\tstage\tconfidence\trationale
# Usage:  ./stage-suggest.sh products.csv
# Rows with confidence < 0.5 should be escalated to the LLM classifier prompt.
set -euo pipefail
CSV="${1:?Usage: stage-suggest.sh products.csv}"

python3 - "$CSV" <<'PY'
import csv, sys, collections, statistics

rows = list(csv.DictReader(open(sys.argv[1])))
by = collections.defaultdict(list)
for r in rows:
    by[r["product_id"]].append(r)

for pid, series in by.items():
    series.sort(key=lambda r: r["quarter"])
    if len(series) < 4:
        print(f"{pid}\tintro\t0.5\tinsufficient_history")
        continue
    mrr = [float(r["mrr_usd"]) for r in series]
    churn = statistics.mean(float(r["churn_pct"]) for r in series[-2:])
    yoy = (mrr[-1] - mrr[-5]) / mrr[-5] * 100 if len(mrr) >= 5 and mrr[-5] > 0 else None
    last_q_growth = (mrr[-1] - mrr[-2]) / mrr[-2] * 100 if mrr[-2] > 0 else 0

    if mrr[-1] < 10000 and yoy is None:
        stage, conf, why = "intro", 0.7, "low_mrr_short_history"
    elif yoy is not None and yoy >= 20 and last_q_growth > 0:
        stage, conf, why = "growth", 0.8, f"yoy={yoy:.0f}%"
    elif yoy is not None and 0 <= yoy < 15 and churn < 5:
        stage, conf, why = "maturity", 0.7, f"yoy={yoy:.0f}%_churn={churn:.1f}%"
    elif yoy is not None and yoy < 0:
        stage, conf, why = "decline", 0.8, f"yoy={yoy:.0f}%"
    else:
        stage, conf, why = "maturity", 0.4, "ambiguous_send_to_llm"

    print(f"{pid}\t{stage}\t{conf}\t{why}")
PY
