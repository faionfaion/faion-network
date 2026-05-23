---
slug: ddd-anti-corruption-layer
tier: pro
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Anti-Corruption Layer (ACL) adapter pattern — translate between legacy/external API and your domain model, keeping foreign terminology and exceptions out of the domain.
content_id: "9e826ddf0884612c"
complexity: medium
produces: code
est_tokens: 4200
tags: [ddd, anti-corruption-layer, adapter, bounded-context, integration]
---
# DDD Anti-Corruption Layer: Translation Adapters for External Systems

## Summary

**One-sentence:** Anti-Corruption Layer (ACL) adapter pattern — translate between legacy/external API and your domain model, keeping foreign terminology and exceptions out of the domain.

**One-paragraph:** When integrating with a legacy API, third-party SaaS, or another Bounded Context, importing their client SDK directly into the domain leaks their model into yours: field names, error shapes, eventual data drift. The ACL is an adapter in the infrastructure layer that implements a domain-defined interface (`InventoryChecker`, `PaymentGateway`) speaking the Ubiquitous Language and translates to/from the external system at the boundary. This methodology pins five rules: domain owns the interface, ACL is the only importer of external SDK, errors are translated, fail-safe defaults documented, and integration tests at the ACL boundary. Output: an ACL adapter + interface conforming to `02-output-contract.xml`.

**Ефективно для:**

- Integration with legacy systems whose model conflicts with the new domain.
- Third-party SaaS (Stripe, Twilio) where the SDK changes faster than your domain.
- Cross-bounded-context calls — each context owns its translation.
- Microservice splits where one team should not absorb another's vocabulary.
- AI-generated integrations where the model defaults to inlining SDK calls in services.

## Applies If (ALL must hold)

- An external system or another Bounded Context must be consumed.
- That system's model materially differs from this domain's model.
- The team controls the calling code (not a thin proxy / API gateway only).
- Domain interface can be added without breaking existing code.

## Skip If (ANY kills it)

- Simple HTTP client with no semantic gap — direct call is fine.
- Throwaway integration (one-off migration script) — overhead exceeds benefit.
- External system is owned by the same team and identical model — no corruption to prevent.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| External API docs | OpenAPI / SDK doc | vendor |
| Domain interface sketch | Markdown / source | team |
| Fail-safe policy | spec | spec / SLA |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ddd-aggregates]] | Domain that the ACL serves. |
| [[ddd-repositories]] | Sibling pattern — repository is an ACL over the database. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: domain-owns-interface, acl-only-sdk-importer, error-translation, fail-safe-documented, contract-tests | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for ACL spec + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: leaked-sdk-types, raw-exceptions, no-failsafe, no-contract-test | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on integration shape → rule | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `design-domain-interface` | sonnet | Vocabulary judgment. |
| `write-acl-adapter` | sonnet | Translation scaffolding. |
| `write-contract-test` | haiku | Mechanical wire-format pinning. |

## Templates

| File | Purpose |
|------|---------|
| `templates/DomainInterface.py` | Domain-layer interface skeleton |
| `templates/AclAdapter.py` | Infrastructure-layer ACL skeleton |
| `templates/contract-test.md` | Outline of contract test cases |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ddd-anti-corruption-layer.py` | Validate ACL spec against schema | Pre-commit on spec artefact |

## Related

- [[ddd-aggregates]]
- [[ddd-repositories]]
- [[ddd-value-objects]]
- parent skill: `pro/dev/software-developer/`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (semantic gap, integration durability, ownership) to a rule from `01-core-rules.xml`. Use it whenever adding a new external integration to decide whether to build a full ACL or accept a direct SDK call.
