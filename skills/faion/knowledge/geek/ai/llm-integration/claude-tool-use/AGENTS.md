# Claude Tool Use

## Summary

Patterns for Claude's tool use (function calling): defining tools with JSON Schema `input_schema`, detecting `stop_reason == "tool_use"`, running the canonical agentic loop, forcing structured JSON output via `tool_choice`, and building custom MCP servers. The core rule: always append the full `response.content` list (not just text) as the assistant turn — omitting tool_use blocks from history causes API errors on the next turn.

## Why

Tool use is the primary mechanism for giving Claude access to external APIs, databases, and search. The forced-tool-call pattern (`tool_choice={"type": "tool", "name": "..."}`) is the most reliable way to get typed JSON output from Claude without prompt engineering tricks. Without the agentic loop pattern and a max-iterations guard, agents exit early on tool_use stops or loop indefinitely.

## When To Use

- Agent loops where Claude must call external functions and incorporate results
- Forcing typed structured JSON output from Claude (tool-choice trick)
- Extracting typed data from unstructured text using a schema-constrained call
- Parallel tool dispatch — Claude can request multiple tools in one response
- MCP server integration for Claude Desktop agents needing filesystem, GitHub, or DB access

## When NOT To Use

- Simple text generation with no external data needs — tool definitions inflate prompt and cost tokens
- When OpenAI Structured Outputs or Gemini `response_schema` are already in use — mixing SDKs adds complexity
- Real-time streaming responses — tool use requires a complete response before the loop can continue
- Tool set larger than ~20 tools — Claude may pick the wrong tool; use tool routing to reduce the visible set

## Content

| File | What's inside |
|------|---------------|
| `content/01-tool-definition.xml` | Tool schema structure (name, description, input_schema), tool_choice options (auto/any/tool), checklist for writing descriptions |
| `content/02-agent-loop.xml` | Canonical agentic loop with max-iterations guard, parallel tool execution pattern, tool result format (success and error) |
| `content/03-structured-output.xml` | Forced tool call for JSON output, extract_user_data schema pattern, accessing tool_use.input |
| `content/04-mcp.xml` | MCP overview, claude_desktop_config.json pattern, custom MCP server in Python (tools/resources/prompts), available official servers |

## Templates

| File | Purpose |
|------|---------|
| `templates/agent-loop.py` | Complete agentic loop with max turns, parallel tool execution, and error handling |
| `templates/tool-definition.json` | Example tool definition with input_schema showing required properties and enum values |
