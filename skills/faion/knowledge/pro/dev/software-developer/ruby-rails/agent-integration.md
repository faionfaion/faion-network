# Agent Integration — Ruby on Rails Backend

## When to use
- Greenfield SaaS or CRUD-heavy domains where Rails-the-omakase (ActiveRecord, ActionController, ActionMailer, ActiveJob, Hotwire) maps cleanly to the product.
- Solo / small-team builds where convention-over-configuration is the productivity edge — you want `rails generate scaffold` shaped code, then refine.
- Modernising an existing Rails 5/6 app to Rails 7+ with Hotwire/Turbo, Solid Queue, Solid Cache, Kamal deploys.
- Backends with substantial async/background work where Sidekiq + Redis is operationally cheap.
- Teams already running RSpec + FactoryBot + Capybara who want service-object + query-object discipline layered on top of Rails defaults.

## When NOT to use
- Hard real-time / low-latency systems (sub-10ms p99). MRI Ruby + Rails middleware is not the right footprint; pick Go/Rust.
- CPU-bound workloads (ML inference, video transcoding). Use Rails as the API surface, push compute to a service in another language.
- Strict single-binary distribution. Rails wants Bundler + a Ruby runtime — not friendly to "drop one binary on the box."
- Polyglot orgs without Ruby expertise. Rails magic (autoloading, callbacks, `method_missing`, scopes) is opaque to non-Ruby agents and becomes a maintenance liability.
- Greenfield where the team explicitly committed to typed Python/Go/TS — Rails is not a "we'll add types later" stack (Sorbet/RBS exists but is opt-in, not idiomatic for most gems).

## Where it fails / limitations
- **Callback hell.** `before_save`, `after_create_commit`, `around_destroy` chains create implicit ordering that breaks when reused via `accepts_nested_attributes_for`. The README's `before_validation :normalize_email` is fine; production accumulates 8 callbacks and diagnoses become forensic.
- **Fat models, then fat services.** Skinny-controller advice pushes logic to model, model bloats, "service objects" extract — but service-object conventions are not standardised. Teams diverge (Interactor, Trailblazer, dry-transaction, hand-rolled `call` like the README).
- **N+1 queries.** ActiveRecord lazy loading is a footgun; `bullet` gem catches local cases, prod still surprises. The README's `with_associations` chain is correct; agents skip it.
- **Strong parameters drift.** `params.require(:user).permit(...)` lists drift from the model schema as columns are added; tests don't catch silent ignored fields.
- **Sidekiq retry semantics.** At-least-once delivery; without idempotency, retries double-charge. README's `return if order.processed?` is the right pattern; agents forget it.
- **Autoloading (Zeitwerk) errors.** Constant-name → file-name mismatch produces `NameError`s only at runtime. Test suites must boot the full app to surface them.
- **Asset pipeline churn.** Sprockets / Webpacker / esbuild / importmap / Propshaft — every Rails upgrade asks you to migrate. Agents copy snippets across pipelines.
- **Scope leakage into tests.** A scope on `User` bleeds into FactoryBot defaults; tests pass locally, fail under random ordering. Use `default_scope` only when you are sure.
- **Database transactional state in tests.** RSpec + transactional fixtures + Sidekiq-inline = surprising commit ordering for `after_create_commit` callbacks.

## Agentic workflow
Drive Rails feature work as a five-stage pipeline: (1) design agent extracts model + endpoint + background-job inventory from the spec; (2) code-gen agent emits migration + model + service object + controller + serializer + RSpec spec aligned to the existing app structure; (3) job agent emits Sidekiq worker + retry/backoff strategy with explicit idempotency; (4) test agent generates request specs, model specs (shoulda-matchers), and service specs with `have_enqueued_mail`; (5) review agent runs the anti-pattern checklist (callbacks > 3, N+1 via `Bullet`, mass-assignment via `permit!`, missing idempotency on jobs). Pin Rails version + key gem versions in `.aidocs/product_docs/rails-stack.md` so agents stop hallucinating Rails 5 syntax in a 7.2 codebase.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — one task = migration + model + service + controller + spec. Sonnet for routine CRUD; opus for service-object boundary + transaction design.
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — run before committing `config/credentials.yml.enc` decrypted dumps, fixtures, or `.env` files; Rails commits are a recurring leak source.
- A **rails-review-agent** (worth adding under `agents/`): single-pass linter for `params.permit!`, `find_each` missing on large iterations, `default_scope`, callbacks > 3 per model, jobs without `idempotent` guard, `update_all` bypassing callbacks unintentionally.
- `feature-executor` skill — sequential mode keeps migration → model → service → controller → spec ordering correct; out-of-order writes leave failing autoload.

### Prompt pattern
Inventory pass:
```
You are a Rails architect. Given the spec in <spec>, produce tables for:
(a) Models: name, columns + indexes, validations, associations, callbacks
   (max 3, justify each).
(b) Endpoints: HTTP verb, path, request params (strong-params list),
   response shape (serializer), status codes.
(c) Jobs: class, queue, retry strategy, idempotency key.
Reject any callback that calls a service object. Reject any job
without an idempotency check.
```

Anti-pattern review pass:
```
You are reviewing a Rails PR. Flag:
(1) params.permit! or no strong-params usage,
(2) callback chain > 3 on a single model,
(3) N+1: controller iterating an association without .includes/.eager_load,
(4) update_all/delete_all that should run callbacks,
(5) Sidekiq job without idempotency guard,
(6) default_scope added,
(7) credentials/.env file committed.
Cite file:line. No fixes — only flags.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `rails` CLI | Generate, migrate, console, server, routes | bundled |
| `bundle` | Gem dependency manager | https://bundler.io |
| `rake` | Task runner (migrations, tests, custom) | bundled |
| `rspec` | Spec runner | https://rspec.info |
| `rubocop` + `rubocop-rails` + `rubocop-rspec` | Linting / style | https://rubocop.org |
| `brakeman` | Static security scanner for Rails | https://brakemanscanner.org |
| `bullet` | Detect N+1 / missing eager-load in dev/test | https://github.com/flyerhzm/bullet |
| `bundler-audit` | CVEs in Gemfile.lock | https://github.com/rubysec/bundler-audit |
| `sidekiq` CLI | Run / inspect Sidekiq workers | https://sidekiq.org |
| `kamal` | Containerised deploys, replaces Capistrano for many Rails apps | https://kamal-deploy.org |
| `solargraph` / `ruby-lsp` | LSP for Ruby; agents use it for symbol resolution | https://solargraph.org |
| `dotenv-rails` / `rails credentials:edit` | Secret management | bundled / `bin/rails credentials:edit` |
| `factory_bot_rails` | Test data factories | https://github.com/thoughtbot/factory_bot_rails |
| `rspec-bisect` | Find spec ordering bugs | `rspec --bisect` |
| `rails db:migrate:status` | Migration drift check | bundled |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Sidekiq + Redis | OSS + SaaS (Sidekiq Pro/Ent) | yes | Default async stack for Rails. |
| Solid Queue / Solid Cache | OSS (Rails 8 default) | yes | Database-backed queue/cache; reduces Redis dependency for small apps. |
| Heroku / Render / Fly.io | SaaS | yes | Idiomatic Rails hosting; agents script with their CLIs. |
| Kamal + bare metal/Hetzner | OSS | yes | DHH's deploy story; agents drive `kamal deploy`. |
| Postgres (managed: RDS/Neon/Supabase) | SaaS | yes | Default DB; `pg` gem. |
| Skylight / Scout APM / Datadog | SaaS | yes | Rails-aware tracing. |
| Honeybadger / Sentry / Rollbar | SaaS | yes | Error tracking; Rails integrations are first-class. |
| AppSignal | SaaS | yes | Combined APM + errors + uptime, strong Rails fit. |
| Faktory | OSS | yes | Multi-language alt to Sidekiq if jobs span Ruby + Go/Python. |
| Mailtrap / Postmark / SES | SaaS | yes | ActionMailer SMTP backends. |
| GoodJob | OSS | yes | Postgres-backed alt to Sidekiq, transactional. |
| Image Magick / libvips + ActiveStorage | OSS | yes | First-class Rails attachment story; libvips beats IM on perf. |

## Templates & scripts
See `templates.md` for service-object, query-object, Sidekiq job, and RSpec skeletons; `examples.md` for full CRUD slices. Add `.bullet.yml` config and a CI step running `bundle exec brakeman --no-pager --quiet --exit-on-warn`. Inline anti-pattern grep:

```bash
#!/usr/bin/env bash
# rails-lint.sh — Rails anti-pattern scan
set -euo pipefail
root="${1:?usage: rails-lint.sh APP_DIR}"
fail=0
echo "## permit! mass-assignment"
grep -rEn 'params(\[.+\])?\.permit!' "$root" && fail=1 || true
echo "## default_scope (avoid)"
grep -rEn '^\s*default_scope' "$root/models" && fail=1 || true
echo "## update_all / delete_all (skip callbacks)"
grep -rEn '\.(update_all|delete_all)\(' "$root" || true
echo "## Sidekiq job missing idempotency comment"
for f in "$root"/jobs/*.rb; do
  grep -q -E '(idempotent|already|processed\?)' "$f" || { echo "no idempotency hint: $f"; fail=1; }
done
echo "## Models with > 3 callbacks"
for f in "$root"/models/*.rb; do
  n=$(grep -cE '^\s*(before|after|around)_(validation|save|create|update|destroy|commit)' "$f" || true)
  [[ "$n" -gt 3 ]] && { echo "$f: $n callbacks"; fail=1; }
done
exit "$fail"
```

## Best practices
- **Service objects are the seam, not the framework.** Keep one shape (`Users::CreateService.new(...).call → ServiceResult`); don't mix Trailblazer + Interactor + hand-rolled.
- **Query objects for non-trivial reads.** Pull chained scopes out of the controller; the README pattern is correct, lint that controllers don't `.where` directly.
- **Cap callbacks.** ≤3 per model, each with a single short method. If you want a fourth, it's probably a service or a job.
- **Strong params + DTOs (serializers).** `params.permit(...)` is the in-boundary; `ActiveModel::Serializers::JSON` / Blueprinter / Alba is the out-boundary. Never render raw `to_json`.
- **Idempotent Sidekiq jobs.** Pass an entity ID, re-fetch inside `perform`, return early if state is already terminal.
- **Backoff strategy per error type.** Linear for "external service down," exponential for unknown errors. README's `sidekiq_retry_in` example is the pattern.
- **Transactions wrap multi-write services.** README wraps `user.save!` + email + audit in `ActiveRecord::Base.transaction`; that block must not include external HTTP calls (push to a job).
- **Disable `open_in_view`-equivalent footguns.** Use `ActiveRecord::Base.strict_loading_by_default = true` in dev/test to make N+1 fail loud.
- **Pin Ruby + Rails patches in CI.** `.ruby-version` + `Gemfile.lock`; agents must not bump majors without explicit approval.
- **Credentials encrypted, env for ops.** `config/credentials.yml.enc` for secrets that ship with code; `ENV` for ops/infra. Never both for the same key.
- **Migrations are forward-only in prod.** Don't rely on `down`; deploy a new migration to revert state.

## AI-agent gotchas
- **Old Rails syntax.** Agents emit Rails 5/6 (`update_attributes`, `serialize :foo, JSON`) in a Rails 7+ project. Pin version in the prompt; lint imports/methods.
- **Convention-over-config bites.** Agents place a model under `app/services/` and Zeitwerk fails to autoload. Enforce path → constant convention via lint.
- **Strong-params drift.** Agent adds a column but forgets `permit`; field silently ignored. Require a spec asserting the column persists.
- **Sidekiq ad-hoc retries.** Agents catch `StandardError` and `raise` blindly, doubling backoff. Force `sidekiq_options retry:` and one explicit `rescue` per error type.
- **`update_all` skipping callbacks.** Agents reach for `.update_all(active: false)` for "perf"; it skips callbacks and audit logs silently. Require justification in PR description.
- **N+1 in serializers.** Agents `belongs_to :user` then serialize `user.profile.name` triggering an extra SELECT per row. Force `.includes(...)` or `Bullet` in CI.
- **Hallucinated FactoryBot traits.** Agents invent `:admin_user` traits; lint factories file membership.
- **Migration + code mismatch.** Agent writes new migration, doesn't run `db:migrate` before generating model code → spec passes locally on stale schema. Force `db:migrate db:test:prepare` in PR setup.
- **Mass-assignment via `permit!`.** Always reject; require explicit field list.
- **Human-in-loop on data migrations.** A migration that touches >100k rows or rewrites enum values needs human review. Don't auto-merge.
- **Background-job idempotency drift.** Each retry should hit a guard; agents test happy path and skip the retry case. Force a spec asserting `perform` twice changes state once.

## References
- Rails Guides. https://guides.rubyonrails.org
- Rails API docs. https://api.rubyonrails.org
- Sidekiq Wiki. https://github.com/sidekiq/sidekiq/wiki
- Hartl, M. "Ruby on Rails Tutorial," 7th+ ed. https://www.railstutorial.org
- Fernandez, O. "The Rails 7 Way."
- Sutton, J. "Refactoring Rails." Series of small books / blog posts.
- thoughtbot blog (service objects, FactoryBot, RSpec). https://thoughtbot.com/blog
- Codeship/CloudBees Rails best-practices. https://github.com/flyerhzm/rails_best_practices
- DHH on Hotwire / Solid Queue / Kamal. https://world.hey.com/dhh
- Sibling methodologies in this repo: `pro/dev/software-developer/clean-architecture/`, `pro/dev/software-developer/microservices-design/`, `pro/dev/code-quality/domain-driven-design/`.
