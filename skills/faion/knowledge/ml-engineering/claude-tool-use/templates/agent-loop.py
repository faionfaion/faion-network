"""
purpose: Canonical Claude agentic loop with parallel tool execution + max-turns guard.
consumes: anthropic.Anthropic client + tool list + execute_fn + user_input
produces: final text response after the loop terminates
depends-on: content/01-core-rules.xml r2-r5; content/04-procedure.xml step 3
token-budget-impact: bounded by MAX_TURNS x avg turn cost

Canonical Claude agentic loop with parallel tool execution.

Usage:
    tools = [{"name": "...", "description": "...", "input_schema": {...}}]
    result = run_agent_loop(client, tools, execute_fn, user_input)
"""
import json
from concurrent.futures import ThreadPoolExecutor
from typing import Callable
import anthropic

MODEL = "claude-sonnet-4-20250514"
MAX_TURNS = 15


def run_agent_loop(
    client: anthropic.Anthropic,
    tools: list[dict],
    execute_fn: Callable[[str, dict], str],
    user_input: str,
    system: str = "",
) -> str:
    """Run the agentic loop. Returns the final text response."""
    messages = [{"role": "user", "content": user_input}]

    for _ in range(MAX_TURNS):
        response = client.messages.create(
            model=MODEL,
            max_tokens=4096,
            system=system,
            tools=tools,
            messages=messages,
        )
        # Append full content list (includes tool_use blocks)
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason != "tool_use":
            break

        # Execute all tool calls in parallel
        tool_uses = [b for b in response.content if b.type == "tool_use"]
        with ThreadPoolExecutor() as executor:
            futures = {b.id: executor.submit(execute_fn, b.name, b.input) for b in tool_uses}

        results = [
            {"type": "tool_result", "tool_use_id": bid, "content": f.result()}
            for bid, f in futures.items()
        ]
        messages.append({"role": "user", "content": results})

    return next(
        (b.text for b in response.content if b.type == "text"),
        "",
    )


def safe_execute(name: str, input_data: dict) -> str:
    """Example tool executor — replace with real implementations."""
    try:
        if name == "example_tool":
            return json.dumps({"result": "ok"})
        return json.dumps({"error": f"Unknown tool: {name}"})
    except Exception as e:
        return json.dumps({"error": str(e), "tool": name})
