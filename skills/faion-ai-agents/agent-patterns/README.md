---
id: agent-patterns
name: "Agent Patterns"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
parent: autonomous-agents
---

# Agent Patterns

## Overview

Implementation patterns for different types of autonomous agents. Each pattern solves specific problems and has distinct characteristics.

## Pattern Comparison

| Pattern | Description | Use Case |
|---------|-------------|----------|
| ReAct | Reason + Act loop | General tasks |
| Plan-and-Execute | Plan first, then execute | Complex projects |
| Reflexion | Self-critique and improve | Learning tasks |
| AutoGPT-style | Full autonomy with goals | Research, automation |

## When to Use

- Complex multi-step tasks
- Tasks requiring tool orchestration
- Research and analysis workflows
- Code generation and execution
- When tasks require iteration and self-correction
- Automating knowledge work

## Pattern Implementations

### 1. ReAct Agent

Reason → Act loop for general task execution.

```python
from openai import OpenAI
from typing import List, Dict
import json

client = OpenAI()

class ReActAgent:
    """Simple ReAct agent implementation."""

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
1. Think about what you need to do
2. Use available tools when needed
3. Analyze tool results
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
```

### 2. Plan-and-Execute Agent

Create a plan first, then execute steps in order.

```python
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Task:
    description: str
    status: str = "pending"  # pending, in_progress, completed, failed
    result: Optional[str] = None
    dependencies: List[int] = None

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

Return a JSON array of tasks:
[{{"description": "task description", "dependencies": [0, 1]}}]

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
            for t in tasks_data.get("tasks", tasks_data)
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
                    context += f"- {self.plan[dep_idx].description}: {self.plan[dep_idx].result}\n"

        prompt = f"""{context}

Current task: {task.description}

Complete this task using available tools. Explain your approach."""

        messages = [
            {"role": "system", "content": "You are an AI assistant executing a plan."},
            {"role": "user", "content": prompt}
        ]

        # Execute with tools
        for _ in range(5):  # Max iterations per task
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
        # Create plan
        self.create_plan(goal)
        print(f"Created plan with {len(self.plan)} tasks")

        # Execute tasks in order (respecting dependencies)
        results = []

        while any(t.status == "pending" for t in self.plan):
            for i, task in enumerate(self.plan):
                if task.status != "pending":
                    continue

                # Check dependencies
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
```

### 3. Reflexion Agent

Self-reflect and improve through iteration.

```python
from typing import Callable

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

    def attempt_task(self, task: str, previous_attempts: List[dict] = None) -> dict:
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

        # Execute with tools
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

            # Make attempt
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

        return f"Failed after {self.max_attempts} attempts. Last result: {attempts[-1]['result']}"
```

## Usage Examples

### ReAct Agent

```python
# Define tools
def search_web(query: str) -> str:
    """Search the web for information."""
    # Implementation
    return f"Search results for: {query}"

def calculate(expression: str) -> str:
    """Calculate mathematical expression."""
    # Implementation
    return str(eval(expression))

# Create tools
tools = [
    Tool(
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
    ),
    Tool(
        name="calculate",
        description="Calculate mathematical expressions",
        function=calculate,
        parameters={
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "Math expression"}
            },
            "required": ["expression"]
        }
    )
]

# Run agent
agent = ReActAgent(tools)
result = agent.run("What is the population of Tokyo divided by 2?")
```

### Plan-and-Execute Agent

```python
agent = PlanAndExecuteAgent(tools)
result = agent.run("Research AI trends in 2026 and create a summary report")
```

### Reflexion Agent

```python
def success_check(result: str) -> bool:
    """Check if result is valid."""
    return "error" not in result.lower()

agent = ReflexionAgent(tools, max_attempts=3)
result = agent.run("Write a Python function to parse JSON", success_check=success_check)
```

## References

- [agent-architectures.md](agent-architectures.md) - Core architecture components
- [ReAct Paper](https://arxiv.org/abs/2210.03629)
- [Reflexion Paper](https://arxiv.org/abs/2303.11366)
- [LangChain Agents](https://python.langchain.com/docs/modules/agents/)
## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Generate tool definitions from API | haiku | Mechanical transformation |
| Review agent reasoning chains | sonnet | Requires logic analysis |
| Design multi-agent orchestration | opus | Complex coordination patterns |

