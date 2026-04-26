# Claude Best Practices

## Summary

A set of production patterns for calling the Anthropic Messages API reliably and cost-efficiently: model tier selection (Haiku/Sonnet/Opus by task), prompt caching for repeated large contexts, Batch API for offline workloads, token counting for pre-flight validation, exponential backoff for rate limits, and a monitored client wrapper for cost attribution per subagent role.

## Why

The Anthropic API has several non-obvious behaviors that silently degrade production systems: `max_tokens` defaults are low and truncate structured output mid-JSON; prompt cache requires byte-identical prefixes (any dynamic injection before the cached block busts the cache); model aliases update without notice; rate limit errors include a `retry-after` header that should be parsed rather than guessed. Applying these patterns prevents silent failures in multi-agent pipelines.

## When To Use

- Building any production system that calls the Anthropic Messages API.
- Optimizing cost/quality tradeoff across multi-agent pipelines.
- When system prompts are large and repeated across many requests (prompt caching).
- Implementing retry logic, fallback models, or monitoring for Claude API calls.
- Selecting the right Claude model tier for a given agent role.

## When NOT To Use

- Quick scripted one-off calls with no cost or reliability concerns.
- Provider-neutral code that must abstract over multiple LLM providers — use an abstraction layer instead.
- Token counting pre-flight adds latency; skip for simple short prompts.

## Content

| File | What's inside |
|------|---------------|
| `content/01-model-selection.xml` | Model tier rules (Haiku/Sonnet/Opus), max_tokens guidance, structured output truncation gotcha. |
| `content/02-cost-optimization.xml` | Prompt caching structure, cache prefix ordering, hit rate monitoring, Batch API pattern. |
| `content/03-reliability-patterns.xml` | Retry with backoff, rate-limit header parsing, fallback model, async batch with AsyncAnthropic. |

## Templates

| File | Purpose |
|------|---------|
| `templates/cached-system-prompt.py` | System prompt with static cached prefix + dynamic tail. |
| `templates/monitored-client.py` | Minimal Claude client with token usage and latency logging. |
