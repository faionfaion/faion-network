---
slug: structured-output
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
content_id: "1237cf075a04f940"
summary: Forces LLM responses into a typed JSON Schema / Pydantic shape using provider-native structured-output features (OpenAI response_format, Anthropic tool-use json mode, Gemini schema) with safe-parse + repair retry.
complexity: medium
produces: code
est_tokens: 3400
tags: [structured-output, json-schema, pydantic, validation, type-safety]
---

# Structured Output for LLMs

## Summary

**One-sentence:** Provider-native structured-output pattern that constrains the LLM to a JSON Schema / Pydantic model, parses safely, and retries with the schema attached to the error on the first parse failure.

**One-paragraph:** Unstructured LLM responses force downstream callers to regex-extract or re-prompt, which fails ≈5-15% of the time even on capable models. Modern providers (OpenAI 4o+, Anthropic, Gemini, Mistral) accept a JSON Schema and return responses that conform — provider-side constrained decoding eliminates the failure class. The methodology pins: declare a Pydantic model OR JSON Schema, pass to provider `response_format` / `tool_choice`, parse with explicit safety, on failure re-prompt once with the schema + error included. Anti-patterns: regex-extracting JSON from natural prose, accepting any parse without schema validation, infinite retry loops. Output: a typed value + a `repair_attempts: int` field.

**Ефективно для:**

- Entity extraction із PDF, email, чатів — pydantic + provider schema дає 99% parse success замість 85% regex.
- Tool dispatchers де agent видає `{tool, args}` JSON — структурний output вилучає весь error-handling шар.
- Multi-step workflows де крок N споживає крок N-1 — типобезпека між кроками робить pipeline тестованим.
- Cost-sensitive cases — провайдер-side constrained decoding швидше і дешевше за re-prompt loop.

## Applies If (ALL must hold)

- Output is consumed by code (parser / downstream call), not displayed to user
- Provider supports structured output natively (OpenAI 4o+, Anthropic, Gemini 2+, Mistral large)
- Schema can be expressed in JSON Schema (no recursive types, no unbounded depth)
- Acceptable to retry once on parse failure (≤2× latency budget)

## Skip If (ANY kills it)

- Output is free-form prose for user display
- Provider doesn't support structured output AND switching providers is off-table
- Schema is genuinely dynamic per request (different shape every call)
- Real-time streaming where partial JSON must render — use streaming JSON parser instead

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| `pydantic-models.py` OR `schema.json` | Pydantic OR JSON Schema | data layer / API spec |
| `provider-rate-cards.yaml` | YAML | finance |
| `sample-inputs.jsonl` | JSONL | dev / SME |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `tool-use-function-calling` | Adjacent pattern; tool calls use the same constrained decoding |
| `llm-decision-framework` | Provider selection where structured-output capability matters |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: provider-native first, schema-validated parse, repair once, log raw on failure, no recursive schemas | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for `StructuredCallResult{value, repair_attempts, raw}` | 700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: regex extract, infinite retry, schema drift, recursive schema, silent fallback | 900 |
| `content/04-procedure.xml` | essential | 5 steps: design schema → pick provider mode → wire parse+repair → eval coverage → ship | 700 |
| `content/05-examples.xml` | essential | Worked example: entity extraction from support emails with Pydantic | 500 |
| `content/06-decision-tree.xml` | essential | Routes by schema complexity + provider to OpenAI response_format / Anthropic tool / Gemini schema | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `extraction_at_scale` | sonnet | Volume, bounded judgement |
| `schema_design_review` | opus | Cross-domain shape thinking |
| `structured_call_lint` | haiku | Schema check |

## Templates

| File | Purpose |
|------|---------|
| `templates/entity-extraction.py` | Pydantic-driven entity extraction with OpenAI response_format |
| `templates/safe-parse.py` | safe-parse + repair-retry wrapper |
| `templates/structured-output.schema.yaml` | Schema for the typed call result |
| `templates/_smoke-test.yaml` | Minimum-viable spec |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-structured-output.py` | Lint structured-output config | Pre-commit |

## Related

- [[tool-use-function-calling]] — sibling pattern
- external: [OpenAI Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs) · [Anthropic JSON mode](https://docs.anthropic.com/en/docs/build-with-claude/tool-use) · [Pydantic](https://docs.pydantic.dev/)

## Decision tree

See `content/06-decision-tree.xml`. Branches by provider availability + schema complexity → {OpenAI response_format, Anthropic tool-use JSON, Gemini structured response, Mistral function-call}.
