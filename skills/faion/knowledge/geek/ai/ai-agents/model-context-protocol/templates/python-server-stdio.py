#!/usr/bin/env python3
# purpose: Minimal Python MCP server scaffold (stdio transport) with health probe + structured error envelope.
# consumes: tool definitions (name, description, inputSchema) and handler callables provided by caller.
# produces: a running MCP server process speaking stdio, ready for Claude Code registration.
# depends-on: `pip install mcp`, Python 3.10+.
# token-budget-impact: trivial — server itself runs locally, no LLM tokens consumed by the scaffold.
"""Edit SERVER_NAME, SERVER_VERSION, list_tools, and call_tool. Keep `ping` as-is."""
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import asyncio
import json

SERVER_NAME = "faion-example"
SERVER_VERSION = "1.0.0"

app = Server(SERVER_NAME)


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="ping",
            description="Health probe; returns server status and version",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="example.echo",
            description="Echo back the supplied message; used as a smoke-test tool",
            inputSchema={
                "type": "object",
                "required": ["message"],
                "properties": {"message": {"type": "string", "description": "Text to echo"}},
            },
        ),
    ]


def _envelope(payload=None, error=None):
    """Structured response envelope — see methodology r6 (version pin) and r7 (error envelope)."""
    body = {"server_version": SERVER_VERSION, "payload": payload, "error": error}
    return [TextContent(type="text", text=json.dumps(body))]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "ping":
        return _envelope({"status": "ok"})
    if name == "example.echo":
        return _envelope({"echoed": arguments.get("message", "")})
    return _envelope(error={"code": "unknown_tool", "message": name, "retryable": False})


async def main() -> None:
    async with stdio_server() as (read, write):
        await app.run(read, write, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
