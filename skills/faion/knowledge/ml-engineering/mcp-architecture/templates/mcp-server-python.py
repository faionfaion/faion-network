"""
purpose: Python MCP server skeleton via official SDK.
consumes: see AGENTS.md ## Prerequisites
produces: spec
depends-on: content/02-output-contract.xml schema for mcp-architecture
token-budget-impact: ≤500 tokens to fill
"""
# mcp>=1.10 (official Python SDK, FastMCP API). Shape follows the worked
# example in content/05-examples.xml: filesystem server, stdio for local hosts.
# Env vars: MCP_TRANSPORT (stdio | streamable-http), MCP_ROOT (served directory),
# MCP_OAUTH_ISSUER + MCP_RESOURCE_URL (remote only).
from __future__ import annotations

import os
from pathlib import Path

from mcp.server.auth.provider import AccessToken, TokenVerifier
from mcp.server.auth.settings import AuthSettings
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base
from mcp.types import LATEST_PROTOCOL_VERSION

# Rule r1: pin the protocol version; refuse to start on an SDK that moved on.
PROTOCOL_VERSION = "2025-11-25"
if LATEST_PROTOCOL_VERSION != PROTOCOL_VERSION:
    raise SystemExit(f"mcp SDK speaks {LATEST_PROTOCOL_VERSION}, spec pins {PROTOCOL_VERSION}")

TRANSPORT = os.environ.get("MCP_TRANSPORT", "stdio")  # rule r3: stdio for local desktop hosts
ROOT = Path(os.environ.get("MCP_ROOT", ".")).resolve()


class BearerVerifier(TokenVerifier):
    """Rule r4: remote transport MUST validate OAuth 2.1 (PKCE) tokens; replace the body
    with introspection against <authorization-server>."""

    async def verify_token(self, token: str) -> AccessToken | None:
        raise NotImplementedError("introspect token at <authorization-server>/introspect")


def build_auth() -> dict:
    if TRANSPORT == "stdio":
        return {}  # auth_method: none_local, the host process boundary is the trust boundary
    return {
        "token_verifier": BearerVerifier(),
        "auth": AuthSettings(
            issuer_url=os.environ["MCP_OAUTH_ISSUER"],
            resource_server_url=os.environ["MCP_RESOURCE_URL"],
            required_scopes=["files:read", "files:write"],
        ),
    }


# Rule r6: capabilities are derived only from primitives registered below; nothing implicit.
mcp = FastMCP(
    name="<spec-name>",
    instructions="Read and write files under the configured root.",
    **build_auth(),
)


def _safe(path: str) -> Path:
    target = (ROOT / path).resolve()
    if ROOT not in target.parents and target != ROOT:
        raise ValueError("path escapes MCP_ROOT")
    return target


# Rule r2: Tools = actions. Rule r5: descriptions are plain statements of what the
# tool does; no instructions to the model, no "always", no "ignore".
@mcp.tool(description="Return the UTF-8 text of a file under the served root.")
def read_file(path: str) -> str:
    return _safe(path).read_text(encoding="utf-8")


@mcp.tool(description="Overwrite a file under the served root with the given text.")
def write_file(path: str, content: str) -> str:
    target = _safe(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return f"wrote {len(content)} chars to {target.relative_to(ROOT)}"


# Rule r2: Resources = read-only data addressed by URI.
@mcp.resource("file://{path}", mime_type="text/plain")
def file_resource(path: str) -> str:
    return _safe(path).read_text(encoding="utf-8")


# Rule r2: Prompts = reusable templates the host lists to the user.
@mcp.prompt(description="Ask for a summary of one file.")
def summarize_file(path: str) -> list[base.Message]:
    return [base.UserMessage(f"Summarize the file at {path} in five bullet points.")]


if __name__ == "__main__":
    mcp.run(transport=TRANSPORT)  # type: ignore[arg-type]
