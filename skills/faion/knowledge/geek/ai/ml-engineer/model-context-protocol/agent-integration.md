# Agent Integration — Model Context Protocol (MCP)

## When to use
- Exposing internal tools (database queries, file system, APIs) to LLM hosts without custom integration per host
- Building reusable tool servers that work across Claude Desktop, VS Code Copilot, and custom agents simultaneously
- Giving agents access to resources that need app-controlled (not model-controlled) presentation of context
- Standardizing tool interfaces across a team — one MCP server, many AI clients
- Enabling sampling: MCP server needs to make LLM calls back through the host (avoids embedding API keys in servers)

## When NOT to use
- Simple single-purpose agent that only needs 1-2 hardcoded tool functions — direct SDK tool definitions are simpler
- Latency-critical paths — MCP stdio transport adds ~5-20ms per round trip; HTTP transport adds network overhead
- Teams without TypeScript or Python experience — MCP SDK requires one of these; no other mature options
- Environments where stdio process management is unreliable (some containerized setups need explicit lifecycle management)
- When the tool surface changes frequently — MCP server restarts are required to reload tool definitions in most clients

## Where it fails / limitations
- Prompt injection via tool responses: malicious content in tool results can hijack the model's subsequent actions — sanitize all tool outputs
- Tool permission escalation: model may chain tool calls in unexpected sequences to achieve goals the user didn't intend; require explicit consent for sensitive operations
- Lookalike tool replacement: a malicious MCP server named similarly to a trusted one can be installed; hosts must verify server provenance
- stdio transport is single-client per process; to serve multiple simultaneous clients, use HTTP+SSE or Streamable HTTP
- No built-in authentication in stdio mode; HTTP transport requires implementing auth yourself
- Capability negotiation adds one round trip on session init — cold start latency is noticeably higher than direct tool calls

## Agentic workflow
Agents consume MCP as clients: the host (Claude Desktop, VS Code, or custom Claude SDK app) launches MCP servers and exposes their tools to the model. In a custom agent, use the MCP Python or TypeScript SDK client to connect to servers, list tools, and forward tool calls the model makes. The model sees MCP tools exactly like native SDK tools — no special handling needed. For agent-specific server implementations, use FastMCP (Python) for rapid server development; it handles JSON-RPC boilerplate automatically.

### Recommended subagents
- Custom Claude Code agents (`~/.claude/agents/`) that expose domain tools via MCP servers
- Any agent needing database, filesystem, or external API access without hardcoded tool code

### Prompt pattern
FastMCP server (Python):
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("project-tools")

@mcp.tool()
def query_database(sql: str) -> str:
    """Execute a read-only SQL query. Returns JSON rows."""
    # validate sql is SELECT only
    import re
    if not re.match(r"^\s*SELECT\b", sql, re.IGNORECASE):
        raise ValueError("Only SELECT queries allowed")
    rows = db.execute(sql).fetchall()
    return json.dumps([dict(r) for r in rows])

@mcp.resource("file:///{path}")
def read_file(path: str) -> str:
    """Read a file from the project directory."""
    return Path(f"/project/{path}").read_text()

if __name__ == "__main__":
    mcp.run()  # stdio transport by default
```

MCP client in agent (Python SDK):
```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run_with_mcp():
    async with stdio_client(StdioServerParameters(command="python", args=["server.py"])) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            # Pass tools to Claude as tool definitions
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `mcp` (Python SDK) | Build MCP servers and clients in Python | `pip install mcp` / github.com/modelcontextprotocol/python-sdk |
| `@modelcontextprotocol/sdk` | TypeScript MCP SDK | `npm install @modelcontextprotocol/sdk` / github.com/modelcontextprotocol/typescript-sdk |
| `fastmcp` | High-level Python MCP server framework | `pip install fastmcp` / github.com/jlowin/fastmcp |
| `mcp-go` | Go MCP SDK | `go get github.com/mark3labs/mcp-go` |
| `mcp inspector` | Debug MCP servers interactively | `npx @modelcontextprotocol/inspector` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Claude Desktop | SaaS (client) | Yes | Natively loads MCP servers from config JSON |
| VS Code / Copilot | SaaS (client) | Yes | MCP server support in agent mode |
| Anthropic SDK | OSS | Yes | Custom clients can connect to MCP servers programmatically |
| GitHub MCP Server | OSS | Yes | Official; exposes repos, PRs, issues as tools |
| Filesystem MCP Server | OSS | Yes | Reference server for local file access |
| Brave Search MCP | OSS | Yes | Web search tool via Brave API |

## Templates & scripts
See `templates.md` for: FastMCP server template, HTTP+SSE server template, client integration snippet for Claude SDK.

Inline: minimal FastMCP server with tool + resource (~20 lines):

```python
from mcp.server.fastmcp import FastMCP
import json

mcp = FastMCP("data-server")

@mcp.tool()
def list_records(table: str, limit: int = 10) -> str:
    """List records from a table. Returns JSON array."""
    allowed = {"users", "products", "orders"}
    if table not in allowed:
        raise ValueError(f"Table must be one of {allowed}")
    rows = db.query(f"SELECT * FROM {table} LIMIT {limit}")
    return json.dumps(rows)

@mcp.resource("config://app/{key}")
def get_config(key: str) -> str:
    """Read application config value."""
    return config.get(key, "")

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

## Best practices
- Sanitize all tool inputs against injection: validate SQL (SELECT only), file paths (no `..`), API parameters
- Implement tool-level access control — not all MCP clients should have access to all tools; check calling client identity
- Use descriptive tool names and docstrings — the model selects tools based on the description; vague names cause wrong tool selection
- Keep tool responses under 10KB; large responses eat context and slow the agent loop
- Log every tool invocation with caller identity, inputs, and outputs for audit trails
- For HTTP transport, implement bearer token auth — stdio trusts the local process by default
- Version your MCP server (`mcp = FastMCP("server-name", version="1.2.0")`) for client compatibility tracking

## AI-agent gotchas
- Human-in-loop checkpoint required for any MCP tool that writes state (file writes, DB mutations, API POSTs) — the model cannot undo tool actions
- Prompt injection through tool responses is the primary MCP attack surface: a database record or web page returned as a tool result can contain instructions the model will follow
- Tools that return errors must return structured error messages — unhandled exceptions cause the model to hallucinate what happened next
- MCP sampling (server requests LLM completion from client) requires explicit host approval; don't design servers that depend on sampling without testing the approval flow
- `list_changed` notifications are not supported by all clients; don't rely on dynamic tool registration in production — restart the server to update tools

## References
- https://modelcontextprotocol.io/specification/2025-11-25
- https://github.com/modelcontextprotocol/python-sdk
- https://github.com/modelcontextprotocol/typescript-sdk
- https://github.com/jlowin/fastmcp
- https://github.com/modelcontextprotocol/servers
- https://www.anthropic.com/news/model-context-protocol
