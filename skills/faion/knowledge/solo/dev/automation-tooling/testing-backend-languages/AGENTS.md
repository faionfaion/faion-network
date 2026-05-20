---
slug: testing-backend-languages
tier: solo
group: dev
domain: automation-tooling
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Each backend language has a canonical test idiom.
content_id: "117afa78a4b317ca"
tags: [testing, rspec, phpunit, spring-boot, rust]
---
# Backend Language Testing: Ruby, PHP, Java, C#, Rust

## Summary

**One-sentence:** Each backend language has a canonical test idiom.

**One-paragraph:** Each backend language has a canonical test idiom. This methodology provides the minimum pattern for Ruby/RSpec, PHP/Laravel+Pest, Java/Spring Boot, C#/.NET xUnit, and Rust, plus the LLM gotchas specific to each stack so agents produce idiomatic tests on the first pass.

## Applies If (ALL must hold)

- Bootstrapping a test suite in a new Ruby on Rails, PHP Laravel, Java Spring, C# .NET, or Rust service.
- Filling coverage holes on an existing backend module — feed source + this reference and ask for unit/integration tests in the project idiom.
- Standardising test style across a polyglot backend monorepo where each service uses a different stack.
- Producing first-cut tests during SDD in-progress/ so review focuses on logic, not boilerplate.

## Skip If (ANY kills it)

- Python/Django — see testing-django-pytest for the pytest + factory_boy idiom.
- Frontend JS/TS — see testing-js-ts-frontend for vitest + Testing Library.
- Performance / load testing — see perf-test-basics, perf-test-tools.
- When the project already has a strong test convention — agent will drift into the generic style here and create churn.

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
