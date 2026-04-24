# Autonomous Agents - Production Templates

## Table of Contents

1. [Project Structure](#project-structure)
2. [Tool Definition Template](#tool-definition-template)
3. [Agent Configuration Template](#agent-configuration-template)
4. [Logging Setup Template](#logging-setup-template)
5. [Error Handling Template](#error-handling-template)
6. [Evaluation Template](#evaluation-template)
7. [Multi-Agent Configuration](#multi-agent-configuration)
8. [Docker Deployment Template](#docker-deployment-template)

---

## Project Structure

```
agent_project/
├── src/
│   ├── __init__.py
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── base.py           # Base agent class
│   │   ├── react.py          # ReAct implementation
│   │   ├── planner.py        # Plan-and-Execute
│   │   ├── reflexion.py      # Reflexion agent
│   │   └── multi_agent.py    # Multi-agent system
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── base.py           # Tool base class
│   │   ├── search.py         # Search tools
│   │   ├── code.py           # Code execution
│   │   └── file.py           # File operations
│   ├── memory/
│   │   ├── __init__.py
│   │   ├── short_term.py
│   │   ├── long_term.py
│   │   └── vector_store.py
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── openai.py
│   │   ├── anthropic.py
│   │   └── router.py         # LLM routing
│   └── utils/
│       ├── __init__.py
│       ├── logging.py
│       ├── metrics.py
│       └── retry.py
├── config/
│   ├── agent.yaml
│   ├── tools.yaml
│   └── logging.yaml
├── tests/
│   ├── test_agent.py
│   ├── test_tools.py
│   └── test_memory.py
├── scripts/
│   ├── run_agent.py
│   └── evaluate.py
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yaml
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

## Tool Definition Template

### tools/base.py

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Optional
import json
import logging

logger = logging.getLogger(__name__)


@dataclass
class ToolResult:
    """Standardized tool result."""
    success: bool
    data: Any
    error: Optional[str] = None
    metadata: Dict = field(default_factory=dict)

    def to_string(self) -> str:
        if self.success:
            if isinstance(self.data, (dict, list)):
                return json.dumps(self.data, indent=2)
            return str(self.data)
        return f"Error: {self.error}"


class BaseTool(ABC):
    """Base class for all tools."""

    name: str
    description: str
    parameters: Dict

    def __init__(self):
        self._call_count = 0
        self._last_call_time = None

    @abstractmethod
    def _execute(self, **kwargs) -> ToolResult:
        """Internal execution logic."""
        pass

    def execute(self, **kwargs) -> str:
        """Execute tool with logging and error handling."""
        self._call_count += 1
        logger.info(f"Tool {self.name} called with: {kwargs}")

        try:
            result = self._execute(**kwargs)
            logger.info(f"Tool {self.name} result: {result.success}")
            return result.to_string()
        except Exception as e:
            logger.error(f"Tool {self.name} error: {e}")
            return ToolResult(
                success=False,
                data=None,
                error=str(e)
            ).to_string()

    def to_openai_format(self) -> Dict:
        """Convert to OpenAI function format."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters
            }
        }

    def to_anthropic_format(self) -> Dict:
        """Convert to Anthropic tool format."""
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.parameters
        }


class ToolRegistry:
    """Registry for managing tools."""

    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}

    def register(self, tool: BaseTool):
        """Register a tool."""
        self._tools[tool.name] = tool

    def get(self, name: str) -> Optional[BaseTool]:
        """Get tool by name."""
        return self._tools.get(name)

    def all(self) -> Dict[str, BaseTool]:
        """Get all tools."""
        return self._tools.copy()

    def to_openai_format(self) -> list:
        """Get all tools in OpenAI format."""
        return [t.to_openai_format() for t in self._tools.values()]


# Global registry
tool_registry = ToolRegistry()
```

### tools/search.py

```python
from .base import BaseTool, ToolResult, tool_registry
import httpx


class WebSearchTool(BaseTool):
    """Web search tool using search API."""

    name = "web_search"
    description = "Search the web for information. Returns relevant results."
    parameters = {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query"
            },
            "num_results": {
                "type": "integer",
                "description": "Number of results (default: 5)",
                "default": 5
            }
        },
        "required": ["query"]
    }

    def __init__(self, api_key: str, endpoint: str = None):
        super().__init__()
        self.api_key = api_key
        self.endpoint = endpoint or "https://api.search.example.com/search"

    def _execute(self, query: str, num_results: int = 5) -> ToolResult:
        """Execute web search."""
        try:
            response = httpx.get(
                self.endpoint,
                params={"q": query, "num": num_results},
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=10
            )
            response.raise_for_status()

            data = response.json()
            results = [
                {
                    "title": r["title"],
                    "url": r["url"],
                    "snippet": r["snippet"]
                }
                for r in data.get("results", [])
            ]

            return ToolResult(
                success=True,
                data=results,
                metadata={"query": query, "num_results": len(results)}
            )

        except httpx.TimeoutException:
            return ToolResult(
                success=False,
                data=None,
                error="Search request timed out"
            )
        except Exception as e:
            return ToolResult(
                success=False,
                data=None,
                error=str(e)
            )


# Register tool
# tool_registry.register(WebSearchTool(api_key="..."))
```

---

## Agent Configuration Template

### config/agent.yaml

```yaml
# Agent Configuration

agent:
  type: "react"  # react, plan_execute, reflexion, multi_agent
  model: "gpt-4o"
  max_iterations: 20
  timeout_seconds: 300

llm:
  provider: "openai"  # openai, anthropic, azure
  model: "gpt-4o"
  temperature: 0.7
  max_tokens: 4096

  # Provider-specific
  openai:
    api_key: "${OPENAI_API_KEY}"
    organization: "${OPENAI_ORG_ID}"

  anthropic:
    api_key: "${ANTHROPIC_API_KEY}"

memory:
  enabled: true
  type: "hybrid"  # short_term, long_term, hybrid

  short_term:
    max_entries: 20

  long_term:
    provider: "qdrant"  # qdrant, pinecone, chroma
    collection: "agent_memory"

    qdrant:
      url: "http://localhost:6333"
      api_key: "${QDRANT_API_KEY}"

  embedding:
    model: "text-embedding-3-small"
    dimensions: 1536

tools:
  enabled:
    - web_search
    - code_execute
    - file_read
    - file_write

  web_search:
    api_key: "${SEARCH_API_KEY}"
    timeout: 10

  code_execute:
    sandbox: true
    timeout: 30
    allowed_languages:
      - python
      - javascript

safety:
  max_tool_calls_per_iteration: 5
  require_approval_for:
    - file_write
    - code_execute
  blocked_patterns:
    - "rm -rf"
    - "DROP TABLE"

reflection:
  enabled: true
  max_attempts: 3
  reflection_model: "gpt-4o-mini"

logging:
  level: "INFO"
  format: "json"
  include_llm_calls: true
  include_tool_calls: true

metrics:
  enabled: true
  track:
    - token_usage
    - latency
    - success_rate
    - tool_usage
```

### config/loader.py

```python
import yaml
import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional


def load_config(config_path: str) -> Dict:
    """Load configuration with environment variable substitution."""
    with open(config_path) as f:
        content = f.read()

    # Substitute environment variables
    for key, value in os.environ.items():
        content = content.replace(f"${{{key}}}", value)

    return yaml.safe_load(content)


@dataclass
class LLMConfig:
    provider: str
    model: str
    temperature: float = 0.7
    max_tokens: int = 4096
    api_key: str = ""


@dataclass
class MemoryConfig:
    enabled: bool = True
    type: str = "hybrid"
    max_short_term: int = 20
    vector_store: str = "qdrant"
    collection: str = "agent_memory"


@dataclass
class SafetyConfig:
    max_tool_calls: int = 5
    require_approval: List[str] = field(default_factory=list)
    blocked_patterns: List[str] = field(default_factory=list)


@dataclass
class AgentConfig:
    type: str = "react"
    model: str = "gpt-4o"
    max_iterations: int = 20
    timeout_seconds: int = 300
    llm: LLMConfig = field(default_factory=LLMConfig)
    memory: MemoryConfig = field(default_factory=MemoryConfig)
    safety: SafetyConfig = field(default_factory=SafetyConfig)
    tools: List[str] = field(default_factory=list)

    @classmethod
    def from_yaml(cls, path: str) -> "AgentConfig":
        """Load config from YAML file."""
        data = load_config(path)
        agent_data = data.get("agent", {})

        return cls(
            type=agent_data.get("type", "react"),
            model=agent_data.get("model", "gpt-4o"),
            max_iterations=agent_data.get("max_iterations", 20),
            timeout_seconds=agent_data.get("timeout_seconds", 300),
            llm=LLMConfig(**data.get("llm", {})),
            memory=MemoryConfig(**data.get("memory", {})),
            safety=SafetyConfig(**data.get("safety", {})),
            tools=data.get("tools", {}).get("enabled", [])
        )
```

---

## Logging Setup Template

### utils/logging.py

```python
import logging
import json
from datetime import datetime
from typing import Dict, Any
import sys


class JSONFormatter(logging.Formatter):
    """JSON log formatter."""

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Add extra fields
        if hasattr(record, "agent_id"):
            log_data["agent_id"] = record.agent_id
        if hasattr(record, "iteration"):
            log_data["iteration"] = record.iteration
        if hasattr(record, "tool_name"):
            log_data["tool_name"] = record.tool_name
        if hasattr(record, "token_usage"):
            log_data["token_usage"] = record.token_usage

        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data)


class AgentLogger:
    """Structured logger for agents."""

    def __init__(self, agent_id: str, level: str = "INFO"):
        self.agent_id = agent_id
        self.logger = logging.getLogger(f"agent.{agent_id}")
        self.logger.setLevel(getattr(logging, level.upper()))

        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(JSONFormatter())
            self.logger.addHandler(handler)

    def _log(
        self,
        level: str,
        message: str,
        **kwargs
    ):
        """Internal log method."""
        extra = {"agent_id": self.agent_id, **kwargs}
        getattr(self.logger, level)(message, extra=extra)

    def info(self, message: str, **kwargs):
        self._log("info", message, **kwargs)

    def error(self, message: str, **kwargs):
        self._log("error", message, **kwargs)

    def warning(self, message: str, **kwargs):
        self._log("warning", message, **kwargs)

    def debug(self, message: str, **kwargs):
        self._log("debug", message, **kwargs)

    def iteration_start(self, iteration: int, task: str):
        """Log iteration start."""
        self.info(
            f"Starting iteration {iteration}",
            iteration=iteration,
            task=task[:100]
        )

    def tool_call(
        self,
        tool_name: str,
        arguments: Dict,
        result: str
    ):
        """Log tool call."""
        self.info(
            f"Tool call: {tool_name}",
            tool_name=tool_name,
            arguments=arguments,
            result_preview=result[:200]
        )

    def llm_call(
        self,
        model: str,
        prompt_tokens: int,
        completion_tokens: int
    ):
        """Log LLM call."""
        self.info(
            f"LLM call to {model}",
            model=model,
            token_usage={
                "prompt": prompt_tokens,
                "completion": completion_tokens,
                "total": prompt_tokens + completion_tokens
            }
        )

    def task_complete(self, success: bool, result: str = None):
        """Log task completion."""
        self.info(
            "Task completed" if success else "Task failed",
            success=success,
            result_preview=result[:200] if result else None
        )


def setup_logging(config: Dict = None):
    """Setup logging configuration."""
    config = config or {}

    level = config.get("level", "INFO")
    format_type = config.get("format", "json")

    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))

    handler = logging.StreamHandler(sys.stdout)

    if format_type == "json":
        handler.setFormatter(JSONFormatter())
    else:
        handler.setFormatter(logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        ))

    root_logger.addHandler(handler)
```

---

## Error Handling Template

### utils/retry.py

```python
import asyncio
from functools import wraps
from typing import Type, Tuple, Callable, Any
import logging
import random

logger = logging.getLogger(__name__)


class RetryConfig:
    """Configuration for retry behavior."""

    def __init__(
        self,
        max_attempts: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
        jitter: bool = True,
        retryable_exceptions: Tuple[Type[Exception], ...] = (Exception,)
    ):
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.jitter = jitter
        self.retryable_exceptions = retryable_exceptions

    def get_delay(self, attempt: int) -> float:
        """Calculate delay for attempt."""
        delay = self.base_delay * (self.exponential_base ** attempt)
        delay = min(delay, self.max_delay)

        if self.jitter:
            delay = delay * (0.5 + random.random())

        return delay


def retry(config: RetryConfig = None):
    """Decorator for retrying functions."""
    config = config or RetryConfig()

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def sync_wrapper(*args, **kwargs) -> Any:
            last_exception = None

            for attempt in range(config.max_attempts):
                try:
                    return func(*args, **kwargs)
                except config.retryable_exceptions as e:
                    last_exception = e
                    if attempt < config.max_attempts - 1:
                        delay = config.get_delay(attempt)
                        logger.warning(
                            f"Attempt {attempt + 1} failed: {e}. "
                            f"Retrying in {delay:.2f}s"
                        )
                        import time
                        time.sleep(delay)

            raise last_exception

        @wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            last_exception = None

            for attempt in range(config.max_attempts):
                try:
                    return await func(*args, **kwargs)
                except config.retryable_exceptions as e:
                    last_exception = e
                    if attempt < config.max_attempts - 1:
                        delay = config.get_delay(attempt)
                        logger.warning(
                            f"Attempt {attempt + 1} failed: {e}. "
                            f"Retrying in {delay:.2f}s"
                        )
                        await asyncio.sleep(delay)

            raise last_exception

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    return decorator


class CircuitBreaker:
    """Circuit breaker for external services."""

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 30.0
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failures = 0
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half-open

    def can_execute(self) -> bool:
        """Check if execution is allowed."""
        if self.state == "closed":
            return True

        if self.state == "open":
            import time
            if time.time() - self.last_failure_time >= self.recovery_timeout:
                self.state = "half-open"
                return True
            return False

        return True  # half-open

    def record_success(self):
        """Record successful execution."""
        self.failures = 0
        self.state = "closed"

    def record_failure(self):
        """Record failed execution."""
        import time
        self.failures += 1
        self.last_failure_time = time.time()

        if self.failures >= self.failure_threshold:
            self.state = "open"
            logger.warning("Circuit breaker opened")


# LLM-specific retry config
llm_retry_config = RetryConfig(
    max_attempts=3,
    base_delay=1.0,
    max_delay=30.0,
    retryable_exceptions=(
        ConnectionError,
        TimeoutError,
        # Add provider-specific exceptions
    )
)
```

---

## Evaluation Template

### scripts/evaluate.py

```python
from dataclasses import dataclass, field
from typing import List, Dict, Any, Callable
import json
import time
from statistics import mean, stdev


@dataclass
class TestCase:
    """Single test case for evaluation."""
    id: str
    task: str
    expected_output: str = None
    expected_tools: List[str] = field(default_factory=list)
    success_criteria: Callable[[str], bool] = None
    max_iterations: int = 20
    timeout: float = 60.0


@dataclass
class TestResult:
    """Result of a single test."""
    test_id: str
    success: bool
    output: str
    iterations: int
    latency: float
    token_usage: int
    tools_used: List[str]
    error: str = None


@dataclass
class EvaluationReport:
    """Full evaluation report."""
    total_tests: int
    passed: int
    failed: int
    success_rate: float
    avg_latency: float
    avg_iterations: float
    avg_tokens: float
    results: List[TestResult]

    def to_dict(self) -> Dict:
        return {
            "summary": {
                "total": self.total_tests,
                "passed": self.passed,
                "failed": self.failed,
                "success_rate": f"{self.success_rate:.2%}",
                "avg_latency": f"{self.avg_latency:.2f}s",
                "avg_iterations": f"{self.avg_iterations:.1f}",
                "avg_tokens": f"{self.avg_tokens:.0f}"
            },
            "results": [
                {
                    "test_id": r.test_id,
                    "success": r.success,
                    "iterations": r.iterations,
                    "latency": f"{r.latency:.2f}s",
                    "tokens": r.token_usage,
                    "error": r.error
                }
                for r in self.results
            ]
        }


class AgentEvaluator:
    """Evaluator for agent performance."""

    def __init__(self, agent_factory: Callable):
        """
        Args:
            agent_factory: Function that creates a new agent instance
        """
        self.agent_factory = agent_factory
        self.results: List[TestResult] = []

    def run_test(self, test: TestCase) -> TestResult:
        """Run a single test case."""
        agent = self.agent_factory()

        start_time = time.time()
        try:
            # Run agent
            result = agent.run(test.task)
            latency = time.time() - start_time

            # Check success
            if test.success_criteria:
                success = test.success_criteria(result)
            elif test.expected_output:
                success = test.expected_output.lower() in result.lower()
            else:
                success = True  # Assume success if no criteria

            return TestResult(
                test_id=test.id,
                success=success,
                output=result,
                iterations=getattr(agent, 'iteration_count', 0),
                latency=latency,
                token_usage=getattr(agent, 'total_tokens', 0),
                tools_used=getattr(agent, 'tools_used', [])
            )

        except Exception as e:
            return TestResult(
                test_id=test.id,
                success=False,
                output="",
                iterations=0,
                latency=time.time() - start_time,
                token_usage=0,
                tools_used=[],
                error=str(e)
            )

    def evaluate(self, tests: List[TestCase]) -> EvaluationReport:
        """Run full evaluation."""
        self.results = []

        for test in tests:
            print(f"Running test: {test.id}")
            result = self.run_test(test)
            self.results.append(result)
            print(f"  Result: {'PASS' if result.success else 'FAIL'}")

        passed = sum(1 for r in self.results if r.success)
        latencies = [r.latency for r in self.results]
        iterations = [r.iterations for r in self.results]
        tokens = [r.token_usage for r in self.results]

        return EvaluationReport(
            total_tests=len(tests),
            passed=passed,
            failed=len(tests) - passed,
            success_rate=passed / len(tests) if tests else 0,
            avg_latency=mean(latencies) if latencies else 0,
            avg_iterations=mean(iterations) if iterations else 0,
            avg_tokens=mean(tokens) if tokens else 0,
            results=self.results
        )


# Example test suite
test_suite = [
    TestCase(
        id="math_simple",
        task="What is 25 * 4?",
        expected_output="100",
        expected_tools=["calculate"]
    ),
    TestCase(
        id="search_basic",
        task="What is the capital of France?",
        success_criteria=lambda x: "paris" in x.lower(),
        expected_tools=["web_search"]
    ),
    TestCase(
        id="multi_step",
        task="Search for the population of Japan and calculate 10% of it",
        success_criteria=lambda x: any(
            c.isdigit() for c in x
        ),
        expected_tools=["web_search", "calculate"]
    ),
]


# Usage
# def create_agent():
#     return ReActAgent(tools=[...])
#
# evaluator = AgentEvaluator(create_agent)
# report = evaluator.evaluate(test_suite)
# print(json.dumps(report.to_dict(), indent=2))
```

---

## Multi-Agent Configuration

### config/multi_agent.yaml

```yaml
# Multi-Agent System Configuration

orchestration:
  type: "supervisor"  # supervisor, hierarchical, debate, market
  supervisor_model: "gpt-4o"
  max_rounds: 10

agents:
  researcher:
    model: "gpt-4o"
    system_prompt: |
      You are a research specialist.
      Your job is to gather and synthesize information.
      Always cite sources and verify facts.
    tools:
      - web_search
      - document_search
    max_iterations: 15

  coder:
    model: "gpt-4o"
    system_prompt: |
      You are a coding specialist.
      Write clean, tested, documented code.
      Follow best practices for the language.
    tools:
      - code_execute
      - file_read
      - file_write
    max_iterations: 20

  reviewer:
    model: "gpt-4o-mini"
    system_prompt: |
      You are a code review specialist.
      Analyze code for bugs, security issues, and improvements.
      Be constructive and specific.
    tools:
      - code_analyze
      - file_read
    max_iterations: 10

  writer:
    model: "gpt-4o"
    system_prompt: |
      You are a technical writer.
      Create clear, concise documentation.
      Use examples and proper formatting.
    tools:
      - file_write
    max_iterations: 10

routing:
  rules:
    - pattern: "research|find|search|look up"
      agent: researcher
    - pattern: "code|implement|write.*function|create.*class"
      agent: coder
    - pattern: "review|analyze|check"
      agent: reviewer
    - pattern: "document|write.*docs|explain"
      agent: writer

  default: researcher

communication:
  shared_context: true
  max_context_size: 10000
  summarize_after: 5000

collaboration:
  allow_agent_to_agent: true
  require_supervisor_approval: false
  max_handoffs: 5
```

---

## Docker Deployment Template

### docker/Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY src/ ./src/
COPY config/ ./config/
COPY scripts/ ./scripts/

# Set environment
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run
CMD ["python", "scripts/run_agent.py"]
```

### docker/docker-compose.yaml

```yaml
version: '3.8'

services:
  agent:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - QDRANT_URL=http://qdrant:6333
    depends_on:
      - qdrant
    volumes:
      - ../config:/app/config:ro
      - agent_logs:/app/logs
    restart: unless-stopped

  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
    volumes:
      - qdrant_data:/qdrant/storage
    restart: unless-stopped

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD:-admin}
    volumes:
      - grafana_data:/var/lib/grafana
    depends_on:
      - prometheus
    restart: unless-stopped

volumes:
  agent_logs:
  qdrant_data:
  grafana_data:
```

### scripts/run_agent.py

```python
#!/usr/bin/env python3
"""Run agent with configuration."""

import argparse
import asyncio
from pathlib import Path

from src.agent.react import ReActAgent
from src.config.loader import AgentConfig
from src.tools.base import tool_registry
from src.utils.logging import setup_logging, AgentLogger


def main():
    parser = argparse.ArgumentParser(description="Run autonomous agent")
    parser.add_argument(
        "--config",
        type=str,
        default="config/agent.yaml",
        help="Path to config file"
    )
    parser.add_argument(
        "--task",
        type=str,
        required=True,
        help="Task for the agent"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    args = parser.parse_args()

    # Load config
    config = AgentConfig.from_yaml(args.config)

    # Setup logging
    setup_logging({"level": "DEBUG" if args.verbose else "INFO"})
    logger = AgentLogger("main")

    # Create agent
    tools = [tool_registry.get(t) for t in config.tools if tool_registry.get(t)]
    agent = ReActAgent(
        tools=tools,
        model=config.model,
        max_iterations=config.max_iterations
    )

    # Run
    logger.info(f"Starting agent with task: {args.task}")
    result = agent.run(args.task)
    logger.task_complete(success=True, result=result)

    print("\n" + "=" * 50)
    print("RESULT:")
    print(result)


if __name__ == "__main__":
    main()
```
