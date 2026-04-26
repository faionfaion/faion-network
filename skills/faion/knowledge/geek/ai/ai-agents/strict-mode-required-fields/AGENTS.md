# Strict-Mode Schemas: Required-Everything + No Additional Properties

## Summary

OpenAI/Azure strict-mode structured outputs (`response_format.json_schema.strict: true`) compile each schema into a finite-state grammar. The grammar refuses any schema where some properties are `required` and others are merely declared, or where the object accepts unknown keys. The rule: every property defined on an object must be listed in `required`, and every object must set `additionalProperties: false`. Optional fields are simulated by making the type nullable (`T | None`), not by omitting them from `required`.

## Why

Strict mode trades flexibility for guaranteed validity. Internally, the schema is converted into a regular grammar; an "optional" key would create non-determinism in the FSM (do we expect this token next or skip to the closing brace?), so the compiler rejects it. The same constraint applies to additional properties — without `additionalProperties: false`, the grammar would have to allow arbitrary key/value tokens at every object boundary, which collapses guarantees. Pydantic's `Optional[X]` translates correctly only when the bridge (`openai-python`, Instructor, `pydantic-ai`) emits `{"type": ["X", "null"]}` AND keeps the field in `required`. Teams hit this every time they migrate a "loose" Pydantic model to strict mode and get `400: schema additionalProperties must be false when strict is true`.

## Why Now (April 2026)

Anthropic's tool-use input schemas, Azure's `parse` API, and Google's Gemini `responseSchema` with `strict` mode all enforce the same constraint. A model that ships in 2026 without this rule will fail in production the first time it touches strict mode.

## When To Use

- Any call against the OpenAI Responses API or Chat Completions with `response_format: {type: "json_schema", strict: true}`.
- Anthropic tool-use where the tool input must be exhaustively typed (`additionalProperties: false` keeps the model from inventing parameters).
- Azure OpenAI strict mode and Google Gemini `responseSchema` with strict enforcement.
- Generating JSON-Schema artifacts to ship to a third-party that runs the same compiler (Outlines / XGrammar with strict-grammar mode).

## When NOT To Use

- Local Outlines or XGrammar pipelines that support standard JSON-Schema optional fields natively — required-everything wastes tokens for no grammar gain.
- Loose JSON mode (`response_format: {type: "json_object"}`) — there is no grammar, so the constraint does not apply (and you also do not get format guarantees).
- Schemas that intentionally accept open-ended additional properties (e.g., a metadata bag for arbitrary user keys) — strict mode is the wrong tool; either drop strict or split the bag into a typed sub-object plus a separate audit field.

## Content

| File | What's inside |
|------|---------------|
| `content/01-strict-mode-rule.xml` | The rule, the FSM rationale, good/bad Pydantic + JSON-Schema examples. |
| `content/02-nullable-vs-optional.xml` | Why `Optional[X]` and `T \| None` are NOT the same in strict mode; the correct nullable encoding. |

## Templates

| File | Purpose |
|------|---------|
| `templates/strict_pydantic.py` | Pydantic model with `extra="forbid"` and nullable fields ready for strict mode. |
| `templates/strict.schema.json` | Equivalent JSON Schema that passes the OpenAI strict-mode compiler. |
