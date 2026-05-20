---
slug: discriminated-union-output
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: When a structured-output schema must choose between two or more distinct shapes (different agent actions, different entity types, different intents, different events), model the output as a discriminated union — a tagged union where one literal field (kind, type, action) is generated FIRST and selects which branch the rest of the object must follow.
content_id: "d72c9b347f599957"
tags: [structured-output, discriminated-union, pydantic, json-schema, schema-design]
---
# Discriminated-Union Structured Output

## Summary

**One-sentence:** When a structured-output schema must choose between two or more distinct shapes (different agent actions, different entity types, different intents, different events), model the output as a discriminated union — a tagged union where one literal field (kind, type, action) is generated FIRST and selects which branch the rest of the object must follow.

**One-paragraph:** When a structured-output schema must choose between two or more distinct shapes (different agent actions, different entity types, different intents, different events), model the output as a discriminated union — a tagged union where one literal field (kind, type, action) is generated FIRST and selects which branch the rest of the object must follow. The discriminator locks the JSON-Schema/grammar branch and turns shape selection into a single constrained-decoding choice instead of a probabilistic mess of optional fields.

## Applies If (ALL must hold)

- Agent action selection where each action has different required arguments (search vs fetch vs finish vs ask-user).
- Polymorphic entity extraction (Person vs Company vs Product vs Address) from one document.
- Router outputs that must dispatch to one of N downstream handlers.
- Event logs / message buses where each event type has its own payload schema.
- Multi-intent classification where every intent owns its own structured payload.

## Skip If (ANY kills it)

- All branches share more than ~90% of their fields — flatten with optional fields and a single kind literal instead, the union machinery costs more than it saves.
- The set of branches is open (user-defined entity types, plug-in actions) — use a registry pattern with free-string kind plus a separate validation pass.
- Targets that do not honour the discriminator keyword (older Outlines/XGrammar versions, custom GBNF grammars without union support) — fall back to two sequential calls (classify, then extract).

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

- parent skill: `geek/ai/ai-agents/`
