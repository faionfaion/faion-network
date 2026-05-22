---
slug: streaming-response-ux
tier: geek
group: ai
domain: ai-core
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: "Produces a streaming-UX spec for one feature surface (chat / inline-AI / copilot): cursor, cancel, partial-state, error recovery, edit-during-stream, scroll lock, plus TTFT + abort-rate telemetry thresholds."
content_id: "be6372b3ce87be0a"
complexity: medium
produces: spec
est_tokens: 4200
tags: [streaming, sse, websocket, chat-ux, copilot, ai, geek]
---

# Streaming Response UX

## Summary

**One-sentence:** Produces a streaming-UX spec for one feature surface (chat / inline-AI / copilot): cursor, cancel, partial-state, error recovery, edit-during-stream, scroll lock, plus TTFT + abort-rate telemetry thresholds.

**Ефективно для:** front-end engineers shipping LLM chat / copilot UX where token-by-token streaming feels broken on jitter; PMs writing acceptance criteria for streaming UX; SREs adding TTFT / abort-rate telemetry to a streaming surface.

**One-paragraph:** This methodology pins the recurring decision around "streaming-response-ux" into a typed artefact governed by 5 testable rules. Inputs are typed and sourced; the output is contract-checked; a named accountable owner signs every record. The decision tree at `content/06-decision-tree.xml` routes preconditions and variant signals to a run / skip / variant outcome, with every conclusion referencing a rule id in `content/01-core-rules.xml`.

## Applies If (ALL must hold)

- Feature uses LLM streaming (SSE / WebSocket / chunked HTTP).
- Users see model output as it generates, not after completion.
- Expected stream length > 500ms median.
- Owner exists for the streaming surface after ship.

## Skip If (ANY kills it)

- Stream completes in <500ms median — batched UX is simpler and cheaper.
- Users are agents/bots, not humans — telemetry-only is sufficient.
- Model already returns structured JSON only — streaming text rules don't apply.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Wire-protocol decision | ADR | tech lead |
| Client framework version | string | frontend lead |
| Telemetry pipeline endpoint | URL | SRE |
| Surface owner | handle / email | team roster |
| Latency budget | ms (target + p95) | PM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[llm-integration]]` | provider SDK streaming primitives |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input / action / output per step | ~900 |
| `content/05-examples.xml` | recommended | one end-to-end worked example | ~600 |
| `content/06-decision-tree.xml` | essential | run / skip / variant router referencing rule ids | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_ux_rules` | haiku | Bounded template fill from prereqs. |
| `synthesize_surface_spec` | sonnet | Per-surface judgment with bounded inputs. |
| `review_for_trust_collapse` | opus | Cross-input synthesis when failures cascade. |

## Templates

| File | Purpose |
|------|---------|
| `templates/streaming-response-ux.json` | JSON Schema for the Streaming Response UX output contract |
| `templates/streaming-response-ux.md` | Markdown skeleton with the required fields |
| `templates/_smoke-test.md` | Filled-in minimum viable example of a streaming-response-ux record |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-streaming-response-ux.py` | Enforce the Streaming Response UX output contract | After subagent returns, before downstream consumer reads |

## Related

- [[llm-integration]] — provider streaming primitives.
- [[ai-feature-ux-patterns]] — adjacent UX-pattern catalogue.
- [[telemetry-spec-template]] — TTFT / abort-rate sink contract.

## Decision tree

Lives at `content/06-decision-tree.xml`. Two-question gate: (1) preconditions present? (2) variant detected per the methodology-specific signal? Routes to run / skip / variant. Every conclusion references a rule id from `content/01-core-rules.xml`.
