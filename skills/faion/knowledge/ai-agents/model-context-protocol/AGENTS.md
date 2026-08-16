# MCP (Model Context Protocol)

## Summary

**One-sentence:** Generates a working MCP server scaffold (stdio or Streamable HTTP) with discoverable tools, JSON Schema definitions, health probe, and Claude Code settings.json entry.

**One-paragraph:** Model Context Protocol is the open standard for exposing tools, resources, and prompts to LLM clients (Claude Code, Cursor, OpenAI Apps, etc.) without per-tool SDK coupling. This methodology produces a production-shaped MCP server in Python or TypeScript that ships a health/ping tool, declares every external tool with a flat JSON Schema, picks the right transport (stdio for local single-process, Streamable HTTP for remote multi-client), and emits a ready-to-paste client registration block. Versioning, error envelope, and OAuth Resource Server posture are baked into the output so the server is shippable, not a demo.

**Ефективно для:** інженера, який інтегрує внутрішні інструменти/дані в Claude Code чи інший MCP-клієнт — закриває петлю між API і агентом без custom SDK на кожен tool.

## Applies If (ALL must hold)

- Need to expose tools, resources, or data to one or more MCP clients (Claude Code, Cursor, OpenAI Apps) via a standardized protocol.
- Toolset is maintained separately from agent code — must version tools without redeploying every agent.
- At least one tool will be reused across ≥2 agents or projects.
- Target client supports MCP (verify the client's MCP spec version before scaffolding).
- A health/ping probe is acceptable as part of the tool surface (required for monitoring).

## Skip If (ANY kills it)

- Sandboxed runtime with no IPC/network — MCP needs stdio pipe or HTTP socket.
- One-shot single-agent tool use — direct LangChain/LlamaIndex tool definition is cheaper.
- Binary streaming response (audio, video) — MCP returns text/JSON; binary requires base64 (heavy).
- Latency budget < 50 ms — stdio process spawn or HTTP round-trip is too costly.
- Requires bidirectional streaming inside a single tool call — MCP tool calls are request/response.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Tool requirements | text or YAML list of `name + description + inputSchema + handler` | product / engineering brief |
| Target MCP client list | list (`claude-code`, `cursor`, `vscode-mcp`, `openai-apps`) | deployment plan |
| Auth posture | one of `none`, `bearer`, `oauth2.1` | security review |
| Transport choice | one of `stdio`, `streamable-http` | infrastructure plan |
| Tool execution code | Python or TypeScript handlers | existing internal services |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents/schema-field-order` | Tool inputSchema field order steers the LLM through the tool call. |
| `geek/ai/ai-agents/schema-version-pinning` | Bake `schema_version` into every tool response payload for evolvable contracts. |
| `geek/ai/claude-code/skills/` (parent) | Where Claude Code reads `mcpServers` config; required to register the scaffolded server. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules: unique tool names, health probe, flat JSON Schema, transport choice, version pin, OAuth on remote, error envelope | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the deliverable manifest (server name, tools[], transport, auth, registration block) + valid/invalid examples | ~800 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns: stdio process explosion, version mismatch silence, complex polymorphic schema, missing auth on remote, idle SSE drop, crash-without-alert | ~750 |
| `content/04-procedure.xml` | medium | 6-step procedure: requirements → transport choice → schema design → handler scaffold → smoke test with mcp-inspector → client registration | ~900 |
| `content/05-examples.xml` | medium | One full worked example: weather + db_query MCP server in Python with stdio, registered in Claude Code | ~600 |
| `content/06-decision-tree.xml` | essential | Pick stdio vs Streamable HTTP vs skip-MCP based on client count, location, auth, latency | ~350 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Generate tool definitions from API spec | haiku | Mechanical mapping (API path → JSON Schema). |
| Author server scaffold + handlers | sonnet | Real code, error handling, transport plumbing — needs reliable code generation. |
| Review schemas for LLM discoverability | sonnet | Cross-checks description clarity, naming, schema flatness. |
| Design multi-server orchestration / OAuth posture | opus | Coordinates auth flow, namespacing, resource server registration. |

## Templates

| File | Purpose |
|------|---------|
| `templates/python-server-stdio.py` | Minimal Python MCP server (stdio) with health probe, one demo tool, registration JSON snippet. |
| `templates/python-server-streamable-http.py` | Streamable HTTP server scaffold with bearer auth and session-id management. |
| `templates/tool-schema.json` | Flat JSON Schema skeleton for one tool — descriptions, required fields, examples. |
| `templates/_smoke-test.py` | Runs the server in a subprocess, calls `list_tools` and `call_tool`, asserts shape. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-model-context-protocol.py` | Validates a server manifest (or live server via mcp-inspector handshake) against the output contract — tool name uniqueness, schema flatness, health probe presence, auth on remote. | Pre-merge of any MCP server PR; CI gate. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[schema-field-order]] — steer the LLM through tool calls by ordering tool inputSchema fields.
- [[schema-version-pinning]] — version every tool response payload, not just the server.
- [[refusal-field-strict-schema]] — pair tool calls with strict-mode SO when the tool answer feeds extraction.
- [[role-specialized-models]] — pick which model invokes which tool by cognitive role.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` decides transport: if the server runs co-located with the client and only ever serves one process, stdio is the right call (lowest latency, no auth needed). If ≥2 clients, remote location, or org-wide reuse — Streamable HTTP with OAuth Resource Server posture. If the brief asks for sub-50 ms latency, no shared tools, or binary streaming inside a call — skip MCP and use a direct SDK tool. Run it the moment a tool-exposure question lands, before any code is written.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/python-server-stdio.py`

```python
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
```

### `templates/python-server-streamable-http.py`

```python
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
```

### `templates/tool-schema.json`

```json
{
  "_header": [
    "purpose: Flat JSON Schema skeleton for one MCP tool input.",
    "consumes: tool description and required fields.",
    "produces: tools[*].inputSchema entry for the server manifest.",
    "depends-on: JSON Schema draft 2020-12.",
    "token-budget-impact: every nested property costs ~2 tokens at tool-selection time; keep it flat."
  ],
  "type": "object",
  "required": [
    "city"
  ],
  "additionalProperties": false,
  "properties": {
    "city": {
      "type": "string",
      "description": "City name in English, e.g. 'Porto'. Diacritics allowed."
    },
    "units": {
      "type": "string",
      "enum": [
        "metric",
        "imperial"
      ],
      "default": "metric",
      "description": "Temperature unit system."
    }
  }
}
```

### `templates/_smoke-test.py`

```python
"""Run as: python _smoke-test.py /srv/mcp/faion-internal/server.py"""
import asyncio
import json
import subprocess
import sys
from pathlib import Path


async def main(server_path: Path) -> int:
    proc = await asyncio.create_subprocess_exec(
        sys.executable,
        str(server_path),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert proc.stdin is not None and proc.stdout is not None

    handshake = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {"protocolVersion": "2026-07-28", "clientInfo": {"name": "smoke", "version": "1"}},
    }
    proc.stdin.write((json.dumps(handshake) + "\n").encode())
    await proc.stdin.drain()
    line = await proc.stdout.readline()
    resp = json.loads(line)
    assert "result" in resp, f"handshake failed: {resp}"
    print(f"[handshake] ok, server={resp['result'].get('serverInfo', {}).get('name')}")

    ping = {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "ping", "arguments": {}}}
    proc.stdin.write((json.dumps(ping) + "\n").encode())
    await proc.stdin.drain()
    line = await proc.stdout.readline()
    resp = json.loads(line)
    body = json.loads(resp["result"]["content"][0]["text"])
    assert body["payload"]["status"] == "ok", f"ping failed: {body}"
    print(f"[ping] ok, server_version={body['server_version']}")

    proc.terminate()
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.stderr.write("usage: python _smoke-test.py <server.py>\n")
        sys.exit(2)
    sys.exit(asyncio.run(main(Path(sys.argv[1]))))
```
