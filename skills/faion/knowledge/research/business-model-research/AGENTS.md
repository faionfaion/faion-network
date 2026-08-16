# Business Model Research

## Summary

**One-sentence:** Builds a Business Model Canvas (9 blocks, Hard/Soft tagged) with P10/P50/P90 unit economics and 5 stress tests, ending in a viable / viable-with-fixes / not-viable verdict.

**One-paragraph:** Systematic analysis of how a business will create, deliver, and capture value, structured as a Business Model Canvas (9 blocks) plus P10/P50/P90 unit economics (CAC, LTV, LTV:CAC, payback period) and 5 stress tests. Every Canvas cell is tagged Hard (sourced) or Soft (founder estimate); LTV is capped at a 60-month lifetime; the verdict reports on the P10 scenario, never the median.

**Ефективно для:**

- Pre-spec фаза: засновник має ідею, але не має захищеної monetization story.
- Pricing-рішення в умовах невизначеності: ARPU/margin/churn треба змоделювати до price page.
- Pivot review: продукт існує, але LTV:CAC < 3:1 і модель може бути зламана.
- Investor memo / seed deck з секцією 'How we make money' + stress tests.
- Multi-revenue-stream дизайн: subscription + usage + marketplace fee blend.

## Applies If (ALL must hold)

- Founder has a product idea but no defended monetization story.
- Pricing decision under uncertainty: ARPU, margin, and churn assumptions must be modeled before a price page ships.
- Pivot review: existing product is missing LTV:CAC >= 3:1 and the model itself may be broken.
- Investor memo / seed deck requires a 'How we make money' section with stress tests.
- Multi-revenue-stream design: subscription + usage + marketplace fee blends in one product.

## Skip If (ANY kills it)

- Internal tools, OSS side-projects, or hobby apps with no intent to monetize.
- Already-shipping product with 12+ months of real ARR data — use aarrr-pirate-metrics instead.
- Pure infrastructure libraries where revenue is a downstream consequence.
- Government or grant-funded work where the customer is a budget line, not a buyer.
- Two-sided marketplace pre-launch with zero supply — run network-effects discovery first.
- Hardware or regulated products where margin is dictated by BOM + compliance, not chosen.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Value-chain map | markdown / diagram | founder interview |
| Public competitor list | list with pricing URLs | competitor-analysis output |
| ARPU and churn assumptions | CSV with Hard/Soft tags | founder + comparables harvest |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[competitor-analysis]] | supplies comparable companies that ground ARPU and churn cells |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules + skip gate | ~1200 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix) | ~900 |
| `content/04-procedure.xml` | essential | 6-step procedure end-to-end | ~900 |
| `content/05-examples.xml` | essential | Worked example trace | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `value-chain-map` | sonnet | Structured diagramming with light judgment. |
| `comparable-harvesting` | haiku | Mechanical WebSearch + URL fetch. |
| `canvas-fill` | sonnet | Synthesis across 9 blocks with Hard/Soft tagging. |
| `unit-economics-compute` | sonnet | Formula application with P10/P50/P90 ranges. |
| `stress-test-verdict` | opus | Strategic interpretation of 5 stress tests + verdict. |

## Templates

| File | Purpose |
|------|---------|
| `templates/business-model-canvas.md.j2` | 9-block Canvas skeleton with Hard/Soft tagging |
| `templates/business-model-canvas.md` | 9-block Canvas skeleton with Hard/Soft tagging Generated from `templates/business-model-canvas.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/unit-econ-scenarios.sh` | P10/P50/P90 LTV:CAC + payback calculator from CLI arguments |
| `templates/business-model-report.md.j2` | Final report skeleton: Canvas + unit economics + stress tests + verdict |
| `templates/business-model-report.md` | Final report skeleton: Canvas + unit economics + stress tests + verdict Generated from `templates/business-model-report.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-business-model-research.py` | Validate the artefact against `content/02-output-contract.xml` schema | CI on each artefact change; pre-commit |

## Related

- [[competitor-analysis]]
- [[market-research-tam-sam-som]]
- [[distribution-channel-research]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals onto a rule id from `content/01-core-rules.xml`, so the agent can decide in one read whether to run the methodology, halt, or route elsewhere. Use it whenever the inputs feel ambiguous.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/unit-econ-scenarios.sh`

```bash
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
```
