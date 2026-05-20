---
slug: business-process-analysis
tier: pro
group: ba
domain: ba-modeling
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: 5-stage analysis cycle for understanding how work actually flows through an organization: identify processes → document current state (with source citations) → analyze (value/time/cost tables) → design future state (diff table, not prose) → validate with stakeholders.
content_id: "aeace75b0feeb5c3"
tags: [business-process, bpmn, process-improvement, workflow, automation]
---
# Business Process Analysis

## Summary

**One-sentence:** 5-stage analysis cycle for understanding how work actually flows through an organization: identify processes → document current state (with source citations) → analyze (value/time/cost tables) → design future state (diff table, not prose) → validate with stakeholders.

**One-paragraph:** 5-stage analysis cycle for understanding how work actually flows through an organization: identify processes → document current state (with source citations) → analyze (value/time/cost tables) → design future state (diff table, not prose) → validate with stakeholders. Output artifacts are process-documentation.md and process-analysis.md; BPMN XML stored in version control alongside them.

## Applies If (ALL must hold)

- Raw process evidence exists (SOP docs, Slack threads, ticket histories, support transcripts) and a normalized model is needed before redesign.
- A cross-team workflow shows symptoms of waste: rework loops, long approval queues, dual data entry.
- Pre-automation discovery: before writing an n8n workflow, RPA bot, or backend service replacing a manual process.
- Pre-spec stage of a BA-heavy SDD feature: BPA output becomes input to requirements-documentation and acceptance-criteria.
- Compliance / audit prep where regulators expect a documented process map with controls and exception handling.

## Skip If (ANY kills it)

- Greenfield product where no current process exists — use use-case-modeling or user-story-mapping instead.
- One-off troubleshooting of a single broken instance — use 5-whys / fishbone root-cause tools.
- Tactical UI tweaks where the "process" is one click.
- Highly creative / knowledge-work flows (R&D, design, writing) where steps are non-deterministic.
- Team is already mid-redesign and stakeholders have agreed on future state — re-modelling as-is delays delivery.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `pro/ba/ba-modeling/`
