---
slug: prompt-basics
tier: geek
group: ai
domain: llm-integration
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Core prompt engineering patterns: zero-shot, few-shot, chain-of-thought, self-consistency, and ReAct.
content_id: "437abcfa259d9363"
tags: [prompt-engineering, llm-api, templates, few-shot, system-prompts]
---
# Prompt Basics

## Summary

**One-sentence:** Core prompt engineering patterns: zero-shot, few-shot, chain-of-thought, self-consistency, and ReAct.

**One-paragraph:** Core prompt engineering patterns: zero-shot, few-shot, chain-of-thought, self-consistency, and ReAct. The PromptTemplate dataclass encapsulates system prompt, user template with variables, and optional few-shot examples. The core rule: store prompt templates as code constants (not runtime strings) — this enables git diff on prompt changes and catches silent regressions when model versions update.

## Applies If (ALL must hold)

- Any pipeline step requiring consistent, parseable LLM output
- Before investing in fine-tuning — prompt engineering resolves most output consistency issues
- When agent inner-loop outputs are unreliable or hallucinating
- Setting up few-shot examples to teach a model a new output schema
- Encoding role, constraints, and output format into a reusable PromptTemplate

## Skip If (ANY kills it)

- When task complexity genuinely requires multi-step reasoning — use Chain-of-Thought or ReAct instead
- When output schema must be guaranteed — use Structured Outputs with Pydantic
- When token budget is the bottleneck — elaborate system prompts eat context; prefer short system + structured output enforcement

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
