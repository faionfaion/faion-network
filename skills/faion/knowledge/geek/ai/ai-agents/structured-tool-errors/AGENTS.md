---
slug: structured-tool-errors
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Tool errors are part of the prompt — they are the next thing the agent reads.
content_id: "f15b4f830865bb44"
tags: [error-handling, structured-errors, agent-loops, mcp, tool-design]
---
# Structured Tool Errors with recoveryHint

## Summary

**One-sentence:** Tool errors are part of the prompt — they are the next thing the agent reads.

**One-paragraph:** Tool errors are part of the prompt — they are the next thing the agent reads. Never bubble raw stack traces, HTTP error bodies, or upstream JSON. Return a structured object: {code, message, recoveryHint, traceId, ...details} where recoveryHint is a closed enum (RETRY_LATER | CHECK_INPUT | TRY_ALTERNATIVE | REPORT_TO_USER | NEEDS_AUTH). The hint is a direct instruction to the model's next reasoning step. The closed code lets the agent's loop decide retry vs escalate vs abort without re-reading the message.

## Applies If (ALL must hold)

- Every error path of every tool, including reads.
- Tools wrapping flaky upstreams (rate limits, auth tokens, transient 5xx).
- Tools where the agent retries automatically — the hint controls the retry policy.
- MCP servers — error structure is part of the public contract.

## Skip If (ANY kills it)

- Don't fabricate recoveryHint when the failure is genuinely unrecoverable — emit REPORT_TO_USER and stop the loop instead of guessing RETRY_LATER.
- Don't add a hint to a successful response with warnings; warnings belong in a separate warnings: [] field, not the error envelope.
- Don't expose internal stack traces inside details — they leak implementation, fill context, and don't help the agent.

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
