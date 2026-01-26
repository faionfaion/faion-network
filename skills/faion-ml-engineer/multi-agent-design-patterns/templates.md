# Multi-Agent Design Patterns: Templates

Reusable scaffolds and configuration templates for multi-agent systems.

## Project Structure Template

```
multi-agent-project/
├── agents/
│   ├── __init__.py
│   ├── base.py              # Base agent class
│   ├── supervisor.py        # Supervisor agent
│   └── workers/
│       ├── __init__.py
│       ├── researcher.py
│       ├── coder.py
│       └── writer.py
├── orchestration/
│   ├── __init__.py
│   ├── graph.py             # LangGraph definition
│   ├── state.py             # State definitions
│   └── routing.py           # Routing logic
├── tools/
│   ├── __init__.py
│   ├── search.py
│   ├── code_executor.py
│   └── file_manager.py
├── config/
│   ├── agents.yaml          # Agent configurations
│   ├── routing.yaml         # Routing rules
│   └── prompts/
│       ├── supervisor.md
│       └── workers/
├── tests/
│   ├── test_agents.py
│   ├── test_routing.py
│   └── test_integration.py
└── main.py
```

---

## Base Agent Template

```python
# agents/base.py
from abc import ABC, abstractmethod
from typing import Any, Optional
from dataclasses import dataclass, field
from langchain_openai import ChatOpenAI

@dataclass
class AgentConfig:
    """Configuration for an agent."""
    name: str
    role: str
    goal: str
    backstory: str = ""
    model: str = "gpt-4o"
    temperature: float = 0.7
    tools: list = field(default_factory=list)
    max_iterations: int = 10
    verbose: bool = False

class BaseAgent(ABC):
    """Base class for all agents."""

    def __init__(self, config: AgentConfig):
        self.config = config
        self.llm = ChatOpenAI(
            model=config.model,
            temperature=config.temperature
        )
        self._setup_tools()

    def _setup_tools(self):
        """Initialize agent tools."""
        self.tools = self.config.tools

    @abstractmethod
    async def execute(self, task: dict, state: dict) -> dict:
        """Execute a task and return result."""
        pass

    def get_system_prompt(self) -> str:
        """Generate system prompt for agent."""
        return f"""You are {self.config.name}, a {self.config.role}.

Goal: {self.config.goal}

{self.config.backstory}

Guidelines:
- Focus on your specialized domain
- Provide structured, actionable outputs
- Escalate if task is outside your expertise
- Be concise but thorough"""

    async def invoke(self, prompt: str) -> str:
        """Invoke LLM with agent context."""
        messages = [
            {"role": "system", "content": self.get_system_prompt()},
            {"role": "user", "content": prompt}
        ]
        response = await self.llm.ainvoke(messages)
        return response.content
```

---

## Supervisor Agent Template

```python
# agents/supervisor.py
from typing import Literal
from .base import BaseAgent, AgentConfig

class SupervisorAgent(BaseAgent):
    """Supervisor that routes requests to workers."""

    def __init__(self, config: AgentConfig, workers: dict[str, BaseAgent]):
        super().__init__(config)
        self.workers = workers

    def get_routing_prompt(self, task: str) -> str:
        worker_descriptions = "\n".join([
            f"- {name}: {worker.config.goal}"
            for name, worker in self.workers.items()
        ])

        return f"""Analyze this task and decide which worker should handle it.

Available workers:
{worker_descriptions}

Task: {task}

Respond with ONLY the worker name. If multiple workers needed, respond with the first one to start."""

    async def route(self, task: str) -> str:
        """Route task to appropriate worker."""
        prompt = self.get_routing_prompt(task)
        response = await self.invoke(prompt)
        return response.strip().lower()

    async def execute(self, task: dict, state: dict) -> dict:
        """Route and execute task."""
        worker_name = await self.route(task["content"])

        if worker_name not in self.workers:
            return {
                "status": "error",
                "message": f"Unknown worker: {worker_name}",
                "routed_to": None
            }

        worker = self.workers[worker_name]
        result = await worker.execute(task, state)

        return {
            "status": "success",
            "routed_to": worker_name,
            "result": result
        }

    async def aggregate_results(self, results: list[dict]) -> str:
        """Aggregate multiple worker results."""
        prompt = f"""Synthesize these worker results into a cohesive response:

{results}

Provide a unified summary that addresses the original task."""

        return await self.invoke(prompt)
```

---

## Worker Agent Template

```python
# agents/workers/base_worker.py
from ..base import BaseAgent, AgentConfig

class WorkerAgent(BaseAgent):
    """Base worker agent with tool execution."""

    def __init__(self, config: AgentConfig):
        super().__init__(config)
        self.output_key = config.name + "_output"

    async def execute(self, task: dict, state: dict) -> dict:
        """Execute task using tools and LLM."""
        context = self._get_context_from_state(state)

        execution_prompt = f"""Execute this task:

Task: {task['content']}

Context from previous steps:
{context}

Use your tools as needed. Provide structured output."""

        # Tool execution loop would go here
        result = await self.invoke(execution_prompt)

        return {
            "output_key": self.output_key,
            "result": result,
            "tools_used": [],  # Track tool usage
            "status": "completed"
        }

    def _get_context_from_state(self, state: dict) -> str:
        """Extract relevant context from shared state."""
        relevant_keys = [k for k in state.keys() if "_output" in k]
        context_parts = [
            f"{k}: {state[k]}" for k in relevant_keys if state[k]
        ]
        return "\n".join(context_parts) if context_parts else "No previous context."

    def can_handle(self, task: dict) -> float:
        """Return confidence score (0-1) for handling this task."""
        # Override in subclasses for smart routing
        return 0.5
```

---

## State Definition Template

```python
# orchestration/state.py
from typing import TypedDict, Optional, Any
from dataclasses import dataclass, field

class BaseAgentState(TypedDict):
    """Base state for all multi-agent systems."""
    messages: list[dict]
    current_agent: str
    iteration: int
    error: Optional[str]

class SupervisorState(BaseAgentState):
    """State for supervisor pattern."""
    routed_to: str
    worker_results: dict[str, Any]
    final_response: Optional[str]

class HierarchicalState(BaseAgentState):
    """State for hierarchical pattern."""
    goal: str
    subtasks: list[dict]
    team_assignments: dict[str, list[str]]
    team_results: dict[str, list[dict]]
    final_output: Optional[str]

class SequentialState(BaseAgentState):
    """State for sequential pattern."""
    pipeline_stage: int
    stage_outputs: dict[str, Any]
    validation_passed: bool
    final_output: Optional[str]

class PeerToPeerState(BaseAgentState):
    """State for peer-to-peer pattern."""
    message_history: list[dict]
    visited_agents: list[str]
    routing_path: list[str]
    consensus_reached: bool
    final_output: Optional[str]

# Factory function
def create_state(pattern: str, **kwargs) -> dict:
    """Create initial state for a pattern."""
    base = {
        "messages": [],
        "current_agent": "",
        "iteration": 0,
        "error": None
    }

    pattern_defaults = {
        "supervisor": {
            "routed_to": "",
            "worker_results": {},
            "final_response": None
        },
        "hierarchical": {
            "goal": "",
            "subtasks": [],
            "team_assignments": {},
            "team_results": {},
            "final_output": None
        },
        "sequential": {
            "pipeline_stage": 0,
            "stage_outputs": {},
            "validation_passed": True,
            "final_output": None
        },
        "peer_to_peer": {
            "message_history": [],
            "visited_agents": [],
            "routing_path": [],
            "consensus_reached": False,
            "final_output": None
        }
    }

    return {**base, **pattern_defaults.get(pattern, {}), **kwargs}
```

---

## Configuration Templates

### Agent Configuration (YAML)

```yaml
# config/agents.yaml

# Supervisor configuration
supervisor:
  name: coordinator
  role: Project Coordinator
  goal: Route requests to appropriate specialists and aggregate results
  model: gpt-4o
  temperature: 0.3
  max_iterations: 5
  routing_strategy: llm  # or "rules"

# Worker configurations
workers:
  researcher:
    name: researcher
    role: Research Specialist
    goal: Gather accurate information from various sources
    backstory: Expert researcher with strong analytical skills
    model: gpt-4o
    temperature: 0.7
    tools:
      - web_search
      - document_reader
      - data_analyzer

  coder:
    name: coder
    role: Software Developer
    goal: Write clean, efficient, well-documented code
    backstory: Senior developer with expertise in multiple languages
    model: gpt-4o
    temperature: 0.5
    tools:
      - code_executor
      - file_manager
      - test_runner

  writer:
    name: writer
    role: Content Writer
    goal: Create engaging, well-structured content
    backstory: Professional writer with technical background
    model: gpt-4o
    temperature: 0.8
    tools:
      - grammar_checker
      - style_guide

# Team configurations (for hierarchical)
teams:
  research_team:
    lead: research_lead
    workers:
      - researcher
      - data_analyst

  development_team:
    lead: dev_lead
    workers:
      - coder
      - tester
```

### Routing Configuration (YAML)

```yaml
# config/routing.yaml

# Rule-based routing
rules:
  - pattern: "search|find|research|look up"
    route_to: researcher
    priority: 1

  - pattern: "code|implement|debug|fix|program"
    route_to: coder
    priority: 1

  - pattern: "write|draft|edit|summarize"
    route_to: writer
    priority: 1

  - pattern: "analyze|evaluate|assess"
    route_to: researcher
    priority: 2

# Fallback
default_route: researcher

# LLM routing configuration
llm_routing:
  enabled: true
  model: gpt-4o-mini
  temperature: 0.1
  fallback_to_rules: true
```

---

## LangGraph Template

```python
# orchestration/graph.py
from typing import Literal, Callable
from langgraph.graph import StateGraph, END
from .state import SupervisorState

def create_supervisor_graph(
    supervisor_fn: Callable,
    workers: dict[str, Callable],
    aggregator_fn: Callable
) -> StateGraph:
    """Factory for creating supervisor pattern graph."""

    def route_to_worker(state: SupervisorState) -> str:
        return state["routed_to"]

    # Build graph
    workflow = StateGraph(SupervisorState)

    # Add nodes
    workflow.add_node("supervisor", supervisor_fn)
    for name, worker_fn in workers.items():
        workflow.add_node(name, worker_fn)
    workflow.add_node("aggregator", aggregator_fn)

    # Set entry
    workflow.set_entry_point("supervisor")

    # Add conditional edges from supervisor to workers
    workflow.add_conditional_edges(
        "supervisor",
        route_to_worker,
        {name: name for name in workers.keys()}
    )

    # Add edges from workers to aggregator
    for name in workers.keys():
        workflow.add_edge(name, "aggregator")

    # Aggregator to end
    workflow.add_edge("aggregator", END)

    return workflow.compile()


def create_sequential_graph(
    stages: list[tuple[str, Callable]]
) -> StateGraph:
    """Factory for creating sequential pattern graph."""
    from .state import SequentialState

    workflow = StateGraph(SequentialState)

    # Add all stage nodes
    for name, fn in stages:
        workflow.add_node(name, fn)

    # Set entry to first stage
    workflow.set_entry_point(stages[0][0])

    # Chain stages sequentially
    for i in range(len(stages) - 1):
        workflow.add_edge(stages[i][0], stages[i + 1][0])

    # Last stage to END
    workflow.add_edge(stages[-1][0], END)

    return workflow.compile()


def create_hierarchical_graph(
    top_supervisor_fn: Callable,
    team_coordinators: dict[str, Callable],
    synthesizer_fn: Callable
) -> StateGraph:
    """Factory for creating hierarchical pattern graph."""
    from .state import HierarchicalState

    workflow = StateGraph(HierarchicalState)

    # Add nodes
    workflow.add_node("top_supervisor", top_supervisor_fn)
    for name, fn in team_coordinators.items():
        workflow.add_node(name, fn)
    workflow.add_node("synthesizer", synthesizer_fn)

    # Entry
    workflow.set_entry_point("top_supervisor")

    # Top supervisor to all team coordinators (parallel-like)
    for name in team_coordinators.keys():
        workflow.add_edge("top_supervisor", name)

    # All coordinators to synthesizer
    for name in team_coordinators.keys():
        workflow.add_edge(name, "synthesizer")

    workflow.add_edge("synthesizer", END)

    return workflow.compile()
```

---

## Testing Template

```python
# tests/test_agents.py
import pytest
from unittest.mock import AsyncMock, MagicMock
from agents.supervisor import SupervisorAgent
from agents.base import AgentConfig

@pytest.fixture
def supervisor_config():
    return AgentConfig(
        name="test_supervisor",
        role="Test Coordinator",
        goal="Route test requests"
    )

@pytest.fixture
def mock_workers():
    return {
        "researcher": MagicMock(),
        "coder": MagicMock()
    }

class TestSupervisorAgent:

    @pytest.mark.asyncio
    async def test_routes_research_task_to_researcher(
        self, supervisor_config, mock_workers
    ):
        supervisor = SupervisorAgent(supervisor_config, mock_workers)
        supervisor.llm = AsyncMock()
        supervisor.llm.ainvoke.return_value = MagicMock(content="researcher")

        result = await supervisor.route("Find information about AI")

        assert result == "researcher"

    @pytest.mark.asyncio
    async def test_routes_coding_task_to_coder(
        self, supervisor_config, mock_workers
    ):
        supervisor = SupervisorAgent(supervisor_config, mock_workers)
        supervisor.llm = AsyncMock()
        supervisor.llm.ainvoke.return_value = MagicMock(content="coder")

        result = await supervisor.route("Write a Python function")

        assert result == "coder"

    @pytest.mark.asyncio
    async def test_handles_unknown_worker(
        self, supervisor_config, mock_workers
    ):
        supervisor = SupervisorAgent(supervisor_config, mock_workers)
        supervisor.llm = AsyncMock()
        supervisor.llm.ainvoke.return_value = MagicMock(content="unknown")

        result = await supervisor.execute(
            {"content": "some task"},
            {}
        )

        assert result["status"] == "error"
        assert "unknown" in result["message"].lower()


# tests/test_integration.py
import pytest
from orchestration.graph import create_supervisor_graph

class TestSupervisorIntegration:

    @pytest.mark.asyncio
    async def test_end_to_end_research_task(self):
        """Integration test for complete research workflow."""
        # Setup real or mocked graph
        graph = create_supervisor_graph(
            supervisor_fn=mock_supervisor,
            workers={"researcher": mock_researcher},
            aggregator_fn=mock_aggregator
        )

        result = await graph.ainvoke({
            "messages": [{"role": "user", "content": "Research AI trends"}],
            "current_agent": "",
            "iteration": 0,
            "error": None,
            "routed_to": "",
            "worker_results": {},
            "final_response": None
        })

        assert result["final_response"] is not None
        assert result["routed_to"] == "researcher"
```

---

## Docker Compose Template

```yaml
# docker-compose.yaml
version: '3.8'

services:
  supervisor:
    build:
      context: .
      dockerfile: Dockerfile
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - AGENT_ROLE=supervisor
      - WORKER_ENDPOINTS=researcher:8001,coder:8002
    ports:
      - "8000:8000"
    depends_on:
      - researcher
      - coder

  researcher:
    build:
      context: .
      dockerfile: Dockerfile
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - AGENT_ROLE=researcher
    ports:
      - "8001:8000"

  coder:
    build:
      context: .
      dockerfile: Dockerfile
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - AGENT_ROLE=coder
    ports:
      - "8002:8000"

  redis:
    image: redis:7
    ports:
      - "6379:6379"

  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
```
