---
name: faion-langchain-agents-architectures
user-invocable: false
description: "LangChain agent architectures and tool integration: ReAct, Plan-and-Execute, LATS"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(python:*), Bash(pip:*)
---

# LangChain Agent Architectures & Tools

**Communication: User's language. Docs/code: English.**

## Purpose

Agent architectures (ReAct, Plan-and-Execute, LATS) and tool integration using LangChain and LangGraph.

## When to Use

- Building ReAct agents with tool use
- Creating multi-step planning agents
- Implementing tree search for complex reasoning
- Integrating tools with agents

---

# Section 1: Agent Architectures

## Architecture 1: ReAct (Reasoning + Acting)

Think step-by-step, use tools, observe results, repeat.

```python
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

# Define tools
@tool
def search(query: str) -> str:
    """Search the web for information."""
    # Implementation
    return f"Results for: {query}"

@tool
def calculator(expression: str) -> str:
    """Calculate a mathematical expression."""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"

# Create ReAct agent
model = ChatOpenAI(model="gpt-4o")
tools = [search, calculator]

agent = create_react_agent(model, tools)

# Run
result = agent.invoke({
    "messages": [("human", "What is 25 * 4 and who invented calculus?")]
})
```

## Architecture 2: Plan-and-Execute

Plan all steps first, then execute each.

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, List
import operator

class PlanExecuteState(TypedDict):
    input: str
    plan: List[str]
    current_step: int
    results: Annotated[List[str], operator.add]
    final_answer: str

def planner(state: PlanExecuteState) -> PlanExecuteState:
    """Create a plan of steps."""
    prompt = f"""Create a step-by-step plan to answer: {state['input']}
    Return a numbered list of steps."""

    response = model.invoke(prompt)
    steps = parse_steps(response.content)

    return {"plan": steps, "current_step": 0}

def executor(state: PlanExecuteState) -> PlanExecuteState:
    """Execute current step."""
    step = state["plan"][state["current_step"]]

    result = model.invoke(f"Execute this step: {step}")

    return {
        "results": [result.content],
        "current_step": state["current_step"] + 1
    }

def should_continue(state: PlanExecuteState) -> str:
    if state["current_step"] >= len(state["plan"]):
        return "synthesize"
    return "execute"

def synthesizer(state: PlanExecuteState) -> PlanExecuteState:
    """Combine results into final answer."""
    all_results = "\n".join(state["results"])
    prompt = f"Synthesize these results into a final answer:\n{all_results}"

    response = model.invoke(prompt)
    return {"final_answer": response.content}

# Build graph
graph = StateGraph(PlanExecuteState)
graph.add_node("plan", planner)
graph.add_node("execute", executor)
graph.add_node("synthesize", synthesizer)

graph.set_entry_point("plan")
graph.add_edge("plan", "execute")
graph.add_conditional_edges("execute", should_continue)
graph.add_edge("synthesize", END)

agent = graph.compile()
```

## Architecture 3: LATS (Language Agent Tree Search)

Tree search with backtracking for complex problems.

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Optional
import random

class LATSState(TypedDict):
    problem: str
    thoughts: List[dict]  # Tree of thoughts
    current_path: List[int]  # Path through tree
    best_solution: Optional[str]
    best_score: float

def generate_thoughts(state: LATSState) -> LATSState:
    """Generate multiple candidate thoughts."""
    current_context = get_current_context(state)

    prompt = f"""Given this problem and context, generate 3 different approaches:
    Problem: {state['problem']}
    Context: {current_context}

    Return 3 distinct approaches."""

    response = model.invoke(prompt)
    new_thoughts = parse_thoughts(response.content)

    # Add to tree
    parent_idx = state["current_path"][-1] if state["current_path"] else -1
    for thought in new_thoughts:
        state["thoughts"].append({
            "content": thought,
            "parent": parent_idx,
            "score": None,
            "children": []
        })

    return state

def evaluate_thoughts(state: LATSState) -> LATSState:
    """Score each thought for promise."""
    for i, thought in enumerate(state["thoughts"]):
        if thought["score"] is None:
            prompt = f"""Rate this approach (0-10):
            Problem: {state['problem']}
            Approach: {thought['content']}
            """
            response = model.invoke(prompt)
            thought["score"] = parse_score(response.content)

    return state

def select_thought(state: LATSState) -> LATSState:
    """Select most promising unexplored thought."""
    unexplored = [
        (i, t) for i, t in enumerate(state["thoughts"])
        if not t["children"] and t["score"] is not None
    ]

    if not unexplored:
        return state

    # UCB-like selection
    best_idx = max(unexplored, key=lambda x: x[1]["score"])[0]
    state["current_path"].append(best_idx)

    return state

def should_continue_lats(state: LATSState) -> str:
    if state["best_score"] and state["best_score"] > 8:
        return END
    if len(state["thoughts"]) > 20:  # Max nodes
        return END
    return "generate"

# Build LATS graph
lats = StateGraph(LATSState)
lats.add_node("generate", generate_thoughts)
lats.add_node("evaluate", evaluate_thoughts)
lats.add_node("select", select_thought)

lats.set_entry_point("generate")
lats.add_edge("generate", "evaluate")
lats.add_edge("evaluate", "select")
lats.add_conditional_edges("select", should_continue_lats)
```

---

# Section 2: Tool Integration

## Defining Tools

```python
from langchain_core.tools import tool, StructuredTool
from pydantic import BaseModel, Field

# Simple tool with decorator
@tool
def search(query: str) -> str:
    """Search the web for information about a topic."""
    return f"Search results for: {query}"

# Tool with complex input
class CalculatorInput(BaseModel):
    expression: str = Field(description="Mathematical expression")
    precision: int = Field(default=2, description="Decimal places")

@tool(args_schema=CalculatorInput)
def calculate(expression: str, precision: int = 2) -> str:
    """Calculate a mathematical expression."""
    result = eval(expression)
    return f"{result:.{precision}f}"

# Dynamic tool creation
def create_api_tool(api_name: str, base_url: str):
    @tool(name=f"{api_name}_api")
    def api_tool(endpoint: str, params: dict = None) -> str:
        f"""Call the {api_name} API."""
        # Implementation
        return f"API response from {base_url}/{endpoint}"
    return api_tool
```

## Tool Error Handling

```python
from langchain_core.tools import ToolException

@tool(handle_tool_error=True)
def risky_tool(input: str) -> str:
    """A tool that might fail."""
    if not input:
        raise ToolException("Input cannot be empty")
    return f"Processed: {input}"

# Custom error handler
def handle_error(error: ToolException) -> str:
    return f"Tool failed: {error}. Please try again with valid input."

@tool(handle_tool_error=handle_error)
def custom_error_tool(input: str) -> str:
    """Tool with custom error handling."""
    if "bad" in input:
        raise ToolException("Bad input detected")
    return input
```

## Tool Binding

```python
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o")
tools = [search, calculate]

# Bind tools to model
model_with_tools = model.bind_tools(tools)

# Invoke
response = model_with_tools.invoke("What is 25 * 4?")

# Check for tool calls
if response.tool_calls:
    for call in response.tool_calls:
        print(f"Tool: {call['name']}, Args: {call['args']}")
```

---

# Quick Reference

## Agent Architectures

| Architecture | Strengths | Use When |
|--------------|-----------|----------|
| ReAct | Simple, debuggable | Basic tool use |
| Plan-and-Execute | Structured | Multi-step tasks |
| LATS | Handles uncertainty | Complex reasoning |

## Tool Integration Patterns

| Pattern | Use Case |
|---------|----------|
| @tool decorator | Simple tools |
| StructuredTool | Complex input schemas |
| Dynamic creation | Runtime tool generation |
| Error handlers | Robust tool execution |

---

# Related

| File | Purpose |
|------|---------|
| [langchain-agents-multi-agent.md](langchain-agents-multi-agent.md) | Multi-agent systems and testing |
| [langchain-memory.md](langchain-memory.md) | Memory and workflows |
| [autonomous-agents.md](autonomous-agents.md) | Building autonomous agents |

---

*faion-langchain-agents-architectures v1.0*
*LangChain 0.3.x / LangGraph 0.2.x*
*Covers: ReAct, Plan-and-Execute, LATS, tool integration*
## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Generate tool definitions from API | haiku | Mechanical transformation |
| Review agent reasoning chains | sonnet | Requires logic analysis |
| Design multi-agent orchestration | opus | Complex coordination patterns |

