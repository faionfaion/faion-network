---
slug: claude-api-basics
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: The single most important rule: pin model IDs with full date strings (e.
content_id: "a1dcfc3746050955"
tags: [claude, api, authentication, rate-limiting, cost-tracking]
---
# Claude API Basics

## Summary

**One-sentence:** The single most important rule: pin model IDs with full date strings (e.

**One-paragraph:** The single most important rule: pin model IDs with full date strings (e.g., claude-sonnet-4-20250514) to prevent silent behavior changes on alias updates. Claude API has non-obvious failure modes: 529 overloaded_error requires retry logic (not a client error), rate limits are per-tier and hit fast in concurrent agent workflows, cost tracking requires exact model ID strings (aliases break lookups), and token counting adds a round-trip that degrades hot-path latency.

## Applies If (ALL must hold)

- Bootstrapping any Anthropic SDK integration from scratch.
- Selecting the right Claude model for a cost vs. capability trade-off.
- Implementing retry/backoff for production LLM calls.
- Tracking token usage and API costs per request or session.
- Debugging authentication and rate-limit failures.

## Skip If (ANY kills it)

- Working client setup already exists — don't re-implement auth/retry per-call.
- Batch-processing non-time-sensitive workloads — use the Batch API (50% cheaper) instead.
- Streaming output needed — see claude-messages-api methodology.
- Task requires tool use or structured JSON output — see claude-tool-use methodology.

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
