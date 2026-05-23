# purpose: P10/P50/P90 LTV:CAC + payback calculator from CLI arguments
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-1500 tokens when loaded as context
#!/usr/bin/env bash
# unit-econ-scenarios.sh — emit P10 / P50 / P90 LTV:CAC and payback
# Usage: ./unit-econ-scenarios.sh <arpu> <margin> <churn> <cac>
# Example: ./unit-econ-scenarios.sh 29 0.80 0.03 50
# margin: 0-1 decimal (e.g. 0.80 = 80%)
# churn: monthly churn rate 0-1 (e.g. 0.03 = 3%)
set -euo pipefail

arpu=$1; margin=$2; churn=$3; cac=$4

python3 - <<PY
arpu, margin, churn, cac = $arpu, $margin, $churn, $cac

def ltv(a, m, c):
    # Cap lifetime at 60 months
    lifetime = min(1/c, 60) if c > 0 else 60
    return a * m * lifetime

def payback(c, a, m):
    return c / (a * m) if a * m > 0 else float('inf')

print(f"{'Scenario':<8} {'ARPU':>6} {'Churn':>6} {'CAC':>6} {'LTV':>8} {'LTV:CAC':>8} {'Payback':>8}")
print("-" * 58)

for label, arpu_mult, churn_mult, cac_mult in (
    ("P10", 0.7, 1.5, 1.3),   # pessimistic: lower ARPU, higher churn and CAC
    ("P50", 1.0, 1.0, 1.0),   # base
    ("P90", 1.3, 0.7, 0.8),   # optimistic: higher ARPU, lower churn and CAC
):
    a = arpu * arpu_mult
    c = churn * churn_mult
    cc = cac * cac_mult
    L = ltv(a, margin, c)
    ratio = L / cc if cc > 0 else float('inf')
    pb = payback(cc, a, margin)
    print(f"{label:<8} {a:>6.0f} {c:>6.3f} {cc:>6.0f} {L:>8.0f} {ratio:>7.1f}:1 {pb:>7.1f}mo")
PY
