# Cached system prompt + tool-use agent loop with MAX_TURNS guard
import random
import time

import anthropic

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env

# System prompt must be >= 1024 tokens to qualify for caching
SYSTEM = [
    {
        "type": "text",
        "text": "You are a production assistant with access to tools. "
                "Always reason step-by-step before calling a tool. "
                "When you have enough information to answer, respond directly without calling more tools.",
        # NOTE: for real cache benefit this block must be >= 1024 tokens.
        # Append your large static context (retrieved documents, tool descriptions, domain rules) here.
        "cache_control": {"type": "ephemeral"},
    }
]

TOOLS = [
    {
        "name": "search",
        "description": "Search the knowledge base. Returns a list of relevant passages.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query string"},
                "top_k": {"type": "integer", "description": "Number of results to return", "default": 5},
            },
            "required": ["query"],
        },
    },
]

MAX_TURNS = 10


def execute_tool(name: str, tool_input: dict) -> str:
    """Dispatch tool calls. Replace with real implementations."""
    if name == "search":
        return f"[search results for: {tool_input['query']}]"
    return f"[unknown tool: {name}]"


def call_with_retry(fn, max_retries: int = 5):
    """Exponential backoff with jitter for rate limits and 5xx errors."""
    for attempt in range(max_retries):
        try:
            return fn()
        except anthropic.RateLimitError:
            if attempt == max_retries - 1:
                raise
            wait = min(2 ** attempt + random.uniform(0, 1), 60)
            time.sleep(wait)
        except anthropic.APIError as e:
            if e.status_code >= 500:
                if attempt == max_retries - 1:
                    raise
                wait = min(2 ** attempt + random.uniform(0, 1), 60)
                time.sleep(wait)
            else:
                raise
    raise RuntimeError("Max retries exceeded")


def run_agent(user_message: str) -> str:
    messages = [{"role": "user", "content": user_message}]
    cache_hits = 0

    for turn in range(MAX_TURNS):
        response = call_with_retry(
            lambda: client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4096,
                system=SYSTEM,
                tools=TOOLS,
                messages=messages,
            )
        )

        cache_hits += getattr(response.usage, "cache_read_input_tokens", 0)

        if response.stop_reason == "end_turn":
            for block in response.content:
                if hasattr(block, "text"):
                    return block.text
            return ""

        if response.stop_reason != "tool_use":
            break

        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                result = execute_tool(block.name, block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result,
                })

        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})

    raise RuntimeError(f"Agent did not reach end_turn after {MAX_TURNS} turns")


if __name__ == "__main__":
    answer = run_agent("What is our refund policy for digital products?")
    print(answer)
