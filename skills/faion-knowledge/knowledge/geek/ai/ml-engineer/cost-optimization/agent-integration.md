# Agent Integration — LLM Cost Optimization

## When to use
- Monthly LLM spend exceeds $500 and is growing faster than revenue
- Agentic pipelines with >10K requests/day where model selection matters
- Batch workloads with >1h latency tolerance (Batch API = 50% off)
- System prompts >1K tokens that repeat across many calls (prompt caching)
- Multi-step pipelines where early stages can use cheap models for routing

## When NOT to use
- Early prototype phase — optimize only after measuring; premature optimization wastes time
- Tasks where quality degradation from cheaper models is unacceptable (medical, legal, safety-critical)
- Very low volume (<100 calls/day) — savings are negligible, complexity is not worth it
- When the cost driver is output tokens on complex reasoning tasks — only better prompts help, not routing

## Where it fails / limitations
- Semantic caching has a cache poisoning risk: stale cached responses served for updated queries if TTL is too long
- Model routing classifiers themselves cost tokens — routing overhead can exceed savings on short tasks
- Prompt caching requires the static prefix to be at least 1024 tokens (OpenAI) or 2048 tokens (Claude) to activate
- Response caching with temperature>0 returns stale creative outputs that users notice
- Aggressive token reduction (removing "please", verbose instructions) can break models trained on verbose instruction-following
- Cost dashboards lag by 15-60 minutes — real-time budget caps require separate token counting, not API usage data

## Agentic workflow
Agents apply cost optimization in two layers: routing (which model) and caching (avoid calling at all). A lightweight classifier agent (Haiku/gpt-4o-mini) reads the task complexity score and routes to Sonnet or Opus. Before any LLM call, a cache lookup checks Redis for exact match (temperature=0) or semantic match (embedding similarity >0.95). The agent pipeline itself should be instrumented to emit per-step token counts, enabling offline analysis of which stages drive the most cost. Budget watchdog agents fire alerts at 80% of daily cap and kill non-critical calls at 100%.

### Recommended subagents
- Any routing agent using a nano/mini model as the classifier
- `faion-sdd-execution` — uses cheaper models for planning steps, Opus only for critical decisions

### Prompt pattern
Simple model router:
```python
from anthropic import Anthropic

client = Anthropic()

def classify_complexity(task: str) -> str:
    """Returns: simple | medium | complex"""
    resp = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=10,
        messages=[{"role": "user", "content": f"Classify task complexity (simple/medium/complex): {task[:200]}"}],
    )
    return resp.content[0].text.strip().lower()

def route_model(task: str) -> str:
    tier = classify_complexity(task)
    return {"simple": "claude-haiku-4-5", "medium": "claude-sonnet-4-5", "complex": "claude-opus-4-5"}.get(tier, "claude-sonnet-4-5")
```

Prompt caching (Claude):
```python
import anthropic

client = anthropic.Anthropic()
SYSTEM = "You are an expert analyst. [... 2000+ token static context ...]"

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    system=[{"type": "text", "text": SYSTEM, "cache_control": {"type": "ephemeral"}}],
    messages=[{"role": "user", "content": "Analyze: ..."}],
)
# Second call with same system prompt hits cache: 90% input cost reduction
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `tiktoken` | Count tokens before sending to estimate cost | `pip install tiktoken` / github.com/openai/tiktoken |
| `anthropic` SDK | Access Claude prompt caching, token counting | `pip install anthropic` / docs.anthropic.com |
| `redis-py` | Response cache backend (exact + semantic) | `pip install redis` / redis.readthedocs.io |
| `litellm` | Unified interface with built-in cost tracking | `pip install litellm` / docs.litellm.ai |
| Langfuse CLI | Query cost analytics, export spend breakdowns | pip install langfuse / langfuse.com/docs |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| OpenAI Batch API | SaaS | Yes | 50% discount; 24h window; submit JSONL, poll for results |
| Anthropic Batch API | SaaS | Yes | Same 50% discount; async job-based |
| Helicone | SaaS (proxy) | Yes | Per-call cost tracking + semantic caching; 1-line integration |
| LiteLLM | OSS | Yes | Cost tracking across providers; proxy with budget enforcement |
| Redis / Valkey | OSS | Yes | Exact-match response cache; <1ms lookup |
| Portkey | SaaS | Yes | Multi-provider fallback routes to cheapest available model |

## Templates & scripts
See `templates.md` for: model router class, prompt cache wrapper, batch job submitter, daily cost alert script.

Inline: token budget enforcer for agent loops (~30 lines):

```python
class TokenBudget:
    def __init__(self, daily_limit_usd: float):
        self.limit = daily_limit_usd
        self.spent = 0.0

    PRICES = {  # per 1M tokens
        "claude-haiku-4-5": {"in": 0.80, "out": 4.00},
        "claude-sonnet-4-5": {"in": 3.00, "out": 15.00},
        "claude-opus-4-5": {"in": 15.00, "out": 75.00},
    }

    def record(self, model: str, input_tokens: int, output_tokens: int):
        p = self.PRICES.get(model, {"in": 3.00, "out": 15.00})
        cost = (input_tokens * p["in"] + output_tokens * p["out"]) / 1_000_000
        self.spent += cost
        if self.spent >= self.limit:
            raise RuntimeError(f"Daily budget ${self.limit} exceeded (${self.spent:.4f} spent)")
        return cost
```

## Best practices
- Track cost per pipeline stage from day 1, not total cost — you can't optimize what you can't attribute
- Use output token limits (`max_tokens`) as both a cost cap and a quality signal — if output truncates, the task is too broad
- Classify tasks by complexity with a cheap model before routing; even 5% misclassification is acceptable
- Cache at temperature=0 only; cache key = hash(model + system + user_message)
- Set separate budget caps for non-critical (news summarization) vs. critical (user-facing answers) pipelines
- Review top-10 most expensive agent calls weekly and redesign them — cost concentrates in a few patterns
- Always separate prompt caching metrics from semantic caching metrics — they have different failure modes

## AI-agent gotchas
- Human-in-loop checkpoint: when daily budget hits 80%, alert before automatic shutdowns — shutting down mid-pipeline corrupts state
- Semantic cache false positives: "what is the capital of France?" and "what is the capital of Germany?" may be semantically similar enough (>0.95 cosine) to return wrong cached answer — tune threshold carefully
- Batch API is async: agents that submit a batch and then wait inline will time out; use a separate completion-handler agent
- Cost routing adds complexity: if the routing classifier is wrong, you pay for a cheap model AND then escalate to an expensive one
- Prompt caching only activates when the prefix bytes match exactly — even a space change invalidates the cache

## References
- https://openai.com/pricing
- https://www.anthropic.com/pricing
- https://docs.litellm.ai/docs/budget_manager
- https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching
- https://github.com/openai/tiktoken
- https://deepsense.ai/blog/llm-inference-optimization-how-to-speed-up-cut-costs-and-scale-ai-models/
