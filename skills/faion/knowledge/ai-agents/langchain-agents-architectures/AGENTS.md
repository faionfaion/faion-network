# LangChain Agent Architectures and Tools

## Summary

**One-sentence:** Picks among the three LangChain/LangGraph agent architectures — ReAct (reason+act loop), Plan-and-Execute (upfront plan + step execution), and LATS (tree search with backtracking) — and wires tools with error handlers, max_iterations caps, output truncation, and LangSmith tracing for production reliability.

**One-paragraph:** Implement tool-using agents with LangChain and LangGraph. Three architectures: ReAct (reason + act in a loop), Plan-and-Execute (plan upfront, then execute), and LATS (tree search for complex reasoning). Master tool definition, error handling, state management. ReAct is the simplest and most debuggable; Plan-and-Execute reduces error propagation on multi-step tasks; LATS adds backtracking when the solution path is uncertain. All three need max_iterations caps, tool error handlers, output truncation, and LangSmith tracing in production.

**Ефективно для:** будь-яких tool-using агентів, де потрібен повторюваний, спостережуваний паттерн з вибором архітектури під конкретну задачу.

## Applies If (ALL must hold)

- Building a tool-using agent with verifiable step-by-step reasoning.
- LangChain/LangGraph is the chosen framework.
- Tools have clear input schemas and error semantics.

## Skip If (ANY kills it)

- Single-tool, single-step retrieval — plain LLM call suffices.
- Hard latency &lt; 1s — ReAct + LATS add round-trips.
- Solution path is already known — use a deterministic pipeline.
- Tool schemas cannot be written (undocumented APIs).

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Tool inventory | List of `@tool`-decorated callables with docstrings | Application code |
| State schema | TypedDict for LangGraph state machines | Application code |
| LangSmith config | env vars or config file | Observability stack |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `idempotent-write-tools` | LangGraph retries must be safe; use idempotency keys. |
| `headless-cli-four-guards` | Agent CLIs need the four guards in production. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Six rules: cap max_iterations, handle_tool_error=True, validate plan, truncate outputs, structured supervisor, LangSmith mandatory | ~1100 |
| `content/02-output-contract.xml` | essential | Tool docstring contract + state schema + supervisor decision | ~1100 |
| `content/03-failure-modes.xml` | essential | Tool hallucination, plan staleness, LATS cost, context bloat | ~900 |
| `content/04-procedure.xml` | recommended | Architecture-pick → tools → graph → tracing | ~1000 |
| `content/05-examples.xml` | recommended | ReAct, Plan-and-Execute, LATS worked examples | ~900 |
| `content/06-decision-tree.xml` | essential | ReAct vs P&amp;E vs LATS by task shape | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Build ReAct agent | sonnet | Standard implementation |
| Design Plan-and-Execute state graph | opus | State design + re-plan logic |
| Author tool docstrings | sonnet | Docstrings are agent-facing prompts |
| LATS scoring | haiku | Constrained scoring task |

## Templates

| File | Purpose |
|------|---------|
| `templates/react-agent.py` | Minimal ReAct agent with `create_react_agent`, tools, error handling |
| `templates/_smoke-test.json` | Minimum valid tool-invocation result for self-test |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-langchain-agents-architectures.py` | Validates a tool-invocation result and confirms max_iterations + error handling are configured | Pre-commit on agent module changes |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[idempotent-write-tools]]
- [[headless-cli-four-guards]]
- [[handoff-id-payload]]

## Decision tree

See `content/06-decision-tree.xml`. Root question asks whether the solution path is uncertain. Branches route to ReAct (debuggable default), Plan-and-Execute (multi-step with upfront plan), or LATS (uncertain path with backtracking). Each leaf maps to a rule in `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/react-agent.py`

```python
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
```

### `templates/_smoke-test.json`

```json
{
  "_purpose": "smallest valid agent result for the validator",
  "_consumes": "nothing",
  "_produces": "example agent result matching content/02-output-contract.xml",
  "_depends_on": "content/01-core-rules.xml",
  "_token_budget_impact": "~50 tokens",
  "final_answer": "42",
  "iterations": 4,
  "session_id": "ses_2026_05_22_001"
}
```
