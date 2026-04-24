# Model Context Protocol (MCP)

> Open protocol for LLM-tool communication. Standardized by Anthropic, adopted by OpenAI, Google, Microsoft.

## Overview

MCP is an open standard enabling seamless integration between LLM applications and external data sources/tools. It provides a universal interface for reading files, executing functions, and handling contextual prompts.

**Protocol Version:** 2025-11-25
**Governance:** Linux Foundation (Agentic AI Foundation)
**Adopters:** Anthropic, OpenAI, Google DeepMind, Microsoft, AWS

## Architecture

```
Host (Claude Desktop, IDE)
  |
  +-- Client 1 --> Server 1 (Files, Git)
  |
  +-- Client 2 --> Server 2 (Database)
  |
  +-- Client 3 --> Server 3 (External APIs)
```

### Components

| Component | Role | Responsibilities |
|-----------|------|------------------|
| **Host** | Container | Manages clients, enforces security, handles AI/LLM integration |
| **Client** | Connector | Maintains server session, handles protocol negotiation |
| **Server** | Provider | Exposes resources, tools, prompts via MCP primitives |

### Communication

- **Protocol:** JSON-RPC 2.0
- **Connection:** Stateful sessions
- **Transports:** stdio, HTTP+SSE, WebSockets, Streamable HTTP

## Core Primitives

| Primitive | Control | Description | Example |
|-----------|---------|-------------|---------|
| **Tools** | Model-controlled | Functions LLM can execute | API calls, file writing |
| **Resources** | App-controlled | Contextual data for LLM | File contents, git history |
| **Prompts** | User-controlled | Template instructions | Slash commands, menus |

### Tools

Model-controlled functions that perform actions or retrieve information.

```json
{
  "name": "get_weather",
  "description": "Get current weather for a location",
  "inputSchema": {
    "type": "object",
    "properties": {
      "location": { "type": "string" }
    },
    "required": ["location"]
  }
}
```

### Resources

Application-controlled data providing context to LLM.

```json
{
  "uri": "file:///project/src/main.rs",
  "name": "main.rs",
  "mimeType": "text/x-rust"
}
```

### Prompts

User-controlled instruction templates.

```json
{
  "name": "code_review",
  "description": "Analyze code quality",
  "arguments": [
    { "name": "code", "required": true }
  ]
}
```

## Additional Features

| Feature | Direction | Purpose |
|---------|-----------|---------|
| **Sampling** | Server-to-Client | Request LLM completions from client |
| **Roots** | Server-to-Client | Inquire about URI/filesystem boundaries |
| **Elicitation** | Server-to-Client | Request additional user context |

## Lifecycle

```
1. Initialize    Client sends init request with capabilities
2. Negotiate     Server responds with supported capabilities
3. Active        Exchange requests/responses/notifications
4. Terminate     Clean session shutdown
```

### Capability Negotiation

```json
{
  "capabilities": {
    "tools": { "listChanged": true },
    "resources": { "subscribe": true, "listChanged": true },
    "prompts": { "listChanged": true }
  }
}
```

## SDKs

| Language | Package | Framework |
|----------|---------|-----------|
| TypeScript | `@modelcontextprotocol/sdk` | FastMCP |
| Python | `mcp` | FastMCP |
| C# | `Microsoft.ModelContextProtocol` | - |
| Go | `github.com/mark3labs/mcp-go` | - |

## Security Considerations

1. **User Consent** - Explicit consent for all data access and tool invocations
2. **Data Privacy** - User data protected with appropriate access controls
3. **Tool Safety** - Tools represent arbitrary code execution, require caution
4. **LLM Sampling** - Users must approve sampling requests

### Known Security Concerns (April 2025)

- Prompt injection vulnerabilities
- Tool permission escalation
- Lookalike tool replacement attacks

## References

- [MCP Specification](https://modelcontextprotocol.io/specification/2025-11-25)
- [GitHub - modelcontextprotocol](https://github.com/modelcontextprotocol)
- [TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Reference Servers](https://github.com/modelcontextprotocol/servers)
- [Anthropic MCP Introduction](https://www.anthropic.com/news/model-context-protocol)

## Files

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Implementation checklist |
| [examples.md](examples.md) | Code examples (TypeScript, Python) |
| [templates.md](templates.md) | Server/client templates |
| [llm-prompts.md](llm-prompts.md) | Prompts for MCP development |

---

*MCP Reference 2025-11-25 | faion-ml-engineer*

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| MCP integration | sonnet | Protocol implementation |
| Tool definition | sonnet | API design |
| Server implementation | sonnet | Backend integration |
