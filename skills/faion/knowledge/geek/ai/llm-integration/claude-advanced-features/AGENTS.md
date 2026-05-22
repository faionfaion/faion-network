---
slug: claude-advanced-features
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Extended Thinking exposes the model's reasoning chain for complex problems.
content_id: "9a57610d31a6965d"
tags: [claude, advanced-features, extended-thinking, computer-use, prompt-caching]
---
# Claude Advanced Features

## Summary

**One-sentence:** Extended Thinking exposes the model's reasoning chain for complex problems.

**One-paragraph:** Extended Thinking exposes the model's reasoning chain for complex problems. Computer Use lets Claude control a desktop or browser via screenshot + action loops. Prompt Caching reduces input token cost by up to 90% for repeated stable prefixes. Batch API cuts cost by 50% for workloads that tolerate up to 24-hour latency.

## Applies If (ALL must hold)

- Extended Thinking: multi-step math, architecture decisions, complex debugging, strategic planning where visible reasoning improves trust.
- Computer Use: automating legacy GUI apps, browser automation, or desktop testing in sandboxed environments.
- Prompt Caching: any pipeline that calls Claude repeatedly with the same system prompt or document context (stable prefix > 1024 tokens).
- Batch API: offline enrichment, content generation, nightly analysis — any workload where 24-hour latency is acceptable.

## Skip If (ANY kills it)

- Extended Thinking: simple extraction, classification, or templating — adds latency and tokens without benefit.
- Computer Use: production systems with live credentials or databases — always requires human-in-the-loop; never unattended.
- Prompt Caching: prompts that change on every call — cache never hits; you pay write cost with no read benefit.
- Batch API: real-time user-facing responses — 24-hour SLA makes it unsuitable for synchronous pipelines.

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
