---
slug: guardrails-basics
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: LLM applications face prompt injection, PII leakage, harmful content generation, and topic drift.
content_id: "f22c1a9df438682d"
tags: [guardrails, safety, prompt-injection, pii-detection, content-moderation]
---
# Guardrails Basics

## Summary

**One-sentence:** LLM applications face prompt injection, PII leakage, harmful content generation, and topic drift.

**One-paragraph:** LLM applications face prompt injection, PII leakage, harmful content generation, and topic drift. A single guardrail layer is insufficient — adversarial inputs circumvent any single check. Defense-in-depth with ordered layers (microsecond regex first, 300–800ms LLM classifier last) catches most attacks while minimizing latency impact.

## Applies If (ALL must hold)

- Production user-facing chatbots accepting untrusted input
- Regulated industries (healthcare, finance, legal) with compliance requirements
- Multi-tenant apps where tenant input must not influence another tenant's context
- System prompts contain instructions that must not be extracted via prompt injection
- Content generation pipelines where output quality and format must be validated before delivery

## Skip If (ANY kills it)

- Internal developer tooling with no external users — guardrails add latency and maintenance cost without benefit
- Prototype/PoC stage — implement before production, not before demo
- Red-teaming or security research that explicitly needs adversarial output generation
- Output format validation only (JSON schema) — use structured output mode in the LLM API instead, it's lighter

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
