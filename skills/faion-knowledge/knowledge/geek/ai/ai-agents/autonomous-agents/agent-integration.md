# Agent Integration — Autonomous Agents

## When to use
- Task requires 3+ sequential tool calls where each step depends on prior output
- Workflow involves dynamic branching based on intermediate observations (e.g., search → read → decide → act)
- Goal is underspecified at start and requires iterative refinement (research, debugging, code generation with feedback loops)
- Automating knowledge work: data collection, analysis, report generation, competitive research
- Code generation tasks that require run-fix-retry cycles (sandbox execution)
- Multi-source information synthesis requiring dynamic retrieval decisions

## When NOT to use
- Single-turn tasks with deterministic output — just use a direct prompt
- Latency-sensitive production paths (each ReAct loop adds 1-3 LLM calls)
- Structured ETL with known schema — a script beats an agent every time
- Tasks with binary success/failure where hallucinated tool calls cause irreversible side effects (financial writes, database deletes)
- When you need reproducible deterministic output — agent non-determinism is a bug here

## Where it fails / limitations
- Infinite loops: ReAct agents without hard iteration caps will spiral on ambiguous tasks
- Tool abuse: calling the same search tool 10+ times without convergence is common
- Context overflow: after 20+ steps, the full thought-action-observation history exceeds context; truncation breaks reasoning
- Hallucinated actions: LLM invents tool parameters that look valid but fail silently
- No error escalation: basic agents swallow tool errors and continue with false assumptions
- Sandboxing gaps: code execution agents that run arbitrary code need OS-level isolation; missing this is a critical security failure

## Agentic workflow
Use a Claude subagent as the orchestrator running a ReAct loop: system prompt defines tools, the agent emits `thought → action → observation` cycles, and a supervisor subagent enforces an iteration cap and classifies terminal states. For multi-step research tasks, spawn a Plan-and-Execute pattern: one subagent (Opus) decomposes the goal into a task list, a pool of executor subagents (Sonnet/Haiku) works through subtasks, and a verifier subagent checks each result before marking it done. Reflexion improves quality by adding a self-critique pass after each major output before writing to persistent storage.

### Recommended subagents
- `orchestrator` — runs ReAct loop, selects tools, tracks iteration count
- `planner` — decomposes goal into ordered task list (use Opus for complex domains)
- `executor` — handles a single subtask with defined inputs/outputs (use Haiku for mechanical steps)
- `verifier` — checks task output against success criteria, returns pass/fail + reason
- `critic` — Reflexion pass: compares output against goal, generates improvement suggestions

### Prompt pattern
```
You are an autonomous research agent. You have these tools: [search, read_url, extract_data, write_file].
Goal: {goal}
Max iterations: 15

On each step output:
Thought: <reasoning about current state and next action>
Action: <tool_name>(<params>)
Observation: <result>

When goal is achieved output:
DONE: <summary of result>
```

```python
# Iteration guard — wrap every agent loop
MAX_ITERS = 15
for i in range(MAX_ITERS):
    response = agent.step(observation)
    if response.is_terminal:
        break
else:
    raise AgentTimeoutError(f"Agent exceeded {MAX_ITERS} iterations")
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `langgraph` | LangGraph agent orchestration with state checkpointing | `pip install langgraph` / https://langchain-ai.github.io/langgraph/ |
| `autogen` | Multi-agent conversation framework (Microsoft) | `pip install pyautogen` / https://microsoft.github.io/autogen/ |
| `crewai` | Role-based multi-agent teams | `pip install crewai` / https://docs.crewai.com/ |
| `agentops` | Agent observability and replay | `pip install agentops` / https://www.agentops.ai/ |
| `e2b` | Secure sandboxed code execution for agents | `pip install e2b-code-interpreter` / https://e2b.dev/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| LangSmith | SaaS | Yes | Trace every agent step; critical for debugging loops |
| E2B Code Interpreter | SaaS/OSS | Yes | Isolated Python sandbox; safe code execution for agents |
| Helicone | SaaS | Yes | LLM proxy with logging; add without code changes |
| Weights & Biases | SaaS | Partial | Track agent runs as experiments; needs manual instrumentation |
| Temporal | OSS | Yes | Durable execution for long-running agent workflows with retries |

## Templates & scripts
See `templates.md` for full ReAct and Plan-Execute agent templates.

Iteration-safe agent loop (≤40 lines):
```python
from typing import Callable
import json

def run_react_agent(
    llm_call: Callable[[list], str],
    tools: dict[str, Callable],
    goal: str,
    max_iters: int = 15,
) -> str:
    messages = [{"role": "user", "content": f"Goal: {goal}"}]
    for i in range(max_iters):
        raw = llm_call(messages)
        messages.append({"role": "assistant", "content": raw})
        if "DONE:" in raw:
            return raw.split("DONE:", 1)[1].strip()
        if "Action:" not in raw:
            break
        action_line = [l for l in raw.splitlines() if l.startswith("Action:")][0]
        tool_call = action_line.replace("Action:", "").strip()
        name, _, args_str = tool_call.partition("(")
        args = json.loads("{" + args_str.rstrip(")") + "}")
        try:
            result = tools[name](**args)
        except Exception as e:
            result = f"ERROR: {e}"
        messages.append({"role": "user", "content": f"Observation: {result}"})
    return "AGENT_TIMEOUT: max iterations reached"
```

## Best practices
- Always set a hard iteration cap (15 is safe default; lower for production critical paths)
- Log every thought-action-observation triplet to a structured store before the next step; this is your only replay artifact
- Use a separate, cheaper model (Haiku) for tool-call parsing and output formatting; reserve Sonnet/Opus for reasoning steps
- Write tools to be idempotent — agents retry on failure, so non-idempotent tools cause data corruption
- Define explicit terminal conditions in the system prompt; vague "stop when done" causes over-running
- Pass only the last N=5 observations into context once history exceeds 10 steps; summarize older steps
- Never give agents write access to production systems without a human approval checkpoint

## AI-agent gotchas
- LLM tool-call JSON is not always valid: always parse with try/except and return structured error back to the agent
- "Observation: None" is invisible to the LLM — always return a non-empty string ("Success: no output" is better than empty)
- Agents will try tools in alphabetical order if tool descriptions are equal quality — name and describe tools precisely
- ReAct agents often confuse "what I should do" with "what I just did" when the observation is similar to a prior step; include step counters in observations
- Streaming responses break action parsing if you parse before the stream completes — buffer fully before parsing
- Human-in-the-loop checkpoint: pause before any irreversible action (file delete, external API write, email send); require explicit confirmation token from a human approval queue

## References
- ReAct paper: https://arxiv.org/abs/2210.03629
- Reflexion paper: https://arxiv.org/abs/2303.11366
- LangGraph agent docs: https://langchain-ai.github.io/langgraph/tutorials/introduction/
- AutoGPT architecture: https://github.com/Significant-Gravitas/AutoGPT
- E2B sandbox: https://e2b.dev/docs
