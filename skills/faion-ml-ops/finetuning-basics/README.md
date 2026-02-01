---
name: faion-finetuning-basics
user-invocable: false
description: ""
---

# LLM Fine-tuning: Techniques & Frameworks

**Core fine-tuning techniques and frameworks (2025-2026)**

---

## Quick Reference

| Area | Key Elements |
|------|--------------|
| **Techniques** | Full fine-tuning, LoRA, QLoRA, DoRA |
| **Frameworks** | LLaMA-Factory, Unsloth, Axolotl, TRL |
| **Alignment** | SFT, RLHF, DPO, ORPO |
| **Deployment** | GGUF, vLLM, TGI, Ollama |

---

## Technique Comparison

| Technique | GPU Memory | Speed | Quality | Use Case |
|-----------|------------|-------|---------|----------|
| **Full FT** | 80GB+ | Slow | Best | Large budgets, critical tasks |
| **LoRA** | 16-24GB | Fast | Good | Most production cases |
| **QLoRA** | 8-12GB | Medium | Good | Consumer GPUs, prototyping |
| **DoRA** | 16-24GB | Fast | Better | LoRA successor (2024+) |
| **OpenAI FT** | N/A | Fast | Good | API-only workflows |

---

## LoRA (Low-Rank Adaptation)

### Core Concept

LoRA freezes base model weights and injects small trainable matrices into attention layers.

```
Original weight W (d x k)
         ↓
W' = W + BA  where B (d x r), A (r x k)
         ↓
Only B and A are trained (r << min(d, k))
```

### Key Parameters

| Parameter | Description | Typical Values |
|-----------|-------------|----------------|
| **rank (r)** | Adapter matrix rank | 8, 16, 32, 64 |
| **alpha** | Scaling factor | Usually = rank |
| **target_modules** | Layers to adapt | q_proj, v_proj, k_proj, o_proj |
| **dropout** | Regularization | 0.0 - 0.1 |

### Rank Selection Guide

| Rank | Memory | Use Case |
|------|--------|----------|
| 8 | Minimal | Simple tasks, prototyping |
| 16 | Low | General fine-tuning |
| 32 | Medium | Complex tasks |
| 64 | Higher | Maximum quality |
| 128+ | High | Rarely needed |

### Target Modules by Model

| Model | Recommended Modules |
|-------|---------------------|
| **LLaMA/Mistral** | q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj |
| **Qwen** | c_attn, c_proj |
| **Phi** | q_proj, k_proj, v_proj, dense |
| **GPT-NeoX** | query_key_value, dense |

---

## QLoRA (Quantized LoRA)

### Memory Savings

QLoRA loads base model in 4-bit precision, trains LoRA adapters in fp16.

| Model Size | Full FT | LoRA (fp16) | QLoRA (4-bit) |
|------------|---------|-------------|---------------|
| 7B | 28GB | 16GB | 6-8GB |
| 13B | 52GB | 28GB | 10-12GB |
| 70B | 280GB | 140GB | 40-48GB |

### Key Components

1. **NF4 Quantization** - 4-bit NormalFloat
2. **Double Quantization** - Quantize quantization constants
3. **Paged Optimizers** - Handle memory spikes
4. **fp16 LoRA** - Full precision adapters

### Configuration

```python
from transformers import BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)
```

---

## OpenAI Fine-tuning API

### Supported Models

| Model | Training Cost | Inference Cost |
|-------|---------------|----------------|
| gpt-4o-mini-2024-07-18 | $3.00/1M tokens | $12.00/1M output |
| gpt-4o-2024-08-06 | $25.00/1M tokens | $100.00/1M output |
| gpt-3.5-turbo-0125 | $0.80/1M tokens | $3.20/1M output |

### Training Data Format

```jsonl
{"messages": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "What is LoRA?"}, {"role": "assistant", "content": "LoRA (Low-Rank Adaptation) is..."}]}
{"messages": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "How to fine-tune?"}, {"role": "assistant", "content": "To fine-tune a model..."}]}
```

### Python API

```python
from openai import OpenAI

client = OpenAI()

# Upload training file
with open("training_data.jsonl", "rb") as f:
    file = client.files.create(file=f, purpose="fine-tune")

# Create fine-tuning job
job = client.fine_tuning.jobs.create(
    training_file=file.id,
    model="gpt-4o-mini-2024-07-18",
    hyperparameters={
        "n_epochs": 3,
        "batch_size": 4,
        "learning_rate_multiplier": 1.8
    },
    suffix="my-custom-model"
)

# Monitor progress
print(f"Job ID: {job.id}")
print(f"Status: {job.status}")

# List events
events = client.fine_tuning.jobs.list_events(job.id)
for event in events.data:
    print(event.message)

# Use fine-tuned model
response = client.chat.completions.create(
    model="ft:gpt-4o-mini-2024-07-18:my-org::abc123",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### Best Practices

1. **Minimum 10 examples** - but 50-100+ recommended
2. **Consistent format** - same system prompt across examples
3. **Quality over quantity** - clean, accurate examples
4. **Validation set** - 10-20% for monitoring
5. **Suffix naming** - descriptive, version-tracked

---

## LLaMA-Factory

### Overview

User-friendly framework with WebUI for training LLMs.

### Installation

```bash
git clone https://github.com/hiyouga/LLaMA-Factory.git
cd LLaMA-Factory
pip install -e ".[torch,metrics]"

# Launch WebUI
python src/webui.py
```

### Supported Models

| Family | Models |
|--------|--------|
| **LLaMA** | Llama-2, Llama-3, Llama-3.1, Llama-3.2 |
| **Mistral** | Mistral-7B, Mixtral-8x7B |
| **Qwen** | Qwen-1.5, Qwen-2, Qwen-2.5 |
| **Yi** | Yi-6B, Yi-34B |
| **Phi** | Phi-2, Phi-3, Phi-3.5 |
| **DeepSeek** | DeepSeek-V2, DeepSeek-V3 |

### CLI Training

```bash
# LoRA fine-tuning
llamafactory-cli train \
    --stage sft \
    --model_name_or_path meta-llama/Llama-3.1-8B \
    --dataset alpaca_en \
    --template llama3 \
    --finetuning_type lora \
    --lora_rank 16 \
    --lora_target q_proj,v_proj \
    --output_dir output/llama3-lora \
    --per_device_train_batch_size 2 \
    --gradient_accumulation_steps 4 \
    --learning_rate 5e-5 \
    --num_train_epochs 3 \
    --fp16

# Merge LoRA adapter
llamafactory-cli export \
    --model_name_or_path meta-llama/Llama-3.1-8B \
    --adapter_name_or_path output/llama3-lora \
    --template llama3 \
    --finetuning_type lora \
    --export_dir merged_model
```

---

## Unsloth

### Overview

2x faster training with 80% less memory using custom CUDA kernels.

### Installation

```bash
pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
pip install --no-deps trl peft accelerate bitsandbytes
```

### Quick Start

```python
from unsloth import FastLanguageModel
from trl import SFTTrainer
from transformers import TrainingArguments

# Load model (4-bit)
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Llama-3.2-1B",
    max_seq_length=2048,
    dtype=None,  # Auto-detect
    load_in_4bit=True,
)

# Add LoRA adapters
model = FastLanguageModel.get_peft_model(
    model,
    r=16,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],
    lora_alpha=16,
    lora_dropout=0,
    bias="none",
    use_gradient_checkpointing="unsloth",  # 30% less VRAM
    random_state=42,
)

# Training arguments
training_args = TrainingArguments(
    output_dir="./outputs",
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    warmup_steps=10,
    max_steps=60,
    learning_rate=2e-4,
    fp16=not torch.cuda.is_bf16_supported(),
    bf16=torch.cuda.is_bf16_supported(),
    logging_steps=1,
    optim="adamw_8bit",
    weight_decay=0.01,
    lr_scheduler_type="linear",
    seed=42,
)

# Train
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    dataset_text_field="text",
    max_seq_length=2048,
    args=training_args,
)

trainer.train()

# Save LoRA
model.save_pretrained("lora_model")
tokenizer.save_pretrained("lora_model")

# Save merged 16-bit
model.save_pretrained_merged("merged_16bit", tokenizer, save_method="merged_16bit")

# Save GGUF for llama.cpp / Ollama
model.save_pretrained_gguf("model_gguf", tokenizer, quantization_method="q4_k_m")
```

### Key Features

| Feature | Benefit |
|---------|---------|
| **RoPE Scaling** | 4x longer context |
| **Gradient Checkpointing** | 30% less VRAM |
| **4-bit Loading** | Train 70B on 48GB |
| **Flash Attention 2** | 2x faster attention |
| **GGUF Export** | Direct Ollama deployment |

---

## Axolotl

### Overview

Advanced framework for complex training scenarios.

### Installation

```bash
pip install axolotl
# Or from source
git clone https://github.com/OpenAccess-AI-Collective/axolotl
cd axolotl
pip install -e ".[flash-attn,deepspeed]"
```

### Configuration (YAML)

```yaml
# config.yaml
base_model: meta-llama/Llama-3.1-8B
model_type: LlamaForCausalLM
tokenizer_type: AutoTokenizer

load_in_8bit: false
load_in_4bit: true
strict: false

datasets:
  - path: my_dataset.jsonl
    type: alpaca
    data_files:
      - train.jsonl

dataset_prepared_path: prepared_data
val_set_size: 0.05
output_dir: ./outputs

adapter: lora
lora_r: 32
lora_alpha: 16
lora_dropout: 0.05
lora_target_modules:
  - q_proj
  - v_proj
  - k_proj
  - o_proj
  - gate_proj
  - down_proj
  - up_proj

sequence_len: 4096
sample_packing: true
pad_to_sequence_len: true

gradient_accumulation_steps: 4
micro_batch_size: 2
num_epochs: 3
optimizer: adamw_bnb_8bit
lr_scheduler: cosine
learning_rate: 2e-4
warmup_ratio: 0.03
weight_decay: 0.01

train_on_inputs: false
group_by_length: false
bf16: auto
fp16: false
tf32: false

gradient_checkpointing: true
flash_attention: true
deepspeed: null

wandb_project: my-finetune
wandb_run_id: run-001
wandb_log_model: false

special_tokens:
  pad_token: "<|end_of_text|>"
```

### Training

```bash
# Single GPU
accelerate launch -m axolotl.cli.train config.yaml

# Multi-GPU (DeepSpeed)
accelerate launch --config_file deepspeed.yaml -m axolotl.cli.train config.yaml

# Inference test
accelerate launch -m axolotl.cli.inference config.yaml --lora_model_dir ./outputs
```

---

## Alignment Methods

### Supervised Fine-tuning (SFT)

Basic instruction following on curated data.

### RLHF (Reinforcement Learning from Human Feedback)

```
SFT Model → Reward Model → PPO Training → RLHF Model
```

### DPO (Direct Preference Optimization)

Simpler alternative to RLHF. No reward model needed.

```python
from trl import DPOTrainer, DPOConfig

# Dataset format
# {"prompt": "...", "chosen": "preferred response", "rejected": "worse response"}

dpo_config = DPOConfig(
    beta=0.1,  # KL penalty
    learning_rate=5e-7,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    num_train_epochs=1,
)

trainer = DPOTrainer(
    model=model,
    ref_model=ref_model,
    args=dpo_config,
    train_dataset=dataset,
    tokenizer=tokenizer,
)

trainer.train()
```

### ORPO (Odds Ratio Preference Optimization)

2024 method. Even simpler than DPO.

```python
from trl import ORPOTrainer, ORPOConfig

orpo_config = ORPOConfig(
    beta=0.1,
    learning_rate=8e-6,
    per_device_train_batch_size=2,
    num_train_epochs=1,
)

trainer = ORPOTrainer(
    model=model,
    args=orpo_config,
    train_dataset=dataset,
    tokenizer=tokenizer,
)
```

---

## Model Merging

### Merge Strategies

| Method | Description | Use Case |
|--------|-------------|----------|
| **Linear** | Weighted average | Simple blending |
| **SLERP** | Spherical interpolation | Smooth transitions |
| **TIES** | Trimmed sparse averaging | Reduce interference |
| **DARE** | Drop and rescale | Better generalization |

### Using mergekit

```bash
pip install mergekit

# Create merge config (merge.yaml)
```

```yaml
# merge.yaml
slices:
  - sources:
      - model: base_model
        layer_range: [0, 32]
      - model: finetuned_model
        layer_range: [0, 32]
    merge_method: slerp
    base_model: base_model
    parameters:
      t: 0.5

merge_method: slerp
dtype: float16
```

```bash
# Run merge
mergekit-yaml merge.yaml ./merged_output
```

### LoRA Merging

```python
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load base model
base_model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-8B",
    torch_dtype=torch.float16,
    device_map="auto",
)

# Load LoRA
model = PeftModel.from_pretrained(base_model, "path/to/lora")

# Merge and unload
merged = model.merge_and_unload()

# Save
merged.save_pretrained("merged_model")
```

---

## References

- [Hugging Face PEFT](https://huggingface.co/docs/peft)
- [TRL Documentation](https://huggingface.co/docs/trl)
- [LLaMA-Factory GitHub](https://github.com/hiyouga/LLaMA-Factory)
- [Unsloth GitHub](https://github.com/unslothai/unsloth)
- [Axolotl GitHub](https://github.com/OpenAccess-AI-Collective/axolotl)
- [OpenAI Fine-tuning Guide](https://platform.openai.com/docs/guides/fine-tuning)
- [QLoRA Paper](https://arxiv.org/abs/2305.14314)
- [LoRA Paper](https://arxiv.org/abs/2106.09685)
- [DPO Paper](https://arxiv.org/abs/2305.18290)
- [ORPO Paper](https://arxiv.org/abs/2403.07691)

---

*Last updated: 2026-01-23*
*Part 1 of 2: Techniques & Frameworks*

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Fine-tuning concept understanding | sonnet | Learning |
| Dataset preparation | sonnet | Data preparation |
| Training job configuration | haiku | Configuration |
