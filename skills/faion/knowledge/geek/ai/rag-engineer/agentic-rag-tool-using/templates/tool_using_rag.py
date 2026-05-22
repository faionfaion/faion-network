# purpose: reference implementation for tool-using agentic RAG with cap + log + cache
# consumes: tool registry (dict[str, Callable]), routing/synthesis models, allowlist
# produces: dict {answer, trace, calls_used, max_calls, models, allowlist_violations}
# depends-on: content/01-core-rules.xml, content/02-output-contract.xml
# token-budget-impact: medium (one routing call per iteration, one synthesis call)
"""Reference ToolUsingRAG skeleton — see content/05-examples.xml for the full body."""
from __future__ import annotations

import time
from typing import Callable


class ToolUsingRAG:
    """Tool-using agentic RAG with bounded loop, intra-run cache, allow-listed web_search."""

    def __init__(
        self,
        registry: dict[str, Callable[[str], list[dict]]],
        routing_model: str = "claude-3-haiku-20240307",
        synthesis_model: str = "claude-3-5-sonnet-20241022",
        max_calls: int = 3,
        web_search_allowlist: list[str] | None = None,
    ) -> None:
        self.registry = registry
        self.routing_model = routing_model
        self.synthesis_model = synthesis_model
        self.max_calls = max_calls
        self.allowlist = set(web_search_allowlist or [])

    def answer(self, query: str) -> dict:
        trace: list[dict] = []
        cache: dict[tuple[str, str], list[dict]] = {}
        violations: list[str] = []
        for i in range(1, self.max_calls + 1):
            tool = self._select_tool(query, trace)
            if tool == "generate_answer":
                break
            key = (tool, query.strip().lower())
            if key in cache:
                result, cached, latency = cache[key], True, 0
            else:
                t0 = time.perf_counter()
                result = self.registry[tool](query)
                latency = int((time.perf_counter() - t0) * 1000)
                cache[key] = result
                cached = False
                if tool == "web_search":
                    violations += [r["source"] for r in result if not self._allowed(r.get("source", ""))]
            trace.append({
                "iteration": i,
                "tool": tool,
                "query": query,
                "result_summary": self._summarise(result)[:200],
                "latency_ms": latency,
                "cached": cached,
            })
        return {
            "answer": self._synthesise(query, trace),
            "trace": trace,
            "calls_used": len(trace),
            "max_calls": self.max_calls,
            "synthesis_model": self.synthesis_model,
            "routing_model": self.routing_model,
            "web_search_allowlist_violations": violations,
        }

    def _allowed(self, url: str) -> bool:
        return any(url.startswith(domain) for domain in self.allowlist)

    def _summarise(self, result: list[dict]) -> str:
        if not result:
            return "no results"
        top = result[0]
        return f"hits={len(result)} top_score={top.get('score', 0):.2f} snippet={top.get('text', '')[:80]}"

    def _select_tool(self, query: str, trace: list[dict]) -> str:
        raise NotImplementedError("wire routing model call here")

    def _synthesise(self, query: str, trace: list[dict]) -> str:
        raise NotImplementedError("wire synthesis model call here")
