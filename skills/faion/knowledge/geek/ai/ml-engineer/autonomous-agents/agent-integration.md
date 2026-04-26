# Agent Integration — Autonomous Agents

## When to use
- Task requires dynamic tool selection across multiple steps with branching based on intermediate results
- Workflow involves research + synthesis + action that cannot be scripted in advance
- Code generation and execution loops where the agent must test and fix iteratively
- Multi-source data gathering where the number of sources is unknown upfront
- Automation of knowledge work: writing, classification, extraction across variable-length inputs

## When NOT to use
- Task is deterministic and mappable to a fixed pipeline — use a DAG, not an agent
- Real-time response (<500ms) is required — autonomous loop latency is incompatible
- Actions are irreversible (send email, delete records, charge cards) without human approval in the loop
- Cost budget is fixed and tight — ReAct loops can expand token usage 5-20x vs a single call
- Task requires guaranteed sequential ordering — plan-and-execute is safer than open-ended ReAct

## Where it fails / limitations
- Infinite loops: agent gets stuck retrying a failing tool call; iteration limit is mandatory
- Tool hallucination: LLM fabricates plausible tool arguments that are subtly wrong (e.g., wrong API field names)
- Context overflow: long-running agents exceed context window — without summarization, they fail silently or loop
- Error propagation: a wrong intermediate result cascades through subsequent steps without self-detection
- Cost explosion: unbounded tool calls on expensive APIs (image gen, video gen) can burn budget in minutes
- Framework lock-in: LangGraph state schemas, CrewAI role configs are not portable across frameworks

## Agentic workflow
Claude subagents implement ReAct or Plan-and-Execute depending on task governance requirements. For exploratory tasks, a subagent receives a goal and a tool manifest, iterates autonomously (think → act → observe → repeat), and returns a structured result. For high-stakes operations, the orchestrator generates a plan first, presents it for review, then dispatches execution agents per plan step. All tool calls are logged. Irreversible actions require an explicit human approval step before dispatch.

### Recommended subagents
- `faion-sdd-executor-agent` — plan-and-execute pattern for SDD task sequences
- `nero-sdd-executor-agent` — same for NERO-internal workflows

### Prompt pattern
```
# System (ReAct agent)
You are an autonomous agent. You have access to these tools: {tool_list}.
Think step by step. After each action, observe the result and decide the next step.
Stop when you have a complete answer. Maximum {max_iterations} iterations.
Never call a tool more than 3 times with the same arguments.

# User
Goal: {goal}
Constraints: {constraints}
```

```python
# Minimal LangGraph ReAct agent skeleton
from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool

@tool
def search_web(query: str) -> str:
    """Search the web for current information."""
    # implement with SearXNG or Brave Search
    ...

llm = ChatAnthropic(model="claude-opus-4-5")
agent = create_react_agent(llm, tools=[search_web])

result = agent.invoke({"messages": [("user", "Research X and summarize in 3 bullets")]})
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `langgraph` | Production agent state machines; persistence | `pip install langgraph` / langchain-ai.github.io/langgraph |
| `langchain` | Tool abstractions, ReAct; pairs with LangGraph | `pip install langchain` / python.langchain.com |
| `crewai` | Role-based multi-agent teams | `pip install crewai` / crewai.com |
| `autogen` | Conversational multi-agent; Microsoft Research | `pip install pyautogen` / microsoft.github.io/autogen |
| `dspy` | Programmatic prompt optimization for agents | `pip install dspy-ai` / dspy.ai |
| `smolagents` | HuggingFace lightweight agent framework | `pip install smolagents` / github.com/huggingface/smolagents |
| `controlflow` | Pythonic agent orchestration (Prefect-style) | `pip install controlflow` / controlflow.ai |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| LangSmith | SaaS | Yes | Trace agent runs, debug tool calls, eval on replays |
| Langfuse | OSS/SaaS | Yes | Self-hosted tracing; agent-submittable spans via SDK |
| E2B | SaaS | Yes | Sandboxed code execution for agents; REST API |
| Browserless | SaaS | Yes | Headless browser for web scraping agents |
| SearXNG (self-hosted) | OSS | Yes | Privacy-preserving web search tool for agents |
| Composio | SaaS | Yes | 250+ pre-built tool integrations (GitHub, Slack, etc.) |
| Temporal | OSS | Yes | Durable workflow execution; agent crash recovery |

## Templates & scripts
See `templates.md` for full ReAct and Plan-and-Execute templates.

Iteration guard (prevents infinite loops):

```python
class IterationGuard:
    def __init__(self, max_iter: int = 20, max_cost_usd: float = 1.0):
        self.count = 0
        self.max_iter = max_iter
        self.cost = 0.0
        self.max_cost = max_cost_usd

    def check(self, tokens_used: int, cost_per_1k: float = 0.003) -> None:
        self.count += 1
        self.cost += (tokens_used / 1000) * cost_per_1k
        if self.count >= self.max_iter:
            raise RuntimeError(f"Iteration limit {self.max_iter} reached")
        if self.cost >= self.max_cost:
            raise RuntimeError(f"Cost limit ${self.max_cost:.2f} reached (spent ${self.cost:.2f})")
```

## Best practices
- Set hard iteration limits (20-50 steps) and per-run cost caps before any agent loop
- Design tools with explicit error returns, not exceptions — agents handle text errors better than stack traces
- Use Plan-and-Execute for high-stakes operations: show the plan, get approval, then execute
- Log every tool call with arguments and results — essential for debugging non-deterministic failures
- Summarize conversation history every N steps to prevent context overflow in long-running agents
- Write tool descriptions as if writing for a person unfamiliar with your codebase — clarity reduces hallucination
- Prefer narrow, composable tools over broad "do everything" tools

## AI-agent gotchas
- Tool argument hallucination is the most common failure; add JSON schema validation on every tool input
- Agents calling themselves recursively (via tool) is possible and catastrophic — guard with depth counter
- LangGraph state machines can deadlock if a node raises an exception without a fallback edge; always add error edges
- CrewAI agent "memory" is not persistent across runs by default; configure vector store for cross-session memory
- Human-in-loop approval is required before: sending external messages, making financial transactions, deleting data
- Never give agents write access to production databases without an explicit rollback plan and approval gate

## References
- https://arxiv.org/abs/2210.03629 (ReAct paper)
- https://arxiv.org/abs/2303.11366 (Reflexion paper)
- https://langchain-ai.github.io/langgraph/
- https://www.crewai.com/
- https://microsoft.github.io/autogen/
- https://www.lindy.ai/blog/ai-agent-architecture
