# purpose: Clean Architecture module layout with four rings and dependency rule.
# consumes: inputs declared in AGENTS.md Prerequisites; schema in content/02-output-contract.xml
# produces: a arch-pattern-clean artefact validating against scripts/validate-arch-pattern-clean.py
# depends-on: content/01-core-rules.xml, content/02-output-contract.xml
# token-budget-impact: ~400-1500 tokens once filled
---
artefact_id: clean-layout-<system>-2026-05-23
owner: <Full Name> <email>
version: 1.0.0
last_reviewed: 2026-05-23
---

## Ring 1 — Entities (Domain)

Modules: `domain/`
- Pure business types (no framework imports).
- Examples: `Order`, `LineItem`, `Money`, value objects.

## Ring 2 — Use Cases (Application)

Modules: `application/`
- Orchestration of domain entities to fulfil use cases.
- Examples: `PlaceOrderUseCase`, `RefundOrderUseCase`.
- Depends on: domain only.

## Ring 3 — Interface Adapters

Modules: `adapters/`
- Controllers (HTTP, CLI), presenters, gateways.
- Examples: `OrderHttpController`, `StripePaymentGateway`.
- Depends on: application + domain.

## Ring 4 — Frameworks & Drivers

Modules: `infrastructure/`
- DB drivers, HTTP server, queue clients, framework wiring.
- Examples: `SqlAlchemyOrderRepository`, `FastApiServer`.
- Depends on: adapters + application + domain.

## Dependency rule

Code in an inner ring MUST NOT import from an outer ring. Enforce via lint (e.g., `importlinter`, `archunit`, `go-import-lint`).
