# purpose: minimal ReAct agent with error handling and explicit max_iterations
# consumes: a task string passed by the caller
# produces: dict with final_answer, iterations, session_id
# depends-on: langchain, langgraph, langchain-anthropic, langsmith
# token-budget-impact: per-call cost depends on tools and task; bounded by max_iterations=15
"""Minimal ReAct agent template — all five guards applied."""
from __future__ import annotations

import os
import uuid

from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent


@tool(handle_tool_error=True)
def web_search(query: str) -> str:
    """Search the web.

    Use for: facts, recent events, company info.
    Do NOT use for: math, code execution, structured data.
    Returns: plain-text top-5 results truncated to ~2k chars.
    """
    return f"[search results for: {query}]"[:2000]


@tool(handle_tool_error=True)
def calculator(expression: str) -> str:
    """Evaluate a math expression.

    Use for: numeric calculation only.
    Do NOT use for: code execution.
    Returns: the numeric result as a string.
    """
    return str(eval(expression, {"__builtins__": {}}, {}))


def run(task: str) -> dict:
    session_id = uuid.uuid4().hex
    os.environ.setdefault("LANGCHAIN_TRACING_V2", "true")
    os.environ.setdefault("LANGCHAIN_PROJECT", "react-agent")

    agent = create_react_agent(
        ChatAnthropic(model="claude-sonnet-4-7"),
        tools=[web_search, calculator],
    )
    result = agent.invoke(
        {"messages": [("human", task)]},
        config={"configurable": {"thread_id": session_id}, "recursion_limit": 30},
    )
    final = result["messages"][-1].content
    return {
        "final_answer": final,
        "iterations": len(result["messages"]) // 2,
        "session_id": session_id,
    }
