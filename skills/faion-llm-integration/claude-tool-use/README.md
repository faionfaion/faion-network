# Claude Tool Use

**Tool Use, Function Calling, Structured Output, MCP**

---

## Tool Use / Function Calling

### Define Tools

```python
tools = [
    {
        "name": "get_weather",
        "description": "Get current weather for a location. Call this when user asks about weather.",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City name, e.g., 'Kyiv, Ukraine'"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "Temperature unit"
                }
            },
            "required": ["location"]
        }
    }
]
```

### Request with Tools

```python
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=tools,
    messages=[
        {"role": "user", "content": "What's the weather in Kyiv?"}
    ]
)

# Check stop reason
if message.stop_reason == "tool_use":
    for block in message.content:
        if block.type == "tool_use":
            print(f"Tool: {block.name}")
            print(f"ID: {block.id}")
            print(f"Input: {block.input}")
```

### Complete Tool Loop

```python
import json

def get_weather(location: str, unit: str = "celsius") -> dict:
    # Your implementation
    return {"temperature": 15, "condition": "cloudy", "unit": unit}

# Initial request
messages = [{"role": "user", "content": "What's the weather in Kyiv?"}]

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=tools,
    messages=messages
)

# Process tool calls
while response.stop_reason == "tool_use":
    # Add assistant message with tool use
    messages.append({"role": "assistant", "content": response.content})

    # Process each tool use
    tool_results = []
    for block in response.content:
        if block.type == "tool_use":
            # Execute tool
            result = get_weather(**block.input)

            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": json.dumps(result)
            })

    # Add tool results
    messages.append({"role": "user", "content": tool_results})

    # Continue conversation
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        tools=tools,
        messages=messages
    )

# Final response
print(response.content[0].text)
```

### Tool Choice

```python
# Auto (default) - model decides
tool_choice = {"type": "auto"}

# Required - must use a tool
tool_choice = {"type": "any"}

# Force specific tool
tool_choice = {"type": "tool", "name": "get_weather"}

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=tools,
    tool_choice=tool_choice,
    messages=[...]
)
```

### Tool Result with Error

```python
# Success
tool_result = {
    "type": "tool_result",
    "tool_use_id": "toolu_01...",
    "content": json.dumps({"temperature": 15})
}

# Error
tool_result = {
    "type": "tool_result",
    "tool_use_id": "toolu_01...",
    "is_error": True,
    "content": "Error: Location not found"
}
```

### Parallel Tool Calls

Claude can request multiple tools simultaneously:

```python
# Response with multiple tool uses
for block in response.content:
    if block.type == "tool_use":
        print(f"Tool: {block.name}, ID: {block.id}")
        # Execute each tool and collect results

# Return all results in single message
tool_results = [
    {"type": "tool_result", "tool_use_id": "toolu_01...", "content": "..."},
    {"type": "tool_result", "tool_use_id": "toolu_02...", "content": "..."}
]
messages.append({"role": "user", "content": tool_results})
```

---

## Structured Output with Tools

### Force JSON Output via Tool

```python
# Force JSON output via tool
json_tool = {
    "name": "output_json",
    "description": "Output the result as structured JSON",
    "input_schema": {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"},
            "email": {"type": "string", "format": "email"}
        },
        "required": ["name", "age"]
    }
}

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=[json_tool],
    tool_choice={"type": "tool", "name": "output_json"},
    messages=[
        {"role": "user", "content": "Extract: John Doe, 30, john@example.com"}
    ]
)

# Get structured data
tool_use = next(b for b in message.content if b.type == "tool_use")
data = tool_use.input  # {"name": "John Doe", "age": 30, "email": "john@example.com"}
```

### Extract Structured Data

```python
# Define extraction schema
extraction_tool = {
    "name": "extract_user_data",
    "description": "Extract user information from text",
    "input_schema": {
        "type": "object",
        "properties": {
            "users": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "role": {"type": "string"},
                        "skills": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["name", "role"]
                }
            }
        },
        "required": ["users"]
    }
}

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=2048,
    tools=[extraction_tool],
    tool_choice={"type": "tool", "name": "extract_user_data"},
    messages=[
        {"role": "user", "content": "Parse this team:\n\nJohn - Software Developer (Python, JavaScript)\nSara - Designer (Figma, Sketch)"}
    ]
)

# Get extracted data
tool_use = next(b for b in message.content if b.type == "tool_use")
users = tool_use.input["users"]
# [
#   {"name": "John", "role": "Software Developer", "skills": ["Python", "JavaScript"]},
#   {"name": "Sara", "role": "Designer", "skills": ["Figma", "Sketch"]}
# ]
```

---

## MCP (Model Context Protocol)

MCP allows Claude to connect to external tools and data sources.

### MCP Overview

```
Claude <-> MCP Server <-> Tools/Resources/Prompts
```

### MCP in Claude Desktop

```json
// claude_desktop_config.json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/files"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "..."
      }
    }
  }
}
```

### Available MCP Servers

| Server | Purpose |
|--------|---------|
| **filesystem** | Read/write local files |
| **github** | GitHub API access |
| **postgres** | PostgreSQL queries |
| **sqlite** | SQLite database |
| **puppeteer** | Browser automation |
| **google-drive** | Google Drive access |
| **slack** | Slack integration |

### MCP with API

```python
# MCP is primarily for Claude Desktop
# For API, use tool use pattern instead

# Tools provide similar functionality:
# - filesystem -> custom file tools
# - github -> GitHub API tools
# - database -> SQL execution tools
```

### Custom MCP Server (Python)

```python
from mcp.server import Server, Tool
import asyncio

# Define server
server = Server("my-mcp-server")

# Add tool
@server.tool()
async def search_docs(query: str) -> str:
    """Search documentation for query"""
    # Your implementation
    return f"Results for: {query}"

# Run server
if __name__ == "__main__":
    asyncio.run(server.run())
```

### Connect to MCP Server

```json
// claude_desktop_config.json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["/path/to/server.py"]
    }
  }
}
```

### MCP Resources

Resources provide read-only data to Claude:

```python
from mcp.server import Server, Resource

server = Server("docs-server")

@server.resource("docs://readme")
async def get_readme() -> str:
    """Project README"""
    with open("README.md") as f:
        return f.read()

@server.resource("docs://api/{endpoint}")
async def get_api_doc(endpoint: str) -> str:
    """API endpoint documentation"""
    # Load from docs
    return load_api_doc(endpoint)
```

### MCP Prompts

Prompts are reusable prompt templates:

```python
from mcp.server import Server, Prompt

server = Server("prompts-server")

@server.prompt("analyze-code")
def analyze_code_prompt(language: str = "python") -> str:
    """Code analysis prompt template"""
    return f"""Analyze the following {language} code:

1. Check for bugs and anti-patterns
2. Suggest improvements
3. Identify security issues
4. Recommend optimizations

Provide specific, actionable feedback."""
```

### MCP Best Practices

1. **Use resources for static data** - Documentation, configs
2. **Use tools for actions** - API calls, file operations
3. **Use prompts for templates** - Reusable prompt patterns
4. **Handle errors gracefully** - Return clear error messages
5. **Document your server** - Descriptions help Claude use it correctly

---

## Related Files

- [claude-api-basics.md](claude-api-basics.md) - Authentication, models, rate limiting
- [claude-messages-api.md](claude-messages-api.md) - Messages API, streaming, vision
- [claude-advanced-features.md](claude-advanced-features.md) - Extended Thinking, Computer Use, Caching, Batch
- [claude-best-practices.md](claude-best-practices.md) - Best practices, optimization, patterns
- [mcp-model-context-protocol.md](mcp-model-context-protocol.md) - MCP deep dive
- [mcp-ecosystem-2026.md](mcp-ecosystem-2026.md) - MCP ecosystem and servers

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Tool definition schema | haiku | Schema creation |
| Tool result handling | sonnet | Integration pattern |
| Multi-step tool use | sonnet | Agent pattern design |
