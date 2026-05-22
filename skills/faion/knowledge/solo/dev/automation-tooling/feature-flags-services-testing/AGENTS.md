---
slug: feature-flags-services-testing
tier: solo
group: dev
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Choosing a flag service, writing pytest fixtures that test both ON and OFF code paths, running a weekly stale-flag CI audit, and wiring a flag agent that generates definitions, wraps new code paths, and creates cleanup tasks are the four operational concerns that complete a production-grade flag system.
content_id: "0c9678e57760bff3"
tags: [feature-flags, testing, pytest, openfeature, agent-workflow]
---
# Feature Flag Services, Testing, and Agentic Workflow

## Summary

**One-sentence:** Choosing a flag service, writing pytest fixtures that test both ON and OFF code paths, running a weekly stale-flag CI audit, and wiring a flag agent that generates definitions, wraps new code paths, and creates cleanup tasks are the four operational concerns that complete a production-grade flag system.

**One-paragraph:** Choosing a flag service, writing pytest fixtures that test both ON and OFF code paths, running a weekly stale-flag CI audit, and wiring a flag agent that generates definitions, wraps new code paths, and creates cleanup tasks are the four operational concerns that complete a production-grade flag system.

## Applies If (ALL must hold)

- Choosing between flag service vendors for a new project or migration.
- Writing tests that must cover both the enabled and disabled code path for a flagged feature.
- Setting up a weekly CI audit to surface flags past their expected cleanup date.
- Configuring an AI agent to generate flag definitions, wrap new code, write dual-branch tests, and register cleanup tasks automatically.

## Skip If (ANY kills it)

- Single-flag prototypes — the overhead of a full service integration outweighs the value.
- Projects that have no CI pipeline — the stale-flag audit workflow assumes a scheduled GitHub Actions runner.

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

- parent skill: `solo/dev/automation-tooling/`
