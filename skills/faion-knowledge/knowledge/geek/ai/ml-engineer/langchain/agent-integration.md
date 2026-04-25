# Agent Integration — LangChain

## When to use
- Building multi-step AI workflows where each step's output feeds the next (LCEL pipe chains)
- Standard ReAct tool-calling agent with 3-10 tools — `create_react_agent()` covers 80% of use cases
- Complex control flow requiring state machines: human-in-the-loop approval, conditional branching, retry logic (LangGraph)
- Long-running workflows that must survive process restarts — LangGraph checkpointing persists state to disk/DB
- Multi-agent orchestration: Supervisor → Worker patterns with role specialization
- RAG pipelines requiring custom retrieval → reranking → synthesis chains

## When NOT to use
- Single LLM call — use the provider SDK directly (anthropic, openai); LangChain adds 50-200ms overhead
- Document-centric RAG with complex index types — LlamaIndex has better RAG abstractions
- Browser or desktop agents — LangChain's tools don't wrap browser automation well; use Playwright directly
- Simple prompt templates — Python f-strings or Jinja2 avoid the dependency
- High-throughput inference (>100 RPS) — LangChain's Python overhead becomes measurable; use vLLM or direct SDK

## Where it fails / limitations
- LCEL operator (`|`) produces hard-to-debug stack traces when intermediate steps fail; error messages point to internal chain internals, not your code
- `create_react_agent()` has no built-in iteration cap — agents loop indefinitely on ambiguous tasks without custom `stop_sequence` or max_iterations config
- LangGraph state serialization fails silently for custom non-serializable objects in state — always use JSON-serializable types in StateGraph
- LangSmith tracing adds ~30ms latency per chain call — disable in latency-critical paths
- Legacy patterns (LLMChain, AgentExecutor, ConversationChain) are deprecated but still widely documented on Stack Overflow — agents trained on web data will suggest them; use LCEL equivalents
- `with_retry()` on chains does not distinguish transient errors from logic errors — blind retry amplifies costs without fixing root cause

## Agentic workflow
Use `create_react_agent(model, tools, checkpointer=MemorySaver())` for simple agent tasks driven by Claude subagents. For complex workflows, define a LangGraph `StateGraph` where each node is a Claude subagent call with a specific role (planner, executor, critic). Route between nodes with `add_conditional_edges` based on structured output from the previous node. Use `interrupt_before` for human-in-the-loop checkpoints at high-risk action nodes. Chain observability through LangSmith by setting `LANGCHAIN_TRACING_V2=true` — every subagent call is automatically traced with full input/output.

### Recommended subagents
- `chain-builder` — constructs LCEL chain given task description and available tools (use for dynamic chain assembly)
- `langgraph-router` — evaluates current state and returns next node name (conditional edge function)
- `tool-executor` — wraps a ToolNode; handles tool call parsing, execution, error formatting
- `synthesizer` — takes accumulated step results from LangGraph state, produces final user-facing response

### Prompt pattern
```python
# LangGraph node with structured output routing
from langchain_core.prompts import ChatPromptTemplate
from langchain_anthropic import ChatAnthropic
from pydantic import BaseModel

class RouteDecision(BaseModel):
    next_node: str  # "executor" | "critic" | "done"
    reasoning: str

def router_node(state: dict) -> dict:
    model = ChatAnthropic(model="claude-sonnet-4-5")
    chain = (
        ChatPromptTemplate.from_template(
            "Given state: {state}\nDecide next step. Options: executor, critic, done."
        )
        | model.with_structured_output(RouteDecision)
    )
    decision = chain.invoke({"state": state})
    return {"next": decision.next_node}
```

```python
# Minimal LangGraph agent with human interrupt
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()
agent = create_react_agent(model, tools, checkpointer=checkpointer)

# Run with thread for persistence
config = {"configurable": {"thread_id": "session-123"}}
result = agent.invoke({"messages": [("user", task)]}, config=config)
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `langchain-core` | Minimal LCEL + base types | `pip install langchain-core` / https://python.langchain.com/ |
| `langgraph` | State machine agent framework | `pip install langgraph` / https://langchain-ai.github.io/langgraph/ |
| `langchain-anthropic` | Claude integration | `pip install langchain-anthropic` |
| `langchain-openai` | OpenAI integration | `pip install langchain-openai` |
| `langsmith` | Tracing and evaluation | `pip install langsmith` / https://docs.smith.langchain.com/ |
| `langchain-community` | Third-party tool integrations | `pip install langchain-community` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| LangSmith | SaaS | Yes | Native LangChain tracing; dataset management for evaluation; required for production debugging |
| LangGraph Cloud | SaaS | Yes | Managed LangGraph execution with auto-scaling; native interrupt/resume for human-in-loop |
| LangChain Hub | SaaS | Yes | Versioned prompt registry; pull prompts in agent workflows to avoid hardcoding |
| Qdrant | OSS/SaaS | Yes | Best vector store integration for LangChain RAG chains |
| Arize Phoenix | OSS | Yes | Alternative to LangSmith; self-hosted tracing with LangChain callback integration |

## Templates & scripts
See `templates.md` for complete LCEL chain and LangGraph workflow templates.

Minimal LangGraph Supervisor pattern:
```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

class SupervisorState(TypedDict):
    task: str
    results: Annotated[list, operator.add]
    next_worker: str

def supervisor_node(state: SupervisorState) -> SupervisorState:
    # Decide which worker to call next
    decision = llm.invoke(f"Route task '{state['task']}' to: researcher|writer|done")
    return {"next_worker": decision.strip()}

graph = StateGraph(SupervisorState)
graph.add_node("supervisor", supervisor_node)
graph.add_node("researcher", researcher_node)
graph.add_node("writer", writer_node)
graph.add_conditional_edges(
    "supervisor",
    lambda s: s["next_worker"],
    {"researcher": "researcher", "writer": "writer", "done": END},
)
graph.set_entry_point("supervisor")
app = graph.compile()
```

## Best practices
- Use `langchain-core` only (not `langchain`) for production agents — core is stable; full langchain pulls 200+ transitive deps
- Always set `max_iterations` on agents using `RunnableConfig` or graph loop bounds — default is unlimited
- Use `.with_structured_output(PydanticModel)` instead of output parsers — structured output is enforced by the API, not fragile string parsing
- Store LangGraph state as flat JSON-serializable dicts — nested custom objects silently fail serialization in checkpoint backends
- Test chains by invoking each component individually before wiring with `|` — isolates bugs before they compound in full chain traces
- Enable LangSmith from day 1 on new projects; retrofitting observability into existing chains is painful

## AI-agent gotchas
- LangChain callbacks execute synchronously in async chains by default — custom callbacks with blocking I/O will stall the entire chain; use `AsyncCallbackHandler`
- `create_react_agent` internally uses `MessagesState` — adding custom state fields requires a custom graph, not the prebuilt agent
- LCEL `batch()` calls run in thread pool by default; if your tools are not thread-safe, `batch()` causes race conditions — use `abatch()` with async tools
- Tool descriptions are passed verbatim to the LLM — ambiguous or overlapping descriptions cause the agent to select wrong tools without error; test tool routing explicitly
- Human-in-the-loop checkpoint: use LangGraph `interrupt_before=["action_node"]` for nodes that perform irreversible actions (send email, write to DB, call payment API); never rely on agent self-restraint

## References
- LangChain Python docs: https://python.langchain.com/docs/
- LangGraph docs: https://langchain-ai.github.io/langgraph/
- LangSmith docs: https://docs.smith.langchain.com/
- LCEL primitives: https://python.langchain.com/docs/how_to/#langchain-expression-language-lcel
- LangGraph human-in-the-loop: https://langchain-ai.github.io/langgraph/how-tos/human_in_the_loop/
- LangChain Hub: https://smith.langchain.com/hub
