# Fine-tuning Code Examples

Production-ready code examples for major fine-tuning frameworks.

---

## Table of Contents

1. [Unsloth (Recommended for Limited GPU)](#unsloth)
2. [LLaMA-Factory](#llama-factory)
3. [Axolotl](#axolotl)
4. [TRL with PEFT](#trl-with-peft)
5. [OpenAI Fine-tuning API](#openai-fine-tuning-api)
6. [DPO Alignment](#dpo-alignment)
7. [ORPO Alignment](#orpo-alignment)
8. [Model Merging](#model-merging)

---

## Unsloth

**Best for:** Consumer GPUs, 2-5x faster training, 80% less memory.

### Installation

```bash
pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
pip install --no-deps trl peft accelerate bitsandbytes
```

### Full Training Script

```python
from unsloth import FastLanguageModel
from trl import SFTTrainer
from transformers import TrainingArguments
from datasets import load_dataset
import torch

# Configuration
MODEL_NAME = "unsloth/Llama-3.2-3B"
MAX_SEQ_LENGTH = 2048
LORA_RANK = 16
OUTPUT_DIR = "./outputs/llama3-finetuned"

# Load model (4-bit quantized)
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=MODEL_NAME,
    max_seq_length=MAX_SEQ_LENGTH,
    dtype=None,  # Auto-detect (bf16 if supported)
    load_in_4bit=True,
)

# Add LoRA adapters
model = FastLanguageModel.get_peft_model(
    model,
    r=LORA_RANK,
    target_modules=[
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj"
    ],
    lora_alpha=LORA_RANK,
    lora_dropout=0,
    bias="none",
    use_gradient_checkpointing="unsloth",  # 30% less VRAM
    random_state=42,
)

# Prepare dataset
def format_instruction(example):
    return f"""### Instruction:
{example['instruction']}

### Input:
{example['input']}

### Response:
{example['output']}"""

dataset = load_dataset("json", data_files="training_data.jsonl", split="train")
dataset = dataset.map(lambda x: {"text": format_instruction(x)})

# Training arguments
training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    warmup_steps=10,
    num_train_epochs=3,
    learning_rate=2e-4,
    fp16=not torch.cuda.is_bf16_supported(),
    bf16=torch.cuda.is_bf16_supported(),
    logging_steps=10,
    optim="adamw_8bit",
    weight_decay=0.01,
    lr_scheduler_type="cosine",
    seed=42,
    save_strategy="epoch",
)

# Train
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    dataset_text_field="text",
    max_seq_length=MAX_SEQ_LENGTH,
    args=training_args,
)

trainer.train()

# Save outputs
model.save_pretrained(f"{OUTPUT_DIR}/lora")
tokenizer.save_pretrained(f"{OUTPUT_DIR}/lora")

# Save merged model (16-bit)
model.save_pretrained_merged(
    f"{OUTPUT_DIR}/merged_16bit",
    tokenizer,
    save_method="merged_16bit"
)

# Save GGUF for Ollama
model.save_pretrained_gguf(
    f"{OUTPUT_DIR}/gguf",
    tokenizer,
    quantization_method="q4_k_m"
)

print(f"Training complete. Outputs saved to {OUTPUT_DIR}")
```

---

## LLaMA-Factory

**Best for:** WebUI, beginners, broad model support.

### Installation

```bash
git clone https://github.com/hiyouga/LLaMA-Factory.git
cd LLaMA-Factory
pip install -e ".[torch,metrics]"
```

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
    --lora_target q_proj,v_proj,k_proj,o_proj \
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

### WebUI Training

```bash
# Launch WebUI
python src/webui.py

# Access at http://localhost:7860
```

### Custom Dataset Configuration

```yaml
# data/dataset_info.json
{
  "my_dataset": {
    "file_name": "my_data.json",
    "columns": {
      "prompt": "instruction",
      "query": "input",
      "response": "output"
    }
  }
}
```

---

## Axolotl

**Best for:** Advanced users, complex configurations, multi-GPU.

### Installation

```bash
pip install axolotl
# Or from source for latest features
git clone https://github.com/OpenAccess-AI-Collective/axolotl
cd axolotl
pip install -e ".[flash-attn,deepspeed]"
```

### Configuration File

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

# LoRA configuration
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

# Sequence settings
sequence_len: 4096
sample_packing: true
pad_to_sequence_len: true

# Training settings
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

# Logging
wandb_project: my-finetune
wandb_run_id: run-001
wandb_log_model: false

special_tokens:
  pad_token: "<|end_of_text|>"
```

### Training Commands

```bash
# Single GPU
accelerate launch -m axolotl.cli.train config.yaml

# Multi-GPU with DeepSpeed
accelerate launch --config_file deepspeed.yaml -m axolotl.cli.train config.yaml

# Inference test
accelerate launch -m axolotl.cli.inference config.yaml \
    --lora_model_dir ./outputs
```

---

## TRL with PEFT

**Best for:** Hugging Face ecosystem, custom training loops.

### QLoRA Training

```python
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer
from datasets import load_dataset

# Configuration
MODEL_NAME = "meta-llama/Llama-3.1-8B"
OUTPUT_DIR = "./outputs/llama3-qlora"

# 4-bit quantization config
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)

# Load model
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True,
)
model = prepare_model_for_kbit_training(model)

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

# LoRA config
lora_config = LoraConfig(
    r=16,
    lora_alpha=16,
    target_modules=[
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj"
    ],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

# Load dataset
dataset = load_dataset("json", data_files="training_data.jsonl", split="train")

# Format function
def format_prompt(example):
    return f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are a helpful assistant.<|eot_id|><|start_header_id|>user<|end_header_id|>
{example['instruction']}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
{example['output']}<|eot_id|>"""

dataset = dataset.map(lambda x: {"text": format_prompt(x)})

# Training arguments
training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    num_train_epochs=3,
    learning_rate=2e-4,
    bf16=True,
    logging_steps=10,
    save_strategy="epoch",
    warmup_ratio=0.03,
    lr_scheduler_type="cosine",
    optim="paged_adamw_8bit",
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
trainer.save_model(OUTPUT_DIR)
```

---

## OpenAI Fine-tuning API

**Best for:** No GPU needed, fast iteration, API-only workflows.

### Data Preparation

```python
import json

# Prepare training data
training_examples = [
    {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is LoRA?"},
            {"role": "assistant", "content": "LoRA (Low-Rank Adaptation) is..."}
        ]
    },
    # Add more examples...
]

# Save as JSONL
with open("training_data.jsonl", "w") as f:
    for example in training_examples:
        f.write(json.dumps(example) + "\n")
```

### Fine-tuning Script

```python
from openai import OpenAI
import time

client = OpenAI()

# Upload training file
with open("training_data.jsonl", "rb") as f:
    file = client.files.create(file=f, purpose="fine-tune")

print(f"File uploaded: {file.id}")

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

print(f"Job created: {job.id}")

# Monitor progress
while True:
    job = client.fine_tuning.jobs.retrieve(job.id)
    print(f"Status: {job.status}")

    if job.status in ["succeeded", "failed", "cancelled"]:
        break

    # Print latest events
    events = client.fine_tuning.jobs.list_events(job.id, limit=5)
    for event in events.data:
        print(f"  {event.message}")

    time.sleep(60)

# Use fine-tuned model
if job.status == "succeeded":
    response = client.chat.completions.create(
        model=job.fine_tuned_model,
        messages=[{"role": "user", "content": "Hello!"}]
    )
    print(response.choices[0].message.content)
```

### Cost Estimation (2025 Pricing)

| Model | Training Cost | Inference Cost |
|-------|---------------|----------------|
| gpt-4o-mini-2024-07-18 | $3.00/1M tokens | $12.00/1M output |
| gpt-4o-2024-08-06 | $25.00/1M tokens | $100.00/1M output |

---

## DPO Alignment

**Best for:** Preference learning without reward model.

```python
from trl import DPOTrainer, DPOConfig
from transformers import AutoModelForCausalLM, AutoTokenizer
from datasets import load_dataset
from peft import LoraConfig

# Load model and tokenizer
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-8B",
    torch_dtype=torch.bfloat16,
    device_map="auto",
)
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B")
tokenizer.pad_token = tokenizer.eos_token

# Reference model (frozen copy)
ref_model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-8B",
    torch_dtype=torch.bfloat16,
    device_map="auto",
)

# LoRA config
peft_config = LoraConfig(
    r=16,
    lora_alpha=16,
    lora_dropout=0.05,
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
    bias="none",
    task_type="CAUSAL_LM",
)

# Load preference dataset
# Format: {"prompt": "...", "chosen": "...", "rejected": "..."}
dataset = load_dataset("json", data_files="preference_data.jsonl", split="train")

# DPO config
dpo_config = DPOConfig(
    output_dir="./outputs/dpo",
    beta=0.1,  # KL penalty coefficient
    learning_rate=5e-7,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    num_train_epochs=1,
    warmup_ratio=0.1,
    bf16=True,
    logging_steps=10,
    save_strategy="epoch",
)

# Train
trainer = DPOTrainer(
    model=model,
    ref_model=ref_model,
    args=dpo_config,
    train_dataset=dataset,
    tokenizer=tokenizer,
    peft_config=peft_config,
)

trainer.train()
trainer.save_model("./outputs/dpo/final")
```

---

## ORPO Alignment

**Best for:** Simpler than DPO, no reference model needed.

```python
from trl import ORPOTrainer, ORPOConfig
from transformers import AutoModelForCausalLM, AutoTokenizer
from datasets import load_dataset
from peft import LoraConfig

# Load model
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-8B",
    torch_dtype=torch.bfloat16,
    device_map="auto",
)
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B")
tokenizer.pad_token = tokenizer.eos_token

# LoRA config
peft_config = LoraConfig(
    r=16,
    lora_alpha=16,
    lora_dropout=0.05,
    target_modules=["q_proj", "v_proj"],
    bias="none",
    task_type="CAUSAL_LM",
)

# Load dataset (same format as DPO)
dataset = load_dataset("json", data_files="preference_data.jsonl", split="train")

# ORPO config
orpo_config = ORPOConfig(
    output_dir="./outputs/orpo",
    beta=0.1,
    learning_rate=8e-6,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    num_train_epochs=1,
    warmup_ratio=0.1,
    bf16=True,
    logging_steps=10,
)

# Train (no reference model needed!)
trainer = ORPOTrainer(
    model=model,
    args=orpo_config,
    train_dataset=dataset,
    tokenizer=tokenizer,
    peft_config=peft_config,
)

trainer.train()
trainer.save_model("./outputs/orpo/final")
```

---

## Model Merging

### LoRA Merging with PEFT

```python
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load base model
base_model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-8B",
    torch_dtype=torch.float16,
    device_map="auto",
)

# Load LoRA adapter
model = PeftModel.from_pretrained(base_model, "path/to/lora")

# Merge and unload
merged = model.merge_and_unload()

# Save merged model
merged.save_pretrained("merged_model")
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B")
tokenizer.save_pretrained("merged_model")
```

### Model Merging with mergekit

```bash
pip install mergekit
```

```yaml
# merge.yaml - SLERP merge
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

---

*Last updated: 2026-01-25*
