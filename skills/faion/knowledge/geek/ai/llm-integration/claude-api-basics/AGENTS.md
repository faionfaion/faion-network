---
slug: claude-api-basics
tier: geek
group: ai
domain: llm-integration
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: "Produces a bootstrapped Anthropic SDK client: env-only auth, full-date pinned model id, tenacity retry covering 429+529, cost tracker keyed off `response.model`, and `x-request-id` logging."
content_id: "0e8f6a4b2c91d780"
complexity: medium
produces: code
est_tokens: 3800
tags: [claude, anthropic, sdk, retry, rate-limit, cost-tracking]
---

# Claude API Basics

## Summary

**One-sentence:** Produces a bootstrapped Anthropic SDK client: env-only auth, full-date pinned model id, tenacity retry covering 429+529, cost tracker keyed off `response.model`, and `x-request-id` logging.

**One-paragraph:** Establishes the minimum viable production wiring for `anthropic.Anthropic()`: API key loaded from `ANTHROPIC_API_KEY` env var, model id pinned with a full-date suffix (no aliases), retry/backoff via `tenacity` covering both `RateLimitError` (429) and `APIStatusError` 529 `overloaded_error`, `stop_reason` discipline (`max_tokens` is silent truncation), `usage`-based `CostTracker` keyed off `response.model` (the response field, not the request), and `x-request-id` captured for support debugging. Multiprocessing path note: each worker constructs its own client; module-level globals are not safe across forks.

**Ефективно для:** any new Claude integration scaffolded from scratch; rate-limit incident debugging where Tier 1 caps (50 req/min, 40K tokens/min) are biting on concurrent subagents; cost-attribution dashboards that need to be alias-proof; teams migrating from a "single-shot script" to a production-grade client wrapper.

## Applies If (ALL must hold)

- Bootstrapping any new Anthropic SDK integration, or refactoring a script-style call site.
- A retry policy and a cost-tracking sink need to be wired in for the first time.
- Calls happen in a server / agent process (not a notebook one-off).
- The team is ready to pin model ids with full-date suffixes.

## Skip If (ANY kills it)

- A working client + retry + cost tracker already exists — extend `[[claude-api-integration]]` instead.
- The workload is offline batch — jump straight to Batch API in `[[claude-advanced-features]]`.
- Streaming is the only requirement — see `[[claude-messages-api]]`.
- Tool-use loops are the goal — see `[[claude-tool-use]]`.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `ANTHROPIC_API_KEY` | env var | secrets manager / 1Password / `.env` |
| Pinned model id | `claude-{sonnet,opus,haiku}-...-YYYYMMDD` | release notes |
| Tier capacity profile | req/min + tokens/min per tier | Anthropic console |
| Cost sink | logger, sqlite, or metrics endpoint | infra |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[claude-messages-api]]` | the only completion endpoint these basics call into |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules covering auth, pinning, retry, cost tracking, multiprocessing | ~850 |
| `content/02-output-contract.xml` | essential | JSON schema + valid/invalid examples for the produced client config | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | ~750 |
| `content/04-procedure.xml` | medium | 6-step procedure from key load to cost-tracker wired in | ~800 |
| `content/06-decision-tree.xml` | essential | Decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Wire env auth + client init | sonnet | Pattern application from template. |
| Author `CostTracker` for current price sheet | sonnet | Deterministic mapping from prices table. |
| Configure tenacity decorator (which exceptions, which backoff) | sonnet | Rule-driven from r3. |
| Diagnose recurring 429 cascade in multi-worker pool | opus | Multi-step reasoning over headers + worker topology. |

## Templates

| File | Purpose |
|------|---------|
| `templates/cost-tracker.py` | `CostTracker` class keyed off `response.model` and `response.usage`. |
| `templates/retry-wrapper.py` | `tenacity` decorator covering 429 + 529 + connect errors. |
| `templates/_smoke-test.py` | Minimal viable invocation against a stub usage object. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-claude-api-basics.py` | Validates an output JSON against `02-output-contract.xml`. | Pre-commit and CI before merge. |

## Related

- parent skill: `geek/ai/llm-integration/`
- `[[claude-api-integration]]`
- `[[claude-best-practices]]`
- `[[claude-messages-api]]`
- `[[claude-tool-use]]`
- `[[openai-api-integration]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` gates whether `claude-api-basics` should apply: root question — "Is this the first Anthropic SDK call site in the codebase, or is an existing client missing retry/cost tracking?". Branches lead to a specific core rule (env-only auth, full-date pinning, tenacity wiring, cost-tracker installation) or to a `skip:` conclusion when the client is already production-grade.
