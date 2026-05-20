---
slug: laravel-patterns
tier: pro
group: dev
domain: backend-enterprise
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Thin controllers that delegate to Action or Service classes; Form Requests for validation and authorization via Policies; API Resources for response shaping; DTOs for type-safe data flow through the service layer.
content_id: "60f0275ee9b5a7f5"
tags: [php, laravel, enterprise, eloquent, patterns]
---
# Laravel Patterns

## Summary

**One-sentence:** Thin controllers that delegate to Action or Service classes; Form Requests for validation and authorization via Policies; API Resources for response shaping; DTOs for type-safe data flow through the service layer.

**One-paragraph:** Thin controllers that delegate to Action or Service classes; Form Requests for validation and authorization via Policies; API Resources for response shaping; DTOs for type-safe data flow through the service layer. Wrap multi-step writes in DB::transaction(). Make queue jobs idempotent with ShouldBeUnique. Never use $request->all() or $model->fill($request->all()); always call $request->validated(). Always eager-load relationships via with() to prevent N+1 queries. Use Attribute::make() (Laravel 9+) for accessors/mutators.

## Applies If (ALL must hold)

- New Laravel 10/11 application with full-stack web or JSON API requirements.
- Refactoring fat controllers into Service classes, Action classes (single-purpose __invoke), and Form Requests.
- Wiring queue-backed jobs (Horizon + Redis), Eloquent scopes, accessors/mutators (Attribute API), and Form Request validation.
- Standing up Pest/PHPUnit feature tests with RefreshDatabase and factories.
- Adding API Resources for response shaping and Sanctum/Passport for authentication.

## Skip If (ANY kills it)

- High-throughput async pipelines with strict tail latency — Laravel's per-request bootstrap is heavy; consider Octane only after profiling.
- Lambda-style functions where cold start matters; Laravel Vapor mitigates but isn't free.
- Microservice meshes where you need fine-grained per-service runtime — Symfony or Slim may be a better fit.
- Pure data-pipeline batch jobs — a CLI in Symfony Console or pure PHP without the framework is leaner.

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
