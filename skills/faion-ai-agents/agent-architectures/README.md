---
id: agent-architectures
name: "Agent Architectures"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
parent: autonomous-agents
---

# Agent Architectures

Production-ready architectures for autonomous agents with memory, tools, and planning capabilities.

## Core Components

### Memory System

```python
from datetime import datetime
from typing import List, Dict, Optional, Callable
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
        self.long_term: List[Dict] = []

    def add(self, content: str, metadata: Dict = None):
        """Add memory entry."""
        entry = {
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {},
            "embedding": self.embedding_func(content)
        }
        self.short_term.append(entry)

        if len(self.short_term) > self.max_short_term:
            old_entry = self.short_term.pop(0)
            self.long_term.append(old_entry)

    def recall(self, query: str, k: int = 5) -> List[Dict]:
        """Recall relevant memories."""
        query_embedding = self.embedding_func(query)
        all_memories = self.short_term + self.long_term

        if not all_memories:
            return []

        similarities = []
        for memory in all_memories:
            sim = np.dot(query_embedding, memory["embedding"]) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(memory["embedding"])
            )
            similarities.append((memory, sim))

        relevant = [(m, s) for m, s in similarities if s >= self.relevance_threshold]
        relevant.sort(key=lambda x: x[1], reverse=True)

        return [m for m, _ in relevant[:k]]

    def summarize_recent(self) -> str:
        """Summarize recent memories."""
        if not self.short_term:
            return "No recent memories."
        recent = self.short_term[-5:]
        return "\n".join([m["content"] for m in recent])
```

### Tool System

```python
from typing import Callable, Any
import json

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
```

### Agent with Memory

```python
from openai import OpenAI

client = OpenAI()

class AgentWithMemory:
    """Agent with memory capabilities."""

    def __init__(
        self,
        tools: List[Tool],
        embedding_func: Callable,
        model: str = "gpt-4o"
    ):
        self.tools = {t.name: t for t in tools}
        self.model = model
        self.memory = Memory(embedding_func)

    def run(self, task: str) -> str:
        """Run agent with memory context."""
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

        self.memory.add(
            f"Task: {task}\nResult: {result}",
            metadata={"type": "task_completion"}
        )

        return result
```

### Production Agent Framework

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
        config: Optional[AgentConfig] = None,
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
            return {"success": True, "result": result, "log": self.execution_log}

        except asyncio.TimeoutError:
            self.state = AgentState.FAILED
            return {"success": False, "error": "Timeout", "log": self.execution_log}

        except Exception as e:
            self.state = AgentState.FAILED
            self.logger.error(f"Agent error: {e}")
            return {"success": False, "error": str(e), "log": self.execution_log}

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

            self.execution_log.append({
                "iteration": iteration + 1,
                "content": message.content,
                "tool_calls": [tc.function.name for tc in (message.tool_calls or [])]
            })

            if not message.tool_calls:
                if self.config.enable_reflection:
                    self.state = AgentState.REFLECTING
                    is_complete = await self._reflect_on_completion(goal, message.content)
                    if is_complete:
                        return message.content
                    self.state = AgentState.EXECUTING
                else:
                    return message.content

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

        system_prompt = f"""You are an autonomous AI agent working to achieve goals.

{memory_context}

Guidelines:
1. Think step by step before acting
2. Use tools when needed
3. Verify your progress
4. Ask for clarification only when truly stuck

Available tools will be provided. Use them wisely."""

        return {"system_prompt": system_prompt}

    async def _call_llm(self):
        """Call the LLM."""
        return client.chat.completions.create(
            model=self.config.model,
            messages=self.messages,
            tools=[t.to_openai_format() for t in self.tools.values()],
            tool_choice="auto"
        )

    async def _process_tool_calls(self, tool_calls):
        """Process tool calls."""
        for tool_call in tool_calls[:self.config.max_tool_calls_per_iteration]:
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

    async def _reflect_on_completion(self, goal: str, result: str) -> bool:
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
```

## Best Practices

### Agent Design

- **Clear Goal Definition**: Specific, measurable objectives with success criteria
- **Bounded Scope**: Limit task complexity and iteration count
- **Tool Design**: Clear descriptions, proper error handling, appropriate granularity

### Safety

- **Iteration Limits**: Prevent infinite loops
- **Sandbox Execution**: Isolate code execution
- **Human Approval**: Critical actions require confirmation
- **Rate Limiting**: Control API costs and usage

### Monitoring

- **Action Logging**: Track all agent decisions and tool calls
- **Token Usage**: Monitor costs and optimize prompts
- **Failure Alerts**: Detect and respond to errors quickly
- **Performance Metrics**: Measure success rates and latency

### Memory Management

- **Summarization**: Compress long conversation histories
- **Relevance Filtering**: Only retrieve pertinent memories
- **Cleanup**: Clear stale or outdated memories
- **Embedding Quality**: Use good embedding models for retrieval

## Common Pitfalls

| Issue | Problem | Solution |
|-------|---------|----------|
| Infinite Loops | No iteration limits | Set `max_iterations` |
| Tool Abuse | Calling same tool repeatedly | Track and limit calls |
| Context Overflow | Too much history | Summarize or filter |
| Hallucinated Actions | Acting on made-up info | Verify tool outputs |
| No Guardrails | Unsafe tool execution | Sandbox and approve |
| Poor Error Recovery | Failing on first error | Implement retry logic |

## Sources

- [ReAct Paper](https://arxiv.org/abs/2210.03629) - Reasoning and Acting
- [Reflexion Paper](https://arxiv.org/abs/2303.11366) - Self-Reflection in Agents
- [AutoGPT](https://github.com/Significant-Gravitas/AutoGPT) - Autonomous GPT-4
- [LangChain Agents](https://python.langchain.com/docs/modules/agents/) - Agent Framework
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling) - Tool Use API
