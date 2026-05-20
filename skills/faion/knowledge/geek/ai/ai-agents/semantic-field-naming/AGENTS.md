---
slug: semantic-field-naming
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Field NAMES are part of the prompt.
content_id: "ac6c44a2f500eb6e"
tags: [semantic, field-naming, structured-output, schema, accuracy]
---
# Semantic Field Naming

## Summary

**One-sentence:** Field NAMES are part of the prompt.

**One-paragraph:** Field NAMES are part of the prompt. Choose names that are specific, English, and semantically loaded — never field1, val, data, output. Renaming a single field can swing accuracy by tens of points. The structured-output pipeline turns your schema into part of the prompt the model is conditioned on. The model has seen tens of millions of answer keys and has very high prior probability for what should follow. It has barely seen final_choice — it has to guess what to put there. Naming equals priming. Specific, semantically-loaded names recruit pre-trained knowledge for free.

## Applies If (ALL must hold)

- Always. Costs nothing.
- Especially for fields with units (age_years, price_usd, weight_kg).
- For Booleans — make truth explicit (is_returning_customer, not flag).
- For enums-mapped strings — the field name should reflect the enum's domain (severity not level).

## Skip If (ANY kills it)

- Never. Even legacy schemas should at least add description to compensate for cryptic names.

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
