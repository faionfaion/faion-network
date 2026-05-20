---
slug: ollama-prompt-engineering
tier: geek
group: ai
domain: ml-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Local Ollama models require careful prompt engineering to match cloud model quality.
content_id: "f3417ab7420c8b22"
tags: [ollama, prompt-engineering, system-prompts, local-llm]
---
# Ollama Prompt Engineering

## Summary

**One-sentence:** Local Ollama models require careful prompt engineering to match cloud model quality.

**One-paragraph:** Local Ollama models require careful prompt engineering to match cloud model quality. This methodology covers system prompts for common roles, task-specific templates (summarization, extraction, classification, code generation), temperature settings per task type, context window management strategies, and chain-of-thought patterns for local models.

## Applies If (ALL must hold)

- Designing prompts for local Ollama deployments where output quality needs to match cloud models.
- Building prompt templates for NLP pipelines (extraction, classification, summarization).
- Optimizing temperature and context settings for specific task types.
- Implementing multi-turn conversation management with local models.

## Skip If (ANY kills it)

- Cloud model prompt engineering — technique overlap is high but cloud models tolerate vaguer prompts; over-constraining cloud models can reduce quality.
- Fine-tuning use cases — prompt engineering is a complement to fine-tuning, not a substitute when specialized behavior is required.

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
