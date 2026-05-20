---
slug: streaming-response-ux
tier: geek
group: ai
domain: ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "35902451b40c9661"
summary: "UX patterns for token-by-token LLM streaming: partial-result rendering, mid-stream cancel, edit-during-stream, and trust-preserving fallbacks."
tags: [streaming-response-ux, ai, geek]
---
# Streaming Response Ux

## Summary

**One-sentence:** UX patterns for token-by-token LLM streaming: partial-result rendering, mid-stream cancel, edit-during-stream, and trust-preserving fallbacks.

**One-paragraph:** Solves the gap between 'streaming feels alive' and 'streaming feels broken when network jitters'. Mechanism: a checklist of seven UX rules (cursor, cancel button, partial-state indicators, error recovery, edit-during-stream, copy-during-stream, scroll lock) plus telemetry for time-to-first-token and stream-abort-rate. Primary output: a streaming-UX spec for one feature surface (chat, inline-AI, copilot) with measurable thresholds.

## Applies If (ALL must hold)

- feature uses LLM streaming (SSE / WebSocket / chunked HTTP)
- users see model output as it generates, not after completion
- expected stream length > 500ms (otherwise streaming is theatre, ship batched)

## Skip If (ANY kills it)

- stream completes in <500ms median — batched UX is simpler and cheaper
- users are agents/bots, not humans — telemetry-only is sufficient
- model already returns structured JSON only — streaming text rules don't apply

## Prerequisites

- wire-protocol decided (SSE vs WebSocket vs HTTP chunked transfer)
- client framework supports streaming primitives (React 18+ Suspense, Svelte transitions, etc.)
- telemetry pipeline ready to capture TTFT (time-to-first-token) and abort events

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai` | parent domain group — provides operating context for Streaming Response Ux |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules grounded in the cited gap | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 7 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/streaming-response-ux.json` | JSON schema for the Streaming Response Ux output contract |
| `templates/streaming-response-ux.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-streaming-response-ux.py` | Enforce Streaming Response Ux output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/ai/`
- upstream playbook: `role-ux-ui-designer/AI-feature UX pattern playbook: shipping copilot / chat / inline-AI without trust collapse`
- geek/ai/llm-integration/streaming-protocols
- pro/ux/ux-ui-designer/ai-feature-ux-patterns
