# Generator-Critic Loop with Hard Cap and Delta Exit

## Summary

Wrap any open-ended generation node (write, code, summarize) in a Generator → Critic → Generator loop. The critic returns both a structured `score` and a `should_continue: bool`. Exit on three conditions, in order: `should_continue=False`, score plateau (delta < epsilon for 2 consecutive iterations), or a hard cap of 3 iterations. Use a smaller/cheaper model as the critic when the criterion is rubric-shaped (style, format, completeness); use the same-tier model only when the critique requires correctness reasoning (code, math).

## Summary mechanics

The second iteration captures most of the quality gain; the fifth wastes tokens. A hard cap plus a delta-based stop curve maximizes the quality/cost ratio.

## Why

Reflection-style loops add real quality on open-ended tasks (writing, codegen, structured extraction with rubrics) — but unbounded reflection is the most common cost trap in production agent stacks. Empirically (Reflection Agents, langchain.com/blog), iteration 2 captures roughly 70-80% of the achievable lift, iteration 3 adds 10-15%, and iterations 4+ contribute below the noise floor. A hard cap of 3 plus an explicit `should_continue` flag from the critic gives bounded latency and an auditable stopping criterion. Cheap-critic-on-rubric is justified by the same data: rubric scoring is a constrained classification task, not free-form reasoning.

## When To Use

- Codegen agents that compile/lint/test their own output before returning.
- Copywriting / summarization with a clear rubric (length, voice, audience).
- Structured extraction where a critic verifies all required fields are populated and citations exist.
- Self-correcting RAG: critic checks each answer against retrieved chunks before the answer ships.

## When NOT To Use

- Latency-critical paths (chat completions visible to a user) — the second pass doubles wall time.
- Tool-calling agents where ground truth comes from the tool result, not a critic — adding a critic creates two truths and confusion.
- Trivial outputs that consistently pass on iteration 1 — measure the actual lift; if iteration 2 changes <2% of cases, kill the loop.

## Content

| File | What's inside |
|------|---------------|
| `content/01-loop-shape.xml` | Loop topology, exit conditions, critic-model sizing. |

## Templates

| File | Purpose |
|------|---------|
| `templates/critic_schema.py` | Pydantic schema for critic output (`score`, `should_continue`, `feedback`). |
| `templates/loop.py` | Reference loop with hard cap, delta exit, structured-output critic. |
