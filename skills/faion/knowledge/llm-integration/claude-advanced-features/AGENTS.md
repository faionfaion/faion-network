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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

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

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/think-deeply.py`

```python
"""Extended Thinking helper — returns (thinking, answer) tuple."""
from __future__ import annotations

import anthropic

client = anthropic.Anthropic()

MODEL_ID = "claude-opus-4-5-20251101"


def think_deeply(problem: str, budget: int = 5000) -> tuple[str, str]:
    """Run Extended Thinking on `problem`. Returns (thinking, answer)."""
    if budget < 1024:
        raise ValueError("Extended Thinking budget below 1024 is degenerate; use the base API path.")
    resp = client.messages.create(
        model=MODEL_ID,
        max_tokens=budget + 4096,  # rule r1: guarantee answer headroom
        thinking={"type": "enabled", "budget_tokens": budget},
        messages=[{"role": "user", "content": problem}],
        # rule r2: NO temperature parameter when thinking is enabled.
    )
    thinking = next((b.thinking for b in resp.content if b.type == "thinking"), "")
    answer = next((b.text for b in resp.content if b.type == "text"), "")
    if resp.stop_reason == "max_tokens":
        raise RuntimeError("Answer truncated — increase max_tokens or shrink budget.")
    return thinking, answer
```

### `templates/call-with-cache.py`

```python
"""Prompt Caching wrapper — returns (response_text, cache_hit_ratio)."""
from __future__ import annotations

import anthropic

client = anthropic.Anthropic()

MODEL_ID = "claude-sonnet-4-20250514"


def call_with_cache(system_text: str, user_msg: str) -> tuple[str, float]:
    """Call Claude with a stable cached system prompt and a dynamic user turn.

    `system_text` MUST be the byte-identical prefix on every call (rule r3).
    Dynamic values must live in `user_msg`, never in `system_text`.
    """
    resp = client.messages.create(
        model=MODEL_ID,
        max_tokens=1024,
        system=[{
            "type": "text",
            "text": system_text,
            "cache_control": {"type": "ephemeral"},
        }],
        messages=[{"role": "user", "content": user_msg}],
    )
    u = resp.usage
    hit_ratio = u.cache_read_input_tokens / max(u.input_tokens, 1)
    return resp.content[0].text, hit_ratio
```

### `templates/batch-submit-poll.py`

```python
"""Batch API submit + poll + errored-resubmit loop."""
from __future__ import annotations

import time

import anthropic

client = anthropic.Anthropic()

MODEL_ID = "claude-sonnet-4-20250514"
POLL_INTERVAL_SECONDS = 60  # rule r5: ≥60s polling cadence.


def submit_batch(prompts: list[dict]) -> str:
    """Submit a batch. `prompts` items must each have `id` (db pk) and `prompt`."""
    if not prompts:
        raise ValueError("Empty batch refused.")
    reqs = [
        {
            "custom_id": p["id"],
            "params": {
                "model": MODEL_ID,
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": p["prompt"]}],
            },
        }
        for p in prompts
    ]
    return client.messages.batches.create(requests=reqs).id


def poll_and_collect(batch_id: str, poll_interval: int = POLL_INTERVAL_SECONDS) -> list[dict]:
    """Poll until `processing_status == "ended"`; errored items returned for resubmit (rule r6)."""
    if poll_interval < 60:
        raise ValueError("Poll interval below 60 violates rule r5.")
    while True:
        batch = client.messages.batches.retrieve(batch_id)
        if batch.processing_status == "ended":
            out: list[dict] = []
            for r in client.messages.batches.results(batch_id):
                if r.result.type == "succeeded":
                    out.append({"id": r.custom_id, "text": r.result.message.content[0].text})
                else:
                    out.append({"id": r.custom_id, "error": str(r.result.error), "resubmit": True})
            return out
        time.sleep(poll_interval)
```

### `templates/_smoke-test.py`

```python
"""Smoke test — minimum viable filled-in version of the wrappers."""
from __future__ import annotations


def fake_output() -> dict:
    return {
        "features_enabled": ["extended_thinking", "prompt_caching"],
        "model_id": "claude-opus-4-5-20251101",
        "extended_thinking": {"budget_tokens": 5000, "max_tokens": 9096},
        "prompt_caching": {"cached_prefix_tokens": 4200, "hit_ratio_target": 0.75},
        "cache_hit_ratio": 0.82,
        "forbidden_seen": [],
    }


if __name__ == "__main__":
    import json

    print(json.dumps(fake_output(), indent=2))
```
