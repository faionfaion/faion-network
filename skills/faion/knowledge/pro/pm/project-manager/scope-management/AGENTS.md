---
slug: scope-management
tier: pro
group: pm
domain: project-manager
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Define, baseline, validate, and control project scope to prevent uncontrolled expansion.
content_id: "3c7f123565e99e04"
tags: [scope, requirements, change-control, traceability, scope-creep]
---
# Scope Management

## Summary

**One-sentence:** Define, baseline, validate, and control project scope to prevent uncontrolled expansion.

**One-paragraph:** Define, baseline, validate, and control project scope to prevent uncontrolled expansion. Scope management produces a scope statement (objectives, deliverables, exclusions, constraints, assumptions), a requirements document with MoSCoW priorities, and a traceability matrix linking every requirement to design, build, and test. The rule: write exclusions before inclusions — explicit "not in scope" prevents 80% of scope disputes.

## Applies If (ALL must hold)

- Project initiation: drafting scope statement, requirement collection, baselining
- Mid-project change requests where impact assessment must precede approval
- Multi-stakeholder programs with conflicting priorities (MoSCoW + traceability)
- Contracted/fixed-price work where every out-of-scope item is a margin event
- Requirements traceability for regulated domains (medtech, fintech, government)

## Skip If (ANY kills it)

- Continuous-discovery agile product — use rolling outcomes instead of scope baselines
- Pure research/spike work where scope is the question, not the input
- Internal tools with fewer than 10 users where formal sign-off is theater
- Crisis incident response — incident scope is "stop the bleeding", not a PMP doc

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
