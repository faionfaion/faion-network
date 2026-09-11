# Claude API Integration

## Summary

**One-sentence:** Produces a `ClaudeService` wrapper bundling sync/async/streaming + tool use + vision + Extended Thinking + Prompt Caching + Batch API on top of a hardened Anthropic client.

**One-paragraph:** Combines all Claude API surfaces into a single service object: sync (`messages.create`) and async (`AsyncAnthropic`) completions, streaming (`messages.stream` with `text_stream` and event-level access), tool use (`tool_use` / `tool_result` round-trip), vision (base64 + URL, images + PDFs), Extended Thinking (no temperature), Prompt Caching (≥1024-token prefix with `cache_control:{"type":"ephemeral"}`), and Batch API (50%-cheaper offline jobs). Centralises `stop_reason` discipline ("max_tokens" silent truncation; "tool_use" loop continuation; "end_turn" normal completion), tenacity retry on 429/5xx/529, and a `ClaudeConfig` dataclass parametrising model / max_tokens / system.

**Ефективно для:** building the canonical Claude wrapper for a multi-agent codebase; pipelines that need to switch between sync and streaming on the same call site; teams who want one place for retry + cost tracking + cache + stop_reason; any agent loop that mixes tool use and Extended Thinking.

## Applies If (ALL must hold)

- A `ClaudeService` (or equivalent) is being authored to be reused across subagents.
- More than one Claude surface is in scope (e.g. completion + tool use + caching).
- Tenacity retry and `stop_reason` discipline must be centralised, not duplicated per-subagent.
- The team accepts a `ClaudeConfig` dataclass (model, max_tokens, system) as the call configuration object.

## Skip If (ANY kills it)

- The integration is a one-off script with no reuse plan — call the SDK directly.
- Token-cost-sensitive inner loop where Haiku alone suffices — skip the wrapper overhead.
- Provider-neutral abstraction is needed (LiteLLM / instructor) — wrap that layer instead.
- Only the Messages API is in scope — see `[[claude-messages-api]]` for the narrower wrapper.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Hardened Anthropic client | `Anthropic()` with env auth, retry, cost tracker | `[[claude-api-basics]]` |
| Pinned model id | full-date string | release notes |
| `ClaudeConfig` requirements | dataclass spec | architect notes |
| Tool registry | `name -> callable` | application code |
| Cached system prompt | text ≥1024 tokens, prefix-stable | content team |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[claude-api-basics]]` | env-auth, retry, cost tracker, x-request-id baseline |
| `[[claude-messages-api]]` | `stop_reason` semantics, message-history rules |
| `[[claude-tool-use]]` | tool definition + agent loop rules |
| `[[claude-advanced-features]]` | Extended Thinking + Prompt Caching + Batch API rules |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 11 testable rules covering sync/async/streaming/tools/vision/caching/batch plus model tiering, thinking-vs-temperature, byte-identical cache prefix, batch-offline-only; Background on model tiers and cost levers | ~1750 |
| `content/02-output-contract.xml` | essential | JSON-schema output shape + valid/invalid examples | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | medium | 6-step procedure from `ClaudeConfig` to validated service | ~1000 |
| `content/05-examples.xml` | essential | Worked code: client init, async + streaming, tool round-trip, vision (base64), Extended Thinking, ClaudeService + ClaudeConfig, tenacity retry, Prompt Caching, Batch API create/poll | ~2600 |
| `content/06-decision-tree.xml` | essential | Decision tree gating whether to apply the full integration | ~650 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Wire `ClaudeService.complete` (sync) | sonnet | Pattern application. |
| Wire `ClaudeService.stream` | sonnet | Pattern + event-type checks. |
| Add tool-use agent loop | sonnet | Stateful loop; sonnet handles within rule envelope. |
| Wire vision (base64 + PDF) | sonnet | Encode + size check. |
| Tune Extended Thinking integration | opus | Multi-step latency × cost × quality decision. |
| Author cached system prompt structure | sonnet | Rewrite to stable-first. |

## Templates

| File | Purpose |
|------|---------|
| `templates/claude-service.py` | `ClaudeService` + `ClaudeConfig`; centralises retry + stop_reason. |
| `templates/batch-api.py` | `create_batch()` + `poll_batch()` helpers. |
| `templates/_smoke-test.py` | Minimal viable invocation against stub responses. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-claude-api-integration.py` | Validates a produced service config against `02-output-contract.xml`. | Pre-commit and CI before merge. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/ai/llm-integration/`
- `[[claude-api-basics]]`
- `[[claude-best-practices]]`
- `[[claude-messages-api]]`
- `[[claude-tool-use]]`
- `[[claude-advanced-features]]`
- `[[function-calling-patterns]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` gates whether the full integration applies. Root question — "Will more than one Claude surface (completion + tool use + cache + batch + vision) be reused across subagents?". Branches name observables (single-surface vs. multi-surface, sync-only vs. streaming, tools-on vs. tools-off) and conclude with one of the core rule ids from `01-core-rules.xml` or a `skip-this-methodology` directive when a narrower methodology (`claude-messages-api`, `claude-tool-use`, `claude-advanced-features`) is enough.
