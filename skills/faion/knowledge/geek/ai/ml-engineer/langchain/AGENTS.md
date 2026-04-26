# LangChain

## Summary

LangChain (LCEL pipe syntax) and LangGraph (state machine framework) for building production AI chains and agents. LangChain handles standard tool-calling agents via `create_react_agent()` and composable pipelines via `prompt | model | parser`. LangGraph adds durable state, checkpointing, human-in-the-loop interrupts, and multi-agent Supervisor patterns for complex control flow.

## Why

LangChain provides provider-agnostic wiring, built-in retry/fallback, and LangSmith observability out of the box. LangGraph's state machine model solves the hardest agent problems: surviving process restarts, pausing for human approval before irreversible actions, and debugging non-linear workflows via time-travel replay.

## When To Use

- Multi-step AI workflows where each step's output feeds the next (LCEL pipe chains)
- Standard ReAct tool-calling agent with 3-10 tools (`create_react_agent()` covers 80% of use cases)
- Complex control flow: human-in-the-loop, conditional branching, retry logic (LangGraph)
- Long-running workflows that must survive process restarts (LangGraph checkpointing)
- Multi-agent Supervisor → Worker patterns with role specialization
- RAG pipelines requiring custom retrieval → reranking → synthesis chains

## When NOT To Use

- Single LLM call — use the provider SDK directly (anthropic, openai); LangChain adds 50-200ms overhead
- Document-centric RAG with complex index types — LlamaIndex has better RAG abstractions
- Simple prompt templates — Python f-strings or Jinja2 avoid the dependency
- High-throughput inference (&gt;100 RPS) — LangChain Python overhead becomes measurable

## Content

| File | What's inside |
|------|---------------|
| `content/01-lcel-chains.xml` | LCEL syntax, chain patterns (sequential, router, fallback), structured output, streaming |
| `content/02-langgraph-agents.xml` | LangGraph StateGraph, nodes, conditional edges, checkpointing, human-in-the-loop |
| `content/03-gotchas.xml` | Known failure modes: deprecated patterns, unlimited iterations, serialization, async pitfalls |

## Templates

| File | Purpose |
|------|---------|
| `templates/langgraph-supervisor.py` | Supervisor pattern with conditional edge routing and state accumulation |
| `templates/langgraph-router-node.py` | Structured-output routing node using `with_structured_output` |
