---
id: evaluation-framework
name: "Evaluation Framework"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
parent: model-evaluation
---

# Evaluation Framework

## Overview

Core evaluation framework and LLM-as-judge patterns for evaluating LLM outputs. Includes basic evaluation classes, automated metrics, and LLM-based quality assessment.

## Evaluation Types

```
┌─────────────────────────────────────────────────────────────┐
│                   OFFLINE EVALUATION                         │
│  - Test datasets                                             │
│  - Ground truth comparison                                   │
│  - Automated metrics                                         │
└─────────────────────────────────────────────────────────────┘
                           │
┌─────────────────────────▼───────────────────────────────────┐
│                   ONLINE EVALUATION                          │
│  - A/B testing                                               │
│  - User feedback                                             │
│  - Production metrics                                        │
└─────────────────────────────────────────────────────────────┘
```

## Basic Evaluation Framework

```python
from dataclasses import dataclass
from typing import List, Dict, Callable, Optional
from datetime import datetime
import json

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
        import time

        self.results = []

        for case in cases:
            start_time = time.time()

            try:
                # Make API call
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
Return JSON: {{"scores": {{"criterion": {{"score": N, "explanation": "..."}}}}, "overall": N}}"""

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

## Usage Examples

### Basic Evaluation

```python
from openai import OpenAI

client = OpenAI()

# Define test cases
cases = [
    EvaluationCase(
        input="What is the capital of France?",
        expected_output="Paris"
    ),
    EvaluationCase(
        input="Explain photosynthesis in one sentence.",
        expected_output=None  # No ground truth
    )
]

# Create evaluator
evaluator = ModelEvaluator(client, model="gpt-4o")

# Add metrics (import from evaluation-metrics.md)
evaluator.add_metric(exact_match)
evaluator.add_metric(contains_match)

# Run evaluation
results = evaluator.evaluate(cases)
print(results)
# {
#   "total_cases": 2,
#   "successful": 2,
#   "failed": 0,
#   "success_rate": 1.0,
#   "metrics": {...},
#   "latency": {...}
# }
```

### LLM-as-Judge

```python
judge = LLMJudge(client, model="gpt-4o")

# Evaluate single output
evaluation = judge.judge(
    input="Explain quantum computing",
    output="Quantum computing uses quantum bits...",
    criteria=["accuracy", "clarity", "completeness"]
)
print(evaluation)
# {
#   "scores": {
#     "accuracy": {"score": 4, "explanation": "..."},
#     "clarity": {"score": 5, "explanation": "..."},
#     "completeness": {"score": 3, "explanation": "..."}
#   },
#   "overall": 4
# }

# Pairwise comparison
comparison = judge.pairwise_comparison(
    input="What is AI?",
    output_a="AI is artificial intelligence...",
    output_b="Artificial intelligence refers to...",
    criteria="clarity and conciseness"
)
print(comparison)
# {"winner": "B", "explanation": "...", "confidence": 0.8}
```

## Best Practices

1. **Diverse Test Sets**
   - Cover edge cases
   - Include adversarial examples
   - Balance across categories

2. **Multiple Metrics**
   - Don't rely on single metric
   - Include automated and human eval
   - Track business metrics

3. **Consistent Methodology**
   - Same prompts across models
   - Control for randomness (temperature=0)
   - Document evaluation setup

4. **Human Baseline**
   - Compare to human performance
   - Get human labels for test set
   - Calibrate automated metrics

## When to Use

| Method | Use Case |
|--------|----------|
| ModelEvaluator | Offline testing with ground truth |
| LLM-as-Judge | Complex tasks without clear metrics |
| Pairwise Comparison | A/B testing, preference evaluation |

## Common Pitfalls

1. **Small Test Sets** - Unreliable results (use 100+ cases)
2. **No Baseline** - Can't measure improvement
3. **Single Metric Focus** - Missing important dimensions
4. **Inconsistent Prompts** - Results not comparable

## References

- See also: [evaluation-metrics.md](evaluation-metrics.md) for metric implementations
- See also: [evaluation-benchmarks.md](evaluation-benchmarks.md) for benchmarking and production monitoring
- [OpenAI Evals](https://github.com/openai/evals)
- [RAGAS](https://docs.ragas.io/)
