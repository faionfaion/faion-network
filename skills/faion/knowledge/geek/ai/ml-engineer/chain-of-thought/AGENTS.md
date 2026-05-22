---
slug: chain-of-thought
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: CoT prompting elicits intermediate reasoning steps before final answers, improving accuracy on multi-step problems by up to 18% (GSM8K) or 70% (with Tree-of-Thoughts).
content_id: "0e37f56d7df41e44"
tags: [chain-of-thought, prompting, reasoning, extended-thinking, llm]
---
# Chain-of-Thought Prompting

## Summary

**One-sentence:** CoT prompting elicits intermediate reasoning steps before final answers, improving accuracy on multi-step problems by up to 18% (GSM8K) or 70% (with Tree-of-Thoughts).

**One-paragraph:** CoT prompting elicits intermediate reasoning steps before final answers, improving accuracy on multi-step problems by up to 18% (GSM8K) or 70% (with Tree-of-Thoughts). For modern models, use zero-shot CoT. Use few-shot only for format enforcement, not reasoning quality. For Claude, use `<thinking>` XML tags or Extended Thinking (Opus). Do NOT add explicit CoT to reasoning models (o1, o3, DeepSeek-R1) as they have it built in. Research shows for strong models, zero-shot CoT matches few-shot CoT — few-shot examples primarily enforce output format rather than improving reasoning quality.

## Applies If (ALL must hold)

- Task requires multi-step reasoning: math, logic puzzles, code debugging, complex decisions
- LLM makes errors on a task it should theoretically solve — CoT surfaces where reasoning breaks
- Output needs to be auditable: visible steps allow reviewers to verify the reasoning path
- Agent must plan a sequence of actions before executing — CoT as a scratchpad before tool calls
- High-stakes single response where Self-Consistency (5 samples + majority vote) is justified

## Skip If (ANY kills it)

- Simple classification, extraction, or translation — CoT adds tokens with no quality gain
- Latency is critical (<1s) — CoT adds tokens and turns
- Using o1/o3/o4-mini/DeepSeek-R1 — built-in reasoning; explicit CoT interferes
- High-volume, low-complexity pipelines — 2-5x token overhead multiplies at scale

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

- parent skill: `geek/ai/ml-engineer/`
