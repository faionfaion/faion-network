# Agent Integration — Ruby ActiveRecord Patterns

## When to use
- Rails 7+ apps where `User.where(...).where(...).joins(...)` chains spread across controllers and models, requiring extraction into Query Objects.
- Tightening N+1 hygiene with `includes`, `preload`, `eager_load`, and `strict_loading!`.
- Standardizing scope/callback/observer patterns; replacing scattered `before_save` hooks with explicit Interactors.
- Pagination + filtering + searching reused across endpoints — Query Objects beat copy-pasted scopes.

## When NOT to use
- Trivial CRUD where `Model.find(id)` and `Model.create!` cover the need; Query Objects add ceremony.
- Reporting / analytics — drop into raw SQL via `find_by_sql`, `select` with `Arel`, or a separate read replica.
- Bulk operations >10k rows — use `insert_all`, `upsert_all`, `update_all`, or `find_each(batch_size: 1000)`.
- Multi-database read/write splits — ActiveRecord's `connected_to` API needs explicit blocks; Query Objects hide where the connection comes from.

## Where it fails / limitations
- Callbacks are a memetic source of bugs: order, `:after_commit` vs `:after_save`, transactional rollback, nesting. Agents copy them without understanding ordering.
- `scope :active, -> { where(active: true) }` returns relations chainable with `.merge`; agents then `.merge` two scopes that conflict on the same column → silently wrong WHERE.
- `includes` decides between `preload` (separate query) and `eager_load` (LEFT OUTER JOIN) by heuristic — agents can't predict which.
- `dependent: :destroy` triggers per-record callbacks; with 100k children this kills the request. Use `:delete_all` when callbacks aren't needed.
- `default_scope` is a hidden trap; new queries inherit it and bypassing requires `unscoped`.

## Agentic workflow
A subagent should: (1) inventory existing scopes/callbacks on the model; (2) propose a Query Object that subsumes chained scopes; (3) generate `app/queries/<name>_query.rb` + RSpec covering each chain combination + N+1 detection (using `bullet` or `query_count`); (4) refactor controllers to call the query. Always require a test that asserts SQL query count to lock down N+1 fixes.

### Recommended subagents
- `faion-sdd-executor-agent` — TDD loop with quality gates.
- A `rails-query-object` subagent (project-local) — produces query class + spec + controller wiring.

### Prompt pattern
```
Refactor the User listing in Api::V1::UsersController#index into UsersQuery.
- Method-chained API: .active.with_role(:admin).search(term).ordered.paginate(page: n)
- Always eager-load :profile and :roles
- Spec must:
  - test each method in isolation
  - test full chain produces correct SQL via to_sql snapshot
  - assert query count <= 3 with bullet/db_query_matchers
Do NOT add a default_scope. Keep User model untouched except for #ransackable_attributes.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `rails console`, `rails dbconsole` | Interactive query iteration | core |
| `bullet` gem | Detect N+1, unused eager loads at runtime | https://github.com/flyerhzm/bullet |
| `prosopite` gem | Better N+1 detector (catches more cases than bullet) | https://github.com/charkost/prosopite |
| `query_count` / `db-query-matchers` | RSpec matcher: `expect { ... }.to make_database_queries(count: 1)` | https://github.com/brigade/db-query-matchers |
| `lol_dba` | Find missing indexes from associations | https://github.com/plentz/lol_dba |
| `pg_query` | Parse + analyze SQL in CI | https://github.com/lfittl/pg_query |
| `ransack` gem | Search forms over ActiveRecord scopes | https://activerecord-hackery.github.io/ransack/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| pganalyze / pgHero | SaaS / OSS | Yes | Surfaces slow queries; agents can read recommendations |
| Skylight / Scout APM | SaaS | Yes | Per-endpoint query breakdown |
| Datadog APM Ruby | SaaS | Yes | Auto-traces ActiveRecord queries |
| pgvector / Searchkick / Meilisearch | OSS | Yes | When `LIKE '%term%'` is too slow, switch to full-text |
| Marginalia | OSS | Yes | Annotate SQL with controller#action — easier debugging from logs |

## Templates & scripts
See `templates.md` for query-object scaffold. Snippet — N+1 lock-down test:

```ruby
# spec/queries/users_query_spec.rb
require "rails_helper"

RSpec.describe UsersQuery do
  describe "#paginate with associations" do
    before { create_list(:user, 5, :with_roles) }

    it "executes constant number of queries" do
      query = described_class.new.active.with_associations.paginate(page: 1)
      expect { query.results.each { |u| u.profile && u.roles.size } }
        .to make_database_queries(count: 3)  # users, profiles, roles
    end

    it "freezes generated SQL shape" do
      sql = described_class.new.active.with_role("admin").results.to_sql
      expect(sql).to include('INNER JOIN "roles"')
      expect(sql).to include('"users"."active" = TRUE')
    end
  end
end
```

## Best practices
- Prefer explicit `preload` over `includes` when you don't need WHERE on the joined table — avoids `eager_load`'s OUTER JOIN cost.
- Use `strict_loading!` per record or globally in dev to surface accidental lazy loads.
- Index every FK column AR creates (`belongs_to`); add composite indexes for `where(:a, :b).order(:c)` patterns.
- Wrap multi-record writes in `ActiveRecord::Base.transaction` and use `lock!`/`with_lock` for read-modify-write.
- Avoid `default_scope` — explicit `Model.active` is clearer and safer.
- Use `.find_each` / `.in_batches` for any iteration over >1k rows; never `.all.each`.
- For complex search, build with Arel (`User.arel_table[:name].matches("%x%")`) — string interpolation is a SQLi vector.
- Move counter caches to `counter_cache: true` instead of `User.posts.count` in views.

## AI-agent gotchas
- Agents write `Model.where("name LIKE '%#{term}%'")` — SQL injection. Always require `?` binds or `sanitize_sql_like`.
- They mix `before_save` and `before_create` without understanding the order; require explicit ordering in code review.
- LLMs put query-building logic in controllers ("just one more `.where`"). Reject controller diffs with more than one chained `.where`.
- They forget `dependent:` on associations, leaking children on parent destroy.
- Generated migrations frequently miss `null: false` and FK constraints (`add_foreign_key`); enforce strong_migrations gem checks.
- Human-in-loop checkpoint: run `EXPLAIN ANALYZE` on prod-like data for new queries — agents can't predict cost; review query plan before merge.

## References
- "Sustainable Web Development with Ruby on Rails" — David Bryant Copeland
- Code Climate — "7 Patterns to Refactor Fat ActiveRecord Models": https://thoughtbot.com/blog/7-patterns-to-refactor-fat-activerecord-models
- "The Rails Way" / "Ruby on Rails Guides" — Active Record Query Interface: https://guides.rubyonrails.org/active_record_querying.html
- Rails source — `ActiveRecord::Relation`: https://github.com/rails/rails/tree/main/activerecord
- Nate Berkopec — "The Complete Guide to Rails Performance"
