# Solo Kpi Dashboard Template

## Summary

**One-sentence:** 5-KPI solo SaaS dashboard (signups, activation, paid conversion, churn, revenue) on one screen with weekly cadence, dashboard URL, and a Sunday review ritual that drives the WIP-1 bet.

**One-paragraph:** 5-KPI solo SaaS dashboard (signups, activation, paid conversion, churn, revenue) on one screen with weekly cadence, dashboard URL, and a Sunday review ritual that drives the WIP-1 bet. The methodology pins the artefact: a fixed shape, a named owner, evidence anchors, and a published review cadence. It is loaded when the role named in the trigger starts the block and produces a committed artefact reviewed against outcomes at the next iteration.

**Ефективно для:**

- Operators who run Solo Kpi Dashboard Template on a recurring cadence and need a reviewable operating tool.
- Solo founders who need a defensible artefact for stakeholder pressure.
- Teams syncing outcome work across PM, design, and engineering.
- Audit / review surface: every artefact has an owner, evidence anchors, and a decay date.

## Applies If (ALL must hold)

- Solo SaaS with live billing and ≥5 paying users.
- Owner runs a Sunday roadmap ritual.
- Analytics tool with weekly aggregation (Plausible / PostHog / Stripe).
- Owner wants ONE screen, not 14 tabs.

## Skip If (ANY kills it)

- Pre-launch with no users.
- Team of ≥3 with role-specific dashboards.
- Compliance-heavy product where regulator dashboards dominate.
- Multi-product portfolio — use portfolio dashboard.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Stripe billing instrumented | API key | Stripe |
| Web analytics instrumented | event taxonomy | Plausible / PostHog |
| KPI definitions agreed | doc | Self |
| Sunday review slot on calendar | calendar event | Self |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-operations/product-analytics` | Source instrumentation. |
| `solo/product/rice-for-one-person-cheatsheet` | Consumes the dashboard signal. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-solo-kpi-dashboard-template` | sonnet | Per-instance judgement; bounded inputs. |
| `validate-solo-kpi-dashboard-template` | haiku | Schema check + threshold checks; deterministic. |
| `review-solo-kpi-dashboard-template` | opus | Cross-cycle synthesis; high-stakes changes to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/solo-kpi-dashboard-template.json` | JSON skeleton conforming to the output contract schema. |
| `templates/solo-kpi-dashboard-template.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-solo-kpi-dashboard-template.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[product-analytics]]
- [[rice-for-one-person-cheatsheet]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
