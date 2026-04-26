# Record / Replay — Deterministic Agent Debugging

## Summary

Architect every agent with two interchangeable modes: **record** captures every LLM call, every tool input/output, and every state transition into a single trace file; **replay** re-runs the exact decision path serving LLM and tool responses from that trace, with zero external network IO. Replay is the only way to debug a 1-in-N production failure deterministically and the only way to mutate one variable (prompt, tool stub, system message) and verify the fix.

## Why

Logs and OTel traces tell you what happened, not why a specific LLM decision was made. Non-deterministic agents (temperature > 0, retries, race conditions in parallel tool calls, MCP server flakiness) cannot be debugged by re-running the same input — you get a different decision tree every time. Record/replay is the standard answer in trustworthy-AI literature (Sakura Sky 2026, debugg.ai 2025) and is implemented natively by LangGraph time-travel checkpoints, Phoenix replay sessions, and AgentOps. Without it, post-mortems devolve into log archaeology and "could not reproduce" tickets.

## When To Use

- Production debugging of intermittent agent failures.
- Building eval sets from real traffic — record once, replay many times with mutations.
- Fix verification — change one prompt token, replay, confirm the bug path is gone.
- Regression testing across model versions — replay last month's traces against the new model.

## When NOT To Use

- Pure stateless single-call generators (one LLM call, no tools) — replay overhead is not justified.
- Outputs containing PII you cannot persist — either redact in record, or skip.
- Quick prototypes where you have not yet stabilised the agent shape — instrument once the API surface is fixed.
- Tools that must hit external state (sending email, taking payment) — record but mark sideeffects as non-replayable.

## Content

| File | What's inside |
|------|---------------|
| `content/01-modes-contract.xml` | The record/replay contract: what each mode MUST capture and serve, what counts as nondeterminism, how to mark side-effects. |
| `content/02-mutation-replay.xml` | Mutation-replay loop: change one variable in a recorded trace and re-run to confirm a fix; the canonical use of replay beyond reproduction. |

## Templates

| File | Purpose |
|------|---------|
| `templates/trace-schema.json` | JSON-schema for a single recorded run — events, ordering, nondeterminism markers. |
