# Fine-tuning Templates

Production-ready templates for LoRA/QLoRA/DoRA fine-tuning pipelines.

## 1. Production Pipeline Class

```python
"""
Production LoRA Fine-tuning Pipeline
=====================================

Usage:
    from lora_pipeline import LoRATrainingPipeline, LoRAConfig

    config = LoRAConfig(
        base_model="meta-llama/Llama-3.1-8B-Instruct",
        rank=16,
        use_4bit=True,
    )

    pipeline = LoRATrainingPipeline(config)
    pipeline.prepare_model()
    result = pipeline.train(train_data, val_data, output_dir="./output")
"""

from dataclasses import dataclass, field
from typing import Optional
import logging
import os

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
)
from peft import (
    LoraConfig,
    get_peft_model,
    prepare_model_for_kbit_training,
    TaskType,
    PeftModel,
)
from datasets import Dataset

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class LoRAConfig:
    """Configuration for LoRA fine-tuning."""

    # Model
    base_model: str

    # LoRA hyperparameters
    rank: int = 16
    alpha: int = 32
    dropout: float = 0.05
    target_modules: list[str] = field(default_factory=lambda: [
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj"
    ])

    # Quantization
    use_4bit: bool = True
    compute_dtype: str = "bfloat16"

    # LoRA variants
    use_rslora: bool = False
    use_dora: bool = False

    # Training
    max_length: int = 2048
    batch_size: int = 4
    grad_accum_steps: int = 4
    num_epochs: int = 3
    learning_rate: float = 2e-4
    warmup_ratio: float = 0.03

    # Hardware
    device_map: str = "auto"

    def __post_init__(self):
        # Alpha should be 2x rank by default
        if self.alpha == 32 and self.rank != 16:
            self.alpha = self.rank * 2


class LoRATrainingPipeline:
    """Production LoRA fine-tuning pipeline."""

    def __init__(self, config: LoRAConfig):
        self.config = config
        self.model = None
        self.tokenizer = None
        self.trainer = None

    def prepare_model(self) -> None:
        """Load and prepare model for training."""
        logger.info(f"Loading model: {self.config.base_model}")

        # Determine compute dtype
        dtype_map = {
            "float16": torch.float16,
            "bfloat16": torch.bfloat16,
            "float32": torch.float32,
        }
        compute_dtype = dtype_map.get(self.config.compute_dtype, torch.bfloat16)

        # Load with or without quantization
        if self.config.use_4bit:
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=compute_dtype,
                bnb_4bit_use_double_quant=True,
            )
            self.model = AutoModelForCausalLM.from_pretrained(
                self.config.base_model,
                quantization_config=bnb_config,
                device_map=self.config.device_map,
                trust_remote_code=True,
            )
            self.model = prepare_model_for_kbit_training(self.model)
        else:
            self.model = AutoModelForCausalLM.from_pretrained(
                self.config.base_model,
                torch_dtype=compute_dtype,
                device_map=self.config.device_map,
                trust_remote_code=True,
            )

        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(self.config.base_model)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.tokenizer.padding_side = "right"

        # Apply LoRA
        lora_config = LoraConfig(
            r=self.config.rank,
            lora_alpha=self.config.alpha,
            lora_dropout=self.config.dropout,
            target_modules=self.config.target_modules,
            bias="none",
            task_type=TaskType.CAUSAL_LM,
            use_rslora=self.config.use_rslora,
            use_dora=self.config.use_dora,
        )

        self.model = get_peft_model(self.model, lora_config)
        self.model.print_trainable_parameters()

    def _format_example(self, example: dict) -> str:
        """Format a single training example."""
        if example.get("input"):
            return f"""### Instruction:
{example['instruction']}

### Input:
{example['input']}

### Response:
{example['output']}"""
        return f"""### Instruction:
{example['instruction']}

### Response:
{example['output']}"""

    def _prepare_dataset(self, data: list[dict]) -> Dataset:
        """Convert raw data to tokenized dataset."""
        def tokenize(example):
            text = self._format_example(example)
            tokens = self.tokenizer(
                text,
                truncation=True,
                max_length=self.config.max_length,
                padding="max_length",
            )
            tokens["labels"] = tokens["input_ids"].copy()
            return tokens

        dataset = Dataset.from_list(data)
        return dataset.map(tokenize, remove_columns=dataset.column_names)

    def train(
        self,
        train_data: list[dict],
        val_data: Optional[list[dict]] = None,
        output_dir: str = "./lora-output",
    ) -> dict:
        """Run training and return results."""
        if self.model is None:
            raise RuntimeError("Call prepare_model() first")

        logger.info(f"Preparing {len(train_data)} training examples")
        train_dataset = self._prepare_dataset(train_data)

        val_dataset = None
        if val_data:
            logger.info(f"Preparing {len(val_data)} validation examples")
            val_dataset = self._prepare_dataset(val_data)

        # Training arguments
        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=self.config.num_epochs,
            per_device_train_batch_size=self.config.batch_size,
            gradient_accumulation_steps=self.config.grad_accum_steps,
            learning_rate=self.config.learning_rate,
            warmup_ratio=self.config.warmup_ratio,
            lr_scheduler_type="cosine",
            fp16=self.config.compute_dtype == "float16",
            bf16=self.config.compute_dtype == "bfloat16",
            logging_steps=10,
            save_strategy="epoch",
            evaluation_strategy="epoch" if val_dataset else "no",
            gradient_checkpointing=True,
            optim="paged_adamw_8bit" if self.config.use_4bit else "adamw_torch",
            max_grad_norm=0.3,
        )

        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False,
        )

        self.trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
            data_collator=data_collator,
        )

        logger.info("Starting training...")
        self.trainer.train()

        # Save adapter
        self.model.save_pretrained(output_dir)
        self.tokenizer.save_pretrained(output_dir)

        logger.info(f"Adapter saved to {output_dir}")

        return {
            "status": "completed",
            "output_dir": output_dir,
            "train_loss": self.trainer.state.log_history[-1].get("train_loss"),
            "eval_loss": self.trainer.state.log_history[-1].get("eval_loss"),
        }

    def generate(self, prompt: str, max_new_tokens: int = 256) -> str:
        """Generate text with the fine-tuned model."""
        if self.model is None:
            raise RuntimeError("Call prepare_model() first")

        self.model.eval()
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=0.7,
                top_p=0.9,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
            )

        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    def merge_and_save(self, output_dir: str) -> None:
        """Merge LoRA weights into base model and save."""
        if self.model is None:
            raise RuntimeError("No model loaded")

        logger.info("Merging LoRA weights into base model...")
        merged = self.model.merge_and_unload()
        merged.save_pretrained(output_dir)
        self.tokenizer.save_pretrained(output_dir)
        logger.info(f"Merged model saved to {output_dir}")

    @classmethod
    def from_adapter(
        cls,
        base_model: str,
        adapter_path: str,
        use_4bit: bool = False,
    ) -> "LoRATrainingPipeline":
        """Load a trained adapter for inference."""
        config = LoRAConfig(base_model=base_model, use_4bit=use_4bit)
        pipeline = cls(config)

        # Load base model
        if use_4bit:
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16,
            )
            base = AutoModelForCausalLM.from_pretrained(
                base_model,
                quantization_config=bnb_config,
                device_map="auto",
            )
        else:
            base = AutoModelForCausalLM.from_pretrained(
                base_model,
                torch_dtype=torch.bfloat16,
                device_map="auto",
            )

        # Load adapter
        pipeline.model = PeftModel.from_pretrained(base, adapter_path)
        pipeline.tokenizer = AutoTokenizer.from_pretrained(adapter_path)

        return pipeline
```

## 2. Config Templates

### Minimal Config (Consumer GPU)

```python
# For RTX 3090/4090 (24GB) - Small models
minimal_config = LoRAConfig(
    base_model="meta-llama/Llama-3.2-3B-Instruct",
    rank=8,
    alpha=16,
    dropout=0.05,
    target_modules=["q_proj", "v_proj"],
    use_4bit=True,
    batch_size=2,
    grad_accum_steps=8,
    max_length=1024,
)
```

### Standard Config (Cloud GPU)

```python
# For A100 40GB/L40S - Medium models
standard_config = LoRAConfig(
    base_model="meta-llama/Llama-3.1-8B-Instruct",
    rank=16,
    alpha=32,
    dropout=0.05,
    target_modules=[
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj"
    ],
    use_4bit=True,
    batch_size=4,
    grad_accum_steps=4,
    max_length=2048,
)
```

### Maximum Quality Config

```python
# For A100 80GB/H100 - Maximum quality
quality_config = LoRAConfig(
    base_model="meta-llama/Llama-3.1-70B-Instruct",
    rank=64,
    alpha=128,
    dropout=0.1,
    target_modules=[
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj"
    ],
    use_4bit=True,
    use_rslora=True,  # For high rank
    use_dora=True,    # Weight decomposition
    batch_size=1,
    grad_accum_steps=16,
    max_length=4096,
    learning_rate=1e-4,
)
```

## 3. Dataset Templates

### Instruction Dataset

```python
"""Template for instruction-following datasets."""

INSTRUCTION_TEMPLATE = {
    "required_fields": ["instruction", "output"],
    "optional_fields": ["input", "system"],
    "format": """### Instruction:
{instruction}

### Input:
{input}

### Response:
{output}""",
}

def validate_instruction_dataset(data: list[dict]) -> list[str]:
    """Validate dataset format and return any errors."""
    errors = []
    for i, example in enumerate(data):
        if "instruction" not in example:
            errors.append(f"Example {i}: missing 'instruction' field")
        if "output" not in example:
            errors.append(f"Example {i}: missing 'output' field")
        if not example.get("instruction", "").strip():
            errors.append(f"Example {i}: empty instruction")
        if not example.get("output", "").strip():
            errors.append(f"Example {i}: empty output")
    return errors
```

### Chat Dataset

```python
"""Template for multi-turn chat datasets."""

CHAT_TEMPLATE = {
    "required_fields": ["messages"],
    "message_format": {"role": "user|assistant|system", "content": "string"},
}

def validate_chat_dataset(data: list[dict]) -> list[str]:
    """Validate chat dataset format."""
    errors = []
    valid_roles = {"user", "assistant", "system"}

    for i, example in enumerate(data):
        if "messages" not in example:
            errors.append(f"Example {i}: missing 'messages' field")
            continue

        messages = example["messages"]
        if not isinstance(messages, list) or len(messages) < 2:
            errors.append(f"Example {i}: messages must be a list with at least 2 turns")
            continue

        for j, msg in enumerate(messages):
            if "role" not in msg or "content" not in msg:
                errors.append(f"Example {i}, message {j}: missing role or content")
            elif msg["role"] not in valid_roles:
                errors.append(f"Example {i}, message {j}: invalid role '{msg['role']}'")

    return errors

def format_chat_for_llama3(messages: list[dict], tokenizer) -> str:
    """Format chat messages for Llama 3."""
    return tokenizer.apply_chat_template(messages, tokenize=False)
```

### Code Dataset

```python
"""Template for code generation datasets."""

CODE_TEMPLATE = {
    "required_fields": ["prompt", "code"],
    "optional_fields": ["language", "explanation"],
    "format": """### Task:
{prompt}

### Language:
{language}

### Solution:
```{language}
{code}
```

### Explanation:
{explanation}""",
}

def validate_code_dataset(data: list[dict]) -> list[str]:
    """Validate code dataset format."""
    errors = []
    for i, example in enumerate(data):
        if "prompt" not in example:
            errors.append(f"Example {i}: missing 'prompt' field")
        if "code" not in example:
            errors.append(f"Example {i}: missing 'code' field")
    return errors
```

## 4. Evaluation Template

```python
"""Template for evaluating fine-tuned models."""

import json
from typing import Callable
from tqdm import tqdm


def evaluate_model(
    model,
    tokenizer,
    test_data: list[dict],
    format_prompt: Callable[[dict], str],
    extract_response: Callable[[str], str],
    score_response: Callable[[str, str], float],
    max_new_tokens: int = 256,
) -> dict:
    """
    Evaluate fine-tuned model on test data.

    Args:
        model: The model to evaluate
        tokenizer: The tokenizer
        test_data: List of test examples
        format_prompt: Function to format example into prompt
        extract_response: Function to extract model response from full output
        score_response: Function to score response (0-1) given prediction and reference
        max_new_tokens: Maximum tokens to generate

    Returns:
        Dictionary with evaluation results
    """
    model.eval()
    results = []
    total_score = 0.0

    for example in tqdm(test_data, desc="Evaluating"):
        prompt = format_prompt(example)
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=0.1,  # Low temperature for evaluation
                do_sample=False,
                pad_token_id=tokenizer.eos_token_id,
            )

        full_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
        response = extract_response(full_output)
        reference = example.get("output", example.get("expected", ""))

        score = score_response(response, reference)
        total_score += score

        results.append({
            "prompt": prompt[:200] + "...",
            "response": response[:200] + "...",
            "reference": reference[:200] + "...",
            "score": score,
        })

    return {
        "average_score": total_score / len(test_data),
        "total_examples": len(test_data),
        "results": results,
    }


# Example usage:
def exact_match_scorer(prediction: str, reference: str) -> float:
    """Score based on exact match."""
    return 1.0 if prediction.strip().lower() == reference.strip().lower() else 0.0


def contains_scorer(prediction: str, reference: str) -> float:
    """Score based on whether prediction contains reference."""
    return 1.0 if reference.strip().lower() in prediction.strip().lower() else 0.0
```

## 5. Training Script Template

```python
#!/usr/bin/env python3
"""
Fine-tune LLM with LoRA
========================

Usage:
    python train.py --config config.json --data data.json --output ./output

Example config.json:
{
    "base_model": "meta-llama/Llama-3.1-8B-Instruct",
    "rank": 16,
    "alpha": 32,
    "use_4bit": true,
    "num_epochs": 3,
    "learning_rate": 0.0002
}
"""

import argparse
import json
import logging
import os
import sys

import torch

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lora_pipeline import LoRATrainingPipeline, LoRAConfig

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Fine-tune LLM with LoRA")
    parser.add_argument("--config", required=True, help="Path to config JSON")
    parser.add_argument("--data", required=True, help="Path to training data JSON")
    parser.add_argument("--val-data", help="Path to validation data JSON (optional)")
    parser.add_argument("--output", default="./lora-output", help="Output directory")
    parser.add_argument("--merge", action="store_true", help="Merge adapter after training")
    args = parser.parse_args()

    # Load config
    logger.info(f"Loading config from {args.config}")
    with open(args.config) as f:
        config_dict = json.load(f)
    config = LoRAConfig(**config_dict)

    # Load data
    logger.info(f"Loading training data from {args.data}")
    with open(args.data) as f:
        train_data = json.load(f)
    logger.info(f"Loaded {len(train_data)} training examples")

    val_data = None
    if args.val_data:
        logger.info(f"Loading validation data from {args.val_data}")
        with open(args.val_data) as f:
            val_data = json.load(f)
        logger.info(f"Loaded {len(val_data)} validation examples")

    # Train
    pipeline = LoRATrainingPipeline(config)
    pipeline.prepare_model()

    result = pipeline.train(train_data, val_data, args.output)
    logger.info(f"Training completed: {result}")

    # Optionally merge
    if args.merge:
        merge_dir = args.output + "-merged"
        pipeline.merge_and_save(merge_dir)

    logger.info("Done!")


if __name__ == "__main__":
    main()
```

## 6. Docker Template

```dockerfile
# Dockerfile for LoRA fine-tuning
FROM nvidia/cuda:12.1-devel-ubuntu22.04

# Install Python
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install PyTorch and dependencies
RUN pip3 install --no-cache-dir \
    torch==2.1.0 \
    transformers>=4.36.0 \
    peft>=0.7.0 \
    trl>=0.7.0 \
    bitsandbytes>=0.41.0 \
    accelerate>=0.25.0 \
    datasets>=2.15.0 \
    wandb \
    scipy

# Optional: Install Flash Attention
RUN pip3 install flash-attn --no-build-isolation

WORKDIR /app

# Copy training scripts
COPY *.py ./
COPY configs/ ./configs/

ENTRYPOINT ["python3", "train.py"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  lora-trainer:
    build: .
    runtime: nvidia
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
      - WANDB_API_KEY=${WANDB_API_KEY}
      - HF_TOKEN=${HF_TOKEN}
    volumes:
      - ./data:/data:ro
      - ./output:/output
      - ~/.cache/huggingface:/root/.cache/huggingface
    command: ["--config", "/data/config.json", "--data", "/data/train.json", "--output", "/output"]
```
