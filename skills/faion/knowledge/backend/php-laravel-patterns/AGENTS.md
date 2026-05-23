# Laravel Patterns

## Summary

**One-sentence:** Clean-architecture layering for Laravel — thin Controller → FormRequest → Service (DB::transaction) → optional Repository → JsonResource; controllers contain no Eloquent or business logic.

**One-paragraph:** Clean-architecture layering for Laravel 10/11/12 services. Controllers stay thin: validate via FormRequest, call one service method, wrap output in a JsonResource, return `JsonResponse`. Services accept primitives or DTOs (never `request()`), encapsulate business rules, and use `DB::transaction(fn() => ...)` for multi-write paths. Services return Eloquent models or DTOs — never `JsonResponse`. Repositories are introduced ONLY when there is a real abstraction need (multiple data sources, query encapsulation); interfaces are skipped for single-implementation repositories.

**Ефективно для:**

- Greenfield Laravel 10/11/12 service that will grow beyond simple CRUD.
- Brownfield refactor where business logic leaks into controllers or models.
- API-first apps where `JsonResource` + `ResourceCollection` must stay stable across releases.
- LLM-assisted teams that need a contract for what each layer is allowed to do.

## Applies If (ALL must hold)

- Laravel 10/11/12 service that grows beyond simple CRUD.
- HTTP API or full-stack web surface.
- Business logic exists that should be unit-testable without booting HTTP.

## Skip If (ANY kills it)

- Prototypes, admin tooling, or one-off scripts — the abstraction tax is wasted; keep Eloquent in the controller.
- Domains requiring DDD aggregates and explicit bounded contexts — use Symfony + hexagonal layout.
- Essentially-CRUD apps already using Filament / Nova — extra service layer is dead weight.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Use-case catalogue | Markdown verb list | product |
| Eloquent model list | Markdown | data modelling |
| API contract | OpenAPI YAML or Markdown | API design |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[php-laravel]] | Umbrella for queue / scheduler discipline. |
| [[php-eloquent]] | ORM rules that controllers / services rely on. |
| [[decomposition-laravel]] | Action + DTO + FormRequest decomposition. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: thin-controller-no-eloquent, service-no-request-globals, validated-only, jsonresource-from-controller-only, db-transaction-closure, repository-only-when-needed | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the layered-Laravel manifest + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: controller-with-eloquent, service-calling-request, transaction-with-swallow-catch, premature-repository, jsonresponse-from-service | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure: FormRequest → Service with DB::transaction → optional Repository → JsonResource → tests | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree mapping observable signals to a rule from 01-core-rules.xml | 700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `extract-service-from-controller` | sonnet | Reading legacy controller + extracting logic. |
| `decide-repository-need` | opus | Premature-abstraction risk. |
| `enforce-layer-discipline` | haiku | Mechanical scan for Eloquent in controllers. |

## Templates

| File | Purpose |
|------|---------|
| `templates/BaseService.php` | Service base class with `DB::transaction` helper. |
| `templates/UserController.php` | Thin controller skeleton (validate → service → Resource). |
| `templates/UserService.php` | Service skeleton with constructor injection + transactional method. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-php-laravel-patterns.py` | Validate the layered-Laravel manifest against the JSON Schema. | Pre-commit; CI on every methodology PR. |

## Related

- [[php-laravel]]
- [[php-eloquent]]
- [[laravel-patterns]]
- [[decomposition-laravel]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (project shape, abstraction need, layer concern) to a rule from `01-core-rules.xml`. Use it before scaffolding or refactoring a feature.
