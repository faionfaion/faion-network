"""
purpose: Python MCP client + tool-bridge skeleton.
consumes: see AGENTS.md ## Prerequisites
produces: code
depends-on: content/02-output-contract.xml schema for mcp-client-integration
token-budget-impact: ≤500 tokens to fill
"""
# mcp>=1.10 (official Python SDK). The SDK is async-only; everything else here is
# straight-line. Bridge target: Anthropic Messages tool schema (anthropic>=0.40).
# Env vars: MCP_AUDIT_LOG (jsonl path), plus whatever each allow-listed server declares.
from __future__ import annotations

import asyncio
import hashlib
import json
import os
import time
from contextlib import AsyncExitStack
from dataclasses import dataclass, field

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Rule r1: allow-list. Anything not here never launches.
# Rule r3: `env` is the full subprocess environment; pass only declared variables.
ALLOW_LIST: dict[str, StdioServerParameters] = {
    "filesystem": StdioServerParameters(
        command="npx", args=["-y", "@modelcontextprotocol/server-filesystem", "<workspace-dir>"], env={}
    ),
    "github": StdioServerParameters(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-github"],
        env={"GITHUB_PERSONAL_ACCESS_TOKEN": os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN", "")},
    ),
}
AUDIT_LOG = os.environ.get("MCP_AUDIT_LOG", "logs/mcp-audit.jsonl")


def ask_user_consent(server: str, tool: str, description: str) -> bool:
    """Rule r2 / r5: consent UI shows the description as untrusted server text, in its own surface."""
    print(f"[mcp:{server}] tool '{tool}' wants to run. Server says: {description!r}")
    return input("allow for this session? [y/N] ").strip().lower() == "y"


@dataclass
class McpBridge:
    caller_session: str
    sessions: dict[str, ClientSession] = field(default_factory=dict)
    tools: tuple[dict, ...] = ()          # rule r4: frozen after first list
    consented: set[str] = field(default_factory=set)

    async def connect(self, stack: AsyncExitStack) -> None:
        for name, params in ALLOW_LIST.items():
            read, write = await stack.enter_async_context(stdio_client(params))
            session = await stack.enter_async_context(ClientSession(read, write))
            await session.initialize()
            self.sessions[name] = session
        self.tools = tuple(await self._list_tools())

    async def _list_tools(self) -> list[dict]:
        bridged: list[dict] = []
        for server, session in self.sessions.items():
            for tool in (await session.list_tools()).tools:
                bridged.append({
                    "name": f"{server}__{tool.name}",          # server prefix defeats lookalikes
                    "description": tool.description or "",     # rule r5: shown in UI, not system prompt
                    "input_schema": tool.inputSchema,
                })
        return bridged

    def sdk_tools(self) -> list[dict]:
        """Hand this list to the model SDK's `tools=` parameter unchanged."""
        return list(self.tools)

    async def call(self, bridged_name: str, arguments: dict) -> str:
        if bridged_name not in {t["name"] for t in self.tools}:
            raise PermissionError(f"tool not in frozen bridge: {bridged_name}")  # rule r4
        server, tool = bridged_name.split("__", 1)
        if bridged_name not in self.consented:
            desc = next(t["description"] for t in self.tools if t["name"] == bridged_name)
            if not ask_user_consent(server, tool, desc):
                self._audit(server, tool, arguments, "denied")
                return "user denied tool call"
            self.consented.add(bridged_name)               # rule r2: cache per session
        result = await self.sessions[server].call_tool(tool, arguments)
        self._audit(server, tool, arguments, "error" if result.isError else "ok")
        # Rule r5 of mcp-security: tool output is data; return it as a string, never re-prompt raw.
        return "\n".join(c.text for c in result.content if getattr(c, "type", "") == "text")

    def _audit(self, server: str, tool: str, arguments: dict, outcome: str) -> None:
        """Rule r6: server_id + tool_name + caller_session + timestamp per call."""
        os.makedirs(os.path.dirname(AUDIT_LOG) or ".", exist_ok=True)
        with open(AUDIT_LOG, "a", encoding="utf-8") as fh:
            fh.write(json.dumps({
                "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "server_id": server,
                "tool_name": tool,
                "caller_session": self.caller_session,
                "arguments_hash": hashlib.sha256(json.dumps(arguments, sort_keys=True).encode()).hexdigest(),
                "outcome": outcome,
            }) + "\n")


async def main() -> None:
    async with AsyncExitStack() as stack:
        bridge = McpBridge(caller_session="<session-id>")
        await bridge.connect(stack)
        print(json.dumps([t["name"] for t in bridge.sdk_tools()], indent=2))
        # Model loop: pass bridge.sdk_tools() to the SDK; on tool_use -> await bridge.call(name, input).


if __name__ == "__main__":
    asyncio.run(main())
