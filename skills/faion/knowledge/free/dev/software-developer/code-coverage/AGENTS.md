---
slug: code-coverage
tier: free
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Coverage measures which lines and branches execute during tests.
content_id: "f4cb3e32da517b08"
tags: [testing, coverage, quality-assurance, ci, metrics]
---
# Code Coverage

## Summary

**One-sentence:** Coverage measures which lines and branches execute during tests.

**One-paragraph:** Coverage measures which lines and branches execute during tests. Use branch coverage (not line-only) as the gate metric, enforce it on diffs (new code), set per-module thresholds via diff-cover, and pair with mutation testing on critical modules to validate assertion quality. High line coverage can coexist with completely missing branches and zero-assertion tests. Branch coverage + diff gating closes the two most common loopholes: the "test exists but asserts nothing" gap and the "legacy code drags total down" excuse.

## Applies If (ALL must hold)

- Setting a CI gate on new-code diff coverage (not absolute repo total)
- Identifying critical untested paths in legacy code prior to refactor
- Pre-release: surface modules below threshold, prioritize test work there
- Code review: confirm new code is covered without chasing 100% globally
- Onboarding tests for a third-party library wrapper before upgrading the dep

## Skip If (ANY kills it)

- As the primary quality metric — 100% coverage with no assertions is worse than 60% with rich ones
- Generated code (migrations, OpenAPI clients, protobuf stubs) — exclude in .coveragerc
- UI / E2E smoke tests where flakiness outweighs coverage signal
- Single-file scripts or spike code — instrumentation overhead not justified

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

- parent skill: `free/dev/software-developer/`
