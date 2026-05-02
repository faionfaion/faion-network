---
name: mcp-server-build
description: Build a working MCP server in TypeScript or Python with stdio and HTTP transports, define 3 typed tools, and wire it into Claude Desktop or Claude Code.
tier: geek
group: mcp-protocol
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a running MCP server — in TypeScript (`@modelcontextprotocol/sdk`) or Python (`mcp`) — that exposes three typed tools (`search`, `fetch`, `summarize`), supports both stdio and Streamable HTTP transports, and is registered in Claude Desktop or Claude Code so agents can invoke the tools immediately.

## Prerequisites

- Node.js 20+ (for TypeScript path) OR Python 3.11+ (for Python path).
- `npm` or `pnpm` installed.
- Claude Desktop installed, or Claude Code with a project `claude.json`.
- Basic familiarity with JSON Schema (TypeScript path) or Pydantic (Python path).
- A working directory, e.g. `~/projects/my-mcp-server/`.

## Steps

### Option A — TypeScript with `@modelcontextprotocol/sdk`

1. Initialize the project.

```bash
mkdir ~/projects/my-mcp-server && cd ~/projects/my-mcp-server
npm init -y
npm install @modelcontextprotocol/sdk zod
npm install -D typescript @types/node tsx
npx tsc --init --target ES2022 --module NodeNext --moduleResolution NodeNext --outDir dist
```

2. Create `src/server.ts` with three tools and dual-transport support.

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  StreamableHTTPServerTransport,
} from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { z } from "zod";
import http from "node:http";

const server = new McpServer({
  name: "my-mcp-server",
  version: "1.0.0",
});

// Tool 1: search — keyword search returning ranked results
server.tool(
  "search",
  "Search a knowledge base by keyword. Returns top-N ranked results.",
  {
    query: z.string().min(1).describe("Search query string"),
    top_n: z.number().int().min(1).max(20).default(5).describe("Number of results"),
  },
  async ({ query, top_n }) => {
    // Replace with real search logic (e.g. Qdrant, pgvector, Elasticsearch)
    const results = [`Result 1 for "${query}"`, `Result 2 for "${query}"`].slice(0, top_n);
    return {
      content: [{ type: "text", text: JSON.stringify(results, null, 2) }],
    };
  }
);

// Tool 2: fetch — retrieve a URL and return its text content
server.tool(
  "fetch",
  "Fetch the text content of a URL. Returns raw page text, stripped of HTML.",
  {
    url: z.string().url().describe("Fully qualified URL to fetch"),
    timeout_ms: z.number().int().min(100).max(30000).default(5000),
  },
  async ({ url, timeout_ms }) => {
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), timeout_ms);
    try {
      const res = await fetch(url, { signal: ctrl.signal });
      const html = await res.text();
      // Naive strip — swap for a real parser (e.g. @mozilla/readability) in production
      const text = html.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim().slice(0, 8000);
      return { content: [{ type: "text", text }] };
    } finally {
      clearTimeout(timer);
    }
  }
);

// Tool 3: summarize — call Claude claude-sonnet-4-6 to summarize text
server.tool(
  "summarize",
  "Summarize a block of text in 2-4 sentences using Claude claude-sonnet-4-6.",
  {
    text: z.string().min(50).describe("Text to summarize (50–50000 chars)"),
    max_sentences: z.number().int().min(1).max(10).default(3),
  },
  async ({ text, max_sentences }) => {
    const Anthropic = (await import("@anthropic-ai/sdk")).default;
    const client = new Anthropic(); // reads ANTHROPIC_API_KEY from env
    const msg = await client.messages.create({
      model: "claude-sonnet-4-6",
      max_tokens: 512,
      messages: [
        {
          role: "user",
          content: `Summarize the following text in ${max_sentences} sentences:\n\n${text}`,
        },
      ],
    });
    const summary = msg.content[0].type === "text" ? msg.content[0].text : "";
    return { content: [{ type: "text", text: summary }] };
  }
);

// Transport selection: stdio (default) or HTTP (PORT env var)
async function main() {
  const port = process.env.PORT ? parseInt(process.env.PORT, 10) : null;

  if (port) {
    // Streamable HTTP transport — one session per request
    const httpServer = http.createServer(async (req, res) => {
      const transport = new StreamableHTTPServerTransport({
        sessionIdGenerator: () => crypto.randomUUID(),
      });
      await server.connect(transport);
      await transport.handleRequest(req, res);
    });
    httpServer.listen(port, () => {
      process.stderr.write(`MCP HTTP server listening on port ${port}\n`);
    });
  } else {
    // stdio transport — used by Claude Desktop and Claude Code subprocess model
    const transport = new StdioServerTransport();
    await server.connect(transport);
  }
}

main().catch((err) => {
  process.stderr.write(`Fatal: ${err}\n`);
  process.exit(1);
});
```

3. Add a start script to `package.json`.

```json
{
  "scripts": {
    "start": "tsx src/server.ts",
    "start:http": "PORT=3100 tsx src/server.ts"
  }
}
```

4. Install the Anthropic SDK (required by the `summarize` tool).

```bash
npm install @anthropic-ai/sdk
```

---

### Option B — Python with `mcp` SDK

1. Set up the project.

```bash
mkdir ~/projects/my-mcp-server && cd ~/projects/my-mcp-server
python3 -m venv .venv && source .venv/bin/activate
pip install mcp anthropic httpx
```

2. Create `server.py` with three tools and dual-transport support.

```python
import os
import sys
import asyncio
from mcp.server.fastmcp import FastMCP
from mcp.server.stdio import stdio_server

mcp = FastMCP("my-mcp-server")


@mcp.tool()
async def search(query: str, top_n: int = 5) -> list[str]:
    """Search a knowledge base by keyword. Returns top-N ranked results.

    Args:
        query: Search query string.
        top_n: Number of results to return (1-20).
    """
    # Replace with Qdrant / pgvector / Elasticsearch call
    return [f"Result {i+1} for '{query}'" for i in range(min(top_n, 20))]


@mcp.tool()
async def fetch(url: str, timeout_ms: int = 5000) -> str:
    """Fetch text content from a URL, HTML stripped.

    Args:
        url: Fully qualified URL.
        timeout_ms: Request timeout in milliseconds.
    """
    import re
    import httpx

    async with httpx.AsyncClient(timeout=timeout_ms / 1000) as client:
        resp = await client.get(url, follow_redirects=True)
        resp.raise_for_status()
        text = re.sub(r"<[^>]+>", " ", resp.text)
        return " ".join(text.split())[:8000]


@mcp.tool()
async def summarize(text: str, max_sentences: int = 3) -> str:
    """Summarize text using Claude claude-sonnet-4-6.

    Args:
        text: Text to summarize (50-50000 characters).
        max_sentences: Target sentence count (1-10).
    """
    import anthropic

    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env
    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        messages=[
            {
                "role": "user",
                "content": f"Summarize the following in {max_sentences} sentences:\n\n{text}",
            }
        ],
    )
    return msg.content[0].text


if __name__ == "__main__":
    port = os.environ.get("PORT")
    if port:
        # Streamable HTTP transport
        mcp.run(transport="streamable-http", host="127.0.0.1", port=int(port))
    else:
        # stdio transport (default for Claude Desktop / Claude Code subprocess)
        mcp.run(transport="stdio")
```

3. Smoke-test the server locally.

```bash
# Test stdio: send a raw initialize message and read the response
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"0.0.1"}}}' \
  | python server.py
```

---

### Register with Claude Desktop (both options)

4. Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows).

```json
{
  "mcpServers": {
    "my-mcp-server": {
      "command": "node",
      "args": ["/Users/<you>/projects/my-mcp-server/node_modules/.bin/tsx", "src/server.ts"],
      "env": {
        "ANTHROPIC_API_KEY": "<your-key>"
      }
    }
  }
}
```

For Python:

```json
{
  "mcpServers": {
    "my-mcp-server": {
      "command": "/Users/<you>/projects/my-mcp-server/.venv/bin/python",
      "args": ["/Users/<you>/projects/my-mcp-server/server.py"],
      "env": {
        "ANTHROPIC_API_KEY": "<your-key>"
      }
    }
  }
}
```

5. Restart Claude Desktop. The tools `search`, `fetch`, `summarize` appear in the tool list.

---

### Register with Claude Code

6. Add to `.claude/claude.json` in the project root (or `~/.claude/claude.json` for global).

```json
{
  "mcpServers": {
    "my-mcp-server": {
      "command": "node",
      "args": ["src/server.ts"],
      "cwd": "/Users/<you>/projects/my-mcp-server",
      "env": {
        "ANTHROPIC_API_KEY": "<your-key>"
      }
    }
  }
}
```

---

### Enable HTTP transport for remote or multi-client use

7. Start the HTTP server and confirm it accepts connections.

```bash
# TypeScript
PORT=3100 npm start

# Python
PORT=3100 python server.py
```

```bash
curl -s -X POST http://127.0.0.1:3100/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"curl-test","version":"0.0.1"}}}' \
  | python3 -m json.tool
```

Expected: a JSON response containing `"result":{"protocolVersion":"2024-11-05",...}`.

## Verify

Open Claude Desktop → new conversation → type: `search for "MCP protocol"`. Claude should invoke the `search` tool and display results. In Claude Code:

```bash
claude mcp list
```

Output must include `my-mcp-server` with status `connected`. Then in a session:

```
Use the search tool to find "streamable HTTP"
```

Claude invokes `search` and returns results. If `summarize` is invoked, the response is a 2-4 sentence paragraph (confirming the Anthropic API call succeeded).

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `claude mcp list` shows `my-mcp-server` as `error` | Executable path wrong in config | Verify absolute path: `which tsx` (TS) or `which python` (Python); use full path in `command` field |
| `ENOENT tsx` at startup | tsx not on PATH when Claude Desktop spawns the subprocess | Use the full `node_modules/.bin/tsx` path or install tsx globally: `npm i -g tsx` |
| `initialize` times out in stdio test | Server startup throws before reading stdin | Run `node src/server.ts` manually and inspect stderr for import/compile errors |
| HTTP `curl` returns connection refused | Server not running, or bound to wrong interface | Confirm `PORT=3100 npm start` is running; check the `host` binding (`0.0.0.0` for external, `127.0.0.1` for local) |
| `summarize` returns 401 Unauthorized | `ANTHROPIC_API_KEY` not passed to subprocess | Add `env.ANTHROPIC_API_KEY` in `claude_desktop_config.json` or Claude Code `claude.json` |
| Tool not visible in Claude Desktop after config change | Config not reloaded | Fully quit Claude Desktop (not just close window) and reopen |
| Python `mcp.run(transport="streamable-http")` AttributeError | mcp SDK version <1.0 | `pip install --upgrade mcp` — HTTP transport added in mcp 1.0 |

## Next

- `context-window-packing` — optimize large tool outputs to fit within the model context before the agent re-reads them.
- `mcp-auth-oauth` — add OAuth 2.0 token injection to the HTTP transport for multi-tenant deployments.
- Read `knowledge/geek/ai/claude-code/mcp` for schema design patterns (Zod refinements, union types) and security boundaries (read-only vs. write-capable tool split).

## References

- [knowledge/geek/ai/claude-code/mcp](../../../knowledge/geek/ai/claude-code/mcp) — schema design patterns, Zod/Pydantic input_schema construction, and stdio-vs-HTTP transport trade-offs that back Steps 2 and 7 of this playbook.
- [knowledge/geek/ai/claude-code/mcp-servers](../../../knowledge/geek/ai/claude-code/mcp-servers) — MCP server catalog covering registration patterns in `claude_desktop_config.json` and Claude Code `claude.json`, which inform Steps 4-6.
- [knowledge/geek/ai/llm-integration/claude-tool-use](../../../knowledge/geek/ai/llm-integration/claude-tool-use) — JSON Schema `input_schema` design and the agentic tool-use loop; backs the tool definition shape in Step 2 and explains why tools need explicit descriptions for reliable agent dispatch.
