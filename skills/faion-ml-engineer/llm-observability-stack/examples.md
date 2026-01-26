---
id: llm-observability-stack-examples
name: "LLM Observability Stack Integration Examples"
domain: ML
skill: faion-ml-engineer
category: "best-practices-2026"
---

# LLM Observability Stack Integration Examples

## OpenLLMetry (OpenTelemetry-Native)

### Basic Setup

```python
# pip install traceloop-sdk openai

from traceloop.sdk import Traceloop

# Initialize - auto-instruments OpenAI, Anthropic, etc.
Traceloop.init(
    app_name="my-llm-app",
    disable_batch=False  # Enable batching for production
)

# All LLM calls are now automatically traced
from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### Export to Multiple Backends

```python
from traceloop.sdk import Traceloop
from traceloop.sdk.decorators import workflow, task, agent, tool

# Export to Langfuse + Datadog simultaneously
Traceloop.init(
    app_name="my-llm-app",
    api_endpoint="https://api.traceloop.com",
    # Or use OTEL exporters:
    # exporter=OTLPSpanExporter(endpoint="...")
)

@workflow(name="rag_pipeline")
def process_query(query: str) -> str:
    context = retrieve_context(query)
    response = generate_response(query, context)
    return response

@task(name="retrieval")
def retrieve_context(query: str) -> list[str]:
    # Traced as separate span
    return ["context_1", "context_2"]

@agent(name="qa_agent")
def generate_response(query: str, context: list[str]) -> str:
    # Traced as agent span
    return call_llm(query, context)

@tool(name="llm_call")
def call_llm(query: str, context: list[str]) -> str:
    # Traced as tool invocation
    from openai import OpenAI
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"Context: {context}"},
            {"role": "user", "content": query}
        ]
    )
    return response.choices[0].message.content
```

### Framework Integrations

```python
# LangChain
from traceloop.sdk.instruments import Instruments
Traceloop.init(instruments=[Instruments.LANGCHAIN])

# LlamaIndex
Traceloop.init(instruments=[Instruments.LLAMA_INDEX])

# CrewAI
Traceloop.init(instruments=[Instruments.CREWAI])

# Multiple frameworks
Traceloop.init(instruments=[
    Instruments.OPENAI,
    Instruments.ANTHROPIC,
    Instruments.LANGCHAIN,
    Instruments.CHROMA,
    Instruments.PINECONE
])
```

---

## Unified Stack: Langfuse + Helicone + OTEL

### Architecture

```python
"""
Complete observability stack:
- Langfuse: Tracing, prompts, evaluations
- Helicone: Cost analytics, caching
- OpenTelemetry: Unified collection, APM integration
"""

import os
from openai import OpenAI
from langfuse import Langfuse
from langfuse.decorators import observe, langfuse_context

# Initialize Langfuse
langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host="https://cloud.langfuse.com"
)

# OpenAI client via Helicone proxy (for caching + cost tracking)
client = OpenAI(
    base_url="https://oai.helicone.ai/v1",
    default_headers={
        "Helicone-Auth": f"Bearer {os.getenv('HELICONE_API_KEY')}",
        "Helicone-Cache-Enabled": "true",
    }
)

@observe()
def process_query(query: str, user_id: str) -> str:
    """Process with unified observability."""
    # Add metadata to Langfuse trace
    langfuse_context.update_current_trace(
        user_id=user_id,
        tags=["production", "v2.1"]
    )

    # Call via Helicone (cached + cost tracked)
    # Traced by Langfuse decorator
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": query}],
        extra_headers={
            "Helicone-User-Id": user_id,
            "Helicone-Property-Feature": "chat"
        }
    )

    return response.choices[0].message.content
```

### OTEL Export to Multiple Backends

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from langfuse.opentelemetry import LangfuseSpanProcessor

# Create provider with multiple exporters
provider = TracerProvider()

# Export to Langfuse
provider.add_span_processor(
    LangfuseSpanProcessor(
        public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
        secret_key=os.getenv("LANGFUSE_SECRET_KEY")
    )
)

# Export to Grafana Tempo
provider.add_span_processor(
    BatchSpanProcessor(
        OTLPSpanExporter(endpoint="http://tempo:4317")
    )
)

# Export to Datadog
provider.add_span_processor(
    BatchSpanProcessor(
        OTLPSpanExporter(endpoint="http://datadog-agent:4317")
    )
)

trace.set_tracer_provider(provider)
```

---

## Portkey AI Gateway

### Multi-Provider Routing with Observability

```python
from portkey_ai import Portkey

portkey = Portkey(
    api_key=os.getenv("PORTKEY_API_KEY"),
    config={
        "strategy": {
            "mode": "fallback"
        },
        "targets": [
            {
                "virtual_key": "openai-prod",
                "override_params": {"model": "gpt-4o"},
                "weight": 1
            },
            {
                "virtual_key": "anthropic-backup",
                "override_params": {"model": "claude-sonnet-4-20250514"},
                "weight": 1
            },
            {
                "virtual_key": "azure-fallback",
                "override_params": {"model": "gpt-4"},
                "weight": 1
            }
        ],
        "retry": {
            "attempts": 3,
            "on_status_codes": [429, 500, 502, 503, 504]
        },
        "cache": {
            "mode": "semantic",
            "max_age": 3600
        }
    }
)

# Call with automatic:
# - Fallback routing
# - Retry handling
# - Caching
# - Full observability
response = portkey.chat.completions.create(
    messages=[{"role": "user", "content": "Hello!"}],
    metadata={
        "user_id": "user_123",
        "team_id": "engineering",
        "feature": "chat"
    }
)

# Access observability data
# GET /analytics?group_by=user_id&metric=cost
# GET /analytics?group_by=model&metric=latency
```

### Load Balancing

```python
portkey = Portkey(
    api_key=os.getenv("PORTKEY_API_KEY"),
    config={
        "strategy": {
            "mode": "loadbalance"
        },
        "targets": [
            {"virtual_key": "openai-1", "weight": 0.5},
            {"virtual_key": "openai-2", "weight": 0.3},
            {"virtual_key": "azure-1", "weight": 0.2}
        ]
    }
)
```

---

## Agent Tracing (LangGraph + LangSmith)

```python
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = "agent-observability"

from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langsmith import traceable
from typing import TypedDict, Annotated
import operator

class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    iteration: int

llm = ChatOpenAI(model="gpt-4o")

@traceable(name="agent_decision", run_type="chain")
def agent_node(state: AgentState) -> dict:
    """Agent decision - fully traced with nested spans."""
    messages = state["messages"]
    iteration = state.get("iteration", 0)

    response = llm.invoke(messages)

    return {
        "messages": [response],
        "iteration": iteration + 1
    }

@traceable(name="tool_execution", run_type="tool")
def tool_node(state: AgentState) -> dict:
    """Tool execution - traced as tool span."""
    # Parse tool calls from last message
    last_message = state["messages"][-1]
    # Execute tools...
    return {"messages": [tool_results]}

def should_continue(state: AgentState) -> str:
    """Routing logic - traced as part of workflow."""
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return "end"

# Build graph
graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.add_node("tools", tool_node)
graph.add_conditional_edges("agent", should_continue, {
    "tools": "tools",
    "end": END
})
graph.add_edge("tools", "agent")
graph.set_entry_point("agent")

app = graph.compile()

# Execute with full observability
result = app.invoke({
    "messages": [{"role": "user", "content": "Search for latest AI news"}],
    "iteration": 0
})
```

---

## FastAPI Middleware Integration

```python
from fastapi import FastAPI, Request
from langfuse import Langfuse
from langfuse.decorators import langfuse_context
from contextlib import asynccontextmanager
import uuid

langfuse = Langfuse()

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    langfuse.flush()

app = FastAPI(lifespan=lifespan)

@app.middleware("http")
async def observability_middleware(request: Request, call_next):
    """Add unified observability to all requests."""
    trace_id = str(uuid.uuid4())
    user_id = request.headers.get("X-User-ID")
    session_id = request.headers.get("X-Session-ID")

    # Start Langfuse trace
    trace = langfuse.trace(
        id=trace_id,
        name=f"{request.method} {request.url.path}",
        user_id=user_id,
        session_id=session_id,
        metadata={
            "path": request.url.path,
            "method": request.method
        }
    )

    # Store in request state
    request.state.trace_id = trace_id
    request.state.trace = trace

    response = await call_next(request)

    # Update trace with response info
    trace.update(
        metadata={"status_code": response.status_code}
    )

    return response

@app.post("/chat")
async def chat(request: Request, query: str):
    """Chat endpoint with full observability."""
    trace = request.state.trace

    # Create span for this operation
    span = trace.span(name="chat_handler")

    # Your LLM logic here
    response = await process_chat(query)

    span.end()
    return {"response": response}
```

---

## Prometheus Metrics Collector

```python
from prometheus_client import Counter, Histogram, Gauge
import time

# Define metrics
LLM_REQUESTS = Counter(
    'llm_requests_total',
    'Total LLM requests',
    ['model', 'endpoint', 'status']
)

LLM_TOKENS = Counter(
    'llm_tokens_total',
    'Total tokens used',
    ['model', 'direction']  # input/output
)

LLM_COST = Counter(
    'llm_cost_usd',
    'Total cost in USD',
    ['model', 'user_id', 'team_id']
)

LLM_LATENCY = Histogram(
    'llm_request_duration_seconds',
    'Request latency',
    ['model', 'endpoint'],
    buckets=[0.1, 0.5, 1, 2, 5, 10, 30]
)

LLM_TTFT = Histogram(
    'llm_ttft_seconds',
    'Time to first token',
    ['model'],
    buckets=[0.1, 0.25, 0.5, 1, 2, 5]
)

LLM_QUALITY = Histogram(
    'llm_quality_score',
    'Quality evaluation score',
    ['model', 'evaluator'],
    buckets=[1, 2, 3, 4, 5]
)

# Pricing (Q1 2026)
MODEL_PRICING = {
    "gpt-4o": {"input": 0.0025, "output": 0.01},
    "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
    "claude-sonnet-4-20250514": {"input": 0.003, "output": 0.015},
}

def track_llm_call(model: str, endpoint: str, input_tokens: int,
                   output_tokens: int, latency: float, ttft: float,
                   user_id: str, team_id: str, status: str = "success"):
    """Record metrics for an LLM call."""
    # Request count
    LLM_REQUESTS.labels(model=model, endpoint=endpoint, status=status).inc()

    # Tokens
    LLM_TOKENS.labels(model=model, direction="input").inc(input_tokens)
    LLM_TOKENS.labels(model=model, direction="output").inc(output_tokens)

    # Cost
    pricing = MODEL_PRICING.get(model, {"input": 0.01, "output": 0.03})
    cost = (input_tokens * pricing["input"] + output_tokens * pricing["output"]) / 1000
    LLM_COST.labels(model=model, user_id=user_id, team_id=team_id).inc(cost)

    # Latency
    LLM_LATENCY.labels(model=model, endpoint=endpoint).observe(latency)

    # TTFT
    LLM_TTFT.labels(model=model).observe(ttft)

def track_quality_score(model: str, evaluator: str, score: float):
    """Record quality evaluation score."""
    LLM_QUALITY.labels(model=model, evaluator=evaluator).observe(score)
```

---

## Async Evaluation Pipeline

```python
import asyncio
from langfuse import Langfuse
from openai import AsyncOpenAI

langfuse = Langfuse()
client = AsyncOpenAI()

EVALUATION_PROMPT = """
You are evaluating an AI response quality.

Query: {query}
Response: {response}

Rate on scale 1-5:
1. Relevance (1-5)
2. Accuracy (1-5)
3. Helpfulness (1-5)

Output JSON: {{"relevance": N, "accuracy": N, "helpfulness": N, "overall": N}}
"""

async def evaluate_trace(trace_id: str, query: str, response: str):
    """Async evaluation using LLM-as-judge."""
    prompt = EVALUATION_PROMPT.format(query=query, response=response)

    result = await client.chat.completions.create(
        model="gpt-4o-mini",  # Cheaper model for evaluation
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    scores = json.loads(result.choices[0].message.content)

    # Record scores in Langfuse
    for metric, score in scores.items():
        langfuse.score(
            trace_id=trace_id,
            name=f"quality_{metric}",
            value=score
        )

    return scores

async def batch_evaluate(traces: list[dict]):
    """Evaluate multiple traces concurrently."""
    tasks = [
        evaluate_trace(t["trace_id"], t["query"], t["response"])
        for t in traces
    ]
    return await asyncio.gather(*tasks)
```

---

## Grafana Dashboard Query Examples

### PromQL for LLM Metrics

```promql
# Total cost (last 24h)
sum(increase(llm_cost_usd[24h]))

# Cost by model (last 24h)
sum by (model)(increase(llm_cost_usd[24h]))

# Request rate (per second)
sum(rate(llm_requests_total[5m]))

# Error rate (percentage)
sum(rate(llm_requests_total{status="error"}[5m]))
/ sum(rate(llm_requests_total[5m])) * 100

# P99 latency
histogram_quantile(0.99, sum(rate(llm_request_duration_seconds_bucket[5m])) by (le))

# P95 TTFT
histogram_quantile(0.95, sum(rate(llm_ttft_seconds_bucket[5m])) by (le))

# Average quality score
avg(llm_quality_score)

# Token usage rate (tokens per minute)
sum(rate(llm_tokens_total[5m])) * 60

# Cache hit rate (if using Helicone)
sum(rate(llm_cache_hits_total[5m]))
/ (sum(rate(llm_cache_hits_total[5m])) + sum(rate(llm_cache_misses_total[5m])))
```
