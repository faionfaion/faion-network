---
slug: architecture-decision-records
tier: solo
group: dev
domain: software-architect
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: An Architecture Decision Record (ADR) is a short document capturing one architecturally significant decision: Context (why the decision was needed), Decision (what was decided), Consequences (trade-offs accepted), and Alternatives (options rejected with reasons).
content_id: "e04a1ee4ff81d8de"
tags: [adr, architecture, decision-records, documentation, governance]
---
# Architecture Decision Records

## Summary

**One-sentence:** An Architecture Decision Record (ADR) is a short document capturing one architecturally significant decision: Context (why the decision was needed), Decision (what was decided), Consequences (trade-offs accepted), and Alternatives (options rejected with reasons).

**One-paragraph:** An Architecture Decision Record (ADR) is a short document capturing one architecturally significant decision: Context (why the decision was needed), Decision (what was decided), Consequences (trade-offs accepted), and Alternatives (options rejected with reasons). ADRs are immutable once accepted — never delete or edit accepted content; create a new superseding ADR instead. Store in docs/adr/ under version control alongside the code they affect.

## Applies If (ALL must hold)

- Any technology choice: language, framework, database, cloud provider
- Architecture style decisions: monolith vs microservices, REST vs gRPC, sync vs async
- Design pattern decisions at system scope: CQRS, Saga, Event Sourcing, API Gateway
- Third-party service selection: auth provider, payment gateway, monitoring tool
- Breaking changes: API versioning strategy, data migration approach
- Security decisions: auth mechanism, encryption standard, compliance approach
- Infrastructure decisions: container orchestration, CI/CD pipeline, deployment strategy
- Bootstrapping a new repo: ADR-0001 documents the starting architecture

## Skip If (ANY kills it)

- Trivial decisions (file naming, single-developer style choices) — overhead not justified
- Reversible cheap changes (variable names, internal helpers)
- Throwaway PoCs where decisions don't outlive the demo
- Ultra-confidential decisions (M&A, vendor pricing) that cannot live in a public Git repo

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

- parent skill: `solo/dev/software-architect/`
