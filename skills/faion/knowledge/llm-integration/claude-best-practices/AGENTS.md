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

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-claude-best-practices.py` | Validates a produced policy JSON against `02-output-contract.xml`. | Pre-commit and CI before merge. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/ai/llm-integration/`
- `[[claude-api-basics]]`
- `[[claude-api-integration]]`
- `[[claude-advanced-features]]`
- `[[claude-messages-api]]`
- `[[claude-tool-use]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters which best-practice fix applies: root question — "Is this a production Claude pipeline (multi-worker OR cost-sensitive OR latency-bounded)?". Branches name observables (multi-worker without shared bucket, cache prefix too short, fallback logging off, Opus in inner loop, offline workload) and point at a specific core rule from `01-core-rules.xml` or at a `skip-this-methodology` directive.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/cached-system-prompt.py`

```python
"""Cached system prompt structure: stable prefix cached, dynamic tail not cached."""
from __future__ import annotations

import anthropic

client = anthropic.Anthropic()

MODEL_ID = "claude-sonnet-4-20250514"


def call_with_cached_system(
    static_content: str,
    dynamic_instructions: str,
    user_task: str,
    max_tokens: int = 4096,
):
    """Call Claude with a two-part system prompt: cached static + uncached dynamic.

    `static_content` MUST be byte-identical on every call (rule r4); place dynamic values
    in `dynamic_instructions` or `user_task`, never in `static_content`.
    """
    system = [
        {"type": "text", "text": static_content, "cache_control": {"type": "ephemeral"}},
        {"type": "text", "text": dynamic_instructions},
    ]
    return client.messages.create(
        model=MODEL_ID,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user_task}],
    )
```

### `templates/monitored-client.py`

```python
"""Minimal Claude client with model + usage + latency + cache + request-id logging."""
from __future__ import annotations

import logging
import time

import anthropic

log = logging.getLogger(__name__)
client = anthropic.Anthropic()

MODELS = {
    "router": "claude-3-5-haiku-20241022",
    "generator": "claude-sonnet-4-20250514",
    "reasoner": "claude-opus-4-5-20251101",
}


def call(role: str, system, messages: list, max_tokens: int = 2048):
    """Call Claude with logging of model, tokens, latency, and cache metrics."""
    model = MODELS[role]
    t0 = time.monotonic()
    r = client.messages.with_raw_response.create(  # captures headers for x-request-id.
        model=model,
        max_tokens=max_tokens,
        system=system,
        messages=messages,
    )
    msg = r.parse()
    elapsed = time.monotonic() - t0
    u = msg.usage
    total = u.input_tokens + u.output_tokens
    cache_hit = getattr(u, "cache_read_input_tokens", 0)
    request_id = r.headers.get("x-request-id", "")
    log.info(
        "role=%s requested=%s response=%s tokens=%d cache_read=%d elapsed=%.2fs request_id=%s",
        role, model, msg.model, total, cache_hit, elapsed, request_id,
    )
    if msg.stop_reason == "max_tokens":  # rule r3.
        raise ValueError(f"Response truncated for role={role}. Retry with higher max_tokens.")
    return msg
```

### `templates/_smoke-test.py`

```python
"""Smoke test — minimum viable filled-in version of the policy pack."""
from __future__ import annotations


def fake_output() -> dict:
    return {
        "model_tier_table": {
            "routing": "claude-3-5-haiku-20241022",
            "generation": "claude-sonnet-4-20250514",
            "reasoning": "claude-opus-4-5-20251101",
        },
        "fallback_logging": True,
        "shared_rate_bucket": True,
        "cache_layout": {"stable_prefix_first": True, "cached_prefix_tokens": 4200},
        "retry_after_parsing": True,
        "batch_api_enabled": True,
        "forbidden_seen": [],
    }


if __name__ == "__main__":
    import json

    print(json.dumps(fake_output(), indent=2))
```
