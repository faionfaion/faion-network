---
slug: ruby-rails-patterns
tier: pro
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Extract multi-step business workflows from fat controllers and models into service-object classes (app/services/BoundedContext/ActionService) with a single #call method returning a ServiceResult (success/failure).
content_id: "e9e3bf1a49df9765"
complexity: medium
produces: code
est_tokens: 5200
tags: [rails, service-objects, patterns, refactoring, transactions]
---
# Ruby on Rails Service Objects

## Summary

**One-sentence:** Extract multi-step business workflows from fat controllers and models into service-object classes (app/services/BoundedContext/ActionService) with a single #call method returning a ServiceResult (success/failure).

**One-paragraph:** Service objects encapsulate one business action (PlaceOrder, CancelOrder, RefundOrder). One class per action; one public #call method; explicit return type (ServiceResult.success(data:) / ServiceResult.failure(error:)). Services own the transaction boundary, validation, and orchestration; controllers stay thin; models stay focused on persistence + invariants. The pattern compresses sprawling logic into named, testable units.

**Ефективно для:**

- Rails apps з fat controllers (>80 LoC per action) або fat models (>500 LoC).
- Multi-step business flows (place_order, refund, cancel) з ≥3 кроками.
- Onboarding нових devs — services є named entry points для бізнес-логіки.
- Refactor god-objects (Order model з 30+ methods) у service-based decomposition.

## Applies If (ALL must hold)

- Rails app with multi-step business workflows.
- Models or controllers exceed maintainability thresholds (>500 / >80 LoC).
- Team commits to a per-action service pattern (not Interactor / Trailblazer / dry-monads).
- Tests can isolate service logic from HTTP + DB.

## Skip If (ANY kills it)

- Trivial CRUD app (model.update is enough).
- Team already on Trailblazer Operations / Interactor — different abstraction.
- Workflows are simple enough that the model's public method works fine.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Business action | named operation (verb + object) | product |
| Current fat code | controller method or model method | repo |
| ServiceResult class | Ruby class with .success / .failure factories | repo / app/services |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ruby-rails]] | Rails conventions are the substrate. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: one-action-per-service, service-result-explicit, service-owns-tx, no-callbacks-call-services, service-tested-in-isolation | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for code + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 900 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `name-and-scope-service` | opus | Naming + context decision is high-judgment. |
| `implement-call` | sonnet | Move logic + add ServiceResult. |
| `lint-callback-calls-service` | haiku | Mechanical grep. |

## Templates

| File | Purpose |
|------|---------|
| `templates/place_order_service.rb` | Service object skeleton with #call + ServiceResult + transaction |
| `templates/service_result.rb` | ServiceResult value object with .success / .failure factories + predicates |
| `templates/spec-skeleton.rb` | RSpec skeleton for service isolation test (no rails_helper) |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ruby-rails-patterns.py` | Validate the service-object artefact against the schema | Pre-commit + CI |

## Related

- [[ruby-rails]]
- [[ruby-activerecord]]
- [[ruby-rspec-testing]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, stack, runtime, scale, etc.) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
