# Model Evaluation Templates

## Evaluation Report Template

```markdown
# Model Evaluation Report

**Date:** YYYY-MM-DD
**Evaluator:** [Name/Team]
**Models Evaluated:** [Model A, Model B, ...]
**Purpose:** [Model selection / Prompt optimization / Pre-deployment / Monitoring]

## Executive Summary

[2-3 sentences summarizing key findings and recommendation]

## Evaluation Setup

### Test Dataset

| Property | Value |
|----------|-------|
| Total cases | N |
| Categories | [List categories] |
| Source | [How data was collected] |
| Date range | [If applicable] |

### Metrics Used

| Metric | Type | Threshold |
|--------|------|-----------|
| [Metric 1] | Quality | >= X |
| [Metric 2] | Latency | <= Y ms |
| [Metric 3] | Cost | <= $Z |

### Configuration

- Temperature: [0 / 0.7 / ...]
- System prompt: [Included/Excluded]
- Max tokens: [N]

## Results

### Quality Metrics

| Model | Metric 1 | Metric 2 | Metric 3 |
|-------|----------|----------|----------|
| Model A | X | Y | Z |
| Model B | X | Y | Z |

### Latency

| Model | p50 (ms) | p95 (ms) | p99 (ms) |
|-------|----------|----------|----------|
| Model A | X | Y | Z |
| Model B | X | Y | Z |

### Cost

| Model | $/1K input | $/1K output | Avg $/request |
|-------|------------|-------------|---------------|
| Model A | X | Y | Z |
| Model B | X | Y | Z |

## Analysis

### Strengths and Weaknesses

**Model A:**
- Strengths: [List]
- Weaknesses: [List]

**Model B:**
- Strengths: [List]
- Weaknesses: [List]

### Edge Cases

[Document any edge cases where models performed differently]

### Failure Analysis

[Analyze common failure modes]

## Recommendation

**Recommended Model:** [Model X]

**Rationale:**
1. [Reason 1]
2. [Reason 2]
3. [Reason 3]

**Trade-offs:**
- [What we're sacrificing]
- [What we're gaining]

## Next Steps

- [ ] [Action 1]
- [ ] [Action 2]
- [ ] [Action 3]

## Appendix

### Raw Data

[Link to detailed results]

### Test Cases Sample

[Include 3-5 representative test cases with results]
```

## Test Dataset Template

```json
{
  "metadata": {
    "name": "Dataset Name",
    "version": "1.0.0",
    "created": "2025-01-01",
    "description": "Description of the dataset",
    "categories": ["cat1", "cat2"],
    "total_cases": 100
  },
  "cases": [
    {
      "id": "case_001",
      "category": "category_name",
      "input": "User input text",
      "expected_output": "Expected model output",
      "context": "Optional context",
      "metadata": {
        "difficulty": "easy|medium|hard",
        "tags": ["tag1", "tag2"],
        "source": "source_of_case"
      }
    }
  ]
}
```

## Benchmark Configuration Template

```yaml
# benchmark_config.yaml

name: "Custom Benchmark"
version: "1.0.0"
description: "Benchmark for [specific use case]"

models:
  - name: "gpt-4o"
    provider: "openai"
    parameters:
      temperature: 0
      max_tokens: 1000

  - name: "claude-3-5-sonnet"
    provider: "anthropic"
    parameters:
      temperature: 0
      max_tokens: 1000

dataset:
  path: "./data/test_cases.json"
  sample_size: null  # null = use all
  categories: null   # null = use all

metrics:
  quality:
    - name: "exact_match"
      threshold: 0.8
    - name: "contains_match"
      threshold: 0.9
    - name: "bleu_score"
      threshold: 0.5

  latency:
    p50_threshold_ms: 1000
    p95_threshold_ms: 3000
    p99_threshold_ms: 5000

  cost:
    max_per_request: 0.05

evaluation:
  runs_per_case: 1
  parallel_requests: 5
  timeout_seconds: 30

output:
  format: "json"
  path: "./results/"
  include_raw_outputs: true
```

## A/B Test Plan Template

```markdown
# A/B Test Plan

## Experiment Details

| Field | Value |
|-------|-------|
| Experiment Name | [Name] |
| Hypothesis | [What we expect to happen] |
| Start Date | YYYY-MM-DD |
| End Date | YYYY-MM-DD |
| Owner | [Name/Team] |

## Variants

### Control (A)
- Model: [Model name]
- System prompt: [Description]
- Configuration: [Key parameters]

### Treatment (B)
- Model: [Model name]
- System prompt: [Description]
- Configuration: [Key parameters]

## Traffic Split

| Variant | Percentage |
|---------|------------|
| Control | 50% |
| Treatment | 50% |

## Success Metrics

### Primary Metric
- **Metric:** [Name]
- **Current baseline:** [X]
- **Target improvement:** [Y%]
- **Minimum detectable effect:** [Z%]

### Secondary Metrics
- [Metric 1]: [Description]
- [Metric 2]: [Description]

### Guardrail Metrics
- Error rate: Must not increase by > 1%
- Latency p95: Must not increase by > 200ms
- Cost: Must not increase by > 10%

## Sample Size Calculation

- Baseline conversion rate: [X%]
- Minimum detectable effect: [Y%]
- Statistical power: 80%
- Significance level: 5%
- **Required sample size per variant:** [N]

## Rollout Plan

1. **Day 1-2:** 5% traffic, monitor for errors
2. **Day 3-7:** 50% traffic, collect data
3. **Day 8:** Analysis and decision

## Analysis Plan

1. Check for sample ratio mismatch
2. Calculate statistical significance
3. Segment analysis by:
   - User type
   - Device
   - Region
4. Review qualitative feedback
5. Make go/no-go decision

## Rollback Criteria

Automatically rollback if:
- Error rate > [X%]
- Latency p95 > [Y ms]
- Quality score < [Z]

## Sign-off

- [ ] Engineering
- [ ] Product
- [ ] Data Science
```

## LLM-as-Judge Evaluation Template

```yaml
# judge_config.yaml

judge:
  model: "gpt-4o"
  temperature: 0
  max_tokens: 500

evaluation_criteria:
  - name: "relevance"
    description: "How relevant is the response to the user's question?"
    scoring:
      1: "Completely irrelevant"
      2: "Mostly irrelevant with minor relevant points"
      3: "Partially relevant"
      4: "Mostly relevant with minor gaps"
      5: "Completely relevant and on-topic"

  - name: "accuracy"
    description: "How factually accurate is the response?"
    scoring:
      1: "Contains multiple factual errors"
      2: "Contains some factual errors"
      3: "Mostly accurate with minor errors"
      4: "Accurate with negligible errors"
      5: "Completely accurate"

  - name: "helpfulness"
    description: "How helpful is the response for the user?"
    scoring:
      1: "Not helpful at all"
      2: "Minimally helpful"
      3: "Somewhat helpful"
      4: "Helpful"
      5: "Extremely helpful"

  - name: "coherence"
    description: "How well-structured and coherent is the response?"
    scoring:
      1: "Incoherent and disorganized"
      2: "Poorly structured"
      3: "Adequately structured"
      4: "Well-structured"
      5: "Excellently structured and flows naturally"

  - name: "safety"
    description: "Is the response safe and appropriate?"
    scoring:
      1: "Contains harmful or inappropriate content"
      2: "Contains potentially problematic content"
      3: "Neutral, no concerning content"
      4: "Appropriate and safe"
      5: "Exemplary in safety and appropriateness"

output_format: "json"
include_explanations: true
```

## Production Monitoring Dashboard Template

```yaml
# monitoring_config.yaml

service_name: "llm-service"
environment: "production"

metrics:
  request_metrics:
    - name: "request_count"
      type: "counter"
      labels: ["model", "endpoint", "status"]

    - name: "request_latency_ms"
      type: "histogram"
      buckets: [100, 250, 500, 1000, 2500, 5000, 10000]
      labels: ["model", "endpoint"]

    - name: "tokens_used"
      type: "histogram"
      buckets: [100, 500, 1000, 2000, 4000, 8000]
      labels: ["model", "token_type"]

  quality_metrics:
    - name: "quality_score"
      type: "gauge"
      labels: ["model", "criterion"]

    - name: "error_rate"
      type: "gauge"
      labels: ["model", "error_type"]

alerts:
  - name: "high_error_rate"
    condition: "error_rate > 0.05"
    severity: "critical"
    channels: ["slack", "pagerduty"]

  - name: "high_latency"
    condition: "p95_latency_ms > 5000"
    severity: "warning"
    channels: ["slack"]

  - name: "quality_degradation"
    condition: "quality_score < 3.5"
    severity: "warning"
    channels: ["slack"]

sampling:
  default_rate: 0.1
  rules:
    - condition: "error"
      rate: 1.0  # Sample all errors
    - condition: "latency > 5000"
      rate: 1.0  # Sample all slow requests

retention:
  raw_logs: "7d"
  aggregated_metrics: "90d"
  evaluation_results: "365d"
```

## Evaluation Results Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["metadata", "summary", "results"],
  "properties": {
    "metadata": {
      "type": "object",
      "required": ["experiment_id", "timestamp", "model", "dataset"],
      "properties": {
        "experiment_id": {"type": "string"},
        "timestamp": {"type": "string", "format": "date-time"},
        "model": {"type": "string"},
        "dataset": {"type": "string"},
        "config": {"type": "object"}
      }
    },
    "summary": {
      "type": "object",
      "required": ["total_cases", "successful", "failed", "metrics"],
      "properties": {
        "total_cases": {"type": "integer"},
        "successful": {"type": "integer"},
        "failed": {"type": "integer"},
        "success_rate": {"type": "number"},
        "metrics": {
          "type": "object",
          "additionalProperties": {
            "type": "object",
            "properties": {
              "mean": {"type": "number"},
              "min": {"type": "number"},
              "max": {"type": "number"},
              "std": {"type": "number"}
            }
          }
        },
        "latency": {
          "type": "object",
          "properties": {
            "mean_ms": {"type": "number"},
            "p50_ms": {"type": "number"},
            "p95_ms": {"type": "number"},
            "p99_ms": {"type": "number"}
          }
        }
      }
    },
    "results": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["case_id", "input", "output", "metrics"],
        "properties": {
          "case_id": {"type": "string"},
          "input": {"type": "string"},
          "output": {"type": "string"},
          "expected": {"type": "string"},
          "metrics": {"type": "object"},
          "latency_ms": {"type": "number"},
          "tokens": {"type": "integer"},
          "error": {"type": "string"}
        }
      }
    }
  }
}
```
