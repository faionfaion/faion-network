# Agent Integration — Modular Monolith

## When to use
- Solo or small-team (≤10 dev) project that needs clean bounded contexts now and the option to extract microservices later.
- Refactoring a "big ball of mud" monolith into module packages with explicit public APIs and per-module schemas.
- Establishing import-boundary linting (import-linter, ArchUnit, depguard, Spring Modulith) as a CI gate.
- Designing schema-per-module separation in a single PostgreSQL/MySQL instance.
- Planning the strangler-fig extraction path: which module leaves first, and how the contract evolves.

## When NOT to use
- True microservices need (independent scaling per module, polyglot stacks, regulatory isolation, ≥10 teams) — go to `microservices-architecture` instead.
- Throwaway prototypes / scripts where module boundaries are noise.
- Existing well-structured monolith that already has clear packages and tests — don't add ceremony for its own sake.
- Distributed teams across timezones with no shared deploy cadence — modular monolith forces a single deploy train.

## Where it fails / limitations
- Agents create modules but skip enforcement — boundaries decay within weeks. Linter must be in CI from day one.
- LLMs invent "shared" / "common" modules that become god-objects; reject unless tightly scoped (DTOs, value objects only).
- Schema-per-module gets violated by ad-hoc cross-schema joins for "just one query" — agent code rarely flags this.
- Event-driven cross-module communication adds eventual consistency that agents don't account for in test plans.
- Migration to microservices: agents focus on code split but ignore data split (the harder half) and shared DB transactions.
- Tools differ wildly per language (Spring Modulith for Java, import-linter for Python, depguard for Go, custom for TS) — agent must know the project's stack.

## Where it fails / limitations (extra)
- Module = bounded context boundary requires real domain understanding; agents draw boundaries by current file structure, which is wrong.
- "Public API" stays public for years; agents add to it casually, creating coupling that's expensive to remove later.

## Agentic workflow
Sonnet for module-boundary design (requires domain reasoning), haiku for module scaffolding and linter config from `templates.md`, opus only when refactoring a large existing monolith. Pair with `architectural-patterns` (Clean/Hexagonal inside each module), `database-selection` (per-module schema/DB), and `event-driven-architecture` (when async events become the cross-module communication style). Output a module map (Mermaid), a public API per module, schema isolation, and the boundary-enforcement linter config — all four required.

### Recommended subagents
- `faion-sdd-executor-agent` — owns the multi-task SDD feature: scaffold modules, set up linter, migrate code, write boundary tests.
- `faion-feature-executor` — runs the sequential extraction tasks when migrating an existing monolith.
- `faion-improver` — captures common boundary violations as patterns/mistakes for future runs.

### Prompt pattern
```
Design modular monolith for <product> in <Python/Go/Java/TS>.
Domains: <list>. Team size: <n>. Database: <PostgreSQL>.
Output:
1) Module map (Mermaid), 2) public API per module (function/method signatures only),
3) schema isolation strategy, 4) boundary linter config (import-linter / ArchUnit / depguard),
5) cross-module communication pattern (sync calls vs events) per pairing.
Flag any module that should NOT exist as a module.
```

```
Migrate <existing monolith> to modular structure. Identify bounded contexts from these
business capabilities: <list>. Produce: target package layout, mechanical refactor plan
(per file moves), boundary linter rules, and 3 risks with mitigations.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `import-linter` | Python: enforce module independence and layered architecture | `pip install import-linter` |
| `pydeps` | Visualize Python import graph | `pip install pydeps` |
| `depguard` (golangci-lint) | Go: deny imports from internal packages | https://golangci-lint.run/ |
| `go list -m` / `goda` | Go: dependency graph analysis | `go install github.com/loov/goda@latest` |
| `archunit` | Java: architecture tests | https://www.archunit.org/ |
| `spring-modulith` | Spring Boot: verify module boundaries | https://spring.io/projects/spring-modulith |
| `dependency-cruiser` | TS/JS: enforce module rules | `npm i -D dependency-cruiser` |
| `madge` | TS/JS: circular dep detection | `npm i -g madge` |
| `pgcli` / `psql` | Inspect schema-per-module isolation | `pip install pgcli` |
| `mermaid-cli` | Render module maps to PNG/SVG for ADRs | `npm i -g @mermaid-js/mermaid-cli` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Spring Modulith | OSS | Yes | First-class modular monolith; verification + docs generation. |
| Backstage | OSS | Partial | Catalog + boundary docs; agent can author entity files. |
| Structurizr | SaaS+OSS | Yes | C4 model + module relationships in DSL; agent-friendly. |
| dbdiagram.io | SaaS | Partial | Per-module ERD; export DBML usable by agent. |
| Atlas (ariga) | OSS | Yes | Schema-as-code with per-module migrations. |
| Liquibase / Flyway | OSS | Yes | Per-module migration paths; agent generates changesets. |

## Templates & scripts
See `templates.md` for module structure (Python/Go/Java) and linter configs. Inline import-linter contract that enforces independence:

```ini
# .importlinter
[importlinter]
root_package = src

[importlinter:contract:modules-independent]
name = Modules must not import each other internals
type = independence
modules =
    src.users
    src.orders
    src.payments
    src.notifications

[importlinter:contract:public-api-only]
name = Cross-module access only via api.py
type = forbidden
source_modules =
    src.users
    src.orders
forbidden_modules =
    src.payments.domain
    src.payments.infrastructure
ignore_imports =
    src.payments.api -> *
```

## Best practices
- Module = bounded context. If you can't name a domain, it's not a module.
- Public API per module is one file (`api.py`, `api.go`, `api.ts`) — agent must funnel all cross-module calls through it.
- Schema-per-module from day one, even on shared DB instance; cross-schema joins forbidden by code review and runtime check.
- Sync direct calls are fine to start; introduce events only when cross-module concerns truly are async (notifications, audit, analytics).
- Linter as CI gate; without enforcement, modular monolith decays in 1-2 sprints.
- Module-level integration tests run in isolation (each module spins up only its own schema + dependencies stubbed).
- Document the extraction order in advance: which module leaves the monolith first, and what its public API will look like as a service.

## AI-agent gotchas
- Agent imports `from orders.models import Order` directly; review must reject cross-module model imports — DTOs only.
- "Shared kernel" temptation: agent puts entities in a `common/` module that everyone depends on; this turns the modular monolith back into a ball of mud.
- Cross-schema joins via raw SQL escape ORM-level lint; demand DB-side check (separate Postgres roles per schema with `REVOKE`).
- Spring Modulith verification only catches boundary violations at test time; agents skip writing the `ApplicationModules.of(App.class).verify()` test.
- Event-driven communication: agent uses in-memory event bus and forgets that it must be replaced with Kafka/RabbitMQ on extraction; mark this as TODO from day one.
- Migration to microservices: agent extracts the code but leaves shared DB transactions intact, creating tight runtime coupling. Always extract data with the service.
- Per-language tooling drift: agent suggests `import-linter` rules in a Go project. Always confirm stack first.
- "Internal" packages in Go: agents put modules at top-level; place each behind `internal/` to leverage compiler-enforced visibility.

## References
- Kamil Grzybek, "Modular Monolith: A Primer." https://www.kamilgrzybek.com/blog/posts/modular-monolith-primer
- Milan Jovanovic, "Modular Monolith Architecture." https://www.milanjovanovic.tech/modular-monolith-architecture
- Sam Newman, "Monolith to Microservices" (2019).
- Spring Modulith Reference — https://docs.spring.io/spring-modulith/reference/
- import-linter docs — https://import-linter.readthedocs.io/
- ArchUnit User Guide — https://www.archunit.org/userguide/html/000_Index.html
- "How Kraken Organizes Their Python Monolith" — https://blog.europython.eu/kraken-technologies-how-we-organize-our-very-large-pythonmonolith/
- Vertical Slice Architecture (Jimmy Bogard) — https://www.jimmybogard.com/vertical-slice-architecture/
