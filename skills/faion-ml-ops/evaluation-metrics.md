---
id: evaluation-metrics
name: "Evaluation Metrics"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
parent: model-evaluation
---

# Evaluation Metrics

## Overview

Metrics for measuring LLM performance across different dimensions including accuracy, quality, latency, cost, safety, and reliability.

## Evaluation Dimensions

| Dimension | Metrics | Priority |
|-----------|---------|----------|
| Quality | Accuracy, F1, BLEU, ROUGE | High |
| Latency | p50, p95, p99 | Medium-High |
| Cost | $/1K tokens, $/request | Medium |
| Safety | Toxicity, bias, refusal rate | High |
| Reliability | Success rate, error rate | High |

## Common Metrics

### Exact Match

```python
def exact_match(input: str, actual: str, expected: Optional[str]) -> float:
    """Check if output exactly matches expected."""
    if expected is None:
        return None
    return 1.0 if actual.strip() == expected.strip() else 0.0
```

### Contains Match

```python
def contains_match(input: str, actual: str, expected: Optional[str]) -> float:
    """Check if expected is contained in output."""
    if expected is None:
        return None
    return 1.0 if expected.lower() in actual.lower() else 0.0
```

### Length Ratio

```python
def length_ratio(input: str, actual: str, expected: Optional[str]) -> float:
    """Ratio of actual length to expected length."""
    if expected is None or len(expected) == 0:
        return None
    return len(actual) / len(expected)
```

### BLEU Score

```python
def bleu_score(input: str, actual: str, expected: Optional[str]) -> float:
    """Calculate BLEU score for translation/generation."""
    if expected is None:
        return None

    from nltk.translate.bleu_score import sentence_bleu
    from nltk.tokenize import word_tokenize

    reference = [word_tokenize(expected.lower())]
    hypothesis = word_tokenize(actual.lower())

    return sentence_bleu(reference, hypothesis)
```

### ROUGE Score

```python
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
```

### Semantic Similarity

```python
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
```

## Task-Specific Metrics

### Classification

```python
def classification_accuracy(predictions: List, labels: List) -> float:
    """Accuracy for classification tasks."""
    correct = sum(1 for p, l in zip(predictions, labels) if p == l)
    return correct / len(predictions)

def classification_f1(predictions: List, labels: List, average='macro') -> float:
    """F1 score for classification."""
    from sklearn.metrics import f1_score
    return f1_score(labels, predictions, average=average)
```

### Question Answering

```python
def qa_exact_match(prediction: str, ground_truth: str) -> float:
    """QA exact match after normalization."""
    import re
    import string

    def normalize(text):
        # Remove articles, punctuation, extra whitespace
        text = text.lower()
        text = re.sub(r'\b(a|an|the)\b', ' ', text)
        text = text.translate(str.maketrans('', '', string.punctuation))
        text = ' '.join(text.split())
        return text

    return 1.0 if normalize(prediction) == normalize(ground_truth) else 0.0

def qa_f1(prediction: str, ground_truth: str) -> float:
    """Token-level F1 for QA."""
    pred_tokens = prediction.lower().split()
    truth_tokens = ground_truth.lower().split()

    common = set(pred_tokens) & set(truth_tokens)

    if len(common) == 0:
        return 0.0

    precision = len(common) / len(pred_tokens)
    recall = len(common) / len(truth_tokens)

    return 2 * (precision * recall) / (precision + recall)
```

### Summarization

```python
def summarization_metrics(summary: str, reference: str) -> Dict:
    """Comprehensive summarization metrics."""
    from rouge_score import rouge_scorer

    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    scores = scorer.score(reference, summary)

    return {
        "rouge1_f": scores['rouge1'].fmeasure,
        "rouge2_f": scores['rouge2'].fmeasure,
        "rougeL_f": scores['rougeL'].fmeasure,
        "compression_ratio": len(summary) / len(reference)
    }
```

### Code Generation

```python
def code_pass_at_k(predictions: List[str], test_cases: List, k: int = 1) -> float:
    """Pass@k metric for code generation."""
    passed = 0

    for pred_list in predictions:
        # Take top k predictions
        top_k = pred_list[:k]

        # Check if any pass all test cases
        for pred in top_k:
            if all(test(pred) for test in test_cases):
                passed += 1
                break

    return passed / len(predictions)
```

## Performance Metrics

### Latency

```python
import numpy as np

def latency_stats(latencies: List[float]) -> Dict:
    """Calculate latency statistics."""
    return {
        "mean_ms": np.mean(latencies),
        "median_ms": np.median(latencies),
        "p50_ms": np.percentile(latencies, 50),
        "p95_ms": np.percentile(latencies, 95),
        "p99_ms": np.percentile(latencies, 99),
        "min_ms": np.min(latencies),
        "max_ms": np.max(latencies)
    }
```

### Cost

```python
def cost_metrics(
    input_tokens: List[int],
    output_tokens: List[int],
    input_price_per_1k: float,
    output_price_per_1k: float
) -> Dict:
    """Calculate cost metrics."""
    total_input = sum(input_tokens)
    total_output = sum(output_tokens)

    input_cost = (total_input / 1000) * input_price_per_1k
    output_cost = (total_output / 1000) * output_price_per_1k
    total_cost = input_cost + output_cost

    return {
        "total_cost": total_cost,
        "input_cost": input_cost,
        "output_cost": output_cost,
        "avg_cost_per_request": total_cost / len(input_tokens),
        "total_tokens": total_input + total_output
    }
```

### Reliability

```python
def reliability_metrics(results: List[Dict]) -> Dict:
    """Calculate reliability metrics."""
    total = len(results)
    successful = sum(1 for r in results if not r.get('error'))
    errors = total - successful

    error_types = {}
    for r in results:
        if r.get('error'):
            error_type = type(r['error']).__name__
            error_types[error_type] = error_types.get(error_type, 0) + 1

    return {
        "success_rate": successful / total,
        "error_rate": errors / total,
        "total_requests": total,
        "successful_requests": successful,
        "failed_requests": errors,
        "error_types": error_types
    }
```

## Safety Metrics

### Toxicity Detection

```python
def toxicity_score(text: str, toxicity_model) -> float:
    """Detect toxicity in generated text."""
    # Using Perspective API or similar
    result = toxicity_model.analyze(text)
    return result['toxicity']['score']

def safe_content_rate(outputs: List[str], toxicity_threshold=0.5) -> Dict:
    """Calculate safe content rate."""
    from transformers import pipeline

    toxicity = pipeline("text-classification", model="unitary/toxic-bert")

    toxic_count = 0
    for output in outputs:
        scores = toxicity(output)[0]
        if scores['label'] == 'toxic' and scores['score'] > toxicity_threshold:
            toxic_count += 1

    return {
        "safe_rate": (len(outputs) - toxic_count) / len(outputs),
        "toxic_count": toxic_count,
        "total": len(outputs)
    }
```

### Bias Detection

```python
def bias_metrics(outputs: List[str], protected_attributes: List[str]) -> Dict:
    """Detect bias in outputs."""
    bias_scores = {}

    for attr in protected_attributes:
        # Count mentions of protected attribute
        mentions = sum(1 for out in outputs if attr.lower() in out.lower())
        bias_scores[attr] = mentions / len(outputs)

    return {
        "protected_attribute_mention_rates": bias_scores,
        "max_mention_rate": max(bias_scores.values()),
        "min_mention_rate": min(bias_scores.values())
    }
```

### Refusal Rate

```python
def refusal_rate(outputs: List[str]) -> Dict:
    """Calculate refusal rate for unsafe prompts."""
    refusal_patterns = [
        "i cannot", "i can't", "sorry", "unable to",
        "not appropriate", "against policy", "as an ai"
    ]

    refusals = 0
    for output in outputs:
        output_lower = output.lower()
        if any(pattern in output_lower for pattern in refusal_patterns):
            refusals += 1

    return {
        "refusal_rate": refusals / len(outputs),
        "refusal_count": refusals,
        "total": len(outputs)
    }
```

## Aggregation

### Metric Aggregation

```python
def aggregate_metrics(results: List[Dict], metric_name: str) -> Dict:
    """Aggregate a metric across results."""
    values = [
        r['metrics'].get(metric_name)
        for r in results
        if isinstance(r['metrics'].get(metric_name), (int, float))
    ]

    if not values:
        return None

    import numpy as np

    return {
        "mean": np.mean(values),
        "median": np.median(values),
        "std": np.std(values),
        "min": np.min(values),
        "max": np.max(values),
        "count": len(values)
    }
```

### Multi-Metric Summary

```python
def create_metric_summary(results: List[Dict]) -> Dict:
    """Create summary of all metrics."""
    summary = {
        "total_cases": len(results),
        "metrics": {}
    }

    # Get all unique metric names
    all_metrics = set()
    for r in results:
        all_metrics.update(r.get('metrics', {}).keys())

    # Aggregate each metric
    for metric in all_metrics:
        summary['metrics'][metric] = aggregate_metrics(results, metric)

    # Add performance stats
    latencies = [r.get('latency_ms', 0) for r in results]
    summary['latency'] = latency_stats(latencies)

    tokens = [r.get('tokens_used', 0) for r in results]
    summary['total_tokens'] = sum(tokens)
    summary['avg_tokens'] = sum(tokens) / len(tokens) if tokens else 0

    return summary
```

## Best Practices

1. **Multiple Metrics** - Use 3-5 metrics per task type
2. **Task-Specific** - Choose metrics matching evaluation goals
3. **Automated + Human** - Combine automated metrics with human eval
4. **Baseline Comparison** - Always compare to baseline
5. **Statistical Significance** - Use adequate sample sizes (100+ cases)
6. **Track Over Time** - Monitor metric trends in production

## References

- [BLEU Score](https://www.aclweb.org/anthology/P02-1040.pdf)
- [ROUGE Score](https://www.aclweb.org/anthology/W04-1013.pdf)
- [Perspective API](https://perspectiveapi.com/)
- [HuggingFace Evaluate](https://huggingface.co/docs/evaluate/)
