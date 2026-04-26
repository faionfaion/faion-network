# Refusal Field for Safety-Aware Strict Extraction

## Summary

Add an explicit nullable `refusal: str | None` field at the TOP of every strict-mode SO schema in safety-sensitive domains. When the model declines to answer, it writes the explanation into `refusal` and leaves payload fields null — instead of corrupting the JSON with a free-form refusal that breaks parsing. OpenAI's strict-mode response already exposes a top-level `refusal`; mirroring that field inside your own schema unifies the contract across providers and lets a single downstream branch handle "I cannot answer" without try/except.

## Why

Strict mode compiles the schema into a finite-state grammar; when the model refuses, it must still emit JSON that satisfies the grammar — otherwise the parser throws and downstream branches see a generic exception instead of a refusal signal. OpenAI's August 2024 SO release introduced a top-level `refusal` string for exactly this reason. Reproducing it inside your schema (a) gives you the refusal text on Anthropic and local backends that don't surface a top-level field, (b) keeps the rest of the schema null-safe under a refusal, (c) replaces brittle "try parse, on fail check for refusal text" code paths with a single `if response.refusal:` branch.

## When To Use

- PII / medical / legal / financial extraction with strict mode
- Content moderation outputs where "this content is abusive, refusing to score" must not throw
- Any pipeline that bills only on success and needs to log refusals separately from errors
- Multi-provider deployments where refusal handling must be uniform across OpenAI/Anthropic/local
- Long batch jobs where one item refusing must not abort the batch

## When NOT To Use

- Trivial transformations (uppercase, regex extract) where refusal is not in the model's repertoire
- Pipelines where any refusal is upstream policy violation and should hard-fail anyway
- When the only consumer is a human reviewer who already reads free-form responses

## Content

| File | What's inside |
|------|---------------|
| `content/01-rule.xml` | The refusal-field rule, OpenAI native vs schema-mirrored variants, branch handler pattern. |

## Templates

| File | Purpose |
|------|---------|
| `templates/refusal_schema.py` | Pydantic model with `refusal` first and all payload fields nullable. |

## References

- [OpenAI — Introducing Structured Outputs in the API](https://openai.com/index/introducing-structured-outputs-in-the-api/)
- [OpenAI structured outputs guide — refusal field](https://developers.openai.com/api/docs/guides/structured-outputs)
