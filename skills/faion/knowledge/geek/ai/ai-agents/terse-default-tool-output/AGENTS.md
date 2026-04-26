# Terse-Default Tool Output, Verbosity Opt-In

## Summary

Tools default to compact, semantic output (one-line summary, Markdown table of IDs, count + top-N) and accept an explicit `format` or `verbosity` parameter so the agent can opt into raw/full payloads only when reasoning needs the detail. Verbose-by-default tool outputs are the most common cause of context blowup in long agent loops — they bury the signal the model actually uses for the next step. SkillReducer reported 48% description / 39% body compression IMPROVED downstream task quality by 2.8% — verbose context is distraction, not help.

## Why

Every token a tool returns becomes a token in the next prompt and every prompt after that until the message is summarised away. A `search_logs` that returns 50 full rows by default burns ~3-5k tokens per call, and the agent only needed timestamps and IDs to plan its next call. Concise outputs also force the tool author to do the summarisation work where it is cheap and deterministic (server-side) instead of where it is expensive and lossy (model-side). The opt-in escape hatch (`format="full"`) preserves correctness for the rare case where raw fields are load-bearing (audit, exact byte match, debug).

## When To Use

- Any tool that can return more than ~500 tokens at the upper bound: `list_*`, `search_*`, `query_*`, log queries, file listings, DB selects.
- Tools chained inside a long-running agent loop where context budget is finite.
- Tools whose output the model uses to plan a next action (only IDs + a hint matter).

## When NOT To Use

- Tools whose every field is load-bearing for the agent's reasoning (e.g., `get_payment_invoice` for an audit task) — terseness drops audit-critical data.
- Tools that return small, fixed-shape responses (`get_user(id)` returning 5 fields) — adding a verbosity knob is overhead with no win.
- Final-result tools at the end of the loop where the user wants the full answer.

## Content

| File | What's inside |
|------|---------------|
| `content/01-terse-default.xml` | The terse-default rule, summary shape, opt-in escape hatch. |

## Templates

| File | Purpose |
|------|---------|
| `templates/search_tool.py` | Reference Python tool with `format: Literal["summary","full"]`. |

## References

- https://medium.com/@shamsul.arefin/building-an-ai-agent-with-mcp-code-execution-from-confusion-to-clarity-6b13fccc8c4b
- https://arxiv.org/html/2603.29919v1
- https://www.harness.io/blog/agent-loop-new-os
