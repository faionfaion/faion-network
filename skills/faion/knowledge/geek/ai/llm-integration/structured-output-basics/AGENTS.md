---
slug: structured-output-basics
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Patterns for getting LLMs to return consistent, parseable JSON: OpenAI JSON Mode (response_format), OpenAI Structured Outputs (beta.
content_id: "1b2d0be7aa5e0863"
tags: [structured-output, json-parsing, pydantic, data-extraction, schema-validation]
---
# Structured Output Basics

## Summary

**One-sentence:** Patterns for getting LLMs to return consistent, parseable JSON: OpenAI JSON Mode (response_format), OpenAI Structured Outputs (beta.

**One-paragraph:** Patterns for getting LLMs to return consistent, parseable JSON: OpenAI JSON Mode (response_format), OpenAI Structured Outputs (beta.parse with Pydantic), Claude prompt + json.loads + retry loop, and function-based forcing via tool calling. The core rule: define schemas in Pydantic with Field(description=...) on every field — descriptions become part of the JSON Schema and measurably improve model accuracy.

## Applies If (ALL must hold)

- Any agent pipeline step that must pass typed data to a downstream system (DB write, API call, UI render)
- Data extraction from unstructured text (invoices, forms, articles, emails)
- Classification tasks where the output enum must be validated
- When Pydantic models already exist for the domain — reuse them as response schemas
- Replacing regex-based parsing of LLM output with schema-enforced extraction

## Skip If (ANY kills it)

- Simple yes/no or short free-text responses where schema overhead adds latency without value
- Tasks requiring narrative output (copywriting, explanations, debugging commentary)
- When beta.parse is unavailable for the target model — use the function-forcing pattern instead
- When the schema changes frequently at runtime — static Pydantic models are hard to generate dynamically

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

- parent skill: `geek/ai/llm-integration/`
