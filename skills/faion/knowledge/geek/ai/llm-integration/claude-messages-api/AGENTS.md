---
slug: claude-messages-api
tier: geek
group: ai
domain: llm-integration
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: "Produces a Messages-API call sequencer enforcing stop_reason discipline, full content-list multi-turn history, vision (base64+URL+PDF) ordering, and SSE delta routing."
content_id: "3c7e9f1a2d8b6450"
complexity: medium
produces: code
est_tokens: 4200
tags: [claude, messages-api, streaming, vision, multi-turn]
---

# Claude Messages Api

## Summary

**One-sentence:** Produces a Messages-API call sequencer enforcing stop_reason discipline, full content-list multi-turn history, vision (base64+URL+PDF) ordering, and SSE delta routing.

**One-paragraph:** Wraps the single Claude completion endpoint (`messages.create` / `messages.stream`) into a discipline pack: `stop_reason` branching (`end_turn` normal, `tool_use` loop-continue, `max_tokens` truncation), full `response.content` append in multi-turn history (text + tool_use + thinking blocks preserved), explicit `max_tokens` on every call, image-first ordering in multi-modal user content, PDF page-count validation (≤100, ≤32MB), `input_json_delta` accumulation until `content_block_stop` for streaming + tool use, `metadata.user_id` for abuse/cost attribution.

**Ефективно для:** any direct Claude completion call site; multi-turn assistant pipelines that mix text + vision + tool use; streaming consumers that must distinguish text deltas from tool/thinking deltas; teams enforcing one Messages-API discipline across many subagents.

## Applies If (ALL must hold)

- Writing or reviewing a `messages.create` / `messages.stream` call site.
- Multi-turn pipeline keeps assistant turns in history.
- Mix of text + vision + tool use in a single conversation.
- Streaming output must be parsed per delta type.

## Skip If (ANY kills it)

- Persistent Threads + Files semantics are required — use OpenAI Assistants instead.
- Provider-neutral abstraction is in place (LiteLLM) — wrap that.
- High-volume offline workload — Batch API is a better fit; see `[[claude-advanced-features]]`.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Hardened client | Anthropic with retry + cost tracker | [[claude-api-basics]] |
| Pinned model id | full-date string | release notes |
| Image / PDF inputs | JPEG/PNG ≤20MB; PDF ≤32MB / ≤100 pages | application |
| Streaming consumer | delta-type-aware parser | UI / pipeline sink |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[claude-api-basics]]` | env-auth, retry, cost tracker baseline |
| `[[claude-tool-use]]` | tool_use round-trip semantics for multi-turn |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples | ~750 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | medium | 6-step procedure with input/action/output per step | ~850 |
| `content/06-decision-tree.xml` | essential | Decision tree gating whether this methodology applies | ~550 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Author or refactor a call site | sonnet | Pattern application from template. |
| Diagnose silent failure in production | opus | Multi-step reasoning over logs + headers. |
| Author / update output config | sonnet | Deterministic from rules. |

## Templates

| File | Purpose |
|------|---------|
| `templates/agent-loop.py` | Multi-turn agent loop with explicit stop_reason branching + max-turns guard. |
| `templates/vision.py` | `analyze_image()` helper: base64 encoding, image-first ordering, PDF page check. |
| `templates/_smoke-test.py` | Minimal viable invocation against stub messages. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-claude-messages-api.py` | Validates an output JSON against `02-output-contract.xml`. | Pre-commit and CI before merge. |

## Related

- parent skill: `geek/ai/llm-integration/`
- `[[claude-api-basics]]`
- `[[claude-api-integration]]`
- `[[claude-tool-use]]`
- `[[claude-advanced-features]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` gates whether claude-messages-api applies. Root question — "Is the call site using `messages.create` / `messages.stream` directly, with mixed modalities, multi-turn, or streaming?". Branches name concrete observables and conclude with a core-rule reference from `01-core-rules.xml` or a `skip-this-methodology` directive when this methodology isn't the right fix.
