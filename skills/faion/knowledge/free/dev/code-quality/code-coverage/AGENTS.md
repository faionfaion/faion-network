---
slug: code-coverage
tier: free
group: dev
domain: code-quality
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Coverage reports make untested branches visible so an agent or developer can write targeted tests.
content_id: "f4cb3e32da517b08"
tags: [coverage, testing, quality, metrics, ci]
---
# Code Coverage

## Summary

**One-sentence:** Coverage reports make untested branches visible so an agent or developer can write targeted tests.

**One-paragraph:** Coverage reports make untested branches visible so an agent or developer can write targeted tests. Branch coverage reveals untested else-branches that line coverage misses. Diff-coverage focuses the gate on new code, so accumulated legacy gaps do not block ongoing work. Martin Fowler's canonical note: coverage is a tool for finding gaps, not a goal — optimize for meaningful assertions, not numbers.

## Applies If (ALL must hold)

- Feeding coverage reports back to an LLM test-author to know which branches still lack tests.
- CI gate: enforce minimum diff-coverage on lines changed by a PR.
- Onboarding a new repo: run coverage once to map what is and is not tested.
- Targeted refactor planning: high-churn + low-coverage files are the first refactor candidates.

## Skip If (ANY kills it)

- Tiny one-shot scripts with no test infrastructure — wiring coverage costs more than it returns.
- UI/visual code where snapshot/visual tests give better signal than line coverage.
- Generated/migration code — exclude from coverage, do not attempt to test.
- As a single quality KPI for performance reviews — Goodhart's law applies.

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

- parent skill: `free/dev/code-quality/`
