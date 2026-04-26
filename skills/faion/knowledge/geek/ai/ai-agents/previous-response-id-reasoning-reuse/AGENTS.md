# previous_response_id — Reasoning-Item Reuse on the Responses API

## Summary

When chaining turns of an OpenAI reasoning model (o3, o4-mini, gpt-5) on the Responses API, pass `previous_response_id=<prior.id>` instead of reconstructing a Chat-Completions–style message array. The Responses API keeps reasoning items adjacent to their function calls server-side, keyed by id; supplying the id reattaches them on the next turn. This preserves the model's mid-loop "thinking", lifts cache-hit rate, and cuts both latency and tokens. Under ZDR (`store=false`), use the encrypted-content variant instead — `previous_response_id` is silently ignored.

## Why

Reasoning items are not just chat messages — they are intermediate scratchpad tokens the model produced between tool calls. The legacy approach (Chat Completions) flattens them away and the model "thinks from scratch" on every turn, producing a 20-40% regression on agentic benchmarks (OpenAI cookbook + community measurements). The Responses API was specifically designed to keep these items co-located with the call/response pair they justify; opting in via `previous_response_id` is the only supported way to inherit them on the next turn for stateful (`store=true`) deployments.

## When To Use

- Multi-turn agent loops on o3, o4-mini, or gpt-5 where the model calls tools and you feed results back.
- Conversational reasoning agents where consecutive user turns continue the same task.
- Long planning loops where mid-trajectory thoughts inform later decisions.
- Anywhere you previously paid for "re-thinking" by reconstructing message arrays manually.

## When NOT To Use

- Non-reasoning models (gpt-4.1, gpt-4.1-mini) — there are no reasoning items to reuse.
- ZDR / `store=false` deployments — the id is silently ignored; use `include=["reasoning.encrypted_content"]` and round-trip the blob (see encrypted-reasoning pattern).
- First turn of a session — there is no prior id yet; pass the user message normally.
- Cross-session continuation — reasoning items expire; do not assume yesterday's id still resolves.

## Content

| File | What's inside |
|------|---------------|
| `content/01-rule.xml` | Core rule, the request shape, why manual message arrays drop reasoning items. |
| `content/02-zdr-fallback.xml` | When `store=false`: encrypted-content fallback and why `previous_response_id` is ignored. |

## Templates

| File | Purpose |
|------|---------|
| `templates/responses-loop.py` | Working agent loop using `previous_response_id` plus a ZDR fallback branch. |
