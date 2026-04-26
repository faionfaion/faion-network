# Handoff Payload — ID + Minimal Metadata

## Summary

When agent A hands off to agent B in a multi-agent topology, the handoff payload is a structured `{task_id, target_agent, decision_metadata}` object — never the conversation history, never the raw input. Agent B reads the actual task state from a shared store (file, queue, DB) keyed by `task_id`. The supervising router returns `SupervisorDecision` objects, not message threads. Each agent's context is sized to its job, not to the cumulative conversation.

## Why

Naively forwarding the conversation between roles ("here is everything we said so far, now you handle it") is the single biggest cause of context blow-up in multi-agent systems. By turn 4, every agent in the chain is reading every prior agent's reasoning, even though most of it is irrelevant to the next role. The OpenAI Agents SDK and LangChain handoffs API both treat handoffs as structured edges with a typed payload, not as message forwarding. NERO's mesh runs on this: a classifier returns `{route: "neromedia", task_id: "t_8821"}` and the worker pulls the article body from `/srv/nero/queue/t_8821.json` — the classifier's context never carries the article at all.

## When To Use

- Multi-agent meshes with role-specialized agents (researcher → writer → editor; classifier → worker).
- Supervisor/worker topologies where the supervisor's only job is routing.
- Long pipelines where each step's relevant context is a small subset of cumulative state.
- Cron-triggered or event-driven agents where the trigger has no conversation to pass on.

## When NOT To Use

- Single-agent loops — the "handoff" is a no-op; adding a store is pure overhead.
- Tightly-coupled co-reasoning where two agents must see each other's intermediate thoughts (use a fork/shared context instead).
- Throwaway prototypes where setting up a task store is more work than the agent itself.

## Content

| File | What's inside |
|------|---------------|
| `content/01-payload-shape.xml` | The required handoff payload schema; what stays in vs. out. |
| `content/02-shared-store.xml` | How the receiving agent retrieves task state by ID; store invariants. |

## Templates

| File | Purpose |
|------|---------|
| `templates/handoff.json` | JSON Schema for the handoff payload object. |
| `templates/supervisor-decision.json` | JSON Schema for the supervisor router's structured output. |
