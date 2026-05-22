---
slug: backlog-grooming-roadmapping
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A structured process for prioritizing backlogs using RICE scoring and MoSCoW categorization, translating the top-priority items into a Now/Next/Later roadmap.
content_id: "ed721940dbfde52b"
tags: [backlog, grooming, roadmap, prioritization, rice-scoring]
---
# Backlog Grooming and Roadmapping

## Summary

**One-sentence:** A structured process for prioritizing backlogs using RICE scoring and MoSCoW categorization, translating the top-priority items into a Now/Next/Later roadmap.

**One-paragraph:** A structured process for prioritizing backlogs using RICE scoring and MoSCoW categorization, translating the top-priority items into a Now/Next/Later roadmap. The grooming loop runs weekly: triage new ideas, re-score top 20, refine upcoming items, archive stale entries. Roadmaps are theme-based for solo projects and time-based for teams with committed delivery windows.

## Applies If (ALL must hold)

- Sprint kickoff: need to pick top N items from backlog for next cycle.
- Quarterly planning: produce a theme-based roadmap from raw backlog data.
- Backlog has grown past 20 unscored items.
- Product review: prioritize incoming requests from users or stakeholders.

## Skip If (ANY kills it)

- Single-task execution sessions where direction is already clear.
- Greenfield projects with no backlog yet. Use spec-requirements or write the first spec directly.
- When RICE inputs (Reach, Impact, Confidence) are pure guesses with no data. Flag as estimate-needed and do not rank.
- Real-time stakeholder negotiations. Async agent output does not substitute for live discussion.

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
