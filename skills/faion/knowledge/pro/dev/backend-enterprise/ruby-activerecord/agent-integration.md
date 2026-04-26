# Agent Integration — ActiveRecord Patterns

## When to use
- Building or refactoring a Rails app where models exceed ~150 lines and inline `where` chains scatter across controllers and views.
- Multi-tenant Rails apps where global scopes, default scopes, and tenant-aware queries must be enforced consistently.
- Codebases adopting Trailblazer / dry-rb partials — Query Objects play nicely as ingest into the new architecture.
- Rails apps with measured ORM hot paths (>30% of request time in AR) — query objects + eager loading patterns measurably improve.
- LLM-driven feature work where you want each AR query reviewable in isolation rather than buried in a controller.

## When NOT to use
- Simple CRUD admin (Rails Admin / ActiveAdmin): the framework manages queries; query objects add ceremony.
- Rails apps under 1k LOC — direct AR `scope` blocks plus thin controllers are fine.
- Read-replicas / sharded DBs where you need raw `connected_to(role: :reading)` calls — query object DSL hides that switch.
- Background-only workers that operate on enqueued IDs and `find_each` — no benefit from a chained query object.
- Reporting/analytics queries — drop to `ActiveRecord::Base.connection.execute` with explicit SQL; AR hydration is the bottleneck.

## Where it fails / limitations
- **N+1 by default.** Lazy associations are AR's killer trap. Without `includes` / `preload` / `eager_load`, agents copy patterns straight into prod regressions.
- **`default_scope` lies.** Once `default_scope { where(deleted_at: nil) }` exists, every `unscoped`/`with_deleted` decision is invisible at call site. Agents can't tell if they're getting all rows.
- **Callback chains explode.** `before_save → after_commit → after_create_commit`-driven logic re-fires on tests, on fixture loads, and at the wrong transactional boundary.
- **Query objects without builder discipline.** Agents add a method per use case; the query object grows to 30 methods covering one-off filters.
- **`includes` vs `preload` vs `eager_load` confusion.** `includes` heuristically picks; agents add `where` on the joined table and it silently switches strategy → broken behavior.
- **Caching invalidation gaps.** AR `cache_key_with_version` invalidates on `updated_at`; agents forget `touch: true` on `belongs_to`, parent caches go stale.
- **`update_all` skips callbacks.** Agents reach for it on bulk paths; `paper_trail`, `counter_cache`, and audit logs silently break.
- **`first` without `order` is non-deterministic** in Postgres — looks fine in tests, breaks under concurrent inserts.

## Agentic workflow
Drive AR work as: (1) a planner subagent reads `app/models/*.rb` and `db/schema.rb` and emits target query/scope changes; (2) a code-writer subagent generates model + scopes + query object + RSpec specs in one pass; (3) a perf subagent runs the test suite under `bullet` (N+1 detector) and `prosopite` and fails on any detection; (4) a migration subagent generates indexes for new `where`-columns and verifies via `EXPLAIN`. Persist changes as `app/models/*.rb` + `app/queries/*.rb` + `db/migrate/*.rb`; agents must touch all three or schema drifts.

### Recommended subagents
- `faion-backend-agent` (referenced in README frontmatter) — implementer for models, scopes, query objects.
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — one task per scope/query object refactor; quality gate runs RSpec + Bullet + Rubocop.
- A purpose-built **ar-perf-agent** (worth creating): runs `rspec` with `Bullet.alert = true` and `prosopite` enabled, parses output, returns offending file:line and proposed `includes` fix.
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — scrub `db/seeds.rb` and fixtures before commit; AR seeds often hard-code emails and tokens.

### Prompt pattern
Scope + query object refactor:
```
You are a Rails 7.1 backend engineer. Move all `User.where(...)`
chains in app/controllers/admin/users_controller.rb into a
UsersQuery class under app/queries/. Output: query class, model
scopes for primitives (active, search), updated controller. Keep
each method ≤8 lines. Run: bundle exec rspec spec/queries/.
```

N+1 detection pass:
```
Run `BULLET=true bundle exec rspec`. For each Bullet warning,
report: spec file, model, association, and propose `.includes(...)`
on the relevant query. Do not modify specs; only modify
controllers, queries, or models. Re-run until zero warnings.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `rails generate model` / `rails db:migrate` | Scaffold + migrate | bundled with Rails |
| `bin/rails console` | Headless REPL for relation testing | bundled |
| `bullet` | N+1 + unused eager-load detector | `gem 'bullet'` (development/test) |
| `prosopite` | Newer N+1 detector, lower noise than Bullet | `gem 'prosopite'` |
| `rails-erd` | Generate ERD diagrams from schema | `gem 'rails-erd'` |
| `strong_migrations` | Block dangerous migrations (e.g., `add_index` without `algorithm: :concurrently`) | `gem 'strong_migrations'` |
| `rubocop-rails` / `rubocop-rspec` | Style + lint, runs in pre-commit | `gem 'rubocop-rails'` |
| `bundle exec rake db:rollback` | Reversibility check before commit | bundled |
| `lol_dba` | Find missing indexes | `gem 'lol_dba'` |
| `pg_query` / `EXPLAIN ANALYZE` | Query plan inspection | Postgres builtins |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Heroku Postgres / RDS / Neon | Managed Postgres | API yes | Branching DBs play well with Rails migrations per branch. |
| Skylight / Scout APM / NewRelic | SaaS APM | API yes | Per-AR-query timing surfaces patterns Bullet missed. |
| Sentry | SaaS errors | API yes | Catches `ActiveRecord::*` exceptions; tag with migration version. |
| pgHero | OSS | yes | Postgres dashboard; `slow queries`, `unused indexes` agents can act on. |
| ActiveRecord-Reset | OSS | yes | Helper for test isolation around `default_scope`. |
| Trailblazer | OSS | yes | Operation/Query objects upgrade path from this pattern. |
| dry-rb (`dry-validation`, `dry-monads`) | OSS | yes | Query object inputs validated; results returned as monads agents can compose. |

## Templates & scripts
See `templates.md` for query object skeleton. Add a CI gate for query budget + missing indexes (≤50 lines):

```bash
#!/usr/bin/env bash
# ar-budget.sh — fail CI on N+1 or queries over per-spec budget.
# Usage: ar-budget.sh [BUDGET]
set -euo pipefail
BUDGET="${1:-15}"
export BULLET=true PROSOPITE=true
LOG=$(mktemp)
bundle exec rspec --format documentation 2>&1 | tee "$LOG"
ruby -e '
budget = ARGV[0].to_i
log = File.read(ARGV[1])
fails = []
log.scan(/^(.+?_spec\.rb:\d+).*?queries:\s*(\d+)/m) do |loc, n|
  fails << [loc, n.to_i] if n.to_i > budget
end
nplus1 = log.scan(/USE eager loading detected.*$/).length \
  + log.scan(/Prosopite::NPlusOneQueriesError/).length
unless fails.empty? && nplus1.zero?
  puts "FAIL: #{nplus1} N+1, #{fails.size} budget breaches"
  fails.each { |loc, n| puts "  #{loc}: #{n} queries (>#{budget})" }
  exit 1
end
puts "OK: zero N+1, all specs ≤#{budget} queries"
' "$BUDGET" "$LOG"
bundle exec rake lol_dba:missing_indexes || true
```

Wire into `.github/workflows/ci.yml` as a required check.

## Best practices
- **Eager-load at the controller boundary, never in views.** A view triggering a query is invisible in code review.
- **Avoid `default_scope`.** Use named scopes (`scope :active`) and force callers to opt-in. Removes hidden filters.
- **`scope` only for parameterless or primitive queries.** Anything taking a model/relation goes into a Query Object.
- **Use `find_each` / `in_batches` for any loop over >1k records.** Prevents memory blowups; agents `User.all.each` by default.
- **Counter caches with `counter_cache: true` + `touch: true`.** Otherwise list endpoints recount every render.
- **Indexes for every `where` and `order_by` column.** Add via migration; verify with `lol_dba:missing_indexes`.
- **Keep callbacks idempotent.** `after_create_commit` may fire twice in edge cases; design for it.
- **Avoid `update_all` on audited or paper-trailed models.** Use `update!` per record or temporarily disable callbacks explicitly.
- **`includes` for read paths; `joins` for filter-only paths** (where you don't need the joined object). Document the choice in a comment.
- **Test scopes in isolation.** `RSpec.describe '.active'` block — agents otherwise test scopes only via the controller.

## AI-agent gotchas
- **Hidden `default_scope`.** Agent reads model, doesn't see scope, writes `User.where(...)`, gets fewer rows than expected. Force agents to grep for `default_scope` before any query change.
- **`where` after `includes` switches strategy silently.** `User.includes(:posts).where('posts.flagged = true')` triggers `eager_load` (one big LEFT OUTER JOIN); plan changes drastically. Use `references(:posts)` or split queries explicitly.
- **`save` vs `save!` confusion.** Agents use `save` and don't check return; record silently fails validation. Standardize on `save!` + rescue at the boundary, or always check `.persisted?`.
- **`update_columns` skips validations AND callbacks.** Agents reach for it for "performance"; audit logs and counter caches go stale. Whitelist methods in code review.
- **Polymorphic `belongs_to` typos.** Wrong `as:` argument silently writes wrong type strings; integrity is not enforced. Add a `before_validation` to enforce the type from a constant list.
- **Test DB ≠ prod DB.** Agents test on sqlite, ship to Postgres; case sensitivity, JSON column behavior, and array types diverge. Force Postgres in CI from day 1.
- **Strong migrations bypass.** Agents `add_index :users, :email` blocking writes for minutes on big tables. Use `algorithm: :concurrently` and `disable_ddl_transaction!` — `strong_migrations` gem enforces.
- **Memoization on a relation.** Agents `@users ||= User.where(...)` returns a relation that re-queries on each `.each`. Memoize `.to_a` not the relation.
- **`pluck` for fields, not records.** Agents `User.where(active: true).map(&:id)` instead of `pluck(:id)` — 100x slower at scale. Lint via Rubocop `Rails/Pluck`.
- **Query object growing into a god class.** Cap at ~10 chainable methods; if more needed, split by use case into multiple query objects.
- **Schema drift across branches.** Two agents add migrations with the same timestamp on parallel branches; merge produces non-deterministic order. Use `bin/rails db:migrate:status` in CI to catch.
- **`destroy` cascade through `dependent: :destroy`** can fan out to thousands of records. Force agents to `find_each` + explicit destroy when chains are deep, or switch to soft delete + background cleanup job.

## References
- Rails Guides — Active Record Query Interface. https://guides.rubyonrails.org/active_record_querying.html
- Rails Guides — Active Record Callbacks. https://guides.rubyonrails.org/active_record_callbacks.html
- thoughtbot — "How We Test Rails Applications" (query objects). https://thoughtbot.com/blog
- "7 Patterns to Refactor Fat ActiveRecord Models." https://codeclimate.com/blog/7-ways-to-decompose-fat-activerecord-models/
- Bullet gem README. https://github.com/flyerhzm/bullet
- Prosopite README. https://github.com/charkost/prosopite
- Strong Migrations README. https://github.com/ankane/strong_migrations
- Sibling methodologies in this repo: `pro/dev/backend-enterprise/ruby-rails/`, `pro/dev/backend-enterprise/ruby-rails-patterns/`, `pro/dev/backend-enterprise/ruby-rspec-testing/`, `pro/dev/backend-enterprise/decomposition-rails/`.
