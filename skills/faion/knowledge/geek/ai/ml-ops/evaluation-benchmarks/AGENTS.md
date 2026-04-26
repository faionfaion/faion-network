# Evaluation Benchmarks

## Summary

Multi-model comparison and continuous production monitoring methodology. `ModelComparison` runs the same test set across multiple LLMs and ranks them per metric. `BenchmarkSuite` standardizes evaluation across classification, QA, summarization, and code task types. `ProductionEvaluator` samples live traffic and runs automated quality checks with alerting.

## Why

A single evaluation snapshot reveals current quality but not trends. Versioned benchmark runs track whether model changes improve or degrade performance over time. Production sampling catches regressions before users report them, and multi-model comparison removes guesswork from provider or version selection decisions.

## When To Use

- Selecting a model or provider for a new project: run `ModelComparison` on a domain-representative test set
- Establishing a repeatable performance baseline before any major prompt or model change
- Setting up CI that blocks deployment if benchmark scores drop below a stored threshold
- Comparing a fine-tuned model to its base model with consistent methodology
- Continuous production monitoring that detects quality regressions automatically

## When NOT To Use

- Fewer than 100 test cases — confidence intervals are too wide to be actionable; build the dataset first
- Benchmark dataset derived from the same source as training data — scores are artificially inflated; use a separate held-out set
- Evaluating safety or alignment — string-based checks are insufficient; use red-teaming and dedicated safety benchmarks
- Expecting a single benchmark run to fully characterize model quality — benchmarks capture only what they measure

## Content

| File | What's inside |
|------|---------------|
| `content/01-model-comparison.xml` | `ModelComparison` class, ranking logic, latency inversion gotcha, parallelization pattern |
| `content/02-benchmark-suite.xml` | `BenchmarkSuite` with classification/QA/summarization loaders, dataset format adapters |
| `content/03-production-monitoring.xml` | `ProductionEvaluator`, persistent JSONL logging, sample rate guidance, alert analysis prompt |

## Templates

| File | Purpose |
|------|---------|
| `templates/persistent-evaluator.py` | Production evaluator with JSONL log flush instead of in-memory accumulation (~40 lines) |
| `templates/benchmark-alert-prompt.txt` | Prompt template for analyzing 24h production metrics vs. 7-day baseline |
