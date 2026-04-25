# Agent Integration — Decision Framework (ML/AI Approach & Model Selection)

## When to use
- Starting a new AI feature and need to choose between prompt engineering, RAG, or fine-tuning
- Cost review: monthly API spend has grown and you suspect model over-selection
- Model migration: an existing model is deprecated or a cheaper/faster alternative is available
- Multi-task pipeline: different pipeline stages require different capability/cost trade-offs
- Evaluating whether a new LLM provider is worth switching to for a specific workload

## When NOT to use
- The task is trivial and the model is already decided (don't over-engineer the decision)
- A deadline is imminent — pick the safe default (Claude Sonnet 4 or GPT-4o) and optimize later
- The use case is purely creative (story generation, marketing copy) — model quality differences are subjective; user preference testing matters more than a framework

## Where it fails / limitations
- Cost comparison tables become stale within weeks as providers change pricing — treat as directional, not absolute
- Framework favors quantifiable factors (cost, latency, tokens) over hard-to-measure ones (trust, brand alignment, compliance)
- "Match model to complexity" advice requires prior knowledge of what "complex" means for your workload — benchmark first
- Fine-tuning ROI is often overestimated: 6x inference cost + training cost + maintenance rarely breaks even unless volume is very high (1M+ requests/month)
- Multi-model routing adds operational complexity: more failure modes, more SDKs to maintain, inconsistent output formatting

## Agentic workflow
An orchestrator agent receives a task description and routes it through the decision framework: it first checks whether external/private data is needed (→ RAG), then whether behavioral specialization is required (→ fine-tuning), and finally selects the appropriate model tier based on task complexity. For high-volume pipelines, a lightweight classifier subagent scores incoming tasks by complexity (simple/medium/complex) and routes them to DeepSeek, Sonnet, or Opus respectively, logging actual cost vs. quality to a metrics store for continuous optimization.

### Recommended subagents
- Complexity classifier subagent — lightweight Haiku/DeepSeek call that scores task complexity before routing to a heavier model
- Cost monitor subagent — reads Langfuse/Helicone traces, computes per-task cost, flags when routing decisions are suboptimal

### Prompt pattern
```
You are a task router. Given the following task description, output JSON:
{
  "approach": "prompt_engineering" | "rag" | "fine_tuning",
  "model": "haiku" | "sonnet" | "opus" | "deepseek",
  "reasoning": "<one sentence>"
}

Rules:
- If task requires external/private data: approach = "rag"
- If task requires domain-specific style/behavior and data is stable: approach = "fine_tuning"
- Otherwise: approach = "prompt_engineering"
- Map complexity (simple/medium/complex) to model tier
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `helicone` | LLM observability, cost tracking | [helicone.ai](https://www.helicone.ai/) |
| `langfuse` | Open-source LLM tracing | `pip install langfuse` — [langfuse.com](https://langfuse.com/) |
| `litellm` | Unified multi-provider SDK with routing | `pip install litellm` — [litellm.ai](https://docs.litellm.ai/) |
| `openrouter` | Multi-model API gateway | [openrouter.ai](https://openrouter.ai/) |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| LiteLLM | OSS | Yes — unified Python API | Supports 100+ models; built-in routing, fallbacks |
| OpenRouter | SaaS | Yes — OpenAI-compatible API | Single API key for all providers; real-time pricing |
| Helicone | SaaS + OSS | Yes — proxy layer | Cost analytics, request logging, model comparison |
| Langfuse | SaaS + OSS | Yes — SDK | Tracing, cost per trace, A/B model testing |
| Portkey | SaaS | Yes — gateway | Fallbacks, load balancing, semantic caching |

## Templates & scripts
See `templates.md` for decision document templates and model selection matrices.

Inline: LiteLLM router with complexity-based routing (< 50 lines):

```python
from litellm import Router

router = Router(
    model_list=[
        {"model_name": "fast", "litellm_params": {"model": "deepseek/deepseek-chat"}},
        {"model_name": "balanced", "litellm_params": {"model": "anthropic/claude-sonnet-4-20250514"}},
        {"model_name": "powerful", "litellm_params": {"model": "anthropic/claude-opus-4-5-20251101"}},
    ]
)

def route_by_complexity(task: str, complexity: str) -> str:
    model_map = {"simple": "fast", "medium": "balanced", "complex": "powerful"}
    model = model_map.get(complexity, "balanced")
    response = router.completion(
        model=model,
        messages=[{"role": "user", "content": task}],
    )
    return response.choices[0].message.content
```

## Best practices
- Default to Claude Sonnet 4 for balanced tasks — it's faster and significantly cheaper than Opus with comparable quality for most workloads
- Calculate total cost of ownership: API cost + developer fix-time + prompt engineering time — simple models may require more prompt engineering, erasing savings
- Route simple classification/extraction to DeepSeek V3 or Haiku; reserve Opus for verifiable reasoning where errors cost real money
- Measure before optimizing: deploy with one model, collect traces for 2 weeks, then apply routing logic based on real task distribution
- Re-evaluate the framework quarterly — model pricing and capabilities shift dramatically (DeepSeek V3 cut prices ~10x vs GPT-4o equivalents in late 2024)
- Latency budgets matter for UX: 10s+ responses (Opus) break user experience in synchronous flows; use async/batch for long-running tasks

## AI-agent gotchas
- Multi-model routing introduces inconsistent output formats — if one pipeline stage uses Opus and another uses Haiku, the output schema must be enforced via structured output on every model
- Model fallback chains must be tested: if Opus is unavailable, the fallback to Sonnet should produce acceptable (not just non-empty) output — test the fallback path explicitly
- Human-in-loop checkpoint: before switching a production pipeline from a capable model (Opus) to a cheaper one (DeepSeek), run a side-by-side quality evaluation with a human reviewer on a representative sample
- Cost alerts: set a hard budget cap in Helicone/Langfuse to catch runaway agentic loops that call expensive models in a retry loop
- Fine-tuning decision is irreversible in the short term — committing to fine-tuning a model means maintaining the dataset and retraining as the base model updates

## References
- [Helicone LLM Model Comparison Guide](https://www.helicone.ai/blog/the-complete-llm-model-comparison-guide)
- [O'Reilly: LLM System Design and Model Selection](https://www.oreilly.com/radar/llm-system-design-and-model-selection/)
- [LiteLLM Router docs](https://docs.litellm.ai/docs/routing)
- [Langfuse cost tracking](https://langfuse.com/docs/model-usage-and-cost)
- [Beyond the Pareto Frontier: pricing LLM mistakes](https://cognaptus.com/blog/2025-07-08-beyond-the-pareto-frontier-pricing-llm-mistakes-in-the-real-world/)
