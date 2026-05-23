---
slug: product-led-growth
tier: pro
group: product
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Metric-driven PLG loop (visitor -> signup -> activated -> PQL -> SQL -> paying -> expansion) with PM-owned aha-moment instrumentation, activation rituals, and expansion-revenue accountability.
content_id: "ae64906ad24e3542"
complexity: deep
produces: spec
est_tokens: 6700
tags: [product-led-growth, plg, activation, retention, pql, self-serve]
---
# Product-Led Growth (PM Angle)

## Summary

**One-sentence:** Metric-driven PLG loop (visitor -> signup -> activated -> PQL -> SQL -> paying -> expansion) with PM-owned aha-moment instrumentation, activation rituals, and expansion-revenue accountability.

**One-paragraph:** Define aha moment as a single event (or short sequence) reachable in <=10 minutes from signup; write PQL criteria; track free->paid conversion by activation cohort (not signup cohort); PM owns expansion revenue; cap concurrent activation experiments at 2 per funnel step. Output: plg-funnel-spec YAML + activation dashboard.

**Ефективно для:**

- Self-serve SaaS / API / dev-tool, де buyer = user.
- Sales-led продукт, що програє на CAC payback >18 місяців.
- Bottom-up wedge у enterprise account через individual sign-up.
- Продукт із вимірюваним aha-moment <=10 хв від signup до first value.

## Applies If (ALL must hold)

- New SaaS / API / dev-tool product where the buyer is also the user.
- Existing sales-led product losing on CAC payback (>18 months) — convert top-of-funnel to self-serve.
- Bottom-up wedge into an enterprise account: individual signs up free, expansion to team is the business model.
- Product has a measurable aha moment reachable in <10 minutes from signup.
- Pricing-page experimentation: PM owns activation funnel and runs PQL -> SQL conversion tests.

## Skip If (ANY kills it)

- Enterprise-sales-only product where buyer != user.
- B2B with no self-serve surface.
- Product where aha moment is structurally > 10 min (long onboarding) — fix onboarding first.
- Commodity product where price/distribution dominates and PLG is not the wedge.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Tracking plan | YAML | product-analytics |
| Signup -> aha funnel data | cohort table | BI |
| PQL criteria draft | YAML | PM |
| Sales hand-off SLA | doc | sales ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[product-analytics]] | Provides activation cohort + funnel instrumentation. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology: aha-instrumented, PQL written, activation-cohort tracking, expansion ownership, experiment throttle | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for plg-funnel-spec | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: aha-vague, PQL drift, signup-cohort conversion, expansion handed off | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: define aha -> instrument -> write PQL -> set cohort metrics -> run experiments | 900 |
| `content/05-examples.xml` | medium | Worked PLG loop for dev-tool with aha = first-successful-call | 800 |
| `content/06-decision-tree.xml` | essential | Apply/skip routing on buyer=user + aha feasibility + CAC payback | 650 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `aha-moment-extract` | sonnet | Define aha from spec + usage data. |
| `pql-criteria-author` | sonnet | Write the PQL criteria with hand-off triggers. |
| `activation-experiment-readout` | opus | Multi-cohort activation experiment synthesis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/plg-definitions.yml` | PLG terms + funnel stages + PQL criteria. |
| `templates/plg-snapshot.sh` | Weekly PLG snapshot script. |
| `templates/activation-experiment.yaml` | Activation-experiment hypothesis skeleton. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-product-led-growth.py` | Validate the methodology output artefact against the schema in content/02-output-contract.xml | Pre-commit + CI on artefact changes |

## Related

- [[product-analytics]]
- [[experimentation-at-scale]]
- [[feedback-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals to apply / skip / route-elsewhere, with each leaf referencing a rule id from `01-core-rules.xml`. Consult the tree before applying the methodology when signals are ambiguous.
