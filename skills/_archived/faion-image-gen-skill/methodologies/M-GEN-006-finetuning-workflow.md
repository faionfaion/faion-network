# M-GEN-006: Fine-tuning Workflow

## Overview

Fine-tuning adapts pre-trained models to specific tasks or domains. This workflow covers dataset preparation, training configuration, evaluation, and deployment. Methods include full fine-tuning, LoRA, QLoRA, and PEFT techniques.

**When to use:** When pre-trained models don't perform well enough on your specific task, or when you need consistent style/format in outputs.

## Core Concepts

### 1. Fine-tuning Methods

| Method | Memory | Speed | Quality | Use Case |
|--------|--------|-------|---------|----------|
| **Full Fine-tune** | Very High | Slow | Best | Unlimited resources |
| **LoRA** | Low | Fast | Good | Most cases |
| **QLoRA** | Very Low | Medium | Good | Consumer GPUs |
| **PEFT** | Low | Fast | Varies | Quick adaptation |
| **Prefix Tuning** | Very Low | Fast | Moderate | Small adjustments |

### 2. Dataset Requirements

| Task Type | Min Examples | Recommended | Format |
|-----------|--------------|-------------|--------|
| **Classification** | 100 | 1000+ | label, text |
| **Generation** | 100 | 500+ | instruction, response |
| **Chat** | 500 | 2000+ | conversations |
| **Code** | 200 | 1000+ | prompt, completion |
| **Summarization** | 100 | 500+ | document, summary |

### 3. Training Pipeline

```
Data Collection → Preparation → Training → Evaluation → Deployment
      ↓              ↓            ↓           ↓            ↓
   Raw data      Clean &       Fine-tune    Benchmark    Serve
                 Format                     Compare      Monitor
```

## Best Practices

### 1. Prepare Quality Datasets

```python
from datasets import Dataset
import json

def prepare_instruction_dataset(raw_data: list) -> Dataset:
    """Prepare dataset for instruction fine-tuning."""

    formatted = []
    for item in raw_data:
        formatted.append({
            "instruction": item["prompt"],
            "input": item.get("context", ""),
            "output": item["response"],
            "system": item.get("system_prompt", "You are a helpful assistant.")
        })

    # Convert to HuggingFace Dataset
    dataset = Dataset.from_list(formatted)

    # Split train/eval
    split = dataset.train_test_split(test_size=0.1)

    return split

def create_chat_format(example: dict) -> str:
    """Format example for chat fine-tuning."""

    messages = []

    if example.get("system"):
        messages.append({"role": "system", "content": example["system"]})

    instruction = example["instruction"]
    if example.get("input"):
        instruction = f"{instruction}\n\nInput: {example['input']}"

    messages.append({"role": "user", "content": instruction})
    messages.append({"role": "assistant", "content": example["output"]})

    return {"messages": messages}
```

### 2. Validate Data Quality

```python
def validate_dataset(dataset: Dataset) -> dict:
    """Validate dataset quality before training."""

    issues = {
        "empty_outputs": [],
        "too_short": [],
        "duplicates": [],
        "encoding_issues": []
    }

    seen_hashes = set()

    for i, example in enumerate(dataset):
        # Check empty outputs
        if not example["output"].strip():
            issues["empty_outputs"].append(i)

        # Check too short
        if len(example["output"].split()) < 5:
            issues["too_short"].append(i)

        # Check duplicates
        content_hash = hash(example["instruction"] + example["output"])
        if content_hash in seen_hashes:
            issues["duplicates"].append(i)
        seen_hashes.add(content_hash)

        # Check encoding
        try:
            example["output"].encode("utf-8").decode("utf-8")
        except:
            issues["encoding_issues"].append(i)

    report = {
        "total_examples": len(dataset),
        "issues": {k: len(v) for k, v in issues.items()},
        "valid_examples": len(dataset) - sum(len(v) for v in issues.values())
    }

    return report
```

### 3. Configure Training Properly

```python
from transformers import TrainingArguments

def get_training_args(
    model_size: str,
    dataset_size: int,
    output_dir: str
) -> TrainingArguments:
    """Get appropriate training arguments."""

    # Base config by model size
    configs = {
        "7b": {
            "per_device_train_batch_size": 4,
            "gradient_accumulation_steps": 4,
            "learning_rate": 2e-4,
            "num_train_epochs": 3,
        },
        "13b": {
            "per_device_train_batch_size": 2,
            "gradient_accumulation_steps": 8,
            "learning_rate": 1e-4,
            "num_train_epochs": 2,
        },
        "70b": {
            "per_device_train_batch_size": 1,
            "gradient_accumulation_steps": 16,
            "learning_rate": 5e-5,
            "num_train_epochs": 1,
        }
    }

    base = configs.get(model_size, configs["7b"])

    # Adjust for dataset size
    if dataset_size < 500:
        base["num_train_epochs"] = min(base["num_train_epochs"] + 2, 5)
    elif dataset_size > 5000:
        base["num_train_epochs"] = max(base["num_train_epochs"] - 1, 1)

    return TrainingArguments(
        output_dir=output_dir,
        **base,
        warmup_ratio=0.03,
        weight_decay=0.001,
        logging_steps=10,
        save_strategy="epoch",
        evaluation_strategy="epoch",
        bf16=True,
        optim="adamw_torch",
        lr_scheduler_type="cosine",
        report_to=["wandb"]
    )
```

## Common Patterns

### Pattern 1: LoRA Fine-tuning with Unsloth

```python
from unsloth import FastLanguageModel

# Load model with 4-bit quantization
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/llama-3.1-8b-instruct",
    max_seq_length=2048,
    dtype=None,  # Auto-detect
    load_in_4bit=True
)

# Add LoRA adapters
model = FastLanguageModel.get_peft_model(
    model,
    r=16,  # LoRA rank
    target_modules=[
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj"
    ],
    lora_alpha=16,
    lora_dropout=0,
    bias="none",
    use_gradient_checkpointing="unsloth"  # Reduce memory
)

# Training
from trl import SFTTrainer

trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    dataset_text_field="text",
    max_seq_length=2048,
    args=TrainingArguments(
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        warmup_steps=5,
        max_steps=100,
        learning_rate=2e-4,
        fp16=not torch.cuda.is_bf16_supported(),
        bf16=torch.cuda.is_bf16_supported(),
        output_dir="outputs"
    )
)

trainer.train()

# Save LoRA weights
model.save_pretrained("lora_model")
```

### Pattern 2: QLoRA with LLaMA-Factory

```yaml
# config.yaml for LLaMA-Factory
model_name_or_path: meta-llama/Meta-Llama-3.1-8B-Instruct
stage: sft
do_train: true
finetuning_type: lora

dataset: my_dataset
template: llama3
cutoff_len: 2048

lora_target: all
lora_rank: 16
lora_alpha: 32
lora_dropout: 0.05

output_dir: output
logging_steps: 10
save_steps: 500
plot_loss: true

per_device_train_batch_size: 2
gradient_accumulation_steps: 4
learning_rate: 5.0e-5
num_train_epochs: 3
lr_scheduler_type: cosine
warmup_ratio: 0.1

quantization_bit: 4
```

```bash
# Run training
llamafactory-cli train config.yaml
```

### Pattern 3: OpenAI Fine-tuning

```python
from openai import OpenAI

client = OpenAI()

def finetune_openai(
    training_file: str,
    base_model: str = "gpt-4o-mini-2024-07-18",
    suffix: str = "custom"
) -> str:
    """Fine-tune OpenAI model."""

    # Upload training file
    file = client.files.create(
        file=open(training_file, "rb"),
        purpose="fine-tune"
    )

    # Create fine-tuning job
    job = client.fine_tuning.jobs.create(
        training_file=file.id,
        model=base_model,
        suffix=suffix,
        hyperparameters={
            "n_epochs": 3,
            "batch_size": "auto",
            "learning_rate_multiplier": "auto"
        }
    )

    # Wait for completion
    while True:
        status = client.fine_tuning.jobs.retrieve(job.id)
        print(f"Status: {status.status}")

        if status.status == "succeeded":
            return status.fine_tuned_model
        elif status.status == "failed":
            raise Exception(f"Fine-tuning failed: {status.error}")

        time.sleep(60)

# Prepare JSONL file
def prepare_openai_jsonl(examples: list, output_path: str):
    """Prepare data in OpenAI fine-tuning format."""
    with open(output_path, "w") as f:
        for ex in examples:
            line = {
                "messages": [
                    {"role": "system", "content": ex.get("system", "")},
                    {"role": "user", "content": ex["instruction"]},
                    {"role": "assistant", "content": ex["output"]}
                ]
            }
            f.write(json.dumps(line) + "\n")
```

### Pattern 4: Evaluation Pipeline

```python
def evaluate_finetuned_model(
    model,
    tokenizer,
    eval_dataset: Dataset,
    metrics: list = ["accuracy", "f1", "bleu"]
) -> dict:
    """Evaluate fine-tuned model."""

    predictions = []
    references = []

    for example in eval_dataset:
        # Generate prediction
        inputs = tokenizer(example["instruction"], return_tensors="pt")
        outputs = model.generate(**inputs, max_new_tokens=256)
        prediction = tokenizer.decode(outputs[0], skip_special_tokens=True)

        predictions.append(prediction)
        references.append(example["output"])

    # Calculate metrics
    results = {}

    if "bleu" in metrics:
        from sacrebleu import corpus_bleu
        results["bleu"] = corpus_bleu(predictions, [references]).score

    if "rouge" in metrics:
        from rouge_score import rouge_scorer
        scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'])
        scores = [scorer.score(ref, pred) for ref, pred in zip(references, predictions)]
        results["rouge1"] = sum(s['rouge1'].fmeasure for s in scores) / len(scores)
        results["rougeL"] = sum(s['rougeL'].fmeasure for s in scores) / len(scores)

    # Compare with base model
    results["improvement"] = compare_with_base(predictions, references)

    return results
```

### Pattern 5: Merge and Deploy

```python
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

def merge_lora_weights(
    base_model_path: str,
    lora_path: str,
    output_path: str
):
    """Merge LoRA weights into base model."""

    # Load base model
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_path,
        torch_dtype=torch.float16,
        device_map="auto"
    )

    # Load LoRA adapter
    model = PeftModel.from_pretrained(base_model, lora_path)

    # Merge weights
    merged_model = model.merge_and_unload()

    # Save merged model
    merged_model.save_pretrained(output_path)
    tokenizer = AutoTokenizer.from_pretrained(base_model_path)
    tokenizer.save_pretrained(output_path)

    print(f"Merged model saved to {output_path}")

def push_to_hub(model_path: str, repo_name: str):
    """Push fine-tuned model to HuggingFace Hub."""
    from huggingface_hub import HfApi

    api = HfApi()
    api.create_repo(repo_name, exist_ok=True)
    api.upload_folder(
        folder_path=model_path,
        repo_id=repo_name,
        commit_message="Upload fine-tuned model"
    )
```

## Anti-patterns

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| Small dataset | Overfitting | Augment data, reduce epochs |
| No validation split | Can't detect overfit | Always hold out 10% |
| Too high LR | Unstable training | Start low, use scheduler |
| Ignoring base quality | Amplifies issues | Curate training data |
| No comparison | Unknown improvement | Benchmark vs base model |

## Tools & References

### Related Skills
- faion-finetuning-skill
- faion-openai-api-skill

### Related Agents
- faion-finetuner-agent

### External Resources
- [Unsloth](https://github.com/unslothai/unsloth) - Fast LoRA
- [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory) - Training toolkit
- [Axolotl](https://github.com/OpenAccess-AI-Collective/axolotl) - Training framework
- [PEFT](https://github.com/huggingface/peft) - Parameter-efficient fine-tuning

## Checklist

- [ ] Collected quality training data
- [ ] Validated and cleaned dataset
- [ ] Split into train/eval sets
- [ ] Selected fine-tuning method (LoRA/QLoRA)
- [ ] Configured hyperparameters
- [ ] Set up logging (W&B, TensorBoard)
- [ ] Ran training with checkpoints
- [ ] Evaluated vs base model
- [ ] Merged weights (if LoRA)
- [ ] Deployed and monitored

---

*Methodology: M-GEN-006 | Category: Multimodal/Generation*
*Related: faion-finetuner-agent, faion-finetuning-skill*
