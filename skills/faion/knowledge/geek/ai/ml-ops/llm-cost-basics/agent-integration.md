# Agent Integration — LLM Cost Basics

## When to use
- Starting a new LLM project and needing a cost model before choosing a provider and model tier
- Setting up cost tracking for an existing API-based system to prevent surprise billing
- Implementing model routing to assign cheap models to simple tasks and expensive ones to complex tasks
- Preparing a budget estimate for a product feature that involves LLM calls
- Auditing existing LLM usage to find optimization opportunities

## When NOT to use
- The application makes fewer than 100 LLM calls per day — overhead of a full cost tracker is unnecessary; use provider dashboard directly
- The system uses only one model with no routing complexity — cost tracking at the provider level (dashboard alerts) is sufficient
- The primary optimization goal is latency, not cost — routing by complexity adds latency overhead that may not be acceptable
- Self-hosted models (Ollama, vLLM) — token-based pricing does not apply; cost model shifts to GPU infrastructure

## Where it fails / limitations
- The `ModelRouter.classify_complexity` heuristic uses keyword matching and prompt length — it misclassifies ambiguous prompts regularly and must be calibrated to actual task distributions
- Pricing in the README is from 2024-2025 and will be outdated — providers change prices without notice; always pull current pricing programmatically or cache with a TTL
- `tiktoken` uses `cl100k_base` encoding for cost estimates, but different models use different tokenizers; estimates for non-OpenAI models (Claude, Gemini) have 10-30% error
- `CostTracker` stores all calls in memory — in long-running processes this causes unbounded memory growth; add periodic flush to a database
- Output token cost is 3-10x input cost for most models, but the heuristic estimate of 500 output tokens is often wrong — measure empirically from production data before using for budgeting

## Agentic workflow
An agent implementing cost-aware LLM usage should classify each request's complexity before calling the model, route to the appropriate tier, record actual token usage and cost after the call, and surface budget alerts when cumulative cost crosses a threshold. For multi-agent pipelines, each subagent should pass its cost record back to the orchestrator so total pipeline cost can be tracked per user session or workflow run.

### Recommended subagents
- `faion-sdd-executor-agent` — drives cost-tracking implementation from task card
- A budget-monitor subagent (custom) — aggregates cost records from all subagents in a session, fires alerts when daily/monthly threshold is crossed

### Prompt pattern
```
Classify the following request by task complexity: simple | medium | complex.
Request: "{user_request}"
Return JSON: {"complexity": str, "rationale": str, "recommended_model": str}
Use these rules: simple = lookup/translation/yes-no; complex = multi-step reasoning/code/analysis.
```

```
Given today's LLM API spend: ${total_cost:.2f} and monthly budget: ${budget:.2f},
calculate burn rate and projected month-end spend.
Return JSON: {"on_track": bool, "projected_total": float, "action": str}
where action is one of: "continue", "reduce_model_tier", "alert_human".
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `tiktoken` | Count tokens for OpenAI models before API calls | `pip install tiktoken` / [github.com/openai/tiktoken](https://github.com/openai/tiktoken) |
| `anthropic` SDK | Built-in `usage` field in responses (input/output tokens) | `pip install anthropic` / [docs.anthropic.com](https://docs.anthropic.com) |
| `openai` SDK | `response.usage.prompt_tokens`, `completion_tokens` | `pip install openai` / [platform.openai.com](https://platform.openai.com/docs) |
| `litellm` | Unified cost tracking across providers | `pip install litellm` / [docs.litellm.ai](https://docs.litellm.ai) |
| Helicone CLI | Cost analytics via proxy (no code change required) | [docs.helicone.ai](https://docs.helicone.ai) |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Helicone | SaaS/OSS | Yes — proxy-based, no SDK change needed | Real-time cost dashboard, per-user/session breakdown |
| LiteLLM | OSS | Yes — Python SDK, unified pricing DB | Best cross-provider cost tracker; active pricing DB |
| OpenAI Usage Dashboard | SaaS | Partial — no API, manual inspection | Set spend limits and alerts in platform settings |
| Anthropic Console | SaaS | Partial — no cost API, use usage.tokens from SDK | Monitor via console; no programmatic budget alerts |
| Langfuse | SaaS/OSS | Yes — cost per trace via SDK | Combines cost with quality metrics; self-hostable |
| AWS Cost Explorer | SaaS | Yes — API | For Bedrock-based deployments |

## Templates & scripts
See `templates.md` for full `CostTracker` class with database persistence.

Inline — LiteLLM-based cost tracking across providers (≤25 lines):

```python
import litellm
from litellm import completion

litellm.success_callback = ["langfuse"]  # optional

def tracked_completion(model: str, messages: list, **kwargs) -> dict:
    response = completion(model=model, messages=messages, **kwargs)
    cost = litellm.completion_cost(completion_response=response)
    return {
        "content": response.choices[0].message.content,
        "input_tokens": response.usage.prompt_tokens,
        "output_tokens": response.usage.completion_tokens,
        "cost_usd": cost,
        "model": model,
    }

# Usage:
result = tracked_completion(
    model="claude-sonnet-4-5",
    messages=[{"role": "user", "content": "Explain photosynthesis"}],
)
print(f"Cost: ${result['cost_usd']:.6f}")
```

## Best practices
- Measure actual output token distribution from 50-100 real requests before using a cost model for budgeting — the 500-token default estimate is frequently 2-5x wrong
- Set provider-level spend limits (OpenAI: hard limit in platform settings; Anthropic: contact support) as a safety net in addition to application-level tracking
- Track cost per feature/endpoint, not just total spend — this reveals which features are cost drivers and where optimization has the highest ROI
- For multi-model routing, measure routing accuracy on a labeled sample before deploying — misrouted complex tasks to cheap models produce bad quality; misrouted simple tasks to expensive models waste budget
- Cache LLM responses for identical or near-identical inputs (Helicone caching, or semantic cache with Redis + embeddings) — 20-40% of production requests are often repeats
- Output tokens cost 3-10x input tokens; reducing response verbosity (system prompt: "be concise") can cut costs 30-50% without quality loss on factual tasks

## AI-agent gotchas
- Agents calling other agents (subagent chains) accumulate costs multiplicatively — the orchestrator must sum costs across all subagent calls, not just its own
- The `classify_complexity` heuristic will assign simple complexity to short prompts that require complex reasoning — agents must not rely on this as a quality gate, only as a cost heuristic
- Streaming responses (`stream=True`) do not return token counts in the initial response object for most providers; agents must count tokens client-side or use a post-stream callback
- Budget alerts based on daily totals can miss intra-day spikes — set hourly sub-budgets for high-volume systems
- Provider pricing APIs do not exist for most providers; hardcoded pricing tables go stale and cause underestimation — use LiteLLM which maintains an updated pricing DB

## References
- [OpenAI Pricing](https://openai.com/pricing)
- [Anthropic Pricing](https://www.anthropic.com/pricing)
- [Google AI Pricing](https://ai.google.dev/pricing)
- [LiteLLM Cost Tracking](https://docs.litellm.ai/docs/completion/token_usage)
- [Helicone — Cost Analytics](https://docs.helicone.ai/features/advanced-usage/costs)
- [tiktoken](https://github.com/openai/tiktoken)
- [OpenAI Production Best Practices — Costs](https://platform.openai.com/docs/guides/production-best-practices/managing-costs)
