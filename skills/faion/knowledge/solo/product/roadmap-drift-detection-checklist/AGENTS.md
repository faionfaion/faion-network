---
slug: roadmap-drift-detection-checklist
tier: solo
group: product
domain: product
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Monthly checklist that catches roadmap drift before the quarter ends: tagged-vs-untagged work ratio, outcome-orphan tickets, stale candidate solutions, and confidence label decay — emits a drift report with action items.
content_id: "99463176e9ce4be7"
complexity: light
produces: checklist
est_tokens: 2900
tags: [roadmap, drift, monthly-review, audit]
---
# Roadmap Drift Detection Checklist

## Summary

**One-sentence:** Monthly checklist that catches roadmap drift before the quarter ends: tagged-vs-untagged work ratio, outcome-orphan tickets, stale candidate solutions, and confidence label decay — emits a drift report with action items.

**One-paragraph:** Monthly checklist that catches roadmap drift before the quarter ends: tagged-vs-untagged work ratio, outcome-orphan tickets, stale candidate solutions, and confidence label decay — emits a drift report with action items. The methodology pins the artefact: a fixed shape, a named owner, evidence anchors, and a published review cadence. It is loaded when the role named in the trigger starts the block and produces a committed artefact reviewed against outcomes at the next iteration.

**Ефективно для:**

- Operators who run Roadmap Drift Detection Checklist on a recurring cadence and need a reviewable operating tool.
- Solo founders who need a defensible artefact for stakeholder pressure.
- Teams syncing outcome work across PM, design, and engineering.
- Audit / review surface: every artefact has an owner, evidence anchors, and a decay date.

## Applies If (ALL must hold)

- Outcome-based roadmap is in place.
- Engineering backlog tags initiatives with outcome IDs.
- Monthly review cadence is scheduled.
- Owner has authority to re-prioritise or kill drifted bets.

## Skip If (ANY kills it)

- No outcome roadmap — nothing to drift from.
- Pure execution sprint — re-prioritisation off the table.
- Pre-PMF — drift is part of discovery.
- Single-bet operator — drift is just 'last week's idea'.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Outcome roadmap (current quarter) | doc | Roadmap |
| Engineering backlog export | CSV | Linear / Jira |
| Sprint completion data | metrics | Backlog tool |
| Outcome metric dashboard | URL | BI |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-planning/outcome-based-roadmaps` | Roadmap under audit. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 700 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-roadmap-drift-detection-checklist` | sonnet | Per-instance judgement; bounded inputs. |
| `validate-roadmap-drift-detection-checklist` | haiku | Schema check + threshold checks; deterministic. |
| `review-roadmap-drift-detection-checklist` | opus | Cross-cycle synthesis; high-stakes changes to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/roadmap-drift-detection-checklist.json` | JSON skeleton conforming to the output contract schema. |
| `templates/roadmap-drift-detection-checklist.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-roadmap-drift-detection-checklist.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[outcome-based-roadmaps]]
- [[okr-setting]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
