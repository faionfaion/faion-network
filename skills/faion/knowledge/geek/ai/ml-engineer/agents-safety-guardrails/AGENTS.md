---
slug: agents-safety-guardrails
tier: geek
group: ai
domain: ml-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Autonomous agents require five categories of guardrail before production deployment: execution safety (iteration limits, timeouts), content safety (input validation, PII handling), financial safety (cost caps, rate limiting), action safety (sandboxed execution, blocked patterns), and human-in-loop gates for irreversible actions.
content_id: "3f3ef0143d291706"
tags: [agents, safety, guardrails, human-in-loop, sandboxing]
---
# Agent Safety Guardrails — Iteration Limits, Cost Caps, Human-in-Loop

## Summary

**One-sentence:** Autonomous agents require five categories of guardrail before production deployment: execution safety (iteration limits, timeouts), content safety (input validation, PII handling), financial safety (cost caps, rate limiting), action safety (sandboxed execution, blocked patterns), and human-in-loop gates for irreversible actions.

**One-paragraph:** Autonomous agents require five categories of guardrail before production deployment: execution safety (iteration limits, timeouts), content safety (input validation, PII handling), financial safety (cost caps, rate limiting), action safety (sandboxed execution, blocked patterns), and human-in-loop gates for irreversible actions. Each category must be implemented in code — not just in the system prompt — because LLM instructions alone are not reliable safety mechanisms.

## Applies If (ALL must hold)

- Any autonomous agent before production deployment.
- Agents with access to external APIs, databases, file systems, or communication channels.
- Agents that may execute code or shell commands.
- Multi-step workflows where a wrong intermediate result cascades through subsequent steps.
- Agents handling user data, financial information, or PII.

## Skip If (ANY kills it)

- Read-only research agents with no external writes — full approval gates add unnecessary latency.
- Human-supervised sandbox exploration where the user is actively watching every step.

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
