# Agent Integration — Tool Use Basics

## When to use
- The LLM needs access to real-time or external data (weather, stock prices, database records, web search)
- Precise computation is required (math, date arithmetic, data aggregation) that LLMs hallucinate when done in-context
- An autonomous agent must take actions (write files, call APIs, send messages) as part of a multi-step workflow
- The system needs to ground LLM responses in authoritative data sources rather than training knowledge
- Building a ReAct-style (Reason + Act) loop where the model iterates until a goal is achieved

## When NOT to use
- The task can be solved with a single in-context prompt without external data — tool calling adds latency and complexity
- All required information is already in the prompt context — don't add tools that duplicate information already provided
- The tool is destructive (deletes data, sends emails, charges money) and there is no human approval gate — tool use without checkpoints is dangerous
- The model is a small/fast model (Haiku, gpt-4o-mini) and the tool schema is complex (>5 tools, nested parameters) — selection accuracy degrades

## Where it fails / limitations
- Vague tool descriptions cause the model to select the wrong tool or skip tool use entirely; description quality is the #1 reliability lever
- Infinite loops: if tool results never satisfy the model's reasoning, it keeps calling tools until the context overflows; always cap iterations (10 is a safe default)
- Parallel tool calls (OpenAI default) can cause race conditions if tools share state; use `tool_choice="auto"` carefully with stateful tools
- JSON argument parsing: the model returns `function.arguments` as a string that may be malformed — always wrap `json.loads()` in a try/except
- Missing `tool_call_id` in the tool result message causes a validation error in OpenAI SDK; Anthropic uses `tool_use_id` — providers differ, test both paths

## Agentic workflow
A subagent implementing tool use should define a tool registry (name → callable), convert the registry to provider-specific schema, run the request-execute-respond loop with an iteration cap, and return a structured summary of tools called and their results. For autonomous agents, the subagent should log every tool call (name, args, result, latency) to a persistent trace so errors can be replayed. Destructive tools (write, delete, send) require a confirmation step before execution.

### Recommended subagents
- `faion-sdd-executor-agent` — scaffold tool registry, schema generator, and execution loop as SDD tasks
- General-purpose subagent — act as the "brain" in a tool-use loop; delegate actual tool execution to specialized subagents

### Prompt pattern
```
You have access to these tools: {tool_names}.
Use them to answer the user's request. Call tools step by step.
After each tool result, reason about whether the goal is achieved.
Stop after at most {max_iterations} tool calls.
User request: {request}
```

```
Generate an OpenAI function calling schema for this Python function:
{function_source}
Include: name, description from docstring, parameter types from type hints, required fields.
Output: valid JSON matching the OpenAI tool schema format.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pip install openai` | OpenAI function calling | [pypi](https://pypi.org/project/openai/) |
| `pip install anthropic` | Anthropic tool use | [pypi](https://pypi.org/project/anthropic/) |
| `pip install google-generativeai` | Gemini function calling | [pypi](https://pypi.org/project/google-generativeai/) |
| `pip install langchain-core` | Tool abstraction layer for multi-provider | [pypi](https://pypi.org/project/langchain-core/) |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| OpenAI Function Calling | SaaS | Yes | Built into Chat Completions; supports parallel calls; max 128 tools |
| Anthropic Tool Use | SaaS | Yes | `stop_reason == "tool_use"` pattern; max 64 tools |
| Gemini Function Calling | SaaS | Yes | `protos.Tool` schema; supports parallel; max 64 tools |
| LangChain Tools | OSS | Yes | 100+ pre-built tools (search, math, file, SQL); provider-agnostic |
| Composio | SaaS | Yes | Managed tool integrations (GitHub, Slack, Gmail) with OAuth; reduces boilerplate |

## Templates & scripts
See `templates.md` for the `chat_with_tools` loop, `generate_tool_definition` from Python function, and the code execution sandboxing template.

Inline iteration-capped tool loop (≤35 lines):
```python
import json

def agent_loop(client, messages, tools, tool_registry, model="gpt-4o", max_iter=10):
    """Run tool-use loop with iteration cap."""
    for _ in range(max_iter):
        resp = client.chat.completions.create(model=model, messages=messages, tools=tools)
        msg = resp.choices[0].message
        messages.append(msg)
        if not msg.tool_calls:
            return msg.content
        for tc in msg.tool_calls:
            fn = tc.function.name
            args = json.loads(tc.function.arguments)
            result = tool_registry.get(fn, lambda **_: {"error": f"unknown tool: {fn}"})(**args)
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": json.dumps(result)})
    return "[max iterations reached]"
```

## Best practices
- Write tool descriptions as if explaining to a junior developer who does not know the system — the model uses the description, not the code, to decide when to call a tool
- Return structured error objects from tools (`{"error": "reason"}`) instead of raising exceptions; let the model decide how to recover
- Execute independent tool calls in parallel (use `asyncio.gather` with async tool implementations) to reduce latency in multi-step pipelines
- Set a hard iteration cap in every tool loop and return a partial result with `[max_iterations_reached]` marker — never let the loop run unbounded
- Version tool schemas; when a tool's parameter schema changes, old conversations with cached schemas will fail — use explicit schema versioning in the tool registry

## AI-agent gotchas
- Code execution tools (running arbitrary Python) must be sandboxed; a model-generated `os.system("rm -rf /")` call in an unsandboxed subprocess is a critical security incident
- Tool result size: very large tool results (>50KB) sent back to the model inflate context dramatically; truncate or summarize large results before returning them
- Human checkpoint required before any tool that modifies external state (database writes, API calls that create/delete resources, email sending) — autonomous tool execution without approval is appropriate only for read-only tools
- Provider schema differences: OpenAI uses `"type": "function"` wrapper, Anthropic uses `"input_schema"` not `"parameters"`, Gemini uses `protos.FunctionDeclaration` — a single tool registry must translate between formats
- `json.loads(tool_call.function.arguments)` raises `JSONDecodeError` when the model generates malformed JSON (rare but happens with complex schemas); always catch and return a tool error instead of crashing the loop

## References
- [OpenAI Function Calling Guide](https://platform.openai.com/docs/guides/function-calling)
- [Anthropic Tool Use Guide](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
- [Gemini Function Calling](https://ai.google.dev/gemini-api/docs/function-calling)
- [LangChain Tools](https://python.langchain.com/docs/modules/tools/)
- [Composio tool integrations](https://composio.dev/docs)
