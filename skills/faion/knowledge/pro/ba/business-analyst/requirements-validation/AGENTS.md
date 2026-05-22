---
slug: requirements-validation
tier: pro
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A four-stage process that confirms requirements build the right thing (not that they are built right).
content_id: "e3f08c20f288ffc2"
tags: [validation, requirements, quality-assurance, sign-off, gate]
---
# Requirements Validation and Sign-Off

## Summary

**One-sentence:** A four-stage process that confirms requirements build the right thing (not that they are built right).

**One-paragraph:** A four-stage process that confirms requirements build the right thing (not that they are built right). A BA-led quality scorecard grades each requirement against eight attributes (correct, complete, unambiguous, consistent, testable, traceable, feasible, necessary), a technique is selected (walkthrough, inspection, prototype review, simulation), findings are captured in a structured issue log, and a human stakeholder provides an explicit sign-off before design begins.

## Applies If (ALL must hold)

- Before flipping an SDD feature from todo/ to in-progress/ — validate that spec.md AC matches what the stakeholder asked, not what the elicitation agent inferred
- After a non-trivial elicitation session to catch summarization drift
- When a major scope change arrives mid-flight, before resuming /faion
- Pre-baseline gate: locking a spec.md version before design starts
- Prototype is available and users can perform task-based walkthroughs to expose gaps

## Skip If (ANY kills it)

- Throwaway spikes or research tasks — use a stop condition and brief, not a validation session
- Pre-elicitation: validating empty or aspirational requirements is theatre
- Pure operational runbook tweaks (cron edits, nginx vhost) — smoke tests, not validation
- Strictly internal refactors with no behavior change
- Post-launch: use Solution Evaluation and feedback loops instead

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

- parent skill: `pro/ba/business-analyst/`
