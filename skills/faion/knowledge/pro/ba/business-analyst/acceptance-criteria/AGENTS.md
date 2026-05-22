---
slug: acceptance-criteria
tier: pro
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Explicit, testable conditions that define when a requirement is accepted as complete.
content_id: "96fc82f8dbdd8592"
tags: [acceptance-criteria, bdd, testing, requirements, agile]
---
# Acceptance Criteria

## Summary

**One-sentence:** Explicit, testable conditions that define when a requirement is accepted as complete.

**One-paragraph:** Explicit, testable conditions that define when a requirement is accepted as complete. Written in Given-When-Then (BDD) or rule-based checklist format, covering the happy path, alternative paths, boundaries, error handling, performance, and security. Each criterion maps to at least one test case and forms part of the Definition of Done.

## Applies If (ALL must hold)

- Every user story or requirement before a sprint starts — criteria must exist before development begins
- Bug fixes where the distinction between "expected" and "actual" behavior needs to be documented
- Technical stories where success requires a measurable outcome (throughput, error rate, response time)
- Before UAT to give users a concrete verification script rather than open-ended exploration
- Integrating with BDD tooling (Cucumber, SpecFlow) where Given-When-Then maps directly to test steps

## Skip If (ANY kills it)

- Vague exploratory stories tagged "spike" or "research" — an output contract is the right artifact, not acceptance criteria
- When writing criteria for 30+ scenarios in one story — the story is too large; split it first
- System-level non-functional requirements (SLOs, capacity) — these belong in the architecture decision record or SLA, not per-story criteria
- Pure infrastructure/ops tasks with no user-visible behavior — a runbook or configuration checklist applies instead

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
