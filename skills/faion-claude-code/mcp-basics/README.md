# MCP Server Development Guide

**Communication: User's language. Code: English.**

## Purpose

Create, install, and configure MCP (Model Context Protocol) servers:
- Build custom MCP servers in TypeScript or Python
- Install popular MCP servers for various services
- Configure MCP servers in Claude Code settings

---

## Creating MCP Servers

### TypeScript (Recommended for npm distribution)

**Setup:**
```bash
mkdir my-mcp-server && cd my-mcp-server
npm init -y
npm install @modelcontextprotocol/sdk zod
npm install -D @types/node typescript
```

**package.json:**
```json
{
  "name": "my-mcp-server",
  "version": "1.0.0",
  "type": "module",
  "main": "build/index.js",
  "bin": {
    "my-mcp-server": "build/index.js"
  },
  "scripts": {
    "build": "tsc",
    "start": "node build/index.js"
  }
}
```

**tsconfig.json:**
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "Node16",
    "moduleResolution": "Node16",
    "outDir": "./build",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "declaration": true
  },
  "include": ["src/**/*"]
}
```

**src/index.ts (Basic Server):**
```typescript
#!/usr/bin/env node
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "my-mcp-server",
  version: "1.0.0",
});

// Define a tool
server.tool(
  "greet",
  "Greet a user by name",
  {
    name: z.string().describe("Name to greet"),
  },
  async ({ name }) => {
    return {
      content: [{ type: "text", text: `Hello, ${name}!` }],
    };
  }
);

// Define a resource
server.resource(
  "config",
  "config://app",
  async (uri) => ({
    contents: [{ uri, mimeType: "application/json", text: JSON.stringify({ version: "1.0" }) }],
  })
);

// Start server
const transport = new StdioServerTransport();
await server.connect(transport);
```

**Build & Test:**
```bash
npm run build
npx @modelcontextprotocol/inspector node build/index.js
```

---

### Python (Recommended for data/ML integrations)

**Setup:**
```bash
mkdir my-mcp-server && cd my-mcp-server
python -m venv venv
source venv/bin/activate
pip install "mcp[cli]" fastmcp
```

**server.py (FastMCP - Recommended):**
```python
#!/usr/bin/env python3
from fastmcp import FastMCP

mcp = FastMCP(name="my-mcp-server")

@mcp.tool
def greet(name: str) -> str:
    """Greet a user by name."""
    return f"Hello, {name}!"

@mcp.tool
def calculate(a: float, b: float, operation: str) -> float:
    """Perform arithmetic: add, subtract, multiply, divide."""
    ops = {
        "add": a + b,
        "subtract": a - b,
        "multiply": a * b,
        "divide": a / b if b != 0 else float('inf'),
    }
    return ops.get(operation, 0)

@mcp.resource("config://app")
def get_config() -> str:
    """Return app configuration."""
    import json
    return json.dumps({"version": "1.0"})

if __name__ == "__main__":
    mcp.run()
```

**server.py (Official SDK):**
```python
#!/usr/bin/env python3
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("my-mcp-server")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="greet",
            description="Greet a user",
            inputSchema={
                "type": "object",
                "properties": {"name": {"type": "string"}},
                "required": ["name"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "greet":
        return [TextContent(type="text", text=f"Hello, {arguments['name']}!")]

async def main():
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

**Test:**
```bash
python -m mcp dev server.py
# or
fastmcp dev server.py
```

---

## MCP Server Templates

### API Wrapper Template (TypeScript)

```typescript
#!/usr/bin/env node
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const API_KEY = process.env.MY_API_KEY;
const BASE_URL = "https://api.example.com";

const server = new McpServer({
  name: "example-api-mcp",
  version: "1.0.0",
});

async function apiCall(endpoint: string, method = "GET", body?: object) {
  const res = await fetch(`${BASE_URL}${endpoint}`, {
    method,
    headers: {
      "Authorization": `Bearer ${API_KEY}`,
      "Content-Type": "application/json",
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  return res.json();
}

// List items
server.tool(
  "list_items",
  "List all items from the API",
  {},
  async () => {
    const data = await apiCall("/items");
    return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] };
  }
);

// Get item by ID
server.tool(
  "get_item",
  "Get a specific item by ID",
  { id: z.string().describe("Item ID") },
  async ({ id }) => {
    const data = await apiCall(`/items/${id}`);
    return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] };
  }
);

// Create item
server.tool(
  "create_item",
  "Create a new item",
  {
    name: z.string().describe("Item name"),
    description: z.string().optional().describe("Item description"),
  },
  async ({ name, description }) => {
    const data = await apiCall("/items", "POST", { name, description });
    return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] };
  }
);

const transport = new StdioServerTransport();
await server.connect(transport);
```

### Database Wrapper Template (Python)

```python
#!/usr/bin/env python3
import os
import json
from fastmcp import FastMCP
import asyncpg

DATABASE_URL = os.environ.get("DATABASE_URL")

mcp = FastMCP(name="database-mcp")

@mcp.tool
async def query(sql: str) -> str:
    """Execute a read-only SQL query."""
    if not sql.strip().upper().startswith("SELECT"):
        return "Error: Only SELECT queries are allowed"

    conn = await asyncpg.connect(DATABASE_URL)
    try:
        rows = await conn.fetch(sql)
        return json.dumps([dict(row) for row in rows], default=str)
    finally:
        await conn.close()

@mcp.tool
async def list_tables() -> str:
    """List all tables in the database."""
    sql = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
    """
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        rows = await conn.fetch(sql)
        return json.dumps([row["table_name"] for row in rows])
    finally:
        await conn.close()

@mcp.tool
async def describe_table(table: str) -> str:
    """Get column information for a table."""
    sql = """
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_name = $1
    """
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        rows = await conn.fetch(sql, table)
        return json.dumps([dict(row) for row in rows])
    finally:
        await conn.close()

if __name__ == "__main__":
    mcp.run()
```

---

## Publishing MCP Servers

### npm (TypeScript)

```bash
# Build
npm run build

# Login to npm
npm login

# Publish
npm publish --access public
```

### PyPI (Python)

```bash
# Install build tools
pip install build twine

# Build
python -m build

# Upload
twine upload dist/*
```

---

## Testing & Debugging

```bash
# TypeScript - use MCP Inspector
npx @modelcontextprotocol/inspector node build/index.js

# Python - use FastMCP dev mode
fastmcp dev server.py

# Or official MCP dev
python -m mcp dev server.py
```

---

## Configuration in Claude Code

### Via CLI

```bash
claude mcp add <name> -s user -- <command> [args...]
claude mcp add <name> -s user -e KEY=value -- <command>
claude mcp list
claude mcp remove <name> -s user
```

### Via settings.json

```json
{
  "mcpServers": {
    "my-server": {
      "command": "npx",
      "args": ["-y", "my-mcp-server"],
      "env": {
        "API_KEY": "..."
      }
    }
  }
}
```

### Manual Configuration

Edit `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "figma": {
      "command": "npx",
      "args": ["-y", "@anthropic/figma-mcp"]
    },
    "meta-ads": {
      "command": "npx",
      "args": ["-y", "@pipeboard-co/meta-ads-mcp"],
      "env": { "META_ACCESS_TOKEN": "..." }
    },
    "stripe": {
      "command": "npx",
      "args": ["-y", "@stripe/mcp", "--tools=all"],
      "env": { "STRIPE_SECRET_KEY": "..." }
    },
    "twitter": {
      "command": "npx",
      "args": ["-y", "mcp-twitter-server"],
      "env": {
        "TWITTER_API_KEY": "...",
        "TWITTER_API_SECRET": "...",
        "TWITTER_ACCESS_TOKEN": "...",
        "TWITTER_ACCESS_SECRET": "..."
      }
    },
    "cloudflare": {
      "command": "npx",
      "args": ["-y", "@cloudflare/mcp-server-cloudflare"],
      "env": {
        "CLOUDFLARE_API_TOKEN": "...",
        "CLOUDFLARE_ACCOUNT_ID": "..."
      }
    }
  }
}
```

### Troubleshooting

| Issue | Solution |
|-------|----------|
| Server not starting | Check `claude mcp list`, verify package exists |
| Auth errors | Verify API keys/tokens in env |
| Timeout | Increase timeout in settings |
| Tools not showing | Restart Claude Code session |

---

## Resources

- [TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [FastMCP](https://gofastmcp.com/)
- [MCP Inspector](https://www.npmjs.com/package/@modelcontextprotocol/inspector)
- [Awesome MCP Servers](https://github.com/wong2/awesome-mcp-servers)
- [Official MCP Servers](https://github.com/modelcontextprotocol/servers)
- [Figma MCP Guide](https://help.figma.com/hc/en-us/articles/32132100833559)
- [Notion MCP](https://www.notion.com/blog/notions-hosted-mcp-server-an-inside-look)

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Create new skill from template | haiku | Mechanical task with clear structure |
| Design agent architecture for complex task | opus | Requires reasoning about delegation and isolation |
| Configure MCP server for Claude | sonnet | Implementation with moderate complexity |
| Write agent system prompt | sonnet | Requires clear communication and nuance |
| Set up hook for pre-commit security | haiku | Mechanical script configuration |
| Implement custom slash command | sonnet | Coding with context and interaction |

