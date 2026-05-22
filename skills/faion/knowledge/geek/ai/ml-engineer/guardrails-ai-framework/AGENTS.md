---
slug: guardrails-ai-framework
tier: geek
group: ai
domain: ml-engineering
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces a Guardrails-AI-wired LLM output pipeline using Pydantic schemas + Hub validators for structured-output enforcement, PII detection, and on-fail reasking.
content_id: "6dc5a13846c17ba1"
complexity: medium
produces: code
est_tokens: 3600
tags: [guardrails-ai, output-validation, pydantic, llm-safety, schema-validation]
---
# Guardrails AI — Validator-Based Output Pipeline

## Summary

**One-sentence:** Produces a Guardrails-AI-wired LLM output pipeline using Pydantic schemas + Hub validators for structured-output enforcement, PII detection, and on-fail reasking.

**One-paragraph:** Produces a Guardrails-AI-wired LLM output pipeline. Guardrails AI runs a validator-based pipeline using Pydantic schemas (or RAIL XML), 50+ pre-built Hub validators (toxic language, PII, regex, semantic similarity), and a code-first API for custom validators. Integrates with OpenAI, Anthropic, and local models. Use when output discipline matters more than model choice and you want a single place to declare invariants.

**Ефективно для:** Бекенд-розробник для structured-output discipline — fixed pipeline з Pydantic + Hub validators + on-fail policy.

## Applies If (ALL must hold)

- LLM output must obey a typed schema (Pydantic / RAIL).
- Need at least one of: PII detection, toxic-language filter, regex match, semantic similarity guard.
- On-fail policy (reask / fix / refrain / filter) is acceptable for the use case.
- Want a single library managing validation + reasking rather than custom code.
- Python stack — Guardrails is Python-first.

## Skip If (ANY kills it)

- Output is free-form prose — no schema to enforce.
- Native provider structured-output (OpenAI / Gemini) suffices and no Hub validators needed.
- Non-Python stack — use provider-native validation.
- Latency budget cannot absorb one extra validation pass.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Output Pydantic schema | py | ML lead |
| On-fail policy | yaml | product |
| Validator selection | list | Hub catalogue |
| LLM provider | string | decision record |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer/llm-decision-framework` | Provider choice. |
| `geek/ai/ml-engineer/llm-observability-stack` | Validator failures traced. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules each with rationale + source. | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + self-check. | ~800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix. | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure: declare-schema → choose-validators → wire-on-fail → run → observe. | ~700 |
| `content/06-decision-tree.xml` | essential | Branch by validator type + on-fail policy. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-pipeline` | haiku | Fill guardrails-pipeline.py from schema + validators. |
| `choose-on-fail` | sonnet | Pick reask vs fix vs refrain vs filter per validator. |
| `debug-reask-loops` | opus | Diagnose infinite reask loops + cost spikes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/guardrails-pipeline.py` | Pipeline with Pydantic schema + Hub validators + on-fail. |
| `templates/custom-validator.py` | Skeleton for a custom validator subclass. |
| `templates/rail-spec.xml` | RAIL XML alternative spec form. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-guardrails-ai-framework.py` | Validate the pipeline config (schema, validators, on-fail). | Pre-merge of every Guardrails pipeline PR. |

## Related

- [[llm-decision-framework]] — provider choice.
- [[llm-observability-stack]] — failure tracing.
- [[claude-api]] — provider-side structured output alternative.

## Decision tree

Decision tree at `content/06-decision-tree.xml` decides per-validator on-fail policy (reask / fix / refrain / filter) and overall pipeline shape.
