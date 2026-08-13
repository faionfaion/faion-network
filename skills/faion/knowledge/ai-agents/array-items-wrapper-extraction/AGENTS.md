# Array Items Wrapper for Extraction

## Summary

**One-sentence:** Wraps variable-cardinality structured-output extraction in a typed envelope `{items[], total_found, truncated}` so strict-mode validators accept it and zero/one/many cases stay isomorphic.

**One-paragraph:** Strict-mode JSON Schema (OpenAI, Azure) rejects top-level arrays because `additionalProperties` is object-only. Even on lenient providers, a bare list collapses zero / one / many into incompatible shapes (`[]`, `null`, single dict, single-item list). This methodology wraps any extraction with `{items: [...], total_found: int, truncated: bool}` and adds the implementation guidance — JSON Schema, Pydantic model, and a few-shot prompt note that produces the wrapper consistently.

**Ефективно для:** Команд, де model іноді повертає `null`, іноді `[]`, іноді `[ent]`, іноді одиничний dict — і парсер падає на edge-кейсі через 2 тижні; envelope усуває весь клас багів за один schema-rewrite.

## Applies If (ALL must hold)

- Extraction has variable cardinality (entities, citations, line items, search hits).
- Output is consumed by deterministic parser (not free-form prose).
- Strict-mode SO is desired or required.
- Total count and truncation diagnostics are useful downstream.
- Streaming UI is not required (envelope blocks streaming until close).

## Skip If (ANY kills it)

- Hard-coded N (exactly 3 suggestions) — use a fixed-length tuple type.
- Single-entity extraction — wrap is overhead.
- Streaming UI that renders items as they arrive.
- Provider does not support strict-mode AND robust try/except handles legacy shapes.

## Prerequisites

| Artifact | Format | Source |
|---|---|---|
| Entity schema | JSON Schema or Pydantic model | Domain owner |
| Provider + SO mode | string (OpenAI strict, Anthropic tool, etc.) | Eng |
| Expected cardinality range | min, typical, max | Domain owner |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents/strict-mode-required-fields/AGENTS.md` | Strict-mode requirements anchor the wrapper rules. |
| `geek/ai/ai-agents/enum-constraints-closed-vocabularies/AGENTS.md` | Related pattern for closed-vocabulary fields. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 3 rules: top-level object, metadata fields, total_found honest | ~700 |
| `content/02-output-contract.xml` | essential | JSON Schema for the envelope | ~600 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns | ~700 |
| `content/06-decision-tree.xml` | essential | Tree: variable-card? → strict-mode? → wrap or stream | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `generate_envelope_schema` | haiku | Mechanical schema transformation. |
| `verify_against_strict_mode` | sonnet | Per-provider strict-mode rules. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the envelope. |
| `templates/output.example.json` | Filled example. |
| `templates/items_wrapper.py` | Python (Pydantic) skeleton for the envelope. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Validate that an output instance matches the envelope. | Per inference call. |

## Related

- parent skill: `geek/ai/ai-agents/`
- peer: [[strict-mode-required-fields]] — strict-mode requires this pattern.
- peer: [[enum-constraints-closed-vocabularies]] — combine for fully-typed extraction.

## Decision tree

See `content/06-decision-tree.xml`. Asks: (1) is cardinality variable? (2) is strict-mode required? (3) does a streaming UI need partial items? Leaves point to "wrap", "use streaming top-level", or "fixed-length tuple".

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/output-schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.net/schemas/array-items-wrapper-extraction/output.json",
  "title": "Array Items Wrapper Extraction Output",
  "description": "purpose=schema; consumes=brief+context; produces=artefact; depends-on=01-core-rules.xml; token-budget-impact=low",
  "type": "object",
  "required": [
    "artefact_id",
    "owner",
    "version",
    "version_stamp",
    "produced_at",
    "rationale",
    "inputs_used"
  ],
  "properties": {
    "artefact_id": {
      "type": "string",
      "minLength": 3
    },
    "owner": {
      "type": "string",
      "minLength": 1
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "version_stamp": {
      "type": "string"
    },
    "produced_at": {
      "type": "string",
      "format": "date-time"
    },
    "fields": {
      "type": "object"
    },
    "rationale": {
      "type": "string",
      "minLength": 20
    },
    "inputs_used": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "minItems": 1
    }
  }
}
```

### `templates/output.example.json`

```json
{
  "artefact_id": "array-items-wrapper-extraction-example-001",
  "owner": "alex@faion.net",
  "version": "1.0.0",
  "version_stamp": "array-items-wrapper-extraction@1.0.0",
  "produced_at": "2026-05-22T12:00:00Z",
  "fields": {
    "placeholder_field": "filled-by-author"
  },
  "rationale": "Example output for Array Items Wrapper Extraction; references at least one named input.",
  "inputs_used": [
    "docs/brief.md"
  ]
}
```

### `templates/items_wrapper.py`

```python
"""Batch-extraction schema with the items wrapper.

The wrapper is mandatory under OpenAI/Azure strict mode (which forbids
top-level arrays) and recommended on every other provider for consistent
zero/one/many parsing.
"""

from pydantic import BaseModel, Field


class Entity(BaseModel):
    """One extracted entity. Replace with your domain shape."""

    name: str = Field(description="Surface form of the entity as it appears in the source.")
    kind: str = Field(description="Entity kind, e.g. 'person', 'org', 'product'.")
    span_start: int = Field(ge=0, description="Inclusive character offset in the source.")
    span_end: int = Field(ge=0, description="Exclusive character offset in the source.")


class EntityList(BaseModel):
    """Top-level extraction result.

    items is the actual list; total_found and truncated expose diagnostics
    the consumer can use without recomputing.
    """

    model_config = {"extra": "forbid"}

    total_found: int = Field(
        ge=0,
        description="Count of entities found. 0 if none. Must equal len(items) unless truncated.",
    )
    truncated: bool = Field(
        description="True if more entities exist beyond the per-call limit and were dropped.",
    )
    items: list[Entity] = Field(
        description="Entities in order of appearance. May be empty.",
    )

    def is_empty(self) -> bool:
        return self.total_found == 0
```
