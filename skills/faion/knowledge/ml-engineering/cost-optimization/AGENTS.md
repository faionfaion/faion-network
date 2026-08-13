# LLM Cost Optimization

## Summary

**One-sentence:** Produces a per-pipeline cost plan combining model routing, prompt caching, response caching, token reduction, and Batch API rules that mechanically reduces LLM spend 60-90% with measurable per-stage attribution.

**One-paragraph:** LLM cost scales super-linearly: every agent turn, pipeline stage, and user query multiplies, output tokens cost 3-5× input tokens, and the most-expensive model becomes the default if no router exists. This methodology installs a layered cost floor — (1) a Haiku-grade classifier routes simple traffic away from Opus, (2) cache_control markers cover system prompts ≥1024/2048 tokens that repeat, (3) deterministic queries get a Redis response cache, (4) offline workloads ≥1h-tolerant ship through Batch API at 50% off, (5) every call carries a token-budget guard that breaks before the daily limit. Optimization is forbidden before measurement: a per-stage cost dashboard MUST exist before any router or cache is enabled.

**Ефективно для:**

- Production-сервісів зі spend ≥$500/міс і трендом росту швидше за виручку — це фінальний шар перед урізанням scope.
- Agentic pipelines з ≥10k requests/day, де неоптимізований routing спалює бюджет на класифікаціях у frontier-моделях.
- Офлайн enrichment workload-ів (теги, summary, embeddings prep) — Batch API ріже навпіл цілий шар.
- Команд із системними промптами ≥1k tokens (OpenAI) / ≥2k tokens (Claude), які повторюються — кеш дає 80-90% economy на input.
- FinOps-аудиту: per-stage attribution робить overspend видимим, замість generic "усе LLM дороге".

## Applies If (ALL must hold)

- Monthly LLM spend has been measured and is ≥$500 OR is growing faster than user revenue.
- Per-stage cost attribution is available (or buildable in <1 day) — token logs tagged with pipeline_stage, model, user_id.
- At least one of: ≥10k requests/day, OR ≥1k-token repeated system prompts, OR ≥100 doc/day offline enrichment, OR multi-step pipeline with cheap-stage candidates.

## Skip If (ANY kills it)

- Pre-launch / prototype phase — quality and shape matter more; optimization is premature.
- <100 calls/day total — savings are below the engineering cost of building the router and cache.
- Workload is medical, legal, or safety-critical and any quality regression from cheaper models is unacceptable.
- Cost is dominated by output tokens on deep reasoning tasks — only prompt redesign helps; routing won't move the needle.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Per-stage cost dashboard | metrics tool URL | Observability stack (Langfuse, Helicone, internal) |
| Token logs tagged by stage | JSONL / DB rows | API gateway / SDK middleware |
| Pipeline DAG with stage list | YAML | Engineering directory |
| Quality SLO per stage | rubric / golden eval set | QA team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[decision-framework]] | Confirms approach (prompt vs RAG vs fine-tune) before the router is built. |
| [[model-evaluation]] | Defines the golden eval set used to verify quality after each cost cut. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: measure-before-optimize, route-by-complexity, cache-only-repeated-prefix, batch-the-offline, log-output-token-share, token-budget-guard | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the cost-plan artefact: router cfg, cache cfg, batch cfg, budget cfg, expected savings per stage | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: optimize-before-measure, route-everything-to-cheap, cache-on-low-traffic, batch-the-interactive, prompt-bloat-from-cache-misuse | 800 |
| `content/04-procedure.xml` | reference | 6-step procedure: instrument → classify → route → cache → batch → guard | 700 |
| `content/06-decision-tree.xml` | essential | Per-stage tree: stage cost share? offline-OK? prefix-stable? deterministic? → action | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify_request_complexity` | haiku-4-5 | Cheap routing decision; even 5% misclass is acceptable. |
| `draft_cost_plan` | sonnet-4-6 | Multi-input synthesis: pipeline DAG + cost dashboard + SLOs. |
| `audit_existing_setup` | opus-4-7 | Identify hidden output-token bloat and silent cache misses in legacy code. |

## Templates

| File | Purpose |
|------|---------|
| `templates/model-router.py` | Complexity-based router (Claude Haiku classifier → Sonnet/Opus). |
| `templates/prompt-cache-claude.py` | Prompt-caching helper with cache_control prefix layout. |
| `templates/token-budget.py` | Per-call cost tracker + daily budget enforcement. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-cost-optimization.py` | Validate a cost-plan artefact against the contract in `02-output-contract.xml`. | Pre-commit on the plan file; CI gate before applying router/cache changes. |

## Related

- [[decision-framework]] — chooses the approach before this methodology costs it.
- [[claude-api]] — implements caching + batching primitives this plan configures.
- [[model-evaluation]] — verifies quality is preserved after each cost cut.

## Decision tree

See `content/06-decision-tree.xml`. The tree walks per pipeline stage: first it asks whether the stage carries ≥10% of total cost (no → skip optimization, the win is too small). Then it branches by offline-tolerance (≥1h tolerance → Batch API). For online stages it asks whether the system prefix is ≥1024/2048 tokens and stable across requests (yes → caching). For deterministic queries (same input → same output) it adds a Redis response cache. Finally it asks whether classification cost is dominated by frontier-model use (yes → route via Haiku classifier). Every leaf cites a rule id from `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/model-router.py`

```python
"""
Complexity-based model router for Claude (Haiku → Sonnet → Opus).
Classifier uses Haiku for minimum overhead.
"""
from anthropic import Anthropic

client = Anthropic()

MODEL_MAP = {
    "simple": "claude-haiku-4-5",
    "medium": "claude-sonnet-4-5",
    "complex": "claude-opus-4-5",
}


def classify_complexity(task: str) -> str:
    """Returns: simple | medium | complex"""
    resp = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=10,
        messages=[{
            "role": "user",
            "content": (
                f"Classify task complexity as 'simple', 'medium', or 'complex'. "
                f"Output exactly one word.\nTask: {task[:200]}"
            ),
        }],
    )
    return resp.content[0].text.strip().lower()


def route_model(task: str) -> str:
    """Return the appropriate model name for the task."""
    tier = classify_complexity(task)
    return MODEL_MAP.get(tier, "claude-sonnet-4-5")


def routed_completion(task: str, max_tokens: int = 2048) -> str:
    """Complete a task using the cheapest model appropriate for its complexity."""
    model = route_model(task)
    resp = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": task}],
    )
    return resp.content[0].text
```

### `templates/prompt-cache-claude.py`

```python
"""
Claude prompt caching with cache_control header.
The static system prompt prefix must be >=2048 tokens to activate caching.
Place ALL dynamic content AFTER the cached static prefix.
"""
import anthropic

client = anthropic.Anthropic()

# Static system prompt (must be >=2048 tokens to activate cache)
STATIC_SYSTEM_PROMPT = """You are an expert analyst. [... 2000+ tokens of static context ...]"""


def analyze_with_cache(user_query: str) -> str:
    """
    Call Claude with prompt caching on the static system prompt.
    Second and subsequent calls with the same prefix pay cache read cost (~10% of full input).
    """
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        system=[
            {
                "type": "text",
                "text": STATIC_SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},  # Cache this prefix
            }
        ],
        messages=[{"role": "user", "content": user_query}],
    )

    # Check if cache was used
    usage = response.usage
    cache_hit = hasattr(usage, "cache_read_input_tokens") and usage.cache_read_input_tokens > 0

    return response.content[0].text
```

### `templates/token-budget.py`

```python
"""
Per-call token cost tracking with daily budget enforcement.
Record every API call; raise RuntimeError when daily limit is exceeded.
"""


class TokenBudget:
    """Track LLM spend and enforce a daily USD budget."""

    PRICES = {  # USD per 1M tokens (input, output)
        "claude-haiku-4-5": {"in": 0.80, "out": 4.00},
        "claude-sonnet-4-5": {"in": 3.00, "out": 15.00},
        "claude-opus-4-5": {"in": 15.00, "out": 75.00},
        "gpt-4o-mini": {"in": 0.15, "out": 0.60},
        "gpt-4o-2024-08-06": {"in": 2.50, "out": 10.00},
    }

    def __init__(self, daily_limit_usd: float):
        self.limit = daily_limit_usd
        self.spent = 0.0
        self.calls = 0

    def record(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """Record token usage and return cost for this call. Raises on budget exceeded."""
        prices = self.PRICES.get(model, {"in": 3.00, "out": 15.00})
        cost = (input_tokens * prices["in"] + output_tokens * prices["out"]) / 1_000_000
        self.spent += cost
        self.calls += 1
        if self.spent >= self.limit:
            raise RuntimeError(
                f"Daily budget ${self.limit:.2f} exceeded "
                f"(${self.spent:.4f} spent across {self.calls} calls)"
            )
        return cost

    def warn_at(self, threshold: float = 0.80) -> bool:
        """Return True if spend has reached the threshold fraction of limit."""
        return self.spent >= self.limit * threshold

    @property
    def remaining(self) -> float:
        return max(0.0, self.limit - self.spent)
```
