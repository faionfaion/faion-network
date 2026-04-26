# Laravel Patterns

## Summary

Thin controllers that delegate to Action or Service classes; Form Requests for validation + authorization; API Resources for response shaping; DTOs for type-safe data flow through the service layer. Wrap multi-step writes in `DB::transaction()`. Make queue jobs idempotent with `ShouldBeUnique`. Never use `$request->all()` or `$model->fill($request->all())`; always call `$request->validated()`.

## Why

Laravel's Eloquent ORM produces N+1 queries invisibly when relationships are accessed inside loops without prior `with()` eager loading. `$request->all()` is a mass-assignment vector. Non-idempotent jobs double-charge or double-send when workers retry. These three failure modes are the most common agent-generated bugs in Laravel codebases and can be caught with Telescope SQL counts, PHPStan, and a `DB::listen` query budget in tests.

## When To Use

- New Laravel 10/11 application with full-stack web or JSON API requirements.
- Refactoring fat controllers into Service/Action classes and Form Requests.
- Wiring queue-backed jobs (Horizon + Redis), Eloquent scopes, and Form Request validation.
- Standing up Pest/PHPUnit feature tests with `RefreshDatabase` and factories.
- Adding API Resources for response shaping and Sanctum/Passport for authentication.

## When NOT To Use

- High-throughput async pipelines with strict tail latency — per-request bootstrap is heavy.
- Lambda-style functions where cold start matters (Vapor mitigates but adds cost).
- Microservice meshes requiring fine-grained per-service runtime (Symfony or Slim may fit better).
- Pure data-pipeline batch jobs — CLI in Symfony Console or pure PHP is leaner.

## Content

| File | What's inside |
|------|---------------|
| `content/01-model-patterns.xml` | Eloquent model with fillable, scopes, accessors/mutators (`Attribute::make`), `Searchable` trait. |
| `content/02-service-and-repository.xml` | Service class with `DB::transaction`, repository interface + implementation, DTO flow. |
| `content/03-http-layer.xml` | Form Request with `authorize()` and `toDTO()`, API Resource, UserCollection, UserController. |
| `content/04-testing-and-gotchas.xml` | Pest feature tests with `RefreshDatabase`, N+1 query budget, antipatterns (fat controller, mass assignment). |

## Templates

| File | Purpose |
|------|---------|
| `templates/query-budget.php` | `DB::listen` test helper that fails when query count exceeds budget (N+1 detector). |
