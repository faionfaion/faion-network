# Embedded Scratchpad Field

**Category:** `so-` (structured output)

## The Rule

Before any non-trivial answer field, embed a `scratchpad`, `plan_steps`, or `reasoning` field IN the schema. The model writes its working notes there before generating the answer. This is structured-output's equivalent of `<thinking>` tags but works even in strict JSON mode where free-form preambles aren't allowed.

## Why It Works

In strict JSON mode the model can ONLY emit valid JSON — there's no room for "let me think out loud first." Without a scratchpad field, the model has to commit to the answer immediately. With one, you give it permission to reason where it would otherwise have to skip reasoning.

This composes with `schema-field-order`: the scratchpad goes FIRST, the answer LAST.

## Empirical Anchor

AWS Bedrock guidance reports a +60% accuracy improvement on GSM8k math benchmark from adding a single `reasoning` field before `answer`. Tab-CoT (Tabular Chain-of-Thought) papers show similar gains on multi-criteria decisions.

## Variants

| Field name | Best for |
|------------|----------|
| `reasoning` | One-shot decisions; ambiguous extraction |
| `plan_steps: list[str]` | Multi-step tasks; complex transformations |
| `evidence: list[str]` | Verdict / classification — quotations grounding the call |
| `scratchpad: str` | Free-form thinking before structured fields |
| `tab_cot: list[Step]` where Step has `step: str, intermediate_result: str` | Math, derivation, calculation chains |

## When To Use

- Strict JSON mode (no free-form preamble allowed)
- Decisions that benefit from CoT but where you also need structured output
- Tasks with > 1 reasoning step
- Anywhere "the model commits before thinking" is a known failure mode

## When NOT To Use

- Pure transformation tasks where reasoning adds latency without accuracy
- When the upstream model is already a reasoning model (o-series, Opus thinking) — paying twice
- For trivial fields where the schema is already forcing the model through an enum

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| `scratchpad` placed AFTER the answer | Reverse order — scratchpad must come BEFORE the answer to act as CoT |
| `reasoning` field with vague description | Description should say "Step-by-step analysis of evidence" — concrete |
| Multiple scratchpad fields competing | Pick one (or one per phase); stacking confuses |
| Scratchpad that just echoes the input | Description must demand actual analysis, not paraphrase |
| Scratchpad max_tokens cap too small | Let it breathe; ~200-500 tokens for non-trivial reasoning |

## Composition

- + **schema-field-order**: scratchpad first, answer last
- + **field-descriptions-as-prompts**: scratchpad description tells the model what to think about
- + **plan-execute-vs-react**: in Plan-Execute, scratchpad lives in the plan-output schema; ReAct uses Thought messages instead

## References

- [AWS Bedrock JSON Schema Structured Output Guide (Feb 2026)](https://explore.n1n.ai/blog/aws-bedrock-json-schema-structured-output-guide-2026-02-16)
- [Tab-CoT: Tabular Chain-of-Thought (paper)](https://arxiv.org/abs/2305.17812)
- [OpenAI structured outputs guide](https://platform.openai.com/docs/guides/structured-outputs)

See `templates.md`, `examples.md`, `checklist.md`, `llm-prompts.md`.
