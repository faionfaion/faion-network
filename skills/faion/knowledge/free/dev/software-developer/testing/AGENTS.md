---
slug: testing
tier: free
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Comprehensive testing patterns for pytest (Python), Jest/Vitest (JavaScript/TypeScript), Go's testing package, Playwright (E2E), and Cypress.
content_id: "dd29eb8ce0bb0e79"
tags: [testing, pytest, vitest, playwright, tdd]
---
# Testing (Multi-Language)

## Summary

**One-sentence:** Comprehensive testing patterns for pytest (Python), Jest/Vitest (JavaScript/TypeScript), Go's testing package, Playwright (E2E), and Cypress.

**One-paragraph:** Comprehensive testing patterns for pytest (Python), Jest/Vitest (JavaScript/TypeScript), Go's testing package, Playwright (E2E), and Cypress. Every test follows Arrange-Act-Assert. Tests are isolated, idempotent, and can run in any order. Coverage threshold: 80% branches minimum.

## Applies If (ALL must hold)

- Unit testing pure functions and services with mocks for external dependencies.
- Configuring pytest, Jest, or Vitest for a new project.
- Setting up fixture factories, parametrization, and async test support.
- Implementing TDD with red-green-refactor cycles.
- Adding E2E tests with Playwright or Cypress.
- A task whose acceptance criteria include "tests pass" — the agent must write or update tests as part of the implementation, not as an afterthought.
- Cross-language repos (Python services + JS frontend + Go workers) where one orchestrating agent needs language-specific testing patterns.
- Establishing a coverage floor (`fail_under = 80`) and wiring it into CI so PRs from agents block on regressions.
- Bootstrapping a new repo with the canonical pytest/jest/vitest/playwright config in one shot.

## Skip If (ANY kills it)

- Integration tests with real databases (see integration-testing methodology instead).
- Load and performance testing (use k6, Locust, or go test -bench=).
- Visual regression testing (use Percy or Chromatic).
- One-off scripts and notebooks that are inherently exploratory (a few asserts in the script itself are enough).
- Pure infra-as-code (terraform/k8s manifests) where the test signal is `plan`/`apply` outcome, not unit testing.
- When the codebase has no testable seams (god objects, no DI, untyped globals) — fix that first; tests bolted on top become brittle and an agent will spend tokens chasing them.
- Visual regression flows — defer to Playwright screenshot diffs / Percy / Chromatic, not unit-test frameworks.

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
