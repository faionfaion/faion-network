# MCP Templates

## TypeScript Server Template

### package.json

```json
{
  "name": "mcp-server-myproject",
  "version": "1.0.0",
  "type": "module",
  "main": "dist/index.js",
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "tsx src/index.ts"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.0.0",
    "zod": "^3.25.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "tsx": "^4.0.0",
    "typescript": "^5.0.0"
  }
}
```

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "declaration": true
  },
  "include": ["src/**/*"]
}
```

### src/index.ts

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

// Server configuration
const SERVER_NAME = "mcp-server-myproject";
const SERVER_VERSION = "1.0.0";

// Initialize server
const server = new McpServer({
  name: SERVER_NAME,
  version: SERVER_VERSION,
  capabilities: {
    tools: { listChanged: false },
    resources: { subscribe: false, listChanged: false },
    prompts: { listChanged: false },
  },
});

// ============================================================================
// TOOLS
// ============================================================================

server.tool(
  "example_tool",
  "Description of what this tool does",
  {
    param1: z.string().describe("First parameter description"),
    param2: z.number().optional().describe("Optional second parameter"),
  },
  async ({ param1, param2 }) => {
    try {
      // Tool implementation
      const result = `Processed: ${param1}${param2 ? ` with ${param2}` : ""}`;

      return {
        content: [{ type: "text", text: result }],
      };
    } catch (error) {
      return {
        content: [
          { type: "text", text: `Error: ${(error as Error).message}` },
        ],
        isError: true,
      };
    }
  }
);

// ============================================================================
// RESOURCES
// ============================================================================

server.resource(
  "example-resource",
  "resource://myproject/example",
  { mimeType: "application/json", description: "Example resource" },
  async (uri) => {
    const data = { message: "Hello from resource" };

    return {
      contents: [
        {
          uri: uri.href,
          mimeType: "application/json",
          text: JSON.stringify(data, null, 2),
        },
      ],
    };
  }
);

// ============================================================================
// PROMPTS
// ============================================================================

server.prompt(
  "example_prompt",
  "Description of this prompt template",
  {
    input: z.string().describe("User input for the prompt"),
  },
  async ({ input }) => {
    return {
      messages: [
        {
          role: "user",
          content: {
            type: "text",
            text: `Process the following input:\n\n${input}\n\nProvide a detailed response.`,
          },
        },
      ],
    };
  }
);

// ============================================================================
// MAIN
// ============================================================================

async function main() {
  const transport = new StdioServerTransport();

  console.error(`Starting ${SERVER_NAME} v${SERVER_VERSION}...`);

  await server.connect(transport);

  console.error("Server connected and ready");
}

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});
```

## Python Server Template

### pyproject.toml

```toml
[project]
name = "mcp-server-myproject"
version = "1.0.0"
description = "MCP server for myproject"
requires-python = ">=3.10"
dependencies = [
    "mcp>=1.0.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### src/server.py

```python
"""MCP Server for MyProject."""

import asyncio
import json
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    Resource,
    ResourceContents,
    TextResourceContents,
    Prompt,
    PromptMessage,
    GetPromptResult,
)

# Server configuration
SERVER_NAME = "mcp-server-myproject"
SERVER_VERSION = "1.0.0"

server = Server(SERVER_NAME)

# ============================================================================
# TOOLS
# ============================================================================

@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="example_tool",
            description="Description of what this tool does",
            inputSchema={
                "type": "object",
                "properties": {
                    "param1": {
                        "type": "string",
                        "description": "First parameter description"
                    },
                    "param2": {
                        "type": "number",
                        "description": "Optional second parameter"
                    }
                },
                "required": ["param1"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Execute a tool."""
    if name == "example_tool":
        param1 = arguments["param1"]
        param2 = arguments.get("param2")

        try:
            result = f"Processed: {param1}{f' with {param2}' if param2 else ''}"
            return [TextContent(type="text", text=result)]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]

    raise ValueError(f"Unknown tool: {name}")


# ============================================================================
# RESOURCES
# ============================================================================

@server.list_resources()
async def list_resources() -> list[Resource]:
    """List available resources."""
    return [
        Resource(
            uri="resource://myproject/example",
            name="Example Resource",
            description="Example resource",
            mimeType="application/json"
        )
    ]


@server.read_resource()
async def read_resource(uri: str) -> ResourceContents:
    """Read a resource."""
    if uri == "resource://myproject/example":
        data = {"message": "Hello from resource"}
        return ResourceContents(
            contents=[
                TextResourceContents(
                    uri=uri,
                    mimeType="application/json",
                    text=json.dumps(data, indent=2)
                )
            ]
        )

    raise ValueError(f"Unknown resource: {uri}")


# ============================================================================
# PROMPTS
# ============================================================================

@server.list_prompts()
async def list_prompts() -> list[Prompt]:
    """List available prompts."""
    return [
        Prompt(
            name="example_prompt",
            description="Description of this prompt template",
            arguments=[
                {
                    "name": "input",
                    "description": "User input for the prompt",
                    "required": True
                }
            ]
        )
    ]


@server.get_prompt()
async def get_prompt(name: str, arguments: dict[str, str] | None) -> GetPromptResult:
    """Get a prompt by name."""
    if name == "example_prompt":
        user_input = arguments.get("input", "") if arguments else ""

        return GetPromptResult(
            messages=[
                PromptMessage(
                    role="user",
                    content={
                        "type": "text",
                        "text": f"Process the following input:\n\n{user_input}\n\nProvide a detailed response."
                    }
                )
            ]
        )

    raise ValueError(f"Unknown prompt: {name}")


# ============================================================================
# MAIN
# ============================================================================

async def main():
    """Run the MCP server."""
    print(f"Starting {SERVER_NAME} v{SERVER_VERSION}...", file=__import__("sys").stderr)

    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)


if __name__ == "__main__":
    asyncio.run(main())
```

## FastMCP Template (Python)

### server.py

```python
"""FastMCP Server Template."""

from fastmcp import FastMCP
from pydantic import BaseModel

mcp = FastMCP(
    name="mcp-server-myproject",
    version="1.0.0"
)

# ============================================================================
# TOOLS
# ============================================================================

class ProcessResult(BaseModel):
    """Structured result from process_data tool."""
    status: str
    items_processed: int
    summary: str


@mcp.tool()
async def process_data(
    data: str,
    format: str = "json"
) -> ProcessResult:
    """Process data and return structured result.

    Args:
        data: The data to process
        format: Output format (json, xml, csv)

    Returns:
        Processing result with status and summary
    """
    # Implementation
    return ProcessResult(
        status="success",
        items_processed=len(data.split()),
        summary=f"Processed data in {format} format"
    )


@mcp.tool()
def simple_tool(message: str) -> str:
    """A simple synchronous tool.

    Args:
        message: Message to process
    """
    return f"Received: {message}"


# ============================================================================
# RESOURCES
# ============================================================================

@mcp.resource("config://app/settings")
async def get_settings() -> str:
    """Get application settings."""
    import json
    settings = {
        "version": "1.0.0",
        "debug": False,
        "features": ["feature1", "feature2"]
    }
    return json.dumps(settings, indent=2)


@mcp.resource("file:///{path}")
async def read_file(path: str) -> str:
    """Read a file from the filesystem.

    Args:
        path: Path to the file
    """
    with open(path) as f:
        return f.read()


# ============================================================================
# PROMPTS
# ============================================================================

@mcp.prompt()
def analyze(content: str, focus: str = "general") -> str:
    """Generate an analysis prompt.

    Args:
        content: Content to analyze
        focus: Analysis focus area
    """
    return f"""Analyze the following content with focus on {focus}:

{content}

Provide:
1. Key findings
2. Recommendations
3. Action items"""


@mcp.prompt()
def code_review(code: str, language: str = "python") -> list[dict]:
    """Generate a code review prompt with multiple messages.

    Args:
        code: Code to review
        language: Programming language
    """
    return [
        {
            "role": "user",
            "content": f"Review this {language} code:\n\n```{language}\n{code}\n```"
        },
        {
            "role": "assistant",
            "content": "I'll analyze this code for quality, bugs, and improvements."
        },
        {
            "role": "user",
            "content": "Please provide specific line-by-line feedback."
        }
    ]


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    mcp.run()
```

## Claude Code Configuration Template

### .claude/settings.json

```json
{
  "mcpServers": {
    "project": {
      "command": "node",
      "args": ["./mcp/dist/index.js"],
      "cwd": "${workspaceFolder}",
      "env": {
        "NODE_ENV": "development"
      }
    },
    "database": {
      "command": "python",
      "args": ["-m", "mcp_server"],
      "cwd": "${workspaceFolder}/mcp",
      "env": {
        "DATABASE_URL": "${env:DATABASE_URL}"
      }
    }
  }
}
```

### Claude Desktop config

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
**Linux:** `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/username/projects"
      ]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxxx"
      }
    },
    "postgres": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-postgres",
        "postgresql://user:pass@localhost/db"
      ]
    },
    "custom": {
      "command": "/path/to/custom-server",
      "args": ["--config", "/path/to/config.json"],
      "env": {
        "API_KEY": "secret"
      }
    }
  }
}
```

## Docker Template

### Dockerfile

```dockerfile
FROM node:20-slim

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci --only=production

# Copy source
COPY dist/ ./dist/

# Run as non-root
USER node

# MCP servers typically use stdio
CMD ["node", "dist/index.js"]
```

### docker-compose.yml

```yaml
version: "3.8"

services:
  mcp-server:
    build: .
    stdin_open: true
    tty: true
    environment:
      - NODE_ENV=production
      - API_KEY=${API_KEY}
    volumes:
      - ./data:/app/data:ro
```

## HTTP Transport Template

### Express Server (TypeScript)

```typescript
import express from "express";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";

const app = express();
const server = new McpServer({
  name: "http-mcp-server",
  version: "1.0.0",
});

// Add tools, resources, prompts...

// SSE endpoint for MCP
app.get("/mcp/sse", async (req, res) => {
  const transport = new SSEServerTransport("/mcp/messages", res);
  await server.connect(transport);
});

// Message endpoint for client requests
app.post("/mcp/messages", express.json(), async (req, res) => {
  // Handle incoming messages
});

app.listen(3000, () => {
  console.log("MCP HTTP server running on port 3000");
});
```

---

*MCP Templates v2025-11-25*
