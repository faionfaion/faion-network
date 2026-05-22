# purpose: runtime middleware that auto-evicts oversized tool results to scratch storage
# consumes: tool runtime, tokeniser, scratch path
# produces: agent sees only typed pointer {path, preview, total_tokens, evicted:true}
# depends-on: content/01-core-rules.xml; paired read_file(path,lines) tool
# token-budget-impact: cuts oversized tool returns from N tokens → ~150 tokens (preview + pointer)
"""Minimal eviction middleware for agent tool runtimes.

Usage:
    @evict(threshold=20_000, scratch="/tmp/agent")
    def my_tool(...): ...

Pair with a `read_file(path, lines)` tool exposed to the agent so it can
recover slices on demand. Source pattern: LangChain Deep Agents
filesystemMiddleware (`toolTokenLimitBeforeEvict`, default 20000).
"""

from __future__ import annotations

import functools
import json
import uuid
from pathlib import Path
from typing import Any, Callable


def count_tokens(text: str) -> int:
    """Replace with your tokeniser (tiktoken, anthropic, etc.)."""
    # Cheap heuristic: ~4 chars per token.
    return max(1, len(text) // 4)


def evict(
    threshold: int = 20_000,
    scratch: str = "/tmp/agent",
    preview_chars: int = 400,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    Path(scratch).mkdir(parents=True, exist_ok=True)

    def decorator(tool: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(tool)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            raw = tool(*args, **kwargs)
            text = raw if isinstance(raw, str) else json.dumps(raw)
            n = count_tokens(text)
            if n <= threshold:
                return raw
            path = Path(scratch) / f"{tool.__name__}_{uuid.uuid4().hex}.txt"
            path.write_text(text)
            return {
                "path": str(path),
                "preview": text[:preview_chars],
                "total_tokens": n,
                "evicted": True,
            }

        return wrapper

    return decorator


def read_file(path: str, start: int = 0, end: int | None = None) -> str:
    """Recovery tool — agent calls this to pull a slice from an evicted result."""
    lines = Path(path).read_text().splitlines()
    return "\n".join(lines[start:end])
