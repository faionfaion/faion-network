# Auto-Evict Tool Results at Token Threshold

## Summary

Wrap the agent's tool-execution runtime so any single tool result whose token count exceeds a fixed threshold N (typically 20,000) is automatically written to disk and substituted with `{path, preview, evicted: true}` BEFORE the LLM ever observes the body. This is a deterministic middleware policy, not an LLM-discretion choice — the agent literally cannot leak the oversized payload because the runtime never feeds it in. It is the enforced sibling of voluntary filesystem-as-memory: same compression, but applied by code.

## Why

LLMs do not self-restrain. When a tool call returns a 35k-token npm log or a 200-row SQL dump, the model will dutifully ingest the whole thing, blow the effective context window, lose track of the goal, and rack up cost. LangChain's Deep Agents observed this empirically and shipped `filesystemMiddleware` with a `toolTokenLimitBeforeEvict` knob (default 20k) that intercepts the result and stores it on disk. The agent then reads only the slice it needs via `read_file(path, lines=...)`. This preserves recoverability (the body is one read away) while keeping per-step effective context bounded — the precondition for accuracy on long-horizon tasks.

## When To Use

- Any tool that talks to a remote service with high payload variance (web fetch, SQL, API search, log retrieval).
- Long-running agents (50+ tool calls) where a single overflow corrupts the rest of the loop.
- Multi-tenant agents where prompt-injection via large tool output is a threat.
- CI/build/log-tail tools that occasionally emit megabytes of output.

## When NOT To Use

- Streaming/realtime tools where the agent must act on each chunk immediately and never re-reads — eviction adds latency without benefit.
- Tools whose every result is small (<1k tokens) — the manifest dance is pure overhead.
- Single-shot stateless agents that exit before context bloat matters.
- Environments without a writable filesystem (browser sandbox, edge runtime) — use M-PL-02 manifest-then-fetch with a content store instead.

## Content

| File | What's inside |
|------|---------------|
| `content/01-rule.xml` | The threshold rule, why discretion fails, the substitution shape. |
| `content/02-implementation.xml` | Middleware wiring, knob naming, preview slicing, recovery via `read_file`. |
| `content/03-anti-patterns.xml` | "Trust the LLM to summarize", missing recovery path, evicting too aggressively. |

## Templates

| File | Purpose |
|------|---------|
| `templates/evict-middleware.py` | Minimal Python middleware that token-counts tool results and rewrites oversized ones to disk. |
