# Agent Integration — Rails Decomposition Patterns

## When to use
- Greenfield Rails 7+ app where you want LLM agents to work in small files (50-150 LOC) instead of fat models.
- Refactoring legacy Rails monoliths with 500-line models or 400-line controllers — decomposition is a precondition for safe agent edits.
- Codebases adopting Service Objects, Query Objects, Form Objects, and Policies — pattern provides a stable convention.
- Multi-developer or multi-agent teams where parallel work on `User`, `Order`, `Billing` must avoid merge collisions.
- Apps adopting SDD (`spec → design → impl-plan → tasks`): one task = one Service Object is a clean unit of work.

## When NOT to use
- Tiny Rails apps (<20 controllers) — `scope` + thin controllers cover it; service-object ceremony costs more than it earns.
- Codebases on Trailblazer / Hanami / dry-rb — they have their own decomposition idioms; mixing produces incoherence.
- Rails Engines for shared internal libs — different patterns apply (engine boundaries, not service objects).
- Hot paths (background jobs processing >1k/s) — service-object indirection adds GC pressure; drop to PORO or direct AR.
- Prototype phase where domain is unstable — locking shapes into service objects + form objects slows discovery.

## Where it fails / limitations
- **Service-object explosion.** Every controller action gets its own `Users::CreateService`, `Users::UpdateService`, `Users::DeleteService`; agents copy boilerplate without consolidating.
- **No standard return shape.** Some services return the record, some return a Result monad, some raise. Agents inconsistent across files.
- **Concerns become dumping grounds.** `Searchable`, `Authenticatable`, `Sluggable` end up with cross-concern logic; LLMs can't reason about model behavior without reading every concern.
- **Form object vs Service object overlap.** Both validate; agents pick whichever they saw last.
- **Query object drift from `scope`.** Same filter exists in both; agents fix one site and forget the other.
- **Convention not enforced by Rails.** `app/services/` is a folder convention only; the next agent introduces `app/lib/services/` or `app/operations/`.
- **Rails callbacks still fire.** Decomposing into services doesn't remove `before_save` magic; agents assume "service-only flow" and break audit logs.

## Agentic workflow
Treat each feature as a tree: `Controller → Service(s) → QueryObject + FormObject + Serializer + Policy + Job + Spec`. Drive with: (1) a planner subagent emits the file list with target line ranges (per `decomposition-rails/README.md` size table); (2) a code-writer subagent generates files in dependency order (FormObject → Service → Controller → Serializer); (3) a test subagent writes one RSpec describe per Service `#call`; (4) a structural-lint subagent fails the PR if any controller exceeds 150 LOC, any model exceeds 150 LOC, or any service exceeds 100 LOC. Persist the convention in `CONTRIBUTING.md` and load as system prompt context.

### Recommended subagents
- `faion-backend-agent` (referenced in README frontmatter) — implementer for services, query objects, form objects.
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — one SDD task per service object; quality gate runs RSpec + Rubocop + Bullet.
- A purpose-built **decomposition-lint-agent** (worth creating): walks `app/` and fails if `controllers/*.rb` LOC > 150, `models/*.rb` LOC > 150, or `services/` is missing for a feature with >2 endpoints.
- `faion-feature-executor` (skill at `skills/faion-feature-executor/`) — sequences the service-object breakdown across SDD tasks.

### Prompt pattern
File-tree generation:
```
You are a Rails 7.1 architect using the decomposition pattern in
decomposition-rails/README.md. Given the spec <spec.md>, output the
exact list of files to create with target LOC ranges from the
"File Size Guidelines" table. One service object per use case.
Form objects for any multi-attr write. Controllers ≤80 LOC. Output
as a markdown checklist; no code yet.
```

Implementation pass:
```
For each file in <checklist>, generate code matching the patterns
in decomposition-rails/README.md sections "Service Object Pattern",
"Query Object Pattern", "Controller Pattern". Wrap multi-write
services in ActiveRecord::Base.transaction. Ship one RSpec spec per
service. Run: bundle exec rubocop && bundle exec rspec.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `bin/rails generate scaffold` | Initial scaffold to decompose | bundled |
| `bundle exec rubocop -a` | Style + lint, runs in pre-commit | `gem 'rubocop-rails'` |
| `bundle exec rspec` | Test runner; one spec per service | `gem 'rspec-rails'` |
| `bullet` | N+1 detector; required when query objects shift query semantics | `gem 'bullet'` |
| `reek` | Code-smell detector (long classes, low cohesion) | `gem 'reek'` |
| `flog` / `flay` | Per-class complexity + duplication | `gem 'flog'`, `gem 'flay'` |
| `dawnscanner` / `brakeman` | Security scan (mass assignment, SQLi) | `gem 'brakeman'` |
| `rails stats` | LOC per layer; baseline for size budgets | bundled |
| `rubycritic` | HTML report combining flog + reek + flay; CI-ready | `gem 'rubycritic'` |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Trailblazer | OSS | yes | First-class Operation/Step/Contract for service objects; upgrade path. |
| dry-rb (`dry-monads`, `dry-validation`, `dry-struct`) | OSS | yes | Service-object Result monad + form object validation; agents handle the DSL well. |
| Interactor / Interactor::Organizer | OSS | yes | Lightweight service-object wrapper; standardizes return shape. |
| ActiveModel::Validations | First-party | yes | Use for form objects without inheriting from ActiveRecord. |
| Pundit / CanCanCan | OSS | yes | Policies extracted from controllers — required for any decomposition pattern. |
| Skylight / Scout APM | SaaS APM | API yes | Per-service-method timing surfaces decomposition cost. |
| GitHub Actions / GitLab CI | CI | yes | Run Rubocop + RSpec + Brakeman as pre-merge gate. |
| Sentry | SaaS errors | API yes | Tag errors by service-object class. |

## Templates & scripts
The methodology already ships file-tree templates in `templates.md`. Add a structural lint (≤50 lines):

```bash
#!/usr/bin/env bash
# decomp-rails-lint.sh — fail if Rails decomposition convention is broken.
# Usage: decomp-rails-lint.sh app/
set -euo pipefail
ROOT="${1:-app}"
fail=0
check() {
  local pattern="$1" max="$2" label="$3"
  while IFS= read -r f; do
    n=$(wc -l <"$f")
    if [ "$n" -gt "$max" ]; then
      echo "FAIL $label: $f has $n lines (max $max)"
      fail=1
    fi
  done < <(find "$ROOT" -path "$pattern" -type f)
}
check "*/controllers/*.rb"    150 "Controller"
check "*/models/*.rb"         150 "Model"
check "*/services/*/*.rb"     100 "Service"
check "*/queries/*/*.rb"       80 "Query"
check "*/serializers/*.rb"    100 "Serializer"
check "*/policies/*.rb"        80 "Policy"
controllers=$(find "$ROOT/controllers" -name '*_controller.rb' | wc -l)
services=$(find "$ROOT/services" -name '*.rb' 2>/dev/null | wc -l)
if [ "$controllers" -gt 5 ] && [ "$services" -eq 0 ]; then
  echo "FAIL: ${controllers} controllers but app/services/ is empty"
  fail=1
fi
exit "$fail"
```

Wire into `.husky/pre-commit` or GitHub Actions `quality` step.

## Best practices
- **One service = one verb.** `Users::CreateService` (not `Users::Service.create`). Maps cleanly to SDD task names.
- **Service `#call` returns a domain object or a Result monad — never `nil`.** Pick one and document. Agents otherwise mix conventions.
- **Form objects validate, services execute.** Don't validate inside the service; surface errors at the form-object boundary so the controller renders them cleanly.
- **Query objects accept and return relations.** Initialize with `relation = Model.all`; chain returns `self`; final `.results` returns the relation. Agents misuse and return arrays prematurely.
- **Concerns hold mixin behavior, not domain logic.** If a concern grows beyond 50 LOC, it's a service waiting to happen.
- **Serializers (or `jbuilder`/`fast_jsonapi`) own response shape.** Never `render json: model` directly — leaks columns.
- **Policies authorize at the controller boundary.** Services assume authorization passed; otherwise services duplicate auth logic.
- **Tag generated files with the spec ID** (e.g., `# @sdd FEAT-007`). Lets agents trace files back to specs during refactor.
- **Lint-as-you-go.** Run Rubocop + Reek + structural-lint in pre-commit so the next agent inherits a clean tree.
- **Reject `Service.new(...).call` chains in controllers** — promote to `service = ...; result = service.call`. Easier to mock and read.

## AI-agent gotchas
- **Pattern collapse under deadline pressure.** When asked to "just add an endpoint quickly," agents skip the service layer. Lock convention in `CONTRIBUTING.md` and reference in every system prompt.
- **Form-object/service-object validation drift.** Agent adds a field to the form, forgets the service's internal invariant check. Centralize: form validates input shape, service validates business rules.
- **Service calling service in same request.** Acceptable if explicit; not acceptable if a deep chain spans transactions. Force agents to declare orchestration in the docblock.
- **Query objects re-implementing scopes.** Agents add `where(active: true)` inside a query object that's already a `scope :active` on the model. Reuse scopes in query objects via `relation.active`.
- **Test-per-service ignored.** Agents assume the controller spec covers the service; it doesn't cover edge cases. Require `services/*/*.rb` ↔ `spec/services/*/*_spec.rb` parity.
- **Service skipping callbacks via `update_columns`.** Agents reach for it for "performance"; counter caches and audit logs silently break.
- **Agents invent new layers.** "Manager", "Coordinator", "Workflow" classes appear after a refactor. Whitelist namespaces (`services/`, `queries/`, `forms/`, `policies/`, `serializers/`) and block PRs introducing new ones without an ADR.
- **Decomposition without DI.** Agents `Users::CreateService.new(params: ...).call` everywhere; mocking is awkward. Standardize on dependency-injected services or use `dry-system`.
- **Service returns void.** Agent emits `def call; @user.save!; end` — downstream code can't compose. Always return the canonical entity or Result.
- **Policy bypass via `find` instead of policy scope.** Agents `User.find(params[:id])` then check policy; multi-tenant data leaks via timing attack on `find`. Use `policy_scope(User).find(...)`.
- **Form object inheriting from ActiveRecord.** Agents reach for `ActiveType::Object` or similar to "save like a model"; produces ghost columns and confusing schema. Use `ActiveModel::Model` + plain attributes only.
- **Serializer leaks fields.** Agent uses `attributes :all` or `model.as_json` inside a serializer. Always explicit attribute lists.

## References
- "Refactoring Rails" by Vladimir Dementyev. https://refactoringrails.com
- thoughtbot — "How We Test Rails Applications" + service object posts. https://thoughtbot.com/blog
- "7 Patterns to Refactor Fat ActiveRecord Models." https://codeclimate.com/blog/7-ways-to-decompose-fat-activerecord-models/
- Trailblazer — Operation pattern docs. https://trailblazer.to/2.1/docs/operation
- dry-rb — `dry-monads` Result. https://dry-rb.org/gems/dry-monads
- Rails Guides — Active Model Basics (form objects). https://guides.rubyonrails.org/active_model_basics.html
- Pundit README. https://github.com/varvet/pundit
- Sibling methodologies in this repo: `pro/dev/backend-enterprise/ruby-rails/`, `pro/dev/backend-enterprise/ruby-rails-patterns/`, `pro/dev/backend-enterprise/ruby-activerecord/`, `pro/dev/backend-enterprise/decomposition-laravel/`.
