# Fine-tuning Examples

Production-ready code examples for LoRA, QLoRA, DoRA, and rsLoRA.

## 1. Basic LoRA Fine-tuning

### Minimal Example

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer
from peft import LoraConfig, get_peft_model, TaskType
from datasets import Dataset
import torch

# Load model
model_name = "meta-llama/Llama-3.2-3B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.bfloat16,
    device_map="auto"
)

# LoRA config
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_dropout=0.05,
    task_type=TaskType.CAUSAL_LM
)

# Apply LoRA
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
# trainable params: 6,815,744 || all params: 3,219,857,408 || trainable%: 0.21%
```

## 2. QLoRA Fine-tuning (4-bit)

### Memory-Efficient Setup

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
import torch

model_name = "meta-llama/Llama-3.1-8B-Instruct"

# 4-bit quantization config
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",           # NormalFloat4 - optimal for normally distributed weights
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True       # Quantize the quantization constants
)

# Load quantized model
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True
)

tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

# Prepare for k-bit training
model = prepare_model_for_kbit_training(model)

# LoRA config with all linear layers
lora_config = LoraConfig(
    r=32,
    lora_alpha=64,
    target_modules=[
        "q_proj", "k_proj", "v_proj", "o_proj",  # Attention
        "gate_proj", "up_proj", "down_proj"       # MLP
    ],
    lora_dropout=0.1,
    bias="none",
    task_type=TaskType.CAUSAL_LM
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
```

## 3. DoRA Fine-tuning (Weight-Decomposed)

### DoRA Configuration

```python
from peft import LoraConfig, get_peft_model
import torch

# DoRA config - uses weight decomposition
dora_config = LoraConfig(
    r=16,                                  # Can use lower rank than LoRA
    lora_alpha=32,
    target_modules=[
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj"
    ],
    lora_dropout=0.05,
    use_dora=True,                         # Enable weight decomposition
    task_type=TaskType.CAUSAL_LM
)

model = get_peft_model(model, dora_config)
model.print_trainable_parameters()
```

### QDoRA (Quantized + DoRA)

```python
from transformers import AutoModelForCausalLM, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
import torch

# 4-bit quantization
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True
)

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-8B-Instruct",
    quantization_config=bnb_config,
    device_map="auto"
)
model = prepare_model_for_kbit_training(model)

# QDoRA config
qdora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.05,
    use_dora=True,                         # DoRA enabled
    task_type=TaskType.CAUSAL_LM
)

model = get_peft_model(model, qdora_config)
```

## 4. rsLoRA (Rank-Stabilized)

### High-Rank Training

```python
from peft import LoraConfig, get_peft_model

# rsLoRA config - enables effective high-rank training
rslora_config = LoraConfig(
    r=128,                                 # High rank works well with rsLoRA
    lora_alpha=256,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.1,
    use_rslora=True,                       # Rank-stabilized scaling: alpha/sqrt(r)
    task_type=TaskType.CAUSAL_LM
)

model = get_peft_model(model, rslora_config)
```

## 5. Data Preparation

### Instruction Format (Alpaca Style)

```python
from datasets import Dataset

def format_instruction(example: dict) -> str:
    """Format example for instruction fine-tuning (Alpaca style)."""
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

def prepare_dataset(examples: list[dict], tokenizer, max_length: int = 2048) -> Dataset:
    """Prepare dataset for training."""

    def tokenize(example):
        text = format_instruction(example)
        tokens = tokenizer(
            text,
            truncation=True,
            max_length=max_length,
            padding="max_length"
        )
        tokens["labels"] = tokens["input_ids"].copy()
        return tokens

    dataset = Dataset.from_list(examples)
    return dataset.map(tokenize, remove_columns=dataset.column_names)

# Example data
training_data = [
    {
        "instruction": "Summarize the following text concisely.",
        "input": "The development of artificial intelligence has progressed rapidly...",
        "output": "AI development has accelerated significantly in recent years."
    },
    {
        "instruction": "Write a haiku about programming.",
        "input": "",
        "output": "Lines of code compile\nBugs emerge from the shadows\nDebugger awaits"
    }
]

train_dataset = prepare_dataset(training_data, tokenizer)
```

### Chat Format (ChatML)

```python
def format_chat(example: dict) -> str:
    """Format example for chat fine-tuning (ChatML)."""
    messages = example["messages"]
    formatted = ""

    for msg in messages:
        role = msg["role"]
        content = msg["content"]
        formatted += f"<|im_start|>{role}\n{content}<|im_end|>\n"

    return formatted

# Example chat data
chat_data = [
    {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is Python?"},
            {"role": "assistant", "content": "Python is a high-level programming language..."}
        ]
    }
]
```

### Llama 3 Chat Format

```python
def format_llama3_chat(example: dict, tokenizer) -> str:
    """Format example for Llama 3 chat fine-tuning."""
    messages = example["messages"]
    return tokenizer.apply_chat_template(messages, tokenize=False)

# Using tokenizer's built-in template
formatted = tokenizer.apply_chat_template(
    [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"},
        {"role": "assistant", "content": "Hi there!"}
    ],
    tokenize=False
)
```

## 6. Training with Trainer

### Standard Trainer

```python
from transformers import TrainingArguments, Trainer, DataCollatorForLanguageModeling

training_args = TrainingArguments(
    output_dir="./lora-output",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    fp16=True,                             # Use bf16=True for newer GPUs
    logging_steps=10,
    save_strategy="epoch",
    warmup_ratio=0.03,
    lr_scheduler_type="cosine",
    optim="paged_adamw_8bit",              # Memory-efficient optimizer
    gradient_checkpointing=True,           # Reduce memory usage
    max_grad_norm=0.3,                     # Gradient clipping
    report_to="wandb",                     # Optional: W&B logging
)

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,              # Optional
    data_collator=data_collator
)

trainer.train()

# Save adapter
model.save_pretrained("./lora-adapter")
tokenizer.save_pretrained("./lora-adapter")
```

### SFTTrainer (Recommended)

```python
from trl import SFTTrainer, SFTConfig

sft_config = SFTConfig(
    output_dir="./sft-output",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    fp16=True,
    logging_steps=10,
    save_strategy="epoch",
    warmup_ratio=0.03,
    lr_scheduler_type="cosine",
    optim="paged_adamw_8bit",
    max_seq_length=2048,
    packing=True,                          # Pack short sequences for efficiency
)

trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    tokenizer=tokenizer,
    args=sft_config,
    peft_config=lora_config,               # Pass LoRA config directly
)

trainer.train()
```

## 7. Loading and Inference

### Load Adapter

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import torch

# Load base model
base_model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-8B-Instruct",
    torch_dtype=torch.bfloat16,
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")

# Load adapter
model = PeftModel.from_pretrained(base_model, "./lora-adapter")
model.eval()
```

### Generate Text

```python
def generate(model, tokenizer, prompt: str, max_new_tokens: int = 256) -> str:
    """Generate text with LoRA model."""
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)

response = generate(model, tokenizer, "### Instruction:\nWrite a poem about AI.\n\n### Response:\n")
```

### Merge Adapter into Base Model

```python
# Merge LoRA weights into base model (for deployment)
merged_model = model.merge_and_unload()

# Save merged model
merged_model.save_pretrained("./merged-model")
tokenizer.save_pretrained("./merged-model")
```

## 8. Multiple Adapters

### Load and Switch Adapters

```python
from peft import PeftModel

# Load base model
base_model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-8B-Instruct",
    torch_dtype=torch.bfloat16,
    device_map="auto"
)

# Load first adapter
model = PeftModel.from_pretrained(
    base_model,
    "./adapters/customer-support",
    adapter_name="customer_support"
)

# Load additional adapters
model.load_adapter("./adapters/code-gen", adapter_name="code_gen")
model.load_adapter("./adapters/summary", adapter_name="summary")

# Switch between adapters
model.set_adapter("customer_support")
response1 = generate(model, tokenizer, "How do I reset my password?")

model.set_adapter("code_gen")
response2 = generate(model, tokenizer, "Write a Python function to sort a list")

model.set_adapter("summary")
response3 = generate(model, tokenizer, "Summarize this article: ...")
```

## 9. Unsloth (2x Faster)

### Unsloth QLoRA Example

```python
from unsloth import FastLanguageModel
import torch

# Load model with Unsloth (2x faster, 50% less memory)
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Llama-3.2-3B-Instruct",
    max_seq_length=2048,
    dtype=None,                            # Auto-detect
    load_in_4bit=True,
)

# Apply LoRA with Unsloth
model = FastLanguageModel.get_peft_model(
    model,
    r=16,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    lora_alpha=32,
    lora_dropout=0.05,
    bias="none",
    use_gradient_checkpointing="unsloth", # 30% faster
    random_state=42,
    use_rslora=True,                       # rsLoRA for high ranks
)

# Training with SFTTrainer
from trl import SFTTrainer, SFTConfig

trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    args=SFTConfig(
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        warmup_steps=10,
        max_steps=100,
        learning_rate=2e-4,
        fp16=not torch.cuda.is_bf16_supported(),
        bf16=torch.cuda.is_bf16_supported(),
        optim="adamw_8bit",
        output_dir="./outputs",
    ),
)

trainer.train()

# Save
model.save_pretrained_merged("./merged-model", tokenizer, save_method="merged_16bit")
# Or save as GGUF for llama.cpp
model.save_pretrained_gguf("./gguf-model", tokenizer, quantization_method="q4_k_m")
```

## 10. Hyperparameter Grid Search

```python
from dataclasses import dataclass
from typing import Optional
import json

@dataclass
class LoRAExperiment:
    rank: int
    alpha: int
    dropout: float
    target_modules: list[str]
    learning_rate: float
    use_rslora: bool = False
    use_dora: bool = False

def run_experiment(config: LoRAExperiment, train_dataset, val_dataset) -> dict:
    """Run a single experiment and return metrics."""

    lora_config = LoraConfig(
        r=config.rank,
        lora_alpha=config.alpha,
        target_modules=config.target_modules,
        lora_dropout=config.dropout,
        use_rslora=config.use_rslora,
        use_dora=config.use_dora,
        task_type=TaskType.CAUSAL_LM
    )

    # ... training code ...

    return {
        "config": config.__dict__,
        "train_loss": trainer.state.log_history[-1].get("train_loss"),
        "eval_loss": trainer.state.log_history[-1].get("eval_loss"),
    }

# Experiment grid
experiments = [
    LoRAExperiment(rank=8, alpha=16, dropout=0.05,
                   target_modules=["q_proj", "v_proj"], learning_rate=2e-4),
    LoRAExperiment(rank=16, alpha=32, dropout=0.05,
                   target_modules=["q_proj", "k_proj", "v_proj", "o_proj"], learning_rate=2e-4),
    LoRAExperiment(rank=32, alpha=64, dropout=0.1,
                   target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
                   learning_rate=1e-4),
    LoRAExperiment(rank=64, alpha=128, dropout=0.1,
                   target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
                   learning_rate=1e-4, use_rslora=True),
]

results = []
for exp in experiments:
    result = run_experiment(exp, train_dataset, val_dataset)
    results.append(result)
    print(f"Rank={exp.rank}, Loss={result['train_loss']:.4f}")

# Save results
with open("experiment_results.json", "w") as f:
    json.dump(results, f, indent=2)
```
