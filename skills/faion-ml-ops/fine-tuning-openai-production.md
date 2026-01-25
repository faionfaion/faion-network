---
id: fine-tuning-openai-production
name: "Fine-tuning OpenAI - Production"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# Fine-tuning OpenAI - Production

Training, evaluation, and production deployment of fine-tuned OpenAI models.

## Upload and Start Fine-tuning

```python
from openai import OpenAI
import time

client = OpenAI()

def upload_training_file(filepath: str) -> str:
    """Upload training file to OpenAI."""
    with open(filepath, "rb") as f:
        response = client.files.create(
            file=f,
            purpose="fine-tune"
        )
    return response.id

def create_fine_tune_job(
    training_file_id: str,
    model: str = "gpt-3.5-turbo-0125",
    suffix: str = None,
    n_epochs: int = 3,
    validation_file_id: str = None
) -> str:
    """Start a fine-tuning job."""
    params = {
        "training_file": training_file_id,
        "model": model,
        "hyperparameters": {
            "n_epochs": n_epochs
        }
    }

    if suffix:
        params["suffix"] = suffix

    if validation_file_id:
        params["validation_file"] = validation_file_id

    response = client.fine_tuning.jobs.create(**params)
    return response.id

def monitor_fine_tune_job(job_id: str) -> dict:
    """Monitor fine-tuning job status."""
    while True:
        job = client.fine_tuning.jobs.retrieve(job_id)

        print(f"Status: {job.status}")

        if job.status == "succeeded":
            return {
                "status": "succeeded",
                "model": job.fine_tuned_model,
                "trained_tokens": job.trained_tokens
            }
        elif job.status == "failed":
            return {
                "status": "failed",
                "error": job.error
            }

        # Print recent events
        events = client.fine_tuning.jobs.list_events(job_id, limit=5)
        for event in events.data:
            print(f"  {event.created_at}: {event.message}")

        time.sleep(60)  # Check every minute

# Full workflow
file_id = upload_training_file("training_data.jsonl")
print(f"Uploaded file: {file_id}")

job_id = create_fine_tune_job(
    training_file_id=file_id,
    model="gpt-3.5-turbo-0125",
    suffix="customer-support",
    n_epochs=3
)
print(f"Started job: {job_id}")

result = monitor_fine_tune_job(job_id)
print(f"Fine-tuned model: {result.get('model')}")
```

## Using Fine-tuned Model

```python
def use_fine_tuned_model(
    model_name: str,
    messages: List[Dict],
    temperature: float = 0.7
) -> str:
    """Use fine-tuned model for inference."""
    response = client.chat.completions.create(
        model=model_name,  # e.g., "ft:gpt-3.5-turbo-0125:org::abc123"
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message.content

# Example usage
fine_tuned_model = "ft:gpt-3.5-turbo-0125:my-org::abc123"

response = use_fine_tuned_model(
    model_name=fine_tuned_model,
    messages=[
        {"role": "system", "content": "You are a helpful customer support agent for TechCorp."},
        {"role": "user", "content": "How do I cancel my subscription?"}
    ]
)
print(response)
```

## Hyperparameter Tuning

```python
def create_fine_tune_with_hyperparameters(
    training_file_id: str,
    model: str = "gpt-3.5-turbo-0125",
    n_epochs: int = "auto",  # Can be 1-50 or "auto"
    batch_size: int = "auto",  # Can be 1-256 or "auto"
    learning_rate_multiplier: float = "auto"  # Can be 0.1-2.0 or "auto"
) -> str:
    """Create fine-tuning job with custom hyperparameters."""
    hyperparameters = {}

    if n_epochs != "auto":
        hyperparameters["n_epochs"] = n_epochs
    if batch_size != "auto":
        hyperparameters["batch_size"] = batch_size
    if learning_rate_multiplier != "auto":
        hyperparameters["learning_rate_multiplier"] = learning_rate_multiplier

    response = client.fine_tuning.jobs.create(
        training_file=training_file_id,
        model=model,
        hyperparameters=hyperparameters if hyperparameters else None
    )

    return response.id

# Guidelines:
# - n_epochs: Start with 3, increase if model underperforms
# - batch_size: Larger = faster but may reduce quality
# - learning_rate_multiplier: Increase for harder tasks, decrease if overfitting
```

## Evaluation

```python
from typing import List, Tuple
import json

def evaluate_fine_tuned_model(
    model_name: str,
    test_data: List[Dict],
    evaluator_model: str = "gpt-4o"
) -> Dict:
    """Evaluate fine-tuned model quality."""
    results = {
        "total": len(test_data),
        "scores": [],
        "examples": []
    }

    for example in test_data:
        user_message = next(
            m["content"] for m in example["messages"]
            if m["role"] == "user"
        )
        expected = next(
            m["content"] for m in example["messages"]
            if m["role"] == "assistant"
        )

        # Get model response
        actual = use_fine_tuned_model(
            model_name,
            [m for m in example["messages"] if m["role"] != "assistant"]
        )

        # Evaluate with GPT-4
        eval_prompt = f"""Compare these two responses and rate similarity/quality.

Expected response:
{expected}

Actual response:
{actual}

Rate from 1-5 where:
5: Equivalent or better
4: Minor differences, same quality
3: Noticeable differences but acceptable
2: Significant quality gap
1: Wrong or unhelpful

Return JSON: {{"score": N, "explanation": "..."}}"""

        eval_response = client.chat.completions.create(
            model=evaluator_model,
            messages=[{"role": "user", "content": eval_prompt}],
            response_format={"type": "json_object"}
        )

        eval_result = json.loads(eval_response.choices[0].message.content)
        results["scores"].append(eval_result["score"])

        results["examples"].append({
            "input": user_message,
            "expected": expected,
            "actual": actual,
            "score": eval_result["score"],
            "explanation": eval_result["explanation"]
        })

    results["average_score"] = sum(results["scores"]) / len(results["scores"])
    return results
```

## Production Pipeline

```python
from dataclasses import dataclass
from typing import List, Dict, Optional
import logging

@dataclass
class FineTuneConfig:
    base_model: str = "gpt-3.5-turbo-0125"
    suffix: str = None
    n_epochs: int = 3
    validation_split: float = 0.1
    min_examples: int = 10

class FineTuningPipeline:
    """Production fine-tuning pipeline."""

    def __init__(self, config: Optional[FineTuneConfig] = None):
        self.config = config or FineTuneConfig()
        self.client = OpenAI()
        self.logger = logging.getLogger(__name__)

    def run(
        self,
        training_data: List[Dict],
        wait_for_completion: bool = True
    ) -> Dict:
        """Execute full fine-tuning pipeline."""
        # Validate data
        self.logger.info("Validating training data...")
        if len(training_data) < self.config.min_examples:
            raise ValueError(f"Need at least {self.config.min_examples} examples")

        # Split data
        val_size = int(len(training_data) * self.config.validation_split)
        train_data = training_data[val_size:]
        val_data = training_data[:val_size]

        # Save and upload files
        self.logger.info("Uploading training files...")
        train_file = self._save_and_upload(train_data, "train")
        val_file = self._save_and_upload(val_data, "val") if val_data else None

        # Start fine-tuning
        self.logger.info("Starting fine-tuning job...")
        job = self.client.fine_tuning.jobs.create(
            training_file=train_file,
            validation_file=val_file,
            model=self.config.base_model,
            suffix=self.config.suffix,
            hyperparameters={"n_epochs": self.config.n_epochs}
        )

        if wait_for_completion:
            return self._wait_for_job(job.id)
        else:
            return {"job_id": job.id, "status": "started"}

    def _save_and_upload(self, data: List[Dict], name: str) -> str:
        """Save data to file and upload."""
        filepath = f"/tmp/{name}_data.jsonl"
        with open(filepath, 'w') as f:
            for example in data:
                f.write(json.dumps(example) + '\n')

        with open(filepath, "rb") as f:
            response = self.client.files.create(file=f, purpose="fine-tune")

        return response.id

    def _wait_for_job(self, job_id: str) -> Dict:
        """Wait for job completion."""
        while True:
            job = self.client.fine_tuning.jobs.retrieve(job_id)

            if job.status == "succeeded":
                self.logger.info(f"Fine-tuning complete: {job.fine_tuned_model}")
                return {
                    "status": "succeeded",
                    "model": job.fine_tuned_model,
                    "trained_tokens": job.trained_tokens
                }
            elif job.status in ["failed", "cancelled"]:
                self.logger.error(f"Fine-tuning failed: {job.error}")
                return {"status": job.status, "error": str(job.error)}

            self.logger.info(f"Status: {job.status}")
            time.sleep(60)
```

## Best Practices

### Data Quality

- Minimum 50-100 high-quality examples
- Diverse examples covering edge cases
- Consistent format across examples

### Data Preparation

- Clean and validate all data
- Use consistent system prompts
- Balance example categories

### Hyperparameters

- Start with defaults ("auto")
- Increase epochs if underfitting
- Use validation set to detect overfitting

### Evaluation

- Hold out test set before training
- Compare to base model
- Test on real-world queries

### Iteration

- Start small, add more data
- Monitor training metrics
- Retrain when data changes

## Common Pitfalls

1. **Too Few Examples** - Need 50+ for meaningful improvement
2. **Inconsistent Format** - Confuses the model during training
3. **No Validation Set** - Can't detect overfitting
4. **Overfitting** - Too many epochs on small dataset
5. **Wrong Base Model** - Using larger model than needed
6. **Ignoring Costs** - Training + inference costs add up

## Related

- [fine-tuning-openai-basics.md](fine-tuning-openai-basics.md) - Data preparation and validation
- [model-evaluation.md](model-evaluation.md) - Evaluation methodologies
- [cost-optimization.md](cost-optimization.md) - Cost management

## References

- [OpenAI Fine-tuning Guide](https://platform.openai.com/docs/guides/fine-tuning)
- [Fine-tuning Best Practices](https://platform.openai.com/docs/guides/fine-tuning/preparing-your-dataset)
- [OpenAI Cookbook Fine-tuning](https://cookbook.openai.com/examples/how_to_finetune_chat_models)
