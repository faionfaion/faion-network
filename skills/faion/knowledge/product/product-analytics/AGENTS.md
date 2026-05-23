# Product Analytics

## Summary

**One-sentence:** Stand up a minimum-viable analytics setup: NSM + 3-5 leading + 1 health metric, tracking plan, dashboard, and a weekly review tying numbers to product decisions.

**One-paragraph:** Analytics for a solo founder is not 'instrument everything'; it's 'instrument the metric that would change a decision'. The template forces a tracking plan written before instrumentation, a dashboard before queries, and a weekly review before redesign so the number serves the decision rather than the dashboard.

**Ефективно для:**

- Solo founder with traffic but no idea what to track; needs a 5-metric setup that feeds decisions, not vanity charts.

## Applies If (ALL must hold)

- Product has ≥1 user touchpoint generating events.
- Founder commits ≥1 hour/week to review the dashboard.
- Decisions can plausibly hinge on the metric movement.

## Skip If (ANY kills it)

- Pre-traffic phase (no events to track).
- Compliance restriction blocks event collection.
- Existing analytics already healthy — skip; tune instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Product surfaces inventory | list | Ops doc |
| NSM candidate list | list | Strategy doc |
| Analytics tool access | credential | Tool |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/weekly-growth-review-rhythm` | Cadence in which these metrics get reviewed. |
| `solo/product/product-manager/product-discovery` | Decisions fed by the metrics. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-product-analytics` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-product-analytics` | haiku | Schema check + threshold checks; deterministic. |
| `review-product-analytics` | opus | Cross-cycle synthesis; high-stakes change to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/product-analytics.json` | JSON skeleton conforming to the output contract schema. |
| `templates/product-analytics.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-product-analytics.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[weekly-growth-review-rhythm]]
- [[product-discovery]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
