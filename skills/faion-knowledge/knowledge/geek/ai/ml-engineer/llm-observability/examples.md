---
id: llm-observability-examples
name: "LLM Observability Code Examples"
domain: ML
skill: faion-ml-engineer
category: "best-practices-2026"
---

# LLM Observability Code Examples

## Langfuse

### Basic Setup (Python)

```python
# pip install langfuse openai

from langfuse import Langfuse
from langfuse.openai import openai  # OpenAI wrapper with auto-tracing

# Initialize Langfuse
langfuse = Langfuse(
    public_key="pk-...",
    secret_key="sk-...",
    host="https://cloud.langfuse.com"  # or self-hosted URL
)

# All OpenAI calls are automatically traced
response = openai.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello, world!"}]
)
```

### Manual Tracing with Decorator

```python
from langfuse.decorators import observe, langfuse_context

@observe()
def process_query(query: str) -> str:
    """Process user query with full tracing."""
    # Add metadata to current trace
    langfuse_context.update_current_trace(
        user_id="user_123",
        session_id="session_456",
        tags=["production", "v2.1"]
    )

    # This span is automatically created
    context = retrieve_context(query)

    # Generate response
    response = generate_response(query, context)

    return response

@observe()
def retrieve_context(query: str) -> list[str]:
    """Retrieve relevant context - traced as span."""
    # Your retrieval logic
    return ["context_1", "context_2"]

@observe(as_type="generation")
def generate_response(query: str, context: list[str]) -> str:
    """Generate LLM response - traced as generation."""
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"Context: {context}"},
            {"role": "user", "content": query}
        ]
    )
    return response.choices[0].message.content
```

### Cost and Token Tracking

```python
from langfuse.decorators import observe, langfuse_context

@observe(as_type="generation")
def tracked_generation(prompt: str) -> str:
    """Generation with explicit cost tracking."""
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )

    # Langfuse auto-captures usage, but you can add custom metrics
    langfuse_context.update_current_observation(
        usage={
            "input": response.usage.prompt_tokens,
            "output": response.usage.completion_tokens,
            "total": response.usage.total_tokens,
            "unit": "TOKENS"
        },
        model="gpt-4o",
        metadata={
            "temperature": 0.7,
            "max_tokens": 1000
        }
    )

    return response.choices[0].message.content
```

### PII Masking

```python
import re
from langfuse import Langfuse

def mask_pii(data):
    """Mask sensitive data before sending to Langfuse."""
    if isinstance(data, str):
        # Mask email
        data = re.sub(r'[\w\.-]+@[\w\.-]+', '[EMAIL]', data)
        # Mask phone
        data = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE]', data)
        # Mask SSN
        data = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[SSN]', data)
    return data

langfuse = Langfuse(
    public_key="pk-...",
    secret_key="sk-...",
    mask=mask_pii  # Applied to all trace data
)
```

### Sampling for High Volume

```python
import random
from langfuse import Langfuse

langfuse = Langfuse(
    public_key="pk-...",
    secret_key="sk-...",
    sample_rate=0.2  # Trace ~20% of requests
)

# Or conditional sampling
def should_sample(request) -> bool:
    """Custom sampling logic."""
    if request.is_error:
        return True  # Always trace errors
    if request.user.is_premium:
        return True  # Always trace premium users
    return random.random() < 0.1  # 10% for others
```

### OpenTelemetry Integration

```python
# pip install langfuse[opentelemetry]

from langfuse import Langfuse
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from langfuse.opentelemetry import LangfuseSpanProcessor

# Set up OTEL with Langfuse exporter
provider = TracerProvider()
provider.add_span_processor(
    LangfuseSpanProcessor(
        public_key="pk-...",
        secret_key="sk-..."
    )
)
trace.set_tracer_provider(provider)

# Now all OTEL spans are also sent to Langfuse
tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("my-operation") as span:
    span.set_attribute("user.id", "123")
    # Your code here
```

---

## LangSmith

### Basic Setup

```python
# pip install langsmith langchain

import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "ls-..."
os.environ["LANGCHAIN_PROJECT"] = "my-project"

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# All LangChain calls are automatically traced
llm = ChatOpenAI(model="gpt-4o")
response = llm.invoke([HumanMessage(content="Hello!")])
```

### Manual Tracing with traceable

```python
from langsmith import traceable
from langsmith.run_helpers import get_current_run_tree

@traceable(name="process_query", run_type="chain")
def process_query(query: str) -> str:
    """Process with LangSmith tracing."""
    # Get current run for metadata
    run = get_current_run_tree()
    run.add_metadata({"user_id": "123", "version": "2.1"})

    context = retrieve_context(query)
    response = generate_response(query, context)

    return response

@traceable(name="retrieve", run_type="retriever")
def retrieve_context(query: str) -> list[str]:
    """Retrieval step."""
    return ["context_1", "context_2"]

@traceable(name="generate", run_type="llm")
def generate_response(query: str, context: list[str]) -> str:
    """LLM generation step."""
    llm = ChatOpenAI(model="gpt-4o")
    return llm.invoke(f"Context: {context}\nQuery: {query}").content
```

### Evaluation with Datasets

```python
from langsmith import Client
from langsmith.evaluation import evaluate

client = Client()

# Create dataset from examples
dataset = client.create_dataset("qa-examples")
client.create_examples(
    dataset_id=dataset.id,
    inputs=[
        {"question": "What is the capital of France?"},
        {"question": "Who wrote Romeo and Juliet?"}
    ],
    outputs=[
        {"answer": "Paris"},
        {"answer": "William Shakespeare"}
    ]
)

# Define evaluators
def correctness(run, example):
    """Check if response matches expected."""
    predicted = run.outputs.get("answer", "")
    expected = example.outputs.get("answer", "")
    return {"score": 1.0 if predicted.lower() == expected.lower() else 0.0}

# Run evaluation
results = evaluate(
    lambda inputs: {"answer": my_qa_function(inputs["question"])},
    data=dataset.name,
    evaluators=[correctness],
    experiment_prefix="qa-v1"
)
```

### LangGraph Agent Tracing

```python
from langgraph.graph import StateGraph, END
from langsmith import traceable

@traceable(name="agent_step", run_type="chain")
def agent_node(state):
    """Agent decision node - fully traced."""
    messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages": messages + [response]}

@traceable(name="tool_execution", run_type="tool")
def tool_node(state):
    """Tool execution - traced separately."""
    # Tool logic here
    pass

# Build graph - all nodes are traced
graph = StateGraph(State)
graph.add_node("agent", agent_node)
graph.add_node("tools", tool_node)
# ... edges
app = graph.compile()
```

---

## Helicone

### Proxy Integration (Simplest)

```python
# Single line change - no SDK needed!

from openai import OpenAI

# Original
# client = OpenAI()

# With Helicone (change base_url only)
client = OpenAI(
    base_url="https://oai.helicone.ai/v1",
    default_headers={
        "Helicone-Auth": "Bearer sk-helicone-...",
    }
)

# All calls are now traced automatically
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### Adding Metadata

```python
client = OpenAI(
    base_url="https://oai.helicone.ai/v1",
    default_headers={
        "Helicone-Auth": "Bearer sk-helicone-...",
        "Helicone-User-Id": "user_123",
        "Helicone-Session-Id": "session_456",
        "Helicone-Property-Feature": "chat",
        "Helicone-Property-Environment": "production"
    }
)
```

### Caching (Cost Reduction)

```python
# Enable caching to reduce costs by 20-30%
client = OpenAI(
    base_url="https://oai.helicone.ai/v1",
    default_headers={
        "Helicone-Auth": "Bearer sk-helicone-...",
        "Helicone-Cache-Enabled": "true",
        "Helicone-Cache-Bucket-Max-Size": "1000",  # Cache up to 1000 requests
    }
)

# Identical requests return cached response (no API cost)
```

### Rate Limiting

```python
client = OpenAI(
    base_url="https://oai.helicone.ai/v1",
    default_headers={
        "Helicone-Auth": "Bearer sk-helicone-...",
        "Helicone-RateLimit-Policy": "100;w=60",  # 100 requests per 60 seconds
    }
)
```

---

## Portkey

### AI Gateway Setup

```python
# pip install portkey-ai

from portkey_ai import Portkey

portkey = Portkey(
    api_key="pk-...",
    virtual_key="openai-virtual-key"  # Configured in Portkey dashboard
)

# Automatic tracing, fallbacks, and cost tracking
response = portkey.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### Multi-Provider Fallback

```python
from portkey_ai import Portkey

portkey = Portkey(
    api_key="pk-...",
    config={
        "strategy": {
            "mode": "fallback"
        },
        "targets": [
            {"virtual_key": "openai-key", "override_params": {"model": "gpt-4o"}},
            {"virtual_key": "anthropic-key", "override_params": {"model": "claude-sonnet-4-20250514"}},
            {"virtual_key": "azure-key", "override_params": {"model": "gpt-4"}}
        ]
    }
)

# Automatically falls back if primary fails
response = portkey.chat.completions.create(
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### Cost Tracking by User/Team

```python
from portkey_ai import Portkey

portkey = Portkey(
    api_key="pk-...",
    virtual_key="openai-key"
)

# Add metadata for cost allocation
response = portkey.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}],
    metadata={
        "user_id": "user_123",
        "team_id": "engineering",
        "project": "chatbot-v2",
        "environment": "production"
    }
)

# Query costs via API
# GET /analytics?group_by=user_id&metric=cost
```

---

## Framework Integrations

### LangChain + Langfuse

```python
from langfuse.callback import CallbackHandler
from langchain_openai import ChatOpenAI

langfuse_handler = CallbackHandler(
    public_key="pk-...",
    secret_key="sk-..."
)

llm = ChatOpenAI(model="gpt-4o")
response = llm.invoke(
    "Hello!",
    config={"callbacks": [langfuse_handler]}
)
```

### LlamaIndex + Langfuse

```python
from langfuse.llama_index import LlamaIndexInstrumentor

# Auto-instrument all LlamaIndex operations
LlamaIndexInstrumentor().start()

# Now all LlamaIndex queries are traced
from llama_index.core import VectorStoreIndex
index = VectorStoreIndex.from_documents(documents)
response = index.as_query_engine().query("What is...?")
```

### FastAPI Middleware

```python
from fastapi import FastAPI, Request
from langfuse import Langfuse
from langfuse.decorators import langfuse_context
import uuid

app = FastAPI()
langfuse = Langfuse()

@app.middleware("http")
async def trace_middleware(request: Request, call_next):
    """Add tracing context to all requests."""
    trace_id = str(uuid.uuid4())
    request.state.trace_id = trace_id

    # Start trace
    trace = langfuse.trace(
        id=trace_id,
        name=f"{request.method} {request.url.path}",
        user_id=request.headers.get("X-User-ID"),
        session_id=request.headers.get("X-Session-ID"),
        metadata={"path": request.url.path}
    )

    response = await call_next(request)

    # Add response info
    trace.update(
        metadata={"status_code": response.status_code}
    )

    return response
```
