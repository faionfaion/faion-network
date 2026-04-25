# Agent Integration — LangChain Workflows

## When to use
- Building stateful, multi-step pipelines where graph nodes represent distinct processing phases (validate → transform → store)
- Human-in-the-loop approval is required before an irreversible action executes — LangGraph's `interrupt_before` makes this explicit
- The workflow has conditional branching that cannot be expressed as a linear chain (error → retry vs. success → next)
- You need resumable workflows — LangGraph checkpoints allow interruption and continuation across process restarts
- Multiple async tasks can run in parallel (fan-out) and must converge before proceeding (fan-in)

## When NOT to use
- Simple A → B → C without branching — plain LCEL chain is lighter and easier to debug
- The task is stateless single-shot LLM generation — LangGraph state management adds overhead with no benefit
- You need real-time streaming of partial tokens to the UI — LangGraph streaming works but LCEL chain streaming has less latency overhead
- The graph topology changes dynamically at runtime — LangGraph graph structure is fixed at compile time
- Team is not familiar with TypedDict state and functional node design — the learning curve produces buggy implicit state mutations

## Where it fails / limitations
- `MemorySaver` stores state in-process memory; it does not survive process restarts — use `AsyncPostgresSaver` or `RedisSaver` for production persistence
- Parallel nodes in LangGraph are not true async by default; they execute sequentially unless the underlying node functions are async and the graph is invoked with `ainvoke()`
- `interrupt_before` checkpointing requires `thread_id` in config — forgetting it means no checkpoint is saved and resumption fails silently
- `StateGraph` with many nodes and complex edges becomes difficult to visualize and debug without Mermaid diagram export
- LangGraph version ≥ 0.2 introduced breaking changes in checkpointer API — `MemorySaver` import path changed
- Error handling inside nodes does not propagate as graph-level exceptions unless explicitly caught and routed via conditional edges

## Agentic workflow
An agent uses LangGraph workflows to represent tasks with well-defined stages and decision points. The orchestrating agent compiles the graph once and invokes it per task, passing a `thread_id` for session isolation. For long-running workflows, a monitoring subagent polls the checkpoint state to report progress, and a recovery subagent resumes from the last checkpoint if the process was interrupted. Human approval gates are modeled as `interrupt_before` nodes where the orchestrator pauses and waits for an external signal.

### Recommended subagents
- General workflow executor subagent — receives a compiled graph and initial state, runs it with a thread_id, returns final state
- Human-in-the-loop coordinator — monitors interrupted checkpoints, sends approval requests, resumes on confirmation

### Prompt pattern
```
You are a workflow execution agent. Run the following LangGraph workflow:
  graph: {workflow_name}
  initial_state: {state_json}
  thread_id: "{thread_id}"

Report state after each node. If workflow hits interrupt_before=["execute"],
pause and output: {"status": "awaiting_approval", "state": <current_state>}.
```

```
Resume workflow "{thread_id}" after human approval.
Current state: {state_json}
Call: workflow.invoke(None, config={"configurable": {"thread_id": "{thread_id}"}})
Return the final state.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `langgraph` | Core stateful graph framework | `pip install langgraph` / https://langchain-ai.github.io/langgraph |
| `langgraph-cli` | Local dev server + graph visualization | `pip install langgraph-cli` / https://github.com/langchain-ai/langgraph |
| `langsmith` | Trace workflow node-by-node execution | `pip install langsmith` / https://smith.langchain.com |
| `langgraph-checkpoint-postgres` | Production PostgreSQL checkpoint backend | `pip install langgraph-checkpoint-postgres` |
| `langgraph-checkpoint-redis` | Redis checkpoint backend | `pip install langgraph-checkpoint-redis` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| LangSmith | SaaS | Yes | Per-node traces with input/output at each graph step |
| LangGraph Cloud | SaaS | Yes | Managed stateful agent runtime with persistence |
| PostgreSQL | OSS | Yes | Production checkpointing via `AsyncPostgresSaver` |
| Redis | OSS | Yes | Fast checkpoint backend for high-throughput workflows |
| Temporal | OSS | Yes | Alternative durable workflow engine; use if LangGraph scale limits hit |
| Prefect | OSS/SaaS | Partial | Task orchestration; does not integrate natively with LangGraph state |

## Templates & scripts
See `templates.md` for workflow templates. Inline workflow with human-in-the-loop:

```python
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

class ActionState(TypedDict):
    input: str
    plan: str
    approved: bool
    result: str

def planner(state: ActionState) -> ActionState:
    return {"plan": f"Plan for: {state['input']}"}

def executor(state: ActionState) -> ActionState:
    return {"result": f"Executed: {state['plan']}"}

graph = StateGraph(ActionState)
graph.add_node("plan", planner)
graph.add_node("execute", executor)
graph.set_entry_point("plan")
graph.add_edge("plan", "execute")
graph.add_edge("execute", END)

memory = MemorySaver()
workflow = graph.compile(checkpointer=memory, interrupt_before=["execute"])

cfg = {"configurable": {"thread_id": "task-001"}}
# Run to interrupt point
state = workflow.invoke({"input": "Deploy to production", "approved": False}, cfg)
print(f"Plan: {state['plan']} — awaiting approval")
# After human approval:
final = workflow.invoke(None, cfg)
print(f"Result: {final['result']}")
```

## Best practices
- Model state with `TypedDict` and use `Annotated[List, operator.add]` only for fields that genuinely accumulate (message history, log entries) — using add-reducer on non-list fields causes subtle bugs
- Write all node functions as pure functions that return partial state dicts, not the full state — this makes each node testable in isolation
- Always compile the graph with a `checkpointer` even in development; catching checkpoint-related bugs early prevents production incidents
- Use `stream_mode="updates"` for debugging — it shows which node produced each state delta, not just the final state
- Design error routing explicitly: every node that can fail should have a conditional edge to an `error_handler` node; don't rely on Python exceptions propagating through the graph
- For parallel fan-out nodes, use `async` node functions and call `await workflow.ainvoke()` — synchronous parallel execution does not actually parallelize
- Export Mermaid diagrams with `workflow.get_graph().draw_mermaid()` at build time and commit them alongside the graph code as documentation

## AI-agent gotchas
- Subgraphs embedded in a parent graph share state schema by default — mismatched TypedDict fields between parent and subgraph cause silent state loss
- `interrupt_before` nodes require the workflow to be invoked a second time with `None` as input and the same `thread_id` — passing a new state dict on resumption overwrites the checkpoint
- LangGraph's `stream()` with `stream_mode="events"` returns a generator; consuming it multiple times raises `StopIteration` — collect to a list if you need to inspect twice
- Conditional edge routing functions receive the full current state — accessing a field that hasn't been set yet raises `KeyError`; use `.get()` with defaults for optional fields
- `MemorySaver` is not thread-safe for concurrent workflow instances with different `thread_id`s if using a single `MemorySaver` object — create one per event loop or use `AsyncPostgresSaver`
- A workflow node that raises an unhandled exception halts the graph and loses the checkpoint — wrap risky operations in try/except and encode error state in the TypedDict

## References
- https://langchain-ai.github.io/langgraph/
- https://langchain-ai.github.io/langgraph/concepts/
- https://langchain-ai.github.io/langgraph/how-tos/human_in_the_loop/
- https://github.com/langchain-ai/langgraph/tree/main/examples
- LangGraph persistence: https://langchain-ai.github.io/langgraph/how-tos/persistence/
