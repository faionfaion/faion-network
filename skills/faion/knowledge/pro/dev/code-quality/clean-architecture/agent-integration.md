# Agent Integration — Clean Architecture

## When to use
- Long-lived application (≥3 years) where business rules outlive frameworks (Django → FastAPI, REST → gRPC).
- Complex domain with non-trivial invariants — entity behavior is worth isolating from I/O.
- Multiple delivery mechanisms (HTTP API + CLI + scheduled job + worker) need to share business logic.
- Strong testability requirement — want to test use cases without spinning up a DB or web server.
- Team practices DDD or plans to; clean architecture is the lower-floor structure DDD lives on.
- Replacement of a third-party dependency (payment gateway, search backend) is foreseeable; ports/adapters preempt the rewrite.

## When NOT to use
- CRUD prototype, MVP, or one-off tool — the indirection overhead exceeds the benefit at this size.
- Heavily framework-coupled stack (Rails, Django admin, Phoenix LiveView) where idiomatic code already organizes concerns.
- Team is unfamiliar with the pattern and there's no senior to enforce the dependency rule — you'll get fake clean architecture (entities importing the ORM).
- Performance-critical hot path where mapping DTO ⇄ entity ⇄ ORM model adds measurable latency.
- The "domain" is a thin facade over external APIs — there's no business logic to protect; you're writing an integration layer.

## Where it fails / limitations
- **Anemic domain model.** Entities become data bags; logic leaks into use cases; "clean" architecture without rich entities = hexagonal CRUD with extra files.
- **Mapper explosion.** DTO ↔ entity ↔ ORM model = three shapes of the same thing; agents (and humans) drift them out of sync.
- **Dependency rule violations slip in silently.** Someone imports `infrastructure.email_client` from a use case "just for now"; six months later half the codebase imports inward-out.
- **Framework leakage in entities.** SQLAlchemy declarative classes get used as entities; once an entity inherits `Base`, you've lost the abstraction.
- **Use case sprawl.** Every endpoint becomes a single-line use case (`get_user`, `update_user_email`, `update_user_name`). The cost is high; the value is low for trivial operations.
- **Async/sync impedance.** Use cases written sync, infra written async (or vice versa); adapter layer becomes thread-pool soup.
- **Repository over-abstraction.** Repository interfaces leak query patterns ("find_users_active_in_last_30_days_with_subscription") that are clearly DB-shaped.
- **Test theater.** Tests mock the repository, assert the mock was called, and verify nothing about the real DB schema or query plan.

## Agentic workflow
Drive clean architecture as a four-pass pipeline: (1) a domain-modeling agent extracts entities, value objects, and domain events from the spec — emits `domain/` skeleton with no framework imports; (2) a use-case agent generates one use case per business operation in `application/use_cases/`, each taking a `UnitOfWork` port and returning a DTO; (3) an adapter agent generates `infrastructure/` repository implementations, ORM models, and DI wiring, plus `presentation/` controllers; (4) a dependency-rule auditor verifies that no import in `domain/` or `application/` references `infrastructure/`, `presentation/`, or any framework. The auditor is the load-bearing pass — generated code that compiles can still violate the architecture.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — implement use cases as SDD tasks; quality gate: every use case has a unit test that runs without the DB or HTTP framework.
- A purpose-built **dependency-rule auditor** (worth creating): walks AST imports per layer; fails CI if `domain/` imports anything from `infrastructure/` / `presentation/` / external packages other than stdlib + value-object libs.
- A purpose-built **anemic-model detector** (worth creating): per entity class, count methods vs. fields; warn when methods < 2 and fields > 4 ("data bag smell").
- `password-scrubber-agent` — DTOs leak credentials (token fields, password hashes); scrub before logging.

### Prompt pattern
Layer scaffolding:
```
Given the spec in <spec>, generate a clean-architecture skeleton:
- domain/entities/<name>.py with rich behavior (no ORM imports)
- domain/value_objects/<vo>.py (frozen dataclasses, validation in __post_init__)
- domain/interfaces/<repo>.py (ABC, async methods)
- application/use_cases/<verb>_<noun>.py with execute() taking input DTO
  and returning output DTO
- application/dto/ for request/response shapes
Reject any file that imports sqlalchemy, fastapi, or pydantic from
domain/ or application/.
```

Dependency audit:
```
Scan src/. For each .py file under domain/ and application/, list its
imports. Flag any import whose module path starts with infrastructure.
or presentation. or matches the banned set: sqlalchemy, fastapi, redis,
boto3, requests, httpx. Output a markdown report grouped by file.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `import-linter` | Enforce layered import contracts in Python via config file | https://import-linter.readthedocs.io |
| `archunit` (Java) / `archunitnet` / `ts-arch` | Architecture rule tests for JVM / .NET / TypeScript | https://www.archunit.org |
| `dep-tree` | Visualize file-level dependency graph; spot inward-rule violations | https://github.com/gabotechs/dep-tree |
| `madge` (JS/TS) | Detect circular deps and visualize layers | https://github.com/pahen/madge |
| `pydeps` | Generate Python module dependency graphs | https://github.com/thebjorn/pydeps |
| `ruff` (Python) | `--select TID` (banned-imports) prevents framework imports in domain | https://docs.astral.sh/ruff/ |
| `eslint-plugin-boundaries` | Layer rules for JS/TS projects | https://github.com/javierbrea/eslint-plugin-boundaries |
| `pytest` + `pytest-asyncio` | Unit-test use cases with fake repositories | https://docs.pytest.org |
| `claude` (Anthropic CLI) | Run scaffolding + audit passes headless | https://docs.anthropic.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Actions / GitLab CI | SaaS / SaaS | yes | Run `import-linter` on every PR; failing layer rules block merge. |
| SonarQube / SonarCloud | SaaS / OSS | API yes | Architecture metrics; can flag cyclic deps and god-objects. |
| Structure101 / NDepend | SaaS | partial | Architectural debt visualization; expensive but useful in large codebases. |
| Snyk / FOSSA | SaaS | yes | License + vulnerability checks per layer dependency. |
| Backstage TechDocs | OSS | yes | Document layer responsibilities per service in a service catalog. |
| Cursor / Continue / Aider | dev tools | yes | Code-edit agents; pair with `import-linter` to keep generated code in bounds. |
| Renovate / Dependabot | SaaS | yes | Keep adapters' frameworks current; the *point* of clean architecture is being able to upgrade them. |

## Templates & scripts
The README ships layer / project / entity examples. The high-leverage missing piece is an `import-linter` config that mechanically enforces the dependency rule. Inline drop-in (≤50 lines):

```ini
# .importlinter — fail CI on layer-rule violations.
# Run: lint-imports
[importlinter]
root_packages =
    domain
    application
    infrastructure
    presentation

[importlinter:contract:layered]
name = Clean architecture: dependencies point inward only
type = layers
layers =
    presentation
    infrastructure
    application
    domain

[importlinter:contract:no-frameworks-in-domain]
name = Domain has no framework imports
type = forbidden
source_modules =
    domain
forbidden_modules =
    sqlalchemy
    fastapi
    starlette
    pydantic
    httpx
    requests
    redis
    boto3
    django
    flask

[importlinter:contract:no-frameworks-in-application]
name = Application has no framework imports
type = forbidden
source_modules =
    application
forbidden_modules =
    sqlalchemy
    fastapi
    starlette
    httpx
    redis
    boto3
```

Wire `lint-imports` into pre-commit and CI; rejection is non-negotiable.

## Best practices
- **Domain has zero third-party imports** (besides stdlib and pure value-object helpers). This single rule keeps the architecture honest.
- **Entities have behavior, not just data.** If your entity has 0 methods and 8 fields, write the methods or merge it into a use case.
- **Repositories return entities, not rows.** No `dict`, no ORM model leaving `infrastructure/`. Mappers convert at the boundary.
- **One use case = one user-visible operation.** Don't split `update_user` into 12 single-field setters; group by intent.
- **Unit-of-work, not bare repositories.** Multi-entity changes commit through a UoW; this is where transaction boundaries live.
- **Ports are thin.** A repository interface defines `find_by_id` / `save` / domain-specific finders; not `execute_raw_sql`.
- **DTOs at the edges.** Use cases take/return DTOs; controllers map to/from HTTP shapes; entities never leak across the layer boundary.
- **Make framework swap a real exercise.** Once a year, swap one adapter (in-memory ↔ Postgres, REST ↔ gRPC) — if you can't, the architecture is decorative.
- **Test pyramid follows layers.** Unit tests for domain entities (no I/O), use-case tests with fake repos, integration tests for adapters, a few e2e tests against real stack.
- **Keep mappers boring and centralized.** One `_mapping.py` per entity; agents will scatter mappers if you don't.

## AI-agent gotchas
- **Domain → infra leakage.** Agents add `from sqlalchemy import Column` "just for the model" inside `domain/`. `import-linter` blocks it; don't ship without it.
- **Anemic entities.** Code-gen agents output dataclasses with public attributes and no methods. Add a "behavior count" check; reject entities with 0 methods.
- **Repository implementing query DSL.** Agents add `find_users_with_subscription_status_in` methods that bake SQL into the interface. Force domain-language method names (`active_subscribers`) and an explicit query object pattern when filters get complex.
- **DTO drift.** Agents change a DTO field name in one layer and forget the mapper. Snapshot-test the mapper or generate it from a single source of truth (Pydantic-on-the-edge, dataclass-in-the-domain).
- **Direct ORM use in use case.** Agents call `session.execute(...)` from `application/use_cases/`. Banned import list catches the obvious ones; a CI rule for `session.execute` / `session.query` catches the rest.
- **Async/sync mixing.** Agents mark domain methods `async` "just in case"; entities should be sync-pure. Async lives in adapters and use cases.
- **One use case per HTTP verb.** Agents generate `GetUserUseCase`, `PutUserUseCase`, `PatchUserUseCase` — that's controller logic disguised as use cases. Re-frame: use cases describe intent, not HTTP shape.
- **Repository fakes that lie.** Agents write in-memory repos that don't enforce uniqueness or referential integrity, hiding bugs. Make the fake a strict mirror of constraints, or test against a real (containerized) DB for adapters.
- **Mapper logic in entities.** Agents add `User.from_orm()` to the entity. The entity must not know its persistence shape; mapper lives in `infrastructure/`.
- **Hallucinated framework versions.** Agents mix `fastapi.Depends` patterns from v0.x and v0.110+. Pin the framework and grep generated imports.

## References
- Martin, R. C. — "Clean Architecture: A Craftsman's Guide to Software Structure and Design." Pearson, 2017.
- Cockburn, A. — "Hexagonal Architecture." https://alistair.cockburn.us/hexagonal-architecture/
- Vernon, V. — "Implementing Domain-Driven Design." Addison-Wesley, 2013.
- Khononov, V. — "Learning Domain-Driven Design." O'Reilly, 2021.
- import-linter docs. https://import-linter.readthedocs.io
- Mark Seemann — "Clean Architecture and the Functional Core." https://blog.ploeh.dk
- "Onion Architecture" — Jeffrey Palermo. https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/
- Sibling: `pro/dev/code-quality/domain-driven-design/` — DDD on top of clean.
- Sibling: `pro/dev/code-quality/microservices-design/` (this batch) — when to push beyond.
