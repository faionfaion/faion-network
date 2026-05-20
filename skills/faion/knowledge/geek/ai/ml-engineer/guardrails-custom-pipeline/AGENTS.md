---
slug: guardrails-custom-pipeline
tier: geek
group: ai
domain: ml-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Custom guardrail implementation gives maximum control and minimum dependency footprint.
content_id: "4a7a9d01bfd6eeae"
tags: [guardrails, pii-detection, prompt-injection, custom-pipeline, fastapi]
---
# Custom LLM Guardrails Pipeline

## Summary

**One-sentence:** Custom guardrail implementation gives maximum control and minimum dependency footprint.

**One-paragraph:** Custom guardrail implementation gives maximum control and minimum dependency footprint. The canonical pattern combines a PIIDetector (regex-based masking), a PromptInjectionDetector (pattern library), a ContentModerator (OpenAI moderation API), and an optional HallucinationDetector (LLM-as-judge) into a GuardrailsPipeline class with process_input() and process_output() methods.

## Applies If (ALL must hold)

- Specific requirements not covered by NeMo or Guardrails AI validators.
- Maximum control over latency with tiered checking (regex first, LLM last).
- Lightweight deployments where framework overhead is not acceptable.
- Existing FastAPI, LangChain, or LlamaIndex applications where guardrails integrate as middleware or runnables.

## Skip If (ANY kills it)

- Complex multi-turn dialog control — NeMo Guardrails Colang DSL is purpose-built for this.
- Teams that need rapid iteration on validators — Guardrails Hub ecosystem is faster to use than building from scratch.

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
