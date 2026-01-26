# OpenAI Fine-Tuning Examples

Complete code examples for fine-tuning workflows.

## Data Format Examples

### SFT Training Data (JSONL)

```jsonl
{"messages": [{"role": "system", "content": "You are a customer support agent for TechCorp."}, {"role": "user", "content": "How do I reset my password?"}, {"role": "assistant", "content": "To reset your password:\n1. Go to settings.techcorp.com/password\n2. Click 'Forgot Password'\n3. Enter your email address\n4. Check your inbox for the reset link\n5. Create a new password (8+ characters)"}]}
{"messages": [{"role": "system", "content": "You are a customer support agent for TechCorp."}, {"role": "user", "content": "I want to cancel my subscription"}, {"role": "assistant", "content": "I understand you'd like to cancel. Before I process this:\n\n1. Your subscription is valid until March 15, 2025\n2. You'll lose access to premium features\n3. Data will be retained for 30 days\n\nTo confirm cancellation, please reply with 'CANCEL'. Or let me know if you'd like to discuss alternatives."}]}
{"messages": [{"role": "system", "content": "You are a customer support agent for TechCorp."}, {"role": "user", "content": "Your app keeps crashing on my iPhone"}, {"role": "assistant", "content": "I'm sorry about the crashes. Let's fix this:\n\n**Quick fixes:**\n1. Force close the app (swipe up from app switcher)\n2. Restart your iPhone\n3. Check for app updates in App Store\n\n**If still crashing:**\n1. Delete and reinstall the app\n2. Ensure iOS is updated (Settings > General > Software Update)\n\nIf issues persist, please share your iOS version and I'll escalate to our engineering team."}]}
```

### DPO Training Data (JSONL)

```jsonl
{"input": [{"role": "user", "content": "Summarize this article about climate change in 2 sentences."}], "preferred_output": [{"role": "assistant", "content": "Global temperatures rose 1.2C above pre-industrial levels in 2024, driven by record fossil fuel emissions. Scientists warn that without immediate action, irreversible tipping points may be reached within a decade."}], "non_preferred_output": [{"role": "assistant", "content": "Climate change is bad and getting worse. We need to do something about it soon."}]}
{"input": [{"role": "user", "content": "Write a professional email declining a meeting request."}], "preferred_output": [{"role": "assistant", "content": "Subject: Re: Meeting Request - March 15\n\nHi Sarah,\n\nThank you for thinking of me for this discussion. Unfortunately, I have a conflict on March 15 that I cannot reschedule.\n\nWould any of these alternatives work?\n- March 17, 2-4 PM\n- March 18, 10 AM-12 PM\n\nAlternatively, I'm happy to provide input via email if that would be helpful.\n\nBest regards,\nJohn"}], "non_preferred_output": [{"role": "assistant", "content": "Hi,\n\nCan't make the meeting on the 15th. Maybe another time?\n\nThanks"}]}
```

### Multi-turn Conversation (SFT)

```jsonl
{"messages": [{"role": "system", "content": "You are an AI coding assistant."}, {"role": "user", "content": "How do I read a file in Python?"}, {"role": "assistant", "content": "Here's how to read a file in Python:\n\n```python\n# Basic file reading\nwith open('file.txt', 'r') as f:\n    content = f.read()\n```\n\nThe `with` statement ensures the file is properly closed after reading."}, {"role": "user", "content": "What if I want to read line by line?"}, {"role": "assistant", "content": "For line-by-line reading, you have several options:\n\n```python\n# Option 1: Iterate directly (memory efficient)\nwith open('file.txt', 'r') as f:\n    for line in f:\n        print(line.strip())\n\n# Option 2: Read all lines into a list\nwith open('file.txt', 'r') as f:\n    lines = f.readlines()\n\n# Option 3: Read specific number of lines\nwith open('file.txt', 'r') as f:\n    first_10_lines = [next(f) for _ in range(10)]\n```\n\nOption 1 is best for large files as it doesn't load everything into memory."}]}
```

### Function Calling Training Data

```jsonl
{"messages": [{"role": "system", "content": "You are a helpful assistant with access to a weather API."}, {"role": "user", "content": "What's the weather in Tokyo?"}, {"role": "assistant", "content": null, "function_call": {"name": "get_weather", "arguments": "{\"location\": \"Tokyo, Japan\", \"units\": \"celsius\"}"}}, {"role": "function", "name": "get_weather", "content": "{\"temp\": 22, \"condition\": \"Partly cloudy\", \"humidity\": 65}"}, {"role": "assistant", "content": "The weather in Tokyo is currently 22°C with partly cloudy skies and 65% humidity."}]}
```

## Complete Workflow Examples

### Example 1: Basic SFT Fine-Tuning

```python
from openai import OpenAI
import json
import time

client = OpenAI()

# Step 1: Prepare training data
training_data = [
    {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi! How can I help you today?"}
        ]
    },
    # Add more examples...
]

# Step 2: Save as JSONL
with open("training_data.jsonl", "w") as f:
    for example in training_data:
        f.write(json.dumps(example) + "\n")

# Step 3: Upload training file
with open("training_data.jsonl", "rb") as f:
    training_file = client.files.create(file=f, purpose="fine-tune")

print(f"Training file ID: {training_file.id}")

# Step 4: Wait for file processing
while True:
    file_status = client.files.retrieve(training_file.id)
    if file_status.status == "processed":
        break
    time.sleep(5)

# Step 5: Create fine-tuning job
job = client.fine_tuning.jobs.create(
    training_file=training_file.id,
    model="gpt-4o-mini-2024-07-18",
    suffix="my-custom-model",
    hyperparameters={
        "n_epochs": 3
    }
)

print(f"Job ID: {job.id}")

# Step 6: Monitor progress
while True:
    job_status = client.fine_tuning.jobs.retrieve(job.id)
    print(f"Status: {job_status.status}")

    if job_status.status == "succeeded":
        print(f"Fine-tuned model: {job_status.fine_tuned_model}")
        break
    elif job_status.status == "failed":
        print(f"Error: {job_status.error}")
        break

    # Print recent events
    events = client.fine_tuning.jobs.list_events(job.id, limit=3)
    for event in events.data:
        print(f"  {event.message}")

    time.sleep(60)

# Step 7: Use fine-tuned model
response = client.chat.completions.create(
    model=job_status.fine_tuned_model,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello"}
    ]
)

print(response.choices[0].message.content)
```

### Example 2: DPO Fine-Tuning

```python
from openai import OpenAI
import json

client = OpenAI()

# Step 1: Prepare DPO data
dpo_data = [
    {
        "input": [
            {"role": "user", "content": "Explain quantum computing simply."}
        ],
        "preferred_output": [
            {"role": "assistant", "content": "Quantum computing uses quantum bits (qubits) that can be 0, 1, or both at once (superposition). This allows quantum computers to process many possibilities simultaneously, making them powerful for specific problems like cryptography and drug discovery. Think of it like checking all paths in a maze at once instead of one at a time."}
        ],
        "non_preferred_output": [
            {"role": "assistant", "content": "Quantum computing is a type of computing that uses quantum mechanics principles like superposition and entanglement to perform calculations. It's very complex and involves qubits instead of regular bits."}
        ]
    },
    # Add more preference pairs...
]

# Step 2: Save and upload
with open("dpo_data.jsonl", "w") as f:
    for example in dpo_data:
        f.write(json.dumps(example) + "\n")

with open("dpo_data.jsonl", "rb") as f:
    training_file = client.files.create(file=f, purpose="fine-tune")

# Step 3: Create DPO job
job = client.fine_tuning.jobs.create(
    training_file=training_file.id,
    model="gpt-4.1-mini-2025-04-14",
    method={
        "type": "dpo",
        "dpo": {
            "hyperparameters": {
                "beta": 0.1  # Controls drift from reference model (0.1-0.5)
            }
        }
    },
    suffix="dpo-aligned"
)

print(f"DPO Job ID: {job.id}")
```

### Example 3: Fine-Tuning with Validation

```python
from openai import OpenAI
import json
import random

client = OpenAI()

# Prepare data with train/validation split
all_data = [...]  # Your examples

random.shuffle(all_data)
split_idx = int(len(all_data) * 0.9)
train_data = all_data[:split_idx]
val_data = all_data[split_idx:]

# Save files
for name, data in [("train", train_data), ("val", val_data)]:
    with open(f"{name}_data.jsonl", "w") as f:
        for example in data:
            f.write(json.dumps(example) + "\n")

# Upload both files
with open("train_data.jsonl", "rb") as f:
    train_file = client.files.create(file=f, purpose="fine-tune")

with open("val_data.jsonl", "rb") as f:
    val_file = client.files.create(file=f, purpose="fine-tune")

# Create job with validation
job = client.fine_tuning.jobs.create(
    training_file=train_file.id,
    validation_file=val_file.id,
    model="gpt-4o-mini-2024-07-18",
    suffix="with-validation",
    hyperparameters={
        "n_epochs": 3,
        "batch_size": 4,
        "learning_rate_multiplier": 1.0
    }
)

# Monitor with validation metrics
while True:
    job_status = client.fine_tuning.jobs.retrieve(job.id)

    if job_status.status in ["succeeded", "failed", "cancelled"]:
        break

    # Check training metrics
    events = client.fine_tuning.jobs.list_events(job.id, limit=5)
    for event in events.data:
        if "training_loss" in event.message or "validation_loss" in event.message:
            print(event.message)

    time.sleep(60)
```

### Example 4: Model Evaluation

```python
from openai import OpenAI
import json
from typing import List, Dict

client = OpenAI()

def evaluate_model(
    model_name: str,
    test_data: List[Dict],
    evaluator_model: str = "gpt-4o"
) -> Dict:
    """Evaluate fine-tuned model against test set."""

    results = {
        "total": len(test_data),
        "scores": [],
        "examples": []
    }

    for example in test_data:
        # Extract user message
        user_msg = next(
            m["content"] for m in example["messages"]
            if m["role"] == "user"
        )

        # Get expected output
        expected = next(
            m["content"] for m in example["messages"]
            if m["role"] == "assistant"
        )

        # Get model output
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                m for m in example["messages"]
                if m["role"] != "assistant"
            ],
            temperature=0
        )
        actual = response.choices[0].message.content

        # Evaluate with GPT-4
        eval_prompt = f"""Compare these responses and rate from 1-5.

Query: {user_msg}

Expected response:
{expected}

Actual response:
{actual}

Rating criteria:
5: Equivalent or better quality
4: Minor differences, same quality
3: Noticeable differences but acceptable
2: Significant quality gap
1: Wrong or unhelpful

Return JSON: {{"score": N, "explanation": "brief reason"}}"""

        eval_response = client.chat.completions.create(
            model=evaluator_model,
            messages=[{"role": "user", "content": eval_prompt}],
            response_format={"type": "json_object"},
            temperature=0
        )

        eval_result = json.loads(eval_response.choices[0].message.content)
        results["scores"].append(eval_result["score"])
        results["examples"].append({
            "input": user_msg,
            "expected": expected,
            "actual": actual,
            "score": eval_result["score"],
            "explanation": eval_result["explanation"]
        })

    results["average_score"] = sum(results["scores"]) / len(results["scores"])
    results["score_distribution"] = {
        i: results["scores"].count(i) for i in range(1, 6)
    }

    return results

# Usage
test_examples = [...]  # Load test data
results = evaluate_model(
    model_name="ft:gpt-4o-mini:my-org::abc123",
    test_data=test_examples
)

print(f"Average score: {results['average_score']:.2f}")
print(f"Distribution: {results['score_distribution']}")
```

### Example 5: A/B Comparison

```python
from openai import OpenAI
import json
from typing import List, Tuple

client = OpenAI()

def compare_models(
    base_model: str,
    fine_tuned_model: str,
    test_queries: List[str],
    system_prompt: str = "You are a helpful assistant."
) -> Dict:
    """A/B compare base vs fine-tuned model."""

    comparisons = []

    for query in test_queries:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]

        # Get both responses
        base_response = client.chat.completions.create(
            model=base_model,
            messages=messages,
            temperature=0
        )

        ft_response = client.chat.completions.create(
            model=fine_tuned_model,
            messages=messages,
            temperature=0
        )

        base_output = base_response.choices[0].message.content
        ft_output = ft_response.choices[0].message.content

        # Judge comparison
        judge_prompt = f"""Compare Response A vs Response B for this query.

Query: {query}

Response A:
{base_output}

Response B:
{ft_output}

Which is better? Return JSON:
{{"winner": "A" or "B" or "tie", "reason": "brief explanation"}}"""

        judgment = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": judge_prompt}],
            response_format={"type": "json_object"},
            temperature=0
        )

        result = json.loads(judgment.choices[0].message.content)
        comparisons.append({
            "query": query,
            "base": base_output,
            "fine_tuned": ft_output,
            "winner": result["winner"],
            "reason": result["reason"]
        })

    # Summarize
    wins = {"A": 0, "B": 0, "tie": 0}
    for c in comparisons:
        wins[c["winner"]] += 1

    return {
        "comparisons": comparisons,
        "summary": {
            "base_wins": wins["A"],
            "fine_tuned_wins": wins["B"],
            "ties": wins["tie"],
            "fine_tuned_win_rate": wins["B"] / len(comparisons)
        }
    }

# Usage
results = compare_models(
    base_model="gpt-4o-mini",
    fine_tuned_model="ft:gpt-4o-mini:my-org::abc123",
    test_queries=[
        "How do I reset my password?",
        "What's your refund policy?",
        "The app isn't working"
    ]
)

print(f"Fine-tuned win rate: {results['summary']['fine_tuned_win_rate']:.1%}")
```

## Data Preparation Examples

### Convert CSV to JSONL

```python
import csv
import json

def csv_to_jsonl(
    csv_path: str,
    jsonl_path: str,
    system_prompt: str,
    input_col: str,
    output_col: str
):
    """Convert CSV with input/output columns to JSONL."""

    with open(csv_path, 'r') as csv_file, \
         open(jsonl_path, 'w') as jsonl_file:

        reader = csv.DictReader(csv_file)

        for row in reader:
            example = {
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": row[input_col]},
                    {"role": "assistant", "content": row[output_col]}
                ]
            }
            jsonl_file.write(json.dumps(example) + "\n")

# Usage
csv_to_jsonl(
    csv_path="data.csv",
    jsonl_path="training.jsonl",
    system_prompt="You are a helpful assistant.",
    input_col="question",
    output_col="answer"
)
```

### Validate JSONL Format

```python
import json
from typing import List, Tuple

def validate_jsonl(filepath: str) -> Tuple[bool, List[str]]:
    """Validate JSONL training file format."""

    errors = []

    with open(filepath, 'r') as f:
        for i, line in enumerate(f, 1):
            try:
                data = json.loads(line)
            except json.JSONDecodeError as e:
                errors.append(f"Line {i}: Invalid JSON - {e}")
                continue

            # Check for messages key
            if "messages" not in data:
                errors.append(f"Line {i}: Missing 'messages' key")
                continue

            messages = data["messages"]

            # Check messages is a list
            if not isinstance(messages, list):
                errors.append(f"Line {i}: 'messages' must be a list")
                continue

            # Check each message
            roles_seen = []
            for j, msg in enumerate(messages):
                if "role" not in msg:
                    errors.append(f"Line {i}, msg {j}: Missing 'role'")
                if "content" not in msg:
                    errors.append(f"Line {i}, msg {j}: Missing 'content'")

                if "role" in msg:
                    roles_seen.append(msg["role"])

            # Check for required roles
            if "assistant" not in roles_seen:
                errors.append(f"Line {i}: No assistant message")

            if "user" not in roles_seen:
                errors.append(f"Line {i}: No user message")

    return len(errors) == 0, errors

# Usage
valid, errors = validate_jsonl("training.jsonl")
if not valid:
    for error in errors:
        print(error)
```

### Token Counting

```python
import tiktoken

def count_tokens(filepath: str, model: str = "gpt-4o") -> dict:
    """Count tokens in training file."""

    encoding = tiktoken.encoding_for_model(model)

    total_tokens = 0
    example_count = 0
    token_counts = []

    with open(filepath, 'r') as f:
        for line in f:
            data = json.loads(line)
            example_tokens = 0

            for msg in data["messages"]:
                # Count message tokens
                example_tokens += len(encoding.encode(msg.get("content", "")))
                # Add overhead for role and formatting
                example_tokens += 4

            example_tokens += 2  # Conversation overhead
            token_counts.append(example_tokens)
            total_tokens += example_tokens
            example_count += 1

    return {
        "total_tokens": total_tokens,
        "example_count": example_count,
        "avg_tokens_per_example": total_tokens / example_count,
        "max_tokens": max(token_counts),
        "min_tokens": min(token_counts)
    }

# Usage
stats = count_tokens("training.jsonl")
print(f"Total tokens: {stats['total_tokens']:,}")
print(f"Estimated cost (3 epochs, gpt-4o-mini): ${stats['total_tokens'] * 3 * 3 / 1_000_000:.2f}")
```
