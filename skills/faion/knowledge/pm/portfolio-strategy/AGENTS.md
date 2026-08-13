# Portfolio Strategy (70/20/10)

## Summary

**One-sentence:** Three-horizon investment allocation (70% Core H1, 20% Adjacent H2, 10% Transformational H3) for a PM owning multiple shipped products; rebalances quarterly with explicit kill triggers.

**One-paragraph:** Tag each product H1/H2/H3 with rationale, enforce 70/20/10 ±5pp allocation, define horizon-appropriate kill triggers (H1 retention/activation, H2 no-PMF in 18mo, H3 no-signal in 36mo), and rebalance via written quarterly memo. Output: portfolio-allocation-record markdown + scorecard YAML.

**Ефективно для:**

- Single PM, який володіє >=2 shipped products із backlog collision.
- Promotion IC PM -> Group/Portfolio PM: рамка змінюється з feature-level на cross-product investment.
- Quarterly review: product-OKRs met, але portfolio розбалансовано (all H1, no H3).
- Handoff line між CPO portfolio strategy і PM-level execution.

## Applies If (ALL must hold)

- A single PM owns two or more shipped products and backlogs are starting to collide.
- Promoting an IC PM to Group PM / Portfolio PM.
- Two product squads both have defensible quarterly plans but the org cannot fund both at full speed.
- Defining the handoff line between portfolio strategy (CPO) and product PM execution.
- Quarterly review when product-level OKRs are met but the portfolio is unbalanced.

## Skip If (ANY kills it)

- Single-product team.
- Pre-PMF where horizon classification is premature.
- Agency / services where engagements are project-bound, not portfolio-bound.
- Existing portfolio memo <=90 days old without trigger events.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Product inventory | list with status + outcome metrics | PM / Head of Product |
| Capacity baseline | headcount / cost per product | finance |
| Last quarter portfolio memo | markdown | previous review |
| Kill-trigger candidates | list per horizon | team retro |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[product-lifecycle]] | Stage informs horizon classification. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology: 3-horizon allocation, per-product tag, kill triggers, quarterly rebalance, portfolio-vs-product roles | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for portfolio-allocation-record | 850 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: all-H1, untagged, no triggers, role confusion | 750 |
| `content/04-procedure.xml` | essential | 5-step procedure: tag -> allocate -> triggers -> memo -> review cadence | 800 |
| `content/06-decision-tree.xml` | essential | Apply/skip routing on portfolio existence + lifecycle stage | 650 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `horizon-tag` | sonnet | Tag each product with H1/H2/H3 + rationale. |
| `allocation-balance-check` | haiku | Compute current vs target ±5pp. |
| `rebalance-memo` | opus | Write the rebalance memo with kill/expand recommendations. |

## Templates

| File | Purpose |
|------|---------|
| `templates/portfolio-allocation-record.md` | Portfolio allocation memo skeleton with horizon tags + triggers. |
| `templates/pm-role-skew.sh` | Compute PM-vs-portfolio role split for each product. |
| `templates/prompt-portfolio-pm.txt` | Prompt template for the portfolio-PM allocation task. |
| `templates/prompt-product-pm.txt` | Prompt template for the product-PM consultation step. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-portfolio-strategy.py` | Validate the methodology output artefact against the schema in content/02-output-contract.xml | Pre-commit + CI on artefact changes |

## Related

- [[product-lifecycle]]
- [[stakeholder-management]]
- [[solo-pivot-decision-framework]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals to apply / skip / route-elsewhere, with each leaf referencing a rule id from `01-core-rules.xml`. Consult the tree before applying the methodology when signals are ambiguous.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/pm-role-skew.sh`

```bash
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
```

### `templates/prompt-portfolio-pm.txt`

```text
You are a portfolio PM. Inputs: list of products with {product_id, owner_pm,
quarterly_plan, eng_cost_usd, current_revenue_usd, lifecycle_stage, owner_count}.

Output JSON:
{
  per_product: [{product_id, recommended_horizon_mix:{h1,h2,h3}, rationale}],
  portfolio_total: {h1,h2,h3},
  pm_role_findings: [{owner_pm, role_mode, risk}],
  cuts: ["<product> H3 cut: <reason>", ...],
  reallocation_memo: "<= 6 bullets, plain English, names cuts and bets>"
}

Constraints:
  - Do NOT invent products not in the input.
  - If two PMs own overlapping scope (>30%), flag as role_conflict in pm_role_findings.
  - Never recommend >10% H3 for a product whose lifecycle_stage = "pre-PMF".
  - If owner_count = 1 and product count > 3, flag "headcount insufficient for stated allocation".
  - cuts: section must appear before reallocation_memo; name specific products and amounts.
  - Pick a side on any tie — do not split the difference; explain the rationale.
  - Use time_allocation field for role classification, not product count alone.
```

### `templates/prompt-product-pm.txt`

```text
You are a single-product PM defending allocation. Given your product's backlog
and the portfolio target {h1_target, h2_target, h3_target}, output JSON:
{
  agreed_cuts: [{item_id, reason}],
  contested_cuts: [{item_id, counter_argument, evidence_url}],
  cross_product_dependencies: [{item_id, depends_on_product, blocking_severity}]
}

Constraints:
  - Stay inside your product. Do not propose cuts to other products.
  - contested_cuts must cite evidence_url (ticket, doc, or research); unverified objections are invalid.
  - cross_product_dependencies must list the specific product and severity (blocks/enables/nice-to-have).
  - Do NOT invent items not in the backlog input.
```
