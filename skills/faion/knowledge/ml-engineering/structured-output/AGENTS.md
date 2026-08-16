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

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-structured-output.py` | Lint structured-output config | Pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[tool-use-function-calling]] — sibling pattern
- external: [OpenAI Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs) · [Anthropic JSON mode](https://docs.anthropic.com/en/docs/build-with-claude/tool-use) · [Pydantic](https://docs.pydantic.dev/)

## Decision tree

See `content/06-decision-tree.xml`. Branches by provider availability + schema complexity → {OpenAI response_format, Anthropic tool-use JSON, Gemini structured response, Mistral function-call}.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/entity-extraction.py`

```python
"""
Entity extraction Pydantic schema.
Works with OpenAI native structured output and instructor (Claude/others).
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class EntityType(str, Enum):
    PERSON = "person"
    ORGANIZATION = "organization"
    LOCATION = "location"
    DATE = "date"
    MONEY = "money"
    PRODUCT = "product"
    EVENT = "event"
    CONCEPT = "concept"


class Entity(BaseModel):
    text: str = Field(description="Entity text as it appears in source")
    type: EntityType = Field(description="Entity category")
    normalized: Optional[str] = Field(default=None, description="Canonical form")
    confidence: float = Field(ge=0, le=1, default=1.0, description="Extraction confidence")
    raw_quote: str = Field(description="Verbatim quote from source that supports this entity")


class EntityExtractionResult(BaseModel):
    entities: List[Entity] = Field(description="All extracted entities")
    summary: str = Field(description="One-sentence summary of the source text")
    language: str = Field(default="en", description="Detected language (ISO 639-1)")
```

### `templates/safe-parse.py`

````python
"""
Safe structured output extraction: strips markdown fences, validates, retries with error context.
Use when not using instructor's automatic retry (e.g., with prompt-based JSON output).
"""
import json
import re
from pydantic import BaseModel, ValidationError
from typing import TypeVar, Type

T = TypeVar("T", bound=BaseModel)


def safe_parse(raw: str, model: Type[T], retries: int = 3) -> T:
    """
    Strip markdown fences and validate JSON against a Pydantic model.
    Raises RuntimeError after all retries are exhausted.
    """
    content = raw.strip()
    # Strip ```json ... ``` or ``` ... ``` wrappers
    content = re.sub(r"^```(?:json)?\s*", "", content)
    content = re.sub(r"\s*```$", "", content)
    for attempt in range(retries):
        try:
            return model.model_validate_json(content)
        except (json.JSONDecodeError, ValidationError) as e:
            if attempt == retries - 1:
                raise RuntimeError(
                    f"Structured output parse failed after {retries} attempts: {e}\n"
                    f"Raw output: {raw[:500]}"
                ) from e
    raise RuntimeError("unreachable")


def extract_with_retry(prompt: str, model_class: Type[T], llm_fn, max_retries: int = 3) -> T:
    """
    Call llm_fn(prompt) and parse with retry.
    On failure, inject the validation error into the next prompt.
    """
    current_prompt = prompt
    for attempt in range(max_retries):
        raw = llm_fn(current_prompt)
        try:
            return safe_parse(raw, model_class)
        except RuntimeError as e:
            if attempt == max_retries - 1:
                raise
            current_prompt = f"{prompt}\n\nPrevious attempt failed validation:\n{e}\n\nPlease correct and try again."
    raise RuntimeError("unreachable")
````

### `templates/structured-output.schema.yaml`

```yaml
$schema: "http://json-schema.org/draft-07/schema#"
type: object
required: [provider, mode, model_name, schema_ref, repair_strategy, log_raw_on_failure]
properties:
  provider: { type: string, enum: [openai, anthropic, gemini, mistral, cohere] }
  mode: { type: string, enum: [response_format, tool_use_json, schema_response, function_call] }
  model_name: { type: string, minLength: 3 }
  schema_ref: { type: string, minLength: 3 }
  repair_strategy: { type: string, enum: [once, none] }
  log_raw_on_failure: { type: boolean }
```

### `templates/_smoke-test.yaml`

```yaml
provider: openai
mode: response_format
model_name: gpt-4o-2024-08-06
schema_ref: schemas/SupportTicket.json
repair_strategy: once
log_raw_on_failure: true
```
