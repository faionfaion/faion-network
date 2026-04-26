# Field Descriptions as Inline Mini-Prompts

**Category:** `so-` (structured output)

## The Rule

Treat every `description=` on a schema field as a TINY prompt the model sees right before it generates that field. Be explicit about format, range, units, edge cases, and forbidden patterns. This is the densest, most surgical place to put steering signal.

## Empirical anchor

PARSE (LLM-driven schema optimization, 2025) showed that **optimizing field descriptions yields 60%+ improvement in extraction accuracy**. Making relationships explicit in descriptions improves complex-reasoning accuracy by up to 40%.

## Why It Works

When a model fills a schema field, it sees the schema serialization as part of the prompt. Each field's description appears just before the field's value position in the autoregressive sequence. The description is, effectively, a per-field micro-instruction.

A short, vague description ("the user's age") leaves the model interpolating from priors. A precise one ("integer years; if you only see month/year DOB, assume day=01 to compute") collapses the variance.

## When To Use

- Always — descriptions cost ~10 tokens each and pay for themselves
- Especially for: ambiguous units (USD vs cents, kg vs lb), formats (ISO-8601), exclusions ("ignore retracted papers"), cardinality bounds
- For fields where you need format compliance > 99%

## When NOT To Use

- When description duplicates enum members verbatim (the enum already constrains decoding)
- When schema is so large that descriptions blow the cold-cache budget — strip them only on cache-warm calls
- When the description would contradict the field name (rename instead)

## What Goes In a Good Description

A description ≈ 1-3 short sentences. Cover up to four:

1. **What** the field represents (semantic meaning)
2. **Format / units / range** if non-obvious
3. **Edge cases** — what to do when the input is missing, ambiguous, or contradictory
4. **Forbidden patterns** — common ways the model mis-fills this field

## Anti-patterns

| Anti-pattern | Fix |
|--------------|-----|
| Empty description | Add at minimum the format/units |
| Description duplicates field name (`age: int = Field(description="age")`) | Drop or expand to format/edge-case info |
| Description asks for reasoning ("explain why...") | Reasoning belongs in its own field; this field is for a value |
| Generic "the X for this object" pattern | Concretize — what *kind* of X, in what *units* |
| Long flowing prose | Tighten to 1-3 sentences; the model parses bullet-style fine |
| Contradictory hints (name says cents, description says dollars) | Reconcile — one source of truth |

## Composition

- + **semantic-field-naming**: name carries the gist, description carries the rules
- + **schema-field-order**: in dependent fields, the description can reference earlier fields by name (e.g., "must be derived from `body` above")
- + **enum constraints**: description complements enum by specifying *when* to choose each value, not duplicating the values

## References

Source 1: [PARSE: LLM Driven Schema Optimization for Reliable Entity Extraction (arxiv 2510.08623)](https://arxiv.org/html/2510.08623v1)
Source 2: [Bad Schemas could break your LLM Structured Outputs — Instructor blog](https://python.useinstructor.com/blog/2024/09/26/bad-schemas-could-break-your-llm-structured-outputs/)

See `templates.md`, `examples.md`, `checklist.md`, `llm-prompts.md`.
