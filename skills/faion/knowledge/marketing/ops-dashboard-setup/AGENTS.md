# Ops Dashboard Setup

## Summary

**One-sentence:** Generates a single-pane ops dashboard spec — KPI tree, freshness SLA, named owner per widget, alert thresholds — replacing fragmented per-tool reports that nobody checks.

**One-paragraph:** Ops Dashboard Setup produces a spec artefact with named owner, evidence anchors, and explicit gates so the practice survives review. The artefact is the contract — the methodology exists to keep that contract honest. Output: a validated spec ready for downstream automation or human sign-off.

**Ефективно для:**

- Solo founder reading metrics across ≥3 tools who needs ONE dashboard with ≤7 widgets, fresh ≤24h, with owner + alert per widget — before metric fatigue kills review cadence.

## Applies If (ALL must hold)

- Metrics live across ≥3 tools today (Stripe, ESP, analytics, CRM, …)
- There is a recurring review cadence (weekly or monthly)
- Founder commits to ≤7 KPIs (not a 40-widget vanity wall)

## Skip If (ANY kills it)

- Pre-revenue with no measurable KPIs — defer until product/market signal exists
- Single tool already exposes everything needed
- Enterprise data-platform context — different methodology

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| KPI tree (north-star → drivers) | doc | product/roadmap |
| Data sources (Stripe, GA, ESP, …) | list | tool inventory |
| Dashboard hosting (Metabase / Looker / Plausible / Notion) | service | infra inventory |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `plausible-analytics` | Sibling — one of the typical data sources. |
| `ops-automation-workflow` | Dashboards read automation health signals. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-single-pane, r2-max-7-widgets, r3-freshness-sla, r4-named-owner-per-widget, r5-alert-threshold-per-widget, r6-monthly-review | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-ops-dashboard-setup` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-ops-dashboard-setup` | haiku | Schema check + threshold checks; deterministic. |
| `review-ops-dashboard-setup` | opus | Cross-cycle synthesis; high-stakes change to copy / pricing / lifecycle. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ops-dashboard-setup.json` | JSON skeleton conforming to the output contract schema. |
| `templates/ops-dashboard-setup.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ops-dashboard-setup.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + monthly review. |

## Related

- [[plausible-analytics]]
- [[ops-automation-workflow]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
