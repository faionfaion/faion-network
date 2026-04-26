# Laravel Patterns

## Summary

Laravel 11 architecture patterns: thin controller → FormRequest validation → Action/Service → Eloquent model → API Resource. Enforces `$fillable` discipline, enum casts, DB transactions, eager loading, typed queues with idempotency, and Policy-based authorization.

## Why

Laravel's "magic" makes it easy to write fat controllers, skip transactions, and produce N+1 queries — all of which are silent until they hit prod. This methodology encodes the concrete guardrails: FormRequests on every mutation, `DB::transaction(fn () => ...)` for multi-step writes, eager loading in services, `ShouldBeUnique` on jobs, and Policy coverage for every protected action.

## When To Use

- Scaffolding a new Laravel 11 app or extending one with models, migrations, FormRequests, Resources
- Generating service/action/DTO classes around Eloquent models
- Authoring API resources with consistent envelopes (JsonResource, ResourceCollection)
- Reviewing PRs for N+1, fat controllers, missing FormRequests, mass-assignment vulnerabilities
- Adding queues (Horizon, Redis, SQS) and event/listener wiring
- Auth flows: Sanctum (SPA), Passport (OAuth2), policies, gates, RBAC

## When NOT To Use

- Hot paths needing sub-millisecond latency — PHP-FPM round trip dominates
- Heavy data engineering or streaming workloads — use a JVM/Go pipeline
- Real-time bidirectional protocols beyond Reverb/Echo scope
- Greenfield where the team has no PHP experience

## Content

| File | What's inside |
|------|---------------|
| `content/01-architecture.xml` | Project structure, model/repository/service/controller layers, FormRequest pattern |
| `content/02-rules.xml` | Fillable discipline, enum casts, transactions, eager loading, queue idempotency, LLM gotchas |
| `content/03-examples.xml` | Model, service, repository, FormRequest, API Resource, controller, test code examples and antipatterns |

## Templates

| File | Purpose |
|------|---------|
| `templates/laravel-pr-gate.sh` | CI gate: pint, phpstan, FormRequest enforcement, eager-load check, fillable check, Pest with coverage |
| `templates/prompt-eloquent-coder.txt` | Subagent prompt for model + migration + factory + seeder generation |
| `templates/prompt-policy-coder.txt` | Subagent prompt for multi-tenant Policy generation |
