# Agent Integration — MCP Server Development

## When to use
- Building a custom integration between Claude Code agents and an internal API, database, or service
- The target service has no existing MCP server in the public catalog
- Standardizing tool interfaces for a team: all agents use the same typed MCP tools instead of ad-hoc curl/Bash
- Wrapping a Python ML pipeline so Claude agents can invoke model inference as a named tool
- Creating a read-only database tool that enforces SELECT-only policy at the server level

## When NOT to use
- A well-maintained public MCP server already exists for the service — prefer `npx -y @package/name` over building from scratch
- The integration is a single-use one-off script — direct Bash/WebFetch is faster to write and maintain
- The service requires complex OAuth flows that are interactive — MCP servers run non-interactively
- You need sub-100ms latency for every tool call — MCP stdio transport adds ~10-50ms per call

## Where it fails / limitations
- Stdio transport (the default) requires a running subprocess per Claude Code session — no connection pooling
- TypeScript servers built with `"type": "module"` require Node.js >= 18; older Node versions silently fail
- FastMCP's `@mcp.tool` decorator doesn't support streaming responses — use the official SDK for streaming
- If the MCP server process crashes mid-session, tools become unavailable with no clear error message to the agent
- Tool descriptions are the only interface between the model and the server — vague descriptions cause wrong tool invocation
- Large return payloads (> 100KB) from tools inflate the agent's context window significantly
- Python SDK async servers don't work with `python -m mcp dev` if the event loop is already running (Jupyter)

## Agentic workflow
A scaffolding agent creates the server directory structure, writes `src/index.ts` or `server.py` from a template, builds and tests with MCP Inspector, then registers the server via `claude mcp add`. A separate validation agent queries the server with known inputs and checks outputs against expected schemas. Deployment is idempotent: the registration script (see Templates) is re-runnable.

### Recommended subagents
- General-purpose implementer (Write, Edit, Bash) — scaffolds server code from template
- Bash testing agent — runs `npx @modelcontextprotocol/inspector` or `fastmcp dev` to validate tools
- `faion-spec-reviewer-agent` — reviews tool descriptions for clarity and completeness

### Prompt pattern
```
Build an MCP server in {TypeScript|Python} that wraps {API/service}.
Tools needed:
- {tool_name}: {description}. Input: {params}. Output: {format}.
Use API key from env var {ENV_VAR_NAME}.
Register as: claude mcp add {server-name} -s user -e {ENV_VAR_NAME}=${{ENV_VAR}} -- {run command}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `npx @modelcontextprotocol/inspector` | Interactive GUI to test any MCP server's tools | `npx @modelcontextprotocol/inspector` |
| `fastmcp dev server.py` | Python dev mode with live reload | `pip install fastmcp` / gofastmcp.com |
| `python -m mcp dev server.py` | Official Python SDK dev mode | `pip install "mcp[cli]"` |
| `npm run build` | Compile TypeScript MCP server | Node.js project |
| `claude mcp add` | Register server in Claude Code settings | Bundled |
| `tsc` | TypeScript compiler for MCP servers | `npm install -D typescript` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| MCP TypeScript SDK | OSS | Native | Recommended for npm-distributed servers |
| FastMCP (Python) | OSS | Yes | Decorator-based; fastest to write; gofastmcp.com |
| MCP Python SDK (official) | OSS | Yes | More control; required for streaming |
| MCP Inspector | OSS | Yes | Web GUI for manual tool testing |
| npm registry | SaaS | Yes | Publish TypeScript servers for team distribution |
| PyPI | SaaS | Yes | Publish Python servers |

## Templates & scripts
TypeScript API wrapper (≤40 lines of core logic):
```typescript
#!/usr/bin/env node
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const API_KEY = process.env.MY_API_KEY ?? (() => { throw new Error("MY_API_KEY required"); })();
const server = new McpServer({ name: "my-api-mcp", version: "1.0.0" });

server.tool("get_item", "Fetch item by ID from MyAPI", { id: z.string() }, async ({ id }) => {
  const res = await fetch(`https://api.example.com/items/${id}`, {
    headers: { Authorization: `Bearer ${API_KEY}` }
  });
  if (!res.ok) return { content: [{ type: "text", text: `Error: ${res.status}` }] };
  return { content: [{ type: "text", text: JSON.stringify(await res.json(), null, 2) }] };
});

await server.connect(new StdioServerTransport());
```

Python FastMCP wrapper (≤20 lines):
```python
#!/usr/bin/env python3
import os, httpx
from fastmcp import FastMCP

mcp = FastMCP(name="my-api-mcp")
API_KEY = os.environ["MY_API_KEY"]

@mcp.tool
async def get_item(id: str) -> str:
    """Fetch item by ID from MyAPI."""
    async with httpx.AsyncClient() as c:
        r = await c.get(f"https://api.example.com/items/{id}",
                        headers={"Authorization": f"Bearer {API_KEY}"})
        return r.text

if __name__ == "__main__":
    mcp.run()
```

## Best practices
- Write tool descriptions as complete sentences explaining what the tool does, when to use it, and what it returns — the model uses these to decide which tool to call
- Return errors as text content (not Python exceptions) — the agent can read and handle text; uncaught exceptions crash the server
- Enforce permissions at the server level, not in the prompt — a READ-ONLY database server should reject non-SELECT queries in code
- Use `zod` (TS) or Pydantic-style type hints (Python) for input schemas — they auto-generate JSON schema for the tool definition
- Truncate large payloads before returning — `json.dumps(data)[:5000]` is better than sending 1MB to Claude's context
- Pin the SDK version in `package.json` / `requirements.txt` — `@modelcontextprotocol/sdk` releases occasionally include breaking changes
- Test with MCP Inspector before deploying — it shows exact JSON input/output and surfaces schema mismatches

## AI-agent gotchas
- An agent building an MCP server cannot use that server in the same session — it must restart Claude Code after `claude mcp add`
- If a tool returns an empty string or null, some clients interpret it as a server error — always return at least a status message
- Tool names must be globally unique within a server (no namespacing); name collisions with other registered servers produce unexpected routing
- The model cannot see the server's source code — it only sees tool names and descriptions; a poorly named tool with a misleading description will be misused
- MCP Inspector (`npx @modelcontextprotocol/inspector`) opens a browser GUI on port 5173 — not usable in headless agent environments; use `--cli` mode or direct stdio testing instead
- Building a server with `fastmcp` and publishing to PyPI means any version bump is immediately pulled by `pip install fastmcp-myserver` — pin versions in production registrations

## References
- https://github.com/modelcontextprotocol/typescript-sdk
- https://github.com/modelcontextprotocol/python-sdk
- https://gofastmcp.com/
- https://www.npmjs.com/package/@modelcontextprotocol/inspector
- https://github.com/modelcontextprotocol/servers
