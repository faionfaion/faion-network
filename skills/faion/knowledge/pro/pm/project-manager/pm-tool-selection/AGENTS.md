---
slug: pm-tool-selection
tier: pro
group: pm
domain: project-manager
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Structured evaluation framework for selecting or replacing a project management tool.
content_id: "fef0da537f092bf5"
tags: [pm-tools, evaluation, procurement, tco, decision-making]
---
# PM Tool Selection Framework

## Summary

**One-sentence:** Structured evaluation framework for selecting or replacing a project management tool.

**One-paragraph:** Structured evaluation framework for selecting or replacing a project management tool. Gather requirements via MoSCoW matrix, run a time-boxed 2-week POC on real project data, score tools against weighted criteria, compute 3-year TCO, and document the decision as an ADR. Human sign-off is mandatory at requirements, POC scoring, and final decision — agents must not pick the tool unilaterally.

## Applies If (ALL must hold)

- New team picking a first PM tool, or current tool causing documented friction
- Vendor renewal cycle where a price jump triggers re-evaluation
- Post-acquisition consolidation across two tool stacks
- Compliance shift (SOC2, HIPAA, EU data residency) forcing reassessment

## Skip If (ANY kills it)

- Teams under 5 people with simple workflow — pick GitHub Projects or Linear free tier, skip the matrix
- Mid-project under deadline pressure — switching tools mid-flight burns more than it saves
- Single-issue gripe (e.g., "velocity report is ugly") — fix the report, do not migrate
- Decision already made by leadership — running a theater POC erodes trust

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

- parent skill: `pro/pm/project-manager/`
