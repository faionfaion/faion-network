# Fine-tuning Checklist

Step-by-step checklist for LLM fine-tuning projects.

---

## Phase 1: Planning

### 1.1 Problem Definition

- [ ] Define the specific task or capability needed
- [ ] Document expected input/output formats
- [ ] Establish success criteria and metrics
- [ ] Confirm fine-tuning is the right approach (not RAG/prompting)

### 1.2 Resource Assessment

- [ ] Inventory available GPU resources
- [ ] Estimate training data volume
- [ ] Calculate approximate compute costs
- [ ] Plan evaluation infrastructure

### 1.3 Technique Selection

| GPU Memory | Recommended Technique |
|------------|----------------------|
| < 8GB | QLoRA (small models only) |
| 8-16GB | QLoRA |
| 16-24GB | LoRA or QLoRA |
| 24-48GB | LoRA or DoRA |
| 48GB+ | Full fine-tuning possible |

---

## Phase 2: Data Preparation

### 2.1 Data Collection

- [ ] Identify data sources
- [ ] Collect minimum 50-100 examples (100-1000 recommended)
- [ ] Ensure data diversity covers edge cases
- [ ] Verify data licensing/ownership

### 2.2 Data Quality

- [ ] Remove duplicates
- [ ] Fix formatting issues
- [ ] Correct factual errors
- [ ] Remove PII/sensitive information
- [ ] Ensure consistent formatting across examples

### 2.3 Data Formatting

**Instruction Format (SFT):**
```json
{
  "instruction": "Task description",
  "input": "User input",
  "output": "Expected response"
}
```

**Chat Format (OpenAI/Claude):**
```json
{
  "messages": [
    {"role": "system", "content": "System prompt"},
    {"role": "user", "content": "User message"},
    {"role": "assistant", "content": "Assistant response"}
  ]
}
```

**Preference Format (DPO/ORPO):**
```json
{
  "prompt": "User message",
  "chosen": "Preferred response",
  "rejected": "Worse response"
}
```

### 2.4 Data Splitting

- [ ] Training set: 80-90%
- [ ] Validation set: 10-20%
- [ ] Hold-out test set: Optional but recommended
- [ ] Ensure no data leakage between sets

---

## Phase 3: Model Selection

### 3.1 Base Model Choice

| Model Size | Use Case | Example Models |
|------------|----------|----------------|
| 1-3B | Edge, mobile, fast inference | Llama-3.2-1B, Phi-3-mini |
| 7-8B | General purpose, balanced | Llama-3.1-8B, Mistral-7B |
| 13-14B | Higher quality, more compute | Llama-2-13B |
| 70B+ | Maximum capability | Llama-3.1-70B |

### 3.2 Model Considerations

- [ ] License compatibility with use case
- [ ] Context length requirements
- [ ] Multimodal needs (if any)
- [ ] Existing fine-tunes to start from

---

## Phase 4: Training Configuration

### 4.1 LoRA Parameters

| Parameter | Conservative | Balanced | Aggressive |
|-----------|--------------|----------|------------|
| rank (r) | 8 | 16-32 | 64-128 |
| alpha | 8 | 16-32 | 64-128 |
| dropout | 0.1 | 0.05 | 0.0 |
| target_modules | q,v | q,k,v,o | all linear |

### 4.2 Training Hyperparameters

| Parameter | Range | Notes |
|-----------|-------|-------|
| Learning rate | 1e-5 to 5e-4 | Start low, increase if needed |
| Batch size | 2-8 | Limit by GPU memory |
| Epochs | 1-5 | Watch for overfitting |
| Warmup ratio | 0.03-0.1 | Stabilizes early training |
| Weight decay | 0.01-0.1 | Regularization |

### 4.3 Pre-training Checklist

- [ ] Hyperparameters configured
- [ ] Logging enabled (WandB/TensorBoard)
- [ ] Checkpointing configured
- [ ] Validation evaluation set up
- [ ] Early stopping configured (if desired)

---

## Phase 5: Training Execution

### 5.1 Training Monitoring

- [ ] Training loss decreasing
- [ ] Validation loss tracking (watch for divergence)
- [ ] Learning rate schedule working
- [ ] GPU utilization reasonable
- [ ] No OOM errors

### 5.2 Warning Signs

| Issue | Symptom | Action |
|-------|---------|--------|
| **Overfitting** | Val loss increases while train loss drops | Reduce epochs, increase dropout |
| **Underfitting** | Both losses plateau high | Increase rank, learning rate |
| **Instability** | Loss spikes or NaN | Reduce learning rate |
| **Catastrophic forgetting** | General capabilities lost | Reduce learning rate, freeze layers |

### 5.3 Preventing Catastrophic Forgetting

- [ ] Use conservative learning rate (1e-5 to 5e-5)
- [ ] Consider freezing lower layers
- [ ] Apply regularization (EWC if needed)
- [ ] Mix in general instruction data

---

## Phase 6: Evaluation

### 6.1 Quantitative Metrics

- [ ] Validation loss
- [ ] Task-specific metrics (accuracy, F1, BLEU, etc.)
- [ ] Perplexity on held-out data
- [ ] Comparison to baseline

### 6.2 Qualitative Evaluation

- [ ] Manual review of 20-50 outputs
- [ ] Edge case testing
- [ ] Instruction following quality
- [ ] Output format consistency

### 6.3 Safety Evaluation

- [ ] Test for harmful outputs
- [ ] Check for bias amplification
- [ ] Verify no PII leakage from training data
- [ ] Adversarial testing (red teaming)

---

## Phase 7: Deployment

### 7.1 Model Export

| Format | Use Case | Tool |
|--------|----------|------|
| Merged weights | Standard deployment | PEFT merge_and_unload |
| LoRA adapter | Low storage, swappable | Save adapter only |
| GGUF | llama.cpp, Ollama | llama.cpp convert |
| ONNX | Cross-platform | Optimum |

### 7.2 Deployment Checklist

- [ ] Model exported in target format
- [ ] Inference tested locally
- [ ] Quantization applied if needed (for production)
- [ ] API endpoint configured
- [ ] Rate limiting set up
- [ ] Monitoring enabled

### 7.3 Post-deployment

- [ ] Monitor output quality
- [ ] Collect feedback for iteration
- [ ] Track inference costs
- [ ] Plan for model updates

---

## Quick Reference: Data Requirements

| Task Type | Minimum Examples | Recommended |
|-----------|------------------|-------------|
| Simple classification | 50 | 200-500 |
| Text generation | 100 | 500-1000 |
| Complex reasoning | 200 | 1000+ |
| Style transfer | 100 | 500+ |
| Domain adaptation | 500 | 2000+ |

---

*Last updated: 2026-01-25*
