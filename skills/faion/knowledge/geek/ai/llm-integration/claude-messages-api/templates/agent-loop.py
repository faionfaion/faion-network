# purpose: TBD-template-header
# consumes: input from methodology
# produces: output artefact
# depends-on: 01-core-rules.xml
# token-budget-impact: small

"""
Multi-turn Claude agent loop with explicit stop_reason branching.

Usage:
    result = agent_loop(client, system="You are a helpful assistant.",
                        initial_prompt="What is 2+2?")
"""
import anthropic

MODEL = "claude-sonnet-4-20250514"


def handle_tools(assistant_content: list) -> list:
    """Execute tool calls and return tool_result list. Override with real logic."""
    results = []
    for block in assistant_content:
        if block.type == "tool_use":
            results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": f"Tool {block.name} not implemented",
            })
    return results


def agent_loop(
    client: anthropic.Anthropic,
    system: str,
    initial_prompt: str,
    tools: list | None = None,
    max_turns: int = 10,
) -> str:
    """Run multi-turn agent loop. Returns final text response."""
    messages = [{"role": "user", "content": initial_prompt}]

    for _ in range(max_turns):
        kwargs = {"model": MODEL, "max_tokens": 4096, "system": system, "messages": messages}
        if tools:
            kwargs["tools"] = tools

        resp = client.messages.create(**kwargs)
        # Always append full content list to preserve tool_use blocks
        messages.append({"role": "assistant", "content": resp.content})

        if resp.stop_reason == "end_turn":
            return resp.content[0].text
        elif resp.stop_reason == "max_tokens":
            raise RuntimeError("Response truncated — increase max_tokens or split task")
        elif resp.stop_reason == "tool_use":
            tool_results = handle_tools(resp.content)
            messages.append({"role": "user", "content": tool_results})
        else:
            break

    return next((b.text for b in resp.content if b.type == "text"), "")
