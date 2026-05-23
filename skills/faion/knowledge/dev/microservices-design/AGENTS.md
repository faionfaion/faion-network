# Microservices Design

## Summary

**One-sentence:** Produces a microservices spec naming bounded contexts, per-service data ownership, transport contracts (HTTP/gRPC/async), circuit-breaker policies, and rules forbidding cross-service code imports and shared tables.

**One-paragraph:** Microservices structure an application as independently deployable services where each service owns its data, exposes a well-defined API, and communicates via HTTP/gRPC or async messaging. Each service has exactly one database (no shared tables); services never import each other's code directly; failures in one service must not cascade to others.

**Ефективно для:**

- Large application з кількома teams що працюють паралельно.
- Independent scaling (checkout 10x під час flash sales, user service ні).
- Continuous deployment де lockstep releases — bottleneck.
- Technology diversity з justified причиною (ML Python, billing Java).

## Applies If (ALL must hold)

- Large application with multiple teams working on different features simultaneously.
- Independent scaling required.
- Continuous deployment without lockstep release.
- Technology diversity justified.
- High availability where one service failure must not take down the product.

## Skip If (ANY kills it)

- Single team / early-stage startup.
- Domain not yet stable — premature service boundaries are costly.
- Team lacks distributed-systems experience.
- ACID across multiple business entities — sagas add significant complexity.
- Tight latency budget — each hop adds round-trip time.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Bounded-context map | Markdown | domain expert |
| Per-service data ownership table | spreadsheet | team |
| Transport policy (HTTP/gRPC/async) | ADR | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[domain-driven-design]] | Bounded contexts from DDD are the service boundaries |
| [[cap-pacelc-walkthrough]] | Each service's data store is chosen with CAP/PACELC explicit |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules with rationale + source | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom + root-cause + fix | ~900 |
| `content/04-procedure.xml` | essential | 7-step end-to-end procedure | ~800 |
| `content/05-examples.xml` | medium | One fully-worked example matching the output schema | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `inventory-services` | sonnet | Map bounded contexts to services + owners. |
| `design-transports` | sonnet | Pick HTTP vs gRPC vs async per interaction. |
| `author-failure-modes` | opus | Cross-service synthesis on circuit breakers + sagas. |
| `validate-output` | haiku | Schema check via the validator script. |

## Templates

| File | Purpose |
|------|---------|
| `templates/service-main.py` | FastAPI service skeleton with circuit-breaker import + DB ownership. |
| `templates/circuit-breaker.py` | Circuit breaker (CLOSED → OPEN → HALF_OPEN → CLOSED) for inter-service calls. |
| `templates/message-bus.py` | Async message bus for inter-service events (publish + subscribe). |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-microservices-design.py` | Validate the output artefact against the schema in 02-output-contract.xml. | CI on each artefact change; pre-commit. |

## Related

- [[domain-driven-design]]
- [[event-sourcing-implementation]]
- [[cap-pacelc-walkthrough]]

## Decision tree

See `content/06-decision-tree.xml`. Tree gates microservices on team count, scaling asymmetry, and ops maturity; otherwise modular monolith is the better default.
