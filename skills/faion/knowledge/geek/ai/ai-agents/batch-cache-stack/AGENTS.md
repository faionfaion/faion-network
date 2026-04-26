# Batch API + Prompt Caching Stack

## Summary

For any non-real-time agent workload (overnight pipelines, eval harnesses, content backfills, dataset labeling), submit requests through the provider's Message Batches / Batch Mode API and put `cache_control` on the longest stable prefix (system + tools). The 50% batch discount stacks multiplicatively with the 90% prompt-cache-read discount on every batch item that hits the cache, yielding an effective ~5% of synchronous-uncached cost on the cached portion. This requires picking the batch route over real-time AND keeping every batch item's prefix byte-identical so cache lookups succeed.

## Why

Anthropic's pricing page documents a 50% discount for the Message Batches API (24h SLA). Cache-read pricing is 0.1× base input cost, and Anthropic explicitly states that batch and cache discounts compose: 0.5 × 0.1 = 0.05 of baseline read cost. Google's Gemini Batch Mode is also 50% off and stacks with implicit context caching. OpenAI's Batch API is 50% off but its prompt caching does NOT stack with batch discount — pick the provider matching your stack. The mechanism is independent: the gateway charges the discount before the cache layer dedupes, so each batch item's cached tokens are billed at the floor of both factors.

## When To Use

- Async content pipelines tolerating up to 24h latency (neromedia/pashtelka/longlife nightly summarization).
- Eval suites and regression runs over 100s-100ks of fixtures sharing one rubric.
- Bulk extraction / classification / labeling over a static document corpus.
- Large agent backfill jobs (re-tag the last 30 days of news with a new schema).
- Any pipeline where the system prompt + tool definitions are byte-identical across all items.

## When NOT To Use

- Interactive chat or any user-facing surface — 24h SLA is unacceptable.
- Real-time tool-use loops where you need streaming and per-call decisions.
- Workloads with strict <1h SLAs — batches can take up to 24h.
- Pipelines whose prefix mutates per item (different system prompt per row) — cache never hits, you pay the 1.25× cache-write tax for nothing.
- OpenAI workloads where you assumed batch+cache stack — they do not on OpenAI; read the provider's pricing carefully.

## Content

| File | What's inside |
|------|---------------|
| `content/01-stacking-rule.xml` | The core rule: batch + cache discounts stack on Anthropic and Gemini; provider-specific math and the prefix-stability requirement. |
| `content/02-prefix-stability.xml` | Antipatterns: per-item drift in system prompts, tool list reordering, timestamp leakage that silently kills cache hits inside batches. |

## Templates

| File | Purpose |
|------|---------|
| `templates/batch_with_cache.py` | Anthropic Messages Batches submission with `cache_control` on system+tools — the canonical stack. |
