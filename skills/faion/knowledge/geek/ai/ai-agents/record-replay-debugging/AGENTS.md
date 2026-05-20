---
slug: record-replay-debugging
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Architect every agent with two interchangeable modes: record captures every LLM call, every tool input/output, and every state transition into a single trace file; replay re-runs the exact decision path serving LLM and tool responses from that trace, with zero external network IO.
content_id: "32db7a60667c7e6f"
tags: [debugging, determinism, testing, reproducibility, agents]
---
# Record / Replay — Deterministic Agent Debugging

## Summary

**One-sentence:** Architect every agent with two interchangeable modes: record captures every LLM call, every tool input/output, and every state transition into a single trace file; replay re-runs the exact decision path serving LLM and tool responses from that trace, with zero external network IO.

**One-paragraph:** Architect every agent with two interchangeable modes: record captures every LLM call, every tool input/output, and every state transition into a single trace file; replay re-runs the exact decision path serving LLM and tool responses from that trace, with zero external network IO. Replay is the only way to debug a 1-in-N production failure deterministically and the only way to mutate one variable (prompt, tool stub, system message) and verify the fix.

## Applies If (ALL must hold)

- Production debugging of intermittent agent failures.
- Building eval sets from real traffic — record once, replay many times with mutations.
- Fix verification — change one prompt token, replay, confirm the bug path is gone.
- Regression testing across model versions — replay last month's traces against the new model.

## Skip If (ANY kills it)

- Pure stateless single-call generators (one LLM call, no tools) — replay overhead is not justified.
- Outputs containing PII you cannot persist — either redact in record, or skip.
- Quick prototypes where you have not yet stabilised the agent shape — instrument once the API surface is fixed.
- Tools that must hit external state (sending email, taking payment) — record but mark sideeffects as non-replayable.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `geek/ai/ai-agents/`
