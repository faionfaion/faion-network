# Iteration-capped tool loop for OpenAI function calling
# Usage: call agent_loop(client, messages, tools, registry)

import json
from typing import Any, Callable, Dict, List, Optional


def agent_loop(
    client,
    messages: List[Dict],
    tools: List[Dict],
    tool_registry: Dict[str, Callable],
    model: str = "gpt-4o",
    max_iter: int = 10,
) -> Optional[str]:
    """Run OpenAI tool-use loop with hard iteration cap.

    Returns the final text response, or "[max_iterations_reached]" if the
    cap is hit. Never raises on tool execution errors — returns error dict.
    """
    for _ in range(max_iter):
        resp = client.chat.completions.create(
            model=model, messages=messages, tools=tools
        )
        msg = resp.choices[0].message
        messages.append(msg)

        if not msg.tool_calls:
            return msg.content

        for tc in msg.tool_calls:
            fn_name = tc.function.name
            try:
                args: Dict[str, Any] = json.loads(tc.function.arguments)
            except json.JSONDecodeError as exc:
                args = {}
                result: Any = {"error": f"malformed arguments: {exc}"}
            else:
                fn = tool_registry.get(fn_name)
                if fn is None:
                    result = {"error": f"unknown tool: {fn_name}"}
                else:
                    try:
                        result = fn(**args)
                    except Exception as exc:
                        result = {"error": str(exc)}

            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": json.dumps(result),
            })

    return "[max_iterations_reached]"
