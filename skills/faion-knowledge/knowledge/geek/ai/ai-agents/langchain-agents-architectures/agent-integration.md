# Agent Integration — LangChain Agent Architectures

## When to use
- Building tool-using agents with verifiable, step-by-step reasoning (ReAct via `create_react_agent`)
- Multi-step research or data-processing tasks where upfront planning reduces error propagation (Plan-and-Execute)
- Complex reasoning problems with solution uncertainty where backtracking improves quality (LATS)
- Integrating heterogeneous tools (web search, calculators, APIs, databases) behind a unified agent interface
- Replacing custom agent loops with battle-tested LangGraph state machines that handle errors, checkpoints, and retries

## When NOT to use
- Single-tool, single-step retrieval tasks — plain LLM call is simpler and faster
- Hard latency requirements (<1 s): ReAct + LATS add multiple round-trips
- Cases where the complete solution path is already known — use a deterministic pipeline, not an agent
- Tasks where tool schemas cannot be written (e.g. the agent must call arbitrary undocumented APIs)
- Contexts where LangChain's verbose abstraction layers increase debugging cost more than they reduce development cost

## Where it fails / limitations
- **ReAct tool hallucination**: model calls tools not in the schema or calls them with invalid argument types; `tool_choice="auto"` does not guarantee valid calls
- **Plan-and-Execute plan staleness**: the upfront plan does not account for intermediate tool results; a failed step 2 leaves steps 3-N invalid
- **LATS cost**: tree search with 3 candidates × 5 evaluation rounds = 15+ LLM calls per problem; cost scales poorly with search depth
- **Tool error propagation**: unless `handle_tool_error=True` is set, a single tool failure raises an exception that aborts the agent run
- **Context window growth**: long ReAct runs with many tool calls fill the context window; LangChain does not auto-truncate by default
- **LATS scoring reliability**: LLM-based scoring of candidate thoughts has low inter-rater reliability; the "best path" selected may not be objectively best
- **LangGraph schema rigidity**: changing `PlanExecuteState` mid-project requires migrating all checkpointed state; plan the schema carefully upfront

## Agentic workflow
A Claude subagent uses `create_react_agent` for standard tool-using tasks and a custom `StateGraph` for Plan-and-Execute or LATS patterns. The subagent's system prompt defines its role and available tools; LangGraph manages state transitions. For multi-agent use, individual agents run as nodes in a parent `StateGraph`, passing typed state between them. Tool definitions use the `@tool` decorator with Pydantic schemas for validated inputs.

### Recommended subagents
- `react-agent` — `create_react_agent` with web search, calculator, and code execution tools; uses Sonnet
- `planner-node` — Plan-and-Execute: generates structured step list from goal; uses Opus
- `executor-node` — Plan-and-Execute: executes one step with tool access; uses Sonnet
- `synthesizer-node` — Plan-and-Execute: combines all step results into final answer; uses Sonnet
- `lats-evaluator` — LATS: scores candidate thoughts (0-10) against a rubric; uses Haiku for cost efficiency

### Prompt pattern
ReAct tool definition:
```python
@tool
def search(query: str) -> str:
    """Search the web for current information about a topic.
    Use for: facts, recent events, company info, pricing.
    Do NOT use for: math, code execution, structured data.
    """
    return web_search(query)
```

Plan-and-Execute planner:
```xml
<task>{{goal}}</task>
<available_tools>{{tool_descriptions}}</available_tools>
<instruction>
Create a minimal step-by-step plan to achieve the goal.
Each step must be executable by one of the available tools.
Return JSON: {"steps": ["step 1 description", "step 2 description", ...]}
Do not include steps that cannot be executed by the available tools.
</instruction>
```

LATS evaluation:
```xml
<problem>{{problem}}</problem>
<candidate>{{thought_or_path}}</candidate>
<instruction>
Rate this approach 0-10. Consider: correctness, efficiency, completeness.
Return JSON: {"score": N, "rationale": "..."}
</instruction>
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `langchain` | `create_react_agent`, tool decorators, `bind_tools` | `pip install langchain` / python.langchain.com |
| `langgraph` | `StateGraph` for Plan-and-Execute and LATS; checkpointing | `pip install langgraph` / langchain-ai.github.io/langgraph |
| `langchain-openai` | `ChatOpenAI` model with tool calling | `pip install langchain-openai` / pypi |
| `langchain-anthropic` | `ChatAnthropic` model with tool calling and extended thinking | `pip install langchain-anthropic` / pypi |
| `langsmith` | Tracing and evaluation of agent runs | `pip install langsmith` / langsmith.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| LangSmith | SaaS | Yes | Traces every ReAct step, tool call, and LATS branch; required for debugging |
| LangGraph Cloud | SaaS | Yes | Managed stateful agent execution; built-in persistence and human-in-loop |
| Tavily Search | SaaS | Yes | Purpose-built search API for agents; cleaner results than SerpAPI for LLM consumption |
| E2B Code Interpreter | SaaS | Yes | Sandboxed Python execution tool for code-writing agents |
| Helicone | SaaS | Yes | Cost and latency tracking per agent architecture type |

## Templates & scripts
See `templates.md` for full ReAct, Plan-and-Execute, and LATS implementations.

Minimal ReAct agent with error handling (≤20 lines):
```python
from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic

model = ChatAnthropic(model="claude-sonnet-4-5")
tools = [search, calculator]  # @tool decorated functions
agent = create_react_agent(model, tools)

def run_agent(task: str) -> str:
    try:
        result = agent.invoke({"messages": [("human", task)]})
        return result["messages"][-1].content
    except Exception as e:
        return f"Agent failed: {e}"
```

## Best practices
- Write tool docstrings as agent-facing prompts, not developer-facing documentation — include when to use, when NOT to use, and expected output format
- Use `handle_tool_error=True` on every tool that can fail; never let a tool exception abort a multi-step run
- For Plan-and-Execute, validate the plan JSON schema before dispatching any execution steps
- In LATS, score with Haiku and expand with Sonnet — this reduces cost by ~70% vs using Sonnet for both
- Always set `max_iterations` on ReAct agents; the default is unbounded in some LangChain versions
- Stream agent events (`agent.stream()`) in production UIs so users see progress rather than waiting for a full result
- Add a `session_id` tag to every LangSmith trace for cross-session cost attribution and debugging

## AI-agent gotchas
- **`create_react_agent` tool names must be unique**: duplicate tool names cause silent routing errors where the wrong tool is called. Always check `{tool.name for tool in tools}` has no duplicates.
- **Plan-and-Execute skips replanning**: if step 2 fails or returns unexpected results, steps 3-N execute on a broken foundation. Add a re-plan gate after each step that checks whether the remaining plan is still valid.
- **LATS backtracking is expensive**: in practice, limit LATS to 2 branches × 3 depth = 6 exploration paths. Full tree search with LLM scoring is rarely justified outside research settings.
- **Tool input validation**: `@tool` with a Pydantic `args_schema` validates inputs before the tool function runs. Without this, malformed LLM outputs (wrong types, missing fields) cause runtime errors deep in the tool function.
- **Human-in-loop at irreversible steps**: for Plan-and-Execute workflows that send emails, write files, or call payment APIs, use LangGraph `interrupt_before` on the executor node. Never execute irreversible actions without an explicit human approval gate.
- **Context window management**: a 20-step Plan-and-Execute run with verbose tool outputs can consume 50k+ tokens. Truncate tool outputs to 2k characters maximum before appending to state.

## References
- LangGraph ReAct prebuilt: https://langchain-ai.github.io/langgraph/reference/prebuilt/#langgraph.prebuilt.chat_agent_executor.create_react_agent
- LangGraph Plan-and-Execute: https://langchain-ai.github.io/langgraph/tutorials/plan-and-execute/plan-and-execute/
- LATS paper: https://arxiv.org/abs/2310.04406
- LangChain tool docs: https://python.langchain.com/docs/modules/tools/
- LangSmith tracing: https://docs.smith.langchain.com/
