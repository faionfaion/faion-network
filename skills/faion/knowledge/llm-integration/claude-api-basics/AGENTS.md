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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

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

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/cost-tracker.py`

```python
"""CostTracker — per-call + session cost accumulation for Claude API."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class CostTracker:
    """Track Claude API costs including prompt-cache pricing.

    Per rule r4, key the PRICES table off `response.model` — the response
    field — not the requested model string, since aliases can resolve to
    a different snapshot than requested.
    """

    PRICES: dict[str, dict[str, float]] = field(default_factory=lambda: {
        "claude-opus-4-5-20251101":  {"in": 15.00, "out": 75.00, "cw": 18.75, "cr": 1.50},
        "claude-sonnet-4-20250514":  {"in":  3.00, "out": 15.00, "cw":  3.75, "cr": 0.30},
        "claude-3-5-haiku-20241022": {"in":  0.80, "out":  4.00, "cw":  1.00, "cr": 0.08},
    })
    total: float = 0.0
    calls: int = 0
    unknown_models: set[str] = field(default_factory=set)

    def track(self, model: str, usage) -> float:
        """Record one API call's cost and return it (USD)."""
        if model not in self.PRICES:
            self.unknown_models.add(model)
        p = self.PRICES.get(model, {"in": 0.0, "out": 0.0, "cw": 0.0, "cr": 0.0})
        cost = (
            usage.input_tokens * p["in"]
            + usage.output_tokens * p["out"]
            + getattr(usage, "cache_creation_input_tokens", 0) * p["cw"]
            + getattr(usage, "cache_read_input_tokens", 0) * p["cr"]
        ) / 1_000_000
        self.total += cost
        self.calls += 1
        return cost

    def report(self) -> str:
        out = f"Total: ${self.total:.4f} across {self.calls} calls"
        if self.unknown_models:
            out += f" (UNKNOWN MODELS: {sorted(self.unknown_models)})"
        return out
```

### `templates/retry-wrapper.py`

```python
"""Tenacity-based retry wrapper for Anthropic API calls."""
from __future__ import annotations

from anthropic import APIConnectionError, APIStatusError, RateLimitError
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

RETRYABLE_STATUSES = {500, 502, 503, 529}


def _is_retryable(exc: BaseException) -> bool:
    if isinstance(exc, (RateLimitError, APIConnectionError)):
        return True
    if isinstance(exc, APIStatusError):
        return getattr(exc, "status_code", 0) in RETRYABLE_STATUSES
    return False


def anthropic_retry(max_attempts: int = 5, min_wait: float = 1.0, max_wait: float = 60.0):
    """Decorator factory: retry on 429 + 500/502/503/529 + connection errors."""
    return retry(
        retry=retry_if_exception(_is_retryable),
        wait=wait_exponential(multiplier=1, min=min_wait, max=max_wait),
        stop=stop_after_attempt(max_attempts),
    )


default_retry = anthropic_retry()
```

### `templates/_smoke-test.py`

```python
"""Smoke test — minimum viable filled-in version of the basics wiring."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class _StubUsage:
    input_tokens: int = 1000
    output_tokens: int = 200
    cache_creation_input_tokens: int = 0
    cache_read_input_tokens: int = 0


def fake_output() -> dict:
    return {
        "auth_source": "env",
        "model_id": "claude-sonnet-4-20250514",
        "retry_policy": {"retry_on": ["429", "500", "502", "503", "529"], "max_attempts": 5},
        "cost_tracker_installed": True,
        "request_id_logged": True,
        "forbidden_seen": [],
    }


if __name__ == "__main__":
    import json

    print(json.dumps(fake_output(), indent=2))
```
