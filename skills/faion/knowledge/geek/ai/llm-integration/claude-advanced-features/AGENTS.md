# Claude Advanced Features

## Summary

Extended Thinking, Computer Use, Prompt Caching, and Batch API are four distinct Claude capabilities that each trade off cost, latency, or complexity for specific gains. Extended Thinking exposes the model's reasoning chain for complex problems. Computer Use lets Claude control a desktop or browser via screenshot + action loops. Prompt Caching reduces input token cost by up to 90% for repeated stable prefixes. Batch API cuts cost by 50% for workloads that tolerate up to 24-hour latency.

## Why

Each feature targets a concrete cost or capability gap: Extended Thinking improves accuracy on multi-step reasoning without requiring custom chain-of-thought scaffolding; Computer Use automates GUI-only workflows that have no API; Prompt Caching makes large-context pipelines economically viable when the same system prompt is reused across many calls; Batch API makes offline enrichment and evaluation affordable at scale.

## When To Use

- Extended Thinking: multi-step math, architecture decisions, complex debugging, strategic planning where visible reasoning improves trust.
- Computer Use: automating legacy GUI apps, browser automation, or desktop testing in sandboxed environments.
- Prompt Caching: any pipeline that calls Claude repeatedly with the same system prompt or document context (stable prefix > 1024 tokens).
- Batch API: offline enrichment, content generation, nightly analysis — any workload where 24-hour latency is acceptable.

## When NOT To Use

- Extended Thinking: simple extraction, classification, or templating — adds latency and tokens without benefit.
- Computer Use: production systems with live credentials or databases — always requires human-in-the-loop; never unattended.
- Prompt Caching: prompts that change on every call — cache never hits; you pay write cost with no read benefit.
- Batch API: real-time user-facing responses — 24-hour SLA makes it unsuitable for synchronous pipelines.

## Content

| File | What's inside |
|------|---------------|
| `content/01-extended-thinking.xml` | Extended Thinking rules, budget sizing, multi-turn handling, gotchas. |
| `content/02-computer-use.xml` | Computer Use tool setup, action handler rules, safety requirements. |
| `content/03-prompt-caching.xml` | Caching rules, prefix ordering, TTL, monitoring cache hit rate. |
| `content/04-batch-api.xml` | Batch API lifecycle, polling pattern, error handling, cost model. |

## Templates

| File | Purpose |
|------|---------|
| `templates/think-deeply.py` | Extended Thinking helper — returns (thinking, answer) tuple. |
| `templates/call-with-cache.py` | Prompt Caching wrapper with cache hit rate logging. |
| `templates/batch-submit-poll.py` | Batch API submit + poll loop. |
