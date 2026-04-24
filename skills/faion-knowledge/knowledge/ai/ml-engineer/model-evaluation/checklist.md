# Model Evaluation Checklist

## Pre-Evaluation Setup

- [ ] Define evaluation goals (model selection, prompt optimization, monitoring)
- [ ] Identify target use cases and user scenarios
- [ ] Select appropriate benchmarks for your domain
- [ ] Prepare test dataset with ground truth labels
- [ ] Set baseline metrics from current solution

## Test Dataset Preparation

- [ ] Minimum 100 test cases for statistical significance
- [ ] Cover all expected input types
- [ ] Include edge cases and adversarial examples
- [ ] Balance across categories/classes
- [ ] Ensure no overlap with training data
- [ ] Document data sources and collection method

## Offline Evaluation

### Benchmark Selection

- [ ] Knowledge: MMLU-Pro, GPQA, ARC
- [ ] Reasoning: HellaSwag, WinoGrande, BoolQ
- [ ] Code: HumanEval+, LiveCodeBench, SWE-bench
- [ ] Math: GSM8K, MATH
- [ ] Safety: ToxiGen, BBQ

### Metrics Selection

| Task Type | Primary Metrics | Secondary Metrics |
|-----------|-----------------|-------------------|
| Classification | Accuracy, F1, Precision, Recall | Confusion matrix |
| Generation | BLEU, ROUGE, BERTScore | Length ratio |
| QA | Exact match, Contains match | F1 |
| Code | pass@1, pass@10 | Syntax validity |
| Summarization | ROUGE-L, BERTScore | Factual consistency |

- [ ] Select 2-3 primary metrics
- [ ] Define success thresholds
- [ ] Include latency and cost metrics

### Evaluation Execution

- [ ] Set temperature=0 for reproducibility
- [ ] Use same prompts across all models
- [ ] Run multiple seeds for stochastic outputs
- [ ] Log all inputs, outputs, and metadata
- [ ] Track token usage and latency

## LLM-as-Judge Evaluation

- [ ] Select judge model (GPT-4, Claude 3.5 Sonnet)
- [ ] Define evaluation criteria with clear rubrics
- [ ] Create scoring prompts (1-5 scale or pairwise)
- [ ] Include reference answers when available
- [ ] Run multiple judgments for consistency check
- [ ] Calculate inter-rater agreement

### Criteria to Evaluate

- [ ] Relevance to the question
- [ ] Factual accuracy
- [ ] Completeness of answer
- [ ] Clarity and coherence
- [ ] Safety and appropriateness
- [ ] Instruction following

## A/B Testing

### Setup

- [ ] Define hypothesis and success metrics
- [ ] Calculate required sample size
- [ ] Set up traffic splitting (50/50 or staged rollout)
- [ ] Implement tracking for all variants
- [ ] Define experiment duration

### Execution

- [ ] Monitor for sample ratio mismatch
- [ ] Track guardrail metrics (errors, latency)
- [ ] Collect user feedback
- [ ] Log all decisions and outputs

### Analysis

- [ ] Calculate statistical significance (p < 0.05)
- [ ] Check for novelty effects
- [ ] Segment analysis (user types, regions)
- [ ] Document learnings

## Model Comparison

- [ ] Test same prompts across all models
- [ ] Compare on multiple dimensions:
  - [ ] Quality (accuracy, relevance)
  - [ ] Latency (p50, p95, p99)
  - [ ] Cost ($/1K tokens, $/request)
  - [ ] Reliability (success rate)
  - [ ] Safety (toxicity, bias)
- [ ] Create comparison matrix
- [ ] Consider trade-offs (quality vs cost vs latency)

## Production Monitoring

### Setup

- [ ] Implement sampling (1-10% of traffic)
- [ ] Set up logging pipeline
- [ ] Create dashboards for key metrics
- [ ] Configure alerts for anomalies

### Ongoing

- [ ] Daily: Check error rates and latency
- [ ] Weekly: Review sampled outputs
- [ ] Monthly: Run comprehensive evaluation
- [ ] Quarterly: Refresh test datasets

### Alert Thresholds

| Metric | Warning | Critical |
|--------|---------|----------|
| Error rate | > 1% | > 5% |
| p95 latency | > 3s | > 10s |
| Empty responses | > 0.5% | > 2% |
| Quality score | < 4.0 | < 3.5 |

## Documentation

- [ ] Document evaluation methodology
- [ ] Record all model versions tested
- [ ] Save test datasets with version control
- [ ] Archive evaluation results
- [ ] Write summary report with recommendations

## Common Pitfalls to Avoid

- [ ] Avoid overfitting to specific benchmarks
- [ ] Don't rely on single metric
- [ ] Ensure test data is not in training set
- [ ] Don't skip edge case testing
- [ ] Avoid small sample sizes
- [ ] Don't ignore latency/cost in favor of quality
- [ ] Remember to establish baselines
- [ ] Don't forget human evaluation for subjective tasks

## Quality Gates

### Before Staging

- [ ] All automated tests pass
- [ ] Quality metrics meet threshold
- [ ] Latency within SLA
- [ ] No safety issues detected

### Before Production

- [ ] Staging evaluation complete
- [ ] A/B test shows positive results
- [ ] Rollback plan documented
- [ ] Monitoring dashboards ready

## Post-Deployment

- [ ] Monitor first 24h closely
- [ ] Collect initial user feedback
- [ ] Compare production metrics to offline evaluation
- [ ] Document any discrepancies
- [ ] Schedule follow-up evaluation
