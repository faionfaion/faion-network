---
slug: generator-critic-bounded-loop
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Wrap generation in Generator → Critic → Generator loop with hard cap of 3 iterations.
content_id: "1f33af6a2872899c"
tags: [agents, reflection, bounded-loops, self-correction, cost-optimization]
---
# Generator-Critic Loop with Hard Cap and Delta Exit

## Summary

**One-sentence:** Wrap generation in Generator → Critic → Generator loop with hard cap of 3 iterations.

**One-paragraph:** Wrap generation in Generator → Critic → Generator loop with hard cap of 3 iterations. Exit on critic veto, plateau, or cap. Use cheap models for rubric criticism.

## Applies If (ALL must hold)

- Codegen agents that compile/lint/test their own output before returning.
- Copywriting / summarization with a clear rubric (length, voice, audience).
- Structured extraction where a critic verifies all required fields are populated and citations exist.
- Self-correcting RAG: critic checks each answer against retrieved chunks before the answer ships.

## Skip If (ANY kills it)

- Latency-critical paths (chat completions visible to a user) — the second pass doubles wall time.
- Tool-calling agents where ground truth comes from the tool result, not a critic — adding a critic creates two truths and confusion.
- Trivial outputs that consistently pass on iteration 1 — measure the actual lift; if iteration 2 changes less than 2% of cases, kill the loop.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `geek/ai/ai-agents/`
