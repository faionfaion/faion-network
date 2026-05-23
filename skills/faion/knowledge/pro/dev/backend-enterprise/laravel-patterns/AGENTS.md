---
slug: laravel-patterns
tier: pro
group: dev
domain: backend
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Enterprise Laravel 10/11 patterns — thin controllers, Action/Service classes, Form Request validation, API Resources, DTOs, DB::transaction for writes, ShouldBeUnique jobs, eager-load discipline.
content_id: "bc28c972516c6397"
complexity: deep
produces: code
est_tokens: 4400
tags: [php, laravel, enterprise, eloquent, patterns]
---
# Laravel Patterns

## Summary

**One-sentence:** Enterprise Laravel 10/11 patterns — thin controllers, Action/Service classes, Form Request validation, API Resources, DTOs, DB::transaction for writes, ShouldBeUnique jobs, eager-load discipline.

**One-paragraph:** Enterprise patterns for Laravel 10/11. Controllers stay thin and delegate to Action (single `__invoke`) or Service classes. Validation lives in Form Requests (`$request->validated()` only — `$request->all()` and `fill($request->all())` are forbidden). Responses go through API Resources with explicit attribute lists. Multi-step writes wrap in `DB::transaction(...)`. Queue jobs implement `ShouldBeUnique` for idempotency. Relationships are eager-loaded via `->with(...)` to kill N+1. Accessors / mutators use the `Attribute::make()` API. Constructor injection replaces `app(Service::class)`.

**Ефективно для:**

- New Laravel 10/11 app with full-stack web or JSON API requirements.
- Refactoring fat controllers into Service classes, Action classes (single-purpose `__invoke`), and Form Requests.
- Wiring queue-backed jobs (Horizon + Redis), Eloquent scopes, accessors/mutators, Form Request validation.
- Standing up Pest / PHPUnit feature tests with RefreshDatabase and factories.
- Adding API Resources for response shaping and Sanctum / Passport for authentication.

## Applies If (ALL must hold)

- Laravel 10/11 app on PHP 8.2+.
- Full-stack web or JSON API surface; queue workers via Horizon.
- Codebase that benefits from canonical conventions for agent contributions.

## Skip If (ANY kills it)

- High-throughput async pipelines with strict tail latency — Laravel's per-request bootstrap is heavy; consider Octane only after profiling.
- Lambda-style functions where cold start matters; Vapor mitigates but is not free.
- Microservice meshes where you need fine-grained per-service runtime — Symfony or Slim may be a better fit.
- Pure data-pipeline batch jobs — a Symfony Console CLI is leaner.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Use-case catalogue | Markdown verb list | product |
| Eloquent model list | Markdown | data modelling |
| Queue worker SLA | text | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[php-laravel]] | Umbrella for service / queue patterns. |
| [[decomposition-laravel]] | Action + DTO + FormRequest pattern. |
| [[php-eloquent]] | ORM discipline that prevents N+1. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: validated-not-all, db-transaction-for-multistep-writes, eager-load-with-relations, api-resource-explicit-fields, shouldbeunique-on-jobs, constructor-injection-not-app | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the Laravel-patterns manifest + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: request-all-mass-assignment, n-plus-one-foreach, mail-inside-transaction, container-resolution-not-injection, queue-job-not-idempotent | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure: scaffold FormRequest + Action → API Resource → DB::transaction → queue job → tests | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree mapping observable signals to a rule from 01-core-rules.xml | 700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `extract-action-from-controller` | sonnet | Verb extraction needs judgment. |
| `harden-queue-job` | opus | Idempotency reasoning across retries. |
| `query-budget-check` | haiku | Mechanical N+1 detection. |

## Templates

| File | Purpose |
|------|---------|
| `templates/query-budget.php` | Pest test helper enforcing query count budget per request. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-laravel-patterns.py` | Validate the Laravel-patterns manifest against the JSON Schema. | Pre-commit; CI on every methodology PR. |

## Related

- [[php-laravel]]
- [[php-laravel-patterns]]
- [[decomposition-laravel]]
- [[php-eloquent]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (write multiplicity, queue use, eager-load gaps) to a rule from `01-core-rules.xml`. Use it before authoring or refactoring a controller / job.
