# M-LLM-008: Cost Optimization

## Overview

LLM cost optimization reduces API spending while maintaining output quality. Strategies include model selection, prompt optimization, caching, batching, and intelligent routing. Critical for production systems processing millions of requests.

**When to use:** Any production LLM deployment, especially at scale where costs can grow exponentially.

## Core Concepts

### 1. Cost Factors

| Factor | Impact | Optimization |
|--------|--------|--------------|
| **Model choice** | 10-100x difference | Use cheapest model that works |
| **Token count** | Linear cost | Shorter prompts, compression |
| **Caching** | 100% savings on hits | Cache frequent queries |
| **Batching** | Lower overhead | Group similar requests |
| **Provider** | 2-5x difference | Multi-provider strategy |

### 2. Model Pricing Comparison (2025)

| Model | Input $/1M tokens | Output $/1M tokens | Notes |
|-------|-------------------|--------------------| ------|
| GPT-4o | $2.50 | $10.00 | Best overall |
| GPT-4o-mini | $0.15 | $0.60 | 90%+ as good for many tasks |
| Claude 3.5 Sonnet | $3.00 | $15.00 | Best for long context |
| Claude 3 Haiku | $0.25 | $1.25 | Fast, cheap |
| Gemini 1.5 Flash | $0.075 | $0.30 | Very cheap, long context |
| Mistral Medium | $2.70 | $8.10 | European option |
| Llama 3.1 (hosted) | $0.20-1.00 | $0.20-1.00 | Varies by provider |

### 3. Cost Calculation

```python
def calculate_cost(
    model: str,
    input_tokens: int,
    output_tokens: int,
    pricing: dict
) -> float:
    input_cost = (input_tokens / 1_000_000) * pricing[model]["input"]
    output_cost = (output_tokens / 1_000_000) * pricing[model]["output"]
    return input_cost + output_cost

# Example
cost = calculate_cost(
    model="gpt-4o-mini",
    input_tokens=1000,
    output_tokens=500,
    pricing=PRICING
)
# ~$0.00015 + $0.00030 = $0.00045 per request
```

## Best Practices

### 1. Model Tiering Strategy

```python
class ModelRouter:
    def __init__(self):
        self.tiers = {
            "simple": "gpt-4o-mini",      # Classification, extraction
            "standard": "gpt-4o",          # Complex reasoning
            "complex": "claude-3-opus",    # Multi-step, creative
        }

    def classify_complexity(self, task: str) -> str:
        """Determine task complexity to select appropriate model."""

        simple_patterns = [
            "classify", "extract", "summarize short",
            "yes/no", "format", "translate simple"
        ]

        complex_patterns = [
            "analyze deeply", "creative writing",
            "multi-step reasoning", "code architecture",
            "long document", "debate"
        ]

        task_lower = task.lower()

        if any(p in task_lower for p in simple_patterns):
            return "simple"
        elif any(p in task_lower for p in complex_patterns):
            return "complex"
        return "standard"

    def get_model(self, task: str) -> str:
        complexity = self.classify_complexity(task)
        return self.tiers[complexity]
```

### 2. Prompt Optimization

```python
def optimize_prompt(prompt: str) -> str:
    """Reduce prompt tokens while preserving meaning."""

    optimizations = [
        # Remove redundant instructions
        (r"Please\s+", ""),
        (r"Could you\s+", ""),
        (r"I would like you to\s+", ""),

        # Shorten common phrases
        (r"in order to", "to"),
        (r"make sure to", "ensure"),
        (r"take into account", "consider"),

        # Remove filler words
        (r"\s+basically\s+", " "),
        (r"\s+actually\s+", " "),
        (r"\s+really\s+", " "),
    ]

    optimized = prompt
    for pattern, replacement in optimizations:
        optimized = re.sub(pattern, replacement, optimized, flags=re.IGNORECASE)

    return optimized.strip()

# Before: "Could you please take into account all the factors and basically summarize..."
# After: "Consider all factors and summarize..."
```

### 3. Semantic Caching

```python
from functools import lru_cache
import hashlib

class SemanticCache:
    def __init__(self, embedding_model, similarity_threshold=0.95):
        self.cache = {}
        self.embeddings = {}
        self.embedding_model = embedding_model
        self.threshold = similarity_threshold

    def get(self, query: str) -> Optional[str]:
        """Get cached response if similar query exists."""

        query_embedding = self.embedding_model.embed(query)

        for cached_query, cached_embedding in self.embeddings.items():
            similarity = cosine_similarity(query_embedding, cached_embedding)
            if similarity >= self.threshold:
                return self.cache[cached_query]

        return None

    def set(self, query: str, response: str):
        """Cache response with embedding."""

        query_embedding = self.embedding_model.embed(query)
        self.cache[query] = response
        self.embeddings[query] = query_embedding

    def get_or_generate(self, query: str, generator_func) -> str:
        """Get from cache or generate and cache."""

        cached = self.get(query)
        if cached:
            return cached

        response = generator_func(query)
        self.set(query, response)
        return response
```

## Common Patterns

### Pattern 1: Request Batching

```python
import asyncio
from typing import List

class BatchProcessor:
    def __init__(self, batch_size: int = 10, max_wait_ms: int = 100):
        self.batch_size = batch_size
        self.max_wait_ms = max_wait_ms
        self.pending: List[dict] = []
        self.lock = asyncio.Lock()

    async def add_request(self, request: dict) -> str:
        """Add request to batch, process when ready."""

        future = asyncio.Future()

        async with self.lock:
            self.pending.append({"request": request, "future": future})

            if len(self.pending) >= self.batch_size:
                await self._process_batch()

        # Wait for result
        return await future

    async def _process_batch(self):
        """Process accumulated requests as batch."""

        batch = self.pending[:self.batch_size]
        self.pending = self.pending[self.batch_size:]

        # Single API call with multiple inputs
        requests = [item["request"] for item in batch]
        responses = await self._batch_call(requests)

        # Distribute results
        for item, response in zip(batch, responses):
            item["future"].set_result(response)

    async def _batch_call(self, requests: List[dict]) -> List[str]:
        """Make batch API call (model-specific implementation)."""
        # Implementation depends on provider
        pass
```

### Pattern 2: Intelligent Fallback

```python
class CostAwareLLM:
    def __init__(self):
        self.models = [
            {"name": "gpt-4o-mini", "cost": 0.00015, "quality_threshold": 0.8},
            {"name": "gpt-4o", "cost": 0.0025, "quality_threshold": 0.9},
            {"name": "claude-3-opus", "cost": 0.015, "quality_threshold": 0.95},
        ]

    async def generate(self, prompt: str, min_quality: float = 0.8) -> dict:
        """Start cheap, escalate if quality insufficient."""

        for model_config in self.models:
            if model_config["quality_threshold"] < min_quality:
                continue

            response = await call_model(model_config["name"], prompt)

            # Quick quality check
            quality_score = self._assess_quality(response, prompt)

            if quality_score >= min_quality:
                return {
                    "response": response,
                    "model": model_config["name"],
                    "cost": model_config["cost"],
                    "quality": quality_score
                }

        # Final fallback to best model
        return await self._use_best_model(prompt)
```

### Pattern 3: Token Budget Management

```python
class TokenBudget:
    def __init__(self, daily_budget: float, alert_threshold: float = 0.8):
        self.daily_budget = daily_budget
        self.alert_threshold = alert_threshold
        self.spent_today = 0.0
        self.last_reset = datetime.now().date()

    def can_spend(self, estimated_cost: float) -> bool:
        """Check if request is within budget."""

        self._check_reset()
        return (self.spent_today + estimated_cost) <= self.daily_budget

    def record_spend(self, actual_cost: float):
        """Record actual spending."""

        self._check_reset()
        self.spent_today += actual_cost

        if self.spent_today >= self.daily_budget * self.alert_threshold:
            self._send_alert()

    def _check_reset(self):
        """Reset counter at midnight."""

        today = datetime.now().date()
        if today > self.last_reset:
            self.spent_today = 0.0
            self.last_reset = today

    def _send_alert(self):
        """Alert when approaching budget limit."""

        remaining = self.daily_budget - self.spent_today
        logger.warning(f"Budget alert: ${remaining:.2f} remaining today")
```

### Pattern 4: Multi-Provider Strategy

```python
class MultiProviderRouter:
    def __init__(self):
        self.providers = {
            "openai": {
                "models": ["gpt-4o", "gpt-4o-mini"],
                "health": True,
                "latency_ms": 500
            },
            "anthropic": {
                "models": ["claude-3-sonnet", "claude-3-haiku"],
                "health": True,
                "latency_ms": 600
            },
            "google": {
                "models": ["gemini-1.5-pro", "gemini-1.5-flash"],
                "health": True,
                "latency_ms": 400
            }
        }

        self.model_mapping = {
            "fast_cheap": ["gemini-1.5-flash", "gpt-4o-mini", "claude-3-haiku"],
            "balanced": ["gpt-4o", "claude-3-sonnet", "gemini-1.5-pro"],
            "best": ["claude-3-opus", "gpt-4-turbo"]
        }

    def get_best_option(self, tier: str = "balanced") -> str:
        """Select best available model for tier."""

        for model in self.model_mapping[tier]:
            provider = self._get_provider(model)
            if self.providers[provider]["health"]:
                return model

        raise Exception("No healthy providers available")

    def _get_provider(self, model: str) -> str:
        for provider, config in self.providers.items():
            if model in config["models"]:
                return provider
        return None
```

## Anti-patterns

| Anti-pattern | Cost Impact | Solution |
|--------------|-------------|----------|
| Using GPT-4 for everything | 10-100x overspend | Model tiering |
| No caching | Redundant calls | Semantic cache |
| Verbose prompts | +50% tokens | Prompt optimization |
| No monitoring | Uncontrolled spend | Budget alerts |
| Single provider | No fallback pricing | Multi-provider |

## Monitoring Dashboard Metrics

```python
metrics_to_track = {
    "cost": {
        "total_daily_cost": "$",
        "cost_per_request": "$",
        "cost_by_model": {"model": "$"},
        "cost_by_task_type": {"task": "$"}
    },
    "usage": {
        "requests_per_hour": "count",
        "tokens_in_per_request": "avg",
        "tokens_out_per_request": "avg",
        "cache_hit_rate": "%"
    },
    "efficiency": {
        "cost_per_successful_task": "$",
        "model_utilization": {"model": "%"},
        "wasted_tokens": "count"
    }
}
```

## Tools & References

### Related Skills
- faion-openai-api-skill
- faion-claude-api-skill
- faion-gemini-api-skill

### Related Agents
- faion-cost-optimizer-agent

### External Resources
- [OpenAI Pricing](https://openai.com/pricing)
- [Anthropic Pricing](https://www.anthropic.com/pricing)
- [LiteLLM](https://github.com/BerriAI/litellm) - Multi-provider gateway
- [Portkey](https://portkey.ai/) - LLM gateway with cost tracking

## Checklist

- [ ] Analyzed current spending patterns
- [ ] Implemented model tiering
- [ ] Set up semantic caching
- [ ] Optimized prompt lengths
- [ ] Added request batching
- [ ] Configured budget limits
- [ ] Set up multi-provider routing
- [ ] Created cost monitoring dashboard
- [ ] Established cost alerts
- [ ] Documented optimization decisions

---

*Methodology: M-LLM-008 | Category: LLM/Orchestration*
*Related: faion-cost-optimizer-agent, faion-openai-api-skill, faion-claude-api-skill*
