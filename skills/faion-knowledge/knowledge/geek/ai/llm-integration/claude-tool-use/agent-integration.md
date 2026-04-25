# Agent Integration — Claude Tool Use

## When to use
- Agent loops where Claude must call external functions (APIs, databases, search) and incorporate results
- Forcing structured JSON output from Claude without a JSON mode parameter (tool-choice trick)
- Extracting typed data from unstructured text using a schema-constrained tool call
- Parallel tool dispatch — Claude can request multiple tools in one response, reducing round-trips
- MCP server integration for Claude Desktop agents that need filesystem, GitHub, or DB access

## When NOT to use
- Simple text generation with no external data needs — tool definitions inflate the prompt and cost tokens
- When OpenAI's structured outputs or Gemini's `response_schema` are already in use — mixing SDKs adds complexity
- Real-time streaming responses — tool use requires a complete response before the loop can continue
- When the tool set is very large (>20 tools) — Claude may pick the wrong tool or fail to call any; use tool routing to reduce the visible set

## Where it fails / limitations
- `stop_reason == "tool_use"` is a stop, not an error — agents must check this explicitly on every response; missing it causes the loop to exit early
- Parallel tool calls return multiple `tool_use` blocks in one response; all must be resolved before the next turn — partial resolution causes API errors
- Tool descriptions are the primary signal for tool selection; vague descriptions lead to wrong tool calls with no error
- `tool_choice={"type": "any"}` forces a tool call but Claude may call an unintended tool if the best match is ambiguous
- MCP is primarily for Claude Desktop (stdio transport) — programmatic API usage requires standard tool use, not MCP

## Agentic workflow
The canonical agentic loop: send message with tools → check `stop_reason` → if `tool_use`, execute all tool calls → append assistant message + tool results → repeat until `stop_reason == "end_turn"`. Agents should set a max-iterations guard (10–20 turns) to prevent infinite loops. Tool execution should be parallelized when Claude requests multiple tools simultaneously — do not serialize what Claude dispatched in parallel.

### Recommended subagents
- `faion-sdd-executor-agent` — implements a multi-step tool loop for SDD task execution
- Any custom subagent that wraps a domain tool set (search, code execution, DB queries)

### Prompt pattern
Structured output via forced tool call (reliable across all Claude models):
```python
extract_tool = {
    "name": "extract",
    "description": "Output the structured result",
    "input_schema": {"type": "object", "properties": {"field": {"type": "string"}}, "required": ["field"]}
}
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=[extract_tool],
    tool_choice={"type": "tool", "name": "extract"},
    messages=[{"role": "user", "content": text}]
)
data = next(b for b in response.content if b.type == "tool_use").input
```

Agent loop skeleton:
```python
MAX_TURNS = 15
for _ in range(MAX_TURNS):
    response = client.messages.create(model=MODEL, max_tokens=4096, tools=tools, messages=messages)
    messages.append({"role": "assistant", "content": response.content})
    if response.stop_reason != "tool_use":
        break
    results = [{"type": "tool_result", "tool_use_id": b.id,
                "content": execute(b.name, b.input)} for b in response.content if b.type == "tool_use"]
    messages.append({"role": "user", "content": results})
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `anthropic` (Python SDK) | Tool use, MCP integration | `pip install anthropic` / https://github.com/anthropics/anthropic-sdk-python |
| `@anthropic-ai/sdk` (Node SDK) | Tool use in TypeScript | `npm install @anthropic-ai/sdk` |
| `mcp` (Python SDK) | Build custom MCP servers | `pip install mcp` / https://github.com/modelcontextprotocol/python-sdk |
| `@modelcontextprotocol/sdk` | Build MCP servers in TypeScript | `npm install @modelcontextprotocol/sdk` |
| `npx @modelcontextprotocol/inspector` | Debug MCP servers interactively | npx (no install) |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Anthropic Messages API | SaaS | Yes | Primary tool-use endpoint |
| MCP Filesystem server | OSS | Yes | `npx @modelcontextprotocol/server-filesystem` |
| MCP GitHub server | OSS | Yes | `npx @modelcontextprotocol/server-github` |
| MCP PostgreSQL server | OSS | Yes | `npx @modelcontextprotocol/server-postgres` |
| MCP Brave Search server | OSS | Yes | `npx @modelcontextprotocol/server-brave-search` |
| LangSmith | SaaS | Yes | Trace tool call sequences and debug loops |

## Templates & scripts
See `templates.md` for the complete agent loop template. Tool error handling pattern:

```python
def execute_tool(name: str, input_data: dict) -> str:
    """Execute tool and return JSON string result or error."""
    try:
        if name == "search":
            return json.dumps(search(input_data["query"]))
        elif name == "read_file":
            return open(input_data["path"]).read()
        else:
            return json.dumps({"error": f"Unknown tool: {name}"})
    except Exception as e:
        return json.dumps({"error": str(e), "tool": name})
```

Return tool errors as content (not `is_error=True`) unless the error should terminate the loop — Claude can often recover from tool errors if they're returned as data.

## Best practices
- Write tool descriptions as if explaining to a colleague who has never seen your codebase — specificity prevents wrong tool selection
- Use `tool_choice={"type": "auto"}` by default; only force specific tools when structured output is the goal
- Always return a result for every `tool_use` block — missing tool results cause API errors on the next turn
- For parallel tool calls, use `asyncio.gather()` or `ThreadPoolExecutor` to execute them concurrently, then collect all results before the next message
- Keep tool input schemas as flat as possible — nested objects with 3+ levels increase tool-call errors
- Include a `reasoning` string field in extraction tool schemas — Claude documents why it chose values, which helps debugging
- Use `is_error=True` in tool results only for unrecoverable errors; otherwise let Claude see the error and try to fix it

## AI-agent gotchas
- Agents that append only the assistant message (not `response.content` which includes tool_use blocks) break the conversation history format and get API errors
- `response.content` is a list of mixed `TextBlock` and `ToolUseBlock` objects — iterate and type-check, never index blindly
- An infinite tool loop (Claude keeps calling the same tool) indicates a broken tool implementation that returns the same unhelpful result — implement result caching to detect and break cycles
- Tool schemas with `additionalProperties: false` can cause Claude to fail on edge cases; allow additional properties unless strict validation is needed
- MCP servers communicate via stdio by default — spawning them as subprocesses requires the agent to manage their lifecycle (start, health check, shutdown)
- Extended Thinking + tool use: thinking blocks appear in `response.content` before tool_use blocks; filter them out when building tool_result messages

## References
- https://docs.anthropic.com/en/docs/build-with-claude/tool-use
- https://docs.anthropic.com/en/docs/build-with-claude/tool-use/parallel-tool-use
- https://modelcontextprotocol.io/introduction
- https://github.com/modelcontextprotocol/servers (official MCP servers)
- https://docs.anthropic.com/en/api/messages (Messages API reference)
