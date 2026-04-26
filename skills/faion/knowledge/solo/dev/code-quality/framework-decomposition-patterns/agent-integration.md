# Agent Integration — Framework Decomposition Patterns

## When to use
- Refactoring fat controllers / God models in Django, Rails, Laravel before any LLM-assisted feature work.
- Preparing a legacy codebase for AI agents: cap files at 150-200 lines so a single Read fits in context.
- Onboarding Claude Code to a framework codebase — service layer + selectors keeps prompt tokens predictable.
- Building a new module: pick the right extraction (services, actions, query objects, hooks) before writing.

## When NOT to use
- Tiny scripts, one-off Lambdas, or files already under 100 lines — decomposition adds ceremony without benefit.
- Prototypes still being thrown away weekly (YAGNI).
- Frameworks with strong opinionated structure already enforcing this (Phoenix contexts, NestJS modules) — follow framework idioms instead.
- Microservices where one service = one concern; extra layers duplicate boundaries.

## Where it fails / limitations
- Service-layer overkill: developers create `UserService.get_user_by_id()` that just wraps `User.objects.get()`. Wrappers without behavior are noise.
- DTO explosion in dynamic languages — Python/Ruby teams often skip DTOs, then service signatures drift.
- React custom hooks are easy to over-extract; a hook used once in one component should stay inline.
- Rails service objects fight the framework if used for trivial CRUD; use them for multi-step business actions only.
- Cross-aggregate transactions become harder when selectors hide the ORM session — agents may not see lock semantics.

## Agentic workflow
Drive decomposition with a refactor agent that reads one fat file, proposes a split into services/selectors/DTOs, writes the new files, then updates call sites. Keep each step a separate commit so a reviewer (or `faion-sdd-executor-agent`) can roll back the boundary that broke. Pair with a test-runner agent: run the test suite after every move; if green, continue; if red, revert and re-plan. Use the framework-specific decomposition file (`decomposition-django.md`, etc.) as the prompt scaffold.

### Recommended subagents
- `faion-sdd-executor-agent` — runs the refactor as an SDD task with quality gates (tests, lint) between extractions.
- `nero-sdd-executor-agent` — same role for NERO repos; uses NERO conventions for Django service layouts.

### Prompt pattern
```
Read knowledge/solo/dev/code-quality/framework-decomposition-patterns/decomposition-django.md.
Target: <app>/views.py (LOC=420). Goal: extract Selectors + Service Layer.
Step 1: list every business operation in the file (verbs).
Step 2: propose new file tree (services.py, selectors.py) with function signatures.
Step 3: write files + update views.py imports. One commit per extraction.
Run pytest after each commit. If red, revert that commit and explain.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `radon` | Python cyclomatic complexity / LOC per file | `pip install radon`; `radon cc -s app/` |
| `lizard` | Multi-language complexity & file-length metrics | `pip install lizard`; `lizard --CCN 10 -L 200` |
| `eslint-plugin-boundaries` | Enforce module boundaries in JS/TS | `npm i -D eslint-plugin-boundaries` |
| `tokei` | LOC counts per file/lang for triage | `cargo install tokei` |
| `rubocop -r rubocop-rails` | Rails rules incl. `Metrics/ClassLength` | `gem install rubocop-rails` |
| `phpstan` / `larastan` | Laravel static analysis to surface fat classes | `composer require --dev larastan/larastan` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| SonarCloud / SonarQube | SaaS + OSS | Yes — REST API for issues | Reports `cognitive_complexity`, `ncloc` per file. |
| CodeClimate Quality | SaaS | Yes — JSON reports + GH checks | Surfaces "God classes". |
| Codacy | SaaS | Partial | Less granular than Sonar. |
| Qodana (JetBrains) | SaaS + OSS | Yes — CLI + JSON output | Strong for Rails/Laravel. |
| GitHub Code Scanning | SaaS | Yes — SARIF feed | Drive agent triage from SARIF. |

## Templates & scripts
See `templates.md` and the four `decomposition-<framework>.md` files for full per-framework skeletons. Use this one-liner to find decomposition candidates:

```bash
# Top 20 longest application files (Python example)
git ls-files '*.py' | grep -Ev 'tests?/|migrations/' \
  | xargs wc -l 2>/dev/null | sort -rn | head -20
```

```javascript
// React: list components > 150 LOC for hook extraction
// node scripts/find-fat-components.mjs
import { readFileSync } from 'node:fs';
import { globSync } from 'glob';
for (const f of globSync('src/**/*.{tsx,jsx}')) {
  const loc = readFileSync(f, 'utf8').split('\n').length;
  if (loc > 150) console.log(loc, f);
}
```

## Best practices
- One commit per extraction; never combine "extract service" + "rename" in one diff — agents lose blame trail.
- Keep a `selectors.py` pure (no writes, no side effects). Services own writes; selectors own reads. Lets an agent reason about cache invalidation.
- Forbid cross-imports between sibling apps' services — define a `shared/` package or a domain event bus.
- DTOs: pydantic v2 / dataclasses / Laravel form requests / TS interfaces. Make them the contract the LLM reads first.
- React: lift hooks only when reused or > 30 LOC of stateful logic. Don't split JSX into 3-line components.
- Rails service objects: return `Result.success(value)` / `Result.failure(error)` not exceptions — agents handle Result types reliably.

## AI-agent gotchas
- Auto-decomposition agents will create empty wrapper classes if you don't give them an LOC threshold and a "must contain logic" rule.
- LLMs over-DRY: they extract the wrong common base when two services accidentally share field names. Require the agent to first write tests, then extract only behavior covered by green tests.
- After decomposition, agents often forget to update `__init__.py` / `index.ts` re-exports — make a final "rebuild barrel" step explicit.
- Selectors with N+1 queries: tell the agent to add `select_related` / `prefetch_related` in the same commit and run a query-count assertion test.
- Human-in-loop checkpoint: review the proposed file tree (Step 2 in the prompt) BEFORE Step 3 writes files. Reverting 12 new files is expensive.

## References
- "Django Styleguide" by HackSoft — service layer + selectors origin: https://github.com/HackSoftware/Django-Styleguide
- "Rails Service Objects" — https://www.toptal.com/ruby-on-rails/rails-service-objects-tutorial
- "Laravel Actions" by Loris Leiva — https://laravelactions.com/
- "Refactoring UI Components" — Kent C. Dodds blog on hook extraction.
- Sibling files: `decomposition-django.md`, `decomposition-rails.md`, `decomposition-laravel.md`, `decomposition-react.md`.
