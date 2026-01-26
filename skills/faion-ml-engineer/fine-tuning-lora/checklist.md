# Fine-tuning Checklist

Pre-flight checklist for LoRA/QLoRA/DoRA fine-tuning projects.

## 1. Data Preparation

### Dataset Quality

- [ ] **Format consistency**: All examples follow identical template
- [ ] **Quality review**: Manually reviewed 50-100 random samples
- [ ] **No duplicates**: Deduplicated dataset
- [ ] **Balanced distribution**: Task types evenly represented
- [ ] **Length analysis**: Checked input/output token distributions
- [ ] **Edge cases**: Included examples for edge cases

### Dataset Size Guidelines

| Task Type | Minimum | Recommended | Maximum Useful |
|-----------|---------|-------------|----------------|
| Style transfer | 100 | 500-1K | 5K |
| Instruction following | 500 | 5K-10K | 50K |
| Domain knowledge | 1K | 10K-50K | 100K+ |
| Code generation | 2K | 20K-50K | 500K+ |

### Data Formatting

- [ ] **Consistent template** applied to all examples
- [ ] **Special tokens** correctly placed (BOS, EOS, pad)
- [ ] **Tokenizer alignment**: Verified tokenizer handles format
- [ ] **Train/val split**: 90/10 or 95/5 for small datasets
- [ ] **Shuffled**: Data is randomly shuffled

## 2. Hardware Assessment

### VRAM Requirements

| Model | Full FP16 | LoRA FP16 | QLoRA 4-bit |
|-------|-----------|-----------|-------------|
| 7B | 28GB | 20GB | 6-8GB |
| 13B | 52GB | 35GB | 10-12GB |
| 70B | 280GB | 180GB | 40-48GB |

### Pre-training Checks

- [ ] **VRAM available**: Sufficient for chosen method
- [ ] **Storage**: Checkpoints need ~1-5GB per save
- [ ] **CUDA version**: >= 11.8 for bitsandbytes
- [ ] **PyTorch**: >= 2.0 recommended
- [ ] **Flash Attention**: Installed for efficiency (optional)

```bash
# Check VRAM
nvidia-smi --query-gpu=memory.total,memory.free --format=csv

# Check CUDA
nvcc --version

# Check PyTorch
python -c "import torch; print(torch.version.cuda)"
```

## 3. Configuration Selection

### Method Selection

| Scenario | Recommended |
|----------|-------------|
| Consumer GPU (24GB) | QLoRA |
| A100/H100 (80GB) | LoRA or DoRA |
| Maximum quality | DoRA |
| High rank needed | rsLoRA |
| Best memory+quality | QDoRA |

### Hyperparameter Defaults

| Parameter | Conservative | Standard | Aggressive |
|-----------|-------------|----------|------------|
| rank (r) | 8 | 16-32 | 64-128 |
| alpha | 16 | 32-64 | 128+ |
| dropout | 0.05 | 0.1 | 0.15 |
| learning_rate | 1e-4 | 2e-4 | 5e-4 |
| batch_size | 2 | 4 | 8+ |
| grad_accum | 8 | 4 | 2 |

### Target Modules Selection

- [ ] **Simple task** (style, format): `["q_proj", "v_proj"]`
- [ ] **Standard task**: `["q_proj", "k_proj", "v_proj", "o_proj"]`
- [ ] **Complex task** (knowledge, reasoning): All attention + MLP layers

```python
# Full target for LLaMA-style models
target_modules = [
    "q_proj", "k_proj", "v_proj", "o_proj",  # Attention
    "gate_proj", "up_proj", "down_proj"       # MLP
]
```

## 4. Training Setup

### Environment

- [ ] **Dependencies installed**:
  ```bash
  pip install transformers peft trl bitsandbytes accelerate datasets
  ```
- [ ] **Hugging Face login** (for gated models):
  ```bash
  huggingface-cli login
  ```
- [ ] **Weights & Biases** (optional tracking):
  ```bash
  wandb login
  ```

### Code Checks

- [ ] **Pad token set**: `tokenizer.pad_token = tokenizer.eos_token`
- [ ] **Gradient checkpointing**: Enabled for memory savings
- [ ] **Mixed precision**: FP16 or BF16 enabled
- [ ] **Device map**: Set to "auto" for multi-GPU

### Training Arguments

- [ ] **Warmup ratio**: 0.03-0.05 of total steps
- [ ] **Scheduler**: Cosine decay recommended
- [ ] **Optimizer**: `paged_adamw_8bit` for QLoRA
- [ ] **Save strategy**: Every epoch or N steps
- [ ] **Evaluation**: Every epoch if validation set exists

## 5. During Training

### Monitoring

- [ ] **Loss tracking**: Initial loss reasonable (2-4 for causal LM)
- [ ] **Loss decreasing**: Steady decrease first epoch
- [ ] **No NaN/Inf**: Check for numerical instability
- [ ] **Memory usage**: Stable, no OOM errors
- [ ] **GPU utilization**: >80% indicates good efficiency

### Common Issues

| Issue | Symptom | Fix |
|-------|---------|-----|
| Learning rate too high | Loss spikes, NaN | Reduce LR by 2-10x |
| Learning rate too low | Loss plateaus early | Increase LR by 2-5x |
| Rank too low | Underfitting | Increase rank |
| No warmup | Early instability | Add 3-5% warmup |
| Wrong target modules | Poor adaptation | Add MLP layers |

## 6. Post-training Validation

### Quality Checks

- [ ] **Inference works**: Model generates coherent output
- [ ] **Task performance**: Tested on held-out examples
- [ ] **No regression**: General capabilities preserved
- [ ] **Formatting correct**: Output matches expected format
- [ ] **Edge cases**: Handles unusual inputs gracefully

### Evaluation Metrics

| Task Type | Metrics |
|-----------|---------|
| Classification | Accuracy, F1, Precision, Recall |
| Generation | BLEU, ROUGE, Perplexity |
| QA | Exact Match, F1 |
| Code | Pass@k, Execution accuracy |
| Reasoning | Chain-of-thought accuracy |

### Adapter Management

- [ ] **Adapter saved**: `model.save_pretrained("./adapter")`
- [ ] **Tokenizer saved**: `tokenizer.save_pretrained("./adapter")`
- [ ] **Config documented**: Hyperparameters recorded
- [ ] **Version tagged**: Git tag or version number

## 7. Deployment

### Merge Decision

| Scenario | Action |
|----------|--------|
| Single adapter | Merge into base model |
| Multiple adapters | Keep separate, switch at runtime |
| Frequent updates | Keep separate for easy updates |
| Minimum latency | Merge (no adapter overhead) |

### Serving Options

- [ ] **Merged model**: `model.merge_and_unload()` + save
- [ ] **Adapter serving**: Load base + adapter separately
- [ ] **vLLM compatible**: Test inference server
- [ ] **GGUF export**: For llama.cpp deployment

```python
# Merge and save
merged = model.merge_and_unload()
merged.save_pretrained("./merged-model")
tokenizer.save_pretrained("./merged-model")

# Or keep adapter for switching
model.save_pretrained("./my-adapter")
```

## Quick Reference Card

### Minimum Viable Config (7B model, 16GB VRAM)

```python
# QLoRA config
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
)

lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_dropout=0.05,
    task_type="CAUSAL_LM",
)

training_args = TrainingArguments(
    per_device_train_batch_size=2,
    gradient_accumulation_steps=8,
    learning_rate=2e-4,
    num_train_epochs=3,
    fp16=True,
    warmup_ratio=0.03,
    lr_scheduler_type="cosine",
    optim="paged_adamw_8bit",
)
```

### Must-Have Checklist (Minimum)

- [ ] Consistent data format
- [ ] Correct pad token
- [ ] Appropriate rank for task complexity
- [ ] Learning rate in 1e-4 to 5e-4 range
- [ ] Warmup enabled
- [ ] Tested inference before deployment
