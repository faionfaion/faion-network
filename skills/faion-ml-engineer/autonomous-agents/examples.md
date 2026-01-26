# Autonomous Agents - Code Examples

## Table of Contents

1. [Basic Tool Definition](#basic-tool-definition)
2. [ReAct Agent](#react-agent)
3. [Plan-and-Execute Agent](#plan-and-execute-agent)
4. [Reflexion Agent](#reflexion-agent)
5. [Memory System](#memory-system)
6. [Production Agent](#production-agent)
7. [Multi-Agent System](#multi-agent-system)
8. [LangGraph Example](#langgraph-example)

---

## Basic Tool Definition

```python
from openai import OpenAI
from typing import Callable, Any
import json

client = OpenAI()


class Tool:
    """Represents an agent tool."""

    def __init__(
        self,
        name: str,
        description: str,
        function: Callable,
        parameters: dict
    ):
        self.name = name
        self.description = description
        self.function = function
        self.parameters = parameters

    def to_openai_format(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters
            }
        }

    def execute(self, **kwargs) -> str:
        try:
            result = self.function(**kwargs)
            return json.dumps(result) if not isinstance(result, str) else result
        except Exception as e:
            return f"Error: {str(e)}"


# Example tools
def search_web(query: str) -> dict:
    """Simulate web search."""
    return {"results": [f"Result for: {query}"]}


def calculate(expression: str) -> dict:
    """Evaluate math expression."""
    try:
        result = eval(expression)  # Use safer eval in production
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}


search_tool = Tool(
    name="search_web",
    description="Search the web for information",
    function=search_web,
    parameters={
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Search query"}
        },
        "required": ["query"]
    }
)

calc_tool = Tool(
    name="calculate",
    description="Evaluate a mathematical expression",
    function=calculate,
    parameters={
        "type": "object",
        "properties": {
            "expression": {"type": "string", "description": "Math expression"}
        },
        "required": ["expression"]
    }
)
```

---

## ReAct Agent

```python
from typing import List, Dict


class ReActAgent:
    """ReAct (Reason + Act) agent implementation."""

    def __init__(
        self,
        tools: List[Tool],
        model: str = "gpt-4o",
        max_iterations: int = 10,
        system_prompt: str = None
    ):
        self.tools = {t.name: t for t in tools}
        self.model = model
        self.max_iterations = max_iterations
        self.system_prompt = system_prompt or self._default_system_prompt()
        self.messages = []

    def _default_system_prompt(self) -> str:
        return """You are a helpful AI assistant with access to tools.

When you need to accomplish a task:
1. Think about what you need to do (Thought)
2. Use available tools when needed (Action)
3. Analyze tool results (Observation)
4. Continue until the task is complete

Always explain your reasoning before taking actions."""

    def run(self, task: str) -> str:
        """Run the agent on a task."""
        self.messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": task}
        ]

        for iteration in range(self.max_iterations):
            response = client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                tools=[t.to_openai_format() for t in self.tools.values()],
                tool_choice="auto"
            )

            message = response.choices[0].message

            # No tool calls - task complete
            if not message.tool_calls:
                return message.content

            # Process tool calls
            self.messages.append(message)

            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)

                print(f"[Tool] {tool_name}: {arguments}")

                if tool_name in self.tools:
                    result = self.tools[tool_name].execute(**arguments)
                else:
                    result = f"Unknown tool: {tool_name}"

                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

        return "Max iterations reached without completion."


# Usage
agent = ReActAgent(tools=[search_tool, calc_tool])
result = agent.run("What is 25 * 4 + 10?")
print(result)
```

---

## Plan-and-Execute Agent

```python
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Task:
    description: str
    status: str = "pending"  # pending, in_progress, completed, failed
    result: Optional[str] = None
    dependencies: List[int] = field(default_factory=list)


class PlanAndExecuteAgent:
    """Agent that creates a plan before executing."""

    def __init__(
        self,
        tools: List[Tool],
        model: str = "gpt-4o",
        planner_model: str = "gpt-4o"
    ):
        self.tools = {t.name: t for t in tools}
        self.model = model
        self.planner_model = planner_model
        self.plan: List[Task] = []

    def create_plan(self, goal: str) -> List[Task]:
        """Create a plan to achieve the goal."""
        tools_description = "\n".join([
            f"- {t.name}: {t.description}"
            for t in self.tools.values()
        ])

        prompt = f"""Create a step-by-step plan to achieve this goal.

Goal: {goal}

Available tools:
{tools_description}

Return a JSON object with a "tasks" array:
{{"tasks": [{{"description": "task description", "dependencies": [0, 1]}}]}}

Dependencies are indices of tasks that must complete first.
Keep the plan focused and minimal."""

        response = client.chat.completions.create(
            model=self.planner_model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        tasks_data = json.loads(response.choices[0].message.content)

        self.plan = [
            Task(
                description=t["description"],
                dependencies=t.get("dependencies", [])
            )
            for t in tasks_data.get("tasks", [])
        ]

        return self.plan

    def execute_task(self, task: Task) -> str:
        """Execute a single task."""
        task.status = "in_progress"

        # Get context from completed dependencies
        context = ""
        if task.dependencies:
            context = "Previous task results:\n"
            for dep_idx in task.dependencies:
                if dep_idx < len(self.plan):
                    dep = self.plan[dep_idx]
                    context += f"- {dep.description}: {dep.result}\n"

        prompt = f"""{context}

Current task: {task.description}

Complete this task using available tools. Explain your approach."""

        messages = [
            {"role": "system", "content": "You are executing a plan step by step."},
            {"role": "user", "content": prompt}
        ]

        # Execute with tools (max 5 iterations per task)
        for _ in range(5):
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=[t.to_openai_format() for t in self.tools.values()],
                tool_choice="auto"
            )

            message = response.choices[0].message

            if not message.tool_calls:
                task.result = message.content
                task.status = "completed"
                return message.content

            messages.append(message)

            for tool_call in message.tool_calls:
                result = self.tools[tool_call.function.name].execute(
                    **json.loads(tool_call.function.arguments)
                )
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

        task.status = "failed"
        return "Task execution timeout"

    def run(self, goal: str) -> str:
        """Run the full plan-and-execute loop."""
        self.create_plan(goal)
        print(f"Created plan with {len(self.plan)} tasks")

        results = []

        while any(t.status == "pending" for t in self.plan):
            for i, task in enumerate(self.plan):
                if task.status != "pending":
                    continue

                # Check if dependencies are complete
                deps_complete = all(
                    self.plan[d].status == "completed"
                    for d in task.dependencies
                    if d < len(self.plan)
                )

                if deps_complete:
                    print(f"Executing task {i + 1}: {task.description}")
                    result = self.execute_task(task)
                    results.append(f"Task {i + 1}: {result}")

        return "\n\n".join(results)


# Usage
agent = PlanAndExecuteAgent(tools=[search_tool, calc_tool])
result = agent.run("Research the population of France and calculate 10% of it")
print(result)
```

---

## Reflexion Agent

```python
class ReflexionAgent:
    """Agent that learns from mistakes through self-reflection."""

    def __init__(
        self,
        tools: List[Tool],
        model: str = "gpt-4o",
        max_attempts: int = 3
    ):
        self.tools = {t.name: t for t in tools}
        self.model = model
        self.max_attempts = max_attempts
        self.reflections: List[str] = []

    def attempt_task(
        self,
        task: str,
        previous_attempts: List[dict] = None
    ) -> dict:
        """Make one attempt at the task."""
        context = ""
        if previous_attempts:
            context = "Previous attempts and reflections:\n"
            for attempt in previous_attempts:
                context += f"\nAttempt: {attempt['action']}\n"
                context += f"Result: {attempt['result']}\n"
                context += f"Reflection: {attempt['reflection']}\n"

        messages = [
            {
                "role": "system",
                "content": f"""You are an AI agent that learns from mistakes.
{context}

Based on previous attempts (if any), improve your approach.
Explain your reasoning before taking action."""
            },
            {"role": "user", "content": task}
        ]

        action_log = []
        for _ in range(5):
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=[t.to_openai_format() for t in self.tools.values()]
            )

            message = response.choices[0].message

            if not message.tool_calls:
                return {
                    "action": "\n".join(action_log),
                    "result": message.content,
                    "success": True
                }

            messages.append(message)

            for tool_call in message.tool_calls:
                action = f"{tool_call.function.name}({tool_call.function.arguments})"
                action_log.append(action)

                result = self.tools[tool_call.function.name].execute(
                    **json.loads(tool_call.function.arguments)
                )

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

        return {
            "action": "\n".join(action_log),
            "result": "Max iterations reached",
            "success": False
        }

    def reflect(self, task: str, attempt: dict) -> str:
        """Reflect on an attempt to improve future attempts."""
        prompt = f"""Reflect on this attempt at the task.

Task: {task}

Actions taken:
{attempt['action']}

Result:
{attempt['result']}

Was this successful? What could be improved?
What should be done differently next time?

Provide a brief, actionable reflection."""

        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content

    def run(self, task: str, success_check: Callable = None) -> str:
        """Run with reflection and retry."""
        attempts = []

        for attempt_num in range(self.max_attempts):
            print(f"Attempt {attempt_num + 1}/{self.max_attempts}")

            attempt = self.attempt_task(task, attempts)

            # Check success
            if success_check:
                success = success_check(attempt["result"])
            else:
                success = attempt["success"]

            if success:
                return attempt["result"]

            # Reflect on failure
            reflection = self.reflect(task, attempt)
            attempt["reflection"] = reflection
            attempts.append(attempt)
            self.reflections.append(reflection)

            print(f"Reflection: {reflection}")

        return f"Failed after {self.max_attempts} attempts."
```

---

## Memory System

```python
from datetime import datetime
import numpy as np


class Memory:
    """Agent memory with short-term and long-term storage."""

    def __init__(
        self,
        embedding_func: Callable,
        max_short_term: int = 10,
        relevance_threshold: float = 0.7
    ):
        self.embedding_func = embedding_func
        self.max_short_term = max_short_term
        self.relevance_threshold = relevance_threshold

        self.short_term: List[Dict] = []
        self.long_term: List[Dict] = []  # Use vector DB in production

    def add(self, content: str, metadata: Dict = None):
        """Add memory entry."""
        entry = {
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {},
            "embedding": self.embedding_func(content)
        }

        self.short_term.append(entry)

        # Move old memories to long-term
        if len(self.short_term) > self.max_short_term:
            old_entry = self.short_term.pop(0)
            self.long_term.append(old_entry)

    def recall(self, query: str, k: int = 5) -> List[Dict]:
        """Recall relevant memories."""
        query_embedding = self.embedding_func(query)
        all_memories = self.short_term + self.long_term

        if not all_memories:
            return []

        # Calculate similarities
        similarities = []
        for memory in all_memories:
            sim = np.dot(query_embedding, memory["embedding"]) / (
                np.linalg.norm(query_embedding) *
                np.linalg.norm(memory["embedding"])
            )
            similarities.append((memory, sim))

        # Filter and sort
        relevant = [
            (m, s) for m, s in similarities
            if s >= self.relevance_threshold
        ]
        relevant.sort(key=lambda x: x[1], reverse=True)

        return [m for m, _ in relevant[:k]]

    def summarize_recent(self) -> str:
        """Summarize recent memories."""
        if not self.short_term:
            return "No recent memories."

        recent = self.short_term[-5:]
        return "\n".join([m["content"] for m in recent])


# Embedding function using OpenAI
def get_embedding(text: str) -> List[float]:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


class AgentWithMemory:
    """Agent with memory capabilities."""

    def __init__(
        self,
        tools: List[Tool],
        model: str = "gpt-4o"
    ):
        self.tools = {t.name: t for t in tools}
        self.model = model
        self.memory = Memory(get_embedding)

    def run(self, task: str) -> str:
        """Run agent with memory context."""
        # Recall relevant memories
        relevant_memories = self.memory.recall(task, k=3)
        memory_context = ""
        if relevant_memories:
            memory_context = "\nRelevant past experiences:\n"
            for mem in relevant_memories:
                memory_context += f"- {mem['content']}\n"

        system_prompt = f"""You are an AI assistant with memory.
{memory_context}

Use your past experiences to inform your decisions."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": task}
        ]

        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=[t.to_openai_format() for t in self.tools.values()]
        )

        result = response.choices[0].message.content or "Task completed"

        # Store experience
        self.memory.add(
            f"Task: {task}\nResult: {result}",
            metadata={"type": "task_completion"}
        )

        return result
```

---

## Production Agent

```python
from dataclasses import dataclass
from enum import Enum
import logging
import asyncio


class AgentState(Enum):
    IDLE = "idle"
    PLANNING = "planning"
    EXECUTING = "executing"
    REFLECTING = "reflecting"
    COMPLETE = "complete"
    FAILED = "failed"


@dataclass
class AgentConfig:
    model: str = "gpt-4o"
    max_iterations: int = 20
    max_tool_calls_per_iteration: int = 5
    timeout_seconds: int = 300
    enable_reflection: bool = True
    enable_memory: bool = True


class ProductionAgent:
    """Production-ready autonomous agent."""

    def __init__(
        self,
        tools: List[Tool],
        config: AgentConfig = None,
        embedding_func: Callable = None
    ):
        self.tools = {t.name: t for t in tools}
        self.config = config or AgentConfig()
        self.logger = logging.getLogger(__name__)

        self.state = AgentState.IDLE
        self.messages: List[Dict] = []
        self.execution_log: List[Dict] = []

        if self.config.enable_memory and embedding_func:
            self.memory = Memory(embedding_func)
        else:
            self.memory = None

    async def run(self, goal: str) -> Dict[str, Any]:
        """Run the agent asynchronously."""
        self.state = AgentState.PLANNING
        self.messages = []
        self.execution_log = []

        try:
            result = await asyncio.wait_for(
                self._execute_goal(goal),
                timeout=self.config.timeout_seconds
            )
            self.state = AgentState.COMPLETE
            return {
                "success": True,
                "result": result,
                "log": self.execution_log
            }

        except asyncio.TimeoutError:
            self.state = AgentState.FAILED
            return {
                "success": False,
                "error": "Timeout",
                "log": self.execution_log
            }

        except Exception as e:
            self.state = AgentState.FAILED
            self.logger.error(f"Agent error: {e}")
            return {
                "success": False,
                "error": str(e),
                "log": self.execution_log
            }

    async def _execute_goal(self, goal: str) -> str:
        """Execute the goal."""
        context = self._build_context(goal)

        self.messages = [
            {"role": "system", "content": context["system_prompt"]},
            {"role": "user", "content": goal}
        ]

        self.state = AgentState.EXECUTING

        for iteration in range(self.config.max_iterations):
            self.logger.info(f"Iteration {iteration + 1}")

            response = await self._call_llm()
            message = response.choices[0].message

            # Log iteration
            self.execution_log.append({
                "iteration": iteration + 1,
                "content": message.content,
                "tool_calls": [
                    tc.function.name
                    for tc in (message.tool_calls or [])
                ]
            })

            # No tool calls - check if complete
            if not message.tool_calls:
                if self.config.enable_reflection:
                    self.state = AgentState.REFLECTING
                    is_complete = await self._reflect_on_completion(
                        goal, message.content
                    )
                    if is_complete:
                        return message.content
                    self.state = AgentState.EXECUTING
                else:
                    return message.content

            # Process tool calls
            self.messages.append(message)
            await self._process_tool_calls(message.tool_calls)

        return "Max iterations reached"

    def _build_context(self, goal: str) -> Dict:
        """Build context for the agent."""
        memory_context = ""
        if self.memory:
            relevant = self.memory.recall(goal, k=3)
            if relevant:
                memory_context = "\nRelevant past experiences:\n" + \
                    "\n".join([f"- {m['content'][:200]}" for m in relevant])

        system_prompt = f"""You are an autonomous AI agent.
{memory_context}

Guidelines:
1. Think step by step before acting
2. Use tools when needed
3. Verify your progress
4. Ask for clarification only when truly stuck"""

        return {"system_prompt": system_prompt}

    async def _call_llm(self):
        """Call the LLM (sync wrapper for now)."""
        return client.chat.completions.create(
            model=self.config.model,
            messages=self.messages,
            tools=[t.to_openai_format() for t in self.tools.values()],
            tool_choice="auto"
        )

    async def _process_tool_calls(self, tool_calls):
        """Process tool calls."""
        max_calls = self.config.max_tool_calls_per_iteration
        for tool_call in tool_calls[:max_calls]:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            self.logger.info(f"Tool call: {tool_name}")

            if tool_name in self.tools:
                result = self.tools[tool_name].execute(**arguments)
            else:
                result = f"Unknown tool: {tool_name}"

            self.messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })

    async def _reflect_on_completion(
        self, goal: str, result: str
    ) -> bool:
        """Reflect on whether the goal is achieved."""
        prompt = f"""Goal: {goal}

Current result: {result}

Has the goal been fully achieved? Respond with JSON:
{{"complete": true/false, "reason": "..."}}"""

        response = client.chat.completions.create(
            model=self.config.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        reflection = json.loads(response.choices[0].message.content)
        return reflection.get("complete", False)


# Usage
async def main():
    config = AgentConfig(
        model="gpt-4o",
        max_iterations=15,
        timeout_seconds=120,
        enable_reflection=True
    )

    agent = ProductionAgent(
        tools=[search_tool, calc_tool],
        config=config,
        embedding_func=get_embedding
    )

    result = await agent.run("Calculate the square root of 144")
    print(result)


# asyncio.run(main())
```

---

## Multi-Agent System

```python
from enum import Enum


class AgentRole(Enum):
    RESEARCHER = "researcher"
    CODER = "coder"
    REVIEWER = "reviewer"
    ORCHESTRATOR = "orchestrator"


class SpecialistAgent:
    """Specialist agent with specific role."""

    def __init__(
        self,
        role: AgentRole,
        tools: List[Tool],
        model: str = "gpt-4o"
    ):
        self.role = role
        self.tools = {t.name: t for t in tools}
        self.model = model
        self.system_prompt = self._get_role_prompt()

    def _get_role_prompt(self) -> str:
        prompts = {
            AgentRole.RESEARCHER: """You are a research specialist.
Your job is to gather and analyze information.
Be thorough and cite sources when possible.""",

            AgentRole.CODER: """You are a coding specialist.
Your job is to write clean, efficient code.
Follow best practices and add comments.""",

            AgentRole.REVIEWER: """You are a code review specialist.
Your job is to analyze code for bugs and improvements.
Be constructive and specific in feedback.""",

            AgentRole.ORCHESTRATOR: """You are the team orchestrator.
Your job is to coordinate tasks between specialists.
Break down complex tasks and assign appropriately."""
        }
        return prompts.get(self.role, "You are a helpful assistant.")

    def execute(self, task: str, context: str = "") -> str:
        """Execute a task."""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"{context}\n\nTask: {task}"}
        ]

        for _ in range(5):
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=[t.to_openai_format() for t in self.tools.values()]
            )

            message = response.choices[0].message

            if not message.tool_calls:
                return message.content

            messages.append(message)

            for tool_call in message.tool_calls:
                result = self.tools[tool_call.function.name].execute(
                    **json.loads(tool_call.function.arguments)
                )
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

        return "Task incomplete"


class MultiAgentSystem:
    """Supervisor pattern multi-agent system."""

    def __init__(self, model: str = "gpt-4o"):
        self.model = model
        self.agents: Dict[AgentRole, SpecialistAgent] = {}
        self.conversation_history: List[Dict] = []

    def add_agent(self, role: AgentRole, tools: List[Tool]):
        """Add a specialist agent."""
        self.agents[role] = SpecialistAgent(role, tools, self.model)

    def route_task(self, task: str) -> AgentRole:
        """Route task to appropriate agent."""
        prompt = f"""Given this task, which specialist should handle it?

Task: {task}

Available specialists:
{', '.join([r.value for r in self.agents.keys()])}

Respond with just the specialist name."""

        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )

        role_str = response.choices[0].message.content.strip().lower()

        for role in AgentRole:
            if role.value in role_str:
                return role

        return AgentRole.ORCHESTRATOR

    def run(self, goal: str) -> str:
        """Run multi-agent system on a goal."""
        # Orchestrator creates plan
        orchestrator = self.agents.get(AgentRole.ORCHESTRATOR)
        if not orchestrator:
            raise ValueError("No orchestrator agent defined")

        plan_prompt = f"""Create a plan to achieve this goal.

Goal: {goal}

Available specialists: {', '.join([r.value for r in self.agents.keys()])}

Return a step-by-step plan with assigned specialists."""

        plan = orchestrator.execute(plan_prompt)
        print(f"Plan:\n{plan}")

        # Execute plan (simplified - in production parse plan properly)
        results = []

        # Route main task
        role = self.route_task(goal)
        agent = self.agents.get(role)

        if agent:
            result = agent.execute(goal, context=f"Plan:\n{plan}")
            results.append(f"[{role.value}]: {result}")

        # Have reviewer check if needed
        if AgentRole.REVIEWER in self.agents and role == AgentRole.CODER:
            reviewer = self.agents[AgentRole.REVIEWER]
            review = reviewer.execute(
                f"Review this output:\n{results[-1]}",
                context=f"Original goal: {goal}"
            )
            results.append(f"[reviewer]: {review}")

        return "\n\n".join(results)


# Usage
system = MultiAgentSystem()
system.add_agent(AgentRole.ORCHESTRATOR, [])
system.add_agent(AgentRole.RESEARCHER, [search_tool])
system.add_agent(AgentRole.CODER, [calc_tool])
system.add_agent(AgentRole.REVIEWER, [])

result = system.run("Research Python best practices and write a hello world")
print(result)
```

---

## LangGraph Example

```python
# pip install langgraph langchain-openai

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    task: str
    plan: list[str]
    current_step: int
    result: str


def create_langgraph_agent():
    """Create a LangGraph-based agent."""

    llm = ChatOpenAI(model="gpt-4o")

    def planner(state: AgentState) -> AgentState:
        """Create a plan for the task."""
        task = state["task"]

        response = llm.invoke([
            HumanMessage(content=f"""Create a 3-step plan for: {task}

Return each step on a new line, numbered 1-3.""")
        ])

        plan = [
            line.strip()
            for line in response.content.split("\n")
            if line.strip()
        ]

        return {
            **state,
            "plan": plan,
            "current_step": 0
        }

    def executor(state: AgentState) -> AgentState:
        """Execute current step."""
        step = state["plan"][state["current_step"]]

        response = llm.invoke([
            HumanMessage(content=f"Execute this step: {step}")
        ])

        state["messages"].append(AIMessage(content=response.content))

        return {
            **state,
            "current_step": state["current_step"] + 1
        }

    def should_continue(state: AgentState) -> str:
        """Check if more steps remain."""
        if state["current_step"] >= len(state["plan"]):
            return "summarize"
        return "execute"

    def summarizer(state: AgentState) -> AgentState:
        """Summarize results."""
        messages = "\n".join([m.content for m in state["messages"]])

        response = llm.invoke([
            HumanMessage(content=f"""Summarize these results:

{messages}

Original task: {state['task']}""")
        ])

        return {
            **state,
            "result": response.content
        }

    # Build graph
    graph = StateGraph(AgentState)

    graph.add_node("planner", planner)
    graph.add_node("executor", executor)
    graph.add_node("summarizer", summarizer)

    graph.set_entry_point("planner")
    graph.add_edge("planner", "executor")
    graph.add_conditional_edges(
        "executor",
        should_continue,
        {
            "execute": "executor",
            "summarize": "summarizer"
        }
    )
    graph.add_edge("summarizer", END)

    return graph.compile()


# Usage
# agent = create_langgraph_agent()
# result = agent.invoke({
#     "task": "Research and summarize AI agent architectures",
#     "messages": [],
#     "plan": [],
#     "current_step": 0,
#     "result": ""
# })
# print(result["result"])
```
