# Structured Output for LLMs

## Summary

Structured output ensures LLMs return data in consistent, parseable formats (JSON matching a schema). Define output schemas as Pydantic models. For OpenAI: use `client.beta.chat.completions.parse()` (native structured output). For Claude: use tool-calling via `instructor` library. For local models: use `outlines` for token-level grammar constraints. Never use raw JSON mode — it guarantees valid JSON syntax but NOT schema compliance.

## Why

Unstructured LLM output cannot be reliably parsed — models add prose, omit fields, or use wrong types. Typed contracts at agent boundaries prevent silent data corruption. Without structured output, every downstream consumer needs brittle regex-based parsing that fails on format variations. Pydantic models generate JSON Schema automatically and provide IDE autocompletion, validation, and retry-on-failure.

## When To Use

- Agent tool calls return typed data consumed by downstream code
- Extracting structured records from unstructured documents (invoices, forms, emails)
- Building pipelines where each stage's input is the previous stage's validated output
- Any place where a parsing failure would silently corrupt downstream state
- Multi-model workflows where one model's output feeds into another model's prompt

## When NOT To Use

- Free-form creative generation where schema over-constrains the response
- Exploratory research where the output structure is unknown in advance
- Very long outputs (&gt;2K tokens) with complex nested schemas — reliability degrades
- Streaming responses where structured output cannot be validated until complete

## Content

| File | What's inside |
|------|---------------|
| `content/01-methods.xml` | Provider comparison (OpenAI, Claude, Gemini, local); JSON mode vs structured output; Pydantic integration |
| `content/02-rules.xml` | Schema design rules, validation retry, failure modes, production gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/entity-extraction.py` | Entity extraction Pydantic schema (Entity, EntityExtractionResult) |
| `templates/safe-parse.py` | Safe extraction with markdown stripping and retry logic |
