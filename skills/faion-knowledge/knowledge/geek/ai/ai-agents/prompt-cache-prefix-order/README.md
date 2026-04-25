# Prompt-Cache Prefix Order

**Category:** `cost-` (cost optimization)

## The Rule

Order your prompt so the STABLE parts come first and the VOLATILE parts come last. Then mark a `cache_control` breakpoint immediately AFTER the longest stable prefix. Subsequent calls in the cache window pay 10% (or less) for the cached prefix instead of 100% for re-reading it.

For Anthropic, the canonical order:

```
[system prompt (long, stable)] → [tool definitions (stable)] → [retrieval context (semi-stable)] → [conversation history (volatile)] → [latest user turn (always volatile)]
```

Place the cache breakpoint after the latest segment that's stable across the next ~5 minutes (Anthropic ephemeral cache TTL).

## Why It Works

Prompt caching exploits the fact that the same prefix is processed identically every time. The model only re-runs attention from the breakpoint forward. If your stable content is at the END of the prompt, no caching happens because every call invalidates from the volatile prefix onward.

Cost reduction is dramatic — Anthropic's docs cite up to 90% savings on the cached portion. The catch is order: get it wrong and the cache never warms.

## Why prefix order matters

Caching is *prefix-based*. Anything that comes before a `cache_control` breakpoint is cached as one block. If a single token in that block changes between calls, the entire block is recomputed. So:

- Tools at position N+1 with system prompt at N → entire system+tools block invalidates if you tweak any tool
- Conversation history before retrieval → cache invalidates every turn
- User-personalized variable interpolated into system prompt → never caches across users

## When To Use

- Long system prompts (>1024 tokens, the Anthropic minimum cacheable size)
- Stable tool definitions (almost always — tool defs rarely change mid-session)
- Long-stable contexts: codebase manifests, user profiles, knowledge bases
- High call volume on the same prefix (chat, agent loops, batch processing)
- Multi-turn agents — each turn pays only for the *new* turn

## When NOT To Use

- One-shot calls (no second call to amortize the cache write)
- Prefixes < 1024 tokens (Anthropic minimum) or < 2048 tokens (OpenAI)
- Prefixes that change every call (no cache hit possible)
- Cost-sensitive systems where prefix is small relative to output (output is never cached)

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Tools defined AFTER user input | Tools go in the SDK's tools field at the top of the request; placement is enforced by SDK |
| User name interpolated into system prompt | Move user-specific data to the user message; keep system stable |
| Conversation history truncated mid-prefix on each turn | Truncate from the OLDEST end and add a fresh `cache_control` breakpoint after each truncation |
| Multiple cache_control breakpoints "to be safe" | Anthropic supports up to 4 — use them deliberately, not redundantly |
| Forgetting cache_control entirely on Claude — assuming "cache is automatic" | Anthropic ephemeral caching is OPT-IN via `cache_control` |

## Caches per provider

| Provider | Mechanism | TTL | Min size |
|----------|-----------|-----|----------|
| Anthropic | Explicit `cache_control: {"type": "ephemeral"}` | 5 min (default) or 1 hour | 1024 tokens |
| OpenAI (Responses API) | Automatic `prompt_cache_key` | minutes-hour | 1024 tokens |
| Gemini | Explicit `cachedContent` (long TTL) or implicit (short) | configurable | varies |

## Composition

- + **schema-field-order**: cached prefix should NOT include schema in JSON-mode if the schema changes; otherwise schema is part of the prefix and benefits from caching
- + **tool-description-as-prompt**: tool definitions are CACHED — descriptions are amortized, so over-investing in description quality is even more justified
- + **weak-model-preselection**: each stage's prompt has its own cache; the weak model also benefits from caching its rubric

## References

Sources:
- [Anthropic — Prompt Caching docs](https://docs.anthropic.com/claude/docs/prompt-caching)
- [OpenAI — Prompt Caching guide](https://platform.openai.com/docs/guides/prompt-caching)
- [Gemini — Context Caching](https://ai.google.dev/gemini-api/docs/caching)

See `templates.md`, `examples.md`, `checklist.md`, `llm-prompts.md`.
