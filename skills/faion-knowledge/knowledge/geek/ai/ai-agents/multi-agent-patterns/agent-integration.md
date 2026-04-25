# Agent Integration — Multi-Agent Patterns

## When to use
- Task decomposes into parallel, independent subtasks that can run simultaneously
- Complex project work where different agents have genuinely different roles (researcher, coder, reviewer)
- Quality-critical output that benefits from a Generator-Critic or Debate loop
- Production systems requiring auditability: hierarchical delegation produces a traceable assignment log
- Creative or strategy work where diverse perspectives from collaborating agents add value

## When NOT to use
- Simple tasks that fit in a single context window — multi-agent overhead is unjustified
- Tight latency budgets: orchestrating multiple agents adds at minimum 2-3 extra round-trips
- When agent roles overlap significantly — agents with redundant roles echo each other rather than contribute
- Tasks requiring fine-grained shared mutable state that cannot be safely passed via messages
- Fully deterministic pipelines where a sequential single-agent chain is simpler and cheaper

## Where it fails / limitations
- **Role confusion**: if system prompts are vague, agents duplicate work or contradict each other
- **Communication overhead**: collaborative patterns can spend more tokens on coordination messages than on actual work
- **Deadlocks** in async message-bus designs when agents wait on each other circularly
- **Echo chambers**: agents trained on similar data converge on the same (possibly wrong) answer even in debate patterns
- **Plan staleness** in hierarchical systems: manager's plan assumes a static world; late-arriving worker results can invalidate earlier assignments
- **Synthesis quality**: the orchestrator's final synthesis call is a single LLM call that may miss conflicts in the individual results
- **Cost explosion**: N agents × M iterations = N×M LLM calls; without budgets, production costs spike unexpectedly

## Agentic workflow
A Claude orchestrator subagent receives the top-level goal, selects the coordination pattern (hierarchical, parallel, debate, collaborative), instantiates specialized worker subagents, routes messages between them via a message bus or direct calls, and invokes a synthesis step to produce the final output. Each worker is a standalone Claude subagent with a scoped system prompt. The orchestrator's only job is delegation and synthesis — it should not perform domain work itself.

### Recommended subagents
- `orchestrator` — manages task decomposition, worker assignment, and result synthesis; uses Opus
- `researcher-worker` — web search + summarization; uses Sonnet
- `coder-worker` — code generation and unit test writing; uses Sonnet
- `reviewer-worker` — code review, critique, adversarial checking; uses Sonnet
- `debate-judge` — evaluates proponent/opponent arguments impartially; uses Opus

### Prompt pattern
Hierarchical delegation:
```xml
<role>Project Manager</role>
<goal>{{project_goal}}</goal>
<workers>
  <worker name="Researcher" role="Gathers facts and references"/>
  <worker name="Developer" role="Implements features"/>
  <worker name="Tester" role="Writes and runs tests"/>
</workers>
<instruction>Decompose the goal into assignments. Return JSON: {"assignments": [{"worker": "name", "subtask": "desc"}]}</instruction>
```

Debate pattern:
```xml
<role>{{proponent|opponent}}</role>
<topic>{{debate_topic}}</topic>
<opponent_argument>{{last_message}}</opponent_argument>
<instruction>Counter the opponent's argument with evidence and logic. Be specific.</instruction>
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `autogen` | Microsoft multi-agent conversation framework | `pip install pyautogen` / microsoft.github.io/autogen |
| `crewai` | Role-based agent teams with task delegation | `pip install crewai` / crewai.com |
| `langgraph` | State-machine graph for multi-agent flows | `pip install langgraph` / langchain-ai.github.io/langgraph |
| `agentops` | Observability SDK for multi-agent cost and trace | `pip install agentops` / agentops.ai |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| AutoGen Studio | OSS | Yes | Visual no-code builder for AutoGen multi-agent configs |
| CrewAI Enterprise | SaaS | Yes | Managed crew execution with role-based access control |
| LangGraph Cloud | SaaS | Yes | Hosted, persistent multi-agent state with checkpointing |
| LangSmith | SaaS | Yes | Traces inter-agent messages; essential for debugging orchestration |
| Helicone | SaaS | Yes | Cost accounting per agent role across a run |

## Templates & scripts
See `templates.md` for ManagerAgent, CollaborativeGroup, and DebateSystem classes.

Minimal parallel fan-out (≤25 lines):
```python
import asyncio

async def fan_out(agents: dict, subtasks: dict) -> dict:
    """Run subtasks in parallel across agents, gather results."""
    async def run_one(name, task):
        return name, agents[name].respond(task)
    results = await asyncio.gather(
        *[run_one(name, task) for name, task in subtasks.items()]
    )
    return dict(results)
```

## Best practices
- Write system prompts that make each agent's role **exclusive**: "you ONLY do X, never Y"
- Log every inter-agent message with sender, receiver, timestamp, and token count
- Set per-agent and per-run token budgets; abort the run if the budget is exceeded
- Use structured output (JSON schema) for all inter-agent messages — free-form text increases parsing failures
- The synthesis step should receive **all** worker outputs simultaneously, not iteratively, to avoid anchoring bias
- In debate patterns, use an independent judge agent not exposed to either debater's system prompt
- Test each agent individually before testing coordination; most failures are in individual agents, not the coordination logic

## AI-agent gotchas
- **Token attribution**: in a 10-agent run, it is hard to know which agent consumed most tokens. Use `agentops` or `LangSmith` tagging per agent role from the start.
- **Non-deterministic plan parsing**: the manager's JSON plan may be malformed. Always validate against a schema before dispatching subtasks; return the error to the manager for re-planning.
- **Worker blocking orchestrator**: in synchronous patterns, one slow worker blocks all downstream agents. Use async with timeouts (`asyncio.wait_for`) per worker call.
- **Context leakage**: agents share no memory by default, but accidentally shared global state (e.g. a Python dict) can cause race conditions in async settings.
- **Human-in-loop checkpoint**: insert an explicit approval gate before any agent executes irreversible actions (send email, write to DB, deploy code). The orchestrator must pause and surface the proposed action before proceeding.
- **Cascading hallucinations**: if the researcher worker fabricates a fact, all downstream workers build on it. Add a fact-check node that validates key claims before passing them to the next stage.

## References
- AutoGen: https://microsoft.github.io/autogen/
- CrewAI: https://github.com/joaomdmoura/crewAI
- MetaGPT: https://github.com/geekan/MetaGPT
- Multi-Agent Survey (2023): https://arxiv.org/abs/2308.08155
- "Orchestrating Agents" — Anthropic blog: https://www.anthropic.com/research/building-effective-agents
