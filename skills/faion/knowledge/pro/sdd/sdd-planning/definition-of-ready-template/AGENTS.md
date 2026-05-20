---
slug: definition-of-ready-template
tier: pro
group: sdd
domain: sdd-planning
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Definition-of-Ready checklist template that a story MUST pass before sprint commit — concrete artifact list, AC-quality, design link, dependency check, capacity reality-check.
content_id: "0986b0bda09edd82"
tags: [sdd, dor, scrum, definition-of-ready, sprint-planning, capacity-check]
---

# Definition of Ready Template

## Summary

**One-sentence:** A 7-item Definition-of-Ready checklist that gates whether a story enters the sprint, covering AC quality, artifact completeness, dependencies, capacity reality-check, and ownership.

**One-paragraph:** Backlog grooming exists in most teams; the DoR GATE — the explicit checkpoint that a story MUST pass before being pulled into the sprint — usually does not. Without it, sprint planning pulls in half-baked tickets and the team burns 20-40% of sprint capacity on clarification rounds and rework. Mechanism: a checklist (AC quality rubric pass, design link if UI-touching, dependency check, capacity reality-check, named PO + owner, success metric, NFR coverage) the story must satisfy. Primary output: a per-story DoR record + a sprint-level "ready set" before sprint planning starts.

## Applies If (ALL must hold)

- team uses Scrum / Kanban with sprint commitments OR a similar batched-commitment model
- backlog has 10+ stories at any time (DoR has no benefit on small backlogs)
- team has experienced sprint failure traceable to "story wasn't really ready" (clarification rounds, scope discovery mid-sprint)
- PO / product manager available for last-minute clarifications during the DoR pass

## Skip If (ANY kills it)

- pure outcome-based pull (Shape Up) — pitch quality replaces DoR; use pitch-quality methodology instead
- solo dev / PO same person — internal mental DoR is faster than formal gate
- continuous-flow team with no sprint boundary — story-level pull readiness is different; use pull-readiness methodology
- team will treat DoR as ceremony only and rubber-stamp — fix culture first (root cause: PM not held accountable for story quality)

## Prerequisites

- backlog with stories in some grooming state (refined / not-refined)
- AC quality rubric in use (`solo/product/product-planning/ac-quality-rubric`)
- design system / design-handoff conventions exist for UI-touching stories
- team velocity / capacity data available (last 3-5 sprints)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-planning/ac-quality-rubric` | DoR includes "ACs pass rubric"; consume the rubric output |
| `solo/ux/ui-designer/design-to-dev-handoff` | UI-touching stories require design handoff bundle; reference that contract |
| `geek/pm/project-manager/cross-role-handoff-protocol` | DoR is one specific role-pair handoff (PM -&gt; Dev); this methodology fills in the bundle |
| `pro/pm/project-manager/capacity-reality-check` | DoR includes capacity check; consume that methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: 7-item-coverage, no-sprint-without-pass, capacity-reality-check, PM-accountable-for-rejects, NFR-coverage | ~1000 |
| `content/02-output-contract.xml` | essential | DoR record schema + sprint-level ready-set contract + forbidden patterns | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes (rubber-stamp DoR, fake green capacity, mid-sprint smuggling, etc.) with detector + repair | ~1000 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `per_item_checklist_check` | sonnet | Run each of 7 items against the story's current state |
| `capacity_reality_check` | sonnet | Compare current sprint commit candidate vs trailing velocity |
| `dependency_graph_audit` | opus | Cross-story dependency analysis — synthesis over the candidate set |
| `dor_aggregation_decision` | haiku | Roll up per-story checks into a sprint-level ready set |

## Templates

| File | Purpose |
|------|---------|
| `templates/dor-checklist.md` | 7-item checklist template |
| `templates/dor-record.json` | JSON Schema for per-story DoR record |
| `templates/sprint-ready-set.json` | Schema for the aggregated sprint commit candidate |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/check-story-dor.py` | Runs the 7-item check, returns per-item pass/fail with reasons | At backlog refinement, end of refinement session, and again at sprint planning |
| `scripts/compute-ready-set.py` | Aggregates DoR records, applies capacity constraint, returns sprint-commit candidate | Before sprint planning meeting |

## Related

- parent skill: `pro/sdd/sdd-planning/`
- peer methodologies: `ac-quality-rubric`, `cross-role-handoff-protocol`, `capacity-reality-check`
- external: [Mike Cohn — Definition of Ready](https://www.mountaingoatsoftware.com/blog/the-definition-of-ready) · [Scrum Guide 2020](https://scrumguides.org/scrum-guide.html) · [Atlassian DoR Guide](https://www.atlassian.com/agile/scrum/definition-of-ready)
