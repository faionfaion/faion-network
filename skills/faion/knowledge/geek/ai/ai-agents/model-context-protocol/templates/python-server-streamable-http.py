#!/usr/bin/env python3
# purpose: Streamable HTTP MCP server scaffold with bearer-token auth and per-session id.
# consumes: tool list, bearer issuer URL, .well-known path.
# produces: an HTTP service speaking the 2026-07-28 MCP Streamable HTTP transport.
# depends-on: `pip install mcp httpx starlette uvicorn`, Python 3.10+.
# token-budget-impact: trivial — service is local proxy, no LLM tokens used by the scaffold.
"""Edit SERVER_NAME, SERVER_VERSION, ISSUER, list_tools, call_tool. Bearer is validated against ISSUER."""
import json
import os
import uuid
from typing import Any
import httpx
from mcp.server import Server
from mcp.server.streamable_http import streamable_http_app
from mcp.types import Tool, TextContent

SERVER_NAME = os.environ.get("MCP_SERVER_NAME", "faion-remote")
SERVER_VERSION = "1.0.0"
ISSUER = os.environ.get("MCP_OAUTH_ISSUER", "https://auth.example.com")
WELL_KNOWN_PATH = "/.well-known/oauth-protected-resource"

app = Server(SERVER_NAME)


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="ping",
            description="Health probe; returns server status and version",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


def _envelope(payload: Any = None, error: dict | None = None) -> list[TextContent]:
    body = {"server_version": SERVER_VERSION, "payload": payload, "error": error}
    return [TextContent(type="text", text=json.dumps(body))]


async def validate_bearer(token: str) -> bool:
    """Verify token against the OAuth Resource Server posture (RFC 7662 introspection)."""
    async with httpx.AsyncClient(timeout=2.0) as cx:
        r = await cx.post(f"{ISSUER}/oauth/introspect", data={"token": token})
        return r.status_code == 200 and r.json().get("active") is True


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "ping":
        return _envelope({"status": "ok", "session": str(uuid.uuid4())})
    return _envelope(error={"code": "unknown_tool", "message": name, "retryable": False})


# starlette/uvicorn wiring; `mcp` provides streamable_http_app helper.
asgi_app = streamable_http_app(
    app,
    auth_validator=validate_bearer,
    well_known_path=WELL_KNOWN_PATH,
    issuer=ISSUER,
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(asgi_app, host="127.0.0.1", port=int(os.environ.get("PORT", "8080")))
