# Agent Integration — MCP Basics (MCP Server Development)

## When to use
- Building a reusable typed interface between Claude agents and an internal system (database, API, filesystem abstraction)
- Replacing ad-hoc `Bash(curl:*)` tool calls with a named, schema-validated MCP tool that other agents can discover
- Creating a Python ML inference server so Claude agents can invoke models as named tools
- Distributing a shared integration to a team via npm or PyPI — MCP servers are installable packages

## When NOT to use
- An existing public MCP server covers the integration — prefer `npx -y @existing/package` over building from scratch
- Single-use task where a direct `WebFetch` or `Bash` call is simpler and won't be reused
- The server needs to maintain stateful sessions between tool calls — stdio transport creates a fresh process per session, no session affinity
- Sub-10ms latency is required per tool call — MCP transport overhead is 10-50ms minimum

## Where it fails / limitations
- TypeScript `"type": "module"` requires Node.js >= 18; silent runtime errors on older Node
- FastMCP does not support streaming tool responses — use the official `mcp` Python SDK for streaming
- If `process.env.API_KEY` is undefined in the TypeScript server, the server starts successfully but all tool calls fail at runtime — validate env at startup
- Large tool return values (>50KB) are passed verbatim into the agent's context window; they crowd out other context
- `npx -y package@latest` at Claude Code startup pulls the latest package version — a breaking upstream release can silently break all agents relying on that server
- MCP Inspector requires a browser (port 5173) — use `--cli` flag or direct stdin testing in headless environments
- Python asyncio servers (`async def` tool handlers) cannot be tested with synchronous test harnesses; use `asyncio.run()` in test scripts

## Agentic workflow
A scaffolding agent writes the server from a template, builds it, and runs MCP Inspector in `--cli` mode to verify each tool returns expected output. A registration agent then runs `claude mcp add` and writes a reproducible `mcp-setup.sh` script. The whole pipeline (scaffold → test → register → document) is sequential, driven by a single orchestrator. Human review at the "register" step is recommended for production servers with write permissions.

### Recommended subagents
- General-purpose implementer (Write, Edit, Bash) — scaffolds TypeScript or Python server from template
- Bash testing agent — runs `echo '{"params": {...}}' | node build/index.js` for manual stdin testing
- `faion-spec-reviewer-agent` — validates tool descriptions and input schemas for completeness

### Prompt pattern
```
Scaffold an MCP server named "{name}" in {TypeScript|Python}.
Tools:
- {tool_name}(input: {schema}) → {return_type}: {description}
API key: process.env.{ENV_VAR} (TypeScript) / os.environ["{ENV_VAR}"] (Python)
After scaffolding:
1. Build: {npm run build | python -m build}
2. Test: echo test input via stdin
3. Register: claude mcp add {name} -s user -e {ENV_VAR}=${{ENV_VAR}} -- {run_command}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `npx @modelcontextprotocol/inspector` | Browser/CLI GUI to test MCP server tools interactively | npmjs.com/package/@modelcontextprotocol/inspector |
| `fastmcp dev server.py` | Python live-reload dev server | `pip install fastmcp` / gofastmcp.com |
| `python -m mcp dev server.py` | Official Python SDK dev server | `pip install "mcp[cli]"` |
| `tsc` | TypeScript compiler | `npm install -D typescript` |
| `claude mcp add/list/remove` | Manage server registrations | Bundled with Claude Code |
| `npm publish` | Publish TypeScript server to npm | nodejs.org |
| `twine upload dist/*` | Publish Python server to PyPI | `pip install twine` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| MCP TypeScript SDK | OSS | Native | `@modelcontextprotocol/sdk`; recommended for npm dist |
| FastMCP (Python) | OSS | Yes | Decorator API; fastest for Python servers |
| MCP Python SDK | OSS | Yes | `mcp[cli]`; required for streaming support |
| MCP Inspector | OSS | Partial | Browser GUI; use `--cli` in headless environments |
| npm | SaaS | Yes | Distribute TypeScript servers as packages |
| PyPI | SaaS | Yes | Distribute Python servers as packages |

## Templates & scripts
Minimal TypeScript server with env validation (≤35 lines):
```typescript
#!/usr/bin/env node
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

// Fail fast on missing env
const API_KEY = process.env.MY_API_KEY;
if (!API_KEY) { console.error("MY_API_KEY env var required"); process.exit(1); }

const server = new McpServer({ name: "my-service-mcp", version: "1.0.0" });

server.tool(
  "fetch_data",
  "Fetch data from MyService by ID. Returns JSON object.",
  { id: z.string().describe("Record ID") },
  async ({ id }) => {
    try {
      const r = await fetch(`https://api.myservice.com/data/${id}`,
        { headers: { Authorization: `Bearer ${API_KEY}` } });
      const text = (await r.text()).slice(0, 10000); // truncate large payloads
      return { content: [{ type: "text", text: r.ok ? text : `Error ${r.status}: ${text}` }] };
    } catch (e) {
      return { content: [{ type: "text", text: `Network error: ${e}` }] };
    }
  }
);

await server.connect(new StdioServerTransport());
```

Python FastMCP (≤20 lines):
```python
#!/usr/bin/env python3
import os, sys, httpx
from fastmcp import FastMCP

API_KEY = os.environ.get("MY_API_KEY")
if not API_KEY:
    print("MY_API_KEY required", file=sys.stderr); sys.exit(1)

mcp = FastMCP(name="my-service-mcp")

@mcp.tool
async def fetch_data(id: str) -> str:
    """Fetch data from MyService by ID. Returns JSON string, max 10KB."""
    async with httpx.AsyncClient() as c:
        r = await c.get(f"https://api.myservice.com/data/{id}",
                        headers={"Authorization": f"Bearer {API_KEY}"})
        return r.text[:10000]

if __name__ == "__main__":
    mcp.run()
```

## Best practices
- Validate all env vars at server startup (before `server.connect()`), not inside tool handlers — fail fast with a clear error message
- Write tool descriptions as Claude would read them: "Fetches X by Y. Returns Z format. Use when you need W." — quality descriptions directly affect agent tool-selection accuracy
- Always truncate large payloads before returning — `text[:10000]` or equivalent prevents context window bloat
- Handle HTTP errors inside the tool handler and return them as text content — do not let exceptions propagate and crash the server
- Pin SDK versions in `package.json` and `requirements.txt` — `"@modelcontextprotocol/sdk": "1.2.3"` not `"*"`
- Add a `mcp-setup.sh` idempotent registration script to the repo root — makes developer onboarding reproducible

## AI-agent gotchas
- An agent that builds a server and runs `claude mcp add` cannot use the new server until Claude Code restarts — the agent must finish and inform the user to restart
- MCP tool names are global within a registered server; if two registered servers expose a tool with the same name, Claude will invoke whichever it finds first — use descriptive, unique names (`{service}_{action}`)
- If a Python FastMCP server uses `async def` handlers but is launched with `python server.py` (not `mcp.run()`), it will start but all async calls silently return None — always use `mcp.run()` as the entry point
- Agents cannot introspect what tools a server provides without calling `list_tools` — the MCP Inspector does this; in automated testing scripts, call `list_tools` first to verify server registration succeeded
- Return values must be serializable to JSON text content — returning a Python object (dict, list) without `json.dumps()` will produce a `[object Object]` string in TypeScript or a type error in Python

## References
- https://github.com/modelcontextprotocol/typescript-sdk
- https://github.com/modelcontextprotocol/python-sdk
- https://gofastmcp.com/
- https://www.npmjs.com/package/@modelcontextprotocol/inspector
- https://docs.anthropic.com/en/docs/claude-code/mcp
