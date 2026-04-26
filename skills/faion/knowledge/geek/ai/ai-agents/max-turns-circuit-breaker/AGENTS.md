# Max-Turns as Circuit Breaker, Not Error

## Summary

Set an explicit `max_turns` on every production agent run (5-10 for retrieval, 15-20 for coding agents) and CATCH the resulting `MaxTurnsExceeded` exception. On catch, hand the partial trajectory to a cheap recovery model that summarizes what was tried and asks the user to clarify, instead of bubbling a 500. Hard turn caps are the only deterministic stop for tool-calling loops that fail by silently consuming budget.

## Why

Tool-calling loops fail open: each tool result still looks like "progress" to the model, so it keeps proposing actions ("call search → no results → call search again with same query"). Token spend grows linearly per turn while the user sees nothing. The OpenAI Agents SDK default of `max_turns=10` (Python) / 25 (JS) is a footgun — too low for coding agents, too high for retrieval. A turn cap paired with an exception handler converts a runaway loop into a structured fallback: partial trace preserved for debugging, graceful answer for the user, no 500.

## When To Use

- Every `Runner.run` / agent-loop invocation that calls tools.
- Retrieval agents (cap 5-10 turns) and code-editing agents (cap 15-20).
- Production deployments where budget is finite and silent loops drain credit.
- Multi-tenant SaaS where one stuck loop can starve others of rate-limit headroom.

## When NOT To Use

- Long-running async coding agents in sandboxes designed for hundreds of turns — use checkpoint + human approval instead, not a single max-turns.
- Chat completions with no tool use — the model already terminates on first non-tool reply.
- Workflows where the cap is an unrecoverable error (DB transaction half-applied) — solve with idempotency, not a turn cap.

## Content

| File | What's inside |
|------|---------------|
| `content/01-cap-and-catch.xml` | The cap-and-catch rule, sizing guidance, recovery handler pattern. |

## Templates

| File | Purpose |
|------|---------|
| `templates/recovery_handler.py` | Reference pattern: catch `MaxTurnsExceeded`, summarize trajectory with cheap model, return graceful reply. |
