"""
purpose: Batched Claude Agent SDK classifier — numeric IDs, single forced tool call, cache-friendly.
consumes: list of items + system_prompt (byte-identical) + batch_size <=10
produces: list of {n, verdict} matched by id
depends-on: content/01-core-rules.xml r3, r4, r5, r6
token-budget-impact: O(N/batch_size) calls; cache reuses system prefix across batches
"""
from __future__ import annotations

import asyncio

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ToolUseBlock,
    create_sdk_mcp_server,
    query,
    tool,
)

SYSTEM_PROMPT = "You are an auditor. Reply only via the verdicts tool."  # byte-identical across batches

VERDICTS_SCHEMA = {
    "type": "object",
    "properties": {
        "results": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {"n": {"type": "integer"}, "sufficient": {"type": "boolean"}},
                "required": ["n", "sufficient"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["results"],
}


@tool("verdicts", "Sufficiency for each numbered document", VERDICTS_SCHEMA)
async def verdicts_tool(args):
    return {"content": [{"type": "text", "text": "ok"}]}


async def classify_batch(items: list[str], batch_size: int = 10) -> list[dict]:
    assert batch_size <= 15, "batch_size > 15 triggers silent truncation (rule r5)"
    server = create_sdk_mcp_server(name="audit", version="0.1.0", tools=[verdicts_tool])
    options = ClaudeAgentOptions(
        model="claude-sonnet-4-6",
        system_prompt=SYSTEM_PROMPT,  # str replaces SDK preset
        setting_sources=[],  # no CLAUDE.md / AGENTS.md auto-load
        mcp_servers={"audit": server},
        allowed_tools=["mcp__audit__verdicts"],
        disallowed_tools=["ToolSearch"],
        permission_mode="bypassPermissions",
        max_turns=2,  # SDK floor
    )
    results: list[dict] = []
    for start in range(0, len(items), batch_size):
        chunk = items[start : start + batch_size]
        prompt = "\n\n".join(f'<doc n="{i + 1}">\n{body}\n</doc>' for i, body in enumerate(chunk))
        async for msg in query(prompt=prompt, options=options):
            if isinstance(msg, AssistantMessage):
                for block in msg.content:
                    if isinstance(block, ToolUseBlock) and block.name == "verdicts":
                        for entry in block.input.get("results", []):
                            entry["n"] = entry["n"] + start  # global index
                            results.append(entry)
    return results


if __name__ == "__main__":
    asyncio.run(classify_batch(["sample 1", "sample 2"]))
