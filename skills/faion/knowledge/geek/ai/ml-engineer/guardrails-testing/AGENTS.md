---
slug: guardrails-testing
tier: geek
group: ai
domain: ml-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Guardrail testing requires three distinct test suites: security tests (injection payloads that must be blocked), accuracy tests (legitimate content that must pass), and performance tests (latency and throughput under load).
content_id: "9648b96078cd82dd"
tags: [guardrails, security-testing, red-teaming, prompt-injection, llm-testing]
---
# LLM Guardrails Testing and Red-Teaming

## Summary

**One-sentence:** Guardrail testing requires three distinct test suites: security tests (injection payloads that must be blocked), accuracy tests (legitimate content that must pass), and performance tests (latency and throughput under load).

**One-paragraph:** Guardrail testing requires three distinct test suites: security tests (injection payloads that must be blocked), accuracy tests (legitimate content that must pass), and performance tests (latency and throughput under load). Red-teaming with adversarial payloads before production and monthly after deployment is mandatory for any guardrail covering security or compliance use cases.

## Applies If (ALL must hold)

- Before deploying any guardrail system to production — run the full security and accuracy test suites.
- Monthly red-team sessions to test against new jailbreak and injection techniques.
- After any guardrail configuration change or underlying model update.
- When investigating false positive reports from production users.

## Skip If (ANY kills it)

- Live production traffic — run tests in staging against production-equivalent guardrail config.
- End-to-end tests with live LLM APIs in CI — use mocked LLM clients to avoid cost and flakiness.

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
