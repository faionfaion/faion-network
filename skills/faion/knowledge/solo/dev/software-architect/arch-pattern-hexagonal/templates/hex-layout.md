# purpose: Hexagonal Architecture layout spec.
# consumes: inputs declared in AGENTS.md Prerequisites; schema in content/02-output-contract.xml
# produces: a arch-pattern-hexagonal artefact validating against scripts/validate-arch-pattern-hexagonal.py
# depends-on: content/01-core-rules.xml, content/02-output-contract.xml
# token-budget-impact: ~400-1500 tokens once filled
---
artefact_id: hex-layout-<system>-2026-05-23
owner: <Full Name> <email>
version: 1.0.0
last_reviewed: 2026-05-23
---

## Application Core

Modules: `domain/`, `application/`
- Pure logic; no framework imports.

## Driving (Inbound) Ports

| Port | Type | Adapter |
|------|------|---------|
| `OrderInputPort` | use-case interface | `HttpOrderController` |
| `OrderInputPort` | same | `CliOrderCommand` |

## Driven (Outbound) Ports

| Port | Type | Adapter |
|------|------|---------|
| `OrderRepositoryPort` | persistence | `SqlAlchemyOrderRepository` |
| `PaymentPort` | external API | `StripePaymentAdapter` |

## Lint

- Tool: importlinter
- Contract: independence; domain MUST NOT import from adapters/*.
