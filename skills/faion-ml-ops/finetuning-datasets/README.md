---
name: faion-finetuning-datasets
user-invocable: false
description: ""
---

# LLM Fine-tuning: Datasets, Training & Deployment

**Dataset preparation, training configuration, evaluation, and deployment (2025-2026)**

---

## Quick Reference

| Area | Key Elements |
|------|--------------|
| **Datasets** | Alpaca, ShareGPT, Conversation, Instruction |
| **Evaluation** | Perplexity, task benchmarks, human eval |
| **Deployment** | GGUF, vLLM, TGI, Ollama |
| **Cost** | GPU selection, cloud pricing, optimization |

---

## Dataset Formats

### Format Comparison

| Format | Structure | Use Case |
|--------|-----------|----------|
| **Alpaca** | instruction, input, output | Single-turn tasks |
| **ShareGPT** | conversations array | Multi-turn chat |
| **OpenAI** | messages array | API fine-tuning |
| **Completion** | prompt, completion | Text completion |

### Alpaca Format

```json
[
  {
    "instruction": "Summarize the following text",
    "input": "Long text here...",
    "output": "Summary here..."
  }
]
```

### ShareGPT Format

```json
[
  {
    "conversations": [
      {"from": "human", "value": "What is AI?"},
      {"from": "gpt", "value": "AI stands for..."}
    ]
  }
]
```

---

## Data Preparation

### Data Cleaning Pipeline

```python
import json
from datasets import load_dataset

def clean_dataset(raw_data):
    cleaned = []
    seen = set()

    for item in raw_data:
        # Remove duplicates
        key = (item.get("instruction", ""), item.get("output", ""))
        if key in seen:
            continue
        seen.add(key)

        # Filter empty
        if not item.get("output", "").strip():
            continue

        # Filter too short
        if len(item.get("output", "")) < 10:
            continue

        # Filter too long (adjust as needed)
        if len(item.get("output", "")) > 4096:
            continue

        cleaned.append(item)

    return cleaned

# Load and clean
with open("raw_data.json") as f:
    raw = json.load(f)

cleaned = clean_dataset(raw)
print(f"Cleaned: {len(raw)} -> {len(cleaned)}")

# Save
with open("cleaned_data.json", "w") as f:
    json.dump(cleaned, f, indent=2)
```

### Prompt Formatting

```python
def format_alpaca(example):
    """Format for instruction-following."""
    if example.get("input"):
        return f"""### Instruction:
{example['instruction']}

### Input:
{example['input']}

### Response:
{example['output']}"""
    else:
        return f"""### Instruction:
{example['instruction']}

### Response:
{example['output']}"""

def format_chat(example):
    """Format for chat models."""
    messages = []
    for msg in example["conversations"]:
        role = "user" if msg["from"] == "human" else "assistant"
        messages.append({"role": role, "content": msg["value"]})
    return messages
```

### Quality Guidelines

| Criterion | Description |
|-----------|-------------|
| **Accuracy** | Factually correct responses |
| **Consistency** | Same format across examples |
| **Diversity** | Varied instructions and domains |
| **Length** | Appropriate response length |
| **No Toxicity** | Filter harmful content |
| **No PII** | Remove personal information |

---

## Training Configuration

### Hyperparameters

| Parameter | Description | Typical Range |
|-----------|-------------|---------------|
| **learning_rate** | Step size | 1e-5 to 5e-4 |
| **batch_size** | Samples per step | 1-8 (per GPU) |
| **epochs** | Full passes | 1-5 |
| **warmup_ratio** | LR warmup | 0.03-0.1 |
| **weight_decay** | Regularization | 0.01-0.1 |
| **max_seq_length** | Token limit | 512-8192 |

### Learning Rate Schedules

| Schedule | Description | Use Case |
|----------|-------------|----------|
| **constant** | Fixed LR | Short training |
| **linear** | Linear decay | General |
| **cosine** | Cosine decay | Best for most cases |
| **cosine_with_restarts** | Multiple cycles | Long training |

### Gradient Accumulation

```python
# Effective batch size = batch_size * gradient_accumulation_steps * num_gpus
# Example: 2 * 4 * 1 = 8 effective batch size
training_args = TrainingArguments(
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
)
```

---

## Evaluation Metrics

### Perplexity

Lower is better. Measures model uncertainty.

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

def calculate_perplexity(model, tokenizer, text, device="cuda"):
    encodings = tokenizer(text, return_tensors="pt").to(device)

    with torch.no_grad():
        outputs = model(**encodings, labels=encodings.input_ids)

    return torch.exp(outputs.loss).item()

# Usage
ppl = calculate_perplexity(model, tokenizer, "Sample text here")
print(f"Perplexity: {ppl:.2f}")
```

### Task-Specific Benchmarks

| Benchmark | Tasks | Metrics |
|-----------|-------|---------|
| **MMLU** | Multi-task knowledge | Accuracy |
| **HellaSwag** | Commonsense reasoning | Accuracy |
| **TruthfulQA** | Factual accuracy | MC1, MC2 |
| **HumanEval** | Code generation | Pass@1, Pass@10 |
| **GSM8K** | Math reasoning | Accuracy |
| **BBH** | Hard tasks | Accuracy |

### Using LM Evaluation Harness

```bash
pip install lm-eval

# Evaluate on multiple benchmarks
lm_eval --model hf \
    --model_args pretrained=./my_model \
    --tasks mmlu,hellaswag,truthfulqa \
    --device cuda:0 \
    --batch_size 8
```

### Human Evaluation

| Aspect | Rating Scale |
|--------|--------------|
| **Fluency** | 1-5 (grammatically correct) |
| **Relevance** | 1-5 (answers the question) |
| **Accuracy** | 1-5 (factually correct) |
| **Helpfulness** | 1-5 (useful response) |

---

## Deployment

### GGUF for llama.cpp / Ollama

```python
# Using Unsloth
model.save_pretrained_gguf("model", tokenizer, quantization_method="q4_k_m")

# Quantization options
# q4_k_m - Good balance (recommended)
# q5_k_m - Better quality
# q8_0 - Highest quality
# q2_k - Smallest size
```

### Create Ollama Model

```dockerfile
# Modelfile
FROM ./model-q4_k_m.gguf

TEMPLATE """{{ if .System }}<|start_header_id|>system<|end_header_id|>

{{ .System }}<|eot_id|>{{ end }}{{ if .Prompt }}<|start_header_id|>user<|end_header_id|>

{{ .Prompt }}<|eot_id|>{{ end }}<|start_header_id|>assistant<|end_header_id|>

{{ .Response }}<|eot_id|>"""

PARAMETER stop "<|start_header_id|>"
PARAMETER stop "<|end_header_id|>"
PARAMETER stop "<|eot_id|>"
```

```bash
ollama create my-model -f Modelfile
ollama run my-model
```

### vLLM Deployment

```bash
pip install vllm

# Start server
python -m vllm.entrypoints.openai.api_server \
    --model ./merged_model \
    --port 8000 \
    --tensor-parallel-size 1

# API call
curl http://localhost:8000/v1/completions \
    -H "Content-Type: application/json" \
    -d '{"model": "merged_model", "prompt": "Hello", "max_tokens": 50}'
```

### Text Generation Inference (TGI)

```bash
docker run --gpus all -p 8080:80 \
    -v $PWD/model:/data \
    ghcr.io/huggingface/text-generation-inference:latest \
    --model-id /data \
    --max-input-length 4096 \
    --max-total-tokens 8192
```

---

## Cost Optimization

### GPU Selection

| GPU | VRAM | Models | Cloud Cost |
|-----|------|--------|------------|
| **RTX 3090** | 24GB | 7B full, 13B QLoRA | $0.50/hr |
| **RTX 4090** | 24GB | 7B full, 13B QLoRA | $0.75/hr |
| **A10G** | 24GB | 7B full, 13B QLoRA | $1.00/hr |
| **A100 40GB** | 40GB | 13B full, 70B QLoRA | $3.50/hr |
| **A100 80GB** | 80GB | 70B full | $4.50/hr |
| **H100** | 80GB | 70B full (fastest) | $8.00/hr |

### Cost Reduction Strategies

| Strategy | Savings | Trade-off |
|----------|---------|-----------|
| **QLoRA instead of LoRA** | 50-70% VRAM | Slightly slower |
| **Gradient checkpointing** | 30% VRAM | 20% slower |
| **Mixed precision (bf16)** | 50% VRAM | None |
| **Smaller batch + grad accum** | Variable | Same effective batch |
| **Shorter sequences** | Linear | Less context |
| **Fewer epochs** | Linear | Less convergence |

### Cloud Providers

| Provider | GPU Options | Pricing Model |
|----------|-------------|---------------|
| **RunPod** | A100, H100, 4090 | Per hour |
| **Lambda Labs** | A100, H100 | Per hour |
| **Vast.ai** | Various | Auction-based |
| **Google Colab Pro+** | A100, V100 | Monthly ($50) |
| **AWS SageMaker** | p4d, p5 | Per hour |

### Training Time Estimation

```python
def estimate_training_time(
    dataset_size: int,
    batch_size: int,
    gradient_accumulation: int,
    epochs: int,
    tokens_per_second: int = 1000,
    avg_seq_length: int = 512
):
    """Estimate training time in hours."""
    steps = (dataset_size // (batch_size * gradient_accumulation)) * epochs
    total_tokens = steps * batch_size * gradient_accumulation * avg_seq_length
    hours = total_tokens / tokens_per_second / 3600
    return hours

# Example
hours = estimate_training_time(
    dataset_size=10000,
    batch_size=2,
    gradient_accumulation=4,
    epochs=3,
    tokens_per_second=2000,  # A100
)
print(f"Estimated: {hours:.1f} hours")
```

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **OOM (Out of Memory)** | Reduce batch size, use QLoRA, gradient checkpointing |
| **Loss not decreasing** | Lower LR, check data quality, increase rank |
| **Overfitting** | Add dropout, reduce epochs, more data |
| **Catastrophic forgetting** | Lower LR, use regularization |
| **Slow training** | Use Flash Attention, optimize data loading |
| **NaN loss** | Lower LR, check for bad data, use bf16 |

### Debugging Tips

```python
# Check GPU memory
import torch
print(f"Allocated: {torch.cuda.memory_allocated() / 1e9:.2f} GB")
print(f"Reserved: {torch.cuda.memory_reserved() / 1e9:.2f} GB")

# Monitor training
from transformers import TrainerCallback

class LogCallback(TrainerCallback):
    def on_log(self, args, state, control, logs=None, **kwargs):
        if logs:
            print(f"Step {state.global_step}: loss={logs.get('loss', 'N/A'):.4f}")
```

---

## Quick Start Checklist

1. [ ] **Choose technique** - LoRA for most cases, QLoRA for limited GPU
2. [ ] **Prepare dataset** - Clean, format, deduplicate (min 100 examples)
3. [ ] **Select base model** - Llama 3.1, Mistral, Qwen 2.5
4. [ ] **Configure training** - LR 2e-4, rank 16, epochs 3
5. [ ] **Monitor metrics** - Loss, perplexity, validation loss
6. [ ] **Evaluate** - Perplexity, task benchmarks, human eval
7. [ ] **Merge/Export** - GGUF for local, vLLM for serving
8. [ ] **Deploy** - Ollama, vLLM, TGI

---

## Tools

| Tool | Purpose |
|------|---------|
| [Hugging Face Hub](https://huggingface.co) | Model hosting, datasets |
| [Weights & Biases](https://wandb.ai) | Experiment tracking |
| [LM Evaluation Harness](https://github.com/EleutherAI/lm-evaluation-harness) | Benchmarking |
| [mergekit](https://github.com/arcee-ai/mergekit) | Model merging |
| [Ollama](https://ollama.ai) | Local deployment |
| [vLLM](https://github.com/vllm-project/vllm) | Production serving |

---

*Last updated: 2026-01-23*
*Part 2 of 2: Datasets, Training & Deployment*

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Dataset format preparation | haiku | Data transformation |
| Quality assessment | sonnet | Data validation |
| Preprocessing strategy | sonnet | Approach selection |
