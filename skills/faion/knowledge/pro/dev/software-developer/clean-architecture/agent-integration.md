# Agent Integration — Clean Architecture

## When to use
- Long-lived enterprise codebases where infrastructure (DB, message bus, auth provider, payment processor) is expected to change at least once over the product lifetime.
- Domains with non-trivial business rules — pricing engines, eligibility checks, regulatory calculations — that deserve to be tested without booting the framework.
- Polyglot persistence: same domain logic must be servable from REST, GraphQL, gRPC, and a CLI without duplication.
- Greenfield builds where the team has DDD literacy and is committed to dependency-inversion as a hard rule.
- Existing Big Ball of Mud where you want a strangler-fig migration: extract a use case at a time into a clean core.

## When NOT to use
- CRUD apps with thin business logic (form → table). Three layers of indirection over a `User` table is pure tax.
- Solo MVP / pre-PMF: the cost (entities + interfaces + use cases + DTOs + adapters) buys nothing while the domain is unstable.
- Throwaway scripts, batch jobs, glue code. Use the framework directly.
- Teams without DDD/inversion experience — Clean Architecture without aggregate boundaries collapses into "DTOs all the way down" with extra mappers.
- Tight latency budgets where every layer's mapping costs measurable µs (HFT, real-time bidding). Direct paths win.
- Frameworks designed against the dependency rule (Rails, Django) where fighting the framework costs more than it saves; modular monolith inside the framework is often the better answer.

## Where it fails / limitations
- **Mapper sprawl.** Every layer translates DTO → entity → ORM model. Without discipline, you get N×M mapping classes; reviews grind.
- **Anaemic domain.** Entities become record-like, all behavior leaks into use cases. Then "use case" is just a "service" by another name.
- **Use-case explosion.** One use case per endpoint × CRUD verbs × resources = hundreds of classes. Without grouping, navigation suffers.
- **Repository misuse.** Repos morph into query factories with `findByXAndYOrderByZ`; the abstraction leaks ORM semantics. README's `interfaces/` shows the intent but doesn't prevent drift.
- **Premature abstraction.** Interfaces for things with one impl forever (a single Postgres). Extra layer with zero option value.
- **Slow tests.** Each use case test sets up entities + repos + UoW + event publisher mocks. Without test fixtures, suite balloons.
- **Cross-cutting concerns.** Logging, tracing, audit, retry — get scattered. Decorators help but require a consistent style.
- **Framework-lock through the back door.** Validation, serialization, auth tied to the web framework leak into use cases via DTOs that are actually request/response models.
- **Async / transaction boundary confusion.** UoW per use case is fine; emitting a domain event mid-transaction and then the event handler tries to commit again — deadlock or lost event.

## Agentic workflow
Drive Clean Architecture as a four-stage pipeline: (1) a domain agent extracts entities, value objects, aggregates, domain events, and domain-service interfaces from the spec — never naming a framework or DB; (2) a use-case agent emits one use case per command/query, each with explicit input DTO, output DTO, and dependency interfaces; (3) an adapter agent implements the interfaces (repository over the chosen ORM, message bus over the chosen broker, web controllers over the chosen framework); (4) a review agent runs the dependency-rule checklist (no domain → infra import, no use case → framework import, no entity → ORM import, no DTO leaking entity, no async-IO inside an entity). Persist the bounded context + use-case map in `.aidocs/product_docs/clean-architecture-map.md` so subsequent feature work appends without re-deriving boundaries. Pair with `pro/dev/code-quality/domain-driven-design/`, `pro/dev/code-quality/cqrs-pattern/`, and `pro/dev/code-quality/event-sourcing-implementation/`.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — one task = one use case (input DTO + interactor + output DTO + tests + adapter wiring). Opus for non-trivial domain modeling; sonnet for routine adapter implementations.
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — adapters touch DB URLs, API keys, broker creds; scrub configs and fixtures pre-commit.
- A **dependency-rule-review-agent** (worth adding under `agents/`): linter that fails the build if `domain/` imports from `infrastructure/`, `application/`, or any framework package; if `application/` imports a framework package; if entities call `await` on IO.
- `faion-feature-executor` skill — sequential mode keeps domain → use case → adapter → controller ordering correct; out-of-order writing produces interactors against not-yet-written entities and cycles in imports.

### Prompt pattern
Inventory pass:
```
You are a Clean Architecture designer. Given the spec in <spec>, output:
(a) Entities: name, identity, invariants (state transitions allowed).
(b) Value objects: name, type, validation rules.
(c) Aggregates: which entities, root, transactional boundary.
(d) Domain events: name, payload (intent + minimal facts).
(e) Use cases: name, kind (command|query), input DTO, output DTO,
    dependencies (interfaces only — no concrete classes), errors.
Do not mention any framework, ORM, or database. Reject any entity
with an `id` of type AutoField/SQLAlchemy.Column/etc.
```

Dependency-rule review:
```
You are reviewing a Clean Architecture PR. Flag:
(1) `from infrastructure...` import inside domain/ or application/,
(2) `from <framework>...` import inside domain/ or application/,
(3) ORM model class used as the public type of a repository method,
(4) entity method calling await/IO,
(5) DTO that exposes ORM relationships (e.g., `user.orders` lazy load),
(6) use case directly importing a concrete adapter class,
(7) `infrastructure/` exporting domain entities (must be the other way),
(8) interface defined in `infrastructure/` instead of the consumer layer.
Cite file:line. No fixes — only flags.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `import-linter` (Python) | Enforce layer/forbidden-import rules in CI | https://import-linter.readthedocs.io |
| `pydeps` / `grimp` | Visualise import graph; find cycles | https://github.com/thebjorn/pydeps |
| `madge` (JS/TS) | Dependency graph + cycles for layered TS/JS | https://github.com/pahen/madge |
| `dependency-cruiser` (JS/TS) | Layer rules in `.dependency-cruiser.js` | https://github.com/sverweij/dependency-cruiser |
| `archunit` / `archunit-junit5` (Java) | Layer rules as JUnit tests | https://www.archunit.org |
| `nDepend` / `ArchUnitNET` (.NET) | Architecture tests | https://ndepend.com / https://archunitnet.readthedocs.io |
| `golangci-lint` + `depguard` (Go) | Forbid imports across packages | https://github.com/OpenPeeDeeP/depguard |
| `errcheck` / `mockgen` (Go) | Generate adapter mocks against interfaces | https://github.com/golang/mock |
| `mockall` (Rust) | Trait-based mocks for adapter interfaces | https://docs.rs/mockall |
| `pact` | Consumer-driven contract tests across adapter boundaries | https://docs.pact.io |
| `pytest` + `pytest-asyncio` | Run use-case tests without a web framework | https://docs.pytest.org |
| `mutmut` / `mutation-testing` | Catch under-tested domain branches | https://mutmut.readthedocs.io |
| `cookiecutter` / `copier` templates | Scaffolding templates for layered projects | https://www.cookiecutter.io |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| SonarCloud / SonarQube | SaaS / OSS | yes | Architecture rules + code-smell detection at PR time. |
| CodeScene | SaaS | yes | Visualises hotspots; finds where the domain rots fastest. |
| Backstage | OSS | yes | Service catalog + TechDocs; agents read the layer convention there. |
| Mermaid / Structurizr / IcePanel | SaaS / OSS | yes | C4 diagrams for the layer + adapter map. |
| dbdiagram.io / dbml-cli | SaaS / OSS | yes | Persist DB schema separate from domain entities. |
| Conftest / OPA | OSS | yes | Policy-as-code for "no infra import in domain" via Rego. |
| Renovate / Dependabot | SaaS | yes | Confines framework upgrades to adapter layer; agents review PRs. |
| Pact Broker | OSS / SaaS | yes | Tracks adapter contracts between services. |

## Templates & scripts
README ships full Python layered structure + entity/use case/repository samples; `templates.md` + `examples.md` cover Go/Java/TS variants. Add an `import-linter` `setup.cfg` block:

```ini
# setup.cfg or pyproject.toml [tool.importlinter]
[importlinter]
root_packages = src

[importlinter:contract:layers]
name = Clean Architecture layers
type = layers
layers =
    src.infrastructure
    src.application
    src.domain
ignore_imports =
    src.infrastructure.config -> src.application.interfaces

[importlinter:contract:no-framework-in-core]
name = No framework in domain or application
type = forbidden
source_modules = src.domain, src.application
forbidden_modules = fastapi, sqlalchemy, django, flask, tornado, aiohttp
```

Inline dependency-rule grep:

```bash
#!/usr/bin/env bash
# clean-arch-lint.sh — flag dependency-rule violations
set -euo pipefail
src="${1:-src}"
fail=0
echo "## Domain importing infra"
grep -rEn '^from src\.infrastructure' "$src/domain" && fail=1 || true
echo "## Domain importing application"
grep -rEn '^from src\.application' "$src/domain" && fail=1 || true
echo "## Application importing infra"
grep -rEn '^from src\.infrastructure' "$src/application" && fail=1 || true
echo "## Domain or application importing a web framework"
grep -rEn '^(from|import) (fastapi|django|flask|sqlalchemy|tortoise|peewee|sanic|aiohttp)' "$src/domain" "$src/application" && fail=1 || true
echo "## Entity calling await (IO inside domain)"
grep -rEn '^\s*await ' "$src/domain" && fail=1 || true
exit "$fail"
```

## Best practices
- **The dependency rule is the only rule.** Everything else is preference. CI enforces it; PRs don't argue about it.
- **Define interfaces at the consumer layer.** `application/interfaces/` declares what use cases need; `infrastructure/` implements. README places repository interfaces in `domain/interfaces/`; both are valid — pick one and stick with it.
- **Entities own behavior.** State transitions, invariants, and domain events fire from entity methods. If your entity is a `@dataclass` with no methods, it's a record, not an entity.
- **Use cases are thin orchestrators.** Fetch via repo, call entity behavior, persist, publish events. No conditionals on infrastructure concerns.
- **DTOs at every boundary.** Input DTO → entity (in adapter / use case input mapping) → output DTO. Never serialize an entity directly.
- **Unit of Work owns the transaction.** Use case opens UoW, mutates, commits. Don't sprinkle `session.commit()` in repositories.
- **Domain events are sync within UoW, async after commit.** Collect events on entities, dispatch after `commit()`. The README's `event_publisher` interface is the right shape.
- **Test the domain pure.** Domain tests run without a DB, web framework, or message bus. If you need them, the boundary is wrong.
- **Adapters are dumb.** A repository implementation is a translator between the persistence model and the domain model. Business logic in the repo is a smell.
- **Migrations live with the adapter.** ORM/DB migrations are infra. Domain models do not own schema concerns.
- **Don't make every interface plural.** One DB? One `UserRepository` impl. The interface still has option value (test fakes), but skip elaborate factory hierarchies.
- **Pick exception or Result and stick.** Either domain raises typed exceptions or returns `Result[T, E]`. Mixing both forces the caller to handle two error paths.

## AI-agent gotchas
- **Domain importing the ORM.** Agents put `Column`, `relationship`, `BaseModel` on the entity for "convenience." Reject in CI; the entity is a plain class.
- **Use case as glue, not orchestrator.** Agents emit a use case that just calls `repo.save(dto)` with no behavior. That's a controller. Force at least one entity-method call inside.
- **DTO leaking ORM relationships.** Agents return the SQLAlchemy model with `.orders`; lazy-load in the serializer. Pin DTOs to dataclasses/Pydantic with no relations.
- **Anaemic entities.** Agents create entities with only properties + setters. Force one behavior method per entity in the spec.
- **Forgotten event dispatch.** Agents collect events on the aggregate but never publish. Force the use case to call `event_publisher.publish_all(aggregate.pull_events())` after `uow.commit()`.
- **Framework decorators on entities.** Agents stamp `@app.exception_handler` or `@router.post` near entity classes by mistake. Lint imports.
- **Async IO inside a method named after business rule.** `Order.calculate_total()` becomes `async` because the agent reaches for the price service. Force a domain service interface or pass the price as input.
- **Mapper drift.** Agents create a new mapper per endpoint; force one mapper per (entity, layer-pair).
- **Repository as query DSL.** Agents add `find_by_X_and_Y_or_Z(...)`; cap at 4 query methods per repo, push complex reads to a CQRS read model.
- **Hallucinated UoW APIs.** Agents invent `uow.session.execute(...)` patterns that bleed ORM semantics. Pin to `uow.users`, `uow.orders`, `uow.commit()`.
- **Tests that boot the framework.** Agents use `TestClient(app)` for use case tests; force pytest-only tests against the use case constructor with fakes.
- **Human-in-loop on entity invariant changes.** Renaming/removing entity fields or invariants ripple to events, projections, and adapters. Don't auto-merge.

## References
- Martin, R. C. "Clean Architecture: A Craftsman's Guide to Software Structure and Design." Prentice Hall, 2017.
- Martin, R. C. "The Clean Architecture." (blog). https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html
- Cockburn, A. "Hexagonal Architecture (Ports & Adapters)." https://alistair.cockburn.us/hexagonal-architecture/
- Vernon, V. "Implementing Domain-Driven Design." Addison-Wesley, 2013.
- Evans, E. "Domain-Driven Design." Addison-Wesley, 2003.
- Percival, H. & Gregory, B. "Architecture Patterns with Python." https://www.cosmicpython.com
- Khononov, V. "Learning Domain-Driven Design." O'Reilly, 2021.
- "Onion Architecture" — Jeffrey Palermo. https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/
- ArchUnit project. https://www.archunit.org
- Sibling methodologies in this repo: `pro/dev/software-developer/microservices-design/`, `pro/dev/software-developer/java-spring-boot/`, `pro/dev/code-quality/domain-driven-design/`, `pro/dev/code-quality/cqrs-pattern/`, `pro/dev/code-quality/event-sourcing-basics/`, `pro/dev/code-quality/event-sourcing-implementation/`.
