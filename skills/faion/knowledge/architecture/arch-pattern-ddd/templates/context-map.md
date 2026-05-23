# purpose: DDD context map: bounded contexts + relationships + aggregates + ubiquitous-language glossary.
# consumes: inputs declared in AGENTS.md Prerequisites; schema in content/02-output-contract.xml
# produces: a arch-pattern-ddd artefact validating against scripts/validate-arch-pattern-ddd.py
# depends-on: content/01-core-rules.xml, content/02-output-contract.xml
# token-budget-impact: ~400-1500 tokens once filled
---
artefact_id: ddd-context-map-<system>-2026-05-23
owner: <Full Name> <email>
version: 1.0.0
last_reviewed: 2026-05-23
---

## Bounded contexts

- **Catalog** — items, prices, availability.
- **Ordering** — order, line items, totals.
- **Fulfilment** — pick-pack-ship.
- **Billing** — invoices, payments.

## Context relationships

| Upstream | Downstream | Pattern |
|----------|------------|---------|
| Catalog | Ordering | Open Host (REST) |
| Ordering | Fulfilment | Domain Events |
| Ordering | Billing | Domain Events |

## Per-context aggregates

### Ordering
- Aggregate root: `Order`
- Entities: `LineItem`
- Value objects: `Money`, `ShippingAddress`
- Invariants:
  - Total = sum(line items) + tax - discounts
  - Order in state SUBMITTED cannot have lines added
- Domain events:
  - `OrderSubmitted`
  - `OrderShipped`
  - `OrderRefunded`

## Ubiquitous-language glossary

| Term | Definition | Owning context |
|------|------------|----------------|
| Order | A submitted basket awaiting fulfilment | Ordering |
| Line item | One product + quantity within an Order | Ordering |
| Item | A SKU + price + availability | Catalog |
