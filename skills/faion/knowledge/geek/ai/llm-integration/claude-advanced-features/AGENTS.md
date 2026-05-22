---
slug: claude-advanced-features
tier: geek
group: ai
domain: llm-integration
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: "Produces a wired-in configuration plus call wrappers for Extended Thinking, Computer Use, Prompt Caching, and Batch API on the Anthropic SDK."
content_id: "9a57610d31a6965d"
complexity: deep
produces: code
est_tokens: 4400
tags: [claude, anthropic, extended-thinking, computer-use, prompt-caching, batch-api]
---

# Claude Advanced Features

## Summary

**One-sentence:** Produces a wired-in configuration plus call wrappers for Extended Thinking, Computer Use, Prompt Caching, and Batch API on the Anthropic SDK.

**One-paragraph:** Covers the four Claude capabilities that are not part of the default Messages API path: Extended Thinking (`thinking={"type":"enabled","budget_tokens":N}`) for visible reasoning chains, Computer Use (versioned beta tool) for sandboxed GUI automation, Prompt Caching (`cache_control:{"type":"ephemeral"}` on stable prefixes ≥1024 tokens) for ~90% input-cost reduction, and Batch API (`client.messages.batches.*`) for 50%-cheaper offline workloads with up to 24h SLA. The methodology produces typed call wrappers, a per-feature usage policy, and a monitoring contract (`cache_read_input_tokens`, `processing_status`, `stop_reason`).

**Ефективно для:** offline enrichment pipelines hitting Claude with a fixed system prompt thousands of times; long-document QA with a reusable cached context; Opus-driven architecture/decision tasks where reasoning trace must be auditable; sandboxed GUI agents that need bounded action loops; cost-reduction sprints on top of an already-working `claude-api-integration` baseline.

## Applies If (ALL must hold)

- The pipeline already has a working `Anthropic` client (env-based auth, retry, stop_reason handling).
- One of {Extended Thinking, Computer Use, Prompt Caching, Batch API} is on the table — selected because the workload matches its sweet spot.
- The model id is pinned with a full date string (e.g. `claude-opus-4-5-20251101`, `claude-sonnet-4-20250514`).
- A monitoring surface exists (`usage.cache_read_input_tokens`, `processing_status`) and is logged on every call.

## Skip If (ANY kills it)

- The baseline integration is not in place yet — bootstrap `[[claude-api-basics]]` and `[[claude-api-integration]]` first.
- The workload is synchronous and user-facing with sub-second latency budget — Batch API and Extended Thinking are wrong here.
- Inputs change byte-for-byte every call (timestamps, request ids in the prefix) — Prompt Caching will only burn write cost.
- Production system carries live credentials and no sandbox — Computer Use is forbidden without an isolation boundary.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Working Anthropic client | `Anthropic(api_key=...)` instance | `[[claude-api-basics]]` |
| Pinned model id | full-date string (`claude-opus-4-5-20251101`) | release notes / `claude-best-practices` |
| Workload profile | latency budget, call volume, prefix-stability flag | architect notes |
| Cost-tracking sink | logger or DB collecting `usage.*_input_tokens` | `[[claude-best-practices]]` |
| Sandboxed VM (Computer Use only) | Docker / Firecracker with no host credentials | infra |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[claude-api-basics]]` | client init, retry, stop_reason discipline |
| `[[claude-api-integration]]` | sync/async/streaming wrappers Extended Thinking layers onto |
| `[[claude-best-practices]]` | model tier selection + cost-monitoring foundation |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules covering the four features | ~900 |
| `content/02-output-contract.xml` | essential | JSON schema + valid/invalid examples for the produced config + wrappers | ~750 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | medium | 6-step procedure to pick a feature, configure it, and verify | ~900 |
| `content/06-decision-tree.xml` | essential | Decision tree gating which advanced feature applies | ~550 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Pick feature(s) for a given workload | sonnet | Rubric-based decision against the table in 04-procedure. |
| Author cached system prompt | sonnet | Pattern application; rewrite to stable-first. |
| Tune Extended Thinking budget | opus | Multi-step trade-off (latency × cost × quality). |
| Write Batch API submit/poll wrapper | sonnet | Boilerplate from `templates/batch-submit-poll.py`. |
| Review Computer Use safety harness | opus | Threat-model reasoning; cannot be templated. |

## Templates

| File | Purpose |
|------|---------|
| `templates/think-deeply.py` | `(thinking, answer)` wrapper enforcing `max_tokens >= budget + 4096`. |
| `templates/call-with-cache.py` | Cached-system-prompt call returning text plus `cache_read_input_tokens` ratio. |
| `templates/batch-submit-poll.py` | Batch submit + 60s-min poll + errored-result re-collect. |
| `templates/_smoke-test.py` | Minimal viable invocation of all three wrappers against fake usage. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-claude-advanced-features.py` | Validates an output JSON against `02-output-contract.xml`. | Pre-commit and CI before merge. |

## Related

- parent skill: `geek/ai/llm-integration/`
- `[[claude-api-basics]]`
- `[[claude-api-integration]]`
- `[[claude-best-practices]]`
- `[[claude-messages-api]]`
- `[[claude-tool-use]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters which of the four advanced features should apply: the root question asks whether the workload tolerates ≥minutes latency. From there branches name concrete observables (system-prompt size in tokens, prefix-stability, GUI-only target, reasoning-trace requirement) and each leaf points at one of the rule ids from `01-core-rules.xml` or at a `skip-this-methodology` conclusion when none of the four features apply.
