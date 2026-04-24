# Agent Integration — Laravel Decomposition Patterns

## When to use
- Greenfield Laravel project where you want LLM agents to extend the codebase without re-reading 500-line controllers.
- Refactoring legacy "fat controller / fat model" Laravel apps to Action + DTO + Resource style before letting agents touch them.
- Multi-developer or multi-agent setups where parallel work on the same domain (User, Order, Billing) must avoid merge collisions.
- Codebases where you ship feature flags often — small files swap behind a flag cleanly.
- Teams adopting SDD (`spec → design → impl-plan → tasks`): one task = one Action class is a clean unit of work.

## When NOT to use
- Tiny CRUD admin tools (<20 endpoints) — Action/DTO ceremony costs more than the readability gain.
- Prototype phase where the domain is unstable; locking shapes into DTOs slows discovery.
- Teams without PHP 8.1+ — readonly props and constructor promotion are load-bearing for the DTO pattern.
- Apps that already use an established pattern (e.g., pure Service-class style à la Spatie); mixing styles is worse than picking one.
- Hot paths where the indirection (Controller → Action → Service → Repository) measurably adds latency.

## Where it fails / limitations
- **DTO sprawl.** Every endpoint gets its own `CreateXDTO`, `UpdateXDTO`, `PatchXDTO`; agents create near-duplicates instead of reusing.
- **Action vs Service confusion.** The methodology recommends Actions for single-purpose ops, Services for orchestrations — agents ignore the rule and put logic anywhere.
- **Over-thin controllers.** Controllers reduced to 3 lines move all branching into Actions, making request-shape variations harder to read.
- **Form Request + DTO duplication.** Validation rules and DTO shapes diverge over time; agents add a field to one and forget the other.
- **Testing surface explodes.** N classes per feature → 4N tests; agents either skip tests or write paper-thin `assertTrue(true)` ones.
- **No enforcement.** Pattern is convention-only; without a linter, the next agent regresses to fat controllers within a sprint.
- **Overkill for read-heavy endpoints.** A 20-line `index()` does not need an Action; agents wrap it anyway.

## Agentic workflow
Treat each feature as a tree: `Controller → Action(s) → DTO + Service/Repo + Resource + Policy + Test`. Drive it with: (1) a planner subagent emits the file list and intended sizes (per the size table); (2) a code-writer subagent generates files in dependency order (DTO → Action → Controller → Resource); (3) a test subagent writes one Pest test per Action; (4) a structural-lint subagent fails the PR if any controller exceeds 150 lines or any Action exceeds 100. Persist the convention in `CONTRIBUTING.md` and load it as system prompt context for every agent run.

### Recommended subagents
- `faion-backend-agent` (referenced in README frontmatter) — implementer for Actions, DTOs, Resources.
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — one SDD task per Action; quality gate runs Pest + Pint + Larastan.
- A purpose-built **decomposition-lint-agent** (worth creating): walks `app/` and fails if `Http/Controllers/*` LOC > 150, `Models/*` LOC > 150, or `Actions/*` directory missing for a feature with >2 endpoints.
- `faion-feature-executor` (skill at `skills/faion-feature-executor/`) — sequences the Action breakdown across multiple SDD tasks.

### Prompt pattern
File-tree generation:
```
You are a Laravel 11 architect using the decomposition pattern in
decomposition-laravel/README.md. Given the spec <spec.md>, output the
exact list of files to create with target line ranges from the
"File Size Guidelines" table. One Action per use case. DTOs derive
fromRequest. Controllers ≤80 lines. Output as a markdown checklist;
no code yet.
```

Implementation pass:
```
For each file in <checklist>, generate code matching the patterns in
decomposition-laravel/README.md sections "Action Pattern", "DTO
Pattern", "Controller Pattern". Wrap multi-write Actions in
DB::transaction. Ship a Pest feature test alongside each Action.
Run: vendor/bin/pint && vendor/bin/pest --filter=<Feature>.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `php artisan make:action` (lorisleiva/laravel-actions) | Scaffold Action class | `composer require lorisleiva/laravel-actions` |
| `php artisan make:request` | Form Request scaffolding | bundled |
| `php artisan make:resource` | API Resource scaffolding | bundled |
| `php artisan make:policy` | Authorization policy | bundled |
| `laravel/pint` | PSR-12 + opinionated formatter, runs in pre-commit | `composer require laravel/pint --dev` |
| `nunomaduro/larastan` | Static analysis; catches DTO/property mismatches | `composer require nunomaduro/larastan --dev` |
| `pestphp/pest` | Test runner (one test file per Action) | `composer require pestphp/pest --dev` |
| `phploc` | Per-file LOC; gate PRs on size | `composer require phploc/phploc --dev` |
| `rector/rector` | Automated refactors (e.g., extract method → Action) | `composer require rector/rector --dev` |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Spatie Laravel-Data | OSS | yes | Drop-in DTO library; replaces hand-rolled `fromRequest`. Reduces boilerplate agents otherwise duplicate. |
| Lorisleiva Laravel-Actions | OSS | yes | Action-as-Controller pattern; first-class `__invoke` support. |
| Laravel Pulse | First-party APM | yes | Per-Action latency surfaces decomposition cost. |
| GitHub Actions / GitLab CI | CI | yes | Run Pint + Larastan + Pest as pre-merge gate. |
| Laravel Forge | SaaS deploy | API yes | Atomic deploy of decomposed apps. |
| SonarCloud | SaaS quality | API yes | Code smells, duplicated DTOs, complexity per Action. |
| GitHub Copilot / Claude in editor | IDE | yes | Pattern is well-suited to inline file generation. |

## Templates & scripts
The methodology already ships file-tree templates in `templates.md`. Add a structural lint (≤50 lines):

```bash
#!/usr/bin/env bash
# decomp-lint.sh — fail if Laravel decomposition convention is broken.
# Usage: decomp-lint.sh app/
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
check "*/Http/Controllers/*.php" 150 "Controller"
check "*/Models/*.php"            150 "Model"
check "*/Actions/*/*.php"         100 "Action"
check "*/Services/*/*.php"        200 "Service"
check "*/DTOs/*/*.php"             40 "DTO"
check "*/Http/Resources/*.php"    100 "Resource"
features=$(ls -d "$ROOT"/Http/Controllers/Api/* 2>/dev/null | wc -l)
actions=$(ls -d "$ROOT"/Actions/* 2>/dev/null | wc -l)
if [ "$features" -gt 0 ] && [ "$actions" -eq 0 ]; then
  echo "FAIL: API controllers exist but app/Actions/ is empty"
  fail=1
fi
exit "$fail"
```

Wire into `.husky/pre-commit` or GitHub Actions `quality` step.

## Best practices
- **One Action = one verb.** `CreateUserAction`, not `UserAction::create()`. Names map cleanly to SDD tasks.
- **DTO `fromRequest` is the single source of truth.** Never reach into `$request->input()` from inside an Action — it couples the Action to HTTP.
- **Resources never call relations.** `$this->relation` inside a Resource is an N+1 trigger; eager-load in the Action and assert presence with `whenLoaded`.
- **Action returns a domain object.** Not an array, not a Resource. The Controller wraps in a Resource; the Action is reusable from queue jobs and console commands.
- **Use Form Request for validation, DTO for transport.** Don't validate inside the DTO — Form Requests integrate with Laravel's auth and locale.
- **No Actions calling Actions in the same request.** That's a Service. Multi-Action orchestrations live one layer up; otherwise transactions span unclear boundaries.
- **Keep Policies in `app/Policies/`, not in Actions.** Authorize at the Controller boundary. Actions assume authorization already passed.
- **Tag each generated file with the spec ID** (e.g., `// @sdd FEAT-007`). Lets agents trace files back to specs during refactor.
- **Lint-as-you-go.** Run Pint + Larastan + the structural lint in the same pre-commit so the next agent inherits a clean tree.

## AI-agent gotchas
- **Pattern collapse under deadline pressure.** When asked to "just add an endpoint quickly," agents skip the Action layer and put logic in the controller. Lock the convention in `CONTRIBUTING.md` and reference it in every system prompt.
- **DTO drift.** Two agents add the same field to `CreateUserDTO` and `User::$fillable` with different names (`first_name` vs `firstName`). Enforce snake_case in DB, camelCase in DTOs only if you have a mapper layer.
- **Resource leaks soft-deleted/hidden fields.** Agent generates Resource with `$this->all()` instead of explicit field list. Never use `all()`, `toArray()`, or spread operators in Resources.
- **Action doing two things.** "CreateUserAction" also sends an email and assigns a role. Acceptable if wrapped in a transaction with intent; not acceptable if email failure rolls back the user. Force agents to declare side-effects in the docblock.
- **Test-per-Action explosion ignored.** Agents skip tests for Actions assuming the Controller test covers them. The Controller test does NOT cover Action edge-cases. Require `actions/*/*.php` ↔ `tests/Feature/Actions/*/*.php` parity.
- **Form Request bypass.** Agents call Action directly from a console command without re-validating; invariants the Form Request enforced are now skipped. Move invariant checks into the Action's first 3 lines.
- **Agents invent new layers.** "Manager", "Coordinator", "Handler" classes appear after a refactor. Whitelist allowed namespaces (`Actions`, `Services`, `Repositories`, `DTOs`, `Policies`) and block PRs introducing new ones without an ADR.
- **Decomposition without DI.** Agents `new CreateUserAction()` inside the controller. Use constructor injection so tests can mock; otherwise the pattern's testability gain evaporates.
- **Repository confusion.** Pattern includes a Repository layer optionally; agents add it everywhere "for consistency". Either adopt repos for all aggregates or for none — partial adoption is the worst case.
- **Action returns void.** Agents emit `public function execute(): void` and mutate state; downstream agents can't compose. Always return the canonical entity or a result object.

## References
- Lorisleiva — "Laravel Actions" docs. https://laravelactions.com
- Spatie — "Laravel Data" docs (DTOs). https://spatie.be/docs/laravel-data
- Freek Van der Herten — "Don't write services, write actions." https://freek.dev/2218
- Stitcher.io — "Laravel beyond CRUD" series (decomposition patterns). https://stitcher.io/blog
- Laravel docs — API Resources. https://laravel.com/docs/eloquent-resources
- Laravel docs — Form Requests. https://laravel.com/docs/validation#form-request-validation
- Sibling methodologies in this repo: `pro/dev/backend-enterprise/php-laravel/`, `pro/dev/backend-enterprise/php-eloquent/`, `pro/dev/backend-enterprise/php-laravel-patterns/`, `pro/dev/backend-enterprise/decomposition-rails/`.
