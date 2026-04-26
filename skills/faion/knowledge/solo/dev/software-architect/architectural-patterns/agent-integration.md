# Agent Integration — Architectural Patterns (Clean / Hexagonal / Onion / DDD)

## When to use
- Domains with non-trivial business rules where the cost of leaking persistence/UI concerns into core logic will become technical debt within a year.
- Multi-interface systems (REST + CLI + scheduled jobs + worker) sharing the same domain — Hexagonal/Ports & Adapters keeps the core single-sourced.
- Long-lived enterprise apps where framework/database/infra are expected to change at least once during the product lifetime.
- Systems with heavy regulatory/audit needs — explicit domain layer makes invariants and policies easier to point at.
- Teams adopting DDD with clearly identifiable bounded contexts (per-context aggregate roots, ubiquitous language) — the patterns reinforce DDD.

## When NOT to use
- CRUD-y admin tools, internal scripts, scrapers — domain layer is empty, layering is overhead.
- Prototypes/MVPs where you intend to throw away V1 — premature layering slows ship.
- Microservices that are already small enough that the domain fits in 200 lines — apply the patterns at the *system* boundary instead.
- Languages/runtimes where the dependency-injection cost is high (Python/JS without DI containers can simulate it, but the boilerplate is real).

## Where it fails / limitations
- Boilerplate explosion: ports + adapters + DTOs + mappers can balloon the file count by 3-5x for thin domains.
- Anaemic Domain Model anti-pattern: teams generate entities with only getters/setters and put logic in services, which defeats Clean/Onion.
- Ports designed too coarse become god-interfaces; too fine become death-by-a-thousand-mocks.
- Cross-aggregate transactions are awkward — Saga or eventual consistency required, which agents skip.
- LLMs over-apply DDD vocabulary (Aggregate, Value Object, Repository) without the underlying analysis; produces well-named but shallow domains.

## Agentic workflow
Run a domain-modeler agent on requirements that drafts entities, value objects, and aggregate boundaries (with ubiquitous-language glossary). A second agent generates the layer scaffold (domain → application → infra/presentation) and the ports per use case. A third agent implements one use case end-to-end and verifies dependencies point inward via an architecture test (ArchUnit/Packwerk/dependency-cruiser/import-linter). Tests are written against the application layer with in-memory adapters, never against the framework.

### Recommended subagents
- `faion-brainstorm` — diverge over which pattern fits (Clean vs Hexagonal vs Onion vs simpler layered).
- `faion-sdd-execution` — produce per-use-case spec/design/test-plan with ports listed explicitly.
- `faion-feature-executor` — implement one vertical slice (use case + adapters + tests) at a time.
- `faion-improver` — periodic dependency-direction audit and anaemic-model sweep.

### Prompt pattern
```
INPUT: requirements <doc> and domain glossary.
TASK: Identify aggregates, entities, value objects. For each aggregate output:
- invariants (must always hold)
- commands (state-changing operations)
- queries (read-only, may bypass aggregate)
- repository port signature
Reject any "Manager"/"Service"/"Helper" naming; force domain-specific names.
```

```
ROLE: dependency-direction critic
TASK: Run an architecture test that fails if domain/ imports
infrastructure/ or presentation/. Output the violations with line numbers
and propose the minimal refactor (move method, extract interface, invert).
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| ArchUnit (Java/Kotlin) | Architecture rule tests | https://www.archunit.org/ |
| Packwerk (Ruby) | Modular monolith package boundaries | https://github.com/Shopify/packwerk |
| import-linter (Python) | Layer rules for Python imports | https://import-linter.readthedocs.io/ |
| dependency-cruiser (JS/TS) | Layer rules + visualization | https://github.com/sverweij/dependency-cruiser |
| go-arch-lint / arch-go | Go layer/package rules | https://github.com/fe3dback/go-arch-lint |
| ts-arch | TS architecture tests | https://github.com/ts-arch/ts-arch |
| madge | TS/JS circular-dep detection | `npm i -g madge` |
| context-mapper | DDD context maps as text | https://contextmapper.org/ |
| event-storming-tool / Miro plugins | Domain modeling | various |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub / GitLab | SaaS | Yes | Host architecture-test runs in CI |
| Backstage TechDocs | OSS | Yes | Document bounded contexts per service |
| Structurizr / LikeC4 | SaaS+OSS | Yes | Render Container/Component diagrams reflecting layers |
| Sourcegraph / Cody | SaaS | Yes | Cross-repo refactors when promoting domain across services |
| Miro / Mural | SaaS | Avoid for agents | Useful for human event storming; not a clean agent input |
| EventStorming.dev / Domo | Templates | Yes | Markdown-based event storms agents can ingest |

## Templates & scripts
See `templates.md` for code templates per pattern. Inline import-linter config to enforce Clean Architecture in Python:

```ini
# .importlinter
[importlinter]
root_package = app

[importlinter:contract:layers]
name = Clean Architecture layers
type = layers
layers =
    app.presentation
    app.infrastructure
    app.application
    app.domain

[importlinter:contract:domain-isolated]
name = Domain has no outward deps
type = forbidden
source_modules =
    app.domain
forbidden_modules =
    app.application
    app.infrastructure
    app.presentation
    django
    sqlalchemy
    fastapi
```

```bash
# Run in CI; fail build on violation.
pip install import-linter
lint-imports
```

## Best practices
- Use vertical slices: deliver one full use case (port → adapter → domain → test) before scaffolding more layers.
- Domain layer must depend on nothing application-level: no logging, no ORM, no clock — inject everything via ports.
- Repository ports return domain objects, not DTOs; keep mapping in adapters.
- Aggregates are transactional consistency boundaries; cross-aggregate updates use domain events + Saga, never multi-aggregate transactions.
- Test the application layer with in-memory adapters; integration tests cover real adapters separately. Most behavioral coverage stays fast.
- Document bounded contexts in a context map; avoid implicit shared kernel that becomes a god-package.
- Run architecture tests in CI on every PR; the patterns decay silently otherwise.

## AI-agent gotchas
- LLMs gravitate to anaemic models — entities with no behavior. Force a "behavior-on-entity" rule and reject service-only logic.
- Agents conflate Clean and Hexagonal terminology; pick one and stick with it per project to avoid mixed vocabulary in code.
- Mappers are commonly forgotten — domain entities leak into HTTP layer or get serialized with persistence ids. Require explicit DTOs at adapter boundaries.
- Cross-aggregate operations get implemented with direct repo calls; require an explicit Saga/process-manager step in the spec when use case spans aggregates.
- Human-in-loop gates: bounded-context boundary changes (rare, expensive), aggregate-boundary changes (data migrations), public port signature changes (consumer breakage).

## References
- "Clean Architecture" — Robert C. Martin (2017)
- https://alistair.cockburn.us/hexagonal-architecture/
- https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/
- "Domain-Driven Design" — Eric Evans (2003)
- "Implementing Domain-Driven Design" — Vaughn Vernon (2013)
- https://martinfowler.com/bliki/AnaemicDomainModel.html
- https://github.com/ddd-crew/ddd-starter-modelling-process
- https://contextmapper.org/
