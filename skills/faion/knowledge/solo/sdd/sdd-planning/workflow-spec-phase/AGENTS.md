---
slug: workflow-spec-phase
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Step-by-step procedures for the SDD specification phase: writing constitutions (two modes: existing codebase analysis vs.
content_id: "2e7fc9fe621df071"
tags: [specification, requirements, workflow, sdd, constitution]
---
# Workflow: Specification Phase

## Summary

**One-sentence:** Step-by-step procedures for the SDD specification phase: writing constitutions (two modes: existing codebase analysis vs.

**One-paragraph:** Step-by-step procedures for the SDD specification phase: writing constitutions (two modes: existing codebase analysis vs. Socratic dialogue for new projects), writing specifications (Brainstorm → Research → Clarify → Draft → Review → Save), backlog grooming with Definition of Ready, and roadmapping with confidence levels (90/70/50%). All workflows have human-in-loop checkpoints at section boundaries.

## Applies If (ALL must hold)

- Starting a new feature where requirements are unclear or only partially defined
- Existing codebase needs a constitution — tech decisions are implicit and undocumented
- Backlog grooming session where features need prioritization and DoR verification
- Roadmap needs a reality check against current feature status

## Skip If (ANY kills it)

- Feature is a bugfix with a single clear root cause — skip spec, go straight to task
- Requirements fully documented elsewhere (existing PRD) — extract, don't re-elicit
- Constitution already exists and team agrees — skip Mode 1 discovery
- Rapid prototype/spike where requirements will change after seeing output

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

- parent skill: `solo/sdd/sdd-planning/`
