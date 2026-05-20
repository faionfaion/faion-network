---
slug: enum-constraints-closed-vocabularies
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Whenever the answer set is finite, declare it as a typed enum (Literal[.
content_id: "4bebb5f1878e0e5a"
tags: [structured-output, enums, classification, constraints, decoding]
---
# Enum Constraints for Closed Vocabularies

## Summary

**One-sentence:** Whenever the answer set is finite, declare it as a typed enum (Literal[.

**One-paragraph:** Whenever the answer set is finite, declare it as a typed enum (Literal[...] in Pydantic, enum in JSON Schema) instead of a free-form string. Constrained decoders mask every non-enum token to probability zero, so a hallucinated label becomes mathematically impossible. The rule is a one-line schema change with the highest accuracy-per-token ratio of any structured-output trick.

## Applies If (ALL must hold)

- Any classification field — sentiment, intent, severity, routing label, language code, status state.
- Pick-one-of-N action selection inside an agent loop.
- Field that maps to a downstream switch/case or DB enum column.
- Pipelines where an unknown label silently breaks the next stage.

## Skip If (ANY kills it)

- Open vocabularies (free-text tags, novel entity types, user names) — enum would clip valid answers.
- Semi-open sets — use Literal[...] | str plus a discriminated union or post-validation instead.
- JSON-mode-only fallback paths on mini/nano models — enums are advisory there, pair with strict mode or a constrained backend (XGrammar, Outlines) to actually enforce them.

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
