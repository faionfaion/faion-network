# Local LLM with Ollama

## Summary

Run LLMs locally via Ollama's HTTP API (port 11434). Primary use: privacy-sensitive workloads, offline environments, and cost elimination for high-volume low-stakes tasks. The OpenAI-compatible `/v1` endpoint allows swapping between local and cloud APIs by changing only `base_url` and `api_key`, enabling local development + cloud production without code changes.

## Why

Cloud APIs send content to external servers and have per-token costs and rate limits. Local inference eliminates both at the cost of hardware. For classifying/summarizing large volumes of internal documents, local models can be 100x cheaper. The OpenAI-compatible API means zero code changes to switch local vs. cloud for testing.

## When To Use

- Data privacy requirements prohibiting external API calls
- High-volume, low-stakes tasks where cloud API costs are prohibitive
- Offline or air-gapped environments
- Development/testing — no API costs, no rate limits, instant iteration
- Deploying a custom fine-tuned model not hosted externally

## When NOT To Use

- Tasks requiring frontier-level reasoning (complex code, multi-step math) — local 7B/13B models underperform Opus/GPT-4o
- Machine has &lt;8GB RAM — models will page to disk and be unusably slow
- Production services with unpredictable load spikes — local GPU is not elastically scalable
- Latest model capabilities needed — local model libraries lag cloud providers by months

## Content

| File | What's inside |
|------|---------------|
| `content/01-setup-usage.xml` | Installation, model selection by RAM, OpenAI-compatible endpoint, health check rule |
| `content/02-production.xml` | Modelfiles, Docker deployment, concurrency limits, GPU detection |

## Templates

| File | Purpose |
|------|---------|
| `templates/ollama-service.py` | OllamaService class with health check, generate, and pull |
