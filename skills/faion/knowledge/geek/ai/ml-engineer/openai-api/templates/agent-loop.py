# purpose: OpenAI Responses API agent loop with tool dispatch and turn cap
# consumes: tool registry + initial user message
# produces: Python agent loop emitting trace + final answer
# depends-on: content/02-output-contract.xml + content/04-procedure.xml
# token-budget-impact: medium

"""
Function-calling agent loop with tool execution.
Handles tool calls → executes → appends result → continues loop.
"""
import json
import openai
from pydantic import BaseModel


class SearchQuery(BaseModel):
    query: str
    max_results: int = 5


def handle_tool(name: str, args: dict) -> str:
    """Dispatch tool calls. Returns result as string."""
    if name == "SearchQuery":
        # Replace with actual tool implementation
        return f"Search results for: {args['query']}"
    raise ValueError(f"Unknown tool: {name}")


def agent_loop(task: str, max_steps: int = 5) -> str:
    """
    Run a function-calling agent loop.
    Returns the final text response or "max steps reached".
    """
    client = openai.OpenAI()
    tools = [openai.pydantic_function_tool(SearchQuery)]
    messages = [{"role": "user", "content": task}]

    for _ in range(max_steps):
        response = client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=messages,
            tools=tools,
            max_tokens=2048,
        )
        msg = response.choices[0].message
        messages.append(msg)

        if msg.finish_reason == "stop":
            return msg.content

        if msg.finish_reason == "length":
            raise RuntimeError("Response truncated — increase max_tokens")

        for tc in msg.tool_calls or []:
            result = handle_tool(tc.function.name, json.loads(tc.function.arguments))
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,  # Must match exactly
                "content": str(result),
            })

    return "max steps reached"
