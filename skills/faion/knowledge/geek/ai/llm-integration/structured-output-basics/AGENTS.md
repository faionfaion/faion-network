# Structured Output Basics

## Summary

Patterns for getting LLMs to return consistent, parseable JSON: OpenAI JSON Mode (`response_format`), OpenAI Structured Outputs (`beta.parse` with Pydantic), Claude prompt + `json.loads` + retry loop, and function-based forcing via tool calling. The core rule: define schemas in Pydantic with `Field(description=...)` on every field — descriptions become part of the JSON Schema and measurably improve model accuracy.

## Why

LLM outputs integrated into applications and APIs must be parseable. JSON Mode guarantees valid JSON but not schema compliance — production pipelines break when required fields are absent or typed wrong. OpenAI Structured Outputs (`beta.parse`) gives schema-level guarantees for gpt-4o; Claude requires a prompt + retry loop. Without Pydantic and `Field` descriptions, the model guesses field semantics and produces semantically invalid data even when JSON is structurally valid.

## When To Use

- Any agent pipeline step that must pass typed data to a downstream system (DB write, API call, UI render)
- Data extraction from unstructured text (invoices, forms, articles, emails)
- Classification tasks where the output enum must be validated
- When Pydantic models already exist for the domain — reuse them as response schemas
- Replacing regex-based parsing of LLM output with schema-enforced extraction

## When NOT To Use

- Simple yes/no or short free-text responses where schema overhead adds latency without value
- Tasks requiring narrative output (copywriting, explanations, debugging commentary)
- When `beta.parse` is unavailable for the target model — use the function-forcing pattern instead
- When the schema changes frequently at runtime — static Pydantic models are hard to generate dynamically

## Content

| File | What's inside |
|------|---------------|
| `content/01-json-modes.xml` | OpenAI JSON Mode vs Structured Outputs comparison, method selection table, provider limitations |
| `content/02-openai-structured.xml` | `beta.parse` with Pydantic BaseModel, Entity/ExtractionResult example, accessing `.parsed` |
| `content/03-claude-json.xml` | Claude prompt + markdown-fence stripping + `json.loads` + retry loop pattern |
| `content/04-complex-schemas.xml` | Task extraction with subtasks, form/invoice extraction, Pydantic enums and validators |

## Templates

| File | Purpose |
|------|---------|
| `templates/extraction-schema.py` | Pydantic models for entity extraction and invoice parsing with Field descriptions |
| `templates/claude-extract.py` | Claude structured extraction with retry loop and markdown-fence stripping |
