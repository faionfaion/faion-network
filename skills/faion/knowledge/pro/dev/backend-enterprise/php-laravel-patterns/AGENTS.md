# Laravel Patterns

## Summary

Clean-architecture layering for Laravel applications: thin Controller (route → service → Resource) → FormRequest (validation) → Service (business logic + DB::transaction) → Repository (optional, for real abstraction needs) → JsonResource (response shape). Each layer has one responsibility; controllers must not contain Eloquent queries or business logic.

## Why

Fat controllers mix HTTP, validation, business logic, and DB access, making each concern hard to test and change independently. The service layer is framework-light (no `request()` calls) and unit-testable without booting Laravel. `FormRequest::validated()` eliminates mass-assignment risk. `DB::transaction(fn () => ...)` handles rollback automatically. `JsonResource` stabilizes the API contract independently of the model shape.

## When To Use

- Greenfield Laravel 10/11/12 service that will grow beyond simple CRUD.
- Brownfield refactor where business logic leaks into controllers or models.
- API-first apps where `JsonResource` + `ResourceCollection` must stay stable across releases.

## When NOT To Use

- Prototypes, admin tooling, or one-off scripts — abstraction tax is wasted; use Eloquent in controller.
- Domains requiring DDD aggregates and explicit bounded contexts — use Symfony + hexagonal layout.
- Essentially-CRUD apps already using Filament/Nova — extra service layer is dead weight.

## Content

| File | What's inside |
|------|---------------|
| `content/01-rules.xml` | Layer responsibilities, constructor injection rules, transaction wrapping, repository justification gate. |
| `content/02-examples.xml` | UserController → UserService → UserRepository full scaffold. |
| `content/03-antipatterns.xml` | Eloquent in controller, FormRequest bypassed, try/catch hiding exceptions, missing return types. |

## Templates

| File | Purpose |
|------|---------|
| `templates/UserController.php` | Thin controller: FormRequest, service call, Resource response, HTTP status codes. |
| `templates/UserService.php` | Service with `DB::transaction`, Hash, event dispatch, no `request()` calls. |
| `templates/BaseService.php` | Abstract base service with paginate/findOrFail/delete for inheritance. |
