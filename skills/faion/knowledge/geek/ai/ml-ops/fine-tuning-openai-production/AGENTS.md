# Fine-tuning OpenAI — Production

## Summary

Full OpenAI fine-tuning production pipeline: file upload, job creation with hyperparameter control, status polling, LLM-as-judge evaluation against a held-out test set, and model ID registry management. The `FineTuningPipeline` class encapsulates the complete workflow with human-checkpoint gates before deployment.

## Why

OpenAI fine-tuning is asynchronous and opaque — training loss is not available in real time and fine-tuned model IDs are ephemeral strings that become invalid when base model versions are deprecated. A structured pipeline with explicit human approval gates, cost estimation before upload, and post-training evaluation prevents wasted spend and silent quality regressions in production.

## When To Use

- Need a fine-tuned model deployable via OpenAI API with zero infrastructure overhead
- Task has 50-10,000 high-quality JSONL examples with a consistent system prompt
- Use cases: style consistency, domain-specific tone, structured output format enforcement, task classifier
- Willing to tolerate 15 minutes to several hours of training latency

## When NOT To Use

- Fewer than 50 examples — base model with few-shot beats fine-tuning; collect more data first
- Task requires up-to-date factual knowledge — OpenAI fine-tuning does not inject new facts
- Cost sensitivity: `ft:gpt-4o-mini` costs 3-6x more per token than base `gpt-4o-mini` — verify ROI
- Proprietary data that must not leave your infrastructure — training data is processed on OpenAI servers
- Need for a fully private model weight — OpenAI retains training data per their data policy

## Content

| File | What's inside |
|------|---------------|
| `content/01-upload-and-train.xml` | File upload, job creation, hyperparameter guidelines, status polling with all job states |
| `content/02-evaluation.xml` | LLM-as-judge eval pattern, test set protocol, scoring, base model comparison |
| `content/03-production-ops.xml` | Model ID registry, versioning, checkpoint expiry, cost estimation, cleanup of uploaded files |

## Templates

| File | Purpose |
|------|---------|
| `templates/finetune-pipeline.py` | `FineTuningPipeline` class: upload → train → poll → evaluate (~80 lines) |
| `templates/estimate-cost.py` | Token count + cost estimate before upload using tiktoken (~20 lines) |
| `templates/eval-prompts.txt` | LLM judge prompts for format_match scoring and promotion decision |
