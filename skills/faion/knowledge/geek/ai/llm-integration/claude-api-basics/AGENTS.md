# Claude API Basics

## Summary

Authentication, model selection, rate-limit handling with exponential backoff, token counting, and cost tracking for the Anthropic Python/TypeScript SDK. The single most important rule: pin model IDs with full date strings (e.g., `claude-sonnet-4-20250514`) to prevent silent behavior changes on alias updates.

## Why

Claude API has non-obvious failure modes: 529 overloaded_error requires retry logic (not a client error), rate limits are per-tier and hit fast in concurrent agent workflows, cost tracking requires exact model ID strings (aliases break lookups), and token counting adds a round-trip that degrades hot-path latency.

## When To Use

- Bootstrapping any Anthropic SDK integration from scratch
- Selecting the right Claude model for a cost vs. capability trade-off
- Implementing retry/backoff for production LLM calls
- Tracking token usage and API costs per request or session
- Debugging authentication and rate-limit failures

## When NOT To Use

- Working client setup already exists — don't re-implement auth/retry per-call
- Batch-processing non-time-sensitive workloads — use the Batch API (50% cheaper) instead
- Streaming output needed — see claude-messages-api methodology
- Task requires tool use or structured JSON output — see claude-tool-use methodology

## Content

| File | What's inside |
|------|---------------|
| `content/01-auth-models.xml` | Authentication setup, required headers, model IDs, model selection guide |
| `content/02-retry-cost.xml` | Rate limit tiers, retry with tenacity, cost tracking by model, agent gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/cost-tracker.py` | CostTracker class for per-call and session cost tracking |
| `templates/retry-wrapper.py` | tenacity-based retry decorator for rate limit and server errors |
