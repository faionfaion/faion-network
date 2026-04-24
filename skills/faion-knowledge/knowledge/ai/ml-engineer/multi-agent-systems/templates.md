# Multi-Agent Systems Templates

## Template 1: Basic Agent Configuration

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable
from enum import Enum

class AgentRole(Enum):
    MANAGER = "manager"
    WORKER = "worker"
    COORDINATOR = "coordinator"
    SPECIALIST = "specialist"

@dataclass
class AgentConfig:
    """Configuration for a single agent."""
    name: str
    role: str
    system_prompt: str
    model: str = "gpt-4o"
    temperature: float = 0.7
    max_tokens: int = 4096
    tools: List[Dict] = field(default_factory=list)
    allowed_handoffs: List[str] = field(default_factory=list)
    guardrails: Dict = field(default_factory=dict)

# Example configurations
AGENT_CONFIGS = {
    "researcher": AgentConfig(
        name="Researcher",
        role="Research Analyst",
        system_prompt="""You are a senior research analyst.
Your responsibilities:
- Gather and analyze information
- Identify key insights and trends
- Provide well-sourced findings

Always cite sources and acknowledge uncertainty.""",
        temperature=0.3,  # Lower for factual work
        tools=["web_search", "document_reader"]
    ),

    "developer": AgentConfig(
        name="Developer",
        role="Software Engineer",
        system_prompt="""You are a senior software engineer.
Your responsibilities:
- Write clean, tested code
- Follow best practices and patterns
- Document your solutions

Always consider edge cases and error handling.""",
        temperature=0.2,  # Low for code generation
        tools=["code_executor", "file_reader", "file_writer"]
    ),

    "reviewer": AgentConfig(
        name="Reviewer",
        role="Code Reviewer",
        system_prompt="""You are an expert code reviewer.
Your responsibilities:
- Review code for bugs and security issues
- Check adherence to best practices
- Provide constructive feedback

Be thorough but respectful.""",
        temperature=0.3,
        tools=["code_analyzer", "security_scanner"]
    ),

    "manager": AgentConfig(
        name="Manager",
        role="Project Manager",
        system_prompt="""You are a project manager.
Your responsibilities:
- Decompose complex tasks into subtasks
- Assign work to appropriate team members
- Synthesize results into deliverables

Focus on clarity and actionable outcomes.""",
        temperature=0.5,
        allowed_handoffs=["researcher", "developer", "reviewer"]
    )
}
```

## Template 2: LangGraph State Schema

```python
from typing import TypedDict, Annotated, List, Dict, Any, Optional
from langgraph.graph import StateGraph, START, END
import operator

class BaseAgentState(TypedDict):
    """Base state schema for multi-agent workflows."""
    messages: Annotated[list, operator.add]
    task: str
    status: str  # "pending", "in_progress", "completed", "failed"
    current_agent: str
    results: Annotated[list, operator.add]
    errors: Annotated[list, operator.add]
    metadata: Dict[str, Any]

class HierarchicalState(BaseAgentState):
    """State for hierarchical workflows."""
    plan: List[Dict]
    assignments: List[Dict]
    worker_results: Annotated[list, operator.add]
    synthesis: str

class CollaborativeState(BaseAgentState):
    """State for collaborative workflows."""
    contributions: Dict[str, str]
    iteration: int
    consensus_reached: bool
    shared_artifacts: Dict[str, str]

class DebateState(BaseAgentState):
    """State for debate/verification workflows."""
    proposition: str
    arguments_for: Annotated[list, operator.add]
    arguments_against: Annotated[list, operator.add]
    verdict: str
    confidence: float

# State factory
def create_initial_state(
    task: str,
    state_type: str = "base"
) -> Dict:
    """Create initial state for workflow."""
    base = {
        "messages": [],
        "task": task,
        "status": "pending",
        "current_agent": "",
        "results": [],
        "errors": [],
        "metadata": {}
    }

    if state_type == "hierarchical":
        return {**base, "plan": [], "assignments": [], "worker_results": [], "synthesis": ""}
    elif state_type == "collaborative":
        return {**base, "contributions": {}, "iteration": 0, "consensus_reached": False, "shared_artifacts": {}}
    elif state_type == "debate":
        return {**base, "proposition": "", "arguments_for": [], "arguments_against": [], "verdict": "", "confidence": 0.0}

    return base
```

## Template 3: CrewAI Configuration

```yaml
# crew_config.yaml
agents:
  - name: researcher
    role: Senior Research Analyst
    goal: Uncover comprehensive insights on given topics
    backstory: |
      You are a meticulous researcher with 10+ years of experience
      in technology analysis. You're known for thorough, well-sourced work.
    verbose: true
    allow_delegation: false
    tools:
      - search_tool
      - web_scraper

  - name: analyst
    role: Data Analyst
    goal: Transform research into actionable insights
    backstory: |
      You excel at finding patterns in data and creating
      clear visualizations and summaries.
    verbose: true
    allow_delegation: false
    tools:
      - data_analyzer
      - chart_generator

  - name: writer
    role: Technical Writer
    goal: Create clear, engaging technical content
    backstory: |
      You're an award-winning technical writer who makes
      complex topics accessible without oversimplifying.
    verbose: true
    allow_delegation: true

  - name: editor
    role: Senior Editor
    goal: Ensure content quality and accuracy
    backstory: |
      You have edited for major tech publications and
      have a keen eye for both accuracy and readability.
    verbose: true
    allow_delegation: false

tasks:
  - name: research_task
    description: |
      Conduct comprehensive research on {topic}.
      Focus on: current state, key players, trends, challenges.
    expected_output: Detailed research report with sources
    agent: researcher

  - name: analysis_task
    description: |
      Analyze the research findings.
      Identify key insights, patterns, and opportunities.
    expected_output: Analysis summary with key findings
    agent: analyst
    context:
      - research_task

  - name: writing_task
    description: |
      Write an engaging article based on research and analysis.
      Target audience: technical decision makers.
    expected_output: Draft article (1000-1500 words)
    agent: writer
    context:
      - research_task
      - analysis_task

  - name: editing_task
    description: |
      Review and polish the article.
      Check for accuracy, clarity, and engagement.
    expected_output: Final polished article
    agent: editor
    context:
      - writing_task

process: sequential  # or hierarchical
verbose: true
```

```python
# Load CrewAI from config
import yaml
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

def load_crew_from_config(config_path: str) -> Crew:
    with open(config_path) as f:
        config = yaml.safe_load(f)

    # Initialize tools
    tools_map = {
        "search_tool": SerperDevTool(),
        # Add other tools
    }

    # Create agents
    agents = {}
    for agent_cfg in config["agents"]:
        agent_tools = [tools_map[t] for t in agent_cfg.get("tools", []) if t in tools_map]
        agents[agent_cfg["name"]] = Agent(
            role=agent_cfg["role"],
            goal=agent_cfg["goal"],
            backstory=agent_cfg["backstory"],
            verbose=agent_cfg.get("verbose", True),
            allow_delegation=agent_cfg.get("allow_delegation", False),
            tools=agent_tools
        )

    # Create tasks
    tasks = []
    task_map = {}
    for task_cfg in config["tasks"]:
        context_tasks = [task_map[c] for c in task_cfg.get("context", []) if c in task_map]
        task = Task(
            description=task_cfg["description"],
            expected_output=task_cfg["expected_output"],
            agent=agents[task_cfg["agent"]],
            context=context_tasks if context_tasks else None
        )
        tasks.append(task)
        task_map[task_cfg["name"]] = task

    # Create crew
    process = Process.sequential if config.get("process") == "sequential" else Process.hierarchical
    return Crew(
        agents=list(agents.values()),
        tasks=tasks,
        process=process,
        verbose=config.get("verbose", True)
    )
```

## Template 4: AutoGen Group Chat Setup

```python
from autogen import ConversableAgent, GroupChat, GroupChatManager
from typing import List, Dict, Optional
import os

class AutoGenTeamBuilder:
    """Builder for AutoGen group chat teams."""

    def __init__(self, config_list: List[Dict] = None):
        self.config_list = config_list or [
            {"model": "gpt-4o", "api_key": os.environ.get("OPENAI_API_KEY")}
        ]
        self.agents: Dict[str, ConversableAgent] = {}

    def add_agent(
        self,
        name: str,
        system_message: str,
        human_input_mode: str = "NEVER",
        code_execution_config: Optional[Dict] = None
    ) -> "AutoGenTeamBuilder":
        """Add an agent to the team."""
        self.agents[name] = ConversableAgent(
            name=name,
            system_message=system_message,
            llm_config={"config_list": self.config_list},
            human_input_mode=human_input_mode,
            code_execution_config=code_execution_config
        )
        return self

    def add_user_proxy(
        self,
        name: str = "User",
        human_input_mode: str = "TERMINATE",
        code_execution_config: Optional[Dict] = None
    ) -> "AutoGenTeamBuilder":
        """Add a user proxy agent."""
        from autogen import UserProxyAgent
        self.agents[name] = UserProxyAgent(
            name=name,
            human_input_mode=human_input_mode,
            code_execution_config=code_execution_config or {"use_docker": False}
        )
        return self

    def build_group_chat(
        self,
        max_round: int = 10,
        speaker_selection_method: str = "auto"
    ) -> tuple[GroupChat, GroupChatManager]:
        """Build the group chat and manager."""
        group_chat = GroupChat(
            agents=list(self.agents.values()),
            messages=[],
            max_round=max_round,
            speaker_selection_method=speaker_selection_method
        )

        manager = GroupChatManager(
            groupchat=group_chat,
            llm_config={"config_list": self.config_list}
        )

        return group_chat, manager

# Usage
team = (
    AutoGenTeamBuilder()
    .add_agent(
        "Architect",
        "You are a software architect. Focus on system design and patterns."
    )
    .add_agent(
        "Developer",
        "You are a senior developer. Write clean, tested code."
    )
    .add_agent(
        "Reviewer",
        "You are a code reviewer. Check for bugs and best practices."
    )
    .add_agent(
        "PM",
        "You coordinate the team. Say 'TASK_COMPLETE' when done."
    )
    .add_user_proxy("User", human_input_mode="TERMINATE")
)

group_chat, manager = team.build_group_chat(max_round=15)
```

## Template 5: Message Bus and Communication

```python
from dataclasses import dataclass, field
from typing import Dict, List, Callable, Any, Optional
from enum import Enum
import asyncio
from datetime import datetime
import uuid

class MessageType(Enum):
    DIRECT = "direct"
    BROADCAST = "broadcast"
    REQUEST = "request"
    RESPONSE = "response"
    EVENT = "event"

class MessagePriority(Enum):
    LOW = 0
    NORMAL = 1
    HIGH = 2
    URGENT = 3

@dataclass
class Message:
    """Message structure for agent communication."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    sender: str = ""
    receiver: str = ""
    content: Any = None
    msg_type: MessageType = MessageType.DIRECT
    priority: MessagePriority = MessagePriority.NORMAL
    correlation_id: str = ""
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict = field(default_factory=dict)
    ttl: Optional[int] = None  # Time to live in seconds

@dataclass
class Subscription:
    """Subscription for message routing."""
    agent_name: str
    handler: Callable
    filter_fn: Optional[Callable[[Message], bool]] = None
    priority: int = 0

class MessageBus:
    """Production-ready message bus for agent communication."""

    def __init__(self, max_history: int = 1000):
        self.subscriptions: Dict[str, List[Subscription]] = {}
        self.message_history: List[Message] = []
        self.max_history = max_history
        self._lock = asyncio.Lock()
        self._pending_responses: Dict[str, asyncio.Future] = {}

    def subscribe(
        self,
        agent_name: str,
        handler: Callable,
        filter_fn: Optional[Callable[[Message], bool]] = None,
        priority: int = 0
    ):
        """Subscribe agent to messages."""
        if agent_name not in self.subscriptions:
            self.subscriptions[agent_name] = []

        sub = Subscription(agent_name, handler, filter_fn, priority)
        self.subscriptions[agent_name].append(sub)
        # Sort by priority
        self.subscriptions[agent_name].sort(key=lambda s: s.priority, reverse=True)

    def unsubscribe(self, agent_name: str):
        """Unsubscribe agent from all messages."""
        if agent_name in self.subscriptions:
            del self.subscriptions[agent_name]

    async def publish(self, message: Message) -> Optional[Any]:
        """Publish message to subscribers."""
        async with self._lock:
            self.message_history.append(message)
            if len(self.message_history) > self.max_history:
                self.message_history = self.message_history[-self.max_history:]

        if message.msg_type == MessageType.BROADCAST:
            await self._broadcast(message)
        elif message.msg_type == MessageType.REQUEST:
            return await self._request_response(message)
        else:
            await self._send_direct(message)

    async def _broadcast(self, message: Message):
        """Send to all subscribers except sender."""
        tasks = []
        for name, subs in self.subscriptions.items():
            if name != message.sender:
                for sub in subs:
                    if sub.filter_fn is None or sub.filter_fn(message):
                        tasks.append(sub.handler(message))
        await asyncio.gather(*tasks, return_exceptions=True)

    async def _send_direct(self, message: Message):
        """Send to specific receiver."""
        if message.receiver in self.subscriptions:
            for sub in self.subscriptions[message.receiver]:
                if sub.filter_fn is None or sub.filter_fn(message):
                    await sub.handler(message)

    async def _request_response(self, message: Message, timeout: float = 30.0) -> Any:
        """Send request and wait for response."""
        future = asyncio.get_event_loop().create_future()
        self._pending_responses[message.id] = future

        await self._send_direct(message)

        try:
            return await asyncio.wait_for(future, timeout=timeout)
        except asyncio.TimeoutError:
            del self._pending_responses[message.id]
            raise
        finally:
            if message.id in self._pending_responses:
                del self._pending_responses[message.id]

    async def respond(self, original_message: Message, response_content: Any):
        """Send response to a request."""
        if original_message.id in self._pending_responses:
            self._pending_responses[original_message.id].set_result(response_content)

        response = Message(
            sender=original_message.receiver,
            receiver=original_message.sender,
            content=response_content,
            msg_type=MessageType.RESPONSE,
            correlation_id=original_message.id
        )
        await self.publish(response)

    def get_history(
        self,
        agent_name: Optional[str] = None,
        msg_type: Optional[MessageType] = None,
        limit: int = 100
    ) -> List[Message]:
        """Get message history with optional filters."""
        history = self.message_history

        if agent_name:
            history = [m for m in history if m.sender == agent_name or m.receiver == agent_name]

        if msg_type:
            history = [m for m in history if m.msg_type == msg_type]

        return history[-limit:]
```

## Template 6: Shared Memory Store

```python
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from datetime import datetime
import json
from abc import ABC, abstractmethod

@dataclass
class MemoryEntry:
    """Single memory entry."""
    key: str
    value: Any
    agent: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    tags: List[str] = field(default_factory=list)
    expires_at: Optional[datetime] = None

class MemoryStore(ABC):
    """Abstract memory store interface."""

    @abstractmethod
    async def set(self, key: str, value: Any, agent: str, tags: List[str] = None, ttl: int = None):
        pass

    @abstractmethod
    async def get(self, key: str) -> Optional[MemoryEntry]:
        pass

    @abstractmethod
    async def search(self, tags: List[str] = None, agent: str = None) -> List[MemoryEntry]:
        pass

    @abstractmethod
    async def delete(self, key: str):
        pass

class InMemoryStore(MemoryStore):
    """In-memory implementation for development."""

    def __init__(self):
        self._store: Dict[str, MemoryEntry] = {}

    async def set(self, key: str, value: Any, agent: str, tags: List[str] = None, ttl: int = None):
        expires_at = None
        if ttl:
            from datetime import timedelta
            expires_at = datetime.utcnow() + timedelta(seconds=ttl)

        self._store[key] = MemoryEntry(
            key=key,
            value=value,
            agent=agent,
            tags=tags or [],
            expires_at=expires_at
        )

    async def get(self, key: str) -> Optional[MemoryEntry]:
        entry = self._store.get(key)
        if entry and entry.expires_at and entry.expires_at < datetime.utcnow():
            del self._store[key]
            return None
        return entry

    async def search(self, tags: List[str] = None, agent: str = None) -> List[MemoryEntry]:
        results = []
        for entry in self._store.values():
            # Check expiry
            if entry.expires_at and entry.expires_at < datetime.utcnow():
                continue

            # Filter by tags
            if tags and not any(t in entry.tags for t in tags):
                continue

            # Filter by agent
            if agent and entry.agent != agent:
                continue

            results.append(entry)

        return results

    async def delete(self, key: str):
        if key in self._store:
            del self._store[key]

class SharedAgentMemory:
    """High-level shared memory for agents."""

    def __init__(self, store: MemoryStore = None):
        self.store = store or InMemoryStore()

    async def remember(self, agent: str, key: str, value: Any, tags: List[str] = None):
        """Store a memory."""
        await self.store.set(key, value, agent, tags)

    async def recall(self, key: str) -> Optional[Any]:
        """Retrieve a memory."""
        entry = await self.store.get(key)
        return entry.value if entry else None

    async def share_artifact(self, agent: str, name: str, content: Any):
        """Share an artifact with all agents."""
        await self.store.set(f"artifact:{name}", content, agent, tags=["artifact"])

    async def get_artifact(self, name: str) -> Optional[Any]:
        """Get a shared artifact."""
        return await self.recall(f"artifact:{name}")

    async def add_note(self, agent: str, content: str, tags: List[str] = None):
        """Add a note to shared memory."""
        key = f"note:{agent}:{datetime.utcnow().isoformat()}"
        await self.store.set(key, content, agent, tags=["note"] + (tags or []))

    async def get_notes(self, agent: str = None, limit: int = 10) -> List[Dict]:
        """Get recent notes."""
        entries = await self.store.search(tags=["note"], agent=agent)
        entries.sort(key=lambda e: e.timestamp, reverse=True)
        return [{"agent": e.agent, "content": e.value, "time": e.timestamp} for e in entries[:limit]]

    async def record_decision(self, agent: str, decision: str, rationale: str):
        """Record a decision."""
        key = f"decision:{datetime.utcnow().isoformat()}"
        await self.store.set(key, {"decision": decision, "rationale": rationale}, agent, tags=["decision"])

    async def get_context_summary(self) -> str:
        """Get summary of shared context."""
        notes = await self.get_notes(limit=5)
        decisions = await self.store.search(tags=["decision"])
        artifacts = await self.store.search(tags=["artifact"])

        return f"""
Recent Notes ({len(notes)}):
{json.dumps(notes, default=str, indent=2)}

Decisions ({len(decisions)}):
{json.dumps([{"agent": d.agent, "value": d.value} for d in decisions[-3:]], indent=2)}

Artifacts: {[a.key.replace("artifact:", "") for a in artifacts]}
"""
```

## Template 7: Production Orchestrator

```python
from dataclasses import dataclass
from typing import Dict, List, Any, Optional, Callable
from enum import Enum
import asyncio
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ExecutionStrategy(Enum):
    HIERARCHICAL = "hierarchical"
    PARALLEL = "parallel"
    SEQUENTIAL = "sequential"
    COLLABORATIVE = "collaborative"

@dataclass
class ExecutionConfig:
    """Configuration for workflow execution."""
    strategy: ExecutionStrategy = ExecutionStrategy.HIERARCHICAL
    max_retries: int = 3
    timeout: float = 300.0
    parallel_limit: int = 5
    enable_checkpoints: bool = True

@dataclass
class ExecutionResult:
    """Result of workflow execution."""
    success: bool
    task: str
    strategy: ExecutionStrategy
    results: List[Dict]
    final_output: Any
    errors: List[str]
    duration: float
    token_usage: int
    metadata: Dict

class ProductionOrchestrator:
    """Production-ready orchestrator for multi-agent workflows."""

    def __init__(
        self,
        agents: Dict[str, Any],  # Agent instances
        llm_client: Any,
        memory: "SharedAgentMemory" = None,
        config: ExecutionConfig = None
    ):
        self.agents = agents
        self.llm = llm_client
        self.memory = memory or SharedAgentMemory()
        self.config = config or ExecutionConfig()
        self._semaphore = asyncio.Semaphore(self.config.parallel_limit)

    async def execute(
        self,
        task: str,
        strategy: ExecutionStrategy = None,
        context: Dict = None
    ) -> ExecutionResult:
        """Execute task with specified strategy."""
        strategy = strategy or self.config.strategy
        start_time = datetime.utcnow()
        errors = []
        results = []
        final_output = None

        try:
            if strategy == ExecutionStrategy.HIERARCHICAL:
                results, final_output = await self._execute_hierarchical(task, context)
            elif strategy == ExecutionStrategy.PARALLEL:
                results, final_output = await self._execute_parallel(task, context)
            elif strategy == ExecutionStrategy.SEQUENTIAL:
                results, final_output = await self._execute_sequential(task, context)
            elif strategy == ExecutionStrategy.COLLABORATIVE:
                results, final_output = await self._execute_collaborative(task, context)

            success = True
        except Exception as e:
            logger.exception(f"Execution failed: {e}")
            errors.append(str(e))
            success = False

        duration = (datetime.utcnow() - start_time).total_seconds()

        return ExecutionResult(
            success=success,
            task=task,
            strategy=strategy,
            results=results,
            final_output=final_output,
            errors=errors,
            duration=duration,
            token_usage=0,  # Track from LLM client
            metadata={"context": context}
        )

    async def _execute_hierarchical(self, task: str, context: Dict = None) -> tuple:
        """Hierarchical execution with manager."""
        # Create plan
        plan = await self._create_plan(task)

        # Execute assignments
        results = []
        for assignment in plan.get("assignments", []):
            async with self._semaphore:
                result = await self._execute_assignment(assignment)
                results.append(result)
                await self.memory.add_note(
                    assignment["agent"],
                    f"Completed: {assignment['task'][:100]}"
                )

        # Synthesize
        final = await self._synthesize(task, results)
        return results, final

    async def _execute_parallel(self, task: str, context: Dict = None) -> tuple:
        """Parallel execution of all agents."""
        async def run_agent(name, agent):
            async with self._semaphore:
                result = await agent.respond(task)
                return {"agent": name, "result": result}

        tasks = [run_agent(n, a) for n, a in self.agents.items()]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        results = [r for r in results if not isinstance(r, Exception)]

        final = await self._synthesize(task, results)
        return results, final

    async def _execute_sequential(self, task: str, context: Dict = None) -> tuple:
        """Sequential pipeline execution."""
        current = task
        results = []

        for name, agent in self.agents.items():
            result = await agent.respond(current)
            results.append({"agent": name, "input": current[:100], "result": result})
            current = result

        return results, current

    async def _execute_collaborative(self, task: str, context: Dict = None) -> tuple:
        """Collaborative refinement execution."""
        contributions = {}

        # Initial round
        for name, agent in self.agents.items():
            contributions[name] = await agent.respond(f"Task: {task}\n\nProvide your approach.")

        # Refinement rounds
        for round_num in range(3):
            for name, agent in self.agents.items():
                others = {k: v for k, v in contributions.items() if k != name}
                prompt = f"""Task: {task}

Your current approach: {contributions[name]}

Others' approaches:
{others}

Refine, incorporating good ideas from others."""

                contributions[name] = await agent.respond(prompt)

        # Synthesize
        final = await self._synthesize(task, [{"agent": k, "result": v} for k, v in contributions.items()])
        return [{"agent": k, "result": v} for k, v in contributions.items()], final

    async def _create_plan(self, task: str) -> Dict:
        """Create execution plan."""
        # Implementation depends on LLM client
        pass

    async def _execute_assignment(self, assignment: Dict) -> Dict:
        """Execute single assignment with retries."""
        agent_name = assignment["agent"]
        subtask = assignment["task"]

        for attempt in range(self.config.max_retries):
            try:
                if agent_name in self.agents:
                    result = await asyncio.wait_for(
                        self.agents[agent_name].respond(subtask),
                        timeout=self.config.timeout / self.config.max_retries
                    )
                    return {"agent": agent_name, "task": subtask, "result": result}
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed for {agent_name}: {e}")

        return {"agent": agent_name, "task": subtask, "result": None, "error": "Max retries exceeded"}

    async def _synthesize(self, task: str, results: List[Dict]) -> str:
        """Synthesize results into final output."""
        # Implementation depends on LLM client
        pass
```
