# Agent Integration — LangChain Multi-Agent Systems

## When to use
- A single agent cannot handle all required specializations — routing to domain-specific agents (researcher, coder, writer) is cleaner than one overloaded agent
- You need consensus-driven decision making where multiple agent perspectives improve output quality (debate pattern)
- The organization of work maps to teams — one team does research, another does implementation, a coordinator routes between them (hierarchical pattern)
- You want to unit-test agent logic in isolation — multi-agent decomposition makes each agent's responsibility narrow and testable with mocked LLM calls
- Supervisor routing allows dynamic task allocation without hard-coded logic in the orchestrator

## When NOT to use
- The task is linear with no branching — a single LangGraph workflow or LCEL chain is simpler and cheaper
- Agents need to share complex state that changes across turns — tight coupling between agents through shared mutable state creates race conditions
- Latency is critical — each supervisor routing call adds an LLM invocation; for time-sensitive tasks, static routing is faster
- The team size is small and there's no domain specialization benefit — multi-agent overhead is not justified for homogeneous tasks
- You need guaranteed execution order — supervisor routing is LLM-driven and non-deterministic

## Where it fails / limitations
- Supervisor routing via natural language is non-deterministic — the same query can route to different agents across runs; not suitable for auditable pipelines
- Debate pattern convergence is not guaranteed — the `round >= 5` hard stop may terminate with no consensus, returning empty output
- Hierarchical team subgraphs require compatible state schemas — mismatched TypedDict fields between parent and subgraph cause silent state loss
- Mock-based unit tests for agents verify logic flow but cannot catch prompt quality issues — integration tests with real LLM calls are required
- `supervisor` node calls the model once per routing decision; high-volume systems that route thousands of requests accumulate significant supervisor LLM costs
- Debate pattern with `enforce_consistency` in judge evaluation doubles judge LLM calls per round

## Agentic workflow
The orchestrating agent dispatches tasks to a compiled LangGraph multi-agent system by providing an initial state dict and a thread_id. The supervisor node routes to specialists; specialist nodes run independently and return partial state updates; results accumulate in the shared state. For Claude-based multi-agent systems, each specialist agent can be a separate Claude API call with a specialized system prompt, routed by a lightweight supervisor that uses structured output to return the specialist name. Evaluation of multi-agent output requires checking both individual specialist outputs and the final synthesized result.

### Recommended subagents
- `faion-autonomous-agent-builder-agent` — scaffolds LangGraph multi-agent systems from a task description; generates supervisor + specialist nodes
- General supervisor subagent — routes incoming tasks to registered specialist agents by name; returns routing decision as structured JSON for auditability

### Prompt pattern
```xml
<system>
You are a supervisor agent. Route the following task to exactly one specialist:
- researcher: information gathering, fact-checking, web search tasks
- coder: code generation, debugging, refactoring tasks
- writer: content creation, editing, summarization tasks

Respond with JSON only: {"agent": "<name>", "reason": "<one sentence>"}
</system>
<human>Task: {task}</human>
```

```xml
<system>
You are a debate judge. Evaluate whether consensus has been reached.
Topic: {topic}
Arguments so far: {arguments}

If consensus: {"consensus": true, "summary": "<summary>"}
If no consensus: {"consensus": false, "summary": null}
</system>
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `langgraph` | Multi-agent state machine framework | `pip install langgraph` |
| `langgraph-cli` | Local dev server + graph visualization | `pip install langgraph-cli` |
| `langsmith` | Trace per-agent step execution | `pip install langsmith` / https://smith.langchain.com |
| `pytest` | Unit + integration testing for agent logic | `pip install pytest pytest-asyncio` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| LangSmith | SaaS | Yes | Per-node traces; shows which specialist handled each turn |
| LangGraph Cloud | SaaS | Yes | Managed stateful multi-agent runtime with persistence |
| LangChain Hub | SaaS | Yes | Version-controlled specialist prompts pulled at runtime |
| Redis | OSS | Yes | Checkpoint backend for multi-agent session state |
| PostgreSQL | OSS | Yes | Production-grade checkpoint persistence |

## Templates & scripts
See `templates.md` for full multi-agent templates. Inline supervisor with structured routing:

```python
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from langchain_anthropic import ChatAnthropic
from pydantic import BaseModel

class Route(BaseModel):
    agent: Literal["researcher", "coder", "writer"]
    reason: str

class TeamState(TypedDict):
    task: str
    route: dict
    result: str

model = ChatAnthropic(model="claude-opus-4-5")
router_model = model.with_structured_output(Route)

def supervisor(state: TeamState) -> TeamState:
    route = router_model.invoke(
        f"Route this task: {state['task']}\n"
        "Options: researcher (facts), coder (code), writer (content)"
    )
    return {"route": route.model_dump()}

def researcher(state: TeamState) -> TeamState:
    resp = model.invoke(f"Research: {state['task']}")
    return {"result": resp.content}

def coder(state: TeamState) -> TeamState:
    resp = model.invoke(f"Write code for: {state['task']}")
    return {"result": resp.content}

def writer(state: TeamState) -> TeamState:
    resp = model.invoke(f"Write content for: {state['task']}")
    return {"result": resp.content}

graph = StateGraph(TeamState)
graph.add_node("supervisor", supervisor)
for name, fn in [("researcher", researcher), ("coder", coder), ("writer", writer)]:
    graph.add_node(name, fn)
    graph.add_edge(name, END)

graph.set_entry_point("supervisor")
graph.add_conditional_edges(
    "supervisor",
    lambda s: s["route"]["agent"],
    {"researcher": "researcher", "coder": "coder", "writer": "writer"}
)

team = graph.compile()
```

## Best practices
- Use `with_structured_output(Route)` for supervisor routing — eliminates string parsing errors and makes routing deterministic per model call
- Log supervisor routing decisions to LangSmith with metadata tags — this creates an audit trail and reveals routing patterns over time
- Write specialist nodes as pure Python functions testable without LLM — mock the model call and verify state transformation logic
- In debate patterns, set a hard round limit (5) AND a consensus threshold — debate without both constraints loops or produces low-quality forced consensus
- For hierarchical teams, compile each team subgraph independently and test it before composing in the parent graph
- Use `pytest.mark.integration` to separate unit tests (mocked LLM) from integration tests (real LLM) — CI should run only unit tests; integration tests run on-demand
- Design specialist prompts to return structured output matching the state schema — free-form text from specialists requires an additional parsing step

## AI-agent gotchas
- Supervisor routing via natural language is susceptible to prompt injection — if user input is passed directly into the supervisor prompt, a malicious task description can manipulate routing
- Hierarchical subgraph state schemas must be a strict superset of parent state — missing fields in subgraph TypedDict cause KeyError at runtime when parent reads subgraph output
- Debate pattern agents that reference their own previous arguments create self-reinforcing loops — include other agent's argument in context, not own history, to encourage genuine divergence
- `pytest.mock.patch("langchain_openai.ChatOpenAI")` patches the class import; if the agent uses `langchain_anthropic.ChatAnthropic`, a different patch path is required — verify the import path being mocked
- Multi-agent systems with shared `MemorySaver` checkpointer and different `thread_id`s are isolated — cross-agent state sharing requires explicit state passing through the graph, not through the checkpointer
- Adding more specialists does not improve task quality linearly — each specialist adds a routing decision cost and potential misrouting; keep the specialist count to 3-5 with clear, non-overlapping domains

## References
- https://langchain-ai.github.io/langgraph/tutorials/multi_agent/multi-agent-collaboration/
- https://langchain-ai.github.io/langgraph/tutorials/multi_agent/agent_supervisor/
- https://langchain-ai.github.io/langgraph/tutorials/multi_agent/hierarchical_agent_teams/
- https://python.langchain.com/docs/how_to/agent_executor/
- LangGraph multi-agent examples: https://github.com/langchain-ai/langgraph/tree/main/examples/multi_agent
