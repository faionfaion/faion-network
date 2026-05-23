# MLP Planning

## Summary

**One-sentence:** Four-layer Minimum Lovable Product audit (Functional -> Reliable -> Usable -> Delightful) for evolving an MVP that users call 'fine' into one they love and recommend.

**One-paragraph:** Layer-by-layer audit scoring (0-5 each) with hard gates: no Delight investment when Functional/Reliable score <3. Delight items require verbatim user evidence; success metric is Day-30 retention curve, not feature throughput. Delight sprints are bounded (<=2 weeks, single named theme). Output: MLP plan markdown + retention-curve target.

**Ефективно для:**

- MVP shipped with measurable activation але Day-30 retention плато <25-30%.
- NPS <30 або churn-survey показує 'fine, але без emotion'.
- Pre-paid acquisition phase: кожен $ на non-lovable продукт компаундує CAC waste.
- Refactor sprint із explicit budget на polish, copy, мікро-інтеракції.

## Applies If (ALL must hold)

- MVP shipped with measurable activation but Day-30 retention plateaus below 25-30%.
- NPS < 30 or churn surveys show users finish the core job but describe the product as 'fine' or 'okay'.
- Retention curve flattens after week 2 — function works, emotion missing.
- About to enter a paid acquisition phase: every dollar spent on a non-lovable product compounds CAC waste.
- Refactor or redesign sprint with explicit budget for polish, copy, micro-interactions.

## Skip If (ANY kills it)

- Pre-MVP product where Functional layer is not yet shipped.
- Commodity product where price/distribution dominates over love.
- B2B procurement product where buyer != user and emotion has low signal.
- Day-30 retention already >40% — invest in growth, not lovability.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Day-30 retention curve | cohort table | product-analytics |
| NPS / CSAT recent survey | table | research / CS |
| User session recordings | links | Hotjar / Fullstory |
| Verbatim user quotes | list with participant_id | continuous-discovery output |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[product-analytics]] | Provides the retention curves the audit consumes. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology: 4-layer audit, base-before-delight, evidence-required, retention-curve gate, bounded sprints | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for MLP plan | 850 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: delight-on-broken-base, designer-opinion, unbounded-polish, missing curve target | 750 |
| `content/04-procedure.xml` | essential | 5-step procedure: audit -> score -> gate -> sprint -> measure | 800 |
| `content/05-examples.xml` | medium | Worked MLP plan moving Day-30 retention from 22% to 38% | 700 |
| `content/06-decision-tree.xml` | essential | Apply/skip routing on retention + NPS + lifecycle stage | 650 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `layer-score` | sonnet | Score 4 layers with cited evidence. |
| `delight-backlog-author` | sonnet | Write delight backlog with verbatim citations. |
| `retention-curve-target` | haiku | Compute the curve target from baseline. |

## Templates

| File | Purpose |
|------|---------|
| `templates/mlp-plan.md` | MLP plan skeleton with 4 layer scores + delight backlog + curve target. |
| `templates/delight-sprint.md` | Single-theme delight sprint plan template. |
| `templates/audit-to-backlog.sh` | Shell script converting layer scores to a prioritized delight backlog. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-mlp-planning.py` | Validate the methodology output artefact against the schema in content/02-output-contract.xml | Pre-commit + CI on artefact changes |

## Related

- [[product-analytics]]
- [[continuous-discovery-habits]]
- [[product-lifecycle]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals to apply / skip / route-elsewhere, with each leaf referencing a rule id from `01-core-rules.xml`. Consult the tree before applying the methodology when signals are ambiguous.
