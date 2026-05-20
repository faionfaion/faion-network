---
slug: field-descriptions-as-prompts
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Treat every `description=` on a schema field as a tiny prompt the model sees right before it generates that field.
content_id: "16876fd226cf6321"
tags: [structured-output, schema-design, llm-reliability, field-descriptions, prompt-engineering]
---
# Field Descriptions as Inline Mini-Prompts

## Summary

**One-sentence:** Treat every `description=` on a schema field as a tiny prompt the model sees right before it generates that field.

**One-paragraph:** Treat every `description=` on a schema field as a tiny prompt the model sees right before it generates that field. Be explicit about format, range, units, edge cases, and forbidden patterns. PARSE research (2025) showed that optimizing field descriptions yields 60%+ improvement in extraction accuracy. Making relationships explicit in descriptions improves complex-reasoning accuracy by up to 40%.

## Applies If (ALL must hold)

- Always — descriptions cost ~10 tokens each and pay for themselves
- Especially for: ambiguous units (USD vs cents, kg vs lb), formats (ISO-8601), exclusions ("ignore retracted papers"), cardinality bounds
- For fields where you need format compliance > 99%

## Skip If (ANY kills it)

- When description duplicates enum members verbatim (the enum already constrains decoding)
- When schema is so large that descriptions blow the cold-cache budget — strip them only on cache-warm calls
- When the description would contradict the field name (rename instead)

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
