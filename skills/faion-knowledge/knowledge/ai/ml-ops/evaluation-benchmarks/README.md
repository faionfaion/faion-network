---
id: evaluation-benchmarks
name: "Evaluation Benchmarks"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
parent: model-evaluation
---

# Evaluation Benchmarks

## Overview

Model comparison, benchmark suites, and production evaluation for LLM systems. Includes standardized benchmarking, multi-model comparison, and continuous production monitoring.

## Model Comparison

```python
from dataclasses import dataclass
from typing import List, Dict, Callable, Optional

@dataclass
class EvaluationCase:
    input: str
    expected_output: Optional[str] = None
    metadata: Dict = None

class ModelComparison:
    """Compare multiple models on the same test set."""

    def __init__(self, client, models: List[str]):
        self.client = client
        self.models = models
        self.evaluators = {
            model: ModelEvaluator(client, model)
            for model in models
        }

    def compare(
        self,
        cases: List[EvaluationCase],
        system_prompt: str = "",
        metrics: List[Callable] = None
    ) -> Dict:
        """Run comparison across all models."""
        results = {}

        for model, evaluator in self.evaluators.items():
            if metrics:
                for metric in metrics:
                    evaluator.add_metric(metric)

            results[model] = evaluator.evaluate(cases, system_prompt)

        return self._create_comparison_report(results)

    def _create_comparison_report(self, results: Dict) -> Dict:
        """Create comparison report."""
        report = {
            "models": list(results.keys()),
            "comparison": {},
            "rankings": {}
        }

        # Compare each metric
        all_metrics = set()
        for model_results in results.values():
            all_metrics.update(model_results.get("metrics", {}).keys())

        for metric in all_metrics:
            metric_values = {}
            for model, model_results in results.items():
                if metric in model_results.get("metrics", {}):
                    metric_values[model] = model_results["metrics"][metric]["mean"]

            report["comparison"][metric] = metric_values

            # Rank models (higher is better assumed)
            ranked = sorted(metric_values.items(), key=lambda x: x[1], reverse=True)
            report["rankings"][metric] = [m for m, _ in ranked]

        # Latency comparison
        latency_comparison = {
            model: results[model]["latency"]["mean_ms"]
            for model in results
        }
        report["comparison"]["latency_ms"] = latency_comparison

        return report
```

## Benchmark Suite

```python
from enum import Enum
from typing import Dict, List
import json

class BenchmarkType(Enum):
    CLASSIFICATION = "classification"
    GENERATION = "generation"
    QA = "qa"
    SUMMARIZATION = "summarization"
    CODE = "code"

class BenchmarkSuite:
    """Standardized benchmark suite for model evaluation."""

    def __init__(self, client):
        self.client = client
        self.benchmarks: Dict[BenchmarkType, List[EvaluationCase]] = {}

    def load_classification_benchmark(self, dataset_path: str):
        """Load classification benchmark."""
        with open(dataset_path) as f:
            data = json.load(f)

        cases = [
            EvaluationCase(
                input=item["text"],
                expected_output=item["label"],
                metadata={"category": "classification"}
            )
            for item in data
        ]

        self.benchmarks[BenchmarkType.CLASSIFICATION] = cases

    def load_qa_benchmark(self, dataset_path: str):
        """Load Q&A benchmark."""
        with open(dataset_path) as f:
            data = json.load(f)

        cases = [
            EvaluationCase(
                input=f"Context: {item['context']}\n\nQuestion: {item['question']}",
                expected_output=item["answer"],
                metadata={"category": "qa"}
            )
            for item in data
        ]

        self.benchmarks[BenchmarkType.QA] = cases

    def run_benchmark(
        self,
        model: str,
        benchmark_type: BenchmarkType,
        system_prompt: str = ""
    ) -> Dict:
        """Run a specific benchmark."""
        if benchmark_type not in self.benchmarks:
            raise ValueError(f"Benchmark {benchmark_type} not loaded")

        cases = self.benchmarks[benchmark_type]
        evaluator = ModelEvaluator(self.client, model)

        # Add appropriate metrics (import from evaluation-metrics.md)
        if benchmark_type == BenchmarkType.CLASSIFICATION:
            evaluator.add_metric(exact_match)
            evaluator.add_metric(contains_match)
        elif benchmark_type == BenchmarkType.QA:
            evaluator.add_metric(contains_match)
            evaluator.add_metric(bleu_score)
        elif benchmark_type == BenchmarkType.SUMMARIZATION:
            evaluator.add_metric(rouge_score)

        return evaluator.evaluate(cases, system_prompt)

    def run_all(self, model: str) -> Dict:
        """Run all loaded benchmarks."""
        results = {}

        for benchmark_type, cases in self.benchmarks.items():
            results[benchmark_type.value] = self.run_benchmark(
                model, benchmark_type
            )

        return results
```

## Production Evaluation

```python
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
import logging
from datetime import datetime, timedelta
import random

@dataclass
class EvaluationConfig:
    sample_rate: float = 0.1  # Sample 10% of production traffic
    metrics: List[str] = None
    alert_thresholds: Dict[str, float] = None
    judge_model: str = "gpt-4o"

class ProductionEvaluator:
    """Continuous evaluation in production."""

    def __init__(
        self,
        client,
        config: Optional[EvaluationConfig] = None
    ):
        self.client = client
        self.config = config or EvaluationConfig()
        self.logger = logging.getLogger(__name__)
        self.evaluation_log = []

    def should_evaluate(self) -> bool:
        """Determine if request should be evaluated (sampling)."""
        return random.random() < self.config.sample_rate

    def evaluate_request(
        self,
        input: str,
        output: str,
        metadata: Dict = None
    ) -> Dict:
        """Evaluate a single production request."""
        if not self.should_evaluate():
            return None

        evaluation = {
            "timestamp": datetime.now().isoformat(),
            "input_length": len(input),
            "output_length": len(output),
            "metadata": metadata or {}
        }

        # Run automated checks
        evaluation["checks"] = self._run_checks(input, output)

        # LLM judge (expensive, use sparingly)
        if self.config.sample_rate < 0.05:  # Only for small samples
            judge = LLMJudge(self.client, self.config.judge_model)
            evaluation["judge_score"] = judge.judge(
                input, output,
                criteria=["relevance", "helpfulness", "accuracy"]
            )

        # Log and check alerts
        self.evaluation_log.append(evaluation)
        self._check_alerts(evaluation)

        return evaluation

    def _run_checks(self, input: str, output: str) -> Dict:
        """Run automated quality checks."""
        checks = {}

        # Empty response check
        checks["non_empty"] = len(output.strip()) > 0

        # Reasonable length
        checks["reasonable_length"] = 10 < len(output) < 10000

        # No error patterns
        error_patterns = ["error", "sorry, i cannot", "as an ai"]
        checks["no_error_patterns"] = not any(
            p in output.lower() for p in error_patterns
        )

        return checks

    def _check_alerts(self, evaluation: Dict):
        """Check if evaluation triggers alerts."""
        if not self.config.alert_thresholds:
            return

        checks = evaluation.get("checks", {})

        for check_name, passed in checks.items():
            if not passed:
                self.logger.warning(
                    f"Quality check failed: {check_name}"
                )

    def get_metrics(self, window_hours: int = 24) -> Dict:
        """Get aggregated metrics for time window."""
        cutoff = datetime.now() - timedelta(hours=window_hours)

        recent = [
            e for e in self.evaluation_log
            if datetime.fromisoformat(e["timestamp"]) > cutoff
        ]

        if not recent:
            return {}

        # Aggregate check pass rates
        check_rates = {}
        for check_name in recent[0].get("checks", {}).keys():
            passed = sum(
                1 for e in recent
                if e.get("checks", {}).get(check_name, False)
            )
            check_rates[check_name] = passed / len(recent)

        return {
            "total_evaluated": len(recent),
            "check_pass_rates": check_rates,
            "avg_output_length": sum(e["output_length"] for e in recent) / len(recent)
        }
```

## Usage Examples

### Model Comparison

```python
from openai import OpenAI

client = OpenAI()

# Define test cases
cases = [
    EvaluationCase(
        input="Explain machine learning",
        expected_output=None
    ),
    # ... more cases
]

# Compare models
comparison = ModelComparison(
    client,
    models=["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"]
)

results = comparison.compare(cases, metrics=[exact_match, bleu_score])
print(results)
# {
#   "models": ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"],
#   "comparison": {
#     "exact_match": {"gpt-4o": 0.85, "gpt-4o-mini": 0.78, ...},
#     "latency_ms": {"gpt-4o": 1200, ...}
#   },
#   "rankings": {
#     "exact_match": ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"]
#   }
# }
```

### Benchmark Suite

```python
# Create benchmark suite
suite = BenchmarkSuite(client)

# Load benchmarks
suite.load_classification_benchmark("data/classification.json")
suite.load_qa_benchmark("data/qa.json")

# Run specific benchmark
results = suite.run_benchmark("gpt-4o", BenchmarkType.QA)

# Run all benchmarks
all_results = suite.run_all("gpt-4o")
print(all_results)
# {
#   "classification": {...},
#   "qa": {...}
# }
```

### Production Evaluation

```python
# Setup production evaluator
config = EvaluationConfig(
    sample_rate=0.1,  # Evaluate 10% of requests
    judge_model="gpt-4o"
)

evaluator = ProductionEvaluator(client, config)

# Evaluate production requests
def handle_request(user_input: str):
    response = generate_response(user_input)

    # Evaluate (sampled)
    evaluator.evaluate_request(
        input=user_input,
        output=response,
        metadata={"user_id": "123"}
    )

    return response

# Get metrics
metrics = evaluator.get_metrics(window_hours=24)
print(metrics)
# {
#   "total_evaluated": 42,
#   "check_pass_rates": {
#     "non_empty": 0.98,
#     "reasonable_length": 0.95,
#     "no_error_patterns": 0.92
#   },
#   "avg_output_length": 256
# }
```

## Best Practices

1. **Regular Evaluation**
   - Before major changes
   - Continuous production monitoring
   - Periodic comprehensive reviews

2. **Consistent Methodology**
   - Same prompts across models
   - Control for randomness (temperature=0)
   - Document evaluation setup

3. **Production Monitoring**
   - Sample evaluation (not 100%)
   - Alert on quality degradation
   - Track metrics over time

4. **Benchmark Diversity**
   - Cover different task types
   - Include edge cases
   - Balance difficulty levels

## Common Pitfalls

1. **Overfitting to Benchmarks** - Gaming specific metrics
2. **Small Test Sets** - Unreliable results (use 100+ cases)
3. **No Baseline** - Can't measure improvement
4. **Ignoring Edge Cases** - Failures in production
5. **Stale Test Data** - Doesn't reflect current use

## When to Use

| Method | Use Case |
|--------|----------|
| Model Comparison | Choosing between providers/models |
| Benchmark Suite | Standardized performance tracking |
| Production Evaluation | Continuous quality monitoring |

## References

- See also: [evaluation-framework.md](evaluation-framework.md) for core evaluation classes
- See also: [evaluation-metrics.md](evaluation-metrics.md) for metric implementations
- [HELM Benchmark](https://crfm.stanford.edu/helm/)
- [LM Evaluation Harness](https://github.com/EleutherAI/lm-evaluation-harness)
- [OpenAI Evals](https://github.com/openai/evals)

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Benchmark selection | sonnet | Evaluation suite |
| Score interpretation | sonnet | Analysis |
| Comparison analysis | sonnet | Evaluation |
