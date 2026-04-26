# Model Evaluation

## Summary

Systematic methodology for assessing LLM quality, latency, cost, safety, and reliability across offline (test dataset), online (A/B production traffic), and continuous monitoring modes. Always run at minimum two evaluation passes per output: automated metric + LLM-as-judge. Never report only BLEU/ROUGE for generation tasks — automated metrics correlate poorly with human preference.

## Why

Models degrade over time as production query distributions shift; benchmark scores compress differences that actually matter in production. LLM-as-judge has evaluator bias (GPT-4 prefers GPT-4 outputs, Claude prefers Claude outputs) — use multi-judge or human calibration. Evaluation results on a static test set decay; re-evaluate quarterly or after major user behavior changes.

## When To Use

- Selecting between two or more candidate models for a production use case
- Before promoting a prompt change or model upgrade to production
- After fine-tuning, to verify quality improvement over the base model
- Setting up continuous monitoring with alerts when quality drifts below threshold
- Running A/B tests to compare a new model against current production baseline

## When NOT To Use

- Task is trivial and any capable model passes — skip formal evaluation, ship
- No baseline exists yet — gather production data first, then evaluate against it
- Purely synthetic benchmarks for a highly domain-specific task — use real query samples
- Budget does not allow LLM-as-judge at scale — use cheaper automated metrics as a proxy first

## Content

| File | What's inside |
|------|---------------|
| `content/01-metrics-and-benchmarks.xml` | Automated metrics by task type, standard benchmarks, benchmark saturation warnings |
| `content/02-evaluation-process.xml` | Offline setup, LLM-as-judge rubric, A/B testing, production monitoring thresholds |

## Templates

| File | Purpose |
|------|---------|
| `templates/llm-judge-prompt.txt` | LLM-as-judge rubric prompt (accuracy, completeness, clarity, hallucination) |
| `templates/batch-eval-runner.py` | Async batch evaluation runner using Anthropic SDK |
