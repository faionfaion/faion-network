# LangChain Workflows

**Part of:** [langchain.md](langchain.md)

## LangGraph Workflows

LangGraph enables building stateful, multi-step workflows with complex control flow.

## Core Concepts

### State Definition

```python
from typing import TypedDict, Annotated, List
import operator

class WorkflowState(TypedDict):
    # Simple fields
    input: str
    output: str

    # Accumulating field (appends instead of replaces)
    messages: Annotated[List[str], operator.add]

    # Optional field
    error: str | None

# Usage: {"messages": ["new"]} adds to existing messages
```

### Node Functions

```python
from langgraph.graph import StateGraph, END

def process_node(state: WorkflowState) -> WorkflowState:
    """Process the input."""
    result = f"Processed: {state['input']}"
    return {
        "output": result,
        "messages": [f"Processed input: {state['input']}"]
    }

def validate_node(state: WorkflowState) -> WorkflowState:
    """Validate the output."""
    if "error" in state["output"].lower():
        return {"error": "Validation failed"}
    return {"messages": ["Validation passed"]}

def finalize_node(state: WorkflowState) -> WorkflowState:
    """Finalize the workflow."""
    return {"messages": ["Workflow complete"]}
```

### Conditional Edges

```python
def should_continue(state: WorkflowState) -> str:
    """Determine next node based on state."""
    if state.get("error"):
        return "error_handler"
    if len(state.get("messages", [])) > 10:
        return END
    return "process"

# Build graph
graph = StateGraph(WorkflowState)

graph.add_node("process", process_node)
graph.add_node("validate", validate_node)
graph.add_node("finalize", finalize_node)
graph.add_node("error_handler", error_handler)

graph.set_entry_point("process")
graph.add_edge("process", "validate")
graph.add_conditional_edges(
    "validate",
    should_continue,
    {
        "process": "process",
        "error_handler": "error_handler",
        END: END
    }
)
graph.add_edge("finalize", END)
graph.add_edge("error_handler", END)

workflow = graph.compile()
```

## Advanced Patterns

### Human-in-the-Loop

```python
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, END

# Create checkpointer for persistence
memory = MemorySaver()

def get_approval(state: WorkflowState) -> WorkflowState:
    """Node that requires human approval."""
    return {"messages": ["Waiting for approval..."]}

def execute_action(state: WorkflowState) -> WorkflowState:
    """Execute after approval."""
    return {"output": "Action executed", "messages": ["Done"]}

# Build graph with interrupt
graph = StateGraph(WorkflowState)
graph.add_node("get_approval", get_approval)
graph.add_node("execute", execute_action)

graph.set_entry_point("get_approval")
graph.add_edge("get_approval", "execute")
graph.add_edge("execute", END)

# Compile with interrupt before execute
workflow = graph.compile(
    checkpointer=memory,
    interrupt_before=["execute"]
)

# First run - stops at interrupt
config = {"configurable": {"thread_id": "1"}}
result = workflow.invoke({"input": "Do something"}, config)

# Resume after approval
result = workflow.invoke(None, config)  # Continues from checkpoint
```

### Subgraphs

```python
from langgraph.graph import StateGraph

# Define subgraph
def create_research_subgraph():
    graph = StateGraph(WorkflowState)
    graph.add_node("search", search_node)
    graph.add_node("analyze", analyze_node)
    graph.set_entry_point("search")
    graph.add_edge("search", "analyze")
    return graph.compile()

research_subgraph = create_research_subgraph()

# Use in main graph
main = StateGraph(WorkflowState)
main.add_node("research", research_subgraph)
main.add_node("synthesize", synthesize_node)

main.set_entry_point("research")
main.add_edge("research", "synthesize")
main.add_edge("synthesize", END)

main_workflow = main.compile()
```

### Parallel Execution

```python
from langgraph.graph import StateGraph
from typing import TypedDict

class ParallelState(TypedDict):
    input: str
    result_a: str
    result_b: str
    result_c: str
    final: str

def task_a(state: ParallelState) -> ParallelState:
    return {"result_a": f"A processed: {state['input']}"}

def task_b(state: ParallelState) -> ParallelState:
    return {"result_b": f"B processed: {state['input']}"}

def task_c(state: ParallelState) -> ParallelState:
    return {"result_c": f"C processed: {state['input']}"}

def combine(state: ParallelState) -> ParallelState:
    combined = f"{state['result_a']}, {state['result_b']}, {state['result_c']}"
    return {"final": combined}

# Build graph with parallel nodes
graph = StateGraph(ParallelState)
graph.add_node("task_a", task_a)
graph.add_node("task_b", task_b)
graph.add_node("task_c", task_c)
graph.add_node("combine", combine)

# All three tasks run in parallel
graph.set_entry_point("task_a")
graph.set_entry_point("task_b")
graph.set_entry_point("task_c")

# Wait for all to complete before combining
graph.add_edge("task_a", "combine")
graph.add_edge("task_b", "combine")
graph.add_edge("task_c", "combine")
graph.add_edge("combine", END)

parallel_workflow = graph.compile()
```

## Streaming

### Basic Streaming

```python
from langgraph.graph import StateGraph

# Stream node outputs
for state in workflow.stream({"input": "Hello"}):
    print(f"Node: {list(state.keys())[0]}")
    print(f"Output: {list(state.values())[0]}")

# Stream with mode
for chunk in workflow.stream(
    {"input": "Hello"},
    stream_mode="values"  # or "updates", "debug"
):
    print(chunk)
```

### Event Streaming

```python
# Stream individual events
for event in workflow.stream(
    {"input": "Hello"},
    stream_mode="events"
):
    if event["event"] == "on_chain_start":
        print(f"Starting: {event['name']}")
    elif event["event"] == "on_chain_end":
        print(f"Completed: {event['name']}")
```

## Error Handling

### Exception Handling in Graphs

```python
from langgraph.graph import StateGraph, END

class SafeState(TypedDict):
    input: str
    output: str
    error: str | None

def safe_node(state: SafeState) -> SafeState:
    try:
        result = risky_operation(state["input"])
        return {"output": result}
    except Exception as e:
        return {"error": str(e)}

def error_handler(state: SafeState) -> SafeState:
    """Handle errors gracefully."""
    return {"output": f"Error occurred: {state['error']}"}

def route_on_error(state: SafeState) -> str:
    if state.get("error"):
        return "error_handler"
    return "next_node"

graph = StateGraph(SafeState)
graph.add_node("risky", safe_node)
graph.add_node("error_handler", error_handler)
graph.add_node("next_node", next_node)

graph.add_conditional_edges("risky", route_on_error)
```

## Best Practices

### 1. State Management

```python
# Good: Use TypedDict for type safety
class MyState(TypedDict):
    input: str
    output: str

# Good: Use Annotated for accumulation
from typing import Annotated
import operator

class MyState(TypedDict):
    messages: Annotated[List[str], operator.add]

# Bad: Use plain dict
state = {}  # No type safety
```

### 2. Node Design

```python
# Good: Pure functions that return partial state
def my_node(state: MyState) -> MyState:
    result = process(state["input"])
    return {"output": result}

# Bad: Mutate state directly
def my_node(state: MyState) -> MyState:
    state["output"] = process(state["input"])  # Don't do this
    return state
```

### 3. Checkpointing

```python
from langgraph.checkpoint.memory import MemorySaver

# Always use checkpointer for production workflows
memory = MemorySaver()
workflow = graph.compile(checkpointer=memory)

# Use thread_id for session management
config = {"configurable": {"thread_id": "user-123"}}
result = workflow.invoke({"input": "Hello"}, config)
```

### 4. Debugging

```python
# Enable debug mode for development
for chunk in workflow.stream(
    {"input": "Hello"},
    stream_mode="debug"
):
    print(chunk)

# Use LangSmith for production monitoring
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "ls__..."
```

### 5. Testing Workflows

```python
import pytest

def test_workflow_happy_path():
    """Test successful workflow execution."""
    result = workflow.invoke({"input": "test"})
    assert result["output"] is not None
    assert result.get("error") is None

def test_workflow_error_handling():
    """Test error path."""
    result = workflow.invoke({"input": "trigger_error"})
    assert result.get("error") is not None

@pytest.mark.asyncio
async def test_workflow_streaming():
    """Test streaming mode."""
    chunks = []
    async for chunk in workflow.astream({"input": "test"}):
        chunks.append(chunk)
    assert len(chunks) > 0
```

## Performance Optimization

### Latency Reduction

```python
# 1. Use parallel nodes where possible
# 2. Cache expensive operations
from functools import lru_cache

@lru_cache(maxsize=100)
def expensive_operation(input: str) -> str:
    # Cached result
    return process(input)

# 3. Use streaming for perceived speed
for chunk in workflow.stream({"input": "Hello"}):
    yield chunk
```

### Cost Optimization

```python
# Use cheaper models for simple tasks
from langchain_openai import ChatOpenAI

cheap_model = ChatOpenAI(model="gpt-4o-mini")
expensive_model = ChatOpenAI(model="gpt-4o")

def smart_route(state: WorkflowState) -> str:
    if is_simple_task(state["input"]):
        return "cheap_node"
    return "expensive_node"
```

---

*Part of faion-langchain-skill v1.0*
*See also: [langchain-chains.md](langchain-chains.md), [langchain-agents-architectures.md](langchain-agents-architectures.md), [langchain-agents-multi-agent.md](langchain-agents-multi-agent.md), [langchain-memory.md](langchain-memory.md)*
## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Implement langchain-workflows pattern | haiku | Straightforward implementation |
| Review langchain-workflows implementation | sonnet | Requires code analysis |
| Optimize langchain-workflows design | opus | Complex trade-offs |

