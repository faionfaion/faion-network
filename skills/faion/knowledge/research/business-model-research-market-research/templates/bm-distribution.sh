#!/usr/bin/env bash
# bm-distribution.sh — emit P25/P50/P75 per archetype from comps.csv
# Usage: ./bm-distribution.sh comps.csv
#
# comps.csv columns (with header):
#   name,archetype,stage,geo,arpu_usd,gross_margin,gross_retention,ndr,cac_payback_mo,source_url,filing_period,fx_rate,status
#
# Requires: pip install pandas tabulate
set -euo pipefail
csv=${1:?path to comps.csv required}

python3 - "$csv" <<'PY'
import sys
import pandas as pd

df = pd.read_csv(sys.argv[1])
required_cols = ["name","archetype","arpu_usd","gross_margin","gross_retention","ndr","cac_payback_mo"]
missing = [c for c in required_cols if c not in df.columns]
if missing:
    print(f"ERROR: missing columns: {missing}", file=sys.stderr)
    sys.exit(1)

metrics = ["arpu_usd","gross_margin","gross_retention","ndr","cac_payback_mo"]
n_per = df.groupby("archetype").size().to_dict()

# Warn about small archetypes
small = [k for k, v in n_per.items() if v < 3]
if small:
    print(f"WARNING: N<3 for archetypes {small} — treat as case studies, not benchmarks")

# Survivorship check
if "status" in df.columns:
    dead_pct = (df["status"].str.lower().isin(["closed","acquired"])).mean()
    if dead_pct < 0.10:
        print(f"WARNING: only {dead_pct:.0%} of comps are dead/acquired — survivorship bias likely")

# Distribution table
dist = (df.groupby("archetype")[metrics]
          .quantile([0.25, 0.5, 0.75])
          .unstack(level=-1)
          .round(1))
dist.columns = [f"{m}_p{int(q*100)}" for m, q in dist.columns]
dist["n"] = [n_per.get(a, 0) for a in dist.index]

try:
    print(dist.to_markdown())
except ImportError:
    print(dist.to_string())

print(f"\nTotal comps: {len(df)}")
print(f"N per archetype: {n_per}")
PY
