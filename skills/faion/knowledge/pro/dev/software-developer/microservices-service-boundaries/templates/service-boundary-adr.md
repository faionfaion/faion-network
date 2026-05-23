<!-- purpose: ADR template per service: context + data + team + contract -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~400 tokens when loaded as context -->

# ADR-XXX: {{service_name}} boundary

## Bounded context

{{Order Management | Billing | Inventory | ...}}

## Domain language

- Aggregate root: {{Order}}
- Value objects: {{LineItem, OrderStatus, ...}}
- Domain events: {{OrderCreated, OrderShipped, ...}}

## Data sovereignty

Owned tables:
- {{orders}}
- {{order_items}}

Cross-context references:
- {{customer_id → customer-profile-service (CDC replica)}}

## Team

- Owner: {{checkout-team}}
- Consumers: {{billing-service, inventory-service, analytics-pipeline}}

## Contract

- OpenAPI: {{https://schema-registry.example.com/order-service/v1}}
- Events published: {{orders.created.v1, orders.cancelled.v1}}
- Events consumed: {{payments.charged.v1, inventory.reserved.v1}}

## Cross-service transactions

- {{place-order saga (see /sagas/place-order.md)}}

## Alternatives considered

- Keep in monolith → rejected because {{independent deploy frequency required}}.
- Split further (Order + LineItem services) → rejected because {{within same aggregate, single tx required}}.
