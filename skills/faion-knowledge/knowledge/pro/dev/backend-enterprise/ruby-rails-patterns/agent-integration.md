# Agent Integration — Rails Patterns (Service Objects + ServiceResult)

## When to use
- Rails 7.x app where controllers and ActiveRecord callbacks have grown unwieldy and need extraction into Service Objects.
- Multi-step writes that must be transactional (`ActiveRecord::Base.transaction`) plus side effects (mailers, audit logs, webhooks).
- Defining a uniform success/failure return shape (`ServiceResult`) so controllers don't sniff exceptions.
- Refactoring fat controllers / fat models toward "skinny everything, services in the middle" architecture.
- Standing up RSpec request specs around Service Objects with FactoryBot.

## When NOT to use
- Tiny single-step writes (`User.create!(params)`) — wrapping them in a service is ceremony.
- Read-only endpoints — services add no value over a query object or scope.
- Background jobs that already encapsulate one action — wrapping a Service inside a Sidekiq job inside another Service is over-engineering.
- Apps using Trailblazer, Interactor, or Dry::Transaction — stick to one paradigm rather than mixing.

## Where it fails / limitations
- ServiceResult collapses multiple error types (validation, authorization, network) into one bag — lossy compared to typed errors.
- Agents tend to reinvent ServiceResult per-service with subtle differences; codebases drift fast without enforcement.
- Side effects after `save!` but inside the transaction (mailers, HTTP) can be rolled back unexpectedly — they should run after `commit` via `after_commit` or a transactional outbox.
- Calling `.deliver_later` inside a transaction can race with the worker reading a not-yet-committed record. Agents miss this.
- ActiveRecord callbacks duplicate logic that lives in services — leads to "did this already run?" debugging.
- N+1 queries proliferate in controllers and serializers; Bullet is essential but agents disable it after one false positive.

## Agentic workflow
Use SDD: spec → migration → model + factory → service object + RSpec service spec → controller + request spec → serializer. Reviewer agent must enforce one ServiceResult shape across the codebase, ban side effects inside transactions (use `after_commit` or `Outbox.enqueue`), and run `bundle exec rubocop` + `bundle exec rspec` per task. Bullet should run in test mode and fail tests on N+1.

### Recommended subagents
- `faion-sdd-executor-agent` — sequential task runner; runs RSpec + RuboCop per task.
- `faion-feature-executor` — feature-level orchestration with quality gates.
- General reviewer subagent — flag duplicate ServiceResult definitions, side effects in transactions, N+1.
- `password-scrubber-agent` — strip secrets from job arguments and exception messages.

### Prompt pattern
Plan: "Service `<Domain>::<Action>Service` with `initialize(params:, current_user:)` and `#call` returning `ServiceResult`. Wrap multi-step write in `ActiveRecord::Base.transaction`. Move mailer/webhook calls to `after_commit` callbacks or outbox. Ban side effects between `save!` and `commit`."

Review: "Run `bundle exec rspec` and `bundle exec rubocop`. Inspect `db.log` for N+1 (Bullet). Audit services for `Mailer.deliver_later` or HTTP calls inside `transaction` blocks; propose moving them to `after_commit`."

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `bin/rails`, `bin/rake` | Project commands | shipped |
| RuboCop + rubocop-rails + rubocop-rspec | Style + Rails-aware lint | rubocop.org |
| StandardRB | Opinionated zero-config alternative | github.com/standardrb/standard |
| Brakeman | Static security scanner | brakemanscanner.org |
| Bundler-audit | Gem vulnerability scan | github.com/rubysec/bundler-audit |
| Sorbet / RBS | Optional typing | sorbet.org / github.com/ruby/rbs |
| Bullet | N+1 detector | github.com/flyerhzm/bullet |
| Pundit / CanCanCan | Authorization | github.com/varvet/pundit |
| FactoryBot | Test factories | github.com/thoughtbot/factory_bot |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Heroku / Render / Fly.io | SaaS | Yes | Buildpacks autodetect Rails; `git push` deploys |
| Sidekiq + Redis | OSS | Yes | Job runner; agent integrates by adding `include Sidekiq::Job` |
| Sidekiq Pro/Enterprise | SaaS | Yes | Adds rate limiting, batches; same API |
| AppSignal / Skylight / Scout APM | SaaS | Yes | Auto-instruments Rails |
| Honeybadger / Sentry / Bugsnag | SaaS | Yes | Drop-in gem, env-var config |
| GitHub Actions | SaaS | Yes | Standard Ruby/Rails matrix templates |

## Templates & scripts
See `templates.md` for `ServiceResult`, base service module, transactional outbox table + worker. Bullet test integration:

```ruby
# spec/rails_helper.rb
Bullet.enable = true
Bullet.bullet_logger = true
Bullet.raise = true # fail tests on N+1
RSpec.configure do |c|
  c.before(:each) { Bullet.start_request }
  c.after(:each)  { Bullet.perform_out_of_channel_notifications if Bullet.notification?; Bullet.end_request }
end
```

## Best practices
- One canonical `ServiceResult` (`app/services/service_result.rb`); all services return it. CI fails on duplicates.
- Side effects (mailers, webhooks, search-index updates) live in `after_commit` callbacks, an outbox, or chained Sidekiq jobs — never mid-transaction.
- Mailers and outbound HTTP calls go through `.deliver_later` / `perform_async` so the request thread stays fast.
- Use Pundit policies; controllers call `authorize @resource` on every action and `policy_scope` on collection endpoints.
- Strong Parameters in controllers; services receive an already-permitted hash.
- Keep ActiveRecord callbacks for invariants only (`before_validation :normalize_email`); business logic stays in services.
- Run Bullet, Brakeman, and bundler-audit in CI; gate merges on green.

## AI-agent gotchas
- LLMs invent slightly different ServiceResult shapes per file (sometimes `result.ok?`, sometimes `result.success?`, sometimes `result.failure?`). Lock the API in CI.
- Agents put `UserMailer.welcome(user).deliver_now` between `save!` and end of transaction — a rolled-back insert leaves a sent email. Always `deliver_later` after commit.
- N+1 patterns reappear in serializers (`ActiveModel::Serializer`/`Jbuilder`); reviewer must check serializer specs, not just controller specs.
- Sidekiq jobs generated by AI often accept ActiveRecord objects directly — pass IDs, not objects, to avoid serialization of stale state.
- Agents skip `Pundit::Authorize` on new actions; require `verify_authorized` and `verify_policy_scoped` in `ApplicationController`.
- Generated migrations are sometimes destructive (drop_column without backfill). Require reversible migrations and review.
- Agents may set `config.active_job.queue_adapter = :inline` for "tests", masking timing bugs in production where Sidekiq is async.

## References
- Rails Guides — https://guides.rubyonrails.org/
- "Sustainable Web Development with Ruby on Rails" (David Bryant Copeland) — https://sustainable-rails.com/
- "Working with Rails: Service Objects" — https://www.toptal.com/ruby-on-rails/rails-service-objects-tutorial
- Bullet — https://github.com/flyerhzm/bullet
- Pundit — https://github.com/varvet/pundit
- Sidekiq best practices — https://github.com/sidekiq/sidekiq/wiki/Best-Practices
- Transactional outbox pattern — https://microservices.io/patterns/data/transactional-outbox.html
