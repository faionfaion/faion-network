# Fine-tuning Configuration Templates

Ready-to-use configuration templates for common fine-tuning scenarios.

---

## Table of Contents

1. [Data Format Templates](#data-format-templates)
2. [LoRA Configuration Templates](#lora-configuration-templates)
3. [Axolotl YAML Templates](#axolotl-yaml-templates)
4. [Training Arguments Templates](#training-arguments-templates)
5. [Quantization Templates](#quantization-templates)

---

## Data Format Templates

### Alpaca Format (Instruction)

```json
{
  "instruction": "Summarize the following text in one sentence.",
  "input": "The quick brown fox jumps over the lazy dog. This sentence contains every letter of the alphabet.",
  "output": "A pangram sentence featuring a fox and dog demonstrates all alphabet letters."
}
```

### ShareGPT Format (Multi-turn)

```json
{
  "conversations": [
    {"from": "human", "value": "What is machine learning?"},
    {"from": "gpt", "value": "Machine learning is a subset of AI..."},
    {"from": "human", "value": "Can you give an example?"},
    {"from": "gpt", "value": "Sure! A common example is email spam filtering..."}
  ]
}
```

### OpenAI Chat Format

```json
{
  "messages": [
    {"role": "system", "content": "You are a helpful coding assistant."},
    {"role": "user", "content": "Write a Python function to reverse a string."},
    {"role": "assistant", "content": "def reverse_string(s):\n    return s[::-1]"}
  ]
}
```

### DPO/ORPO Preference Format

```json
{
  "prompt": "Explain quantum computing in simple terms.",
  "chosen": "Quantum computing uses quantum bits (qubits) that can exist in multiple states simultaneously, unlike classical bits that are either 0 or 1. This allows quantum computers to solve certain problems much faster.",
  "rejected": "Quantum computing is a type of computing that uses quantum mechanics. It's very complex and uses qubits instead of bits."
}
```

### Function Calling Format

```json
{
  "messages": [
    {"role": "system", "content": "You are an assistant that can call functions."},
    {"role": "user", "content": "What's the weather in Paris?"},
    {"role": "assistant", "content": null, "function_call": {"name": "get_weather", "arguments": "{\"location\": \"Paris\"}"}}
  ],
  "functions": [
    {
      "name": "get_weather",
      "description": "Get current weather for a location",
      "parameters": {
        "type": "object",
        "properties": {
          "location": {"type": "string", "description": "City name"}
        },
        "required": ["location"]
      }
    }
  ]
}
```

---

## LoRA Configuration Templates

### Conservative (Small Tasks)

```python
lora_config = LoraConfig(
    r=8,
    lora_alpha=8,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.1,
    bias="none",
    task_type="CAUSAL_LM",
)
```

### Balanced (General Purpose)

```python
lora_config = LoraConfig(
    r=16,
    lora_alpha=16,
    target_modules=[
        "q_proj", "k_proj", "v_proj", "o_proj"
    ],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)
```

### Comprehensive (Complex Tasks)

```python
lora_config = LoraConfig(
    r=32,
    lora_alpha=32,
    target_modules=[
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj"
    ],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)
```

### Maximum Quality

```python
lora_config = LoraConfig(
    r=64,
    lora_alpha=64,
    target_modules=[
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj",
        "embed_tokens", "lm_head"
    ],
    lora_dropout=0.0,
    bias="none",
    task_type="CAUSAL_LM",
)
```

### Target Modules by Model Family

```python
# LLaMA / Mistral / Qwen2
LLAMA_MODULES = [
    "q_proj", "k_proj", "v_proj", "o_proj",
    "gate_proj", "up_proj", "down_proj"
]

# Phi-3
PHI_MODULES = [
    "q_proj", "k_proj", "v_proj", "dense",
    "gate_up_proj", "down_proj"
]

# GPT-NeoX / Pythia
NEOX_MODULES = [
    "query_key_value", "dense", "dense_h_to_4h", "dense_4h_to_h"
]

# Falcon
FALCON_MODULES = [
    "query_key_value", "dense", "dense_h_to_4h", "dense_4h_to_h"
]
```

---

## Axolotl YAML Templates

### Basic LoRA Fine-tuning

```yaml
# basic-lora.yaml
base_model: meta-llama/Llama-3.1-8B
model_type: LlamaForCausalLM
tokenizer_type: AutoTokenizer

load_in_4bit: true
strict: false

datasets:
  - path: data/train.jsonl
    type: alpaca

val_set_size: 0.05
output_dir: ./outputs/basic-lora

adapter: lora
lora_r: 16
lora_alpha: 16
lora_dropout: 0.05
lora_target_modules:
  - q_proj
  - v_proj
  - k_proj
  - o_proj

sequence_len: 2048
sample_packing: false

gradient_accumulation_steps: 4
micro_batch_size: 2
num_epochs: 3
optimizer: adamw_bnb_8bit
lr_scheduler: cosine
learning_rate: 2e-4
warmup_ratio: 0.03

bf16: auto
gradient_checkpointing: true
```

### QLoRA with Sample Packing

```yaml
# qlora-packed.yaml
base_model: meta-llama/Llama-3.1-8B
model_type: LlamaForCausalLM
tokenizer_type: AutoTokenizer

load_in_4bit: true
strict: false

datasets:
  - path: data/train.jsonl
    type: alpaca

dataset_prepared_path: prepared_data
val_set_size: 0.05
output_dir: ./outputs/qlora-packed

adapter: qlora
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

gradient_checkpointing: true
flash_attention: true

wandb_project: my-finetune
```

### Multi-GPU with DeepSpeed

```yaml
# deepspeed-multi-gpu.yaml
base_model: meta-llama/Llama-3.1-70B
model_type: LlamaForCausalLM
tokenizer_type: AutoTokenizer

load_in_4bit: true
strict: false

datasets:
  - path: data/train.jsonl
    type: alpaca

val_set_size: 0.05
output_dir: ./outputs/70b-finetune

adapter: qlora
lora_r: 64
lora_alpha: 32
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

gradient_accumulation_steps: 8
micro_batch_size: 1
num_epochs: 2
optimizer: adamw_bnb_8bit
lr_scheduler: cosine
learning_rate: 1e-4
warmup_ratio: 0.03

bf16: auto
gradient_checkpointing: true
flash_attention: true

deepspeed: deepspeed_configs/zero3_bf16.json
```

### DPO Alignment

```yaml
# dpo-alignment.yaml
base_model: meta-llama/Llama-3.1-8B-Instruct
model_type: LlamaForCausalLM
tokenizer_type: AutoTokenizer

load_in_4bit: true
strict: false

rl: dpo
datasets:
  - path: data/preferences.jsonl
    type: chatml.intel

val_set_size: 0.05
output_dir: ./outputs/dpo

adapter: lora
lora_r: 16
lora_alpha: 16
lora_dropout: 0.05
lora_target_modules:
  - q_proj
  - v_proj

sequence_len: 2048
sample_packing: false

gradient_accumulation_steps: 4
micro_batch_size: 1
num_epochs: 1
optimizer: adamw_bnb_8bit
lr_scheduler: cosine
learning_rate: 5e-7
warmup_ratio: 0.1

bf16: auto
gradient_checkpointing: true
```

---

## Training Arguments Templates

### Conservative (Prevent Overfitting)

```python
training_args = TrainingArguments(
    output_dir="./outputs",
    per_device_train_batch_size=1,
    gradient_accumulation_steps=8,
    num_train_epochs=1,
    learning_rate=1e-5,
    warmup_ratio=0.1,
    weight_decay=0.1,
    lr_scheduler_type="cosine",
    bf16=True,
    logging_steps=10,
    save_strategy="steps",
    save_steps=100,
    evaluation_strategy="steps",
    eval_steps=100,
    load_best_model_at_end=True,
)
```

### Balanced (General Purpose)

```python
training_args = TrainingArguments(
    output_dir="./outputs",
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    num_train_epochs=3,
    learning_rate=2e-4,
    warmup_ratio=0.03,
    weight_decay=0.01,
    lr_scheduler_type="cosine",
    bf16=True,
    logging_steps=10,
    save_strategy="epoch",
    optim="paged_adamw_8bit",
)
```

### Aggressive (Maximum Learning)

```python
training_args = TrainingArguments(
    output_dir="./outputs",
    per_device_train_batch_size=4,
    gradient_accumulation_steps=2,
    num_train_epochs=5,
    learning_rate=5e-4,
    warmup_ratio=0.01,
    weight_decay=0.0,
    lr_scheduler_type="linear",
    bf16=True,
    logging_steps=5,
    save_strategy="epoch",
    optim="adamw_8bit",
)
```

---

## Quantization Templates

### 4-bit NF4 (Recommended)

```python
from transformers import BitsAndBytesConfig
import torch

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)
```

### 8-bit (Higher Quality)

```python
from transformers import BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(
    load_in_8bit=True,
)
```

### GGUF Export Quantization Methods

| Method | Size | Quality | Use Case |
|--------|------|---------|----------|
| `q2_k` | Smallest | Lowest | Extreme constraints |
| `q3_k_m` | Small | Low | Mobile |
| `q4_k_m` | Medium | Good | **Recommended default** |
| `q5_k_m` | Larger | Better | Quality focus |
| `q6_k` | Large | High | Near-FP16 quality |
| `q8_0` | Largest | Highest | Maximum quality |

```python
# Export with Unsloth
model.save_pretrained_gguf(
    "model_gguf",
    tokenizer,
    quantization_method="q4_k_m"  # Balanced quality/size
)
```

---

## Model-Specific Templates

### Llama 3.1 Chat Template

```python
def format_llama3_chat(messages):
    formatted = "<|begin_of_text|>"
    for msg in messages:
        role = msg["role"]
        content = msg["content"]
        formatted += f"<|start_header_id|>{role}<|end_header_id|>\n\n{content}<|eot_id|>"
    formatted += "<|start_header_id|>assistant<|end_header_id|>\n\n"
    return formatted
```

### Mistral Instruct Template

```python
def format_mistral_instruct(instruction, response=None):
    text = f"<s>[INST] {instruction} [/INST]"
    if response:
        text += f" {response}</s>"
    return text
```

### Qwen2 Chat Template

```python
def format_qwen2_chat(messages):
    formatted = ""
    for msg in messages:
        role = msg["role"]
        content = msg["content"]
        if role == "system":
            formatted += f"<|im_start|>system\n{content}<|im_end|>\n"
        elif role == "user":
            formatted += f"<|im_start|>user\n{content}<|im_end|>\n"
        elif role == "assistant":
            formatted += f"<|im_start|>assistant\n{content}<|im_end|>\n"
    formatted += "<|im_start|>assistant\n"
    return formatted
```

---

*Last updated: 2026-01-25*
