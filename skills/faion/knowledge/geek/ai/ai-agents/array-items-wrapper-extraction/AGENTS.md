---
slug: array-items-wrapper-extraction
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: When extracting N entities from a document, never make the top-level structured-output response a bare array.
content_id: "0f0a0928361f82ef"
tags: [structured-output, extraction, schema-design, strict-mode, cardinality]
---
# Array Items Wrapper for Extraction

## Summary

**One-sentence:** When extracting N entities from a document, never make the top-level structured-output response a bare array.

**One-paragraph:** When extracting N entities from a document, never make the top-level structured-output response a bare array. Always wrap with {items: [...]} plus metadata fields like total_found and truncated. Strict-mode validators reject top-level arrays because schema-level controls like additionalProperties are object-only; wrapping standardises the shape across zero/one/many cases and lets you add count and truncation diagnostics without reshaping consumers.

## Applies If (ALL must hold)

- Any extraction with variable cardinality (entities, citations, line items, search hits).
- Document-level summarisation that yields a list of facts/claims.
- Batch classification where N inputs map to N outputs.
- Any strict-mode SO call (OpenAI, Azure) — the top-level array is forbidden there anyway.

## Skip If (ANY kills it)

- Hard-coded N (always exactly 3 suggestions) — use a fixed-length tuple type or named fields instead.
- Single-entity extraction with no list semantics — wrap is overhead for a one-shot field.
- Streaming UIs that render items as they arrive — items at top level can stream natively; wrap blocks streaming until the wrapper closes.

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
