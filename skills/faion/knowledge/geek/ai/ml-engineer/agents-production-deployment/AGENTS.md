---
slug: agents-production-deployment
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Production autonomous agents require five production-grade components beyond the core loop: (1) a typed tool base class with a shared registry, (2) YAML configuration with env-var substitution, (3) structured JSON logging for every LLM and tool call, (4) exponential backoff retry with circuit breaker for external services, (5) a repeatable evaluation harness that measures success rate, latency, iterations, and token cost.
content_id: "6b7c79757cf6cfa5"
tags: [agents, production, deployment, logging, evaluation]
---
# Agent Production Deployment — Tool Design, Logging, Evaluation, Docker

## Summary

**One-sentence:** Production autonomous agents require five production-grade components beyond the core loop: (1) a typed tool base class with a shared registry, (2) YAML configuration with env-var substitution, (3) structured JSON logging for every LLM and tool call, (4) exponential backoff retry with circuit breaker for external services, (5) a repeatable evaluation harness that measures success rate, latency, iterations, and token cost.

**One-paragraph:** Production autonomous agents require five production-grade components beyond the core loop: (1) a typed tool base class with a shared registry, (2) YAML configuration with env-var substitution, (3) structured JSON logging for every LLM and tool call, (4) exponential backoff retry with circuit breaker for external services, (5) a repeatable evaluation harness that measures success rate, latency, iterations, and token cost. Skip any one of these and debugging production failures becomes prohibitively expensive.

## Applies If (ALL must hold)

- Moving an autonomous agent from prototype to production deployment.
- Agents that will run on a schedule or receive external requests.
- Any agent deployment where failures are visible to users or have business impact.
- Teams that need to measure agent quality over time and detect regressions.

## Skip If (ANY kills it)

- One-off research experiments or local prototypes — production overhead exceeds value.
- Agents run only in interactive notebooks with a human watching every step.

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
