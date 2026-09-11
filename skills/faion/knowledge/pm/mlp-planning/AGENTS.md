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

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[product-analytics]] | Provides the retention curves the audit consumes. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 18 testable rules + skip-this-methodology: 4-layer audit, base-before-delight, evidence-required, retention-curve gate, bounded sprints, 4+ MLP threshold, polish-priority formula, layer-solid-before-next, the four layers defined, 1-5 rating scale, per-feature audit, four delight moments, explicit MLP criteria, gap analysis; background: what MLP is, MVP vs MLP | 2350 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for MLP plan | 1250 |
| `content/03-failure-modes.xml` | essential | 7 antipatterns: delight-on-broken-base, designer-opinion, unbounded-polish, missing curve target, cosmetic polish, context-blind delight, features-instead-of-polish | 1050 |
| `content/04-procedure.xml` | essential | 5-step procedure: audit -> score -> gate -> sprint -> measure; then the 5-step planning process: audit -> find delight moments -> prioritise -> write MLP criteria -> plan the gap; mlp-plan.md reference | 950 |
| `content/05-examples.xml` | medium | Worked MLP plan moving Day-30 retention 22% -> 38%, note-taking and invoicing upgrade cases, the five delight types | 900 |
| `content/06-decision-tree.xml` | essential | Apply/skip routing on retention + NPS + lifecycle stage, then per-feature audit and gap branches | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `layer-score` | sonnet | Score 4 layers with cited evidence. |
| `delight-backlog-author` | sonnet | Write delight backlog with verbatim citations. |
| `retention-curve-target` | haiku | Compute the curve target from baseline. |

## Templates

| File | Purpose |
|------|---------|
| `templates/mlp-plan.md.j2` | MLP plan skeleton with 4 layer scores + delight backlog + curve target. |
| `templates/mlp-plan.md` | MLP plan skeleton with 4 layer scores + delight backlog + curve target. Generated from `templates/mlp-plan.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/delight-sprint.md.j2` | Single-theme delight sprint plan template. |
| `templates/delight-sprint.md` | Single-theme delight sprint plan template. Generated from `templates/delight-sprint.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-mlp-planning.py` | Validate the methodology output artefact against the schema in content/02-output-contract.xml | Pre-commit + CI on artefact changes |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[product-analytics]]
- [[continuous-discovery-habits]]
- [[product-lifecycle]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals to apply / skip / route-elsewhere, with each leaf referencing a rule id from `01-core-rules.xml`. Consult the tree before applying the methodology when signals are ambiguous.
