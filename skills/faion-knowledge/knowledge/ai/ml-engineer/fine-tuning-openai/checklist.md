# OpenAI Fine-Tuning Checklist

Step-by-step workflow for fine-tuning OpenAI models.

## Phase 1: Planning

### 1.1 Requirements Assessment

- [ ] Define the specific task/behavior to improve
- [ ] Confirm prompt engineering alone is insufficient
- [ ] Identify success metrics (accuracy, style, format)
- [ ] Choose fine-tuning method: SFT or DPO
- [ ] Select base model based on cost/performance needs

### 1.2 Model Selection

| Use Case | Recommended Model | Notes |
|----------|-------------------|-------|
| Complex reasoning | gpt-4.1 | Highest quality, 1M context |
| Production workloads | gpt-4.1-mini | Best cost/quality ratio |
| High-volume simple tasks | gpt-4.1-nano | Lowest cost |
| Vision/multimodal | gpt-4o | Image fine-tuning support |
| Budget production | gpt-4o-mini | Good quality, low cost |

### 1.3 Cost Estimation

- [ ] Estimate training tokens (file size x epochs)
- [ ] Calculate training cost
- [ ] Estimate monthly inference volume
- [ ] Calculate total cost vs base model

```
Training: [tokens] x [epochs] x [$/M] = $___
Inference: [monthly_tokens] x [$/M] = $___/month
```

## Phase 2: Data Preparation

### 2.1 Data Collection

- [ ] Collect 50-100+ high-quality examples minimum
- [ ] Ensure diversity across edge cases
- [ ] Include examples of desired output format
- [ ] Balance categories if classification task

### 2.2 Data Formatting

**SFT Format (JSONL):**
```json
{"messages": [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}
```

**DPO Format (JSONL):**
```json
{"input": [{"role": "user", "content": "..."}], "preferred_output": [{"role": "assistant", "content": "..."}], "non_preferred_output": [{"role": "assistant", "content": "..."}]}
```

- [ ] Format all examples as JSONL
- [ ] Use consistent system prompts
- [ ] Keep assistant responses focused
- [ ] Validate JSON syntax

### 2.3 Data Validation

- [ ] Check for duplicate examples
- [ ] Verify no PII or sensitive data
- [ ] Ensure responses match your quality bar
- [ ] Check token counts per example (<4K recommended)
- [ ] Split into training (90%) and validation (10%) sets

### 2.4 Quality Checks

| Check | Status |
|-------|--------|
| Minimum 50 examples | [ ] |
| Consistent format across examples | [ ] |
| No contradictory examples | [ ] |
| Balanced category distribution | [ ] |
| Examples cover edge cases | [ ] |
| System prompts are consistent | [ ] |

## Phase 3: Fine-Tuning

### 3.1 File Upload

- [ ] Upload training file with `purpose="fine-tune"`
- [ ] Upload validation file with `purpose="fine-tune"`
- [ ] Verify file IDs received
- [ ] Check file processing status

### 3.2 Job Configuration

| Hyperparameter | Default | Guidance |
|----------------|---------|----------|
| n_epochs | auto | 3 for small datasets, 1-2 for large |
| batch_size | auto | Larger = faster, may reduce quality |
| learning_rate_multiplier | auto | Lower if overfitting |
| beta (DPO only) | 0.1 | 0.1-0.5, lower = more drift |

- [ ] Choose hyperparameters or use "auto"
- [ ] Set model suffix for identification
- [ ] Enable data sharing for inference discount (optional)

### 3.3 Start Training

- [ ] Create fine-tuning job
- [ ] Record job ID for monitoring
- [ ] Set up monitoring (poll every 60s)

### 3.4 Monitor Progress

| Metric | What to Look For |
|--------|------------------|
| Training loss | Decreasing over time |
| Validation loss | Decreasing, not increasing |
| Loss gap | Small gap = good generalization |

- [ ] Monitor training loss curve
- [ ] Watch for overfitting (val loss increasing)
- [ ] Check job events for errors

## Phase 4: Evaluation

### 4.1 Test Set Preparation

- [ ] Hold out test examples (not in training/validation)
- [ ] Include diverse test cases
- [ ] Prepare ground truth for comparison

### 4.2 Model Comparison

| Test | Base Model | Fine-tuned | Improvement |
|------|------------|------------|-------------|
| Accuracy | ___% | ___% | ___% |
| Format compliance | ___% | ___% | ___% |
| Latency (avg ms) | ___ | ___ | ___ |
| Cost per 1K calls | $___ | $___ | $___ |

- [ ] Run test set through base model
- [ ] Run test set through fine-tuned model
- [ ] Compare outputs (manual or automated)
- [ ] Calculate improvement metrics

### 4.3 Evaluation Methods

**Automated:**
- [ ] Use model-graded evals (GPT-4 as judge)
- [ ] Calculate ROUGE/BLEU for generation
- [ ] Measure exact match for classification

**Manual:**
- [ ] Human review of sample outputs
- [ ] A/B comparison: base vs fine-tuned
- [ ] Rate outputs on quality scale

### 4.4 Quality Gates

| Gate | Threshold | Status |
|------|-----------|--------|
| Test accuracy | >baseline | [ ] |
| Format compliance | >95% | [ ] |
| Human preference | >60% prefer | [ ] |
| No regressions | verified | [ ] |

## Phase 5: Deployment

### 5.1 Pre-Production

- [ ] Test with production-like traffic
- [ ] Verify error handling
- [ ] Confirm rate limits sufficient
- [ ] Set up monitoring/logging

### 5.2 Production Rollout

- [ ] Deploy to staging environment
- [ ] Run smoke tests
- [ ] Gradual rollout (10% -> 50% -> 100%)
- [ ] Monitor error rates and latency

### 5.3 Post-Launch

- [ ] Monitor inference costs
- [ ] Track quality metrics over time
- [ ] Collect user feedback
- [ ] Plan retraining if quality degrades

## Phase 6: Iteration

### 6.1 Continuous Improvement

- [ ] Analyze failures and edge cases
- [ ] Add new training examples for gaps
- [ ] Consider DPO for preference alignment
- [ ] Schedule periodic retraining

### 6.2 Model Lifecycle

| Version | Date | Changes | Metrics |
|---------|------|---------|---------|
| v1 | ___ | Initial training | ___ |
| v2 | ___ | Added edge cases | ___ |
| v3 | ___ | DPO alignment | ___ |

## Common Issues

| Issue | Solution |
|-------|----------|
| Training loss not decreasing | Check data quality, increase epochs |
| Validation loss increasing | Reduce epochs, add more data |
| Model refuses expected queries | Check for over-represented refusals in data |
| Inconsistent output format | Add more format examples, use consistent system prompt |
| Cost too high | Try smaller model, reduce prompt length |
| Poor generalization | Add more diverse examples |

## Checklist Summary

| Phase | Status |
|-------|--------|
| 1. Planning | [ ] |
| 2. Data Preparation | [ ] |
| 3. Fine-Tuning | [ ] |
| 4. Evaluation | [ ] |
| 5. Deployment | [ ] |
| 6. Iteration | [ ] |
