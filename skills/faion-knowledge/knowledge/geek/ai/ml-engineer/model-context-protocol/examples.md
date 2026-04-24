# MCP Examples

## TypeScript Server Examples

### Basic Server with Tools

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "weather-server",
  version: "1.0.0",
});

// Define tool with Zod schema
server.tool(
  "get_weather",
  "Get current weather for a location",
  {
    location: z.string().describe("City name or zip code"),
    units: z.enum(["celsius", "fahrenheit"]).default("celsius"),
  },
  async ({ location, units }) => {
    // Implementation
    const weather = await fetchWeather(location, units);
    return {
      content: [
        {
          type: "text",
          text: `Temperature: ${weather.temp}${units === "celsius" ? "C" : "F"}\nConditions: ${weather.conditions}`,
        },
      ],
    };
  }
);

// Start server
const transport = new StdioServerTransport();
await server.connect(transport);
```

### Server with Resources

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import * as fs from "fs/promises";

const server = new McpServer({
  name: "file-server",
  version: "1.0.0",
});

// Static resource
server.resource(
  "config",
  "file:///app/config.json",
  { mimeType: "application/json" },
  async (uri) => {
    const content = await fs.readFile("/app/config.json", "utf-8");
    return {
      contents: [
        {
          uri: uri.href,
          mimeType: "application/json",
          text: content,
        },
      ],
    };
  }
);

// Dynamic resource template
server.resourceTemplate(
  "project-file",
  "file:///{path}",
  { mimeType: "text/plain" },
  async (uri, { path }) => {
    const content = await fs.readFile(path, "utf-8");
    return {
      contents: [
        {
          uri: uri.href,
          mimeType: "text/plain",
          text: content,
        },
      ],
    };
  }
);

const transport = new StdioServerTransport();
await server.connect(transport);
```

### Server with Prompts

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "code-review-server",
  version: "1.0.0",
});

server.prompt(
  "code_review",
  "Analyze code quality and suggest improvements",
  {
    code: z.string().describe("The code to review"),
    language: z.string().optional().describe("Programming language"),
  },
  async ({ code, language }) => {
    return {
      messages: [
        {
          role: "user",
          content: {
            type: "text",
            text: `Please review this ${language || "code"}:\n\n\`\`\`${language || ""}\n${code}\n\`\`\`\n\nProvide:\n1. Code quality assessment\n2. Potential bugs\n3. Improvement suggestions`,
          },
        },
      ],
    };
  }
);

const transport = new StdioServerTransport();
await server.connect(transport);
```

### Complete Server Example

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "database-server",
  version: "1.0.0",
  capabilities: {
    tools: { listChanged: true },
    resources: { subscribe: true, listChanged: true },
    prompts: { listChanged: true },
  },
});

// Tool: Execute SQL query
server.tool(
  "execute_query",
  "Execute a read-only SQL query",
  {
    query: z.string().describe("SQL SELECT query"),
    database: z.string().default("main"),
  },
  async ({ query, database }) => {
    // Validate query is read-only
    if (!/^\s*SELECT/i.test(query)) {
      return {
        content: [{ type: "text", text: "Only SELECT queries are allowed" }],
        isError: true,
      };
    }

    const results = await executeQuery(database, query);
    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(results, null, 2),
        },
      ],
      structuredContent: results,
    };
  }
);

// Resource: Database schema
server.resource(
  "schema",
  "db://main/schema",
  { mimeType: "application/json" },
  async () => {
    const schema = await getSchema("main");
    return {
      contents: [
        {
          uri: "db://main/schema",
          mimeType: "application/json",
          text: JSON.stringify(schema, null, 2),
        },
      ],
    };
  }
);

// Prompt: Generate SQL query
server.prompt(
  "generate_sql",
  "Generate SQL query from natural language",
  {
    description: z.string().describe("What you want to query"),
  },
  async ({ description }) => {
    return {
      messages: [
        {
          role: "user",
          content: {
            type: "text",
            text: `Generate a SQL SELECT query for: ${description}\n\nDatabase schema is available at db://main/schema`,
          },
        },
      ],
    };
  }
);

const transport = new StdioServerTransport();
await server.connect(transport);
```

## Python Server Examples

### Basic Server with Tools

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("weather-server")

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="get_weather",
            description="Get current weather for a location",
            inputSchema={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name or zip code"
                    },
                    "units": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "default": "celsius"
                    }
                },
                "required": ["location"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "get_weather":
        location = arguments["location"]
        units = arguments.get("units", "celsius")

        # Implementation
        weather = await fetch_weather(location, units)

        return [
            TextContent(
                type="text",
                text=f"Temperature: {weather['temp']}{units[0].upper()}\nConditions: {weather['conditions']}"
            )
        ]

    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

### FastMCP Server (Simpler API)

```python
from fastmcp import FastMCP

mcp = FastMCP("My Server")

@mcp.tool()
async def get_weather(location: str, units: str = "celsius") -> str:
    """Get current weather for a location.

    Args:
        location: City name or zip code
        units: Temperature units (celsius or fahrenheit)
    """
    weather = await fetch_weather(location, units)
    return f"Temperature: {weather['temp']}{units[0].upper()}\nConditions: {weather['conditions']}"

@mcp.resource("file:///{path}")
async def read_file(path: str) -> str:
    """Read a file from the filesystem."""
    with open(path) as f:
        return f.read()

@mcp.prompt()
def code_review(code: str, language: str = "python") -> str:
    """Generate a code review prompt."""
    return f"Please review this {language} code:\n\n```{language}\n{code}\n```"

if __name__ == "__main__":
    mcp.run()
```

### Server with Resources

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Resource, ResourceContents, TextResourceContents

server = Server("file-server")

@server.list_resources()
async def list_resources() -> list[Resource]:
    return [
        Resource(
            uri="file:///project/README.md",
            name="README.md",
            description="Project documentation",
            mimeType="text/markdown"
        ),
        Resource(
            uri="file:///project/config.json",
            name="config.json",
            description="Configuration file",
            mimeType="application/json"
        )
    ]

@server.read_resource()
async def read_resource(uri: str) -> ResourceContents:
    if uri.startswith("file:///"):
        path = uri[7:]  # Remove file:// prefix

        with open(path, "r") as f:
            content = f.read()

        return ResourceContents(
            contents=[
                TextResourceContents(
                    uri=uri,
                    mimeType="text/plain",
                    text=content
                )
            ]
        )

    raise ValueError(f"Unknown resource: {uri}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## Client Examples

### TypeScript Client

```typescript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
import { spawn } from "child_process";

// Create transport to server process
const transport = new StdioClientTransport({
  command: "node",
  args: ["server.js"],
});

const client = new Client({
  name: "my-client",
  version: "1.0.0",
});

await client.connect(transport);

// List available tools
const { tools } = await client.listTools();
console.log("Available tools:", tools.map((t) => t.name));

// Call a tool
const result = await client.callTool({
  name: "get_weather",
  arguments: { location: "New York" },
});
console.log("Result:", result.content);

// List resources
const { resources } = await client.listResources();
console.log("Available resources:", resources.map((r) => r.uri));

// Read a resource
const { contents } = await client.readResource({
  uri: "file:///project/README.md",
});
console.log("Content:", contents[0].text);

// Get a prompt
const { messages } = await client.getPrompt({
  name: "code_review",
  arguments: { code: "def hello(): print('world')" },
});
console.log("Prompt messages:", messages);

await client.close();
```

### Python Client

```python
from mcp import ClientSession
from mcp.client.stdio import stdio_client

async def main():
    async with stdio_client(
        command="python",
        args=["server.py"]
    ) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize
            await session.initialize()

            # List tools
            tools = await session.list_tools()
            print(f"Available tools: {[t.name for t in tools.tools]}")

            # Call tool
            result = await session.call_tool(
                name="get_weather",
                arguments={"location": "New York"}
            )
            print(f"Result: {result.content}")

            # List resources
            resources = await session.list_resources()
            print(f"Available resources: {[r.uri for r in resources.resources]}")

            # Read resource
            content = await session.read_resource(uri="file:///project/README.md")
            print(f"Content: {content.contents[0].text}")

            # Get prompt
            prompt = await session.get_prompt(
                name="code_review",
                arguments={"code": "def hello(): print('world')"}
            )
            print(f"Messages: {prompt.messages}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## Claude Code Configuration

### claude_desktop_config.json

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/files"]
    },
    "database": {
      "command": "python",
      "args": ["~/mcp-servers/database-server.py"],
      "env": {
        "DATABASE_URL": "postgresql://localhost/mydb"
      }
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

### .claude/settings.json (Claude Code)

```json
{
  "mcpServers": {
    "project-tools": {
      "command": "node",
      "args": ["./mcp/server.js"],
      "cwd": "${workspaceFolder}"
    }
  }
}
```

## JSON-RPC Message Examples

### Initialize Request

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2025-11-25",
    "capabilities": {
      "sampling": {}
    },
    "clientInfo": {
      "name": "my-client",
      "version": "1.0.0"
    }
  }
}
```

### Initialize Response

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2025-11-25",
    "capabilities": {
      "tools": { "listChanged": true },
      "resources": { "subscribe": true }
    },
    "serverInfo": {
      "name": "my-server",
      "version": "1.0.0"
    }
  }
}
```

### Tool Call with Structured Output

```json
{
  "jsonrpc": "2.0",
  "id": 5,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "{\"temperature\": 22.5, \"conditions\": \"Partly cloudy\"}"
      }
    ],
    "structuredContent": {
      "temperature": 22.5,
      "conditions": "Partly cloudy"
    }
  }
}
```

### Resource with Annotations

```json
{
  "uri": "file:///project/README.md",
  "name": "README.md",
  "mimeType": "text/markdown",
  "annotations": {
    "audience": ["user", "assistant"],
    "priority": 0.8,
    "lastModified": "2025-01-12T15:00:58Z"
  }
}
```

---

*MCP Examples v2025-11-25*
