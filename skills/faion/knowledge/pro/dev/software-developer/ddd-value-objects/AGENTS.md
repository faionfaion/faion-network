---
slug: ddd-value-objects
tier: pro
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A Value Object is a domain concept defined entirely by its attributes, not by identity.
content_id: "15f593ebd58453d6"
tags: [ddd, value-objects, immutability, domain-model, primitive-obsession]
---
# DDD Value Objects: Immutable Self-Validating Domain Types

## Summary

**One-sentence:** A Value Object is a domain concept defined entirely by its attributes, not by identity.

**One-paragraph:** A Value Object is a domain concept defined entirely by its attributes, not by identity. Two Value Objects with the same attributes are equal. Value Objects are immutable: instead of mutating state, operations return new instances. They encapsulate validation, making illegal states unrepresentable. Use them to replace primitive obsession (raw strings, ints, Decimals) with meaningful types (Money, Email, Address, PhoneNumber).

## Applies If (ALL must hold)

- Any domain primitive with validation rules: email addresses, phone numbers, monetary amounts, postal codes, URLs, percentages.
- Any primitive whose meaning is context-dependent: a "quantity" VO in the order context vs. an "inventory level" VO in the warehouse context.
- Compound values that always travel together: street + city + postal + country = Address; amount + currency = Money.
- Replacing repeated inline validation scattered across the codebase.

## Skip If (ANY kills it)

- Objects with identity that persist across time — those are Entities, not Value Objects.
- Simple configuration tuples or DTOs in the application/infrastructure layer where domain semantics do not apply.
- Extremely performance-sensitive hot paths where object allocation cost is measurable — profile first.

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
