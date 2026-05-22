---
slug: manifest-then-fetch
tier: geek
group: ai
domain: ai-agents
version: 2.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Implements the manifest-then-fetch tool protocol (small manifest preview + on-demand fetch) for an agent's tool surface and emits a protocol-spec.
content_id: 3a2b3dca89641401
complexity: medium
produces: spec
est_tokens: 4000
tags: [tool-protocol, context-budget, manifest-fetch, agent-design]
---
# Manifest Then Fetch

## Summary

**One-sentence:** Implements the manifest-then-fetch tool protocol (small manifest preview + on-demand fetch) for an agent's tool surface and emits a protocol-spec.

**One-paragraph:** Tools that return raw payloads blow up the context window the moment they hit a large result. The manifest-then-fetch protocol returns only a small manifest (execution_id, preview, size_tokens) and stores the body externally. The agent fetches the body via get_full_result(execution_id) only when needed. This methodology converts a tool inventory into a deterministic protocol-spec: which tools wrap, manifest size, retention TTL, fetch policy.

**Ефективно для:** solopreneur whose agent context blows past 50K tokens after one search call.

## Applies If (ALL must hold)

- Agent calls ≥1 tool that returns >2KB output.
- Object/blob store available (S3, local fs, Redis) for body parking.
- Tools surface returns text payloads (not binaries).
- Latency budget allows an extra fetch step when needed.
- Agent can be taught to call get_full_result conditionally.

## Skip If (ANY kills it)

- All tool outputs are <500 bytes (manifests add overhead).
- Single-turn tool calls — context blowup not a concern.
- Cannot host body store.
- Tool outputs are sensitive and must not be retained beyond the turn.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `tool-inventory.yaml` | tools (list with avg_output_bytes, sensitivity), store_backend, manifest_size_target_tokens | author |
| `Body store endpoint` | S3 / Redis / fs | infra |
| `Agent loop ability to call follow-up tool` | yes/no | agent framework |

## Assumes Loaded

| Methodology | Why |
|---|---|
| [[max-turns-circuit-breaker]] | Manifest-then-fetch adds turns; cap them. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | Rules for manifest shape, preview size, fetch policy, retention TTL. | ~1000 |
| `content/02-output-contract.xml` | essential | protocol-spec schema + examples. | ~800 |
| `content/03-failure-modes.xml` | essential | Manifest leak (full body in preview), unbounded retention, stale execution_id, fetch before preview. | ~700 |
| `content/04-procedure.xml` | recommended | 5-step wiring procedure. | ~800 |
| `content/06-decision-tree.xml` | essential | Decision tree | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| Profile parsing | haiku | Mechanical. |
| Decision drafting | sonnet | Tradeoffs require sound reasoning. |
| Code/config emission | sonnet | Mechanical but must compile. |
| Failure-mode cross-check | opus | Catches subtle gaps. |

## Templates

| File | Purpose |
|---|---|
| `templates/tool-inventory.yaml` | Input. |
| `templates/protocol-spec.md` | Output. |
| `templates/manifest_then_fetch.py` | Working tool wrapper. |
| `templates/_smoke-test.yaml` | Minimum. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-manifest-then-fetch.py` | Validates output against the JSON schema. | Pre-commit. |

## Related

- [[max-turns-circuit-breaker]]
- [[mcp-resource-vs-tool-vs-prompt]]
- [[map-reduce-send-fanout]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Branches on avg_bytes (<500 → skip; >=500 → wrap), then on sensitivity (high → short TTL + per-call store; low → shared store with longer TTL), then on preview strategy (head-N | summary | structured). Each leaf cites a rule id in 01-core-rules.xml so the agent always cites which rule drove the choice — and can be replayed for audit.
