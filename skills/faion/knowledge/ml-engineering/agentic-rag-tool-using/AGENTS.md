# Agentic RAG — Tool-Using Agent

## Summary

**One-sentence:** Routes each RAG sub-query through an LLM-selected tool from a registry (vector_search, keyword_search, sql_query, web_search) and synthesises one answer from accumulated multi-source context.

**One-paragraph:** Instead of always calling the vector store, a tool-using agentic RAG lets the LLM select from a registry of retrieval tools on each step. The agent loops up to a `max_calls` budget, logs every selection decision, then asks a heavier model to synthesise a final answer from the accumulated multi-source context. Built on LangGraph / LlamaIndex `FunctionCallingAgent` primitives.

**Ефективно для:** RAG engineer who needs to fuse SQL + documents + web search behind one query — closes the gap between structured and unstructured retrieval in a single auditable loop.

## Applies If (ALL must hold)

- Questions require combining structured data (SQL/tables) with unstructured document retrieval.
- Corpus has known coverage gaps that require web_search as a fallback.
- Different query types in the same application benefit from different retrieval strategies (semantic vs exact vs structured).
- Auditable retrieval decisions are required — each tool call and its result is logged for offline debugging.

## Skip If (ANY kills it)

- Single-corpus apps where all info lives in one vector store — tool-selection overhead adds latency with no benefit.
- Data governance forbids external lookups but `web_search` is in the registry without an allow-list — security regression.
- LLM lacks reliable structured function calling — tool selection degrades to free-text parsing.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Tool registry definition | Python dict / JSON | author-supplied callables |
| Tool descriptions for the selector | text | derived from registry |
| Vector store handle | client object | `db-qdrant` / `db-chroma` |
| SQL connection (optional) | SQLAlchemy engine | application DB |
| Web search API key (optional) | env var | provider credentials |
| Model for selection | sonnet/haiku/gpt-4o-mini | application config |
| Model for synthesis | opus/sonnet/gpt-4o | application config |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/rag-engineer/rag-architecture` | Pipeline shape this agent slots into. |
| `geek/ai/llm-integration/function-calling` | Underlying mechanism the selector relies on. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: max_calls cap + log, specific tool descriptions, cheap routing model, result caching, allow-list for web_search | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for the agent's emitted trace + final answer, with valid/invalid examples | ~800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: full-results-in-selector, unrestricted web_search, ambiguous tool names, routing with heavy model | ~800 |
| `content/04-procedure.xml` | deep | 6-step procedure: define registry → write tool descriptions → run loop with cap → cache → synthesise → log | ~900 |
| `content/05-examples.xml` | medium | Worked example: ToolUsingRAG class with 4 tools answering a hybrid query | ~600 |
| `content/06-decision-tree.xml` | essential | Branch on registry-size + governance + function-calling support | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `tool-selection` | haiku | Classification task — which tool — does not need deep reasoning. |
| `intermediate-summarisation` | haiku | One-line summary per tool result for selector context. |
| `final-synthesis` | opus | Multi-source synthesis under faithfulness constraints. |
| `trace-audit` | sonnet | Reviewer pass over the selection log for compliance. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tool_using_rag.py` | Reference implementation of ToolUsingRAG with 4-tool registry, max_calls cap, result cache, and JSON trace emit. |
| `templates/output-schema.json` | JSON Schema for the agent's `{answer, trace, calls_used}` output. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agentic-rag-tool-using.py` | Validate emitted JSON trace against output schema, check call cap respected, no web_search outside allow-list. | After each agent run, before answer ships. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[rag-architecture]] — outer RAG pipeline this loop plugs into.
- [[agentic-rag-iterative-retrieval]] — sibling pattern for single-store iterative refinement.
- [[agentic-rag-query-decomposition]] — pre-step splits one user question into sub-queries.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` decides whether tool-using RAG is the right pattern at all (≥2 retrieval modalities + auditable + reliable function calling) versus collapsing to a single-store iterative agent. Branches gate `web_search` behind an explicit allow-list before any production rollout.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/tool_using_rag.py`

```python
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
```

### `templates/output-schema.json`

```json
{
  "_header": {
    "purpose": "JSON Schema for ToolUsingRAG agent output",
    "consumes": "agent emitted dict {answer, trace, calls_used, max_calls, models, violations}",
    "produces": "pass/fail validation against this schema",
    "depends-on": "content/02-output-contract.xml",
    "token-budget-impact": "small"
  },
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "faion://agentic-rag-tool-using/output.schema.json",
  "type": "object",
  "required": [
    "answer",
    "trace",
    "calls_used",
    "max_calls",
    "synthesis_model",
    "routing_model"
  ],
  "properties": {
    "answer": {
      "type": "string",
      "minLength": 1
    },
    "trace": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "iteration",
          "tool",
          "query",
          "result_summary",
          "latency_ms"
        ],
        "properties": {
          "iteration": {
            "type": "integer",
            "minimum": 1
          },
          "tool": {
            "type": "string",
            "enum": [
              "vector_search",
              "keyword_search",
              "sql_query",
              "web_search",
              "generate_answer"
            ]
          },
          "query": {
            "type": "string",
            "minLength": 1
          },
          "result_summary": {
            "type": "string",
            "maxLength": 200
          },
          "latency_ms": {
            "type": "integer",
            "minimum": 0
          },
          "cached": {
            "type": "boolean"
          }
        }
      }
    },
    "calls_used": {
      "type": "integer",
      "minimum": 1
    },
    "max_calls": {
      "type": "integer",
      "minimum": 1,
      "maximum": 10
    },
    "synthesis_model": {
      "type": "string"
    },
    "routing_model": {
      "type": "string"
    },
    "web_search_allowlist_violations": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "maxItems": 0
    }
  }
}
```
