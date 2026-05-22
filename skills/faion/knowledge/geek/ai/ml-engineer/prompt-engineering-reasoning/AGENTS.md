---
slug: prompt-engineering-reasoning
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Complex tasks — math, multi-step logic, decision analysis, code review — require structured reasoning prompts.
content_id: "a05106ed8085f961"
tags: [chain-of-thought, reasoning, self-consistency, prompt-engineering, cot]
---
# Prompt Engineering — Reasoning Patterns

## Summary

**One-sentence:** Complex tasks — math, multi-step logic, decision analysis, code review — require structured reasoning prompts.

**One-paragraph:** Complex tasks — math, multi-step logic, decision analysis, code review — require structured reasoning prompts. This methodology covers chain-of-thought, self-consistency, critique-and-revise, multi-perspective analysis, and tree-of-thought patterns, with complete templates and when-to-use guidance for each technique.

## Applies If (ALL must hold)

- Math, calculation, or multi-step logic where intermediate steps matter.
- Decision analysis with multiple options and trade-offs.
- Code review or debugging where cause-and-effect reasoning is needed.
- Tasks where you need verifiable, auditable reasoning (legal, medical, financial).
- High-stakes outputs where reliability matters more than latency or cost.

## Skip If (ANY kills it)

- Simple, well-defined tasks — CoT adds tokens and latency without quality gain.
- Latency-sensitive real-time pipelines — CoT scratchpads can double or triple response time.
- Self-consistency in production — multiple samples are expensive; reserve for offline evaluation.
- Tasks where chain-of-thought is already embedded in the model via RLHF (modern instruction-tuned models often reason internally without explicit CoT prompting).

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
