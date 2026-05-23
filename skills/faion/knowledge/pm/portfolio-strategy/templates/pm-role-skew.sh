#!/usr/bin/env bash
# purpose: Compute PM-vs-portfolio role split for each product.
# consumes: input from methodology
# produces: artefact for downstream agent
# depends-on: content/02-output-contract.xml
# token-budget-impact: 0 (executes locally)
set -euo pipefail
#!/usr/bin/env bash
# pm-role-skew.sh — detect single-product vs portfolio PM patterns from allocation CSV.
# Input CSV columns: pm, product, horizon (H1/H2/H3), eng_cost_usd
# Usage: ./pm-role-skew.sh pm_allocations.csv
# Flags: h1-only-risk, h3-zombie-risk, bimodal-no-bridge, single-product, portfolio-PM
set -euo pipefail
CSV="${1:?pm_allocations.csv required}"
python3 - "$CSV" <<'PY'
import csv, sys, collections
path = sys.argv[1]
by_pm = collections.defaultdict(lambda: collections.Counter())
products = collections.defaultdict(set)
with open(path) as f:
    for r in csv.DictReader(f):
        pm, prod, h = r["pm"], r["product"], r["horizon"].upper()
        cost = float(r.get("eng_cost_usd") or 0)
        by_pm[pm][h] += cost
        products[pm].add(prod)
print(f"{'PM':<18}{'#prod':>6}{'H1%':>7}{'H2%':>7}{'H3%':>7}  flag")
for pm, mix in by_pm.items():
    total = sum(mix.values()) or 1
    h1, h2, h3 = (round(100*mix[k]/total, 1) for k in ("H1","H2","H3"))
    flag = []
    if len(products[pm]) == 1: flag.append("single-product")
    if len(products[pm]) >= 3: flag.append("portfolio-PM")
    if h1 >= 95: flag.append("h1-only-risk")
    if h3 >= 50: flag.append("h3-zombie-risk")
    if h2 < 5 and h1 > 0 and h3 > 0: flag.append("bimodal-no-bridge")
    print(f"{pm:<18}{len(products[pm]):>6}{h1:>7}{h2:>7}{h3:>7}  {','.join(flag) or 'ok'}")
PY
