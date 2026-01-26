# LLM Prompts for Fine-tuning Assistance

Prompts for LLMs to help with LoRA fine-tuning tasks.

## 1. Configuration Advisor

### Prompt: Recommend LoRA Configuration

```markdown
You are an ML engineer expert in parameter-efficient fine-tuning. Help me configure LoRA for my fine-tuning task.

## My Setup

**Hardware:**
- GPU: [GPU model and VRAM, e.g., "RTX 4090 24GB"]
- RAM: [System RAM]

**Model:**
- Base model: [model name, e.g., "Llama-3.1-8B-Instruct"]
- Model size: [parameters]

**Task:**
- Type: [instruction following / code generation / chat / domain adaptation / other]
- Description: [brief task description]
- Dataset size: [number of examples]
- Example length: [average tokens per example]

**Goals:**
- Priority: [quality / speed / memory efficiency]
- Special requirements: [any constraints]

## Please Recommend

1. **Method**: LoRA, QLoRA, DoRA, or rsLoRA
2. **Hyperparameters**:
   - rank (r)
   - alpha
   - dropout
   - target_modules
   - learning_rate
3. **Training settings**:
   - batch_size
   - gradient_accumulation_steps
   - num_epochs
4. **Expected VRAM usage**
5. **Rationale** for each choice
```

### Example Response Format

```markdown
## Recommended Configuration

### Method: QLoRA

**Why**: Your RTX 4090 has 24GB VRAM. QLoRA with 4-bit quantization will fit the 8B model comfortably while allowing batch size > 1.

### Hyperparameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| rank | 16 | Standard for instruction-following tasks |
| alpha | 32 | 2x rank for good scaling |
| dropout | 0.05 | Low dropout for 5K examples |
| target_modules | All linear | Better for domain adaptation |
| learning_rate | 2e-4 | Standard for LoRA |

### Training Settings

| Setting | Value | Rationale |
|---------|-------|-----------|
| batch_size | 4 | Fits in 24GB with QLoRA |
| grad_accum | 4 | Effective batch = 16 |
| epochs | 3 | Standard for instruction tuning |

### Expected VRAM: ~16GB

### Code

```python
from peft import LoraConfig
from transformers import BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
)

lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.05,
    task_type="CAUSAL_LM",
)
```
```

## 2. Data Format Converter

### Prompt: Convert Dataset Format

```markdown
You are a data engineering expert. Convert my dataset to the format required for LoRA fine-tuning.

## Source Format

```json
[sample of my data - paste 2-3 examples]
```

## Target Format

I need: [Alpaca format / ChatML / Llama 3 chat / custom]

## Requirements

- Template: [paste expected template or describe]
- Special handling: [any special cases]
- Output: Python code to convert the dataset

Please provide:
1. Analysis of my source format
2. Conversion code
3. Validation checks
4. 2-3 example outputs
```

## 3. Troubleshooting Assistant

### Prompt: Debug Training Issues

```markdown
You are an ML debugging expert. Help me fix my LoRA fine-tuning issue.

## Issue

**Symptom**: [describe what's happening, e.g., "Loss not decreasing", "OOM error", "NaN loss"]

**When it occurs**: [at start / after N steps / randomly]

## My Configuration

```python
[paste your LoraConfig and TrainingArguments]
```

## Training Log

```
[paste relevant training output/errors]
```

## Hardware

- GPU: [model and VRAM]
- CUDA version: [version]
- PyTorch version: [version]

Please:
1. Identify the likely cause
2. Explain why this happens
3. Provide specific fixes
4. Suggest preventive measures
```

### Common Issues Reference

```markdown
## Quick Troubleshooting Reference

### OOM (Out of Memory)

Causes:
- Batch size too large
- Sequence length too long
- Not using gradient checkpointing

Fixes:
1. Reduce batch_size
2. Increase gradient_accumulation_steps
3. Add gradient_checkpointing=True
4. Use QLoRA instead of LoRA
5. Reduce max_length

### Loss Not Decreasing

Causes:
- Learning rate too low/high
- Wrong target modules
- Data formatting issues

Fixes:
1. Try learning rates: 5e-5, 1e-4, 2e-4, 5e-4
2. Add MLP layers to target_modules
3. Verify data format consistency

### NaN/Inf Loss

Causes:
- Learning rate too high
- Numerical instability
- Corrupted data

Fixes:
1. Reduce learning_rate by 10x
2. Add max_grad_norm=0.3
3. Use bf16 instead of fp16
4. Check data for invalid values

### Poor Quality Output

Causes:
- Rank too low
- Not enough training data
- Wrong data format

Fixes:
1. Increase rank (8 → 16 → 32)
2. Add more training examples
3. Improve data quality
4. Add MLP layers to target_modules
```

## 4. Evaluation Design

### Prompt: Design Evaluation Strategy

```markdown
You are an ML evaluation expert. Help me design an evaluation strategy for my fine-tuned model.

## Task

**Type**: [classification / generation / QA / code / chat]
**Description**: [what the model should do]

## Success Criteria

**Must have**:
- [criterion 1]
- [criterion 2]

**Nice to have**:
- [criterion 3]

## Available Resources

- Test set size: [N examples]
- Human evaluation: [yes/no, budget]
- Baseline: [existing model to compare against]

Please recommend:
1. Quantitative metrics with implementation
2. Qualitative evaluation criteria
3. Test set design
4. A/B testing approach (if applicable)
5. Red-teaming considerations
```

## 5. Hyperparameter Tuning

### Prompt: Design Hyperparameter Search

```markdown
You are a hyperparameter tuning expert. Help me find optimal LoRA hyperparameters.

## Constraints

- Compute budget: [N GPU hours / N experiments]
- Hardware: [GPU specs]
- Time limit: [if any]

## Task Characteristics

- Dataset size: [N examples]
- Complexity: [simple style change / moderate / complex reasoning]
- Base model: [model name]

## Current Best

```python
[current config if any]
```

**Current performance**: [metrics]

Please provide:
1. Search space (rank, alpha, LR, target_modules)
2. Search strategy (grid / random / Bayesian)
3. Number of experiments needed
4. Early stopping criteria
5. Python code for the search
```

## 6. Production Deployment

### Prompt: Plan Deployment Strategy

```markdown
You are an MLOps expert. Help me deploy my LoRA fine-tuned model to production.

## Model Details

- Base model: [name and size]
- Adapter size: [MB]
- Quantization: [4-bit / 8-bit / none]

## Requirements

- Latency: [max acceptable latency]
- Throughput: [requests per second]
- Cost budget: [if any]
- Multi-adapter: [need to switch adapters?]

## Infrastructure

- Cloud: [AWS / GCP / Azure / on-prem]
- Existing stack: [K8s / Docker / serverless]
- GPU available: [type and count]

Please recommend:
1. Serving framework (vLLM / TGI / Triton / custom)
2. Infrastructure setup
3. Merge vs adapter-serving decision
4. Scaling strategy
5. Monitoring approach
6. Cost estimation
```

## 7. Quick Reference Prompts

### Get Target Modules for Any Model

```markdown
What are the correct target_modules for LoRA with [MODEL_NAME]?

List all linear layers that can be adapted, grouped by:
1. Attention layers (required)
2. MLP/FFN layers (optional, for complex tasks)

Provide the exact Python list to use with PEFT.
```

### Compare LoRA Variants

```markdown
Compare LoRA, QLoRA, DoRA, and rsLoRA for my use case:

- Model: [size]
- GPU: [VRAM]
- Task: [description]
- Priority: [quality / speed / memory]

Table format with: Method | Memory | Quality | Training Speed | Best For
```

### Generate Training Data

```markdown
I'm fine-tuning a model for [TASK]. Generate 10 diverse training examples in this format:

```json
{
    "instruction": "...",
    "input": "...",
    "output": "..."
}
```

Requirements:
- Vary complexity (easy/medium/hard)
- Include edge cases
- Realistic inputs
- High-quality outputs
```

### Estimate Training Resources

```markdown
Estimate resources for fine-tuning:

Model: [name, size]
Method: [LoRA/QLoRA]
Dataset: [N examples, avg tokens]
Epochs: [N]

Provide:
1. VRAM required
2. Training time (rough estimate per epoch)
3. Recommended GPU
4. Cost estimate (cloud pricing)
```
