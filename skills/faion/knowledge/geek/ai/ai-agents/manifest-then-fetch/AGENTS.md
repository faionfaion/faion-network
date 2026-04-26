# Manifest-Then-Fetch — Two-Phase Tool Result

## Summary

A tool-result protocol where every tool returns a small manifest first (`{execution_id, preview, size_tokens}`) and the full payload is stored externally. The agent inspects only the preview; it must explicitly call `get_full_result(execution_id)` to load the body. Default behaviour is preview-only — large payloads never enter the LLM context unless the agent decides they are needed.

## Why

Tool calls have heavy-tailed payload sizes: a `sql_query` or `web_fetch` is small most of the time but occasionally returns hundreds of kilobytes. Stuffing every full result into the conversation triggers "lost in the middle" degradation and burns prompt-cache prefixes. The Maximum Effective Context Window paper (arXiv 2509.21361) shows accuracy collapses far below the advertised window, so the cheapest way to keep accuracy high is to keep tool bodies out of context by default. Manifest-then-fetch makes that the protocol, not a habit the LLM has to remember.

## When To Use

- Tools with high payload variance — `web_fetch`, `sql_query`, `log_search`, `read_file` on unknown sizes.
- Agents that loop ≥30 turns and accumulate tool history.
- Pipelines where most calls only need a count, header, or first match.
- Multi-tenant agent platforms where some tools occasionally return megabyte responses.

## When NOT To Use

- Tools where every result is small (<1k tokens) — the manifest dance is pure overhead.
- Single-shot stateless tool calls in a one-turn agent — no later step exists to fetch the body.
- Streaming tools where the agent must act on each chunk live — manifests delay action.

## Content

| File | What's inside |
|------|---------------|
| `content/01-protocol.xml` | The two-phase contract: manifest envelope, fetch tool, default preview-only behaviour. |
| `content/02-preview-design.xml` | What goes into the preview field; size budget; structured vs free-text previews. |

## Templates

| File | Purpose |
|------|---------|
| `templates/manifest.json` | Reference shape of the manifest envelope returned by every wrapped tool. |
| `templates/fetch-tool.json` | JSON tool definition for `get_full_result(execution_id)` companion tool. |
