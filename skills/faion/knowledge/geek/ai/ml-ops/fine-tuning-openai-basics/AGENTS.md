# Fine-tuning OpenAI — Basics

## Summary

Data preparation methodology for OpenAI fine-tuning: creating JSONL training examples in the chat messages format, validating structure and token counts with `tiktoken`, and generating additional examples with GPT-4. Covers the decision matrix for when fine-tuning beats few-shot prompting or RAG, and the three-phase pipeline: dataset prep → job submission → evaluation.

## Why

OpenAI fine-tuning requires exactly the right JSONL format — missing `assistant` turns or inconsistent system prompts silently produce poor models. Validating dataset structure and estimating cost before upload prevents wasted training spend. Starting with a solid data preparation workflow is the highest-leverage step in the fine-tuning pipeline.

## When To Use

- Output format or style is inconsistently produced by the base model despite prompt engineering (below 80% compliance)
- Domain-specific vocabulary causes incorrect or inconsistent terminology in base model outputs
- Current prompts are long (>500 tokens of examples) and reducing them via fine-tuning would cut latency and cost
- Deterministic output structure (strict JSON schemas) needed but base model produces it inconsistently
- Task clearly benefits from style/format fine-tuning rather than knowledge injection

## When NOT To Use

- Goal is injecting new facts or knowledge — fine-tuning memorizes patterns, not facts; use RAG
- Fewer than 50 high-quality examples available — invest in data collection first
- Prompt engineering already achieves >90% quality — fine-tuning adds cost and operational overhead without meaningful gain
- Application uses many diverse tasks — a task-specific fine-tuned model can regress on other tasks
- Rapid iteration is needed — fine-tuning jobs take 30-60 minutes; prompt engineering allows instant iteration
- Sensitive data that must not be processed on OpenAI servers

## Content

| File | What's inside |
|------|---------------|
| `content/01-data-prep.xml` | JSONL format spec, `create_training_example`, `prepare_dataset`, quality checklist |
| `content/02-validation.xml` | `validate_dataset` with token counting, error detection, cost estimation |
| `content/03-workflow.xml` | Three-phase agentic workflow, job submission, polling pattern, promotion decision |

## Templates

| File | Purpose |
|------|---------|
| `templates/training-example.jsonl` | Minimal valid JSONL training file with system/user/assistant structure |
| `templates/submit-job.py` | End-to-end upload → create job → poll → return model ID (~45 lines) |
| `templates/dataset-review-prompt.txt` | Prompt for LLM quality review of training examples |
