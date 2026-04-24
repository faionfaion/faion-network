# OpenAI Fine-Tuning Templates

Reusable code templates for fine-tuning workflows.

## Configuration Templates

### Fine-Tuning Config Dataclass

```python
from dataclasses import dataclass, field
from typing import Optional, Literal

@dataclass
class FineTuneConfig:
    """Configuration for OpenAI fine-tuning job."""

    # Model settings
    base_model: str = "gpt-4o-mini-2024-07-18"
    suffix: Optional[str] = None

    # Hyperparameters
    n_epochs: int | Literal["auto"] = "auto"
    batch_size: int | Literal["auto"] = "auto"
    learning_rate_multiplier: float | Literal["auto"] = "auto"

    # DPO settings
    method: Literal["supervised", "dpo"] = "supervised"
    dpo_beta: float = 0.1  # Only for DPO

    # Data settings
    validation_split: float = 0.1
    min_examples: int = 10

    # Job settings
    enable_data_sharing: bool = False  # For inference discount

    def to_api_params(self) -> dict:
        """Convert to OpenAI API parameters."""
        params = {
            "model": self.base_model,
        }

        if self.suffix:
            params["suffix"] = self.suffix

        # Hyperparameters
        hyperparams = {}
        if self.n_epochs != "auto":
            hyperparams["n_epochs"] = self.n_epochs
        if self.batch_size != "auto":
            hyperparams["batch_size"] = self.batch_size
        if self.learning_rate_multiplier != "auto":
            hyperparams["learning_rate_multiplier"] = self.learning_rate_multiplier

        if hyperparams:
            params["hyperparameters"] = hyperparams

        # Method (DPO)
        if self.method == "dpo":
            params["method"] = {
                "type": "dpo",
                "dpo": {
                    "hyperparameters": {
                        "beta": self.dpo_beta
                    }
                }
            }

        return params
```

### Environment Config

```python
import os
from dataclasses import dataclass

@dataclass
class FineTuneEnvConfig:
    """Environment configuration for fine-tuning."""

    openai_api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    organization_id: Optional[str] = field(default_factory=lambda: os.getenv("OPENAI_ORG_ID"))

    # Storage paths
    data_dir: str = "./data"
    output_dir: str = "./output"

    # Monitoring
    poll_interval_seconds: int = 60
    enable_logging: bool = True
    log_file: str = "fine_tuning.log"

    def validate(self) -> bool:
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY not set")
        return True
```

## Pipeline Templates

### Production Fine-Tuning Pipeline

```python
from openai import OpenAI
from dataclasses import dataclass
from typing import List, Dict, Optional
import json
import time
import logging

class FineTuningPipeline:
    """Production fine-tuning pipeline with logging and error handling."""

    def __init__(
        self,
        config: FineTuneConfig,
        env: Optional[FineTuneEnvConfig] = None
    ):
        self.config = config
        self.env = env or FineTuneEnvConfig()
        self.env.validate()

        self.client = OpenAI(api_key=self.env.openai_api_key)
        self.logger = self._setup_logging()

    def _setup_logging(self) -> logging.Logger:
        logger = logging.getLogger("fine_tuning")
        logger.setLevel(logging.INFO)

        if self.env.enable_logging:
            handler = logging.FileHandler(self.env.log_file)
            handler.setFormatter(
                logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            )
            logger.addHandler(handler)

        return logger

    def run(
        self,
        training_data: List[Dict],
        wait_for_completion: bool = True
    ) -> Dict:
        """Execute fine-tuning pipeline."""

        self.logger.info(f"Starting pipeline with {len(training_data)} examples")

        # Validate
        self._validate_data(training_data)

        # Split data
        train_data, val_data = self._split_data(training_data)

        # Upload files
        train_file_id = self._upload_file(train_data, "train")
        val_file_id = self._upload_file(val_data, "val") if val_data else None

        # Create job
        job = self._create_job(train_file_id, val_file_id)

        if wait_for_completion:
            return self._wait_for_completion(job.id)

        return {"job_id": job.id, "status": "started"}

    def _validate_data(self, data: List[Dict]):
        if len(data) < self.config.min_examples:
            raise ValueError(
                f"Need at least {self.config.min_examples} examples, "
                f"got {len(data)}"
            )

        for i, example in enumerate(data):
            if "messages" not in example:
                raise ValueError(f"Example {i}: Missing 'messages' key")

    def _split_data(self, data: List[Dict]) -> tuple:
        if self.config.validation_split <= 0:
            return data, None

        split_idx = int(len(data) * (1 - self.config.validation_split))
        return data[:split_idx], data[split_idx:]

    def _upload_file(self, data: List[Dict], name: str) -> str:
        filepath = f"{self.env.data_dir}/{name}_data.jsonl"

        os.makedirs(self.env.data_dir, exist_ok=True)

        with open(filepath, 'w') as f:
            for example in data:
                f.write(json.dumps(example) + "\n")

        with open(filepath, "rb") as f:
            response = self.client.files.create(file=f, purpose="fine-tune")

        self.logger.info(f"Uploaded {name} file: {response.id}")
        return response.id

    def _create_job(self, train_file_id: str, val_file_id: Optional[str]):
        params = self.config.to_api_params()
        params["training_file"] = train_file_id

        if val_file_id:
            params["validation_file"] = val_file_id

        job = self.client.fine_tuning.jobs.create(**params)
        self.logger.info(f"Created job: {job.id}")

        return job

    def _wait_for_completion(self, job_id: str) -> Dict:
        while True:
            job = self.client.fine_tuning.jobs.retrieve(job_id)

            self.logger.info(f"Job status: {job.status}")

            if job.status == "succeeded":
                self.logger.info(f"Model ready: {job.fine_tuned_model}")
                return {
                    "status": "succeeded",
                    "model": job.fine_tuned_model,
                    "trained_tokens": job.trained_tokens
                }

            if job.status in ["failed", "cancelled"]:
                self.logger.error(f"Job failed: {job.error}")
                return {"status": job.status, "error": str(job.error)}

            time.sleep(self.env.poll_interval_seconds)
```

### Job Manager

```python
from openai import OpenAI
from typing import List, Optional
from datetime import datetime

class FineTuneJobManager:
    """Manage multiple fine-tuning jobs."""

    def __init__(self):
        self.client = OpenAI()

    def list_jobs(
        self,
        limit: int = 10,
        after: Optional[str] = None
    ) -> List[dict]:
        """List fine-tuning jobs."""
        jobs = self.client.fine_tuning.jobs.list(limit=limit, after=after)

        return [
            {
                "id": job.id,
                "model": job.model,
                "status": job.status,
                "fine_tuned_model": job.fine_tuned_model,
                "created_at": datetime.fromtimestamp(job.created_at),
                "trained_tokens": job.trained_tokens
            }
            for job in jobs.data
        ]

    def get_job(self, job_id: str) -> dict:
        """Get job details."""
        job = self.client.fine_tuning.jobs.retrieve(job_id)

        return {
            "id": job.id,
            "model": job.model,
            "status": job.status,
            "fine_tuned_model": job.fine_tuned_model,
            "created_at": datetime.fromtimestamp(job.created_at),
            "finished_at": datetime.fromtimestamp(job.finished_at) if job.finished_at else None,
            "trained_tokens": job.trained_tokens,
            "error": str(job.error) if job.error else None,
            "hyperparameters": {
                "n_epochs": job.hyperparameters.n_epochs,
                "batch_size": job.hyperparameters.batch_size,
                "learning_rate_multiplier": job.hyperparameters.learning_rate_multiplier
            }
        }

    def get_events(self, job_id: str, limit: int = 20) -> List[dict]:
        """Get job events."""
        events = self.client.fine_tuning.jobs.list_events(job_id, limit=limit)

        return [
            {
                "created_at": datetime.fromtimestamp(event.created_at),
                "level": event.level,
                "message": event.message,
                "data": event.data
            }
            for event in events.data
        ]

    def cancel_job(self, job_id: str) -> dict:
        """Cancel a running job."""
        job = self.client.fine_tuning.jobs.cancel(job_id)
        return {"id": job.id, "status": job.status}

    def list_models(self) -> List[str]:
        """List all fine-tuned models."""
        models = self.client.models.list()

        return [
            model.id for model in models.data
            if model.id.startswith("ft:")
        ]

    def delete_model(self, model_id: str) -> dict:
        """Delete a fine-tuned model."""
        result = self.client.models.delete(model_id)
        return {"id": result.id, "deleted": result.deleted}
```

## Data Templates

### JSONL Builder

```python
from typing import List, Dict, Optional
import json

class TrainingDataBuilder:
    """Build training data in correct format."""

    def __init__(self, system_prompt: Optional[str] = None):
        self.system_prompt = system_prompt
        self.examples: List[Dict] = []

    def add_example(
        self,
        user_message: str,
        assistant_response: str,
        system_prompt: Optional[str] = None
    ) -> "TrainingDataBuilder":
        """Add single-turn example."""

        messages = []

        sys_prompt = system_prompt or self.system_prompt
        if sys_prompt:
            messages.append({"role": "system", "content": sys_prompt})

        messages.extend([
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": assistant_response}
        ])

        self.examples.append({"messages": messages})
        return self

    def add_conversation(
        self,
        turns: List[tuple],  # [(user, assistant), ...]
        system_prompt: Optional[str] = None
    ) -> "TrainingDataBuilder":
        """Add multi-turn conversation."""

        messages = []

        sys_prompt = system_prompt or self.system_prompt
        if sys_prompt:
            messages.append({"role": "system", "content": sys_prompt})

        for user_msg, assistant_msg in turns:
            messages.append({"role": "user", "content": user_msg})
            messages.append({"role": "assistant", "content": assistant_msg})

        self.examples.append({"messages": messages})
        return self

    def add_dpo_example(
        self,
        user_message: str,
        preferred: str,
        non_preferred: str
    ) -> "TrainingDataBuilder":
        """Add DPO preference pair."""

        self.examples.append({
            "input": [{"role": "user", "content": user_message}],
            "preferred_output": [{"role": "assistant", "content": preferred}],
            "non_preferred_output": [{"role": "assistant", "content": non_preferred}]
        })
        return self

    def save(self, filepath: str):
        """Save to JSONL file."""
        with open(filepath, 'w') as f:
            for example in self.examples:
                f.write(json.dumps(example) + "\n")

    def get_examples(self) -> List[Dict]:
        return self.examples.copy()

# Usage
builder = TrainingDataBuilder(system_prompt="You are a helpful assistant.")
builder.add_example("Hello", "Hi! How can I help you today?")
builder.add_example("What's 2+2?", "2 + 2 equals 4.")
builder.save("training.jsonl")
```

### Data Validator

```python
import json
from typing import List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class ValidationResult:
    valid: bool
    errors: List[str]
    warnings: List[str]
    stats: dict

class TrainingDataValidator:
    """Validate training data format and quality."""

    def __init__(
        self,
        min_examples: int = 10,
        max_tokens_per_example: int = 4096
    ):
        self.min_examples = min_examples
        self.max_tokens = max_tokens_per_example

    def validate_file(self, filepath: str) -> ValidationResult:
        """Validate JSONL file."""
        errors = []
        warnings = []

        examples = []
        with open(filepath, 'r') as f:
            for i, line in enumerate(f, 1):
                try:
                    data = json.loads(line)
                    examples.append(data)
                except json.JSONDecodeError as e:
                    errors.append(f"Line {i}: Invalid JSON - {e}")

        # Check minimum examples
        if len(examples) < self.min_examples:
            errors.append(
                f"Insufficient examples: {len(examples)} < {self.min_examples}"
            )

        # Validate each example
        for i, example in enumerate(examples, 1):
            example_errors = self._validate_example(example, i)
            errors.extend(example_errors)

        # Quality warnings
        quality_warnings = self._check_quality(examples)
        warnings.extend(quality_warnings)

        # Stats
        stats = self._calculate_stats(examples)

        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            stats=stats
        )

    def _validate_example(self, example: dict, index: int) -> List[str]:
        errors = []

        # SFT format
        if "messages" in example:
            messages = example["messages"]

            if not isinstance(messages, list):
                errors.append(f"Example {index}: 'messages' must be list")
                return errors

            roles = [m.get("role") for m in messages]

            if "assistant" not in roles:
                errors.append(f"Example {index}: No assistant message")
            if "user" not in roles:
                errors.append(f"Example {index}: No user message")

            for j, msg in enumerate(messages):
                if "role" not in msg:
                    errors.append(f"Example {index}, msg {j}: Missing 'role'")
                if "content" not in msg:
                    errors.append(f"Example {index}, msg {j}: Missing 'content'")

        # DPO format
        elif "input" in example:
            required = ["input", "preferred_output", "non_preferred_output"]
            for key in required:
                if key not in example:
                    errors.append(f"Example {index}: Missing '{key}'")

        else:
            errors.append(f"Example {index}: Unknown format")

        return errors

    def _check_quality(self, examples: List[dict]) -> List[str]:
        warnings = []

        # Check for duplicates
        seen = set()
        for i, ex in enumerate(examples):
            key = json.dumps(ex, sort_keys=True)
            if key in seen:
                warnings.append(f"Duplicate example at index {i}")
            seen.add(key)

        # Check balance (if applicable)
        # Add domain-specific quality checks here

        return warnings

    def _calculate_stats(self, examples: List[dict]) -> dict:
        return {
            "total_examples": len(examples),
            "format": "sft" if examples and "messages" in examples[0] else "dpo"
        }
```

## Evaluation Templates

### Evaluation Runner

```python
from openai import OpenAI
from typing import List, Dict, Callable
from dataclasses import dataclass
import json

@dataclass
class EvalResult:
    score: float
    details: Dict
    examples: List[Dict]

class ModelEvaluator:
    """Evaluate fine-tuned model performance."""

    def __init__(
        self,
        model_name: str,
        evaluator_model: str = "gpt-4o"
    ):
        self.client = OpenAI()
        self.model_name = model_name
        self.evaluator_model = evaluator_model

    def evaluate(
        self,
        test_data: List[Dict],
        eval_prompt_template: str
    ) -> EvalResult:
        """Run evaluation on test data."""

        scores = []
        examples = []

        for test_case in test_data:
            # Get model response
            response = self._get_model_response(test_case)

            # Evaluate
            score, explanation = self._evaluate_response(
                test_case, response, eval_prompt_template
            )

            scores.append(score)
            examples.append({
                "input": test_case,
                "output": response,
                "score": score,
                "explanation": explanation
            })

        avg_score = sum(scores) / len(scores) if scores else 0

        return EvalResult(
            score=avg_score,
            details={
                "total": len(test_data),
                "avg_score": avg_score,
                "min_score": min(scores) if scores else 0,
                "max_score": max(scores) if scores else 0,
                "distribution": {i: scores.count(i) for i in range(1, 6)}
            },
            examples=examples
        )

    def _get_model_response(self, test_case: Dict) -> str:
        messages = [
            m for m in test_case["messages"]
            if m["role"] != "assistant"
        ]

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=0
        )

        return response.choices[0].message.content

    def _evaluate_response(
        self,
        test_case: Dict,
        response: str,
        template: str
    ) -> Tuple[int, str]:
        # Get expected response
        expected = next(
            (m["content"] for m in test_case["messages"] if m["role"] == "assistant"),
            ""
        )

        # Get user input
        user_input = next(
            (m["content"] for m in test_case["messages"] if m["role"] == "user"),
            ""
        )

        eval_prompt = template.format(
            input=user_input,
            expected=expected,
            actual=response
        )

        eval_response = self.client.chat.completions.create(
            model=self.evaluator_model,
            messages=[{"role": "user", "content": eval_prompt}],
            response_format={"type": "json_object"},
            temperature=0
        )

        result = json.loads(eval_response.choices[0].message.content)
        return result["score"], result.get("explanation", "")
```

## CLI Template

### Fine-Tuning CLI

```python
#!/usr/bin/env python3
"""CLI for OpenAI fine-tuning operations."""

import argparse
import json
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="OpenAI Fine-Tuning CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Upload command
    upload_parser = subparsers.add_parser("upload", help="Upload training file")
    upload_parser.add_argument("file", type=Path, help="JSONL file path")
    upload_parser.add_argument("--validate", action="store_true", help="Validate before upload")

    # Train command
    train_parser = subparsers.add_parser("train", help="Start fine-tuning")
    train_parser.add_argument("--training-file", required=True, help="Training file ID")
    train_parser.add_argument("--validation-file", help="Validation file ID")
    train_parser.add_argument("--model", default="gpt-4o-mini-2024-07-18")
    train_parser.add_argument("--suffix", help="Model suffix")
    train_parser.add_argument("--epochs", type=int, default=3)
    train_parser.add_argument("--method", choices=["supervised", "dpo"], default="supervised")

    # Status command
    status_parser = subparsers.add_parser("status", help="Check job status")
    status_parser.add_argument("job_id", help="Job ID")

    # List command
    list_parser = subparsers.add_parser("list", help="List jobs")
    list_parser.add_argument("--limit", type=int, default=10)

    # Cancel command
    cancel_parser = subparsers.add_parser("cancel", help="Cancel job")
    cancel_parser.add_argument("job_id", help="Job ID")

    # Evaluate command
    eval_parser = subparsers.add_parser("evaluate", help="Evaluate model")
    eval_parser.add_argument("--model", required=True, help="Model to evaluate")
    eval_parser.add_argument("--test-file", required=True, type=Path)
    eval_parser.add_argument("--output", type=Path, help="Results output file")

    args = parser.parse_args()

    # Route to handler
    if args.command == "upload":
        handle_upload(args)
    elif args.command == "train":
        handle_train(args)
    elif args.command == "status":
        handle_status(args)
    elif args.command == "list":
        handle_list(args)
    elif args.command == "cancel":
        handle_cancel(args)
    elif args.command == "evaluate":
        handle_evaluate(args)

def handle_upload(args):
    from openai import OpenAI
    client = OpenAI()

    if args.validate:
        validator = TrainingDataValidator()
        result = validator.validate_file(args.file)
        if not result.valid:
            print("Validation failed:")
            for error in result.errors:
                print(f"  - {error}")
            return

    with open(args.file, "rb") as f:
        response = client.files.create(file=f, purpose="fine-tune")

    print(f"Uploaded: {response.id}")

def handle_train(args):
    from openai import OpenAI
    client = OpenAI()

    params = {
        "training_file": args.training_file,
        "model": args.model,
        "hyperparameters": {"n_epochs": args.epochs}
    }

    if args.validation_file:
        params["validation_file"] = args.validation_file
    if args.suffix:
        params["suffix"] = args.suffix
    if args.method == "dpo":
        params["method"] = {"type": "dpo", "dpo": {"hyperparameters": {"beta": 0.1}}}

    job = client.fine_tuning.jobs.create(**params)
    print(f"Job started: {job.id}")

def handle_status(args):
    from openai import OpenAI
    client = OpenAI()

    job = client.fine_tuning.jobs.retrieve(args.job_id)
    print(f"Status: {job.status}")
    print(f"Model: {job.fine_tuned_model or 'Not ready'}")

    if job.error:
        print(f"Error: {job.error}")

def handle_list(args):
    from openai import OpenAI
    client = OpenAI()

    jobs = client.fine_tuning.jobs.list(limit=args.limit)
    for job in jobs.data:
        print(f"{job.id} | {job.status} | {job.model} | {job.fine_tuned_model or '-'}")

def handle_cancel(args):
    from openai import OpenAI
    client = OpenAI()

    job = client.fine_tuning.jobs.cancel(args.job_id)
    print(f"Cancelled: {job.id}")

def handle_evaluate(args):
    # Load test data
    test_data = []
    with open(args.test_file, 'r') as f:
        for line in f:
            test_data.append(json.loads(line))

    evaluator = ModelEvaluator(args.model)
    result = evaluator.evaluate(test_data, EVAL_PROMPT_TEMPLATE)

    print(f"Average score: {result.score:.2f}")
    print(f"Details: {result.details}")

    if args.output:
        with open(args.output, 'w') as f:
            json.dump({
                "score": result.score,
                "details": result.details,
                "examples": result.examples
            }, f, indent=2)

EVAL_PROMPT_TEMPLATE = """Compare the actual response to the expected response.

Input: {input}

Expected: {expected}

Actual: {actual}

Rate 1-5 and explain. Return JSON: {{"score": N, "explanation": "..."}}"""

if __name__ == "__main__":
    main()
```

## Usage

Copy and adapt these templates for your fine-tuning projects. Key files:

1. **Config** - Customize `FineTuneConfig` for your needs
2. **Pipeline** - Use `FineTuningPipeline` for end-to-end workflow
3. **Data** - Use `TrainingDataBuilder` to construct training data
4. **Validation** - Use `TrainingDataValidator` before uploading
5. **Evaluation** - Use `ModelEvaluator` to assess quality
6. **CLI** - Adapt CLI template for command-line operations
