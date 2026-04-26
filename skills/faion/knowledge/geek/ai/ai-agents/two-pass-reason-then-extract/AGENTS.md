# Two-Pass: Free-Form Reasoning Then Structured Extraction

## Summary

When raw reasoning quality matters more than output format (math proofs, deep research synthesis, code with subtle constraints), do not lock the strong model into strict JSON during the reasoning step. Run two passes: (1) the strong model reasons in free text or extended-thinking mode, (2) a cheap small model extracts the answer into the strict schema. The format constraint never interferes with the reasoning trace, and the strict typing still lands on the consumer.

## Why

Forcing strict JSON during reasoning measurably hurts accuracy on hard tasks — the SLOT paper (arXiv 2505.04016) and the BuildMVPFast 2026 guide both report 10–15 percent drops on math and complex analysis benchmarks when the same prompt is run with strict structured output versus free text. The grammar mask burns probability on schema-conforming tokens that are not the reasoning the model would otherwise produce. Splitting the work — Opus thinks freely, Haiku extracts — recovers the lost accuracy at near-zero extraction cost (the extraction prompt is short and the schema is small, so caching plus a Haiku-class model is cheap).

## When To Use

- Math word problems, proofs, multi-step calculations.
- Research synthesis where the answer is a few fields but the analysis is paragraphs.
- Code generation that needs deep reasoning before a structured diff/patch.
- Legal or medical analysis where the verdict structure is rigid but the reasoning must be unconstrained.
- Anything where Opus extended thinking is justified by the task difficulty.

## When NOT To Use

- Simple extraction (entities, key/value, sentiment) — single-pass strict SO is faster and cheaper.
- Latency-critical paths under ~1 second total — two model calls always cost more wall-clock than one.
- Tasks small enough that Haiku-class extraction quality is the bottleneck — extract directly with the strong model.
- High call volume where the doubled provider cost exceeds the accuracy gain.

## Content

| File | What's inside |
|------|---------------|
| `content/01-rule.xml` | Core rule, two-pass mechanism, Opus + Haiku worked example. |
| `content/02-cost-model.xml` | When the cost math favors two-pass vs single-pass; cache placement and extraction prompt sizing. |

## Templates

| File | Purpose |
|------|---------|
| `templates/two_pass.py` | Reusable Opus-think-then-Haiku-extract function with strict Pydantic verdict schema. |
