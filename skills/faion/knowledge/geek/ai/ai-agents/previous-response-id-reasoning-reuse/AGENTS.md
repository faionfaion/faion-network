---
slug: previous-response-id-reasoning-reuse
tier: geek
group: ai
domain: ai-agents
version: 2.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
content_id: 23f97afa2a89b56d
summary: Produces an agent-continuity spec wiring OpenAI Responses API `previous_response_id` to preserve reasoning items across turns instead of reconstructing Chat-Completions message arrays.
complexity: medium
produces: spec
est_tokens: 4000
tags: [reasoning, responses-api, agent-continuity, cache-optimization, multi-turn]
---
# previous_response_id Reasoning Reuse

## Summary

**One-sentence:** Produces an agent-continuity spec wiring OpenAI Responses API `previous_response_id` to preserve reasoning items across turns instead of reconstructing Chat-Completions message arrays.

**One-paragraph:** Multi-turn agents that rebuild a Chat-Completions message array per turn lose reasoning items and pay cache eviction costs. Responses API's `previous_response_id` carries reasoning + tool-result state server-side. This methodology emits a deterministic spec: when to use previous_response_id, retention TTL, fallback to message-array, observability hookup.

**Ефективно для:** team running OpenAI Responses API agents whose costs balloon on long conversations.

## Applies If (ALL must hold)

- Using OpenAI Responses API (not Chat Completions).
- Multi-turn agent (>= 3 turns).
- Reasoning models (o1, o3, etc.) where reasoning tokens are expensive.
- Stateless server doesn't preclude session continuity.

## Skip If (ANY kills it)

- Using Chat Completions API exclusively.
- Single-turn endpoint.
- Cannot rely on OpenAI server-side state retention.
- Hard requirement to log full message history client-side.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `api-flavor` | "responses" / "chat" | infra |
| `turn_count_distribution` | histogram | analytics |
| `retention_ttl_hours` | integer | OpenAI policy |

## Assumes Loaded

| Methodology | Why |
|---|---|
| [[prompt-cache-prefix-order]] | Complementary cache strategy. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 rules: use previous_response_id, store id per conversation, fallback path on 404, retention TTL, log id per turn. | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for the spec. | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: dropping id, mixing chat + responses, no fallback, leaking ids cross-user. | ~700 |
| `content/04-procedure.xml` | recommended | 4-step procedure. | ~600 |
| `content/05-examples.xml` | recommended | One canonical multi-turn worked example. | ~600 |
| `content/06-decision-tree.xml` | essential | Picks previous_response_id vs message-array. | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `parse_api_flavor` | haiku | Mechanical. |
| `audit_continuity_path` | opus | Subtle id leakage between users. |
| `emit_spec` | sonnet | Mechanical. |

## Templates

| File | Purpose |
|---|---|
| `templates/agent-loop.py` | Responses API loop using previous_response_id. |
| `templates/_smoke-test.yaml` | Minimum spec. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-previous-response-id-reasoning-reuse.py` | Validates spec against the schema. | Pre-commit. |

## Related

- [[prompt-cache-prefix-order]]
- [[reasoning-first-architectures]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Branches on api_flavor (chat → fallback; responses → continue), then on multi_turn (yes → previous_response_id; no → single-call). Each leaf cites a rule id.
