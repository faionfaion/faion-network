# Map-Reduce Fan-Out with Bounded Concurrency and Idempotent Branches

## Summary

Use dynamic fan-out (`Send(node, payload)` in LangGraph, `ParallelAgent` in ADK, `asyncio.gather` in plain Python) to map a per-item LLM call across a list, then reduce with an annotated reducer (`Annotated[list, operator.add]` or a custom merge). Cap concurrency at ≤20 to avoid rate-limit cliffs, and design every branch to be idempotent + retryable because any single branch failure fails the entire super-step atomically. Never use map-reduce fan-out for branches that mutate shared external state — use a queue + workers instead.

## Why

Latency in agent stacks is dominated by serialized LLM calls. For embarrassingly parallel work (per-document scoring, multi-source RAG, multi-candidate generation, batch tool calls over a list), map-reduce drops wall time from `O(N · turn)` to `O(turn)` — a 5-20× latency win on N=20 — and lets you route each branch to a cheaper model (Haiku per item, Sonnet for the reduce). The constraints exist because rate-limit cliffs are real (most providers rate-limit hard at 60-300 req/s, and parallel branches share that budget) and because LangGraph's super-step semantics fail atomically — a non-idempotent branch on the failing path produces a half-applied side effect on retry.

## When To Use

- Per-document scoring or classification across N documents.
- Multi-source RAG fan-out (vector search + web search + memory lookup, then merge).
- Multi-candidate generation (sample N drafts, pick best with a reducer / vote).
- Batch tool calls over a list (enrich N rows, classify N emails) where each item is independent.

## When NOT To Use

- Fixed-N parallel where N is known at graph-compile time — use static fan-out edges; Send is for runtime-variable N.
- Branches that mutate shared external state (write to the same DB row, append to one file) — use a queue + workers, not Send. Atomic-fail of the super-step double-applies on retry.
- N > 20 with a single provider — split into batches, otherwise rate-limit kills the run; or move to provider Batch API.
- Strong consistency requirements across branches (every branch must see the same prior state) — use sequential.

## Content

| File | What's inside |
|------|---------------|
| `content/01-fanout-shape.xml` | Send / Parallel pattern, reducer choice, concurrency cap, idempotency requirement. |

## Templates

| File | Purpose |
|------|---------|
| `templates/send_fanout.py` | LangGraph reference: router emits `Send(...)` per item, reducer aggregates with `operator.add`. |
