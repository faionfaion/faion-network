# Cost Optimization Templates

Ready-to-use templates for LLM cost optimization implementation.

## Cost Tracking Configuration

```python
# cost_config.py - Copy and customize

from dataclasses import dataclass, field
from typing import Optional, Dict

@dataclass
class CostOptimizationConfig:
    """Configuration for cost-optimized LLM service."""

    # Feature flags
    enable_caching: bool = True
    enable_model_routing: bool = True
    enable_prompt_compression: bool = True
    enable_batch_mode: bool = True

    # Cache settings
    cache_ttl_hours: int = 24
    max_memory_cache_items: int = 1000
    redis_url: Optional[str] = None

    # Model settings
    default_model: str = "gpt-4.1-mini"
    fallback_model: str = "gpt-4.1"
    routing_thresholds: Dict[str, int] = field(default_factory=lambda: {
        "simple_max_length": 200,
        "complex_min_length": 2000,
        "complex_indicator_threshold": 2
    })

    # Budget controls
    daily_budget_usd: Optional[float] = None
    monthly_budget_usd: Optional[float] = None
    max_tokens_per_request: int = 4096

    # Rate limiting
    requests_per_minute: int = 60
    tokens_per_minute: int = 100_000

    # Batching
    batch_size: int = 32
    max_concurrent_requests: int = 10
    batch_delay_seconds: float = 0.1

    # Monitoring
    enable_logging: bool = True
    log_level: str = "INFO"
    metrics_export_interval: int = 60  # seconds


# Environment-specific configs
DEV_CONFIG = CostOptimizationConfig(
    daily_budget_usd=5.00,
    default_model="gpt-4.1-nano",
    enable_batch_mode=False
)

STAGING_CONFIG = CostOptimizationConfig(
    daily_budget_usd=50.00,
    default_model="gpt-4.1-mini"
)

PRODUCTION_CONFIG = CostOptimizationConfig(
    daily_budget_usd=500.00,
    monthly_budget_usd=10000.00,
    redis_url="redis://localhost:6379",
    enable_logging=True
)
```

## Model Pricing Table

```python
# pricing.py - Update monthly with latest prices

from dataclasses import dataclass
from datetime import date

@dataclass
class ModelPricing:
    input_per_1m: float
    output_per_1m: float
    context_window: int
    batch_discount: float = 0.5  # 50% off for batch

# Last updated: 2025-01
PRICING_2025_01 = {
    # OpenAI
    "gpt-4.1": ModelPricing(2.00, 8.00, 1_000_000),
    "gpt-4.1-mini": ModelPricing(0.40, 1.60, 1_000_000),
    "gpt-4.1-nano": ModelPricing(0.10, 0.40, 1_000_000),
    "gpt-4o": ModelPricing(2.50, 10.00, 128_000),
    "gpt-4o-mini": ModelPricing(0.15, 0.60, 128_000),
    "o3": ModelPricing(10.00, 40.00, 200_000),
    "o3-mini": ModelPricing(1.10, 4.40, 200_000),
    "o1": ModelPricing(15.00, 60.00, 200_000),
    "o1-mini": ModelPricing(3.00, 12.00, 128_000),

    # Anthropic
    "claude-4-opus-20250514": ModelPricing(15.00, 75.00, 200_000),
    "claude-4-sonnet-20250514": ModelPricing(3.00, 15.00, 200_000),
    "claude-3-5-sonnet-20241022": ModelPricing(3.00, 15.00, 200_000),
    "claude-3-5-haiku-20241022": ModelPricing(0.80, 4.00, 200_000),

    # Google
    "gemini-2.0-pro": ModelPricing(1.25, 5.00, 2_000_000),
    "gemini-2.0-flash": ModelPricing(0.10, 0.40, 1_000_000),
    "gemini-1.5-pro": ModelPricing(1.25, 5.00, 2_000_000),
    "gemini-1.5-flash": ModelPricing(0.075, 0.30, 1_000_000),

    # Mistral
    "mistral-large": ModelPricing(2.00, 6.00, 128_000),
    "mistral-medium": ModelPricing(0.65, 1.95, 32_000),
    "mistral-small": ModelPricing(0.10, 0.30, 32_000),
}

PRICING = PRICING_2025_01


def calculate_cost(
    model: str,
    input_tokens: int,
    output_tokens: int,
    is_batch: bool = False
) -> float:
    """Calculate cost for a request."""
    pricing = PRICING.get(model)
    if not pricing:
        return 0.0

    multiplier = pricing.batch_discount if is_batch else 1.0

    cost = (
        (input_tokens / 1_000_000) * pricing.input_per_1m +
        (output_tokens / 1_000_000) * pricing.output_per_1m
    ) * multiplier

    return round(cost, 6)
```

## Model Router Configuration

```python
# router_config.py

from enum import Enum
from typing import List, Callable, Optional

class TaskType(Enum):
    CLASSIFICATION = "classification"
    EXTRACTION = "extraction"
    SUMMARIZATION = "summarization"
    TRANSLATION = "translation"
    QA_SIMPLE = "qa_simple"
    QA_COMPLEX = "qa_complex"
    CODE_GENERATION = "code_generation"
    CODE_REVIEW = "code_review"
    ANALYSIS = "analysis"
    CREATIVE = "creative"
    REASONING = "reasoning"

# Model routing rules
ROUTING_RULES = {
    TaskType.CLASSIFICATION: "gpt-4.1-nano",
    TaskType.EXTRACTION: "gpt-4.1-nano",
    TaskType.SUMMARIZATION: "gpt-4.1-mini",
    TaskType.TRANSLATION: "gpt-4.1-mini",
    TaskType.QA_SIMPLE: "gpt-4.1-nano",
    TaskType.QA_COMPLEX: "gpt-4.1-mini",
    TaskType.CODE_GENERATION: "gpt-4.1",
    TaskType.CODE_REVIEW: "gpt-4.1-mini",
    TaskType.ANALYSIS: "gpt-4.1",
    TaskType.CREATIVE: "gpt-4.1",
    TaskType.REASONING: "o3-mini",
}

# Task detection patterns
TASK_PATTERNS = {
    TaskType.CLASSIFICATION: [
        r"classify|categorize|label|tag",
        r"is this .+\?$",
        r"which category",
    ],
    TaskType.EXTRACTION: [
        r"extract|find|get .+ from",
        r"parse|identify .+ in",
    ],
    TaskType.CODE_GENERATION: [
        r"write (?:a |the )?(?:code|function|script|class)",
        r"implement|create .+ function",
        r"```\w+",  # Code block present
    ],
    TaskType.REASONING: [
        r"step by step|chain of thought",
        r"prove|derive|calculate",
        r"why .+ and .+ but",
    ],
}
```

## Budget Alert Template

```python
# alerts.py

from dataclasses import dataclass
from typing import Callable, Optional
from datetime import datetime

@dataclass
class BudgetAlert:
    threshold_percent: float
    message: str
    triggered: bool = False
    triggered_at: Optional[datetime] = None

class BudgetAlertSystem:
    """Budget monitoring with alerts."""

    def __init__(
        self,
        daily_budget: float,
        on_alert: Callable[[BudgetAlert, float], None]
    ):
        self.daily_budget = daily_budget
        self.on_alert = on_alert
        self.current_spend = 0.0

        self.alerts = [
            BudgetAlert(0.5, "50% of daily budget used"),
            BudgetAlert(0.8, "80% of daily budget used - consider throttling"),
            BudgetAlert(0.95, "95% of daily budget used - critical"),
            BudgetAlert(1.0, "Daily budget exceeded - blocking new requests"),
        ]

    def record_spend(self, amount: float):
        """Record spend and check alerts."""
        self.current_spend += amount
        percent_used = self.current_spend / self.daily_budget

        for alert in self.alerts:
            if not alert.triggered and percent_used >= alert.threshold_percent:
                alert.triggered = True
                alert.triggered_at = datetime.now()
                self.on_alert(alert, self.current_spend)

    def reset_daily(self):
        """Reset for new day."""
        self.current_spend = 0.0
        for alert in self.alerts:
            alert.triggered = False
            alert.triggered_at = None


# Usage
def send_slack_alert(alert: BudgetAlert, spend: float):
    # Implement Slack/email notification
    print(f"ALERT: {alert.message} (${spend:.2f})")

alerts = BudgetAlertSystem(
    daily_budget=100.00,
    on_alert=send_slack_alert
)
```

## Metrics Export Template

```python
# metrics.py

from dataclasses import dataclass, field
from typing import Dict, List
from datetime import datetime, timedelta
import json

@dataclass
class CostMetrics:
    """Exportable cost metrics."""
    timestamp: datetime = field(default_factory=datetime.now)

    # Totals
    total_cost: float = 0.0
    total_requests: int = 0
    total_input_tokens: int = 0
    total_output_tokens: int = 0

    # By model
    by_model: Dict[str, dict] = field(default_factory=dict)

    # By endpoint/feature
    by_feature: Dict[str, dict] = field(default_factory=dict)

    # Cache stats
    cache_hits: int = 0
    cache_misses: int = 0

    # Routing stats
    routing_distribution: Dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp.isoformat(),
            "totals": {
                "cost_usd": round(self.total_cost, 4),
                "requests": self.total_requests,
                "input_tokens": self.total_input_tokens,
                "output_tokens": self.total_output_tokens,
            },
            "by_model": self.by_model,
            "by_feature": self.by_feature,
            "cache": {
                "hits": self.cache_hits,
                "misses": self.cache_misses,
                "hit_rate": round(
                    self.cache_hits / max(1, self.cache_hits + self.cache_misses) * 100,
                    1
                )
            },
            "routing": self.routing_distribution
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


class MetricsCollector:
    """Collect and export metrics."""

    def __init__(self):
        self.current = CostMetrics()
        self.history: List[CostMetrics] = []

    def record(
        self,
        model: str,
        cost: float,
        input_tokens: int,
        output_tokens: int,
        feature: str = "unknown",
        cached: bool = False
    ):
        """Record a request."""
        self.current.total_cost += cost
        self.current.total_requests += 1
        self.current.total_input_tokens += input_tokens
        self.current.total_output_tokens += output_tokens

        # By model
        if model not in self.current.by_model:
            self.current.by_model[model] = {"cost": 0, "requests": 0}
        self.current.by_model[model]["cost"] += cost
        self.current.by_model[model]["requests"] += 1

        # By feature
        if feature not in self.current.by_feature:
            self.current.by_feature[feature] = {"cost": 0, "requests": 0}
        self.current.by_feature[feature]["cost"] += cost
        self.current.by_feature[feature]["requests"] += 1

        # Cache
        if cached:
            self.current.cache_hits += 1
        else:
            self.current.cache_misses += 1

        # Routing
        tier = "premium" if "4.1" in model and "mini" not in model and "nano" not in model else "standard" if "mini" in model else "economy"
        self.current.routing_distribution[tier] = self.current.routing_distribution.get(tier, 0) + 1

    def export(self) -> dict:
        """Export current metrics."""
        return self.current.to_dict()

    def rotate(self):
        """Archive current and start new period."""
        self.history.append(self.current)
        self.current = CostMetrics()

        # Keep last 30 periods
        if len(self.history) > 30:
            self.history = self.history[-30:]
```

## FastAPI Integration Template

```python
# fastapi_integration.py

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from contextlib import asynccontextmanager

# Assuming the classes from examples.md are available
# from .llm_service import CostOptimizedLLM, CostConfig

app = FastAPI()
llm_service: Optional[CostOptimizedLLM] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global llm_service
    from openai import OpenAI

    llm_service = CostOptimizedLLM(
        client=OpenAI(),
        config=CostConfig(
            enable_caching=True,
            enable_routing=True,
            daily_budget=100.00
        )
    )
    yield
    # Cleanup
    print(f"Final report: {llm_service.get_report()}")

app = FastAPI(lifespan=lifespan)

class CompletionRequest(BaseModel):
    prompt: str
    system: Optional[str] = None
    model: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 1000

class CompletionResponse(BaseModel):
    content: str
    model: str
    cached: bool
    cost: float
    tokens: Optional[dict] = None

@app.post("/v1/complete", response_model=CompletionResponse)
async def complete(request: CompletionRequest):
    """Cost-optimized completion endpoint."""
    if llm_service is None:
        raise HTTPException(500, "Service not initialized")

    try:
        result = llm_service.complete(
            prompt=request.prompt,
            system=request.system or "",
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        return CompletionResponse(**result)
    except RuntimeError as e:
        if "budget" in str(e).lower():
            raise HTTPException(429, str(e))
        raise HTTPException(500, str(e))

@app.get("/v1/metrics")
async def get_metrics():
    """Get cost metrics."""
    if llm_service is None:
        raise HTTPException(500, "Service not initialized")
    return llm_service.get_report()

@app.get("/health")
async def health():
    """Health check with budget status."""
    if llm_service is None:
        return {"status": "unhealthy", "reason": "not initialized"}

    report = llm_service.get_report()
    over_budget = llm_service.tracker.is_over_budget()

    return {
        "status": "degraded" if over_budget else "healthy",
        "budget_remaining": not over_budget,
        "total_cost_today": report["cost"]["total_cost"],
        "cache_hit_rate": report["cache_hit_rate"]
    }
```

## Environment Variables Template

```bash
# .env.template - Copy to .env and fill in

# LLM Providers
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...

# Cost Optimization
LLM_DAILY_BUDGET_USD=100.00
LLM_MONTHLY_BUDGET_USD=2000.00
LLM_DEFAULT_MODEL=gpt-4.1-mini
LLM_FALLBACK_MODEL=gpt-4.1

# Caching
REDIS_URL=redis://localhost:6379
LLM_CACHE_TTL_HOURS=24
LLM_CACHE_MAX_MEMORY_ITEMS=1000

# Rate Limiting
LLM_REQUESTS_PER_MINUTE=60
LLM_TOKENS_PER_MINUTE=100000

# Batching
LLM_BATCH_SIZE=32
LLM_MAX_CONCURRENT=10

# Monitoring
LLM_METRICS_ENABLED=true
LLM_LOG_LEVEL=INFO

# Alerts
SLACK_WEBHOOK_URL=https://hooks.slack.com/...
ALERT_EMAIL=team@example.com
```
