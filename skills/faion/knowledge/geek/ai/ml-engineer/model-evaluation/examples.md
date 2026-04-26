# Model Evaluation Examples

## Basic Evaluation Framework

```python
from dataclasses import dataclass
from typing import List, Dict, Callable, Optional
from datetime import datetime
import json
import time

@dataclass
class EvaluationCase:
    input: str
    expected_output: Optional[str] = None
    metadata: Dict = None

@dataclass
class EvaluationResult:
    case: EvaluationCase
    actual_output: str
    metrics: Dict
    latency_ms: float
    tokens_used: int
    error: Optional[str] = None

class ModelEvaluator:
    """Evaluate LLM performance on test cases."""

    def __init__(
        self,
        client,
        model: str = "gpt-4o",
        metrics: List[Callable] = None
    ):
        self.client = client
        self.model = model
        self.metrics = metrics or []
        self.results: List[EvaluationResult] = []

    def add_metric(self, metric_fn: Callable):
        """Add a metric function."""
        self.metrics.append(metric_fn)

    def evaluate(
        self,
        cases: List[EvaluationCase],
        system_prompt: str = ""
    ) -> Dict:
        """Evaluate model on test cases."""
        self.results = []

        for case in cases:
            start_time = time.time()

            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": case.input}
                    ]
                )

                actual_output = response.choices[0].message.content
                latency_ms = (time.time() - start_time) * 1000
                tokens_used = response.usage.total_tokens

                # Calculate metrics
                metrics = {}
                for metric_fn in self.metrics:
                    try:
                        metric_name = metric_fn.__name__
                        metric_value = metric_fn(
                            case.input,
                            actual_output,
                            case.expected_output
                        )
                        metrics[metric_name] = metric_value
                    except Exception as e:
                        metrics[metric_fn.__name__] = {"error": str(e)}

                result = EvaluationResult(
                    case=case,
                    actual_output=actual_output,
                    metrics=metrics,
                    latency_ms=latency_ms,
                    tokens_used=tokens_used
                )

            except Exception as e:
                result = EvaluationResult(
                    case=case,
                    actual_output="",
                    metrics={},
                    latency_ms=(time.time() - start_time) * 1000,
                    tokens_used=0,
                    error=str(e)
                )

            self.results.append(result)

        return self._aggregate_results()

    def _aggregate_results(self) -> Dict:
        """Aggregate evaluation results."""
        if not self.results:
            return {}

        successful = [r for r in self.results if r.error is None]
        failed = [r for r in self.results if r.error is not None]

        # Aggregate metrics
        metric_aggregates = {}
        for metric_fn in self.metrics:
            metric_name = metric_fn.__name__
            values = [
                r.metrics.get(metric_name)
                for r in successful
                if isinstance(r.metrics.get(metric_name), (int, float))
            ]
            if values:
                metric_aggregates[metric_name] = {
                    "mean": sum(values) / len(values),
                    "min": min(values),
                    "max": max(values)
                }

        # Latency stats
        latencies = [r.latency_ms for r in successful]

        return {
            "total_cases": len(self.results),
            "successful": len(successful),
            "failed": len(failed),
            "success_rate": len(successful) / len(self.results),
            "metrics": metric_aggregates,
            "latency": {
                "mean_ms": sum(latencies) / len(latencies) if latencies else 0,
                "p50_ms": sorted(latencies)[len(latencies)//2] if latencies else 0,
                "p95_ms": sorted(latencies)[int(len(latencies)*0.95)] if latencies else 0
            },
            "total_tokens": sum(r.tokens_used for r in successful)
        }
```

## Common Metrics

```python
import re
from typing import Optional, Dict

# Exact match
def exact_match(input: str, actual: str, expected: Optional[str]) -> float:
    """Check if output exactly matches expected."""
    if expected is None:
        return None
    return 1.0 if actual.strip() == expected.strip() else 0.0

# Contains match
def contains_match(input: str, actual: str, expected: Optional[str]) -> float:
    """Check if expected is contained in output."""
    if expected is None:
        return None
    return 1.0 if expected.lower() in actual.lower() else 0.0

# Length ratio
def length_ratio(input: str, actual: str, expected: Optional[str]) -> float:
    """Ratio of actual length to expected length."""
    if expected is None or len(expected) == 0:
        return None
    return len(actual) / len(expected)

# BLEU score
def bleu_score(input: str, actual: str, expected: Optional[str]) -> float:
    """Calculate BLEU score for translation/generation."""
    if expected is None:
        return None

    from nltk.translate.bleu_score import sentence_bleu
    from nltk.tokenize import word_tokenize

    reference = [word_tokenize(expected.lower())]
    hypothesis = word_tokenize(actual.lower())

    return sentence_bleu(reference, hypothesis)

# ROUGE score
def rouge_score(input: str, actual: str, expected: Optional[str]) -> Dict:
    """Calculate ROUGE scores for summarization."""
    if expected is None:
        return None

    from rouge_score import rouge_scorer

    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'])
    scores = scorer.score(expected, actual)

    return {
        "rouge1": scores['rouge1'].fmeasure,
        "rouge2": scores['rouge2'].fmeasure,
        "rougeL": scores['rougeL'].fmeasure
    }

# Semantic similarity using embeddings
def semantic_similarity(
    input: str,
    actual: str,
    expected: Optional[str],
    embedding_func: Callable = None
) -> float:
    """Calculate semantic similarity using embeddings."""
    if expected is None or embedding_func is None:
        return None

    import numpy as np

    emb_actual = embedding_func(actual)
    emb_expected = embedding_func(expected)

    similarity = np.dot(emb_actual, emb_expected) / (
        np.linalg.norm(emb_actual) * np.linalg.norm(emb_expected)
    )

    return float(similarity)

# pass@k for code generation
def pass_at_k(n: int, c: int, k: int) -> float:
    """
    Calculate pass@k metric.
    n: total number of samples
    c: number of correct samples
    k: k in pass@k
    """
    if n - c < k:
        return 1.0
    return 1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1))
```

## LLM-as-Judge Evaluation

```python
class LLMJudge:
    """Use LLM to evaluate outputs."""

    def __init__(self, client, model: str = "gpt-4o"):
        self.client = client
        self.model = model

    def judge(
        self,
        input: str,
        output: str,
        criteria: List[str],
        reference: Optional[str] = None
    ) -> Dict:
        """Evaluate output using LLM judge."""
        criteria_str = "\n".join([f"- {c}" for c in criteria])

        prompt = f"""Evaluate the following response based on these criteria:
{criteria_str}

Input: {input}

Response: {output}
"""
        if reference:
            prompt += f"\nReference answer: {reference}\n"

        prompt += """
For each criterion, provide a score from 1-5 and brief explanation.
Return JSON: {"scores": {"criterion": {"score": N, "explanation": "..."}}, "overall": N}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)

    def pairwise_comparison(
        self,
        input: str,
        output_a: str,
        output_b: str,
        criteria: str
    ) -> Dict:
        """Compare two outputs and pick the better one."""
        prompt = f"""Compare these two responses and determine which is better.

Criterion: {criteria}

Input: {input}

Response A:
{output_a}

Response B:
{output_b}

Return JSON: {{"winner": "A" or "B" or "tie", "explanation": "...", "confidence": 0.0-1.0}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)

    def evaluate_batch(
        self,
        cases: List[Dict],
        criteria: List[str]
    ) -> List[Dict]:
        """Evaluate multiple cases."""
        results = []

        for case in cases:
            result = self.judge(
                input=case["input"],
                output=case["output"],
                criteria=criteria,
                reference=case.get("reference")
            )
            results.append({
                "input": case["input"],
                "output": case["output"],
                "evaluation": result
            })

        return results
```

## Model Comparison

```python
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

## A/B Testing Framework

```python
import random
import hashlib
from typing import Optional, Dict, Any
from datetime import datetime

class ABTest:
    """A/B testing framework for LLM variants."""

    def __init__(
        self,
        experiment_name: str,
        variants: Dict[str, Any],  # {"control": config_a, "treatment": config_b}
        traffic_split: Dict[str, float] = None  # {"control": 0.5, "treatment": 0.5}
    ):
        self.experiment_name = experiment_name
        self.variants = variants
        self.traffic_split = traffic_split or {k: 1.0/len(variants) for k in variants}
        self.results = {variant: [] for variant in variants}

    def assign_variant(self, user_id: str) -> str:
        """Deterministically assign user to variant."""
        hash_input = f"{self.experiment_name}:{user_id}"
        hash_value = int(hashlib.md5(hash_input.encode()).hexdigest(), 16)
        normalized = (hash_value % 10000) / 10000

        cumulative = 0
        for variant, split in self.traffic_split.items():
            cumulative += split
            if normalized < cumulative:
                return variant

        return list(self.variants.keys())[-1]

    def record_result(
        self,
        variant: str,
        user_id: str,
        metrics: Dict[str, float]
    ):
        """Record experiment result."""
        self.results[variant].append({
            "user_id": user_id,
            "timestamp": datetime.now().isoformat(),
            "metrics": metrics
        })

    def analyze(self) -> Dict:
        """Analyze experiment results."""
        analysis = {}

        for variant, results in self.results.items():
            if not results:
                continue

            # Aggregate metrics
            all_metrics = {}
            for result in results:
                for metric, value in result["metrics"].items():
                    if metric not in all_metrics:
                        all_metrics[metric] = []
                    all_metrics[metric].append(value)

            analysis[variant] = {
                "n": len(results),
                "metrics": {
                    metric: {
                        "mean": sum(values) / len(values),
                        "std": self._std(values),
                        "min": min(values),
                        "max": max(values)
                    }
                    for metric, values in all_metrics.items()
                }
            }

        # Statistical significance
        if len(self.results) == 2:
            variants = list(self.results.keys())
            analysis["comparison"] = self._compare_variants(
                variants[0], variants[1]
            )

        return analysis

    def _std(self, values: List[float]) -> float:
        """Calculate standard deviation."""
        if len(values) < 2:
            return 0
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / (len(values) - 1)
        return variance ** 0.5

    def _compare_variants(self, variant_a: str, variant_b: str) -> Dict:
        """Compare two variants using t-test."""
        from scipy import stats

        results_a = self.results[variant_a]
        results_b = self.results[variant_b]

        if not results_a or not results_b:
            return {}

        # Get first metric for comparison
        metric = list(results_a[0]["metrics"].keys())[0]

        values_a = [r["metrics"][metric] for r in results_a]
        values_b = [r["metrics"][metric] for r in results_b]

        t_stat, p_value = stats.ttest_ind(values_a, values_b)

        return {
            "metric": metric,
            "t_statistic": t_stat,
            "p_value": p_value,
            "significant": p_value < 0.05,
            "winner": variant_a if sum(values_a)/len(values_a) > sum(values_b)/len(values_b) else variant_b
        }
```

## Production Evaluation Service

```python
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
import logging
from datetime import datetime, timedelta

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
        import random
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
                self.logger.warning(f"Quality check failed: {check_name}")

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

## Benchmark Suite

```python
from enum import Enum
from typing import Dict, List

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

        # Add appropriate metrics
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

## Using DeepEval Library

```python
# pip install deepeval

from deepeval import evaluate
from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric,
    ContextualPrecisionMetric,
    ContextualRecallMetric,
    HallucinationMetric
)
from deepeval.test_case import LLMTestCase

# Create test cases
test_case = LLMTestCase(
    input="What is the capital of France?",
    actual_output="The capital of France is Paris.",
    expected_output="Paris",
    context=["France is a country in Western Europe. Its capital is Paris."]
)

# Define metrics
metrics = [
    AnswerRelevancyMetric(threshold=0.7),
    FaithfulnessMetric(threshold=0.7),
    HallucinationMetric(threshold=0.5)
]

# Run evaluation
results = evaluate([test_case], metrics)
```

## Using RAGAS for RAG Evaluation

```python
# pip install ragas

from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall
)
from datasets import Dataset

# Prepare data
data = {
    "question": ["What is the capital of France?"],
    "answer": ["The capital of France is Paris."],
    "contexts": [["France is a country in Western Europe. Its capital is Paris."]],
    "ground_truth": ["Paris"]
}

dataset = Dataset.from_dict(data)

# Evaluate
results = evaluate(
    dataset,
    metrics=[
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall
    ]
)

print(results)
```
