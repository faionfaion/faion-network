# Claude Best Practices

## Summary

**One-sentence:** Produces a production policy pack for Claude calls: model-tier table, prompt-caching layout, `retry-after` parsing, fallback logging, dry-run gates.

**One-paragraph:** Codifies the production-grade patterns from `[[claude-api-basics]]` + `[[claude-api-integration]]` into a single policy pack: tier-aware model selection (Haiku/Sonnet/Opus per sub-task), shared rate-limit token bucket across workers, `retry-after` header parsing (do not guess), explicit fallback-model logging (Sonnet → Haiku must surface in logs), strict prompt-caching prefix discipline, and pre-flight token counting only when budget enforcement is strict. All call sites use `messages.create` with `max_tokens` explicit; structured output via forced tool call rather than prompt engineering.

**Ефективно для:** any production Claude workload before launch; multi-worker orchestrators sharing a single API key; cost-sensitive workloads where every call must hit the cache; teams establishing a baseline policy across multiple Claude integrations.

## Applies If (ALL must hold)

- Building a new production Claude pipeline or hardening an existing one.
- Cost and reliability are explicit non-functional requirements.
- More than one worker / process makes Anthropic calls.
- Cache hit ratio is being monitored and gated.

## Skip If (ANY kills it)

- Quick scripted one-off calls with no cost or reliability concerns.
- Provider-neutral abstraction layer is required (LiteLLM, instructor) — wrap that.
- All calls go through a third-party gateway you don't control.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Hardened client | Anthropic client + retry + cost tracker | `[[claude-api-basics]]` |
| `ClaudeService` | wrapper with `complete/stream/agent_loop` | `[[claude-api-integration]]` |
| Tier capacity profile | req/min + tokens/min per tier | Anthropic console |
| Workload sub-task map | list of (sub_task, model_tier) pairs | architect notes |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[claude-api-basics]]` | env-auth, retry, cost-tracker baseline |
| `[[claude-api-integration]]` | `ClaudeService` wrapper for centralised stop_reason |
| `[[claude-advanced-features]]` | Prompt Caching + Batch API + Extended Thinking rules |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (model tiers, pinning, max_tokens, caching layout, retry-after, batch) | ~900 |
| `content/01-model-selection.xml` | essential | Model-tier table preserved from v1 | ~500 |
| `content/02-output-contract.xml` | essential | JSON schema + valid/invalid examples for the policy pack | ~800 |
| `content/02-cost-optimization.xml` | essential | Cost-optimization patterns preserved from v1 | ~500 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | ~800 |
| `content/03-reliability-patterns.xml` | essential | Reliability patterns preserved from v1 | ~500 |
| `content/04-procedure.xml` | medium | 6-step procedure from tier-table to validated policy | ~900 |
| `content/06-decision-tree.xml` | essential | Decision tree gating which best-practice fix applies | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Author tier table for a workload | sonnet | Rubric-based; deterministic from sub-task list. |
| Verify cache layout | sonnet | Static check on prefix length + dynamic-content position. |
| Diagnose 429 cascade across worker pool | opus | Multi-step reasoning over headers + worker topology. |
| Decide if a workload qualifies for Batch API | sonnet | Latency-budget vs. workload pattern. |

## Templates

| File | Purpose |
|------|---------|
| `templates/cached-system-prompt.py` | System prompt object with static cached prefix + dynamic tail. |
| `templates/monitored-client.py` | Minimal Claude wrapper logging `response.model`, usage, elapsed, x-request-id. |
| `templates/_smoke-test.py` | Minimal viable invocation against stub. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-claude-best-practices.py` | Validates a produced policy JSON against `02-output-contract.xml`. | Pre-commit and CI before merge. |

## Related

- parent skill: `geek/ai/llm-integration/`
- `[[claude-api-basics]]`
- `[[claude-api-integration]]`
- `[[claude-advanced-features]]`
- `[[claude-messages-api]]`
- `[[claude-tool-use]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters which best-practice fix applies: root question — "Is this a production Claude pipeline (multi-worker OR cost-sensitive OR latency-bounded)?". Branches name observables (multi-worker without shared bucket, cache prefix too short, fallback logging off, Opus in inner loop, offline workload) and point at a specific core rule from `01-core-rules.xml` or at a `skip-this-methodology` directive.
