# LoRA and QLoRA

**Low-Rank Adaptation and Quantized LoRA for Efficient Fine-tuning**

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

## Training with LoRA/QLoRA

### Basic Setup

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

# Load base model with 4-bit quantization
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-8B",
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True,
)

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B")

# Prepare for QLoRA
model = prepare_model_for_kbit_training(model)

# LoRA config
lora_config = LoraConfig(
    r=16,
    lora_alpha=16,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)

# Apply LoRA
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
# trainable params: 4,194,304 || all params: 8,030,261,248 || trainable%: 0.05%
```

### Training Loop

```python
from transformers import TrainingArguments
from trl import SFTTrainer

training_args = TrainingArguments(
    output_dir="./lora_output",
    per_device_train_batch_size=4,
    gradient_accumulation_steps=2,
    num_train_epochs=3,
    learning_rate=2e-4,
    logging_steps=10,
    save_steps=100,
    optim="paged_adamw_8bit",
    warmup_ratio=0.03,
    lr_scheduler_type="cosine",
    fp16=True,
)

trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    tokenizer=tokenizer,
    max_seq_length=2048,
    dataset_text_field="text",
)

trainer.train()
```

### Saving and Loading

```python
# Save LoRA adapter
model.save_pretrained("./lora_adapter")
tokenizer.save_pretrained("./lora_adapter")

# Load LoRA adapter
from peft import AutoPeftModelForCausalLM

model = AutoPeftModelForCausalLM.from_pretrained(
    "./lora_adapter",
    device_map="auto",
    torch_dtype=torch.float16,
)

# Merge adapter with base model
merged_model = model.merge_and_unload()
merged_model.save_pretrained("./merged_model")
```

---

## Advanced Techniques

### DoRA (Weight-Decomposed LoRA)

2024 successor to LoRA with better performance.

```python
from peft import LoraConfig

lora_config = LoraConfig(
    r=16,
    lora_alpha=16,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    use_dora=True,  # Enable DoRA
    task_type="CAUSAL_LM",
)
```

### Multiple LoRA Adapters

Train different adapters for different tasks.

```python
# Train adapter 1 for task A
model = get_peft_model(model, lora_config_task_a)
trainer.train()
model.save_pretrained("./adapter_task_a")

# Train adapter 2 for task B
model = get_peft_model(base_model, lora_config_task_b)
trainer.train()
model.save_pretrained("./adapter_task_b")

# Switch between adapters
model.load_adapter("./adapter_task_a", adapter_name="task_a")
model.load_adapter("./adapter_task_b", adapter_name="task_b")
model.set_adapter("task_a")  # Use task A adapter
```

### LoRA Scaling

Adjust LoRA influence during inference.

```python
# Increase LoRA effect
model.set_adapter_scale("default", 1.5)

# Decrease LoRA effect
model.set_adapter_scale("default", 0.5)

# Disable LoRA temporarily
model.disable_adapter()

# Re-enable
model.enable_adapter()
```

---

## Best Practices

### Parameter Selection

| Scenario | Rank | Alpha | LR | Epochs |
|----------|------|-------|-----|--------|
| **Quick prototype** | 8 | 8 | 3e-4 | 1-2 |
| **General fine-tuning** | 16 | 16 | 2e-4 | 3 |
| **Complex task** | 32-64 | 32-64 | 1e-4 | 3-5 |
| **Large dataset** | 16 | 16 | 5e-5 | 1-2 |

### Memory Optimization

```python
# Enable gradient checkpointing (30% memory savings)
model.gradient_checkpointing_enable()

# Use 8-bit optimizer
training_args = TrainingArguments(
    optim="paged_adamw_8bit",
    ...
)

# Reduce sequence length
max_seq_length = 1024  # Instead of 2048

# Smaller batch size with gradient accumulation
per_device_train_batch_size = 1
gradient_accumulation_steps = 8
```

### Quality Tips

1. **Target all attention layers** - q, k, v, o projections
2. **Match alpha to rank** - alpha = rank (common practice)
3. **Use cosine scheduler** - Better than linear for most cases
4. **Monitor validation loss** - Prevent overfitting
5. **Warmup is important** - 3-10% of total steps
6. **bf16 over fp16** - If GPU supports it (A100, H100)

---

## Comparison with Full Fine-tuning

| Aspect | Full Fine-tuning | LoRA | QLoRA |
|--------|------------------|------|-------|
| **Trainable params** | 100% | 0.1-1% | 0.1-1% |
| **Memory (7B model)** | 28GB | 16GB | 6-8GB |
| **Training speed** | 1x | 1.2x | 0.8x |
| **Final quality** | Best | Very good | Good |
| **Inference cost** | Same | Same | Same (merged) |
| **Storage** | Full model | Small adapter | Small adapter |

---

## References

- [LoRA Paper](https://arxiv.org/abs/2106.09685)
- [QLoRA Paper](https://arxiv.org/abs/2305.14314)
- [DoRA Paper](https://arxiv.org/abs/2402.09353)
- [PEFT Documentation](https://huggingface.co/docs/peft)

---

*See also: [finetuning-basics.md](finetuning-basics.md), [finetuning-datasets.md](finetuning-datasets.md)*
