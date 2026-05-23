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
