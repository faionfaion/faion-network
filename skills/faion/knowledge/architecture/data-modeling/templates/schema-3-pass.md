# purpose: Three-pass schema spec template.
# consumes: inputs declared in AGENTS.md Prerequisites; schema in content/02-output-contract.xml
# produces: a data-modeling artefact validating against scripts/validate-data-modeling.py
# depends-on: content/01-core-rules.xml, content/02-output-contract.xml
# token-budget-impact: ~400-1500 tokens once filled
---
artefact_id: schema-<system>-2026-05-23
owner: <Full Name> <email>
version: 1.0.0
last_reviewed: 2026-05-23
engine: <postgres 16 | mongo 7 | dynamodb | ...>
---

## Pass 1 — Conceptual

Entities and relationships in business language. No attributes.

```
Order *--* LineItem
Order >--1 Customer
LineItem >--1 Item
```

## Pass 2 — Logical

Attributes, keys, cardinality, 3NF, tech-agnostic.

| Entity | Attributes | Keys |
|--------|------------|------|
| Order | id, customer_id, status, total, created_at | PK(id), FK(customer_id) |
| LineItem | order_id, item_id, qty, unit_price | PK(order_id, item_id), FK(order_id), FK(item_id) |

## Pass 3 — Physical

Engine-specific types, indexes, partitions.

```sql
CREATE TABLE orders (
  id          uuid PRIMARY KEY,
  customer_id uuid NOT NULL REFERENCES customers(id),
  status      order_status NOT NULL,
  total       numeric(12,2) NOT NULL,
  created_at  timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX orders_customer_id_created_at ON orders (customer_id, created_at DESC);
```

## Migration plan

- DDL: `migrations/2026-05-23-orders.sql`
- Backfill: <strategy>
- Rollback: drop + restore from `_old` shadow table.
