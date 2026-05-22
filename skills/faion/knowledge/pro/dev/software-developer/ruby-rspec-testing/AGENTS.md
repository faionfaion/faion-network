---
slug: ruby-rspec-testing
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Write comprehensive, maintainable tests for Rails applications using RSpec 3.
content_id: "4f0ee38e298ed1e1"
tags: [rspec, testing, rails, tdd, factory-bot]
---
# RSpec Testing (Rails)

## Summary

**One-sentence:** Write comprehensive, maintainable tests for Rails applications using RSpec 3.

**One-paragraph:** Write comprehensive, maintainable tests for Rails applications using RSpec 3.13+, FactoryBot, Shoulda Matchers, and Capybara. Model specs test validations and associations using matchers; service specs exercise business logic; request specs validate HTTP contracts; system specs verify end-to-end flows. Modern idioms: `is_expected.to` (not `should`), request specs (never deprecated controller specs), `build_stubbed` for speed, `travel_to` for time-dependent code.

## Applies If (ALL must hold)

- Backfilling tests on a Rails monolith that has shipped without sufficient model/controller/service coverage
- Driving TDD on a new Rails app where RSpec + FactoryBot + Shoulda Matchers + Capybara is the team standard
- Standardizing a mixed Minitest/RSpec codebase to a single style; or generating RSpec specs from existing fixtures
- Adding request specs to lock down API contracts before a controller refactor or migration to GraphQL
- Writing service-object specs for Trailblazer / Interactor / dry-monads-style command objects extracted from fat controllers
- Generating system / feature specs with Capybara + Selenium / Cuprite for happy-path regression coverage

## Skip If (ANY kills it)

- Sinatra / Roda apps, gems with no Rails dependency — drop the `rails_helper`, use plain RSpec or Minitest
- Performance-sensitive Ruby microservices where startup tax of `rails_helper` (>3s) breaks CI throughput. Consider Minitest or `rspec` without `rails_helper`
- Codebases standardized on Minitest / Test::Unit — don't impose RSpec
- Jobs / mailers heavy on third-party APIs without a contract layer — mocks in RSpec drift; use VCR + Pact
- Throwaway prototypes / Hanami / dry-system experiments where Shoulda Matchers / FactoryBot don't apply

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

- parent skill: `pro/dev/software-developer/`
