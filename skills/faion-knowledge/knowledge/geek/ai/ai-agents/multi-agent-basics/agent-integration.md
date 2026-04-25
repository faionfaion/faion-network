# Agent Integration — Multi-Agent Systems Basics

## When to use
- Problem naturally divides into specialist roles (research, writing, review) with clear handoff boundaries
- Single agent struggles with scope: task requires more context than one conversation can hold
- Debate or adversarial review is needed to catch errors a single agent would miss
- Simulation scenarios where multiple viewpoints or actors must be modeled
- Building a reusable agent infrastructure that will serve many different task types over time

## When NOT to use
- Simple question-answering or single-step data transformation
- Tasks where the coordinator's orchestration cost exceeds the value added by worker specialization
- Environments without reliable message persistence — agents lose context on failure
- When role definitions cannot be made non-overlapping; overlapping roles produce conflicting outputs
- Proof-of-concept stages where debugging a multi-agent system is harder than building it

## Where it fails / limitations
- **Role confusion**: broad or overlapping system prompts cause agents to duplicate work
- **Communication overhead**: every send/receive consumes tokens; small tasks pay disproportionate coordination tax
- **Deadlocks**: agents waiting on each other's outputs without timeout will hang indefinitely
- **Echo chambers**: agents with similar training data converge on the same (possibly wrong) answer in debate or review
- **Coordination failure**: without a clear decision-making authority, no consensus is reached
- **Resource waste**: parallel agents that share a rate-limited API key will hit rate limits faster
- **Sequential bottlenecks**: debate and collaborative patterns serialize naturally; parallelism gains are limited

## Agentic workflow
A Claude orchestrator subagent initializes specialized worker subagents with scoped system prompts, routes messages between them (direct or broadcast), collects their outputs, and synthesizes a final response. For sequential pipelines, the orchestrator simply chains calls; for parallel, it uses `asyncio.gather`; for debate, it alternates calls between proponent and opponent before calling a judge. Workers never talk to each other directly — all communication routes through the orchestrator.

### Recommended subagents
- `orchestrator` — top-level coordinator; decomposes task and synthesizes results; uses Opus
- `specialist-worker` — domain-specific execution (research, coding, design critique); uses Sonnet
- `debate-judge` — impartial evaluation of competing agent outputs; uses Opus
- `pipeline-stage` — sequential transformer in a multi-step content pipeline; uses Haiku for simple transformations

### Prompt pattern
Sequential pipeline:
```xml
<role>{{agent_role}}</role>
<previous_stage_output>{{upstream_result}}</previous_stage_output>
<task>{{this_stage_task}}</task>
<output_format>{{schema_or_format}}</output_format>
```

Broadcast to all agents:
```xml
<broadcast>true</broadcast>
<task>{{shared_task}}</task>
<instruction>Provide your perspective from the viewpoint of your role. Be specific and non-redundant.</instruction>
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `autogen` | Conversational multi-agent framework (Microsoft) | `pip install pyautogen` / microsoft.github.io/autogen |
| `crewai` | Role-based agent teams | `pip install crewai` / crewai.com |
| `langgraph` | Graph-based agent coordination with state | `pip install langgraph` / langchain-ai.github.io/langgraph |
| `agentops` | Observability and cost tracking per agent | `pip install agentops` / agentops.ai |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| AutoGen Studio | OSS | Yes | No-code GUI for building multi-agent configs locally |
| CrewAI Enterprise | SaaS | Yes | Managed crew execution with role-based teams |
| LangGraph Cloud | SaaS | Yes | Persistent agent state, checkpointing, human-in-loop |
| LangSmith | SaaS | Yes | Full trace of every inter-agent message and tool call |
| Helicone | SaaS | Yes | Per-agent cost attribution, rate-limit monitoring |

## Templates & scripts
See `templates.md` for Agent, MultiAgentOrchestrator, SequentialPipeline, and DebateSystem implementations.

Minimal orchestrator with broadcast (≤20 lines):
```python
class MinimalOrchestrator:
    def __init__(self, agents: dict):
        self.agents = agents  # {name: agent_fn}

    def broadcast(self, message: str) -> dict:
        return {name: fn(message) for name, fn in self.agents.items()}

    def route(self, to: str, message: str) -> str:
        if to not in self.agents:
            raise ValueError(f"Unknown agent: {to}")
        return self.agents[to](message)
```

## Best practices
- Give each agent a **single, focused responsibility** — if a role description uses "and", split it into two agents
- Log all inter-agent messages with sender, receiver, content hash, and token count from the start
- Use structured JSON for all inter-agent communication; free-form text introduces parsing fragility
- Set explicit token budgets per agent and per run; alert when 80% is consumed
- Test each agent in isolation before testing coordination — most bugs are in individual agents
- In debate systems, the judge agent must not see the other agents' system prompts to avoid anchoring bias
- Implement per-worker timeouts so a single slow agent cannot block the entire pipeline

## AI-agent gotchas
- **Deadlock via mutual dependency**: Agent A waits for B's output, B waits for A's. Use a coordinator that detects cycles at plan-time.
- **Context loss on handoff**: agents have separate message histories. Pass full context in each handoff message, not just the delta.
- **Rate limit amplification**: 5 parallel agents hitting the same API key multiplies effective request rate by 5. Use per-agent rate limiters or a shared token bucket.
- **Synthesizer anchoring**: if the orchestrator reads worker outputs one by one (streaming), early outputs anchor the synthesis. Pass all outputs simultaneously.
- **Human-in-loop checkpoint**: any irreversible action (write to DB, send message, deploy) must pause for explicit human approval, even in a multi-agent pipeline. The orchestrator is responsible for surfacing this gate.
- **Debug complexity**: failures in multi-agent runs are harder to reproduce because agent message order may vary. Always record the full conversation history with timestamps.

## References
- AutoGen: https://microsoft.github.io/autogen/
- CrewAI: https://github.com/joaomdmoura/crewAI
- MetaGPT: https://github.com/geekan/MetaGPT
- Multi-Agent Survey: https://arxiv.org/abs/2308.08155
- "Building Effective Agents" — Anthropic (2024): https://www.anthropic.com/research/building-effective-agents
