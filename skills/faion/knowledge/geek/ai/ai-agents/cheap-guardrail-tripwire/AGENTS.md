---
slug: cheap-guardrail-tripwire
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Run an input_guardrail (or equivalent pre-agent classifier) on a small/fast model — gpt-4o-mini, Haiku 4.
content_id: "d2dab35bb8d55299"
tags: [input-guardrail, cost-optimization, agent-safety, classifier]
---
# Cheap-Guardrail Tripwire Before Expensive Agent

## Summary

**One-sentence:** Run an input_guardrail (or equivalent pre-agent classifier) on a small/fast model — gpt-4o-mini, Haiku 4.

**One-paragraph:** Run an input_guardrail (or equivalent pre-agent classifier) on a small/fast model — gpt-4o-mini, Haiku 4.5, gemini-flash-lite — BEFORE the main agent ever sees the request. The guardrail returns a structured verdict; if it sets tripwire_triggered=True (or its equivalent), the SDK raises an exception and the expensive agent loop is never invoked. Off-topic, jailbreak, abuse, and spam traffic short-circuit at ~1% of the cost of running the strong model. The guardrail itself must be one cheap call returning a typed schema — never a tool-using sub-agent.

## Applies If (ALL must hold)

- Public-facing endpoints exposed to internet traffic (chatbots, support bots, search assistants).
- Any agent on a premium model where >10% of inputs are filterable cheaply (PII, off-topic, jailbreak, abuse).
- Policy enforcement that must run before any tool call has side effects (refund agents, write-capable agents, code-execution agents).
- High-volume APIs where a 1% cost reduction translates to material savings.

## Skip If (ANY kills it)

- Internal pipelines with trusted callers — guardrail latency and complexity outweigh near-zero filter rate.
- Per the user's NERO rule: never downgrade the user's own LLM calls inside NERO to save cost — this pattern is for THIRD-PARTY products, not Ruslan's personal agents.
- Output guardrails on streaming responses — buffering the full response to classify breaks streaming and harms UX (open Agents SDK issue #495).
- Tasks where the cheap classifier's confidence is poorly calibrated for your domain — it will false-positive and reject legitimate traffic.

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

- parent skill: `geek/ai/ai-agents/`
