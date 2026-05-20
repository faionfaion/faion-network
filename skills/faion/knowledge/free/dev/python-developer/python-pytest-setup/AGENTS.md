---
slug: python-pytest-setup
tier: free
group: dev
domain: python-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Wire pytest into a Python project: install the essential plugin set, configure pyproject.
content_id: "aabf85df9e38e31e"
tags: [pytest, configuration, ci, coverage, python]
---
# pytest Project Setup — Plugins, Configuration, Coverage, and CI

## Summary

**One-sentence:** Wire pytest into a Python project: install the essential plugin set, configure pyproject.

**One-paragraph:** Wire pytest into a Python project: install the essential plugin set, configure pyproject.toml with strict markers and coverage gates, structure the tests/ directory mirroring src/, add parallel execution for CI, and follow the agentic TDD loop for feature development.

## Applies If (ALL must hold)

- New Python project — wire pytest as the only test runner; never use stdlib unittest for new code.
- Migrating from unittest.TestCase — keep existing tests running, add new tests in pytest style (the mix is supported).
- CI pipeline that needs coverage reporting, parallel execution, or artifact upload.
- Team project that needs enforced marker discipline and reproducible test ordering.

## Skip If (ANY kills it)

- Doctest-only libraries — pytest can run doctests but adds setup overhead; pure "python -m doctest" is sufficient for tiny libs.
- Single-script tools where the setup overhead dominates — assert + manual run is fine.
- BDD-style requirement docs — pytest-bdd works but behave is more idiomatic for Gherkin-first teams.
- Serious performance benchmarks — pytest-benchmark works but asv (airspeed velocity) or vendor profilers give better regression detection.
- Hard-real-time or hardware-in-loop tests — pytest's discovery and fixture model add latency; use a dedicated harness.

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

- parent skill: `free/dev/python-developer/`
