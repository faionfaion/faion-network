"""Anthropic-format parallel tool executor with ThreadPoolExecutor and timeout.

Usage:
    tool_results = run_tools_parallel(response.content, TOOL_REGISTRY)
    messages.append({"role": "user", "content": tool_results})
"""
import concurrent.futures
import json


def run_tools_parallel(
    tool_blocks: list,
    registry: dict,
    timeout: int = 30,
    max_result_chars: int = 8000,
) -> list[dict]:
    """Execute all tool_use blocks in parallel. Returns tool_result list.

    Args:
        tool_blocks: List of content blocks from Claude response. Non-tool blocks ignored.
        registry: Dict mapping tool name to callable.
        timeout: Per-tool execution timeout in seconds.
        max_result_chars: Truncate results longer than this (approx 2000 tokens).

    Returns:
        List of tool_result dicts in Anthropic format.
    """
    tool_calls = [b for b in tool_blocks if b.type == "tool_use"]
    results = []

    with concurrent.futures.ThreadPoolExecutor() as ex:
        futures = {
            ex.submit(registry[tc.name], **tc.input): tc
            for tc in tool_calls
            if tc.name in registry
        }
        unknown = [tc for tc in tool_calls if tc.name not in registry]

        for future, tc in futures.items():
            try:
                result = future.result(timeout=timeout)
            except concurrent.futures.TimeoutError:
                result = {"error": f"timeout after {timeout}s", "code": "TIMEOUT"}
            except Exception as e:
                result = {"error": str(e), "code": "TOOL_ERROR"}
            content = json.dumps(result)[:max_result_chars]
            results.append({"type": "tool_result", "tool_use_id": tc.id, "content": content})

        for tc in unknown:
            results.append({
                "type": "tool_result",
                "tool_use_id": tc.id,
                "content": json.dumps({"error": f"unknown tool: {tc.name}", "code": "UNKNOWN_TOOL"}),
            })

    return results
