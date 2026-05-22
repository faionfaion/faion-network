---
slug: unit-testing
tier: free
group: dev
domain: dev
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Isolated, deterministic, single-behaviour tests with Arrange-Act-Assert; mock only at process boundary.
content_id: "0f0eecaea7164387"
complexity: medium
produces: code
est_tokens: 3700
tags: [unit-testing, pytest, aaa-pattern, test-doubles, tdd]
---
# Unit Testing

## Summary

**One-sentence:** Isolated, deterministic, single-behaviour tests with Arrange-Act-Assert; mock only at process boundary.

**One-paragraph:** Methodology for writing isolated, deterministic tests that verify a single behaviour per test using the Arrange-Act-Assert pattern. Each test names its scenario explicitly (test_<behavior>_when_<context>), uses fixtures or fakes for setup, and mocks only at process boundaries (network, disk, clock).

**Ефективно для:** інженера, який пише або ревʼює юніт-тести — закриває петлю між неоднозначним 'тестом' і AAA-структурованим, ізольованим, single-behaviour тестом.

## Applies If (ALL must hold)

- New code with branching logic, math, parsing, validation, or state transitions.
- Refactoring legacy code — safety net before changing internals.
- Pure functions or services with mockable boundaries.
- Defining the consumer contract of a new module.

## Skip If (ANY kills it)

- Integration test territory — load testing methodology.
- Pure config files with no logic.
- Generated code that mirrors a verified schema.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Test runner installed | package | pytest / vitest / go test |
| Function or class under test | code | src/ |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `free/dev/software-developer/tdd-workflow` | Red-Green-Refactor cycle this fits inside. |
| `free/dev/software-developer/testing` | Shared multi-language testing rules. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: one behaviour per test, AAA explicit, descriptive name, mock at boundary only, deterministic, fakes over mocks for repeated behaviour. | ~1000 |
| `content/02-output-contract.xml` | essential | Shape: test_<behaviour>_when_<context> function with Arrange/Act/Assert comments; one observable behaviour. Forbidden: multiple unrelated assertions, real network/disk/clock, naming like test_1. | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: multi-behaviour tests, real I/O in unit, brittle mocks, generic names, shared mutable state. | ~800 |
| `content/04-procedure.xml` | medium | Steps: pick one behaviour → arrange → act → assert → review for isolation + idempotence. | ~700 |
| `content/06-decision-tree.xml` | essential | Tree: pure function? → call directly. External dep? → mock at boundary. Repeated behaviour mocked? → fake/stub. Else: integration. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `write-unit-test` | sonnet | Translate behaviour to AAA with judgement. |
| `audit-unit-suite` | opus | Cross-cutting: detect multi-behaviour, brittle mocks, naming. |

## Templates

| File | Purpose |
|------|---------|
| `templates/test_unit.py` | Python AAA skeleton with mock at boundary. |
| `templates/test_unit.ts` | Vitest AAA skeleton. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-unit-testing.py` | Check tests have one observable assertion target, name matches test_<behaviour>_when_<context>, no real network. | Pre-commit. |

## Related

- [[tdd-workflow]]
- [[testing]]
- [[python-pytest-setup]]

## Decision tree

The tree at content/06-decision-tree.xml decides whether a test is genuinely a unit, which boundary to mock, and fake vs mock. Walk it whenever the test feels slow or uses real I/O.
