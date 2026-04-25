# Agent Integration — Agent Patterns

## When to use
- Task requires iterative tool use with intermediate observations (ReAct)
- Task is long-horizon with multiple dependent steps that benefit from upfront decomposition (Plan-and-Execute)
- Output quality needs automated self-verification, e.g. code generation, math, structured data extraction (Reflexion)
- Research or automation workflows where the agent may need to recover from dead ends
- Any scenario where a single LLM call cannot produce reliable output without feedback

## When NOT to use
- Single-step lookup or retrieval — overhead of agentic loop is wasteful
- Latency-sensitive paths where one round-trip must complete in <2 s
- Tasks with no verifiable success criterion (Reflexion loop has no termination signal)
- Environments without tool access — ReAct without tools degenerates to plain chain-of-thought
- Budget-constrained situations where multiple LLM calls are prohibitive

## Where it fails / limitations
- ReAct can get stuck in repetitive tool-call loops when tool results are ambiguous
- Plan-and-Execute plans become stale if early steps produce unexpected results; replanning is expensive
- Reflexion requires a reliable `success_check` function — if the check itself has false positives, the loop exits early with wrong output
- Max-iteration guards are necessary but arbitrary; tasks that genuinely need more steps silently fail
- All three patterns accumulate message history that can exceed context limits on long runs
- Tool-call JSON parsing errors break the loop mid-task without clean recovery unless caught explicitly

## Agentic workflow
Claude subagents map naturally onto each pattern: a ReAct subagent is invoked once per task and loops internally via tool calls; a Plan-and-Execute subagent splits into a planner call that returns a structured plan, then an executor subagent per step; a Reflexion subagent wraps an inner ReAct agent and calls a critic after each attempt. The parent orchestrator decides which pattern to apply based on task complexity and provides the `success_check` callback.

### Recommended subagents
- `researcher` — ReAct pattern with web-search and code-execution tools for open-ended investigation
- `planner` — Plan-and-Execute pattern for project-scoped tasks with known subtask types
- `code-fixer` — Reflexion pattern for iterative code generation with test-suite as success signal

### Prompt pattern
```xml
<task>{{task_description}}</task>
<pattern>react</pattern>
<max_iterations>10</max_iterations>
<tools>{{tool_list_json}}</tools>
```

```xml
<task>{{goal}}</task>
<pattern>reflexion</pattern>
<success_criterion>All unit tests pass with exit code 0</success_criterion>
<max_attempts>3</max_attempts>
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `langchain-cli` | Scaffold LangChain agent projects | `pip install langchain-cli` / langchain.com/docs |
| `litellm` | Proxy multiple LLM backends behind one API | `pip install litellm` / docs.litellm.ai |
| `instructor` | Structured output from LLM calls (useful for plan parsing) | `pip install instructor` / python.useinstructor.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| LangSmith | SaaS | Yes | Traces every ReAct step; essential for debugging loops |
| Weights & Biases Weave | SaaS | Yes | Logs multi-turn agent runs, cost tracking |
| Helicone | SaaS | Yes | Per-request cost/latency observability for all patterns |
| LangGraph Cloud | SaaS | Yes | Hosted execution for LangGraph-based ReAct/Plan-and-Execute |

## Templates & scripts
See `templates.md` for ReAct and Plan-and-Execute skeleton classes.

Minimal Reflexion runner (≤30 lines):
```python
def run_reflexion(agent_fn, task, success_check, max_attempts=3):
    history = []
    for i in range(max_attempts):
        result = agent_fn(task, history)
        if success_check(result["output"]):
            return result["output"]
        reflection = reflect(task, result)
        history.append({**result, "reflection": reflection})
    return history[-1]["output"]  # best effort
```

## Best practices
- Always cap `max_iterations` and `max_attempts`; never allow unbounded loops in production
- Persist message history to a store (Redis, SQLite) so crashed agents resume rather than restart
- In Plan-and-Execute, validate the plan structure (JSON schema) before executing any step to fail fast
- Use a cheaper model for the Reflexion critic call; full Opus is rarely needed for self-evaluation
- Emit structured logs per iteration (`iteration`, `tool_name`, `result_summary`) to enable post-hoc debugging
- Separate tool-execution errors from logic errors; tool failures should trigger retry with backoff, not full agent restart
- For Reflexion, make `success_check` deterministic — non-deterministic checks cause flapping across attempts

## AI-agent gotchas
- **Context growth**: Every ReAct iteration appends to messages; after ~15 turns the full history may overflow GPT-4o's 128k window. Truncate or summarize old observations before appending new ones.
- **Tool-call hallucination**: Models occasionally fabricate tool names not in the schema. Guard with `if tool_name in self.tools` before executing.
- **Plan staleness**: Plan-and-Execute assumes the world is static. If step 3 discovers new constraints, the remaining plan is invalid. Add a re-plan gate after each step that checks if continuation is still valid.
- **Reflexion termination**: Without a reliable `success_check`, agents loop to `max_attempts` on every run, tripling costs. Always wire in a real verifier (test runner, schema validator, linter).
- **Human-in-the-loop breakpoint**: For destructive actions (file writes, API mutations), insert an explicit human approval step before execution, even inside an autonomous Reflexion loop.

## References
- ReAct paper: https://arxiv.org/abs/2210.03629
- Reflexion paper: https://arxiv.org/abs/2303.11366
- LangChain agents docs: https://python.langchain.com/docs/modules/agents/
- "Building Effective Agents" — Anthropic blog (2024): https://www.anthropic.com/research/building-effective-agents
