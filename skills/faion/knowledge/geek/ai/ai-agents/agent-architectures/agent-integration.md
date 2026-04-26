# Agent Integration — Agent Architectures

## When to use
- Building a production autonomous agent that requires persistent memory, tool use, and failure recovery
- Designing the state machine for a multi-step agent workflow (IDLE → PLANNING → EXECUTING → REFLECTING → COMPLETE)
- Implementing a memory system (short-term + long-term with embedding-based retrieval) for a Claude subagent
- Replacing a monolithic prompt chain with a proper tool-equipped agent that can handle partial failures

## When NOT to use
- Simple single-step LLM tasks — the architecture overhead is not justified
- When the task graph is fully deterministic (no conditional branching based on tool results) — use a chain, not an agent
- Latency-critical paths where multi-iteration ReAct loops add unacceptable delay
- When you don't control the execution environment (e.g., no way to sandbox tool calls or enforce iteration limits)

## Where it fails / limitations
- Memory retrieval quality depends on embedding model quality; a weak embedder causes the agent to miss relevant past context
- `max_iterations` must be tuned per task type; too low causes premature termination, too high wastes tokens
- The `_reflect_on_completion` step itself costs LLM calls; on long tasks, reflection overhead can exceed 20% of total token spend
- Async execution requires careful error propagation; a failed tool call that doesn't raise will silently corrupt the message history
- The `AgentWithMemory` pattern uses OpenAI-format tool definitions; adapting to Anthropic's tool format requires schema translation

## Agentic workflow
A Claude Sonnet agent orchestrates the full architecture: it initializes the state machine, selects and calls tools, processes results, and decides when to enter the REFLECTING state. Opus is appropriate for the reflection step on complex tasks (goal-completion judgment). Haiku handles tool-definition generation from API schemas. The memory system runs as a sidecar: the orchestrator writes task outcomes to memory after each iteration and retrieves relevant context at the start of each new task. Human approval is required before any tool call that modifies external state (database writes, API mutations).

### Recommended subagents
- `faion-sdd-executor-agent` — drives agent-architecture implementation tasks from SDD specs
- `nero-sdd-executor-agent` — NERO-side execution with the same pattern

### Prompt pattern
```
<agent_task>
  <goal>Research and summarize the top 5 AI research tools for market researchers in 2026</goal>
  <tools>["web_search", "perplexity_query", "file_write"]</tools>
  <constraints>
    <max_iterations>10</max_iterations>
    <timeout_seconds>120</timeout_seconds>
    <require_approval>file_write</require_approval>
  </constraints>
  <output_schema>{"summary": "string", "sources": ["url"], "confidence": "low|medium|high"}</output_schema>
</agent_task>
```

```
<reflection_check>
  <goal>{{original_goal}}</goal>
  <current_result>{{agent_output}}</current_result>
  <question>Has the goal been fully achieved? Output JSON: {"complete": bool, "reason": "string", "missing": ["string"]}</question>
</reflection_check>
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `anthropic` SDK | Primary LLM calls for Claude-based agents | `pip install anthropic` / [docs](https://docs.anthropic.com/) |
| `openai` SDK | OpenAI-format tool definitions (compatible pattern) | `pip install openai` |
| `numpy` | Cosine similarity for memory retrieval | `pip install numpy` |
| `asyncio` | Async agent execution loop | stdlib |
| `langsmith` | Trace agent execution chains | `pip install langsmith` / [docs](https://docs.smith.langchain.com/) |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Anthropic Claude API | SaaS | Yes | Native tool use; use `tool_use` content blocks |
| OpenAI API | SaaS | Yes | Reference implementation in README; OpenAI tool format |
| LangSmith | SaaS | Yes — SDK | Agent execution tracing; essential for debugging ReAct loops |
| Chroma | OSS | Yes | Vector store for long-term memory embeddings |
| Pinecone | SaaS | Yes | Hosted vector store; lower ops overhead than Chroma |
| Modal | SaaS | Yes | Sandboxed code execution for tool calls; prevents host contamination |

## Templates & scripts
See `templates.md` for the full ProductionAgent template. Minimal Anthropic-native agent loop (replaces the OpenAI reference in README):

```python
import anthropic, json
from typing import Callable

client = anthropic.Anthropic()

def run_agent(goal: str, tools: list[dict], tool_fns: dict[str, Callable],
              max_iter: int = 10) -> str:
    messages = [{"role": "user", "content": goal}]
    for i in range(max_iter):
        r = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=4096,
            tools=tools,
            messages=messages
        )
        messages.append({"role": "assistant", "content": r.content})
        if r.stop_reason == "end_turn":
            text = next((b.text for b in r.content if hasattr(b, "text")), "")
            return text
        tool_results = []
        for block in r.content:
            if block.type == "tool_use":
                fn = tool_fns.get(block.name)
                result = fn(**block.input) if fn else f"Unknown tool: {block.name}"
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": str(result)
                })
        messages.append({"role": "user", "content": tool_results})
    return "Max iterations reached"
```

## Best practices
- Set `max_iterations` based on measured task complexity, not intuition; instrument production agents and tune from real data
- Write tool descriptions with the precision of API documentation — the agent's tool selection quality is directly proportional to description clarity
- Separate memory write (after task completion) from memory read (at task start); mixing them mid-iteration corrupts retrieval context
- Use `asyncio.wait_for` with an explicit `timeout_seconds` to prevent runaway agents from consuming unbounded tokens
- Log every tool call and result to a structured execution log; debugging a 15-iteration agent without logs is impractical
- Treat the reflection step as a quality gate, not an optimization; if reflection consistently returns `complete=true` on iteration 1, the max_iterations limit is likely too high

## AI-agent gotchas
- The `_reflect_on_completion` prompt asks the agent to evaluate its own output — this is unreliable for tasks where the agent cannot observe external effects (e.g., whether a file was actually written)
- Embedding functions must be thread-safe if the agent runs async; numpy and most embedding clients are not thread-safe by default
- Tool call arguments are untyped JSON; the agent will pass wrong types unless tool schemas enforce strict typing with `required` and `type` fields
- AgentState transitions are not enforced by the framework; a buggy tool can leave the agent in EXECUTING state permanently if the exception is swallowed
- The `Memory.summarize_recent()` method returns raw content without compression; for long-running agents, this will overflow the context window after ~50 iterations

## References
- [ReAct Paper](https://arxiv.org/abs/2210.03629)
- [Reflexion Paper](https://arxiv.org/abs/2303.11366)
- [Anthropic Tool Use Docs](https://docs.anthropic.com/en/docs/tool-use)
- [LangSmith Agent Tracing](https://docs.smith.langchain.com/)
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [Chroma Vector Store](https://docs.trychroma.com/)
