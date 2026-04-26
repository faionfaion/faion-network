# Laravel Patterns (Controller → Service → Resource)

## Summary

Layered Laravel architecture: thin HTTP controllers, service classes that own business logic and transactions, Eloquent models accessed through service methods, and API Resources for response shaping. Form Requests handle validation and authorization. No Eloquent calls in controllers; no `request()` helper in services; inject contracts, not facades.

## Why

Fat controllers accumulate unrelated business rules, making them untestable and unmergeable. The Controller/Service/Resource split separates HTTP concerns from domain logic: controllers receive a Request, delegate to a Service, return a Resource. Services own `DB::transaction` and event dispatch. Resources produce consistent, explicit API contracts and preserve pagination metadata. This is testable at each layer independently.

## When To Use

- Greenfield Laravel 10/11/12 APIs that need Controller → Service → Resource layering.
- Brownfield refactors extracting business logic out of fat controllers.
- Generating CRUD slices (Controller + FormRequest + Resource + Service + Policy) for new resources.
- Cross-cutting hardening: FormRequests for validation, Resources for serialization, Services for transactions.
- Standardizing API versioning (`Api\V1\`) and Sanctum/Passport authentication at the controller boundary.

## When NOT To Use

- Tiny apps (<10 routes) where Service + Resource is over-engineering — Eloquent inside controllers is acceptable.
- Projects standardized on `lorisleiva/laravel-actions` or Spatie LaravelData + DDD — check team standard first.
- Inertia / Livewire / Filament apps where the framework idiom (controller → component) is the boundary.
- Console-only artisan apps — the controller/FormRequest/Resource trio doesn't apply.

## Content

| File | What's inside |
|------|---------------|
| `content/01-layer-rules.xml` | Rules for controller, service, resource, FormRequest, Policy boundaries |
| `content/02-antipatterns.xml` | Eloquent in controllers, request() in services, facades in services, N+1 in resources, tx wrapping HTTP |

## Templates

| File | Purpose |
|------|---------|
| `templates/controller.php` | Thin API controller: constructor-injected service, all five CRUD methods returning Resource |
| `templates/service.php` | Service class: paginate, create (with transaction + event), update, delete |
| `templates/laravel-anti-pattern-lint.sh` | Shell auditor: Eloquent in controllers, validator() in controllers, request() in services, facade in services |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/laravel-anti-pattern-lint.sh` | Flag banned patterns across app/Http/Controllers and app/Services |
