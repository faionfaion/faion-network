# Rails Patterns (Service Objects)

## Summary

Extract multi-step business logic into Service Objects (`app/services/<Domain>::<Action>Service`) that accept `params:` and `current_user:` in `initialize` and return a single canonical `ServiceResult` from `#call`. Wrap multi-step writes in `ActiveRecord::Base.transaction`. Move mailers, webhooks, and HTTP calls to `after_commit` callbacks or a transactional outbox — never mid-transaction. One `ServiceResult` class for the entire codebase.

## Why

Fat controllers and fat models with callbacks lead to unpredictable execution order and test coupling. `ServiceResult` gives controllers a uniform success/failure contract without exception sniffing. The most dangerous agent-generated bug is calling `.deliver_later` or HTTP inside a transaction: a rolled-back insert leaves a sent email or a charged card. Bullet in test mode with `raise: true` catches N+1 at CI time.

## When To Use

- Rails 7.x app where controllers or `ActiveRecord` callbacks have grown unwieldy.
- Multi-step writes that must be transactional plus side effects (mailers, audit logs, webhooks).
- Defining a uniform success/failure return shape so controllers don't rescue exceptions.
- Refactoring fat controllers/models toward service-centric architecture.

## When NOT To Use

- Tiny single-step writes (`User.create!(params)`) — wrapping in a service is ceremony.
- Read-only endpoints — services add no value over a query object or scope.
- Background jobs that already encapsulate one action — nesting Service inside Sidekiq inside Service is over-engineering.
- Apps using Trailblazer, Interactor, or Dry::Transaction — stick to one paradigm.

## Content

| File | What's inside |
|------|---------------|
| `content/01-service-result.xml` | `ServiceResult` class, `success?`/`failure?`, constructor methods, controller integration. |
| `content/02-service-object.xml` | `Users::CreateService` example: `initialize`, `#call`, transaction, side effects, error rescue. |
| `content/03-antipatterns.xml` | Side effects in transactions, non-idempotent jobs, N+1 in serializers, inconsistent `ServiceResult` API. |

## Templates

| File | Purpose |
|------|---------|
| `templates/bullet-rspec.rb` | RSpec configuration enabling Bullet N+1 detection with `raise: true` in test mode. |
