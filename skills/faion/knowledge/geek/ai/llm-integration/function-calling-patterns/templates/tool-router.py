"""
purpose: Two-stage tool router to surface ≤20 tools per LLM call.
consumes: full tool registry + LLM call for category selection
produces: visible tool subset for a given query
depends-on: content/01-core-rules.xml r1
token-budget-impact: one extra LLM call per request (category selection)
"""
from __future__ import annotations

from typing import Any


def select_category(query: str, categories: list[str], llm_call: Any) -> str:
    """LLM-routed: pick the single best category for the query."""
    prompt = f"Categories: {categories}\nQuery: {query}\nReply with one category name exactly."
    return llm_call(prompt).strip()


def visible_tools(registry: list[dict], category: str) -> list[dict]:
    return [t for t in registry if t.get("category") == category][:20]


def route(query: str, registry: list[dict], llm_call: Any) -> list[dict]:
    categories = sorted({t["category"] for t in registry if t.get("category")})
    cat = select_category(query, categories, llm_call)
    return visible_tools(registry, cat)
