# Agent Integration — Dev Methodologies: Practices

## When to use
- Greenfield service scaffolding: agent uses the language section as a template for project layout, imports, services, view/controller thinness.
- Refactor passes that align an existing module to a known-good shape (`thin views + services/`, `thin controllers + service objects`, `internal/cmd/pkg`).
- Producing CLAUDE.md / AGENTS.md / per-folder docs in the canonical 100-150 line shape — the doc skeleton at the bottom of `README.md` is the source of truth.
- Cross-language onboarding: agent must produce equivalent shape in two stacks (e.g., Django service + Spring service mirroring the same use case).

## When NOT to use
- Architecture-level decisions (microservices vs modular monolith, sync vs async, choice of DB) — see `dev-methodologies-architecture` and `software-architect` skill.
- Testing patterns — see sibling `dev-methodologies-testing`.
- Performance tuning, caching strategies, observability — out of scope here.
- When the project already has a documented house style that diverges from these examples (e.g., Django Ninja instead of DRF, or Rails service objects via `interactor` gem) — agent will overwrite it.

## Where it fails / limitations
- Reference is breadth-first: 40 patterns across 8+ languages but each only one snippet. Agents extrapolate confidently from one example and miss edge cases (e.g., Django `update_fields` requires the field list to match — easy to break with new columns).
- "Fat model / thin view" is asserted but not enforced — agents often re-create god services if the prompt isn't explicit about service granularity.
- The Next.js App Router section is pre-15; React 19 server actions / partial prerendering are not covered (see `best-practices-2026`).
- TypeScript Strict Mode block omits `exactOptionalPropertyTypes`, `noUncheckedIndexedAccess` defaults — agents copy as-is and miss modern strictness.
- Go example uses `interface where it's used` correctly, but the snippet still places the interface in the producer package — easy to mis-apply.
- Storybook snippet targets v7 CSF3; v8/v9 args + `tags: ['autodocs']` aren't shown.

## Agentic workflow
Treat this as a per-language *cheat sheet* the agent loads when the file's language is detected. For multi-stack work, dispatch one subagent per language so each one keeps a focused context. Always read the project's existing module of the same kind first (e.g., another Django app's `services/`) and have the agent imitate that, falling back to this reference only when the project has no precedent. Pair with a linter run (`ruff`, `eslint`, `golangci-lint`, `clippy`) as a hard gate.

### Recommended subagents
- `faion-sdd-executor-agent` — applies these patterns inside the SDD task loop.
- Language-specific worker subagents (no project-specific ones exist yet) — instantiate ad hoc with the relevant section preloaded.

### Prompt pattern
```
Apply the Django coding standards from
solo/dev/automation-tooling/dev-methodologies-practices/README.md (sections:
"Django Coding Standards", "Django Code Decision Tree") to apps/billing.
Constraints:
- moves DB-mutating logic into apps/billing/services/
- keeps views < 20 lines
- imports cross-app modules with module-level alias
- updates apps/billing/CLAUDE.md to the 100-150 line skeleton
Run `ruff check --fix apps/billing && pytest apps/billing -x`.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ruff` | Python lint + format (replaces black/isort/flake8) | `pip install ruff` · https://docs.astral.sh/ruff |
| `mypy` / `pyright` | Python type checking | `pip install mypy` / `npm i -g pyright` |
| `eslint` + `@typescript-eslint` | JS/TS lint | `npm i -D eslint @typescript-eslint/{parser,eslint-plugin}` |
| `prettier` | JS/TS/MD formatter | `npm i -D prettier` |
| `tsc --noEmit` | TS type-check gate | bundled with `typescript` |
| `golangci-lint` | Go meta-linter | https://golangci-lint.run |
| `clippy` + `cargo fmt` | Rust lint + format | `rustup component add clippy rustfmt` |
| `rubocop` / `standardrb` | Ruby lint | `gem install rubocop` |
| `phpstan` / `psalm` + `php-cs-fixer` | PHP static analysis + formatter | `composer require --dev phpstan/phpstan` |
| `dotnet format` + Roslyn analyzers | .NET style + analysis | bundled with .NET SDK |
| `pre-commit` | Run all of the above on commit | `pip install pre-commit` · https://pre-commit.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Actions | SaaS | Yes — first-class | Standard place to gate the linters above. |
| pre-commit.ci | SaaS | Yes | Hosted runs of the local `pre-commit` config; auto-PRs fixes. |
| SonarCloud / Sonar | SaaS / OSS | Yes — REST API | Tracks practice violations + duplications across stacks. |
| Code Climate Quality | SaaS | Partial | Engine maintenance lagging; consider Sonar instead. |
| Renovate / Dependabot | SaaS / OSS | Yes | Keep dep-management section honest (lockfiles always green). |
| Storybook (hosted via Chromatic) | SaaS | Yes — CLI + API | For the Storybook section; visual regression on top. |

## Templates & scripts
The `README.md` already inlines templates per language. The most reused agent-facing artifact is the CLAUDE.md skeleton — keep agents within these size limits:

```markdown
# {Folder Name}

{One-sentence description}

## Overview
{2-3 sentences}

## Structure
| Path | Purpose |
|------|---------|
| `file.py` | Description |

## Key Concepts
- **Concept**: explanation

## Entry Points
- `main.py` — primary entry

## Common Operations
### Operation 1
```bash
command
```

## Dependencies
- dep: purpose
```

Target 100-150 lines, hard cap 200. See `templates.md` for the full shape.

## Best practices
- Pin the dependency manager per language in the prompt: Python → `uv` (preferred 2026) or `poetry`; Node → `pnpm`; Ruby → `bundler`; Go → modules; Rust → `cargo`. Mixed managers in one repo break agent assumptions.
- Use module-level imports with alias for cross-app Django (`from apps.users import services as user_services`) — never `from apps.users.services import *`. Easier rename, no shadowing.
- Keep services as functions, not classes, unless they hold connection/cache state. A class around a single method is a code smell agents repeatedly produce.
- Forbid magic numbers / strings — promote to `constants.py` / `const.ts`. Agents copy literals across files; lint with `PLR2004` / `no-magic-numbers`.
- For Go, declare interfaces in the *consumer* package (Go's "accept interfaces, return structs" rule). The README's snippet contradicts this; correct the agent.
- TypeScript: use `import type { X }` for type-only imports — keeps bundle slim and matches the strict config block.
- Each public function gets a one-line docstring explaining *why*, not *what*. Agents default to restating the signature; reject and re-prompt.

## AI-agent gotchas
- Agent will silently rewrite imports across the file when fixing one — restrict edits with explicit line ranges or use the Edit tool.
- Django `save(update_fields=[...])` requires the list to match real columns; agent renaming a field forgets to update the list, leading to silent partial saves.
- Agent confuses Pydantic v1 vs v2 syntax (`@validator` vs `@field_validator`) inside FastAPI examples — always state the major version.
- Spring `@Autowired` field injection is shown but discouraged; agents replicate field injection. Force constructor injection in the prompt.
- Rust async section uses `reqwest`; agent imports `reqwest::blocking::Client` inside `#[tokio::main]` — compiles, but blocks the runtime. Catch in review.
- CLAUDE.md generation: agents consistently exceed the 200-line cap when summarising large folders; require word/line budget in the prompt.
- Human-in-loop checkpoint: any change to base models, shared interfaces, or DI registration must be reviewed — those are blast-radius changes.
- Mass-rename refactors (e.g., service-functions extraction) need a typecheck + test gate per file batch; otherwise the agent commits a half-migrated tree.

## References
- https://docs.djangoproject.com/en/5.0/misc/design-philosophies/ — Django philosophy
- https://www.cosmicpython.com/ — "Architecture Patterns with Python" (services pattern)
- https://google.github.io/styleguide/ — Google style guides (Python, TS, Java, Go)
- https://go.dev/doc/effective_go — Go idioms (interfaces consumer-side)
- https://rust-lang.github.io/api-guidelines/ — Rust API guidelines
- https://martinfowler.com/eaaCatalog/ — service / repository / DTO patterns
