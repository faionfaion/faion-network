# OpenAI API Templates

Reusable code templates for common OpenAI API patterns.

## Table of Contents

1. [Client Configuration](#client-configuration)
2. [Chat Completion Patterns](#chat-completion-patterns)
3. [Streaming Patterns](#streaming-patterns)
4. [Structured Output Schemas](#structured-output-schemas)
5. [Tool Definitions](#tool-definitions)
6. [Error Handling](#error-handling)
7. [Cost Tracking](#cost-tracking)
8. [Prompt Templates](#prompt-templates)
9. [Testing Utilities](#testing-utilities)

---

## Client Configuration

### Production Client

```python
import os
from openai import OpenAI
from typing import Optional

def create_client(
    api_key: Optional[str] = None,
    organization: Optional[str] = None,
    timeout: float = 30.0,
    max_retries: int = 3
) -> OpenAI:
    """Create production-ready OpenAI client."""
    return OpenAI(
        api_key=api_key or os.environ.get("OPENAI_API_KEY"),
        organization=organization or os.environ.get("OPENAI_ORG_ID"),
        timeout=timeout,
        max_retries=max_retries
    )

# Usage
client = create_client()
```

### Async Client

```python
from openai import AsyncOpenAI

def create_async_client(**kwargs) -> AsyncOpenAI:
    """Create async OpenAI client."""
    return AsyncOpenAI(**kwargs)
```

### Client with Custom Base URL (Azure, Proxies)

```python
def create_azure_client(
    azure_endpoint: str,
    api_version: str = "2024-02-01"
) -> OpenAI:
    """Create client for Azure OpenAI."""
    return OpenAI(
        api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
        base_url=f"{azure_endpoint}/openai/deployments",
        default_headers={"api-version": api_version}
    )
```

---

## Chat Completion Patterns

### Basic Completion

```python
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class CompletionConfig:
    """Configuration for chat completions."""
    model: str = "gpt-4o-2024-08-06"
    temperature: float = 0.7
    max_tokens: int = 1000
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    stop: Optional[List[str]] = None

def complete(
    messages: List[Dict[str, str]],
    config: CompletionConfig = None,
    client: OpenAI = None
) -> str:
    """Execute chat completion with config."""
    config = config or CompletionConfig()
    client = client or OpenAI()

    response = client.chat.completions.create(
        model=config.model,
        messages=messages,
        temperature=config.temperature,
        max_tokens=config.max_tokens,
        top_p=config.top_p,
        frequency_penalty=config.frequency_penalty,
        presence_penalty=config.presence_penalty,
        stop=config.stop
    )

    return response.choices[0].message.content
```

### Conversation Manager

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable

@dataclass
class ConversationManager:
    """Manage multi-turn conversations."""
    system_prompt: str
    model: str = "gpt-4o-2024-08-06"
    max_history: int = 20
    messages: List[Dict[str, str]] = field(default_factory=list)
    client: OpenAI = field(default_factory=OpenAI)

    def __post_init__(self):
        self.messages = [{"role": "system", "content": self.system_prompt}]

    def chat(self, user_message: str, **kwargs) -> str:
        """Send message and get response."""
        self.messages.append({"role": "user", "content": user_message})

        # Trim history if needed
        if len(self.messages) > self.max_history + 1:
            self.messages = [self.messages[0]] + self.messages[-(self.max_history):]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            **kwargs
        )

        assistant_message = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": assistant_message})

        return assistant_message

    def reset(self):
        """Reset conversation history."""
        self.messages = [{"role": "system", "content": self.system_prompt}]

    def get_history(self) -> List[Dict[str, str]]:
        """Get conversation history without system prompt."""
        return self.messages[1:]
```

### Message Builder

```python
class MessageBuilder:
    """Fluent builder for chat messages."""

    def __init__(self):
        self.messages: List[Dict] = []

    def system(self, content: str) -> "MessageBuilder":
        """Add system message."""
        self.messages.append({"role": "system", "content": content})
        return self

    def user(self, content: str) -> "MessageBuilder":
        """Add user message."""
        self.messages.append({"role": "user", "content": content})
        return self

    def assistant(self, content: str) -> "MessageBuilder":
        """Add assistant message."""
        self.messages.append({"role": "assistant", "content": content})
        return self

    def user_with_image(self, text: str, image_url: str, detail: str = "auto") -> "MessageBuilder":
        """Add user message with image."""
        self.messages.append({
            "role": "user",
            "content": [
                {"type": "text", "text": text},
                {"type": "image_url", "image_url": {"url": image_url, "detail": detail}}
            ]
        })
        return self

    def build(self) -> List[Dict]:
        """Return built messages."""
        return self.messages

# Usage
messages = (
    MessageBuilder()
    .system("You are a helpful assistant.")
    .user("Hello!")
    .assistant("Hi there! How can I help?")
    .user("What is 2+2?")
    .build()
)
```

---

## Streaming Patterns

### Stream Handler

```python
from typing import Generator, Callable, Optional
from dataclasses import dataclass

@dataclass
class StreamConfig:
    """Configuration for streaming."""
    on_token: Optional[Callable[[str], None]] = None
    on_complete: Optional[Callable[[str], None]] = None
    on_error: Optional[Callable[[Exception], None]] = None

def stream_completion(
    messages: List[Dict[str, str]],
    model: str = "gpt-4o-2024-08-06",
    config: StreamConfig = None
) -> Generator[str, None, str]:
    """Stream completion with callbacks."""
    config = config or StreamConfig()
    client = OpenAI()
    full_content = []

    try:
        stream = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True
        )

        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                full_content.append(content)
                if config.on_token:
                    config.on_token(content)
                yield content

        result = "".join(full_content)
        if config.on_complete:
            config.on_complete(result)

        return result

    except Exception as e:
        if config.on_error:
            config.on_error(e)
        raise
```

### Async Stream Handler

```python
from openai import AsyncOpenAI
import asyncio

async def async_stream_completion(
    messages: List[Dict[str, str]],
    model: str = "gpt-4o-2024-08-06"
) -> str:
    """Async streaming completion."""
    client = AsyncOpenAI()
    full_content = []

    stream = await client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True
    )

    async for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            full_content.append(content)
            yield content

    return "".join(full_content)
```

### Server-Sent Events (SSE) for FastAPI

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import json

app = FastAPI()

async def sse_generator(messages: List[Dict]):
    """Generate SSE events for streaming."""
    client = AsyncOpenAI()

    stream = await client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=messages,
        stream=True
    )

    async for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            data = json.dumps({"content": content})
            yield f"data: {data}\n\n"

    yield "data: [DONE]\n\n"

@app.post("/chat/stream")
async def stream_chat(request: dict):
    return StreamingResponse(
        sse_generator(request["messages"]),
        media_type="text/event-stream"
    )
```

---

## Structured Output Schemas

### Common Response Schemas

```python
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from enum import Enum

# Classification Result
class ClassificationResult(BaseModel):
    """Generic classification output."""
    category: str = Field(description="Classified category")
    confidence: float = Field(ge=0, le=1, description="Confidence score")
    reasoning: str = Field(description="Reasoning for classification")

# Sentiment Analysis
class SentimentResult(BaseModel):
    """Sentiment analysis output."""
    sentiment: Literal["positive", "negative", "neutral"]
    score: float = Field(ge=-1, le=1, description="-1 to 1 sentiment score")
    aspects: List[str] = Field(default_factory=list, description="Mentioned aspects")

# Entity Extraction
class Entity(BaseModel):
    """Single extracted entity."""
    text: str = Field(description="Entity text")
    type: str = Field(description="Entity type (person, org, location, etc.)")
    start: Optional[int] = Field(default=None, description="Start position")
    end: Optional[int] = Field(default=None, description="End position")

class EntityExtractionResult(BaseModel):
    """Entity extraction output."""
    entities: List[Entity]
    text_length: int

# Summary
class Summary(BaseModel):
    """Text summary output."""
    summary: str = Field(description="Summarized text")
    key_points: List[str] = Field(description="Key points extracted")
    word_count: int = Field(description="Original word count")

# Q&A Response
class QAResponse(BaseModel):
    """Question answering output."""
    answer: str = Field(description="Answer to the question")
    confidence: float = Field(ge=0, le=1)
    sources: List[str] = Field(default_factory=list, description="Source references")
    needs_clarification: bool = Field(default=False)
```

### Complex Nested Schemas

```python
# Product Review Analysis
class Aspect(BaseModel):
    """Single product aspect."""
    name: str
    sentiment: Literal["positive", "negative", "neutral"]
    mentions: int = Field(ge=0)

class ReviewAnalysis(BaseModel):
    """Product review analysis output."""
    overall_sentiment: Literal["positive", "negative", "mixed"]
    rating_prediction: float = Field(ge=1, le=5)
    aspects: List[Aspect]
    pros: List[str]
    cons: List[str]
    summary: str

# Document Structure
class Section(BaseModel):
    """Document section."""
    title: str
    content: str
    subsections: List["Section"] = Field(default_factory=list)

Section.model_rebuild()  # Enable self-reference

class DocumentStructure(BaseModel):
    """Parsed document structure."""
    title: str
    authors: List[str] = Field(default_factory=list)
    abstract: Optional[str] = None
    sections: List[Section]
    references: List[str] = Field(default_factory=list)
```

### Schema with Validation

```python
from pydantic import BaseModel, Field, field_validator
import re

class EmailExtraction(BaseModel):
    """Email data extraction with validation."""
    sender: str = Field(description="Sender email address")
    recipients: List[str] = Field(description="Recipient email addresses")
    subject: str
    date: str = Field(description="Date in ISO format YYYY-MM-DD")
    priority: Literal["low", "normal", "high"] = "normal"

    @field_validator("sender", "recipients", mode="before")
    @classmethod
    def validate_email(cls, v):
        if isinstance(v, list):
            return [e for e in v if re.match(r"[^@]+@[^@]+\.[^@]+", e)]
        if not re.match(r"[^@]+@[^@]+\.[^@]+", v):
            return "invalid@example.com"
        return v

    @field_validator("date", mode="before")
    @classmethod
    def validate_date(cls, v):
        if not re.match(r"\d{4}-\d{2}-\d{2}", v):
            return "1970-01-01"
        return v
```

---

## Tool Definitions

### Tool Definition Builder

```python
from typing import Dict, List, Any, Callable
import inspect
from pydantic import BaseModel

def function_to_tool(func: Callable, description: str = None) -> Dict:
    """Convert Python function to OpenAI tool definition."""
    sig = inspect.signature(func)
    docstring = func.__doc__ or ""

    properties = {}
    required = []

    for name, param in sig.parameters.items():
        if name == "self":
            continue

        prop = {"type": "string"}  # Default type

        # Try to infer type from annotation
        if param.annotation != inspect.Parameter.empty:
            if param.annotation == int:
                prop = {"type": "integer"}
            elif param.annotation == float:
                prop = {"type": "number"}
            elif param.annotation == bool:
                prop = {"type": "boolean"}
            elif param.annotation == list:
                prop = {"type": "array", "items": {"type": "string"}}

        properties[name] = prop

        if param.default == inspect.Parameter.empty:
            required.append(name)

    return {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": description or docstring.strip(),
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required
            }
        }
    }

# Usage
def search_products(query: str, max_results: int = 10, category: str = None) -> list:
    """Search for products in the catalog."""
    pass

tool = function_to_tool(search_products)
```

### Common Tool Definitions

```python
COMMON_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for current information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "num_results": {"type": "integer", "default": 5}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get current date and time",
            "parameters": {
                "type": "object",
                "properties": {
                    "timezone": {"type": "string", "default": "UTC"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Perform mathematical calculation",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "Math expression to evaluate"}
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read contents of a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path"},
                    "encoding": {"type": "string", "default": "utf-8"}
                },
                "required": ["path"]
            }
        }
    }
]
```

### Tool Executor

```python
import json
from typing import Dict, Callable, Any

class ToolExecutor:
    """Execute tools and manage the tool use loop."""

    def __init__(self, tools: List[Dict], functions: Dict[str, Callable]):
        self.tools = tools
        self.functions = functions
        self.client = OpenAI()

    def execute(self, messages: List[Dict], model: str = "gpt-4o-2024-08-06") -> str:
        """Execute conversation with tool use."""
        while True:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                tools=self.tools,
                tool_choice="auto"
            )

            message = response.choices[0].message
            messages.append(message)

            if not message.tool_calls:
                return message.content

            for tool_call in message.tool_calls:
                result = self._execute_tool(tool_call)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })

    def _execute_tool(self, tool_call) -> Any:
        """Execute single tool call."""
        func_name = tool_call.function.name
        func_args = json.loads(tool_call.function.arguments)

        func = self.functions.get(func_name)
        if func:
            try:
                return func(**func_args)
            except Exception as e:
                return {"error": str(e)}
        return {"error": f"Unknown function: {func_name}"}
```

---

## Error Handling

### Retry Decorator

```python
import time
import functools
from openai import RateLimitError, APIError, APIConnectionError

def retry_on_error(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential: bool = True
):
    """Decorator for automatic retry with exponential backoff."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except (RateLimitError, APIConnectionError) as e:
                    last_exception = e
                    if attempt == max_retries - 1:
                        raise

                    if exponential:
                        delay = min(base_delay * (2 ** attempt), max_delay)
                    else:
                        delay = base_delay

                    time.sleep(delay)

                except APIError as e:
                    if e.status_code and e.status_code >= 500:
                        last_exception = e
                        if attempt == max_retries - 1:
                            raise
                        delay = min(base_delay * (2 ** attempt), max_delay)
                        time.sleep(delay)
                    else:
                        raise

            raise last_exception

        return wrapper
    return decorator

# Usage
@retry_on_error(max_retries=5)
def reliable_completion(messages):
    return client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=messages
    )
```

### Error Handler Class

```python
from dataclasses import dataclass
from typing import Optional, Callable
import logging

@dataclass
class ErrorHandler:
    """Centralized error handling for OpenAI API."""
    on_rate_limit: Optional[Callable[[Exception], None]] = None
    on_auth_error: Optional[Callable[[Exception], None]] = None
    on_server_error: Optional[Callable[[Exception], None]] = None
    logger: logging.Logger = None

    def __post_init__(self):
        self.logger = self.logger or logging.getLogger(__name__)

    def handle(self, func: Callable, *args, **kwargs):
        """Execute function with error handling."""
        try:
            return func(*args, **kwargs)
        except AuthenticationError as e:
            self.logger.error(f"Authentication error: {e}")
            if self.on_auth_error:
                self.on_auth_error(e)
            raise
        except RateLimitError as e:
            self.logger.warning(f"Rate limit hit: {e}")
            if self.on_rate_limit:
                self.on_rate_limit(e)
            raise
        except APIError as e:
            if e.status_code and e.status_code >= 500:
                self.logger.error(f"Server error: {e}")
                if self.on_server_error:
                    self.on_server_error(e)
            raise
```

---

## Cost Tracking

### Usage Tracker

```python
from dataclasses import dataclass, field
from typing import Dict, List
from datetime import datetime
import json

@dataclass
class UsageRecord:
    """Single API call usage record."""
    timestamp: datetime
    model: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost: float

@dataclass
class UsageTracker:
    """Track API usage and costs."""
    records: List[UsageRecord] = field(default_factory=list)

    PRICES = {
        "gpt-4o": {"input": 2.50, "output": 10.00},
        "gpt-4o-2024-08-06": {"input": 2.50, "output": 10.00},
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        "gpt-4o-mini-2024-07-18": {"input": 0.15, "output": 0.60},
        "o1": {"input": 15.00, "output": 60.00},
        "o3-mini": {"input": 1.10, "output": 4.40},
        "text-embedding-3-large": {"input": 0.13, "output": 0},
        "text-embedding-3-small": {"input": 0.02, "output": 0},
    }

    def record(self, response) -> UsageRecord:
        """Record usage from API response."""
        model = response.model
        usage = response.usage

        # Get base model name for pricing
        base_model = model.split("-202")[0] if "-202" in model else model
        prices = self.PRICES.get(base_model, {"input": 0, "output": 0})

        cost = (
            usage.prompt_tokens * prices["input"] +
            usage.completion_tokens * prices["output"]
        ) / 1_000_000

        record = UsageRecord(
            timestamp=datetime.now(),
            model=model,
            prompt_tokens=usage.prompt_tokens,
            completion_tokens=usage.completion_tokens,
            total_tokens=usage.total_tokens,
            cost=cost
        )

        self.records.append(record)
        return record

    def total_cost(self) -> float:
        """Get total cost across all records."""
        return sum(r.cost for r in self.records)

    def total_tokens(self) -> int:
        """Get total tokens across all records."""
        return sum(r.total_tokens for r in self.records)

    def summary(self) -> Dict:
        """Get usage summary."""
        return {
            "total_requests": len(self.records),
            "total_tokens": self.total_tokens(),
            "total_cost": f"${self.total_cost():.4f}",
            "by_model": self._group_by_model()
        }

    def _group_by_model(self) -> Dict:
        """Group usage by model."""
        by_model = {}
        for r in self.records:
            if r.model not in by_model:
                by_model[r.model] = {"requests": 0, "tokens": 0, "cost": 0}
            by_model[r.model]["requests"] += 1
            by_model[r.model]["tokens"] += r.total_tokens
            by_model[r.model]["cost"] += r.cost
        return by_model

    def export_json(self, path: str):
        """Export records to JSON."""
        data = [
            {
                "timestamp": r.timestamp.isoformat(),
                "model": r.model,
                "prompt_tokens": r.prompt_tokens,
                "completion_tokens": r.completion_tokens,
                "cost": r.cost
            }
            for r in self.records
        ]
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

# Usage
tracker = UsageTracker()
response = client.chat.completions.create(...)
tracker.record(response)
print(tracker.summary())
```

### Token Counter

```python
import tiktoken

class TokenCounter:
    """Count tokens for cost estimation."""

    def __init__(self, model: str = "gpt-4o"):
        self.model = model
        self.encoding = tiktoken.encoding_for_model(model)

    def count(self, text: str) -> int:
        """Count tokens in text."""
        return len(self.encoding.encode(text))

    def count_messages(self, messages: List[Dict]) -> int:
        """Count tokens in message list."""
        total = 0
        for message in messages:
            total += 4  # Message overhead
            for key, value in message.items():
                if isinstance(value, str):
                    total += self.count(value)
                elif isinstance(value, list):  # Multi-content (images)
                    for item in value:
                        if item.get("type") == "text":
                            total += self.count(item["text"])
                        elif item.get("type") == "image_url":
                            total += 85  # Low detail estimate
        total += 2  # Priming
        return total

    def estimate_cost(
        self,
        prompt_tokens: int,
        estimated_completion: int = 500,
        model: str = None
    ) -> float:
        """Estimate cost in USD."""
        model = model or self.model
        prices = UsageTracker.PRICES.get(model, {"input": 2.50, "output": 10.00})
        return (
            prompt_tokens * prices["input"] +
            estimated_completion * prices["output"]
        ) / 1_000_000
```

---

## Prompt Templates

### Template Manager

```python
from string import Template
from typing import Dict, Any
import re

class PromptTemplate:
    """Manage prompt templates with variable substitution."""

    def __init__(self, template: str, defaults: Dict[str, str] = None):
        self.template = template
        self.defaults = defaults or {}
        self._variables = self._extract_variables()

    def _extract_variables(self) -> set:
        """Extract variable names from template."""
        return set(re.findall(r'\{(\w+)\}', self.template))

    def format(self, **kwargs) -> str:
        """Format template with variables."""
        # Merge defaults with provided values
        values = {**self.defaults, **kwargs}

        # Check for missing required variables
        missing = self._variables - set(values.keys())
        if missing:
            raise ValueError(f"Missing required variables: {missing}")

        return self.template.format(**values)

    def partial(self, **kwargs) -> "PromptTemplate":
        """Create new template with some variables filled."""
        new_defaults = {**self.defaults, **kwargs}
        return PromptTemplate(self.template, new_defaults)

# Common templates
TEMPLATES = {
    "classification": PromptTemplate(
        """Classify the following {input_type} into one of these categories: {categories}

{input_type}:
<input>
{input}
</input>

Respond with only the category name."""
    ),

    "extraction": PromptTemplate(
        """Extract {fields} from the following {document_type}.

{document_type}:
<document>
{document}
</document>

Output as JSON with fields: {fields}
Use null for fields not found."""
    ),

    "summarization": PromptTemplate(
        """Summarize the following {content_type} in {length}.

{content_type}:
<content>
{content}
</content>

Focus on: {focus_areas}"""
    ),

    "qa": PromptTemplate(
        """Answer the question based only on the provided context.

Context:
<context>
{context}
</context>

Question: {question}

If the answer is not in the context, say "I cannot find this information in the provided context."
"""
    )
}

# Usage
prompt = TEMPLATES["classification"].format(
    input_type="customer feedback",
    categories="positive, negative, neutral",
    input="Great product, love it!"
)
```

---

## Testing Utilities

### Mock Client

```python
from unittest.mock import MagicMock, patch
from dataclasses import dataclass

@dataclass
class MockChoice:
    message: MagicMock
    finish_reason: str = "stop"

@dataclass
class MockUsage:
    prompt_tokens: int = 10
    completion_tokens: int = 20
    total_tokens: int = 30

@dataclass
class MockResponse:
    choices: list
    model: str = "gpt-4o-2024-08-06"
    usage: MockUsage = None

    def __post_init__(self):
        self.usage = self.usage or MockUsage()

def create_mock_response(content: str, **kwargs) -> MockResponse:
    """Create mock API response for testing."""
    message = MagicMock()
    message.content = content
    message.tool_calls = kwargs.get("tool_calls")
    message.refusal = kwargs.get("refusal")

    return MockResponse(
        choices=[MockChoice(message=message)],
        **{k: v for k, v in kwargs.items() if k not in ["tool_calls", "refusal"]}
    )

# Usage in tests
def test_my_function():
    with patch("openai.OpenAI") as mock_openai:
        mock_client = MagicMock()
        mock_openai.return_value = mock_client

        mock_client.chat.completions.create.return_value = create_mock_response(
            "Hello, world!"
        )

        result = my_function_that_uses_openai()
        assert "Hello" in result
```

### Test Data Generator

```python
def generate_test_messages(
    num_turns: int = 3,
    include_system: bool = True
) -> List[Dict]:
    """Generate test message sequences."""
    messages = []

    if include_system:
        messages.append({
            "role": "system",
            "content": "You are a helpful assistant."
        })

    for i in range(num_turns):
        messages.append({
            "role": "user",
            "content": f"Test user message {i+1}"
        })
        messages.append({
            "role": "assistant",
            "content": f"Test assistant response {i+1}"
        })

    return messages

def generate_test_tool_calls(num_calls: int = 2) -> List[Dict]:
    """Generate test tool call data."""
    return [
        {
            "id": f"call_{i}",
            "type": "function",
            "function": {
                "name": f"test_function_{i}",
                "arguments": json.dumps({"arg": f"value_{i}"})
            }
        }
        for i in range(num_calls)
    ]
```

---

## Quick Reference

### Template Selection Guide

| Task | Template/Pattern |
|------|------------------|
| Single request | Basic Completion |
| Multi-turn | Conversation Manager |
| Real-time UI | Stream Handler |
| JSON output | Structured Output Schema |
| External actions | Tool Executor |
| Cost optimization | Usage Tracker |
| Testing | Mock Client |
