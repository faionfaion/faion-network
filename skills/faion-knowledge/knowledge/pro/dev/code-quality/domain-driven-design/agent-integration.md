# Agent Integration — Domain-Driven Design

## When to use
- Greenfield service where the business rules are non-trivial (orders, billing, inventory, claims, scheduling, pricing) and rules will keep changing.
- Splitting a monolith into services and you need bounded contexts before drawing service boundaries — DDD prevents distributed-monolith outcomes.
- Refactoring an anemic codebase where logic has leaked into controllers/services and the same invariant is enforced in 4 places.
- A team includes a domain expert who can sit in modeling sessions; ubiquitous language is impossible without one.
- Multiple teams share a database/codebase and you need explicit context maps to negotiate ownership.

## When NOT to use
- CRUD admin tools, reporting dashboards, or scrapers — the "domain" is just data; DDD adds ceremony with no payoff.
- Solo prototype or MVP under ~2k LOC where requirements still flip weekly. Use a transaction script and refactor toward DDD only when the rules stabilize.
- Hot data-pipeline / ETL code — the model is rows and transformations, not aggregates with invariants.
- Real-time / latency-critical paths where the cost of repository hydration and event dispatch is not justified.
- Team has no access to a domain expert; you will produce a developer-invented model that the business does not recognize.

## Where it fails / limitations
- "DDD-lite" cargo cult: folders named `entities/`, `value_objects/`, `aggregates/` but the model is still anemic — same setters, same service-driven flow.
- Aggregate boundaries drawn around UI screens instead of true invariants → contention on the aggregate root, eventual lock storms.
- Repositories that leak ORM types (`Query`, `Session`, lazy-loaded relations) — the domain layer becomes infrastructure-coupled.
- Domain events fired before transaction commit → consumers act on data that gets rolled back. Always dispatch post-commit.
- LLMs over-decompose: every noun becomes an aggregate, every verb a domain service. The model fragments faster than humans can read it.
- Strategic design (context maps, core/supporting/generic subdomains) skipped because it requires business conversations that LLMs cannot have alone.

## Agentic workflow
DDD splits cleanly into a strategic phase (event storming, context mapping — human-led, LLM as scribe) and a tactical phase (entities/VOs/aggregates/repos — LLM does most of the typing under human review). Drive the strategic phase with `faion-brainstorm` to diverge on candidate bounded contexts, then converge on a context map. Drive the tactical phase with `faion-sdd-executor-agent` per bounded context: spec → design → implementation-plan → tasks, with `faion-sdd-execution` enforcing quality gates (no anemic models, no cross-aggregate references, repos return aggregates not rows). Always pass the ubiquitous-language glossary as the first context block of every prompt — without it the LLM invents synonyms (`User` vs `Customer` vs `Account`) within a single session.

### Recommended subagents
- `faion-brainstorm` — diverge/converge on bounded context candidates; surface domain events from event-storming notes; propose aggregate boundaries with rationale.
- `faion-sdd-executor-agent` — pick up a bounded-context task (e.g. "implement Order aggregate") and run spec → design → impl-plan → code with commit lifecycle.
- `faion-sdd-execution` — quality-gate hook: rejects PRs with anemic entities (only getters/setters), aggregate-to-aggregate object references, or domain code importing ORM/HTTP modules.
- `faion-feature-executor` — sequential execution across the tasks of one bounded context once the design is approved.
- `password-scrubber-agent` — run before committing example code; DDD examples often inline test credentials in repository fixtures.

### Prompt pattern
```
You are modeling the <bounded context> context.
Ubiquitous language (authoritative, do not rename):
  Order, OrderLine, Customer, Money, ShippingAddress, OrderPlaced, OrderShipped.

Produce: aggregates (with root + invariants), value objects (frozen),
domain events, repository interface (returns aggregates only).
Forbidden: ORM imports in domain layer, setters on entities,
references between aggregate roots (use IDs).
For each invariant, cite the business rule it enforces.
```

```
Review this diff against DDD tactical patterns.
Reject if: anemic entity, aggregate root with public mutable state,
repository returning DTOs/rows, domain service with infrastructure deps,
event published before transaction commit. Output one verdict block.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pyright` / `mypy --strict` | Catch leaking `Any` from ORM into domain layer | `pip install pyright` / `pip install mypy` |
| `ruff` (rules `B`, `SIM`, `UP`, `TCH`) | Enforces frozen dataclasses, imports-only-for-typing in domain | `pip install ruff` |
| `import-linter` | Declarative layer rules: domain forbidden to import infrastructure | https://import-linter.readthedocs.io |
| `archunit-py` / ArchUnit (JVM) | Architecture tests: aggregates only referenced via repos | https://www.archunit.org |
| `ddd-py` (community templates) | Scaffolds aggregate/VO/repo boilerplate | https://github.com/topics/ddd-python |
| `event-storming-md` | Plaintext event-storming sessions stored alongside code | any markdown editor |
| `context-mapper` (DSL + tooling) | Formal CML language for context maps, generates diagrams | https://contextmapper.org |
| `plantuml` / `mermaid` | Render context maps from text; LLM-friendly source format | https://plantuml.com / https://mermaid.js.org |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Miro / FigJam | SaaS | Partial (REST API) | Event storming whiteboards; agents can post sticky notes via API but cluster reasoning stays human |
| EventStorm.me | SaaS | No | Online event storming; no API |
| Context Mapper | OSS (VS Code + CLI) | Yes | CML files are plain text — perfect for LLM read/write; generates PlantUML |
| Structurizr | SaaS + DSL | Yes | C4 model in code; complements DDD context maps with deployment views |
| Lucid (Lucidchart) | SaaS | Partial | Diagram API exists; better as render target than reasoning surface |
| domainstorytelling.org tool | OSS web app | Partial | Export JSON for agents to parse |
| MURAL | SaaS | Partial (API) | Same model as Miro |
| Confluence | SaaS | Yes (REST) | Persist ubiquitous-language glossary as a single source of truth agents query before generating code |

## Templates & scripts

See `templates.md` for aggregate/VO/repository skeletons. The script below enforces the most-violated DDD rule (no infrastructure imports in `domain/`) — wire it into pre-commit or CI.

```bash
#!/usr/bin/env bash
# domain-purity-check.sh — fail if domain/ imports infrastructure libs.
# Usage: domain-purity-check.sh <repo-root>
set -euo pipefail

ROOT="${1:-.}"
FORBIDDEN='sqlalchemy|django\.db|pymongo|redis|requests|httpx|aiohttp|kafka|boto3|fastapi|flask|pydantic\.BaseModel'

mapfile -t files < <(find "$ROOT" -type d -name domain -prune -exec grep -rlE "^(import|from) ($FORBIDDEN)" {} +)

if [ "${#files[@]}" -gt 0 ]; then
  echo "DDD violation: infrastructure imports inside domain layer:"
  printf '  %s\n' "${files[@]}"
  exit 1
fi

echo "domain/ is pure (no forbidden imports)."
```

Companion ruleset for `import-linter` (`.importlinter`):

```ini
[importlinter]
root_package = order

[importlinter:contract:domain-purity]
name = Domain layer must not import infrastructure or application layers
type = forbidden
source_modules = order.domain
forbidden_modules = order.infrastructure, order.application, sqlalchemy, requests
```

## Best practices
- Write the ubiquitous-language glossary in `domain/GLOSSARY.md` and load it into every code-gen prompt as the first context block — single largest quality lever for LLM-generated DDD code.
- Treat aggregates as transaction boundaries: one aggregate per transaction, period. If you need to update two, publish an event and let a separate handler update the second.
- Reference other aggregates by ID only, never by object pointer; this prevents the reviewer-LLM from accidentally hydrating half the database.
- Make value objects `frozen=True` (Python) / `record` (Java) / `readonly struct` (C#) — immutability is non-negotiable, otherwise equality semantics break.
- Push validation into the constructor / factory method of the VO or aggregate, not into a service. If `Money(-5, "USD")` is impossible to construct, every consumer is automatically safe.
- Dispatch domain events post-commit (outbox pattern). The `Order.collect_events()` pattern in the README only works if the application service drains the buffer after the unit-of-work commits.
- Keep the core subdomain (where competitive advantage lives) hand-coded; let agents scaffold supporting/generic subdomains where commodity patterns suffice.
- Use Anti-Corruption Layers for every external system whose model you do not control — including agents calling external APIs. Translate at the boundary, never inside the domain.
- Distinguish core, supporting, and generic subdomains explicitly in the context map — only the core subdomain deserves full DDD investment. Supporting can be plain services; generic should be bought (Stripe, Auth0) or wrapped behind an ACL.
- Version the ubiquitous language: when business rules change, bump the glossary, regenerate stubs, diff the result.
- Co-locate aggregate, VOs, events, and repository interface in one folder per aggregate (`order/domain/`), and forbid imports between sibling aggregate folders. Folder boundaries become the architectural firewall agents cannot cross.
- Write architecture tests (`pytest` + `import-linter` or `archunit-py`) that fail the build on any DDD-rule violation. Treat them as load-bearing — they are the only feedback loop an unattended agent has.

## AI-agent gotchas
- LLMs love anemic models. Without an explicit "no public setters, methods must enforce invariants" instruction, the agent will emit `@dataclass` containers and put logic in services.
- Multi-context agent runs leak vocabulary across contexts: `Customer` from Sales reappears in Billing where the term is `Account`. Run each bounded context in its own conversation/worktree to keep namespaces clean.
- Agents conflate VOs with DTOs and silently make them mutable to "support serialization". Pin `frozen=True` and add a unit test that asserts immutability.
- LLMs cross aggregate boundaries by reflex: `order.customer.wallet.balance`. Add a lint rule (or prompt-level constraint) that aggregate roots may only hold IDs of other aggregates.
- Repositories drift toward "generic CRUD with filter dict" — kills the encapsulation. Force named query methods (`find_unpaid_orders_for_customer`) in the prompt.
- Domain events get fired inside the entity but never dispatched — agents forget the application-layer drain step. Add an integration test that asserts `published_events == expected`.
- Bounded-context boundaries are a human/business decision. An agent that proposes contexts from code alone will draw them around screens, tables, or REST resources — wrong axis. Human checkpoint mandatory before locking the context map.
- Ubiquitous language drift across sessions: an agent that starts saying `User` mid-session for what was `Customer` will poison the codebase. Pre-flight every prompt with the glossary; reject diffs that introduce new domain nouns without a glossary update PR.
- Token cost: full DDD prompts (glossary + invariants + existing aggregates) are large. Cache the glossary block and load only the relevant context's aggregates per task.
- Human-in-the-loop checkpoints: (1) bounded context map, (2) aggregate boundary decisions, (3) public method signatures of the aggregate root, (4) integration event contracts between contexts.

## References
- Eric Evans, *Domain-Driven Design: Tackling Complexity in the Heart of Software* (2003).
- Vaughn Vernon, *Implementing Domain-Driven Design* (2013) and *Domain-Driven Design Distilled* (2016).
- Alberto Brandolini, *Introducing EventStorming* (Leanpub, ongoing).
- DDD Reference card — https://www.domainlanguage.com/ddd/reference/
- Martin Fowler, "BoundedContext" and "AggregateRoot" — https://martinfowler.com/bliki/BoundedContext.html
- Context Mapper DSL — https://contextmapper.org/docs/language-reference/
- "Cosmic Python" / *Architecture Patterns with Python* (Percival & Gregory) — https://www.cosmicpython.com/
- Microsoft DDD-oriented microservices guide — https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/
