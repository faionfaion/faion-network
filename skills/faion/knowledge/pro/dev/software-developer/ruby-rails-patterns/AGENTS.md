# Rails Patterns (Service Objects)

## Summary

Rails service object pattern: extract multi-step business workflows from fat controllers/models into `app/services/<BoundedContext>/<Action>Service` classes with a single `call` method that returns a `ServiceResult` (success/failure). Keeps controllers as pure HTTP adapters; business logic and transaction management live in services.

## Why

Rails controllers balloon when they own database writes, mailer calls, audit logging, and job enqueuing. ActiveRecord callbacks create unmaintainable side-effect chains. Service objects enforce a single responsibility, make transaction boundaries explicit, and let RSpec test business logic in isolation without loading the full HTTP stack.

## When To Use

- Controllers that have grown past ~100 lines and need workflow extraction
- Multi-step business operations (signup, checkout, refund) that span multiple models in one transaction
- Replacing fat-model callbacks when side effects have become unmanageable
- Standardizing controller response shapes: every action maps `ServiceResult` → HTTP status

## When NOT To Use

- Trivial CRUD where a `before_action` + `model.save` already does the job — service objects add indirection without value
- Pure data-access logic — that belongs in Query Objects or scopes, not services
- One-off rake tasks or scripts — plain Ruby objects without the result wrapper are fine

## Content

| File | What's inside |
|------|---------------|
| `content/01-service-pattern.xml` | Service object structure rules, ServiceResult shape, namespace conventions, transaction guidance |
| `content/02-examples.xml` | Service implementation, controller wiring, RSpec spec skeleton, antipatterns |

## Templates

| File | Purpose |
|------|---------|
| `templates/service_result.rb` | ServiceResult value object with success/failure constructors |
| `templates/spec-skeleton.rb` | RSpec request + service spec template covering success, validation failure, DB rollback |
