#!/usr/bin/env bash
# portfolio-allocate.sh — compute current vs target horizon allocation from a CSV backlog.
# Usage: ./portfolio-allocate.sh backlog.csv stable
# CSV columns required: id, title, horizon (H1|H2|H3|?), eng_cost_usd
# Macro conditions: growth (60/25/15) | stable (70/20/10) | recession (80/15/5)
# Output: current allocation, target, drift_pp, and REBALANCE_NEEDED if drift > 3pp
set -euo pipefail
CSV="${1:?backlog.csv required}"
COND="${2:-stable}"  # growth | stable | recession
case "$COND" in
  growth)    TH1=60; TH2=25; TH3=15;;
  stable)    TH1=70; TH2=20; TH3=10;;
  recession) TH1=80; TH2=15; TH3=5;;
  *) echo "unknown condition: $COND (use growth|stable|recession)"; exit 2;;
esac
python3 - "$CSV" "$TH1" "$TH2" "$TH3" <<'PY'
import csv, sys
csv_path, th1, th2, th3 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
totals = {"H1": 0.0, "H2": 0.0, "H3": 0.0, "?": 0.0}
with open(csv_path) as f:
    for row in csv.DictReader(f):
        h = (row.get("horizon") or "?").strip().upper()
        cost = float(row.get("eng_cost_usd") or 0)
        totals[h if h in totals else "?"] += cost
known = sum(v for k, v in totals.items() if k != "?")
if known == 0:
    print("no classified items with eng_cost_usd -- run classifier first"); sys.exit(1)
pct = {h: round(100 * totals[h] / known, 1) for h in ("H1", "H2", "H3")}
print(f"current   H1={pct['H1']}%  H2={pct['H2']}%  H3={pct['H3']}%  unclassified=${totals['?']:.0f}")
print(f"target    H1={th1}%  H2={th2}%  H3={th3}%")
drift = {h: pct[h] - t for h, t in zip(("H1","H2","H3"), (th1,th2,th3))}
print(f"drift_pp  H1={drift['H1']:+.1f}  H2={drift['H2']:+.1f}  H3={drift['H3']:+.1f}")
if any(abs(drift[h]) > 3 for h in ("H1","H2","H3")):
    print("REBALANCE_NEEDED -- escalate to CPO for approval")
PY
