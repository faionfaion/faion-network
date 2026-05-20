---
slug: cot-basics
tier: geek
group: ai
domain: llm-integration
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Chain-of-Thought (CoT) prompting instructs an LLM to emit intermediate reasoning steps before producing a final answer.
content_id: "2cbd5a5f22cf4585"
tags: [chain-of-thought, reasoning, prompting, self-consistency, extended-thinking]
---
# Chain-of-Thought Basics

## Summary

**One-sentence:** Chain-of-Thought (CoT) prompting instructs an LLM to emit intermediate reasoning steps before producing a final answer.

**One-paragraph:** Chain-of-Thought (CoT) prompting instructs an LLM to emit intermediate reasoning steps before producing a final answer. Three main variants: zero-shot CoT (append "Let's think step by step." to the user turn), few-shot CoT (provide 2–3 worked reasoning examples), and self-consistency (run N=3–7 parallel paths and vote on the majority answer). For Claude, native extended thinking (budget_tokens) replaces manual CoT when maximum accuracy is required.

## Applies If (ALL must hold)

- Task requires multi-step reasoning: math, logic, code debugging, root cause analysis.
- Agent must explain reasoning to a downstream consumer or auditor.
- Accuracy matters more than latency (self-consistency requires N calls).
- Structured decomposition is needed before calling external tools (plan before act).

## Skip If (ANY kills it)

- Simple lookup or classification tasks — CoT adds tokens with no accuracy gain.
- Latency-critical paths where a single-token answer suffices.
- Tasks whose steps cannot be verified (pure creative generation) — overhead without benefit.
- High-volume pipelines where cost dominates; use zero-shot direct answering instead.

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

- parent skill: `geek/ai/llm-integration/`
