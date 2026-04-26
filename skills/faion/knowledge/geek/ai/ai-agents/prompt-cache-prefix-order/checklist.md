# Checklist — Prompt-Cache Prefix Order

## Audit current ordering

- [ ] System prompt is STABLE across all calls in the next 5 minutes
- [ ] Tool definitions are STABLE (no per-call interpolation)
- [ ] Retrieval / context segment placed BEFORE conversation history
- [ ] Conversation history truncated from the OLDEST end, not the middle
- [ ] User-personalized data is in the user message, not system prompt

## Add cache breakpoints (Anthropic)

- [ ] System prompt: `cache_control: ephemeral` on the last block
- [ ] Tools: implicit caching of the tool list (depends on SDK)
- [ ] Retrieval block: `cache_control` if it's the same across many calls
- [ ] Latest user message: NEVER cache (always volatile)
- [ ] Total cache_control breakpoints ≤ 4

## Verify

- [ ] First call returns `cache_creation_input_tokens > 0`
- [ ] Second call within 5 min returns `cache_read_input_tokens > 0` and `cache_creation_input_tokens == 0`
- [ ] Cost dashboard shows the expected ~90% reduction on cached portion
- [ ] If cache hit rate is low, log first 200 chars of system+tools per call and diff — find the volatile char

## Maintenance

- [ ] When tool list changes, expect a one-call cache miss (acceptable)
- [ ] When system prompt changes, all cache invalidates — schedule big changes during low-traffic windows
- [ ] Don't tweak system prompt for A/B tests in production — caches diverge per variant
- [ ] Use 1-hour TTL `{"type": "ephemeral", "ttl": "1h"}` for batch workloads

## Composition

- [ ] tool-description-as-prompt: rich tool descriptions are cached, amortized
- [ ] schema-field-order: cached schema = stable schema; don't change order between calls if cache matters
- [ ] weak-model-preselection: each model has its own cache; orchestrate accordingly
