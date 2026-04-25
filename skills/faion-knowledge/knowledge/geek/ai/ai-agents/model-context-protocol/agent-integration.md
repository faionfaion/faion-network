# Agent Integration — Model Context Protocol (MCP)

## When to use
- You need to expose tools, resources, or data sources to Claude (or other MCP clients) via a standardized protocol without custom SDK integration per tool
- Building a reusable tool server that multiple agents or clients can consume without duplicating integration code
- The tool set is maintained separately from the agent code — MCP decouples tool versioning from agent versioning
- You want Claude Code to access project-specific tools (databases, APIs, file systems) without per-project SDK configuration
- Integrating with existing MCP ecosystem servers (Brave Search, PostgreSQL, GitHub, filesystem) that are already MCP-compliant

## When NOT to use
- The agent runs in a fully sandboxed environment with no external communication — MCP requires a transport layer (stdio or SSE)
- You only need one-time tool use for a single agent — direct LangChain/LlamaIndex tool definition is simpler for non-shared tools
- The tool response is a binary stream (audio, video) — MCP currently handles text/JSON tool results; binary data requires base64 encoding
- Latency is critical (<100ms) — stdio transport adds process spawn overhead; SSE adds network round-trip
- You need bidirectional streaming during tool execution — MCP tool calls are request/response, not streaming mid-call

## Where it fails / limitations
- MCP stdio transport requires spawning a subprocess per client connection — high connection volume causes process explosion
- MCP spec is versioned; clients and servers must negotiate a compatible version — version mismatch causes silent tool registration failure
- Tool input schema is JSON Schema; complex recursive or polymorphic types are difficult to express and may confuse LLM tool selection
- MCP has no built-in authentication for stdio transport — any process with access to the transport can invoke tools
- SSE transport requires a persistent HTTP connection; proxies and load balancers with short connection timeouts drop the session
- Error handling is limited to string error messages in tool results — structured error codes are not part of the base spec

## Agentic workflow
An agent uses MCP by connecting to one or more MCP servers at startup, discovering available tools, and invoking them during task execution. Claude Code automatically discovers MCP servers from `settings.json` and makes their tools available to the agent. For custom MCP servers built for a project, the pattern is: define tool schemas in the server, register the server in Claude Code settings, then invoke tools by name during agent reasoning without any import or SDK call. For multi-agent systems, a single MCP server can be shared across all agents — tools are stateless and connection-multiplexed.

### Recommended subagents
- `faion-mcp-server-builder` — scaffolds an MCP server for a given set of Python functions; generates schema definitions and transport config
- General tool-discovery subagent — connects to MCP server, lists available tools with descriptions, returns tool manifest for orchestrator to select from

### Prompt pattern
```
You have access to MCP tools registered under server "my-project-tools".
Available tools: {tool_list}

Task: "{task}"
Select the appropriate tool and call it with the correct parameters.
After the tool returns, validate the result and proceed.
```

```
Build an MCP server exposing these functions: {function_signatures}
Use stdio transport. Generate:
1. Tool JSON schema for each function
2. Server implementation in Python using mcp SDK
3. Claude Code settings.json entry to register the server
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `mcp` (Python SDK) | Build MCP servers in Python | `pip install mcp` / https://github.com/modelcontextprotocol/python-sdk |
| `@modelcontextprotocol/sdk` | Build MCP servers in TypeScript/Node | `npm install @modelcontextprotocol/sdk` |
| `mcp-inspector` | Debug and test MCP servers interactively | `npx @modelcontextprotocol/inspector` |
| `mcpx` | Run MCP servers via npx without install | `npx mcpx <server>` |
| `claude` (Claude Code CLI) | MCP client; discovers servers from settings | `npm install -g @anthropic-ai/claude-code` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Claude Code | OSS | Yes | Primary MCP client; discovers servers from `settings.json` |
| Brave Search MCP | OSS | Yes | Web search tool server; `@modelcontextprotocol/server-brave-search` |
| GitHub MCP | OSS | Yes | Repo operations: read files, create PRs, list issues |
| PostgreSQL MCP | OSS | Yes | NL-to-SQL via MCP; `@modelcontextprotocol/server-postgres` |
| Filesystem MCP | OSS | Yes | Read/write local files; `@modelcontextprotocol/server-filesystem` |
| Anthropic MCP Registry | SaaS | Yes | Official directory of verified MCP servers |
| mcp.run | SaaS | Yes | Hosted MCP server marketplace |

## Templates & scripts
Minimal Python MCP server exposing one tool:

```python
# server.py — run via: python server.py
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import asyncio, json

app = Server("my-tools")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="get_weather",
            description="Get current weather for a city",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name"}
                },
                "required": ["city"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "get_weather":
        city = arguments["city"]
        # Replace with real weather API call
        return [TextContent(type="text", text=f"Weather in {city}: 22°C, sunny")]
    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read, write):
        await app.run(read, write, app.create_initialization_options())

asyncio.run(main())
```

Register in Claude Code `settings.json`:
```json
{
  "mcpServers": {
    "my-tools": {
      "command": "python",
      "args": ["/path/to/server.py"]
    }
  }
}
```

## Best practices
- Use `mcp-inspector` during development to validate tool schemas and test responses before connecting to Claude Code — inspector catches schema errors that Claude would silently ignore
- Keep tool descriptions concise and action-oriented ("Search the web for current information about X") — vague descriptions cause the LLM to select wrong tools or skip valid tools
- Return structured JSON as tool result text (not prose) when the caller is an agent — agents parse tool results programmatically
- Version MCP servers explicitly in their `name` field (`"my-tools-v2"`) — this allows rolling upgrades without breaking existing agent sessions
- Expose each domain as a separate MCP server rather than one monolithic server — isolation makes debugging easier and allows per-server access control
- Use SSE transport only if the server is remote; for local tools, stdio is more reliable and lower latency
- Add a `health` or `ping` tool to every server — agents can verify server availability before running tasks

## AI-agent gotchas
- Claude Code reloads MCP server list at startup, not per-session — adding a new server to `settings.json` requires restarting Claude Code for the agent to discover it
- Tool names must be globally unique across all connected MCP servers — two servers with a tool named `search` causes ambiguous tool selection
- MCP tool schemas use JSON Schema draft 7; `oneOf`, `anyOf`, and `$ref` are supported but LLMs interpret them poorly — prefer flat, explicit schemas
- An MCP server crash does not raise an error to the agent — the agent receives a connection error on the next tool call; implement server health monitoring separately
- `mcp-inspector` does not simulate real LLM tool selection — a tool that looks good in inspector may still be ignored by Claude if the description is not sufficiently distinct from other tools
- Secrets passed as environment variables to MCP servers are visible in process listings — use a secrets manager or file-based secrets for sensitive credentials

## References
- https://modelcontextprotocol.io/introduction
- https://github.com/modelcontextprotocol/python-sdk
- https://github.com/modelcontextprotocol/typescript-sdk
- https://modelcontextprotocol.io/docs/concepts/tools
- MCP server examples: https://github.com/modelcontextprotocol/servers
- Claude Code MCP guide: https://docs.anthropic.com/en/docs/claude-code/mcp
