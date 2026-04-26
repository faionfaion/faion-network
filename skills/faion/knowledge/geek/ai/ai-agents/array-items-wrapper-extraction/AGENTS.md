# Array Items Wrapper for Extraction

## Summary

When extracting N entities from a document, never make the top-level structured-output response a bare array. Always wrap with `{items: [...]}` plus metadata fields like `total_found` and `truncated`. Strict-mode validators reject top-level arrays because schema-level controls like `additionalProperties` are object-only; wrapping standardises the shape across zero/one/many cases and lets you add count and truncation diagnostics without reshaping consumers.

## Why

OpenAI strict mode and Azure structured outputs require the top-level schema to be an object — bare arrays are not allowed. Even on providers that permit it, asking the model for `list[Entity]` collapses three cases (zero, one, many) into shapes that downstream parsers handle inconsistently: zero entities sometimes returns `[]`, sometimes `null`, sometimes a single dict; a single entity sometimes returns `[ent]`, sometimes `ent`. Wrapping in `{items: [...], total_found, truncated}` removes the ambiguity, lets the model report "I found 0" or "I truncated at 50" explicitly, and keeps the consumer code single-shape. Simon Willison's `--schema-multi` pattern in `llm` formalises the same wrapper for batch extraction CLIs.

## When To Use

- Any extraction with variable cardinality (entities, citations, line items, search hits).
- Document-level summarisation that yields a list of facts/claims.
- Batch classification where N inputs map to N outputs.
- Any strict-mode SO call (OpenAI, Azure) — the top-level array is forbidden there anyway.

## When NOT To Use

- Hard-coded N (always exactly 3 suggestions) — use a fixed-length tuple type or named fields instead.
- Single-entity extraction with no list semantics — wrap is overhead for a one-shot field.
- Streaming UIs that render items as they arrive — items at top level can stream natively; wrap blocks streaming until the wrapper closes.

## Content

| File | What's inside |
|------|---------------|
| `content/01-rule.xml` | Core rule, wrapper shape, zero/one/many failure modes, strict-mode requirement. |

## Templates

| File | Purpose |
|------|---------|
| `templates/items_wrapper.py` | Pydantic batch-entity-extraction schema with items + total_found + truncated. |
