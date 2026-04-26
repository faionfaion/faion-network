# Structured Output Patterns

## Summary

Production patterns for reliable LLM structured extraction: Pydantic schema design, retry with error-message injection, streaming JSON handling, and the StructuredOutputService abstraction. Core rule: keep schemas flat (1–2 nesting levels) — models handle flat schemas with near-zero errors; deeply nested schemas (5+ levels) cause frequent parse failures even in structured output mode.

## Why

Ad-hoc `json.loads()` after LLM calls fails silently on missing fields, wrong types, and validation errors. A service layer with Pydantic validation, typed retry, and structured fallback ensures type safety at every pipeline handoff and prevents bad data from propagating downstream.

## When To Use

- Agent pipelines passing data between steps — structured output prevents parse errors at handoff points
- Extracting information from unstructured text (emails, docs, PDFs) for downstream processing
- Multi-agent coordination where subagent outputs must conform to a contract
- Any agent output feeding into a database, API, or service expecting typed data

## When NOT To Use

- Free-form conversational responses — forcing JSON on chat output degrades quality
- Schema changes frequently — Pydantic + re-generation overhead is unnecessary if shape unknown at design time
- Simple string outputs (yes/no, short answers) — structured output adds token overhead for no gain
- OpenAI Structured Outputs beta unavailable for your model tier — fall back to JSON mode with manual validation

## Content

| File | What's inside |
|------|---------------|
| `content/01-schema-design.xml` | Flat schema rule, Literal enums, Field descriptions, versioning rule |
| `content/02-retry-service.xml` | Retry with error injection, streaming JSON, StructuredOutputService pattern |

## Templates

| File | Purpose |
|------|---------|
| `templates/structured-output-service.py` | StructuredOutputService with retry, parse fallback, and batch_extract |
| `templates/agent-task-schema.py` | Canonical agent pipeline output schema (AgentTaskResult) |
