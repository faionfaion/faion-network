---
id: reasoning-first-architectures-templates
name: "Reasoning-First Architectures Templates"
parent: reasoning-first-architectures
---

# Reasoning-First Architectures Templates

## 1. OpenAI o3/o4 Configuration Templates

### Basic o3 Configuration

```python
# template: openai_o3_basic.py

from openai import OpenAI

class O3ReasoningClient:
    """Template for OpenAI o3 reasoning client."""

    def __init__(
        self,
        api_key: str = None,
        default_effort: str = "medium",
        default_max_tokens: int = 16000
    ):
        self.client = OpenAI(api_key=api_key)
        self.default_effort = default_effort
        self.default_max_tokens = default_max_tokens

    def reason(
        self,
        prompt: str,
        effort: str = None,
        max_tokens: int = None,
        system: str = None
    ) -> dict:
        """
        Execute reasoning request.

        Args:
            prompt: User prompt
            effort: "low", "medium", or "high"
            max_tokens: Max completion tokens (includes reasoning)
            system: Optional system prompt

        Returns:
            dict with answer and usage
        """
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model="o3",
            messages=messages,
            reasoning_effort=effort or self.default_effort,
            max_completion_tokens=max_tokens or self.default_max_tokens
        )

        return {
            "answer": response.choices[0].message.content,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            },
            "model": response.model,
            "finish_reason": response.choices[0].finish_reason
        }

    def reason_with_tools(
        self,
        prompt: str,
        tools: list[dict],
        tool_executor: callable,
        effort: str = None,
        max_iterations: int = 10
    ) -> dict:
        """Execute reasoning with tool use."""
        messages = [{"role": "user", "content": prompt}]
        iterations = 0

        while iterations < max_iterations:
            response = self.client.chat.completions.create(
                model="o3",
                messages=messages,
                tools=tools,
                reasoning_effort=effort or self.default_effort,
                max_completion_tokens=self.default_max_tokens
            )

            assistant_msg = response.choices[0].message
            messages.append(assistant_msg)

            if not assistant_msg.tool_calls:
                return {
                    "answer": assistant_msg.content,
                    "iterations": iterations + 1
                }

            # Execute tools
            for tool_call in assistant_msg.tool_calls:
                result = tool_executor(
                    tool_call.function.name,
                    tool_call.function.arguments
                )
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                })

            iterations += 1

        return {"error": "Max iterations reached"}


# Usage
if __name__ == "__main__":
    client = O3ReasoningClient(default_effort="medium")

    result = client.reason(
        prompt="Solve: If 3x + 7 = 22, what is x?",
        effort="low"
    )
    print(result["answer"])
```

### o4-mini for High-Volume

```python
# template: openai_o4_mini_batch.py

import asyncio
from openai import AsyncOpenAI
from dataclasses import dataclass
from typing import Optional

@dataclass
class ReasoningRequest:
    id: str
    prompt: str
    effort: str = "low"
    max_tokens: int = 4000

@dataclass
class ReasoningResult:
    id: str
    answer: str
    tokens_used: int
    success: bool
    error: Optional[str] = None

class O4MiniBatchProcessor:
    """Template for batch processing with o4-mini."""

    def __init__(
        self,
        api_key: str = None,
        max_concurrent: int = 10,
        retry_attempts: int = 3
    ):
        self.client = AsyncOpenAI(api_key=api_key)
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.retry_attempts = retry_attempts

    async def process_single(
        self,
        request: ReasoningRequest
    ) -> ReasoningResult:
        """Process single request with retry logic."""
        async with self.semaphore:
            for attempt in range(self.retry_attempts):
                try:
                    response = await self.client.chat.completions.create(
                        model="o4-mini",
                        messages=[{"role": "user", "content": request.prompt}],
                        reasoning_effort=request.effort,
                        max_completion_tokens=request.max_tokens
                    )

                    return ReasoningResult(
                        id=request.id,
                        answer=response.choices[0].message.content,
                        tokens_used=response.usage.total_tokens,
                        success=True
                    )
                except Exception as e:
                    if attempt == self.retry_attempts - 1:
                        return ReasoningResult(
                            id=request.id,
                            answer="",
                            tokens_used=0,
                            success=False,
                            error=str(e)
                        )
                    await asyncio.sleep(2 ** attempt)

    async def process_batch(
        self,
        requests: list[ReasoningRequest]
    ) -> list[ReasoningResult]:
        """Process batch of requests concurrently."""
        tasks = [self.process_single(req) for req in requests]
        return await asyncio.gather(*tasks)


# Usage
async def main():
    processor = O4MiniBatchProcessor(max_concurrent=5)

    requests = [
        ReasoningRequest(id=f"task_{i}", prompt=f"Calculate {i} * {i+1}")
        for i in range(100)
    ]

    results = await processor.process_batch(requests)

    success_count = sum(1 for r in results if r.success)
    print(f"Processed {len(results)} requests, {success_count} successful")
```

## 2. Claude Extended Thinking Templates

### Basic Extended Thinking

```python
# template: claude_extended_thinking.py

import anthropic
from dataclasses import dataclass
from typing import Optional

@dataclass
class ThinkingResponse:
    thinking: str
    answer: str
    input_tokens: int
    output_tokens: int

class ClaudeExtendedThinking:
    """Template for Claude with extended thinking."""

    MODELS = {
        "opus": "claude-opus-4-20250514",
        "sonnet": "claude-sonnet-4-20250514",
        "sonnet-3.7": "claude-3-7-sonnet-20250219"
    }

    def __init__(
        self,
        api_key: str = None,
        model: str = "sonnet",
        default_thinking_budget: int = 4000,
        default_max_tokens: int = 8000
    ):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = self.MODELS.get(model, model)
        self.default_thinking_budget = default_thinking_budget
        self.default_max_tokens = default_max_tokens

    def think(
        self,
        prompt: str,
        thinking_budget: int = None,
        max_tokens: int = None,
        system: str = None
    ) -> ThinkingResponse:
        """
        Execute request with extended thinking.

        Args:
            prompt: User prompt
            thinking_budget: Token budget for thinking (min 1024)
            max_tokens: Max output tokens
            system: Optional system prompt
        """
        budget = max(1024, thinking_budget or self.default_thinking_budget)

        kwargs = {
            "model": self.model,
            "max_tokens": max_tokens or self.default_max_tokens,
            "thinking": {
                "type": "enabled",
                "budget_tokens": budget
            },
            "messages": [{"role": "user", "content": prompt}]
        }

        if system:
            kwargs["system"] = system

        response = self.client.messages.create(**kwargs)

        # Parse response blocks
        thinking_parts = []
        answer_parts = []

        for block in response.content:
            if block.type == "thinking":
                thinking_parts.append(block.thinking)
            elif block.type == "text":
                answer_parts.append(block.text)

        return ThinkingResponse(
            thinking="\n".join(thinking_parts),
            answer="\n".join(answer_parts),
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens
        )

    def think_with_history(
        self,
        messages: list[dict],
        thinking_budget: int = None,
        preserve_thinking: bool = True
    ) -> ThinkingResponse:
        """
        Extended thinking with conversation history.

        Claude 4 preserves thinking blocks by default.
        """
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.default_max_tokens,
            thinking={
                "type": "enabled",
                "budget_tokens": thinking_budget or self.default_thinking_budget
            },
            messages=messages
        )

        thinking_parts = []
        answer_parts = []

        for block in response.content:
            if block.type == "thinking":
                thinking_parts.append(block.thinking)
            elif block.type == "text":
                answer_parts.append(block.text)

        return ThinkingResponse(
            thinking="\n".join(thinking_parts),
            answer="\n".join(answer_parts),
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens
        )


# Usage
if __name__ == "__main__":
    client = ClaudeExtendedThinking(model="sonnet")

    result = client.think(
        prompt="Design a caching strategy for a high-traffic API",
        thinking_budget=8000
    )

    print("=== Thinking ===")
    print(result.thinking[:500] + "...")
    print("\n=== Answer ===")
    print(result.answer)
```

### Interleaved Thinking with Tools

```python
# template: claude_interleaved_tools.py

import anthropic
from typing import Callable, Any

class ClaudeInterleavedThinking:
    """
    Template for Claude 4 with interleaved thinking and tools.

    Requires beta header: interleaved-thinking-2025-05-14
    """

    def __init__(
        self,
        api_key: str = None,
        model: str = "claude-sonnet-4-20250514",
        thinking_budget: int = 4000
    ):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        self.thinking_budget = thinking_budget

    def execute_with_tools(
        self,
        prompt: str,
        tools: list[dict],
        tool_executor: Callable[[str, dict], Any],
        max_iterations: int = 10
    ) -> dict:
        """
        Execute reasoning with interleaved thinking between tool calls.

        Args:
            prompt: User prompt
            tools: Tool definitions
            tool_executor: Function(tool_name, input) -> result
            max_iterations: Max tool use iterations
        """
        messages = [{"role": "user", "content": prompt}]
        all_thinking = []
        iterations = 0

        while iterations < max_iterations:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=8000,
                thinking={
                    "type": "enabled",
                    "budget_tokens": self.thinking_budget
                },
                tools=tools,
                messages=messages,
                betas=["interleaved-thinking-2025-05-14"]
            )

            # Collect thinking blocks
            assistant_content = []
            for block in response.content:
                if block.type == "thinking":
                    all_thinking.append(block.thinking)
                assistant_content.append(block)

            messages.append({"role": "assistant", "content": assistant_content})

            # Check for tool use
            tool_uses = [b for b in response.content if b.type == "tool_use"]

            if not tool_uses:
                # Extract final text answer
                final_answer = "\n".join(
                    b.text for b in response.content if b.type == "text"
                )
                return {
                    "answer": final_answer,
                    "thinking": all_thinking,
                    "iterations": iterations + 1
                }

            # Execute tools and continue
            tool_results = []
            for tool_use in tool_uses:
                result = tool_executor(tool_use.name, tool_use.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": str(result)
                })

            messages.append({"role": "user", "content": tool_results})
            iterations += 1

        return {"error": "Max iterations reached", "thinking": all_thinking}


# Usage
def my_tool_executor(name: str, params: dict) -> str:
    if name == "calculator":
        return str(eval(params["expression"]))
    elif name == "search":
        return f"Search results for: {params['query']}"
    return "Unknown tool"

tools = [
    {
        "name": "calculator",
        "description": "Evaluate mathematical expressions",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {"type": "string"}
            },
            "required": ["expression"]
        }
    },
    {
        "name": "search",
        "description": "Search for information",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"}
            },
            "required": ["query"]
        }
    }
]

if __name__ == "__main__":
    client = ClaudeInterleavedThinking()
    result = client.execute_with_tools(
        prompt="What is 15% of $2,340 and search for current tax rates",
        tools=tools,
        tool_executor=my_tool_executor
    )
    print(result["answer"])
```

## 3. DeepSeek R1 Templates

### Basic R1 Client

```python
# template: deepseek_r1_client.py

import re
from openai import OpenAI
from dataclasses import dataclass
from typing import Optional

@dataclass
class R1Response:
    thinking: str
    answer: str
    full_response: str
    tokens_used: int

class DeepSeekR1Client:
    """Template for DeepSeek R1 with visible reasoning."""

    MODELS = {
        "r1": "deepseek-reasoner",
        "r1-distill-7b": "deepseek-r1-distill-qwen-7b",
        "r1-distill-14b": "deepseek-r1-distill-qwen-14b",
        "r1-distill-32b": "deepseek-r1-distill-qwen-32b",
        "r1-distill-70b": "deepseek-r1-distill-llama-70b"
    }

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.deepseek.com/v1",
        model: str = "r1"
    ):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = self.MODELS.get(model, model)

    def reason(
        self,
        prompt: str,
        max_tokens: int = 8000,
        temperature: float = 0.0
    ) -> R1Response:
        """
        Execute reasoning with visible chain-of-thought.

        Response includes <think>...</think> blocks with reasoning.
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature
        )

        full_text = response.choices[0].message.content

        # Parse thinking blocks
        thinking_match = re.search(
            r'<think>(.*?)</think>',
            full_text,
            re.DOTALL
        )
        thinking = thinking_match.group(1).strip() if thinking_match else ""

        # Extract answer (text outside thinking tags)
        answer = re.sub(r'<think>.*?</think>', '', full_text, flags=re.DOTALL).strip()

        return R1Response(
            thinking=thinking,
            answer=answer,
            full_response=full_text,
            tokens_used=response.usage.total_tokens
        )

    def reason_with_system(
        self,
        prompt: str,
        system: str,
        max_tokens: int = 8000
    ) -> R1Response:
        """Execute reasoning with system prompt."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens
        )

        return self._parse_response(response)

    def _parse_response(self, response) -> R1Response:
        full_text = response.choices[0].message.content
        thinking_match = re.search(r'<think>(.*?)</think>', full_text, re.DOTALL)
        thinking = thinking_match.group(1).strip() if thinking_match else ""
        answer = re.sub(r'<think>.*?</think>', '', full_text, flags=re.DOTALL).strip()

        return R1Response(
            thinking=thinking,
            answer=answer,
            full_response=full_text,
            tokens_used=response.usage.total_tokens
        )


# Usage
if __name__ == "__main__":
    client = DeepSeekR1Client(api_key="your-api-key")

    result = client.reason(
        prompt="Prove that there are infinitely many prime numbers."
    )

    print("=== Thinking Process ===")
    print(result.thinking[:1000])
    print("\n=== Final Answer ===")
    print(result.answer)
```

### Local R1 Distilled with Ollama

```python
# template: deepseek_r1_ollama.py

import requests
import re
from dataclasses import dataclass

@dataclass
class LocalR1Response:
    thinking: str
    answer: str
    duration_ms: float

class DeepSeekR1Ollama:
    """
    Template for running distilled DeepSeek R1 locally via Ollama.

    Setup:
        ollama pull deepseek-r1:7b
        ollama pull deepseek-r1:14b
        ollama pull deepseek-r1:32b
    """

    def __init__(
        self,
        host: str = "http://localhost:11434",
        model: str = "deepseek-r1:7b"
    ):
        self.host = host
        self.model = model

    def reason(
        self,
        prompt: str,
        temperature: float = 0.0,
        num_ctx: int = 8192
    ) -> LocalR1Response:
        """Execute local reasoning with Ollama."""

        response = requests.post(
            f"{self.host}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_ctx": num_ctx
                }
            }
        )

        data = response.json()
        full_text = data["response"]

        # Parse thinking
        thinking_match = re.search(r'<think>(.*?)</think>', full_text, re.DOTALL)
        thinking = thinking_match.group(1).strip() if thinking_match else ""
        answer = re.sub(r'<think>.*?</think>', '', full_text, flags=re.DOTALL).strip()

        return LocalR1Response(
            thinking=thinking,
            answer=answer,
            duration_ms=data.get("total_duration", 0) / 1e6
        )

    def chat(
        self,
        messages: list[dict],
        temperature: float = 0.0
    ) -> LocalR1Response:
        """Multi-turn conversation with reasoning."""

        response = requests.post(
            f"{self.host}/api/chat",
            json={
                "model": self.model,
                "messages": messages,
                "stream": False,
                "options": {"temperature": temperature}
            }
        )

        data = response.json()
        full_text = data["message"]["content"]

        thinking_match = re.search(r'<think>(.*?)</think>', full_text, re.DOTALL)
        thinking = thinking_match.group(1).strip() if thinking_match else ""
        answer = re.sub(r'<think>.*?</think>', '', full_text, flags=re.DOTALL).strip()

        return LocalR1Response(
            thinking=thinking,
            answer=answer,
            duration_ms=data.get("total_duration", 0) / 1e6
        )
```

## 4. ReAct Agent Template

```python
# template: react_agent.py

from openai import OpenAI
from dataclasses import dataclass
from typing import Callable, Any
import re
import json

@dataclass
class ReActStep:
    thought: str
    action: str | None
    action_input: dict | None
    observation: str | None

@dataclass
class ReActResult:
    answer: str
    steps: list[ReActStep]
    total_tokens: int

class ReActAgent:
    """
    Template for ReAct (Reasoning + Acting) agent.

    Pattern: Thought -> Action -> Observation -> Thought -> ... -> Answer
    """

    SYSTEM_PROMPT = """You are a reasoning agent. Think step by step.

Available tools:
{tools}

Use this format:

Thought: [your reasoning about the current situation]
Action: [tool_name]
Action Input: {{"param": "value"}}

After receiving an observation, continue with more thoughts and actions.

When you have enough information to answer:
Thought: [final reasoning]
Final Answer: [your answer]

Begin!"""

    def __init__(
        self,
        client: OpenAI = None,
        model: str = "gpt-4o",
        tools: dict[str, Callable] = None
    ):
        self.client = client or OpenAI()
        self.model = model
        self.tools = tools or {}

    def add_tool(
        self,
        name: str,
        description: str,
        func: Callable[[dict], Any]
    ):
        """Register a tool for the agent to use."""
        self.tools[name] = {
            "description": description,
            "func": func
        }

    def run(
        self,
        query: str,
        max_steps: int = 10
    ) -> ReActResult:
        """Execute ReAct loop until answer or max steps."""

        tools_desc = "\n".join([
            f"- {name}: {info['description']}"
            for name, info in self.tools.items()
        ])

        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT.format(tools=tools_desc)},
            {"role": "user", "content": query}
        ]

        steps = []
        total_tokens = 0

        for _ in range(max_steps):
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.1
            )

            total_tokens += response.usage.total_tokens
            assistant_text = response.choices[0].message.content
            messages.append({"role": "assistant", "content": assistant_text})

            # Parse response
            step = self._parse_step(assistant_text)
            steps.append(step)

            # Check for final answer
            if "Final Answer:" in assistant_text:
                answer = assistant_text.split("Final Answer:")[-1].strip()
                return ReActResult(
                    answer=answer,
                    steps=steps,
                    total_tokens=total_tokens
                )

            # Execute action
            if step.action and step.action in self.tools:
                try:
                    observation = self.tools[step.action]["func"](step.action_input)
                except Exception as e:
                    observation = f"Error: {str(e)}"

                step.observation = str(observation)
                messages.append({
                    "role": "user",
                    "content": f"Observation: {observation}"
                })

        return ReActResult(
            answer="Max steps reached without final answer",
            steps=steps,
            total_tokens=total_tokens
        )

    def _parse_step(self, text: str) -> ReActStep:
        """Parse thought, action, and action input from text."""

        thought_match = re.search(r'Thought:\s*(.+?)(?=Action:|Final Answer:|$)', text, re.DOTALL)
        thought = thought_match.group(1).strip() if thought_match else ""

        action_match = re.search(r'Action:\s*(\w+)', text)
        action = action_match.group(1) if action_match else None

        action_input_match = re.search(r'Action Input:\s*(\{.+?\})', text, re.DOTALL)
        action_input = None
        if action_input_match:
            try:
                action_input = json.loads(action_input_match.group(1))
            except json.JSONDecodeError:
                pass

        return ReActStep(
            thought=thought,
            action=action,
            action_input=action_input,
            observation=None
        )


# Usage example
if __name__ == "__main__":
    agent = ReActAgent()

    # Add tools
    agent.add_tool(
        "calculator",
        "Evaluate mathematical expressions. Input: {'expression': 'math expression'}",
        lambda params: eval(params["expression"])
    )

    agent.add_tool(
        "search",
        "Search for information. Input: {'query': 'search query'}",
        lambda params: f"Search results for: {params['query']}"
    )

    result = agent.run("What is 15% of 847 plus 23?")

    print("=== Steps ===")
    for i, step in enumerate(result.steps):
        print(f"\nStep {i+1}:")
        print(f"  Thought: {step.thought[:100]}...")
        if step.action:
            print(f"  Action: {step.action}")
        if step.observation:
            print(f"  Observation: {step.observation}")

    print(f"\n=== Answer ===\n{result.answer}")
```

## 5. Reasoning Router Template

```python
# template: reasoning_router.py

from enum import Enum
from dataclasses import dataclass
from typing import Any
from openai import OpenAI
import anthropic

class Complexity(Enum):
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"

@dataclass
class RouterConfig:
    simple_model: str = "gpt-4o-mini"
    moderate_model: str = "o4-mini"
    complex_model: str = "o3"
    moderate_effort: str = "low"
    complex_effort: str = "high"

class ReasoningRouter:
    """
    Template for routing requests to appropriate reasoning model.

    Optimizes cost while maintaining quality.
    """

    CLASSIFIER_PROMPT = """Classify this task's complexity level.

Task: {task}

Respond with exactly one word: SIMPLE, MODERATE, or COMPLEX

SIMPLE: Direct questions, simple formatting, basic lookups
MODERATE: Multi-step tasks, standard coding, some reasoning
COMPLEX: Math proofs, complex algorithms, strategic analysis"""

    def __init__(
        self,
        openai_key: str = None,
        anthropic_key: str = None,
        config: RouterConfig = None
    ):
        self.openai = OpenAI(api_key=openai_key)
        self.anthropic = anthropic.Anthropic(api_key=anthropic_key) if anthropic_key else None
        self.config = config or RouterConfig()

    def classify(self, task: str) -> Complexity:
        """Classify task complexity."""
        response = self.openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "user",
                "content": self.CLASSIFIER_PROMPT.format(task=task)
            }],
            temperature=0,
            max_tokens=10
        )

        text = response.choices[0].message.content.strip().upper()

        if "SIMPLE" in text:
            return Complexity.SIMPLE
        elif "COMPLEX" in text:
            return Complexity.COMPLEX
        return Complexity.MODERATE

    def route(self, task: str, force_complexity: Complexity = None) -> dict:
        """Route task to appropriate model and execute."""

        complexity = force_complexity or self.classify(task)

        if complexity == Complexity.SIMPLE:
            return self._execute_simple(task)
        elif complexity == Complexity.MODERATE:
            return self._execute_moderate(task)
        else:
            return self._execute_complex(task)

    def _execute_simple(self, task: str) -> dict:
        """Fast, cheap execution for simple tasks."""
        response = self.openai.chat.completions.create(
            model=self.config.simple_model,
            messages=[{"role": "user", "content": task}]
        )
        return {
            "answer": response.choices[0].message.content,
            "model": self.config.simple_model,
            "complexity": "simple",
            "tokens": response.usage.total_tokens
        }

    def _execute_moderate(self, task: str) -> dict:
        """Balanced execution with light reasoning."""
        response = self.openai.chat.completions.create(
            model=self.config.moderate_model,
            messages=[{"role": "user", "content": task}],
            reasoning_effort=self.config.moderate_effort
        )
        return {
            "answer": response.choices[0].message.content,
            "model": self.config.moderate_model,
            "complexity": "moderate",
            "tokens": response.usage.total_tokens
        }

    def _execute_complex(self, task: str) -> dict:
        """Full reasoning for complex tasks."""
        response = self.openai.chat.completions.create(
            model=self.config.complex_model,
            messages=[{"role": "user", "content": task}],
            reasoning_effort=self.config.complex_effort,
            max_completion_tokens=32000
        )
        return {
            "answer": response.choices[0].message.content,
            "model": self.config.complex_model,
            "complexity": "complex",
            "tokens": response.usage.total_tokens
        }


# Usage
if __name__ == "__main__":
    router = ReasoningRouter()

    # Simple task
    result = router.route("What is the capital of France?")
    print(f"Simple: {result['model']} - {result['answer']}")

    # Complex task
    result = router.route("Prove that the sum of two even numbers is even")
    print(f"Complex: {result['model']} - {result['answer'][:200]}...")
```

## 6. Thinking Budget Optimizer

```python
# template: thinking_budget_optimizer.py

from dataclasses import dataclass
import time
import anthropic

@dataclass
class OptimizationResult:
    optimal_budget: int
    accuracy: float
    cost_per_request: float
    latency_p50: float

class ThinkingBudgetOptimizer:
    """
    Template for finding optimal thinking budget.

    Balances accuracy, cost, and latency.
    """

    BUDGETS = [1024, 2048, 4096, 8192, 16384, 32768]

    def __init__(
        self,
        api_key: str = None,
        model: str = "claude-sonnet-4-20250514"
    ):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def optimize(
        self,
        test_prompts: list[str],
        expected_outputs: list[str],
        accuracy_threshold: float = 0.9,
        cost_weight: float = 0.3
    ) -> OptimizationResult:
        """
        Find optimal budget that meets accuracy threshold.

        Args:
            test_prompts: List of test prompts
            expected_outputs: Expected answers (for accuracy)
            accuracy_threshold: Minimum required accuracy
            cost_weight: Weight for cost vs accuracy (0-1)
        """

        results = []

        for budget in self.BUDGETS:
            accuracy, latencies, costs = self._evaluate_budget(
                test_prompts, expected_outputs, budget
            )

            results.append({
                "budget": budget,
                "accuracy": accuracy,
                "latency_p50": sorted(latencies)[len(latencies)//2],
                "cost": sum(costs) / len(costs)
            })

            # Early stop if we meet threshold with min budget
            if accuracy >= accuracy_threshold and budget == self.BUDGETS[0]:
                break

        # Find optimal: highest accuracy meeting threshold with lowest cost
        valid = [r for r in results if r["accuracy"] >= accuracy_threshold]

        if not valid:
            # No budget meets threshold, use highest accuracy
            best = max(results, key=lambda x: x["accuracy"])
        else:
            # Minimize cost among valid options
            best = min(valid, key=lambda x: x["cost"])

        return OptimizationResult(
            optimal_budget=best["budget"],
            accuracy=best["accuracy"],
            cost_per_request=best["cost"],
            latency_p50=best["latency_p50"]
        )

    def _evaluate_budget(
        self,
        prompts: list[str],
        expected: list[str],
        budget: int
    ) -> tuple[float, list[float], list[float]]:
        """Evaluate accuracy at given budget."""

        correct = 0
        latencies = []
        costs = []

        for prompt, exp in zip(prompts, expected):
            start = time.time()

            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                thinking={
                    "type": "enabled",
                    "budget_tokens": budget
                },
                messages=[{"role": "user", "content": prompt}]
            )

            latencies.append(time.time() - start)

            # Calculate cost (approximate)
            input_cost = response.usage.input_tokens * 0.000003  # $3/M
            output_cost = response.usage.output_tokens * 0.000015  # $15/M
            costs.append(input_cost + output_cost)

            # Check accuracy (simple string match - customize for your use case)
            answer = "".join(
                b.text for b in response.content if b.type == "text"
            ).lower()

            if exp.lower() in answer:
                correct += 1

        accuracy = correct / len(prompts)
        return accuracy, latencies, costs
```
