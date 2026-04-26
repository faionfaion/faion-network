# Agent Integration — Multi-Agent Design Patterns

## When to use
- A single agent context window is insufficient for the full task — break into specialized workers
- Tasks have parallelizable subtasks (research + writing + validation can run concurrently)
- Domain expertise needs to be isolated — a billing agent should not have access to CRM tools
- Reliability requires redundancy — parallel agents can cross-check each other's outputs
- Enterprise workflows map naturally to organizational units (teams, departments, roles)

## When NOT to use
- Simple single-step tasks — multi-agent adds coordination overhead with no benefit
- Latency is critical (< 2s) — agent-to-agent round trips add 500ms–2s each
- The problem is not well-decomposed yet — build a working single agent first, then extract workers
- Token budget is constrained — multi-agent systems use significantly more tokens per task
- The team does not have infrastructure to run concurrent agent processes reliably

## Where it fails / limitations
- Supervisor pattern is a single point of failure — if the supervisor LLM call fails, the entire workflow halts
- Hierarchical pattern has "middle management" latency: each coordination layer adds 500ms+ of LLM call overhead
- Sequential pattern has no fault isolation — a failure at stage N blocks stages N+1 through end
- Peer-to-peer pattern is hard to debug: no central trace of message flow; requires distributed tracing
- State sharing between agents via files/queues introduces race conditions if not properly serialized
- LLM routing in supervisor agents is probabilistic — the supervisor can route to the wrong worker for ambiguous inputs

## Agentic workflow
Choose a pattern based on the task structure, then implement it using LangGraph (state machines), CrewAI (role-based), or Google ADK (native multi-agent primitives). Define agent roles before writing prompts — the role determines the tool set and context the agent receives. Use typed shared state (Pydantic models) to pass structured data between agents rather than raw text. Always instrument with a tracer (LangSmith, Langfuse) from day one.

### Recommended subagents
- `faion-sdd-executor-agent` — for implementing a multi-agent architecture as a tracked SDD feature
- `faion-brainstorm` skill — for choosing the right pattern before implementation
- General Claude subagent — as worker agent in supervisor/hierarchical patterns

### Prompt pattern
Supervisor routing prompt:
```xml
<supervisor>
  <available-agents>
    <agent name="research-agent">Finds and summarizes information from the web and documents</agent>
    <agent name="code-agent">Writes and reviews Python code</agent>
    <agent name="validation-agent">Checks facts and detects hallucinations</agent>
  </available-agents>
  <task>{user_request}</task>
  <instruction>Select the most appropriate agent. Return JSON: {"agent": "name", "reason": "..."}</instruction>
</supervisor>
```

Sequential pipeline state:
```python
from pydantic import BaseModel
from typing import Optional

class PipelineState(BaseModel):
    raw_input: str
    parsed: Optional[dict] = None
    enriched: Optional[dict] = None
    validated: Optional[bool] = None
    output: Optional[str] = None
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `langgraph` | Graph-based multi-agent state machines | `pip install langgraph` · langchain-ai.github.io/langgraph |
| `crewai` | Role-based crew with manager/worker model | `pip install crewai` · docs.crewai.com |
| `autogen` | Microsoft multi-agent conversation framework | `pip install pyautogen` · microsoft.github.io/autogen |
| `google-adk` | Google Agent Development Kit | `pip install google-adk` · google.github.io/adk-docs |
| `langfuse` | Multi-agent tracing and observability | `pip install langfuse` · langfuse.com |
| `anthropic` | Claude SDK — Claude subagents via API | `pip install anthropic` · docs.anthropic.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| LangSmith | SaaS | Yes — SDK | Tracing, evaluation, monitoring for LangGraph pipelines |
| Langfuse | SaaS/OSS | Yes — SDK | Open-source LangSmith alternative; self-hostable |
| Prefect | SaaS/OSS | Yes — Python | Orchestrating agent workflows as Prefect flows |
| Temporal | OSS | Yes — SDK | Durable execution for long-running multi-agent workflows |
| Google ADK Cloud | SaaS | Yes — ADK | Managed agent runtime on GCP |
| CrewAI Enterprise | SaaS | Yes — API | Managed crew deployment |

## Templates & scripts
See `templates.md` for LangGraph supervisor graph scaffold and CrewAI crew definition template.

Inline: minimal LangGraph supervisor (< 50 lines):

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Literal

class State(TypedDict):
    task: str
    agent: str
    result: str

def supervisor(state: State) -> dict:
    # LLM call to route
    agent = route_with_llm(state["task"])
    return {"agent": agent}

def research_agent(state: State) -> dict:
    result = run_research(state["task"])
    return {"result": result}

def code_agent(state: State) -> dict:
    result = run_code_generation(state["task"])
    return {"result": result}

def router(state: State) -> Literal["research", "code", "__end__"]:
    return state.get("agent", "__end__")

graph = StateGraph(State)
graph.add_node("supervisor", supervisor)
graph.add_node("research", research_agent)
graph.add_node("code", code_agent)
graph.set_entry_point("supervisor")
graph.add_conditional_edges("supervisor", router)
graph.add_edge("research", END)
graph.add_edge("code", END)
app = graph.compile()
```

## Best practices
- Choose the simplest pattern that solves the problem: sequential → supervisor → hierarchical; do not start with peer-to-peer
- Define tool permissions per agent at design time — a research agent should not have write access to production databases
- Use Pydantic models for all inter-agent messages; raw string passing causes downstream parsing failures
- Implement a timeout at each agent call — a stuck worker should not block the entire workflow indefinitely
- Add a fallback path: if the primary agent fails, the supervisor should either retry or escalate to a human-in-the-loop checkpoint
- Log the complete agent trace (inputs, outputs, tool calls, latency) for every run — debugging multi-agent failures without traces is nearly impossible
- For Generator-Critic pattern, always run at least 2 critique passes — first critique catches obvious errors, second catches subtler issues

## AI-agent gotchas
- Infinite loops: a supervisor can route to agent A, which routes back to supervisor, which routes to A again — add a max_steps guard
- Token explosion: multi-agent conversations accumulate history; each agent sending its full conversation history to the next compounds token usage — summarize or trim between steps
- Tool access leakage: in frameworks like AutoGen where agents share a conversation, one agent can see tool results intended for another — use explicit message routing
- LLM routing is not deterministic: the same supervisor prompt may route differently on retries — design for idempotency at each worker
- Human-in-the-loop checkpoints must be explicit in the graph, not added as an afterthought — retrofitting approval steps into LangGraph requires graph restructuring
- Parallel fan-out agents writing to shared state simultaneously will produce race conditions — use merge nodes with explicit conflict resolution

## References
- https://langchain-ai.github.io/langgraph/tutorials/multi_agent/hierarchical_agent_teams/
- https://google.github.io/adk-docs/agents/multi-agents/
- https://docs.crewai.com/
- https://microsoft.github.io/autogen/
- https://docs.databricks.com/aws/en/generative-ai/guide/agent-system-design-patterns
- https://arxiv.org/abs/2504.00587 (AgentNet NeurIPS 2025)
- https://arxiv.org/html/2501.06322v1 (Multi-Agent Collaboration Survey)
