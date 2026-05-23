---
slug: domain-driven-design
tier: pro
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a DDD module: bounded context with ubiquitous-language entities + value objects + aggregates enforcing invariants in the model (not in services), plus a context map between bounded contexts.
content_id: "a753b3732f78dae8"
complexity: deep
produces: code
est_tokens: 4300
tags: [ddd, domain, architecture, modeling, ubiquitous-language]
---
# Domain-Driven Design

## Summary

**One-sentence:** Produces a DDD module: bounded context with ubiquitous-language entities + value objects + aggregates enforcing invariants in the model (not in services), plus a context map between bounded contexts.

**One-paragraph:** DDD models complex business domains through a shared ubiquitous language, explicit bounded contexts, and rich domain objects (entities, value objects, aggregates) that enforce invariants inside the model — not in services. An Order that cannot be placed when empty is safer than a service that checks emptiness before calling order.place(). Without DDD, business rules scatter across controllers and services; with DDD, the model owns them.

**Ефективно для:**

- Складний domain з правилами що еволюціонують (orders, billing, claims).
- Monolith → microservices — bounded contexts визначають service boundaries.
- Anemic codebase, де logic витекла в services/controllers.
- Команда з domain expert у modeling sessions.

## Applies If (ALL must hold)

- Complex business domain with rules that keep changing.
- Splitting a monolith — bounded contexts define service boundaries.
- Refactoring an anemic codebase where logic leaked into controllers/services.
- Team has access to a domain expert for modeling sessions.

## Skip If (ANY kills it)

- CRUD admin tools or scrapers — DDD adds ceremony without payoff.
- Solo prototype under ~2k LOC where requirements flip weekly.
- Hot ETL code — the model is rows + transformations, not aggregates.
- Latency-critical path where repository hydration cost is unjustified.
- Team has no domain expert — you will produce a developer-invented model the business does not recognise.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Domain expert availability | schedule | team |
| Glossary / ubiquitous-language draft | Markdown | domain expert |
| Aggregate / entity / value-object list | model doc | domain expert |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[clean-architecture]] | DDD entities live in the domain layer Clean Architecture defines |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules with rationale + source | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | ~900 |
| `content/04-procedure.xml` | essential | 6-step end-to-end procedure | ~800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-ubiquitous-language` | sonnet | Term list from interviews + glossary refinement. |
| `model-aggregates` | sonnet | Pick aggregate roots + identify invariants enforced internally. |
| `write-context-map` | opus | Cross-context synthesis when multiple bounded contexts interact. |
| `validate-output` | haiku | Schema check via the validator script. |

## Templates

| File | Purpose |
|------|---------|
| `templates/aggregate.py` | Aggregate root template with internal invariant enforcement. |
| `templates/ddd-prompt.txt` | Prompt template for domain-expert modeling session. |
| `templates/domain-purity-check.sh` | Shell script: greps domain/ for framework imports; exits 1 if any. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-domain-driven-design.py` | Validate the output artefact against the schema in 02-output-contract.xml. | CI on each artefact change; pre-commit. |

## Related

- [[clean-architecture]]
- [[cqrs-pattern]]
- [[event-sourcing-basics]]

## Decision tree

See `content/06-decision-tree.xml`. Tree gates DDD on domain complexity, expert availability, and team willingness to enforce model purity.
