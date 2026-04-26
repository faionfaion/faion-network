"""ToolRouter: register tools, build definitions, execute with agentic loop.

Usage:
    router = ToolRouter(client)
    router.register("get_weather", "Get weather. Call when user asks about weather.", params, fn)
    result = router.execute("What's the weather in Tokyo?")
"""
import json
from typing import Callable
import anthropic

client = anthropic.Anthropic()


class ToolRouter:
    """Register tools and execute queries with an agentic loop."""

    def __init__(self, max_iterations: int = 10):
        self.max_iterations = max_iterations
        self._tools: list[dict] = []
        self._impls: dict[str, Callable] = {}

    def register(self, name: str, description: str, parameters: dict, fn: Callable):
        """Register a tool. Description must answer 'when to call this'."""
        self._tools.append({
            "name": name,
            "description": description,
            "input_schema": parameters,
        })
        self._impls[name] = fn

    def execute(self, query: str, model: str = "claude-sonnet-4-20250514") -> dict:
        """Execute query using registered tools. Returns {response, iterations}.

        Args:
            query: User's question or task.
            model: Claude model ID to use.

        Returns:
            dict with keys: response (str), iterations (int), tool_calls (list).
        """
        messages = [{"role": "user", "content": query}]
        tool_history = []

        for i in range(self.max_iterations):
            resp = client.messages.create(
                model=model,
                max_tokens=4096,
                tools=self._tools,
                messages=messages,
            )
            if resp.stop_reason == "end_turn":
                return {"response": resp.content[0].text, "iterations": i + 1,
                        "tool_calls": tool_history}
            # Handle tool_use
            messages.append({"role": "assistant", "content": resp.content})
            tool_results = []
            for block in resp.content:
                if block.type == "tool_use":
                    try:
                        result = self._impls[block.name](**block.input)
                    except Exception as e:
                        result = {"error": str(e), "code": "TOOL_ERROR"}
                    tool_history.append({"tool": block.name, "result": result})
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result)[:8000],
                    })
            messages.append({"role": "user", "content": tool_results})

        raise RuntimeError(f"max_iterations={self.max_iterations} reached")
