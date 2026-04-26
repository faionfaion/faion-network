# PHP Laravel Backend

## Summary

Production Laravel backend patterns: Controller → FormRequest → Service → Eloquent model → API Resource slice. Controllers are thin HTTP adapters (10-30 lines). Business logic and `DB::transaction` live in service classes. Form Requests own validation and policy authorization. API Resources produce explicit field lists. No `Request::all()`, no Eloquent in controllers, no `request()` in services.

## Why

Laravel's batteries (auth, queues, mail, broadcasting, scheduler) accelerate CRUD-heavy backends, but the framework's permissiveness allows fat controllers and mass-assignment vulnerabilities by default. The full-slice approach enforces separation of concerns at every layer, makes each layer testable in isolation, and produces consistent API contracts via Resources regardless of underlying Eloquent changes.

## When To Use

- Greenfield CRUD-heavy backends (SaaS, e-commerce, internal tools) with 1-5 person teams.
- API-first products pairing Sanctum/Passport for auth and Resource classes for serialization.
- Brownfield migration from raw PHP, WordPress, or CodeIgniter when shipping speed matters.
- Any project where convention-over-configuration can replace bespoke framework glue.

## When NOT To Use

- Sub-millisecond hot paths (HFT, ad serving) — PHP request bootstrap (~30-80ms cold) is a floor.
- Heavy CPU/ML workloads — use Laravel as the front door, offload via queues.
- WebSocket-first apps with persistent connections — use Reverb only as a complement.
- Stateful long-lived processes (game servers, media transcoders) — wrong runtime model.
- Teams with zero PHP experience facing a hard deadline.

## Content

| File | What's inside |
|------|---------------|
| `content/01-full-slice.xml` | Complete Controller/FormRequest/Service/Resource/Repository/Model structure rules |
| `content/02-eloquent-patterns.xml` | Model definition, scopes, relationships, accessors, repository pattern |
| `content/03-antipatterns.xml` | Request::all(), Eloquent in controllers, N+1 in resources, facades in services, mass-assignment |

## Templates

| File | Purpose |
|------|---------|
| `templates/controller.php` | CRUD controller with typed constructor injection, all five methods, Resource returns |
| `templates/service.php` | Service with paginate, findOrFail, create (hash+event), update, delete |
| `templates/model.php` | Eloquent model with fillable, casts, relationships, scopes, accessors |
| `templates/repository.php` | UserRepository with eager loading, pagination, findByEmail |
