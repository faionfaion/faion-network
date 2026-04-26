# Agent Integration — Domain-Driven Design

## When to use
- Complex domains where business rules outweigh CRUD: insurance pricing, scheduling, billing, compliance, fulfillment, healthcare.
- Multi-team systems with strong language barriers between engineers and domain experts — DDD's Ubiquitous Language is the bridge.
- Splitting a monolith: identifying Bounded Contexts before extracting microservices avoids creating distributed monoliths.
- Long-lived products (>3 years) where evolving rules will outpace any "anemic CRUD" model.

## When NOT to use
- Pure CRUD apps, internal tooling, dashboards — Active Record / minimal DTOs are faster.
- Greenfield startups still discovering the domain — invest in DDD only after Bounded Contexts stabilize.
- Throwaway scripts, ETL jobs, prototypes.
- Real-time / streaming systems where the domain is data flow, not state changes — actor models or stream processors fit better.
- Teams without domain experts available — DDD without subject-matter experts produces fictional models.

## Where it fails / limitations
- "Big upfront DDD" creates a thicket of Aggregates/Repositories/Services for a domain that's actually CRUD. Cargo-cult DDD is worse than no DDD.
- Aggregate boundaries are hard — too small means transactional consistency fights, too large means write contention.
- Anti-Corruption Layers double the surface; agents tend to skip translation and leak external models into the domain.
- Domain Events without an outbox/eventual consistency story create dual-write bugs (DB committed, event lost).
- Repositories over ORMs: thin repos add a layer; rich repos try to recreate the ORM.
- "Anemic" model creep — once teams accept setters, the rich-domain discipline collapses.

## Agentic workflow
DDD work splits cleanly into modeling (high-judgment) and implementation (mechanical). Use a planner subagent (Opus) to produce a Bounded Context map and event-storming output as Markdown — that's a checkpoint for human review. Once the model is signed off, an implementation subagent (Sonnet/Haiku) generates Aggregate roots, Value Objects, Repository interfaces, Domain Events, and Application Services from the spec. Always include unit tests pinning Aggregate invariants and a separate Anti-Corruption Layer when integrating with external systems.

### Recommended subagents
- `faion-sdd-executor-agent` — drives spec → tests → implementation cycle once model is locked.
- A `ddd-modeler` subagent (Opus, planner) — outputs Bounded Context map + Aggregate diagrams in Markdown/Mermaid.
- A `ddd-implementer` subagent (Sonnet, code) — generates Aggregate + VO + Repo + Events from the locked spec.
- An `acl-builder` subagent — generates Anti-Corruption Layer adapters when integrating with legacy or external services.

### Prompt pattern
```
Phase 1 (modeler):
Domain: subscription billing. Produce:
- Bounded Contexts (Subscription, Billing, Notifications) with relationships
  (Customer-Supplier, Shared Kernel, ACL)
- Aggregates per context with root + invariants list
- Domain events crossing contexts
- Ubiquitous Language glossary (term -> definition)
Output as Markdown for human review. STOP. Do not write code.

Phase 2 (implementer, after sign-off):
Implement Subscription aggregate per locked spec at .product/ddd/subscription.md:
- Aggregate root Subscription with invariants enforced in methods
- Value Objects: BillingPeriod, Money (frozen)
- Domain events: SubscriptionActivated, SubscriptionRenewed, SubscriptionCancelled
- Repository interface SubscriptionRepository (no ORM types)
- Tests covering each invariant + state transition
Use frozen dataclasses (Python) or records (Java/C#). No setters on root.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `mermaid-cli` (`mmdc`) | Render Bounded Context maps from Markdown | `npm i -g @mermaid-js/mermaid-cli` |
| `eventstorming` (Miro/Lucid web) | Event Storming workshops | https://www.eventstorming.com |
| `context-mapper` | DSL for Bounded Context maps + analysis | https://contextmapper.org |
| `pact-broker` / `pactflow` | Contract testing across Bounded Contexts | https://pactflow.io |
| `archunit` (Java), `dependency-cruiser` (TS) | Enforce layer/Bounded Context boundaries in code | https://www.archunit.org / https://github.com/sverweij/dependency-cruiser |
| `tach` (Python), `nx` (TS monorepo) | Module-boundary enforcement | https://github.com/gauge-sh/tach |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| EventStoreDB / Marten | OSS | Yes | Native event-sourced store, fits Aggregate event streams |
| Kafka / Redpanda + Outbox pattern | OSS | Yes | Domain events with at-least-once delivery; pair with `debezium` |
| Axon Framework (Java) | OSS + commercial | Partially | DDD/CQRS framework; opinionated, agents need ramp-up |
| Wolverine (.NET) | OSS | Yes | DDD-friendly mediator + outbox |
| Marten (.NET on Postgres) | OSS | Yes | Event store + document DB; LLMs handle it well |
| Temporal | SaaS + OSS | Yes | Long-running domain workflows = sagas across contexts |
| Specflow / Cucumber | OSS | Yes | Behavior tests in Ubiquitous Language |

## Templates & scripts
See `templates.md` for Aggregate/VO/Event scaffolds. Snippet — Aggregate invariant test (pytest):

```python
# tests/domain/test_order.py
import pytest
from decimal import Decimal
from order.domain.entities.order import Order, OrderStatus
from order.domain.value_objects import Money, Address

def test_cannot_place_empty_order():
    order = Order(customer_id="c-1")
    with pytest.raises(DomainError, match="empty"):
        order.place(shipping_address=_addr())

def test_place_emits_event():
    order = Order(customer_id="c-1")
    order.add_line("p-1", "X", 1, Money(Decimal("10"), "USD"))
    order.place(shipping_address=_addr())
    events = order.collect_events()
    assert len(events) == 1
    assert events[0].order_id == order.id

def test_cannot_modify_after_place():
    order = Order(customer_id="c-1")
    order.add_line("p-1", "X", 1, Money(Decimal("10"), "USD"))
    order.place(_addr())
    with pytest.raises(DomainError, match="placed"):
        order.add_line("p-2", "Y", 1, Money(Decimal("5"), "USD"))

def _addr():
    return Address("1 Main", "City", "ST", "12345", "US")
```

## Best practices
- Start with Event Storming, not class diagrams. The output names the Aggregates and events, not your imagination.
- One Aggregate per transaction. Cross-aggregate consistency is eventual, via events + sagas.
- Value Objects: frozen, immutable, with self-validation in `__post_init__` / constructor.
- Repository returns Aggregates by ID, not collections by query — those go in a Read Model / Query side.
- Keep domain layer free of framework imports (no Django, Rails, EF, JPA). Only the infrastructure layer adapts.
- Use `private` setters and intention-revealing methods (`order.place()` not `order.status = "placed"`).
- Anti-Corruption Layer everywhere you touch a legacy/external API — never let their model leak.
- Pair Domain Events with the Outbox pattern (insert event row in same DB tx as state change; relay later).
- Apply CQRS only when read and write demands genuinely diverge — DDD ≠ CQRS.

## AI-agent gotchas
- Agents produce anemic models by default — entities are dataclasses with services manipulating fields. Pin "no public setters; behavior on the entity" in prompts and review for it.
- They cross Aggregate boundaries (`order.customer.wallet.balance`) — flag any Aggregate field access that traverses another root.
- LLMs invent Bounded Contexts that don't reflect actual organizational boundaries. The model must come from real domain experts; the agent only formalizes it.
- Generated Domain Events lack idempotency keys / event IDs — handlers will double-process.
- Agents conflate Domain Services with Application Services — Domain Services hold pure logic, Application Services orchestrate (transaction, repository, dispatch). Require explicit naming.
- Human-in-loop checkpoint #1: Bounded Context map and Ubiquitous Language MUST be reviewed by a domain expert before any code generation.
- Human-in-loop checkpoint #2: invariants list per Aggregate (frozen as failing tests first) — verify with the team before implementation.
- Watch for "DDD washing": adding folders called `domain/`, `application/`, `infrastructure/` while keeping anemic models is theater.

## References
- Eric Evans — "Domain-Driven Design: Tackling Complexity in the Heart of Software" (the Blue Book)
- Vaughn Vernon — "Implementing Domain-Driven Design" (the Red Book)
- Vaughn Vernon — "Domain-Driven Design Distilled" (short intro)
- Alberto Brandolini — "Introducing EventStorming": https://www.eventstorming.com/book/
- Martin Fowler — DDD tag: https://martinfowler.com/tags/domain%20driven%20design.html
- Khalil Stemmler — DDD in TypeScript: https://khalilstemmler.com/articles/categories/domain-driven-design/
- DDD Reference (Evans, free PDF): https://www.domainlanguage.com/ddd/reference/
