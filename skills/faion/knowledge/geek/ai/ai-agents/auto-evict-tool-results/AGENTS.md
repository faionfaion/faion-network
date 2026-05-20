---
slug: auto-evict-tool-results
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Wrap the agent's tool-execution runtime so any single tool result whose token count exceeds a fixed threshold N (typically 20,000) is automatically written to disk and substituted with {path, preview, evicted: true} BEFORE the LLM ever observes the body.
content_id: "822349028b614046"
tags: [context-management, tool-results, token-accounting, middleware, long-horizon-agents]
---
# Auto-Evict Tool Results at Token Threshold

## Summary

**One-sentence:** Wrap the agent's tool-execution runtime so any single tool result whose token count exceeds a fixed threshold N (typically 20,000) is automatically written to disk and substituted with {path, preview, evicted: true} BEFORE the LLM ever observes the body.

**One-paragraph:** Wrap the agent's tool-execution runtime so any single tool result whose token count exceeds a fixed threshold N (typically 20,000) is automatically written to disk and substituted with {path, preview, evicted: true} BEFORE the LLM ever observes the body. This is a deterministic middleware policy, not an LLM-discretion choice — the agent literally cannot leak the oversized payload because the runtime never feeds it in. It is the enforced sibling of voluntary filesystem-as-memory: same compression, but applied by code.

## Applies If (ALL must hold)

- Any tool that talks to a remote service with high payload variance (web fetch, SQL, API search, log retrieval).
- Long-running agents (50+ tool calls) where a single overflow corrupts the rest of the loop.
- Multi-tenant agents where prompt-injection via large tool output is a threat.
- CI/build/log-tail tools that occasionally emit megabytes of output.

## Skip If (ANY kills it)

- Streaming/realtime tools where the agent must act on each chunk immediately and never re-reads — eviction adds latency without benefit.
- Tools whose every result is small (<1k tokens) — the manifest dance is pure overhead.
- Single-shot stateless agents that exit before context bloat matters.
- Environments without a writable filesystem (browser sandbox, edge runtime) — use M-PL-02 manifest-then-fetch with a content store instead.

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
