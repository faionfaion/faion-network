---
slug: strict-mode-required-fields
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: OpenAI/Azure strict-mode structured outputs compile each schema into a finite-state grammar.
content_id: "bea87bacbd08a657"
tags: [structured-outputs, json-schema, strict-mode, pydantic, openai]
---
# Strict-Mode Schemas: Required-Everything + No Additional Properties

## Summary

**One-sentence:** OpenAI/Azure strict-mode structured outputs compile each schema into a finite-state grammar.

**One-paragraph:** OpenAI/Azure strict-mode structured outputs compile each schema into a finite-state grammar. The grammar refuses any schema where some properties are required and others are merely declared, or where the object accepts unknown keys. The rule: every property defined on an object must be listed in required, and every object must set additionalProperties: false. Optional fields are simulated by making the type nullable (T | None), not by omitting them from required.

## Applies If (ALL must hold)

- Any call against the OpenAI Responses API or Chat Completions with response_format: {type: "json_schema", strict: true}.
- Anthropic tool-use where the tool input must be exhaustively typed (additionalProperties: false keeps the model from inventing parameters).
- Azure OpenAI strict mode and Google Gemini responseSchema with strict enforcement.
- Generating JSON-Schema artifacts to ship to a third-party that runs the same compiler (Outlines / XGrammar with strict-grammar mode).

## Skip If (ANY kills it)

- Local Outlines or XGrammar pipelines that support standard JSON-Schema optional fields natively — required-everything wastes tokens for no grammar gain.
- Loose JSON mode (response_format: {type: "json_object"}) — there is no grammar, so the constraint does not apply (and you also do not get format guarantees).
- Schemas that intentionally accept open-ended additional properties (e.g., a metadata bag for arbitrary user keys) — strict mode is the wrong tool; either drop strict or split the bag into a typed sub-object plus a separate audit field.

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
