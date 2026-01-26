# Cost Optimization Examples

Production-ready code examples for LLM cost optimization.

## Cost Tracking

```python
from dataclasses import dataclass
from typing import Dict, Optional
from datetime import datetime
import tiktoken

@dataclass
class ModelPricing:
    """Pricing per 1M tokens (2025 rates)."""
    input_per_1m: float
    output_per_1m: float

# Current pricing - update as needed
PRICING = {
    # OpenAI
    "gpt-4.1": ModelPricing(2.00, 8.00),
    "gpt-4.1-mini": ModelPricing(0.40, 1.60),
    "gpt-4.1-nano": ModelPricing(0.10, 0.40),
    "gpt-4o": ModelPricing(2.50, 10.00),
    "gpt-4o-mini": ModelPricing(0.15, 0.60),
    "o3-mini": ModelPricing(1.10, 4.40),
    # Anthropic
    "claude-4-opus-20250514": ModelPricing(15.00, 75.00),
    "claude-4-sonnet-20250514": ModelPricing(3.00, 15.00),
    "claude-3-5-haiku-20250514": ModelPricing(0.80, 4.00),
    # Google
    "gemini-2.0-pro": ModelPricing(1.25, 5.00),
    "gemini-2.0-flash": ModelPricing(0.10, 0.40),
}


class CostTracker:
    """Track LLM API costs in real-time."""

    def __init__(self, budget_limit: Optional[float] = None):
        self.calls: list[dict] = []
        self.total_cost = 0.0
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.budget_limit = budget_limit

    def record(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int,
        metadata: Optional[Dict] = None
    ) -> float:
        """Record API call and return cost."""
        pricing = PRICING.get(model)
        if not pricing:
            cost = 0.0
        else:
            cost = (
                (input_tokens / 1_000_000) * pricing.input_per_1m +
                (output_tokens / 1_000_000) * pricing.output_per_1m
            )

        self.calls.append({
            "timestamp": datetime.now().isoformat(),
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost": cost,
            "metadata": metadata or {}
        })

        self.total_cost += cost
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens

        return cost

    def is_over_budget(self) -> bool:
        """Check if budget exceeded."""
        if self.budget_limit is None:
            return False
        return self.total_cost >= self.budget_limit

    def get_summary(self) -> Dict:
        """Get cost breakdown by model."""
        by_model: Dict[str, dict] = {}
        for call in self.calls:
            model = call["model"]
            if model not in by_model:
                by_model[model] = {"calls": 0, "cost": 0.0, "tokens": 0}
            by_model[model]["calls"] += 1
            by_model[model]["cost"] += call["cost"]
            by_model[model]["tokens"] += call["input_tokens"] + call["output_tokens"]

        return {
            "total_cost": round(self.total_cost, 6),
            "total_calls": len(self.calls),
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "by_model": by_model,
            "avg_cost_per_call": round(
                self.total_cost / len(self.calls), 6
            ) if self.calls else 0
        }
```

## Response Caching

```python
import hashlib
import json
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import redis

class ResponseCache:
    """Multi-tier response cache: memory + Redis."""

    def __init__(
        self,
        redis_client: Optional[redis.Redis] = None,
        ttl_hours: int = 24,
        max_memory_items: int = 1000
    ):
        self.redis = redis_client
        self.ttl = timedelta(hours=ttl_hours)
        self.memory_cache: Dict[str, Dict] = {}
        self.max_memory_items = max_memory_items
        self.hits = 0
        self.misses = 0

    def _make_key(
        self,
        model: str,
        messages: list,
        **kwargs
    ) -> str:
        """Create deterministic cache key."""
        key_data = {
            "model": model,
            "messages": messages,
            "temperature": kwargs.get("temperature", 1.0),
            "max_tokens": kwargs.get("max_tokens"),
            "tools": kwargs.get("tools"),
        }
        key_str = json.dumps(key_data, sort_keys=True)
        return hashlib.sha256(key_str.encode()).hexdigest()

    def get(
        self,
        model: str,
        messages: list,
        **kwargs
    ) -> Optional[str]:
        """Get cached response."""
        # Only cache deterministic requests
        if kwargs.get("temperature", 1.0) != 0:
            return None

        key = self._make_key(model, messages, **kwargs)

        # Check memory first
        if key in self.memory_cache:
            entry = self.memory_cache[key]
            if datetime.now() < entry["expires"]:
                self.hits += 1
                return entry["response"]
            del self.memory_cache[key]

        # Check Redis
        if self.redis:
            cached = self.redis.get(f"llm:{key}")
            if cached:
                self.hits += 1
                response = json.loads(cached)
                # Warm memory cache
                self._set_memory(key, response)
                return response

        self.misses += 1
        return None

    def set(
        self,
        model: str,
        messages: list,
        response: str,
        **kwargs
    ):
        """Cache response."""
        if kwargs.get("temperature", 1.0) != 0:
            return

        key = self._make_key(model, messages, **kwargs)
        self._set_memory(key, response)

        if self.redis:
            self.redis.setex(
                f"llm:{key}",
                int(self.ttl.total_seconds()),
                json.dumps(response)
            )

    def _set_memory(self, key: str, response: str):
        """Set memory cache with eviction."""
        if len(self.memory_cache) >= self.max_memory_items:
            # Evict oldest 10%
            oldest = sorted(
                self.memory_cache.items(),
                key=lambda x: x[1]["created"]
            )[:self.max_memory_items // 10]
            for k, _ in oldest:
                del self.memory_cache[k]

        self.memory_cache[key] = {
            "response": response,
            "created": datetime.now(),
            "expires": datetime.now() + self.ttl
        }

    @property
    def hit_rate(self) -> float:
        """Cache hit rate percentage."""
        total = self.hits + self.misses
        return (self.hits / total * 100) if total > 0 else 0.0
```

## Model Routing

```python
from enum import Enum
from dataclasses import dataclass
from typing import Optional, Callable
import re

class TaskComplexity(Enum):
    SIMPLE = "simple"      # Classification, extraction
    MEDIUM = "medium"      # General chat, summaries
    COMPLEX = "complex"    # Reasoning, analysis, code

@dataclass
class ModelConfig:
    name: str
    max_context: int
    capabilities: list[str]

class ModelRouter:
    """Route requests to cost-appropriate models."""

    def __init__(self):
        self.models = {
            TaskComplexity.SIMPLE: ModelConfig(
                name="gpt-4.1-nano",
                max_context=128_000,
                capabilities=["classification", "extraction", "simple_qa"]
            ),
            TaskComplexity.MEDIUM: ModelConfig(
                name="gpt-4.1-mini",
                max_context=1_000_000,
                capabilities=["chat", "summarization", "translation"]
            ),
            TaskComplexity.COMPLEX: ModelConfig(
                name="gpt-4.1",
                max_context=1_000_000,
                capabilities=["reasoning", "code", "analysis", "creative"]
            )
        }

        # Custom classifiers
        self.classifiers: list[Callable[[str], Optional[TaskComplexity]]] = []

    def add_classifier(
        self,
        classifier: Callable[[str], Optional[TaskComplexity]]
    ):
        """Add custom complexity classifier."""
        self.classifiers.append(classifier)

    def classify(self, prompt: str) -> TaskComplexity:
        """Classify task complexity."""
        # Custom classifiers first
        for classifier in self.classifiers:
            result = classifier(prompt)
            if result is not None:
                return result

        # Heuristic classification
        prompt_lower = prompt.lower()

        # Complex indicators
        complex_patterns = [
            r"analyze|evaluate|compare",
            r"step by step|chain of thought",
            r"write (?:a |the )?(?:code|function|script)",
            r"debug|fix|refactor",
            r"explain (?:in detail|why|how)",
            r"multiple (?:perspectives|approaches)",
        ]

        # Simple indicators
        simple_patterns = [
            r"^(?:yes|no)\??$",
            r"translate .{1,50} to",
            r"^what is .{1,30}\??$",
            r"list .{1,20}$",
            r"classify|categorize|label",
            r"extract .{1,30} from",
        ]

        complex_score = sum(
            1 for p in complex_patterns
            if re.search(p, prompt_lower)
        )
        simple_score = sum(
            1 for p in simple_patterns
            if re.search(p, prompt_lower)
        )

        # Length heuristics
        if len(prompt) > 3000:
            complex_score += 1
        elif len(prompt) < 100:
            simple_score += 1

        if complex_score >= 2:
            return TaskComplexity.COMPLEX
        elif simple_score >= 2 or (simple_score >= 1 and complex_score == 0):
            return TaskComplexity.SIMPLE
        return TaskComplexity.MEDIUM

    def get_model(
        self,
        prompt: str,
        force_complexity: Optional[TaskComplexity] = None,
        require_capability: Optional[str] = None
    ) -> str:
        """Get appropriate model for task."""
        complexity = force_complexity or self.classify(prompt)

        # Check capability requirements
        if require_capability:
            for c in [TaskComplexity.COMPLEX, TaskComplexity.MEDIUM, TaskComplexity.SIMPLE]:
                if require_capability in self.models[c].capabilities:
                    complexity = max(complexity, c, key=lambda x: x.value)
                    break

        return self.models[complexity].name
```

## Prompt Optimization

```python
import re
from typing import Optional
import tiktoken

class PromptOptimizer:
    """Optimize prompts for token efficiency."""

    def __init__(self, model: str = "gpt-4o"):
        try:
            self.encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            self.encoding = tiktoken.get_encoding("cl100k_base")

    def count_tokens(self, text: str) -> int:
        """Count tokens in text."""
        return len(self.encoding.encode(text))

    def truncate(self, text: str, max_tokens: int) -> str:
        """Truncate to max tokens."""
        tokens = self.encoding.encode(text)
        if len(tokens) <= max_tokens:
            return text
        return self.encoding.decode(tokens[:max_tokens])

    def compress(self, prompt: str) -> str:
        """Apply compression techniques."""
        result = prompt

        # Normalize whitespace
        result = re.sub(r'\s+', ' ', result)
        result = re.sub(r'\n\s*\n', '\n', result)

        # Remove filler phrases
        fillers = [
            r"please\s+",
            r"kindly\s+",
            r"could you please\s+",
            r"i would like you to\s+",
            r"i need you to\s+",
            r"can you\s+",
            r"would you\s+",
        ]
        for filler in fillers:
            result = re.sub(filler, "", result, flags=re.IGNORECASE)

        return result.strip()

    def optimize_system_prompt(self, system: str) -> str:
        """Optimize system prompt."""
        result = system

        verbose_map = {
            "You are a helpful assistant that": "You",
            "You are an AI assistant": "You",
            "Please make sure to": "",
            "It is important that you": "",
            "Remember to always": "",
            "Your task is to": "",
            "Please respond with": "Respond with",
            "Please provide": "Provide",
        }

        for verbose, concise in verbose_map.items():
            result = result.replace(verbose, concise)

        return self.compress(result)

    def estimate_cost(
        self,
        prompt: str,
        system: str = "",
        model: str = "gpt-4.1-mini",
        expected_output_tokens: int = 500
    ) -> dict:
        """Estimate request cost."""
        input_tokens = self.count_tokens(prompt) + self.count_tokens(system)
        pricing = PRICING.get(model)

        if not pricing:
            return {"error": f"Unknown model: {model}"}

        input_cost = (input_tokens / 1_000_000) * pricing.input_per_1m
        output_cost = (expected_output_tokens / 1_000_000) * pricing.output_per_1m

        return {
            "model": model,
            "input_tokens": input_tokens,
            "expected_output_tokens": expected_output_tokens,
            "input_cost": round(input_cost, 6),
            "output_cost": round(output_cost, 6),
            "total_cost": round(input_cost + output_cost, 6)
        }
```

## Batch Processing

```python
import asyncio
from typing import List, Optional, Any
from dataclasses import dataclass
from openai import AsyncOpenAI

@dataclass
class BatchResult:
    prompt: str
    response: Optional[str]
    error: Optional[str]
    tokens_used: int

class BatchProcessor:
    """Efficient batch processing with rate limiting."""

    def __init__(
        self,
        client: AsyncOpenAI,
        batch_size: int = 32,
        max_concurrent: int = 10,
        delay_between_batches: float = 0.1
    ):
        self.client = client
        self.batch_size = batch_size
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.delay = delay_between_batches

    async def process(
        self,
        prompts: List[str],
        model: str = "gpt-4.1-mini",
        system: str = "",
        **kwargs
    ) -> List[BatchResult]:
        """Process prompts in parallel batches."""
        results: List[BatchResult] = []

        for i in range(0, len(prompts), self.batch_size):
            batch = prompts[i:i + self.batch_size]

            tasks = [
                self._process_one(prompt, model, system, **kwargs)
                for prompt in batch
            ]

            batch_results = await asyncio.gather(*tasks)
            results.extend(batch_results)

            # Rate limit between batches
            if i + self.batch_size < len(prompts):
                await asyncio.sleep(self.delay)

        return results

    async def _process_one(
        self,
        prompt: str,
        model: str,
        system: str,
        **kwargs
    ) -> BatchResult:
        """Process single request with semaphore."""
        async with self.semaphore:
            try:
                messages = []
                if system:
                    messages.append({"role": "system", "content": system})
                messages.append({"role": "user", "content": prompt})

                response = await self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    **kwargs
                )

                return BatchResult(
                    prompt=prompt,
                    response=response.choices[0].message.content,
                    error=None,
                    tokens_used=response.usage.total_tokens
                )
            except Exception as e:
                return BatchResult(
                    prompt=prompt,
                    response=None,
                    error=str(e),
                    tokens_used=0
                )
```

## Production Service

```python
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import logging

@dataclass
class CostConfig:
    """Cost optimization configuration."""
    enable_caching: bool = True
    enable_routing: bool = True
    enable_compression: bool = True
    cache_ttl_hours: int = 24
    default_model: str = "gpt-4.1-mini"
    fallback_model: str = "gpt-4.1"
    daily_budget: Optional[float] = None
    max_retries: int = 3

class CostOptimizedLLM:
    """Production LLM service with cost optimization."""

    def __init__(
        self,
        client,
        config: Optional[CostConfig] = None,
        redis_client=None
    ):
        self.client = client
        self.config = config or CostConfig()
        self.logger = logging.getLogger(__name__)

        # Initialize components
        self.cache = ResponseCache(
            redis_client=redis_client,
            ttl_hours=self.config.cache_ttl_hours
        )
        self.router = ModelRouter()
        self.optimizer = PromptOptimizer()
        self.tracker = CostTracker(budget_limit=self.config.daily_budget)

    def complete(
        self,
        prompt: str,
        system: str = "",
        model: Optional[str] = None,
        use_cache: bool = True,
        **kwargs
    ) -> Dict[str, Any]:
        """Get completion with all optimizations."""
        # Budget check
        if self.tracker.is_over_budget():
            raise RuntimeError("Daily budget exceeded")

        # Optimize prompts
        if self.config.enable_compression:
            prompt = self.optimizer.compress(prompt)
            system = self.optimizer.optimize_system_prompt(system)

        # Build messages
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        # Select model
        if model:
            selected_model = model
        elif self.config.enable_routing:
            selected_model = self.router.get_model(prompt)
        else:
            selected_model = self.config.default_model

        # Check cache
        if self.config.enable_caching and use_cache:
            cached = self.cache.get(selected_model, messages, **kwargs)
            if cached:
                self.logger.debug(f"Cache hit: {selected_model}")
                return {
                    "content": cached,
                    "model": selected_model,
                    "cached": True,
                    "cost": 0.0
                }

        # API call with retry
        for attempt in range(self.config.max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=selected_model,
                    messages=messages,
                    **kwargs
                )
                break
            except Exception as e:
                if attempt == self.config.max_retries - 1:
                    # Final attempt: try fallback
                    self.logger.warning(
                        f"{selected_model} failed, using fallback"
                    )
                    response = self.client.chat.completions.create(
                        model=self.config.fallback_model,
                        messages=messages,
                        **kwargs
                    )
                    selected_model = self.config.fallback_model

        content = response.choices[0].message.content

        # Track cost
        cost = self.tracker.record(
            model=selected_model,
            input_tokens=response.usage.prompt_tokens,
            output_tokens=response.usage.completion_tokens
        )

        # Cache response
        if self.config.enable_caching and use_cache:
            self.cache.set(selected_model, messages, content, **kwargs)

        return {
            "content": content,
            "model": selected_model,
            "cached": False,
            "cost": cost,
            "tokens": {
                "input": response.usage.prompt_tokens,
                "output": response.usage.completion_tokens
            }
        }

    def get_report(self) -> Dict:
        """Get cost and cache report."""
        return {
            "cost": self.tracker.get_summary(),
            "cache_hit_rate": f"{self.cache.hit_rate:.1f}%"
        }
```

## Usage Example

```python
from openai import OpenAI

# Initialize
client = OpenAI()
llm = CostOptimizedLLM(
    client=client,
    config=CostConfig(
        enable_caching=True,
        enable_routing=True,
        daily_budget=10.00  # $10/day limit
    )
)

# Simple query → routes to nano/mini
result = llm.complete(
    prompt="What is Python?",
    temperature=0  # Enable caching
)
print(f"Model: {result['model']}, Cost: ${result['cost']:.6f}")

# Complex query → routes to full model
result = llm.complete(
    prompt="Analyze the trade-offs between microservices and monolith architecture for a startup with 5 engineers",
    system="You are a senior software architect."
)
print(f"Model: {result['model']}, Cost: ${result['cost']:.6f}")

# Get report
print(llm.get_report())
```
