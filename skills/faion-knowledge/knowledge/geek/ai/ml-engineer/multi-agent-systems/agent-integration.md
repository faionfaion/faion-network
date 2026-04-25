# Agent Integration — Multi-Agent Systems

## When to use
- Task requires parallel specialized work: research + coding + review happening simultaneously
- Problem is too large for a single context window (>100K tokens of reasoning)
- Workflow has natural role boundaries: planner, executor, critic, verifier
- Iterative refinement loops benefit from adversarial agents (generator vs. critic)
- Long-running pipelines where intermediate outputs need validation checkpoints

## When NOT to use
- Simple, linear task a single agent can complete in one pass
- Low latency is required — multi-agent adds orchestration overhead (2-5x latency)
- Budget is tight — multiple agents multiply token spend quickly
- Task has tight coupling between steps where parallelization creates conflicts
- Team lacks observability tooling — debugging multi-agent failures is hard without traces

## Where it fails / limitations
- Orchestrator prompt drift: after 5+ back-and-forth exchanges, manager agents lose track of original goals
- State desynchronization: agents reading/writing shared state concurrently produce race conditions without explicit locking
- Error propagation: worker failure silently passes bad output downstream unless each stage validates its inputs
- Tool abuse loops: agents calling tools in cycles when stuck, running up costs without making progress
- Context window fragmentation: sub-agents with small contexts miss critical info passed by orchestrator; always serialize full context, not summaries
- Persona collapse in peer-to-peer: agents with similar prompts converge on agreement rather than productive disagreement

## Agentic workflow
Deploy multi-agent systems via the Claude Agent SDK's subagent primitive: parent agent spawns child agents with tool access, waits for structured results, then routes to the next stage. For hierarchical patterns, keep the orchestrator stateless (just routing) and push state into a shared file or queue that all workers read. For sequential pipelines, chain outputs as explicit inputs to the next stage rather than relying on shared memory. Always instrument each agent boundary with structured logging.

### Recommended subagents
- `faion-brainstorm` — diverge/converge/review cycle; wraps multi-agent ideation natively
- `faion-sdd-execution` — uses planner/executor/reviewer pattern for code tasks
- `faion-poll-agents` — manages a self-replenishing pool of parallel worktree subagents

### Prompt pattern
```
You are the ORCHESTRATOR. Your only job is routing and synthesis.
Workers: [researcher, coder, reviewer]
State file: /tmp/task-state.json
On each turn: read state → pick one worker → emit JSON with {"worker": "...", "instruction": "..."}
Never do the work yourself. Never skip validation.
```

```
You are the RESEARCHER worker. Task: <specific scoped task>.
Write output ONLY to: /tmp/task-state.json under key "research".
Signal completion: {"status": "done", "worker": "researcher"}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `langgraph` | Graph-based state machine for agent workflows | `pip install langgraph` / docs.langchain.com/langgraph |
| `crewai` | Role-based multi-agent teams with task delegation | `pip install crewai` / docs.crewai.com |
| `autogen` | Conversational multi-agent (Microsoft) | `pip install pyautogen` / microsoft.github.io/autogen |
| `swarm` | Lightweight OpenAI agent handoffs (prototyping) | `pip install openai-swarm` / github.com/openai/swarm |
| `langsmith` | Tracing and debugging agent chains | `pip install langsmith` / docs.langchain.com/langsmith |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| LangSmith | SaaS/Self-hosted | Yes | Full trace visualization per agent; essential for debugging |
| Langfuse | OSS (MIT) | Yes | Self-hostable alternative; no vendor lock-in |
| Redis / Valkey | OSS | Yes | Shared state store; use for pub/sub between agents |
| PostgreSQL | OSS | Yes | Persistent checkpoints (LangGraph PostgresSaver) |
| Docker | OSS | Yes | Sandbox code-executing agents; prevents runaway tool use |

## Templates & scripts
See `templates.md` for LangGraph state machine template, CrewAI role definition template, and tool-call retry wrapper.

Inline: minimal two-agent orchestrator pattern (Python, ~40 lines):

```python
import anthropic, json
from pathlib import Path

client = anthropic.Anthropic()
STATE_FILE = Path("/tmp/agent-state.json")

def run_agent(role: str, instruction: str, state: dict) -> dict:
    resp = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=4096,
        system=f"You are the {role}. Return JSON only.",
        messages=[{"role": "user", "content": f"State: {json.dumps(state)}\n\nTask: {instruction}"}],
    )
    return json.loads(resp.content[0].text)

def run_pipeline(task: str) -> dict:
    state = {"task": task, "research": None, "draft": None, "review": None}
    state["research"] = run_agent("researcher", "Research the task. Return {\"findings\": \"...\"}.", state)
    state["draft"] = run_agent("writer", "Write draft using findings. Return {\"draft\": \"...\"}.", state)
    state["review"] = run_agent("reviewer", "Review draft. Return {\"verdict\": \"pass|fail\", \"notes\": \"...\"}.", state)
    STATE_FILE.write_text(json.dumps(state, indent=2))
    return state
```

## Best practices
- Use immutable state updates: agents append to state, never overwrite previous stages
- Set hard token budgets per agent role (orchestrator gets less; workers get more)
- Validate schema of each agent output before passing to the next stage
- Implement a global timeout watchdog that terminates the pipeline after N minutes
- Prefer sequential pipelines for deterministic tasks; use peer-to-peer only for creative/research work
- Never pass raw conversation history between agents — serialize structured state only
- Use separate model tiers: orchestrator → Claude Opus; workers → Sonnet; formatters → Haiku

## AI-agent gotchas
- Human-in-loop checkpoint required before any destructive tool call (file delete, API POST, DB write)
- Orchestrators with >4 workers lose coherence; split into sub-orchestrators instead
- Cost runaway: set `max_tokens` on each agent AND a total spend cap for the pipeline
- Do not use `InMemorySaver` in production LangGraph — lost on restart; use `PostgresSaver`
- Worker agents must receive full task context, not just a summary — summaries cause hallucinated assumptions
- Test single-agent mode first; only add multi-agent when single-agent demonstrably fails

## References
- https://docs.langchain.com/langgraph/
- https://docs.crewai.com/
- https://microsoft.github.io/autogen/
- https://github.com/openai/swarm
- https://research.aimultiple.com/agentic-frameworks/
- https://latenode.com/blog/ai-frameworks-technical-infrastructure/langgraph-multi-agent-orchestration/
