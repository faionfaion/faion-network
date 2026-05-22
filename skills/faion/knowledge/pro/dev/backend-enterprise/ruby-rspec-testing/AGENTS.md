---
slug: ruby-rspec-testing
tier: pro
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Build comprehensive Rails test suites using layered RSpec strategies: model specs test validations and scopes, service specs test business logic, request specs test HTTP contracts, and system specs test browser behavior.
content_id: "4f0ee38e298ed1e1"
tags: [rspec, testing, rails, bdd, coverage]
---
# RSpec Testing for Rails Applications

## Summary

**One-sentence:** Build comprehensive Rails test suites using layered RSpec strategies: model specs test validations and scopes, service specs test business logic, request specs test HTTP contracts, and system specs test browser behavior.

**One-paragraph:** Build comprehensive Rails test suites using layered RSpec strategies: model specs test validations and scopes, service specs test business logic, request specs test HTTP contracts, and system specs test browser behavior. Use factory_bot for test data, shoulda-matchers for one-liners, and SimpleCov branch tracking to find uncovered paths. BDD structure (describe/context/it) enforces one behavior per test block and produces diagnostic failure messages.

## Applies If (ALL must hold)

- Rails app with layered behavior: models with validations, PORO services, REST endpoints.
- TDD or red/green/refactor cycles with LLM agents — RSpec DSL maps to agent prompts well.
- Codebases enforcing coverage gates (simplecov ≥80% for services).
- Multi-developer teams using shared examples and shared contexts to reduce duplication.
- Refactor-heavy phases where fast model + service specs are the safety net.

## Skip If (ANY kills it)

- Greenfield Hanami/Roda/Sinatra apps — rails_helper and Rails matchers do not apply.
- Pure CLI gems — spec_helper only; rails_helper is overkill.
- Codebases standardized on Minitest — mixing creates two test infrastructures.
- Performance benchmarks — use benchmark/ips, not RSpec.
- Visual regression — use Percy/Chromatic via Capybara, but the value is in the visual-diff service, not RSpec itself.

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

- parent skill: `pro/dev/backend-enterprise/`
