# Agent Integration — Ruby on Rails Backend

## When to use
- Generating new Rails 7+ resources (models, controllers, services, jobs) using the project's existing conventions: service objects with `ServiceResult`, query objects, RSpec, FactoryBot, Sidekiq.
- Refactoring "fat controller" / "fat model" code into dedicated service and query objects per the methodology.
- Adding background processing for slow workflows: Sidekiq jobs with retry policies, dead-letter handling, batch processing via `find_each`.
- Auditing N+1 queries, missing eager-loading, and unindexed FKs in an existing Rails app.

## When NOT to use
- The project uses Hanami, Sinatra, or pure Rack — Rails conventions don't transfer.
- You're inside an Active Admin / Spree engine where conventions diverge — defer to the engine's patterns.
- High-throughput message processing (>10k msg/s) — Sidekiq + Redis hits ceiling; use Karafka or a dedicated Go/Rust worker.
- The team is on Rails 5/6 LTS — some patterns (`after_create_commit`, encrypted attributes, Trilogy adapter) require Rails 7+.

## Where it fails / limitations
- LLM-generated controllers default to ActiveRecord directly in actions (`User.create(params)`); reject this — the methodology mandates service objects.
- Agents emit `before_save` callbacks that mutate state in surprising ways and break tests; prefer explicit service-layer logic with one public `#call`.
- Sidekiq retry counts and `dead: true` flags are easy to mistype; the agent must read `sidekiq.yml` and existing job class to align with team conventions.
- `params.permit(...)` is often forgotten or too permissive ("permit!"); CI must enforce strong parameters.
- N+1 detection: `bullet` gem catches them in dev/test; agent must enable it before generating views/serializers.
- Rails 7's encrypted attributes need `bin/rails db:encryption:init` first — agents skip this and produce migrations that crash in CI.

## Agentic workflow
A subagent generates a vertical slice: migration → model → service → controller → job (if async) → RSpec specs → factories. It runs `bundle exec rspec` and `bundle exec rubocop` in a sandbox, iterating until green. A second pass runs `bundle exec brakeman` and `bundle exec bundler-audit` for security, plus `bullet` log review for N+1. Schema changes require explicit human approval before `db:migrate` in non-dev envs.

### Recommended subagents
- `faion-sdd-executor-agent` — vertical-slice generator with quality gates (rubocop, rspec, brakeman, bundler-audit).
- `faion-feature-executor` — multi-task delivery (migration → model → service → controller → spec).
- A custom `rspec-runner` agent scoped to `Bash(bundle exec rspec:*)`, `Bash(bundle exec rubocop:*)`, `Read`, `Edit`.
- For background jobs: pair with a `sidekiq-runner` agent that can read `web/sidekiq` and JSON metrics, but cannot drain queues.

### Prompt pattern
```
Add resource Order with fields total_cents:integer, status:string,
user:references. Generate migration, model with scopes
(:pending, :paid, :failed), Orders::CreateService returning ServiceResult,
Api::V1::OrdersController#create using strong params, RSpec model + service
+ request specs with FactoryBot. Run bundle exec rspec and rubocop.
```

```
Audit app/services/**/*.rb. For each service, check: 1) one public #call,
2) ServiceResult.success/failure, 3) ActiveRecord::Base.transaction wraps
multi-step writes, 4) no controller-layer logic. Output a checklist.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `bundle` / `bin/rails` | Standard build, generate, console | bundled |
| `rspec`, `factory_bot_rails` | Tests + factories | Gemfile |
| `rubocop` + `rubocop-rails`, `rubocop-rspec` | Style + Rails-specific lint | Gemfile |
| `brakeman` | Static security scanner | `gem install brakeman` |
| `bundler-audit` | CVE scan on Gemfile.lock | `gem install bundler-audit` |
| `bullet` | N+1 detection (dev/test) | Gemfile :development, :test |
| `standard` (alt to rubocop) | Opinionated formatter | optional |
| `sidekiq` CLI + `sidekiqmon` | Worker, queue inspection | bundled with sidekiq |
| `derailed_benchmarks` | Memory + boot diagnostics | Gemfile |
| `rails-erd` / `dbml` exporter | Generate schema diagrams | optional |
| `dotenv-rails` | Local env vars | Gemfile :development, :test |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Heroku / Render / Fly.io | SaaS | Yes | Standard Rails buildpack; CLI scriptable. |
| AWS RDS Postgres | SaaS | Yes | Standard adapter; agent uses `psql` for ad-hoc. |
| Redis Cloud / ElastiCache | SaaS | Yes | Sidekiq backend. |
| Sidekiq Pro / Enterprise | SaaS | Partial | Adds batches / unique jobs; license-gated, cannot scaffold without key. |
| GoodJob, SolidQueue | OSS | Yes | DB-backed alternatives to Sidekiq for small scale. |
| Sentry / Honeybadger / Rollbar | SaaS | Yes | Error tracking; agent reads issue API. |
| Skylight / Scout APM / New Relic | SaaS | Yes | Performance traces; agent pulls slow endpoints. |
| AppSignal | SaaS | Yes | Combined APM + errors + logs. |

## Templates & scripts
See `templates.md` for service object, query object, and Sidekiq job skeletons. Inline pre-commit verification:

```bash
#!/usr/bin/env bash
# verify-rails.sh
set -euo pipefail
bundle exec rubocop --parallel
bundle exec rspec --format progress
bundle exec brakeman -q --no-pager --exit-on-warn
bundle exec bundler-audit check --update
echo "OK: lint + tests + security passed"
```

## Best practices
- One public method per service: `#call`. Constructor takes deps + params; never reach into globals.
- Wrap multi-record writes in `ActiveRecord::Base.transaction` and raise — never silently `save` and check `errors`.
- `find_each(batch_size: 1000)` for any iteration over `> 1000` records; loose `.each` causes Heroku R14 OOM.
- `after_create_commit` for side effects that need the row persisted (mailers, jobs); never `after_save` for these.
- Sidekiq jobs accept primitives (IDs, strings) — never AR objects; job runs on different process / time.
- Add DB-level constraints (`null: false`, `foreign_key: true`, unique indexes) — model validations alone race.
- Gem upgrades through `bundle outdated --groups` and run `bundle exec rails app:update` for Rails majors.

## AI-agent gotchas
- Agents fall back to ActiveRecord callbacks (`before_save :do_thing`) for cross-cutting work — review and push into services.
- Strong parameters are silently regenerated as `params.permit!` — fail CI on this string.
- `update_columns` / `update_all` skip callbacks AND validations; agents reach for them to "make tests pass" — block in review.
- Sidekiq jobs without `retry: <N>` and without idempotency cause double-processing on transient errors; require explicit retry config.
- LLMs use `Time.now` instead of `Time.current` — wrong timezone in test CI.
- Rails secrets vs credentials confusion (Rails 5.2+ encrypted credentials.yml.enc); agents emit `Rails.application.secrets` (deprecated). Use `Rails.application.credentials.dig(:scope, :key)`.
- Human-in-loop checkpoint: any migration with `remove_column`, `rename_column`, or `down` block — review before `db:migrate`.
- `where("name LIKE ?", "%#{q}%")` pattern: agents generate this safely, but reviewers should confirm parameterization (no string interpolation into raw SQL).
- Sidekiq jobs that take >30s can be killed at deploy; agent should chunk into smaller jobs or use Sidekiq Iterable Job.

## References
- Rails Guides: https://guides.rubyonrails.org
- Sidekiq Wiki: https://github.com/sidekiq/sidekiq/wiki
- Brakeman: https://brakemanscanner.org
- Bullet: https://github.com/flyerhzm/bullet
- Sandi Metz, "Practical Object-Oriented Design in Ruby" (POODR)
- Avdi Grimm, "Confident Ruby"
- Justin Searls, "Test Doubles" (testdouble.com posts)
- Andrew Kane (Ankane) gems — `pghero`, `searchkick`, `ahoy` — battle-tested patterns
