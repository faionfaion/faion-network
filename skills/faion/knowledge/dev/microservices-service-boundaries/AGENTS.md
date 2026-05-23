# Microservices Service Boundaries

## Summary

**One-sentence:** Define microservice boundaries using DDD bounded contexts: ownership, data sovereignty, transactional locality, team alignment, and contract-first APIs.

**One-paragraph:** Boundary mistakes are the dominant cost in microservices — chatty cross-service calls, distributed transactions, brittle dependency chains. Use DDD bounded contexts: each service owns its domain language, data, and team. Boundaries align with business sub-domains, not technical layers. Each service exposes a published contract; internal models are private. Cross-service consistency uses sagas or eventual consistency, never shared databases.

**Ефективно для:**

- Monolith → microservices decomposition: де провести розрізи.
- Greenfield N-сервісного дизайну: визначити bounded contexts перед кодом.
- Architecture review для встановлення data ownership + контрактів.
- Refactor поточних мікросервісів які мають chatty inter-service traffic.

## Applies If (ALL must hold)

- ≥2 candidate services exist OR planned decomposition of a monolith.
- Domain has identifiable sub-domains (DDD bounded contexts can be drawn).
- Team can commit to data sovereignty (no cross-service joins on DB level).
- Contract-first culture (OpenAPI/protobuf in source control).

## Skip If (ANY kills it)

- Service count <2 — boundary discussion is N/A.
- Domain is genuinely tightly coupled (single transactional unit) — keep monolith.
- Team < 5 people total — boundary cost > benefit.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Domain model | event-storming output / domain glossary | domain experts |
| Team structure | Conway's-law map | engineering org |
| Current DB schema | ER diagram / migration history | DBA |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ddd-aggregates]] | Aggregate is the unit of consistency inside a bounded context. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: one-bounded-context-one-service, data-sovereignty, transactional-locality, published-contract, team-alignment-conway | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for spec + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 900 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `event-storming-synthesis` | opus | Domain modeling is high-judgment; needs holistic reasoning. |
| `data-ownership-mapping` | sonnet | Templated mapping table generation. |
| `lint-cross-service-joins` | haiku | Mechanical SQL grep + DSN audit. |

## Templates

| File | Purpose |
|------|---------|
| `templates/service-boundary-adr.md` | ADR template per service: context + data + team + contract |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-microservices-service-boundaries.py` | Validate the boundary artefact against the schema | Pre-commit + CI |

## Related

- [[ddd-aggregates]]
- [[microservices-inter-service-comm]]
- [[microservices-saga-pattern]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, stack, runtime, scale, etc.) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
