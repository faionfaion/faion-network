# Cost-Aware Gateway with Fallback Chain (OpenRouter Pattern)

## Summary

Do not hard-code a single model in production agent code. Send each call to a gateway (OpenRouter, LiteLLM proxy, Portkey, Kong AI Gateway) that exposes a primary model plus an ordered fallback chain; on provider 5xx, 429, or timeout the gateway transparently retries the next model in the list. Bill only the successful run. The result: better availability than any single vendor, no code change to swap models, and a single integration surface for prompt-caching, retries, observability, and budget caps.

## Why

Single-vendor agents fail closed: a 30-minute Anthropic outage is a 30-minute product outage. Multi-provider gateways turn vendor incidents into degraded-but-running scenarios. OpenRouter's Zero Completion Insurance and ordered fallbacks have been observed to keep tail availability above 99.95% while individual providers run at 99.5-99.9%. The economic side is equally strong: per-call routing across providers lets the gateway pick the cheapest model that meets the quality bar, and the fallback chain absorbs rate limits during traffic spikes without code change. Direct vendor SDK calls give up all of that for a marginal latency win.

## When To Use

- Production agents with an availability SLA above the single-vendor floor.
- Teams running A/B experiments across providers (Anthropic vs OpenAI vs Gemini) without code changes.
- Workloads that hit rate limits on a single provider during peak hours.
- Multi-region deployments where the cheapest provider differs per region.

## When NOT To Use

- Strict data-residency or compliance regimes (EU healthcare, defense) where the gateway is a third-party processor — go direct, with a controlled fallback inside the same boundary.
- Pipelines that depend on raw vendor SDK features the gateway does not expose (Anthropic prompt caching, OpenAI Batch API, fine-tuned models).
- Local development and experimentation — the gateway adds latency and operational surface for no production benefit.
- Edge / on-device inference — gateway round-trip dominates total latency.

## Content

| File | What's inside |
|------|---------------|
| `content/01-gateway-fallback.xml` | The fallback-chain semantics, error class, billing model, and what to put in the chain. |
| `content/02-gateway-tradeoffs.xml` | Compliance, vendor-feature parity, observability, and the one-call-per-success billing rule. |

## Templates

| File | Purpose |
|------|---------|
| `templates/openrouter_call.py` | OpenRouter chat-completions call with a primary model and an explicit fallback chain. |
