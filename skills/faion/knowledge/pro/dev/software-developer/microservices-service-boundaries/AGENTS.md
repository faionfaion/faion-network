---
slug: microservices-service-boundaries
tier: pro
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Microservices architecture structures an application as a collection of loosely coupled, independently deployable services.
content_id: "7db354d14f880357"
tags: [microservices, architecture, bounded-context, service-design, ddd]
---
# Microservices Service Boundaries and Structure

## Summary

**One-sentence:** Microservices architecture structures an application as a collection of loosely coupled, independently deployable services.

**One-paragraph:** Microservices architecture structures an application as a collection of loosely coupled, independently deployable services. Each service owns its data and business logic, communicating through well-defined APIs. Boundaries follow bounded contexts — not layers, not convenience, not team politics.

## Applies If (ALL must hold)

- Large applications requiring independent scaling.
- Multiple teams (three or more) working on different features where service boundaries cleanly map to team boundaries (Conway's Law in reverse).
- Systems needing technology diversity (polyglot persistence is a real need — transactional Postgres for orders, document store for catalog, Redis for sessions).
- Applications requiring high availability and blast-radius isolation (PCI scope, PHI scope, regional data residency).
- Organizations practicing continuous deployment where independent deploy cadences matter.
- A monolith that has been internally modularised (modular monolith) and the seams are clearly load-bearing.
- Long-running async workflows where event-driven decoupling beats request/response chains.

## Skip If (ANY kills it)

- Solo or two-person teams — operational overhead (CI per service, deploy choreography, observability) eats more capacity than it returns.
- Pre-product-market-fit — domain boundaries are unstable; you will re-cut them three times and pay full distributed-systems tax each rewrite.
- Sub-millisecond synchronous chains (high-frequency trading, real-time bidding) — network hops kill the latency budget.
- "Microservices for resume" — a modular monolith with clean module boundaries delivers most benefits without the distributed pain.
- Tight transactional boundaries across services — if every command spans three services and two-phase coordination, the boundary is wrong.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `pro/dev/software-developer/`
