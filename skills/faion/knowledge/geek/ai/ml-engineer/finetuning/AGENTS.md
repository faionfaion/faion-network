# LLM Fine-tuning (General Guide)

## Summary

A general guide to fine-tuning LLMs covering the decision framework (prompt → RAG → fine-tune), technique selection (Full FT, LoRA, QLoRA, DoRA, OpenAI API), and framework comparison (Unsloth, LLaMA-Factory, Axolotl, TRL, Torchtune). Always follow the decision tree before committing to fine-tuning — it is the most expensive and least reversible enhancement strategy.

## Why

Fine-tuning internalizes domain jargon, output format constraints, and behavioral style, reducing per-call inference cost through shorter prompts and making behavior more reliable. However, it bakes in a knowledge snapshot (use RAG for live data), requires labeled data (500+ clean examples minimum), and creates a maintenance burden on every model version upgrade. Catastrophic forgetting is the primary failure mode — mix 20-30% general instruction data in training to prevent it.

## When To Use

- Prompt engineering and RAG have both been tried and still fail to meet quality bar
- Domain jargon, output format, or behavioral style needs to be internalized rather than injected per-call
- Production volume is high enough that shorter prompts reduce inference cost meaningfully
- You have 500+ verified examples in the target distribution with clear correct/incorrect labels
- Compliance requires a local or private model with no external API calls

## When NOT To Use

- Fewer than 100 quality examples — fine-tuning will overfit; use few-shot prompting
- Task requirements are exploratory or changing — fine-tuning creates a liability that degrades as the task evolves
- Real-time knowledge is required — use RAG for dynamic data
- Time-to-production is critical — fine-tuning adds days of iteration; try prompting first
- No labeled data exists — data collection must precede training

## Content

| File | What's inside |
|------|---------------|
| `content/01-decision.xml` | Decision framework (prompt → RAG → fine-tune), when/when-not table, technique comparison |
| `content/02-frameworks.xml` | Framework selection (Unsloth, LLaMA-Factory, Axolotl, TRL, Torchtune), VRAM/dataset-size routing |
| `content/03-pipeline.xml` | Data validation, training loop stages, eval gate, deployment, agent gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/validate-jsonl.py` | Data quality validation script (JSONL format check, min examples gate) |
| `templates/framework-selector.py` | Framework selection helper (VRAM, dataset size, WebUI need) |
| `templates/data-formats.json` | Training data format examples: Alpaca, ShareGPT, OpenAI Chat, DPO |
