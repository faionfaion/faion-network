---
slug: guardrails-concepts
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Guardrails (or "rails") are specific mechanisms for controlling LLM behavior.
content_id: "54accd58c30beb31"
tags: [guardrails, llm-safety, content-moderation, prompt-injection, pii]
---
# LLM Guardrails — Concepts, Types, and Architecture

## Summary

**One-sentence:** Guardrails (or "rails") are specific mechanisms for controlling LLM behavior.

**One-paragraph:** Guardrails (or "rails") are specific mechanisms for controlling LLM behavior. They transform unpredictable generative models into reliable, safe, and compliant systems by preventing harmful content, enforcing topic boundaries, validating output format and structure, detecting prompt injection attacks, filtering PII and sensitive data, and reducing hallucinations.

## Applies If (ALL must hold)

- Any customer-facing LLM application where uncontrolled output could harm users or expose the business to liability.
- Regulated domains: healthcare, finance, legal — where hallucinations or off-topic responses have compliance consequences.
- Agent pipelines that execute tool calls or write to external systems — execution rails prevent unauthorized actions.
- Multi-turn conversations where topic drift or persona breaking is a risk.
- Applications handling PII — input/output rails must mask before logging and processing.

## Skip If (ANY kills it)

- Internal developer tooling where trust is high and false positives waste time.
- Latency-critical paths under 50ms budget — LLM-as-judge guardrails add 500ms+ and break the budget.
- Guardrails add no value if the base model already refuses the content class (e.g., Claude refusing CSAM).
- Prototyping and local experimentation — premature guardrails slow iteration.

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
