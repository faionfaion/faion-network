---
slug: ddd-anti-corruption-layer
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: The Anti-Corruption Layer (ACL) is an adapter in the infrastructure layer that translates between the external system's model (a legacy API, a third-party service, another Bounded Context) and your domain model.
content_id: "058dbbad8be61ac9"
tags: [ddd, anti-corruption-layer, adapter, bounded-context, integration]
---
# DDD Anti-Corruption Layer: Translation Adapters for External Systems

## Summary

**One-sentence:** The Anti-Corruption Layer (ACL) is an adapter in the infrastructure layer that translates between the external system's model (a legacy API, a third-party service, another Bounded Context) and your domain model.

**One-paragraph:** The Anti-Corruption Layer (ACL) is an adapter in the infrastructure layer that translates between the external system's model (a legacy API, a third-party service, another Bounded Context) and your domain model. The domain defines an interface (InventoryChecker, PaymentGateway) that speaks the domain's Ubiquitous Language. The ACL implementation translates to and from the external system's terminology, data shapes, and error types — preventing the external model from leaking into your domain.

## Applies If (ALL must hold)

- Integrating with any external or third-party API (payment gateways, shipping carriers, inventory services, CRMs).
- Integrating with a legacy system that uses a different model or Ubiquitous Language than your bounded context.
- Integrating with another Bounded Context in the same organization that has its own model — the ACL prevents model contamination across context boundaries.
- Any integration where you want to isolate your domain from external API versioning and breaking changes.

## Skip If (ANY kills it)

- The external system's model is identical to your domain model and you control both — a direct call is simpler.
- Throwaway integrations that will be replaced within a sprint — overhead exceeds value for very short-lived adapters.
- The integration is purely read-only and the external data maps trivially to a DTO used only in the application layer (not in the domain).

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
