# Agent Integration — Evaluation Benchmarks

## When to use
- Selecting a model or provider for a new project: run `ModelComparison` across candidate models on a domain-representative test set
- Establishing a repeatable performance baseline before any major prompt or model change
- Setting up continuous production monitoring that detects quality regressions before users report them
- Comparing a fine-tuned model to the base model with consistent methodology
- Building a CI quality gate that blocks deployment if benchmark scores drop below threshold

## When NOT to use
- The test set has fewer than 100 cases — `ModelComparison` results will have confidence intervals too wide to be actionable
- The benchmark dataset is derived from the same source as the training data — this produces artificially inflated scores; use a held-out dataset from a different collection
- The goal is evaluating safety or alignment — `ProductionEvaluator` string checks are insufficient; use red-teaming and dedicated safety benchmarks (e.g., ToxiGen, BBQ)
- A single benchmark run is expected to fully characterize model quality — benchmarks capture what they measure, not everything that matters in production

## Where it fails / limitations
- `ModelComparison._create_comparison_report` assumes "higher is better" for all metrics — this is wrong for latency; the ranking direction must be parameterized per metric
- `BenchmarkSuite.run_all` runs benchmarks sequentially — for large test sets and multiple benchmark types, this is slow; parallelize with `asyncio` or a thread pool
- `ProductionEvaluator._run_checks` uses hardcoded error patterns (`"sorry, i cannot"`, `"as an ai"`) — these are model-version-specific and go stale as providers change phrasings
- The production evaluator logs all evaluations in memory — for high-volume systems (>10k req/day), this causes OOM; flush to a database or observability platform every N evaluations
- `BenchmarkSuite.load_qa_benchmark` only supports a flat JSON format — real datasets (SQuAD, TriviaQA) require format adapters
- `ModelComparison` creates one `ModelEvaluator` per model but shares the same `cases` list — if cases include mutable metadata (dict), side effects can corrupt results across model runs

## Agentic workflow
An agent running benchmark evaluation should load a versioned test dataset, run `ModelComparison` or `BenchmarkSuite` at `temperature=0`, compare results to the stored baseline (from previous run or deployment), and return a structured pass/fail report. For production monitoring, a lightweight background subagent samples live requests at 5-10%, applies `ProductionEvaluator` checks, and pushes aggregated metrics to the observability platform every hour for dashboard display.

### Recommended subagents
- `faion-sdd-executor-agent` — drives benchmark setup and CI integration from a task card
- A benchmark-runner subagent (custom) — takes model list, test dataset path, metric list; returns `ModelComparison` report JSON
- A production-monitor subagent (custom) — runs on a cron schedule, queries sampled evaluations from the past hour, compares to baseline, creates alerts or SDD tasks on regression

### Prompt pattern
```
Run a model comparison benchmark for the following models: {model_list}.
Test dataset: {N} cases, task type: {classification|qa|summarization}.
Metrics: {metric_list}. Temperature: 0.

Return JSON: {
  "winner": str,
  "rankings": {"metric": [model_list_ranked]},
  "comparison": {"metric": {"model": score}},
  "recommendation": str,
  "latency_ms": {"model": float}
}
```

```
Analyze production evaluation metrics from the past 24h:
- non_empty pass rate: {rate}
- reasonable_length pass rate: {rate}
- no_error_patterns pass rate: {rate}
- avg output length: {chars}

Compare to 7-day baseline. Flag any check that dropped >5% absolute.
Return JSON: {"alerts": [{"check": str, "delta": float, "severity": str}], "overall_health": "ok|degraded|critical"}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `lm-evaluation-harness` | EleutherAI standard benchmark runner (MMLU, HellaSwag, etc.) | `pip install lm-eval` / [github.com/EleutherAI/lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) |
| `openai` SDK | Run `ModelComparison` and `BenchmarkSuite` API calls | `pip install openai` |
| `datasets` (HuggingFace) | Load standard benchmark datasets (SQuAD, MMLU, TriviaQA) | `pip install datasets` / [huggingface.co/docs/datasets](https://huggingface.co/docs/datasets) |
| `evaluate` (HuggingFace) | Metric implementations for benchmark scoring | `pip install evaluate` |
| `pandas` | Aggregate and pivot benchmark results | `pip install pandas` |
| `pytest` | Run benchmark suite as CI test with threshold assertions | `pip install pytest` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Braintrust | SaaS | Yes — SDK + dataset versioning | Best for versioned benchmark management and comparison history |
| Langfuse | SaaS/OSS | Yes — score API per trace | Attach benchmark scores to traces for trend tracking |
| OpenAI Evals | OSS | Yes — YAML/Python eval runner | Standardized benchmark definitions; good for regression CI |
| HELM (Stanford CRFM) | OSS | Partial — requires local model access | Gold standard for holistic model comparison; complex setup |
| PromptFoo | OSS | Yes — YAML config, CI-ready | Fast multi-model comparison with LLM-as-judge support |
| Weights & Biases | SaaS | Yes — log benchmark runs as W&B runs | Compare benchmark metrics across model versions in W&B tables |

## Templates & scripts
See `templates.md` for full CI benchmark pipeline and dataset format specifications.

Inline — production evaluator with persistent logging to JSONL (≤40 lines):

```python
import json
import random
import logging
from datetime import datetime
from pathlib import Path

class PersistentProductionEvaluator:
    def __init__(self, log_path: str, sample_rate: float = 0.1):
        self.log_path = Path(log_path)
        self.sample_rate = sample_rate
        self.logger = logging.getLogger(__name__)

    def evaluate_request(self, input: str, output: str, metadata: dict = None) -> dict | None:
        if random.random() >= self.sample_rate:
            return None
        checks = {
            "non_empty": len(output.strip()) > 0,
            "reasonable_length": 10 < len(output) < 10000,
            "no_error_patterns": not any(
                p in output.lower() for p in ["sorry, i cannot", "as an ai", "i'm unable"]
            ),
        }
        record = {
            "timestamp": datetime.utcnow().isoformat(),
            "input_length": len(input),
            "output_length": len(output),
            "checks": checks,
            "metadata": metadata or {},
        }
        with self.log_path.open("a") as f:
            f.write(json.dumps(record) + "\n")
        if not all(checks.values()):
            self.logger.warning("Quality check failed: %s", {k: v for k, v in checks.items() if not v})
        return record
```

## Best practices
- Store benchmark datasets in version control (Git LFS or DVC) alongside prompt versions — changes to either should trigger a benchmark re-run to detect regressions
- Always run benchmarks at `temperature=0` with a fixed random seed where the API supports it — stochastic results between runs are noise, not signal
- Maintain a "golden" test set that never changes: use it for regression detection. Maintain a separate "current" test set that grows with new failure modes from production
- For `ModelComparison`, use at least 50 cases per task type — fewer than 50 produces rankings that reverse with each new run due to sampling variance
- Track benchmark results in a time-series database (Langfuse, W&B, or simple JSONL) — a single evaluation snapshot has low value; trends over 4-8 weeks reveal model drift and quality degradation
- For production `ProductionEvaluator`, set sample rate based on traffic: 10% at 1k req/day, 1% at 100k req/day, 0.1% at 1M req/day — evaluation should cost <5% of production inference cost
- Calibrate error pattern strings against actual model outputs every 3-6 months; provider phrasings change and stale patterns produce false negatives

## AI-agent gotchas
- `ModelComparison` rankings assume higher metric value is better — latency ranking is therefore reversed; agents using ranking output for model selection must explicitly handle latency inversion
- Running `ModelComparison` with 3 models × 100 cases × 1s latency = 300s sequential — agents should parallelize model evaluation with `asyncio.gather` or separate subagents, not run serially
- `ProductionEvaluator.evaluate_request` uses `random.random()` which is not reproducible — for debugging a specific production failure, the sampling will not reliably re-capture it; always log all raw requests separately from the evaluation sample
- Benchmark overfitting is a real risk: if the same test set is used to tune prompts, the test set is no longer an unbiased evaluator — agents must not expose the full test set to prompt-optimization loops
- The `BenchmarkSuite` does not validate that loaded cases share a consistent schema — mixing datasets with different field names (e.g., `"answer"` vs. `"label"`) silently produces empty `expected_output` fields and misleadingly high metrics

## References
- [HELM Benchmark](https://crfm.stanford.edu/helm/)
- [LM Evaluation Harness (EleutherAI)](https://github.com/EleutherAI/lm-evaluation-harness)
- [OpenAI Evals](https://github.com/openai/evals)
- [PromptFoo — Model Comparison](https://promptfoo.dev/docs/guides/compare-llms/)
- [HuggingFace Datasets](https://huggingface.co/docs/datasets/)
- [Braintrust — Evaluation](https://www.braintrust.dev/docs/guides/evals)
- [RAGAS — RAG Benchmarking](https://docs.ragas.io/)
