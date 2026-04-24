---
id: fine-tuning-openai-basics
name: "Fine-tuning OpenAI - Basics"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# Fine-tuning OpenAI - Basics

## Overview

OpenAI fine-tuning allows customizing GPT models on your specific data to improve performance on domain-specific tasks, reduce prompt length, achieve more consistent outputs, and lower costs by using smaller fine-tuned models.

## When to Use

- Consistent style/format requirements
- Domain-specific terminology
- Reducing prompt engineering complexity
- Improving output reliability
- Cost reduction (fine-tuned gpt-3.5-turbo vs. gpt-4)
- Low latency requirements

## Key Concepts

### Fine-tunable Models

| Model | Context | Cost (Training) | Cost (Inference) |
|-------|---------|-----------------|------------------|
| gpt-4o-2024-08-06 | 128K | $25/1M tokens | $3.75/1M in, $15/1M out |
| gpt-4o-mini-2024-07-18 | 128K | $3/1M tokens | $0.30/1M in, $1.20/1M out |
| gpt-3.5-turbo-0125 | 16K | $8/1M tokens | $3/1M in, $6/1M out |

### When Fine-tuning Helps

| Use Case | RAG | Few-shot | Fine-tune |
|----------|-----|----------|-----------|
| Learn new facts | Best | OK | Poor |
| Consistent format | OK | OK | Best |
| Domain style | OK | OK | Best |
| Reduce latency | OK | Poor | Best |
| Reduce cost | Depends | Poor | Best |

## Data Preparation

### Creating Training Examples

```python
import json
from typing import List, Dict
import tiktoken

def create_training_example(
    system: str,
    user: str,
    assistant: str
) -> Dict:
    """Create a single training example in OpenAI format."""
    return {
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
            {"role": "assistant", "content": assistant}
        ]
    }

def prepare_dataset(
    examples: List[Dict],
    output_file: str
) -> None:
    """Save examples to JSONL format for fine-tuning."""
    with open(output_file, 'w') as f:
        for example in examples:
            f.write(json.dumps(example) + '\n')

# Example: Creating a customer support dataset
training_data = [
    create_training_example(
        system="You are a helpful customer support agent for TechCorp.",
        user="How do I reset my password?",
        assistant="To reset your password:\n1. Go to login page\n2. Click 'Forgot Password'\n3. Enter your email\n4. Check your inbox for reset link\n5. Create a new password\n\nNeed more help? Contact support@techcorp.com"
    ),
    create_training_example(
        system="You are a helpful customer support agent for TechCorp.",
        user="What are your business hours?",
        assistant="TechCorp support is available:\n- Monday-Friday: 9 AM - 6 PM EST\n- Saturday: 10 AM - 4 PM EST\n- Sunday: Closed\n\nFor urgent issues, email urgent@techcorp.com"
    ),
]

prepare_dataset(training_data, "training_data.jsonl")
```

## Data Validation

### Validation Script

```python
import json
import tiktoken
from collections import defaultdict

def validate_dataset(filepath: str, model: str = "gpt-3.5-turbo") -> Dict:
    """Validate fine-tuning dataset."""
    encoding = tiktoken.encoding_for_model(model)

    stats = {
        "total_examples": 0,
        "total_tokens": 0,
        "errors": [],
        "token_distribution": defaultdict(int)
    }

    with open(filepath, 'r') as f:
        for i, line in enumerate(f):
            try:
                example = json.loads(line)

                # Check structure
                if "messages" not in example:
                    stats["errors"].append(f"Line {i}: Missing 'messages' key")
                    continue

                messages = example["messages"]

                # Check roles
                roles = [m.get("role") for m in messages]
                if "assistant" not in roles:
                    stats["errors"].append(f"Line {i}: Missing assistant message")

                # Count tokens
                tokens = 0
                for message in messages:
                    content = message.get("content", "")
                    tokens += len(encoding.encode(content))

                stats["total_tokens"] += tokens
                stats["total_examples"] += 1

                # Track distribution
                bucket = (tokens // 100) * 100
                stats["token_distribution"][bucket] += 1

            except json.JSONDecodeError as e:
                stats["errors"].append(f"Line {i}: Invalid JSON - {e}")

    # Calculate cost estimate
    stats["estimated_cost"] = (stats["total_tokens"] / 1_000_000) * 8  # $8/1M for gpt-3.5

    return stats

# Usage
stats = validate_dataset("training_data.jsonl")
print(f"Examples: {stats['total_examples']}")
print(f"Tokens: {stats['total_tokens']}")
print(f"Estimated cost: ${stats['estimated_cost']:.2f}")
print(f"Errors: {stats['errors']}")
```

## Data Generation

### Generating Training Data with GPT-4

```python
def generate_training_data(
    seed_examples: List[Dict],
    num_examples: int = 100,
    model: str = "gpt-4o"
) -> List[Dict]:
    """Generate additional training examples using GPT-4."""
    from openai import OpenAI

    client = OpenAI()
    generated = []

    prompt = f"""Based on these examples of customer support conversations, generate {num_examples} new varied examples.

Examples:
{json.dumps(seed_examples[:5], indent=2)}

Generate diverse questions and helpful, consistent responses.
Return as JSON array of objects with 'user' and 'assistant' keys."""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    data = json.loads(response.choices[0].message.content)

    for item in data.get("examples", []):
        generated.append(create_training_example(
            system="You are a helpful customer support agent for TechCorp.",
            user=item["user"],
            assistant=item["assistant"]
        ))

    return generated
```

## Dataset Guidelines

### Minimum Requirements

- **50-100 examples** minimum for meaningful improvement
- **Consistent format** across all examples
- **Diverse examples** covering edge cases
- **Balanced categories** if using multiple types

### Quality Checklist

- All examples follow same message structure
- System prompts are consistent
- Assistant responses match desired style
- No missing or malformed messages
- Token counts are reasonable (not too long)
- Examples cover common user queries
- Edge cases included

## Related

- [fine-tuning-openai-production.md](fine-tuning-openai-production.md) - Training, evaluation, production pipeline
- [fine-tuning-lora.md](fine-tuning-lora.md) - LoRA fine-tuning for open models
- [finetuning-datasets.md](finetuning-datasets.md) - Dataset preparation guide

## References

- [OpenAI Fine-tuning Guide](https://platform.openai.com/docs/guides/fine-tuning)
- [Fine-tuning Best Practices](https://platform.openai.com/docs/guides/fine-tuning/preparing-your-dataset)
- [OpenAI Cookbook Fine-tuning](https://cookbook.openai.com/examples/how_to_finetune_chat_models)

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| OpenAI fine-tuning setup | haiku | Configuration |
| Job submission | haiku | API usage |
| Result retrieval | haiku | Data collection |
