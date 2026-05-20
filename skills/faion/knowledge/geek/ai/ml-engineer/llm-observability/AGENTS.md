---
slug: llm-observability
tier: geek
group: ai
domain: ml-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: LLM observability is the practice of tracing, monitoring, evaluating, and debugging LLM applications in production.
content_id: "e05478f17cf26fd8"
tags: [llm, observability, tracing, monitoring, evaluation]
---
# LLM Observability and Monitoring

## Summary

**One-sentence:** LLM observability is the practice of tracing, monitoring, evaluating, and debugging LLM applications in production.

**One-paragraph:** LLM observability is the practice of tracing, monitoring, evaluating, and debugging LLM applications in production. Unlike traditional APM, LLM observability focuses on output quality, cost tracking, and prompt effectiveness. Key Challenge: LLM applications are non-deterministic — they don't always behave the same way, making them difficult to debug and optimize without proper observability.

## Applies If (ALL must hold)

- Any production LLM application handling real users — tracing from day 1 prevents blind debugging later.
- Multi-agent pipelines where a single user request fans out across 5+ LLM calls.
- When cost attribution per feature/user/pipeline stage is needed for business decisions.
- After deploying a new prompt version — need to compare quality vs. previous version.
- Detecting quality regressions: hallucination rate increase, response relevance drop.
- Debugging intermittent agent failures that only reproduce in production traffic.

## Skip If (ANY kills it)

- Prototyping phase with fewer than 100 requests/day — overhead isn't justified yet.
- When data privacy rules prohibit sending prompt/response content to third-party SaaS — use self-hosted Langfuse instead.
- Already have comprehensive OTEL tracing — may be redundant; check if existing stack can be extended with LLM spans.

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
