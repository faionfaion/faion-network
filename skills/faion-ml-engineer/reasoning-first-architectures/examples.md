---
id: reasoning-first-architectures-examples
name: "Reasoning-First Architectures Examples"
parent: reasoning-first-architectures
---

# Reasoning-First Architectures Examples

## 1. ReAct Pattern Implementation

### Python Implementation

```python
from openai import OpenAI

client = OpenAI()

def react_agent(query: str, tools: list[dict], max_iterations: int = 5) -> str:
    """
    ReAct agent with interleaved reasoning and acting.

    Pattern: Thought -> Action -> Observation -> Thought -> ...
    """

    system_prompt = """You are a reasoning agent that thinks step by step.

For each step, use this format:
Thought: [your reasoning about what to do next]
Action: [tool_name](parameters)
Observation: [will be filled by tool result]

When you have enough information, provide:
Thought: [final reasoning]
Answer: [your final answer]

Available tools:
{tools}
"""

    messages = [
        {"role": "system", "content": system_prompt.format(tools=tools)},
        {"role": "user", "content": query}
    ]

    for i in range(max_iterations):
        response = client.chat.completions.create(
            model="gpt-4o",  # or use o3 for complex reasoning
            messages=messages,
            temperature=0.1
        )

        assistant_message = response.choices[0].message.content
        messages.append({"role": "assistant", "content": assistant_message})

        # Check if we have a final answer
        if "Answer:" in assistant_message:
            return extract_answer(assistant_message)

        # Extract and execute action
        action = extract_action(assistant_message)
        if action:
            observation = execute_tool(action, tools)
            messages.append({
                "role": "user",
                "content": f"Observation: {observation}"
            })

    return "Max iterations reached without answer"


def extract_action(text: str) -> dict | None:
    """Extract Action: tool_name(params) from text."""
    import re
    match = re.search(r'Action:\s*(\w+)\((.*?)\)', text)
    if match:
        return {"tool": match.group(1), "params": match.group(2)}
    return None


def extract_answer(text: str) -> str:
    """Extract final answer from text."""
    import re
    match = re.search(r'Answer:\s*(.+)', text, re.DOTALL)
    return match.group(1).strip() if match else text
```

### Example ReAct Trace

```
Query: What was Company X's Q4 2025 revenue and how does it compare to last year?

Thought: I need to find Company X's Q4 2025 revenue. Let me search for their financial report.
Action: search("Company X Q4 2025 revenue report")
Observation: [Search results showing $4.2B revenue announced in earnings call]

Thought: Found Q4 2025 revenue was $4.2B. Now I need Q4 2024 for YoY comparison.
Action: search("Company X Q4 2024 revenue")
Observation: [Search results showing $3.8B revenue for Q4 2024]

Thought: I have both figures. Q4 2025: $4.2B, Q4 2024: $3.8B.
Growth = (4.2 - 3.8) / 3.8 = 10.5% YoY increase.
Answer: Company X's Q4 2025 revenue was $4.2B, representing a 10.5% year-over-year increase from $3.8B in Q4 2024.
```

## 2. OpenAI o3 with Reasoning Effort

### Basic Usage

```python
from openai import OpenAI

client = OpenAI()

def solve_complex_problem(problem: str, effort: str = "medium") -> dict:
    """
    Use o3 with configurable reasoning effort.

    effort: "low" (~5K tokens), "medium" (~15K), "high" (~30K+)
    """

    response = client.chat.completions.create(
        model="o3",
        messages=[
            {"role": "user", "content": problem}
        ],
        reasoning_effort=effort,
        max_completion_tokens=16000  # includes reasoning + output
    )

    return {
        "answer": response.choices[0].message.content,
        "usage": {
            "input_tokens": response.usage.prompt_tokens,
            "output_tokens": response.usage.completion_tokens,
            # Note: reasoning tokens are hidden but billed
            "total_tokens": response.usage.total_tokens
        }
    }


# Example: Math problem
result = solve_complex_problem(
    """
    A farmer has a rectangular field. If he increases the length by 20%
    and decreases the width by 10%, the area increases by 100 square meters.
    If he decreases the length by 10% and increases the width by 20%,
    the area increases by 200 square meters. Find the original dimensions.
    """,
    effort="high"
)
print(result["answer"])
```

### o3 with Tools

```python
def o3_with_tools(query: str, tools: list[dict]) -> str:
    """
    o3 can reason about when and how to use tools.
    Trained via RL to make tool decisions based on outcomes.
    """

    response = client.chat.completions.create(
        model="o3",
        messages=[{"role": "user", "content": query}],
        tools=tools,
        reasoning_effort="medium",
        max_completion_tokens=8000
    )

    # Handle tool calls in reasoning loop
    while response.choices[0].message.tool_calls:
        tool_calls = response.choices[0].message.tool_calls

        # Execute tools
        tool_results = []
        for call in tool_calls:
            result = execute_tool(call.function.name, call.function.arguments)
            tool_results.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": result
            })

        # Continue reasoning with tool results
        response = client.chat.completions.create(
            model="o3",
            messages=[
                {"role": "user", "content": query},
                response.choices[0].message,
                *tool_results
            ],
            tools=tools,
            reasoning_effort="medium",
            max_completion_tokens=8000
        )

    return response.choices[0].message.content
```

## 3. Claude Extended Thinking

### Basic Extended Thinking

```python
import anthropic

client = anthropic.Anthropic()

def claude_extended_thinking(
    prompt: str,
    thinking_budget: int = 4000,
    model: str = "claude-sonnet-4-20250514"
) -> dict:
    """
    Claude with extended thinking enabled.

    thinking_budget: Minimum 1024 tokens, adjust based on complexity.
    """

    response = client.messages.create(
        model=model,
        max_tokens=8000,
        thinking={
            "type": "enabled",
            "budget_tokens": thinking_budget
        },
        messages=[{"role": "user", "content": prompt}]
    )

    # Parse response - thinking blocks + text blocks
    thinking_blocks = []
    text_blocks = []

    for block in response.content:
        if block.type == "thinking":
            thinking_blocks.append(block.thinking)
        elif block.type == "text":
            text_blocks.append(block.text)

    return {
        "thinking": "\n".join(thinking_blocks),
        "answer": "\n".join(text_blocks),
        "usage": {
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens
        }
    }


# Example
result = claude_extended_thinking(
    """
    Design a database schema for a multi-tenant SaaS application
    that needs to support:
    - User authentication with SSO
    - Role-based access control
    - Audit logging
    - Data isolation between tenants

    Consider performance, scalability, and security.
    """,
    thinking_budget=8000
)

print("=== Thinking Process ===")
print(result["thinking"])
print("\n=== Final Answer ===")
print(result["answer"])
```

### Interleaved Thinking with Tools

```python
def claude_interleaved_thinking_with_tools(
    prompt: str,
    tools: list[dict],
    thinking_budget: int = 4000
) -> str:
    """
    Claude 4 with interleaved thinking between tool calls.
    Requires beta header for interleaved-thinking-2025-05-14.
    """

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8000,
        thinking={
            "type": "enabled",
            "budget_tokens": thinking_budget
        },
        tools=tools,
        messages=[{"role": "user", "content": prompt}],
        betas=["interleaved-thinking-2025-05-14"]
    )

    messages = [{"role": "user", "content": prompt}]

    while response.stop_reason == "tool_use":
        # Extract tool uses and thinking from response
        assistant_content = response.content
        messages.append({"role": "assistant", "content": assistant_content})

        # Execute tools
        tool_results = []
        for block in assistant_content:
            if block.type == "tool_use":
                result = execute_tool(block.name, block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result
                })

        messages.append({"role": "user", "content": tool_results})

        # Continue with more thinking after tool results
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8000,
            thinking={"type": "enabled", "budget_tokens": thinking_budget},
            tools=tools,
            messages=messages,
            betas=["interleaved-thinking-2025-05-14"]
        )

    # Extract final text answer
    return "".join(
        block.text for block in response.content
        if block.type == "text"
    )
```

## 4. DeepSeek R1 with Visible Reasoning

### Parsing Think Tags

```python
import re
from openai import OpenAI

# DeepSeek R1 uses OpenAI-compatible API
client = OpenAI(
    base_url="https://api.deepseek.com/v1",
    api_key="your-deepseek-api-key"
)

def deepseek_r1_reasoning(prompt: str) -> dict:
    """
    DeepSeek R1 with visible chain-of-thought in <think> tags.
    """

    response = client.chat.completions.create(
        model="deepseek-reasoner",  # or deepseek-r1
        messages=[{"role": "user", "content": prompt}],
        max_tokens=8000
    )

    full_response = response.choices[0].message.content

    # Parse <think>...</think> blocks
    thinking_match = re.search(
        r'<think>(.*?)</think>',
        full_response,
        re.DOTALL
    )

    thinking = thinking_match.group(1).strip() if thinking_match else ""

    # Remove thinking tags to get final answer
    answer = re.sub(
        r'<think>.*?</think>',
        '',
        full_response,
        flags=re.DOTALL
    ).strip()

    return {
        "thinking": thinking,
        "answer": answer,
        "full_response": full_response
    }


# Example
result = deepseek_r1_reasoning(
    "Prove that the square root of 2 is irrational."
)

print("=== DeepSeek R1 Thinking ===")
print(result["thinking"][:1000] + "...")
print("\n=== Final Answer ===")
print(result["answer"])
```

### Using Distilled Models

```python
def deepseek_r1_distilled(
    prompt: str,
    model_size: str = "7b"
) -> dict:
    """
    Use distilled DeepSeek R1 models for cost efficiency.

    Available sizes: 1.5b, 7b, 8b, 14b, 32b, 70b
    Based on Qwen2.5 and Llama3.
    """

    model_map = {
        "1.5b": "deepseek-r1-distill-qwen-1.5b",
        "7b": "deepseek-r1-distill-qwen-7b",
        "8b": "deepseek-r1-distill-llama-8b",
        "14b": "deepseek-r1-distill-qwen-14b",
        "32b": "deepseek-r1-distill-qwen-32b",
        "70b": "deepseek-r1-distill-llama-70b"
    }

    # Can run locally via Ollama or vLLM
    # Or use DeepSeek API for cloud inference
    response = client.chat.completions.create(
        model=model_map.get(model_size, "deepseek-r1-distill-qwen-7b"),
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4000
    )

    return parse_deepseek_response(response.choices[0].message.content)
```

## 5. Tree-of-Thought Implementation

### Basic ToT

```python
from dataclasses import dataclass
from typing import Callable

@dataclass
class ThoughtNode:
    content: str
    score: float
    children: list["ThoughtNode"]

def tree_of_thought(
    problem: str,
    generate_thoughts: Callable,
    evaluate_thought: Callable,
    num_branches: int = 3,
    max_depth: int = 3,
    beam_width: int = 2
) -> str:
    """
    Tree-of-Thought reasoning with beam search.

    Explores multiple reasoning paths and selects the best.
    """

    # Generate initial thoughts
    initial_thoughts = generate_thoughts(problem, num_branches)

    # Create root nodes
    frontier = [
        ThoughtNode(
            content=thought,
            score=evaluate_thought(problem, thought),
            children=[]
        )
        for thought in initial_thoughts
    ]

    # Beam search through thought tree
    for depth in range(max_depth):
        # Keep top beam_width nodes
        frontier.sort(key=lambda x: x.score, reverse=True)
        frontier = frontier[:beam_width]

        if depth == max_depth - 1:
            break

        # Expand best nodes
        new_frontier = []
        for node in frontier:
            context = f"{problem}\n\nPrevious reasoning:\n{node.content}"
            child_thoughts = generate_thoughts(context, num_branches)

            for child_thought in child_thoughts:
                full_thought = f"{node.content}\n\n{child_thought}"
                child_node = ThoughtNode(
                    content=full_thought,
                    score=evaluate_thought(problem, full_thought),
                    children=[]
                )
                node.children.append(child_node)
                new_frontier.append(child_node)

        frontier = new_frontier

    # Return best path
    frontier.sort(key=lambda x: x.score, reverse=True)
    return frontier[0].content if frontier else ""


def generate_thoughts(context: str, n: int) -> list[str]:
    """Generate n different reasoning approaches."""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": f"""Given this problem/context, generate {n} different
            reasoning approaches or next steps. Format as a numbered list.

            {context}"""
        }],
        temperature=0.8
    )

    # Parse numbered list
    text = response.choices[0].message.content
    thoughts = re.findall(r'\d+\.\s*(.+?)(?=\d+\.|$)', text, re.DOTALL)
    return [t.strip() for t in thoughts][:n]


def evaluate_thought(problem: str, thought: str) -> float:
    """Score a reasoning path 0-1."""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": f"""Rate this reasoning approach for solving the problem.
            Score from 0.0 to 1.0 based on:
            - Logical coherence
            - Progress toward solution
            - Likelihood of success

            Problem: {problem}

            Reasoning: {thought}

            Respond with just a number between 0.0 and 1.0"""
        }],
        temperature=0
    )

    try:
        return float(response.choices[0].message.content.strip())
    except:
        return 0.5
```

## 6. Reflexion Pattern

### Self-Improving Agent

```python
def reflexion_agent(
    task: str,
    executor: Callable,
    evaluator: Callable,
    max_iterations: int = 3
) -> dict:
    """
    Reflexion agent that learns from its mistakes.

    Pattern: Execute -> Evaluate -> Reflect -> Retry
    """

    memory = []  # Store reflections

    for iteration in range(max_iterations):
        # Generate with memory of past failures
        memory_context = "\n".join([
            f"Previous attempt {i+1}:\n{m['attempt']}\nReflection: {m['reflection']}"
            for i, m in enumerate(memory)
        ]) if memory else "This is your first attempt."

        prompt = f"""Task: {task}

{memory_context}

Based on any previous reflections, provide your best solution."""

        # Execute
        result = executor(prompt)

        # Evaluate
        evaluation = evaluator(task, result)

        if evaluation["success"]:
            return {
                "result": result,
                "iterations": iteration + 1,
                "memory": memory
            }

        # Reflect on failure
        reflection_prompt = f"""Task: {task}

Your attempt: {result}

Feedback: {evaluation['feedback']}

Reflect on what went wrong and how to improve. Be specific."""

        reflection = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": reflection_prompt}]
        ).choices[0].message.content

        memory.append({
            "attempt": result,
            "feedback": evaluation["feedback"],
            "reflection": reflection
        })

    return {
        "result": result,
        "iterations": max_iterations,
        "memory": memory,
        "success": False
    }
```

## 7. Hybrid Reasoning Router

### Route Based on Complexity

```python
from enum import Enum

class TaskComplexity(Enum):
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"

def classify_complexity(task: str) -> TaskComplexity:
    """Classify task complexity for model routing."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": f"""Classify this task's complexity:

Task: {task}

Respond with exactly one of: SIMPLE, MODERATE, COMPLEX

SIMPLE: Direct factual queries, simple formatting, basic Q&A
MODERATE: Multi-step tasks, some reasoning needed, standard coding
COMPLEX: Mathematical proofs, complex code, strategic analysis, research"""
        }],
        temperature=0
    )

    text = response.choices[0].message.content.strip().upper()

    if "SIMPLE" in text:
        return TaskComplexity.SIMPLE
    elif "COMPLEX" in text:
        return TaskComplexity.COMPLEX
    return TaskComplexity.MODERATE


def reasoning_router(task: str) -> str:
    """
    Route tasks to appropriate model based on complexity.
    Optimizes cost while maintaining quality.
    """

    complexity = classify_complexity(task)

    if complexity == TaskComplexity.SIMPLE:
        # Fast, cheap model for simple tasks
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": task}]
        )
        return response.choices[0].message.content

    elif complexity == TaskComplexity.MODERATE:
        # Balanced model with light reasoning
        response = client.chat.completions.create(
            model="o4-mini",
            messages=[{"role": "user", "content": task}],
            reasoning_effort="low"
        )
        return response.choices[0].message.content

    else:  # COMPLEX
        # Full reasoning power
        response = client.chat.completions.create(
            model="o3",
            messages=[{"role": "user", "content": task}],
            reasoning_effort="high",
            max_completion_tokens=32000
        )
        return response.choices[0].message.content
```

## 8. Multi-Model Verification

### Ensemble Reasoning

```python
async def ensemble_reasoning(
    problem: str,
    models: list[dict]
) -> dict:
    """
    Use multiple reasoning models and aggregate results.
    Increases reliability for high-stakes decisions.
    """
    import asyncio

    async def query_model(model_config: dict) -> dict:
        if model_config["provider"] == "openai":
            response = await async_openai.chat.completions.create(
                model=model_config["model"],
                messages=[{"role": "user", "content": problem}],
                **model_config.get("params", {})
            )
            return {
                "model": model_config["model"],
                "answer": response.choices[0].message.content
            }
        elif model_config["provider"] == "anthropic":
            response = await async_anthropic.messages.create(
                model=model_config["model"],
                messages=[{"role": "user", "content": problem}],
                **model_config.get("params", {})
            )
            return {
                "model": model_config["model"],
                "answer": response.content[0].text
            }

    # Query all models in parallel
    results = await asyncio.gather(*[query_model(m) for m in models])

    # Aggregate results
    aggregation_prompt = f"""Problem: {problem}

Different AI models provided these answers:

{chr(10).join(f"Model {r['model']}: {r['answer']}" for r in results)}

Synthesize the best answer by:
1. Identifying points of agreement
2. Resolving disagreements using logical analysis
3. Providing the most accurate final answer"""

    final = client.chat.completions.create(
        model="o3",
        messages=[{"role": "user", "content": aggregation_prompt}],
        reasoning_effort="medium"
    )

    return {
        "individual_results": results,
        "aggregated_answer": final.choices[0].message.content
    }


# Example configuration
models = [
    {"provider": "openai", "model": "o3", "params": {"reasoning_effort": "medium"}},
    {"provider": "anthropic", "model": "claude-sonnet-4-20250514",
     "params": {"thinking": {"type": "enabled", "budget_tokens": 4000}}},
    {"provider": "deepseek", "model": "deepseek-r1", "params": {}}
]
```
