# OpenAI Embeddings & Batch API

**Text embeddings, vector search, and batch processing for cost savings**

---

## Quick Reference

| API | Use Case | Cost Savings |
|-----|----------|--------------|
| **Embeddings** | Vector search, RAG, semantic similarity | - |
| **Batch API** | Non-time-sensitive workloads | 50% off |

---

## Embeddings API

### Generate Embeddings

```python
from openai import OpenAI

client = OpenAI()

response = client.embeddings.create(
    model="text-embedding-3-large",
    input="Faion Network provides AI tools for solopreneurs",
    encoding_format="float",  # "float" | "base64"
    dimensions=1536           # Optional, reduce for cost savings
)

embedding = response.data[0].embedding
print(f"Dimensions: {len(embedding)}")
```

### Batch Embeddings

```python
texts = [
    "What is SDD methodology?",
    "How to create AI agents?",
    "Faion Network pricing plans"
]

response = client.embeddings.create(
    model="text-embedding-3-large",
    input=texts
)

for i, item in enumerate(response.data):
    print(f"Text {i}: {len(item.embedding)} dimensions")
```

### Models

| Model | Dimensions | Max Tokens | Price $/M |
|-------|------------|------------|-----------|
| **text-embedding-3-large** | 3072 (or custom) | 8191 | $0.13 |
| **text-embedding-3-small** | 1536 (or custom) | 8191 | $0.02 |
| **text-embedding-ada-002** | 1536 | 8191 | $0.10 |

### Dimensionality Reduction

```python
# Reduce dimensions for cost/performance tradeoff
response = client.embeddings.create(
    model="text-embedding-3-large",
    input="Your text",
    dimensions=256  # Reduced from 3072
)
```

### Cosine Similarity

```python
import numpy as np

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

query_embedding = client.embeddings.create(
    model="text-embedding-3-small",
    input="How to use SDD?"
).data[0].embedding

doc_embedding = client.embeddings.create(
    model="text-embedding-3-small",
    input="SDD is a specification-driven methodology..."
).data[0].embedding

similarity = cosine_similarity(query_embedding, doc_embedding)
print(f"Similarity: {similarity:.4f}")
```

---

## Batch API

**50% cost reduction for non-time-sensitive workloads with 24-hour completion window**

### Create Batch File

```python
import json

# Create JSONL file with requests
requests = [
    {
        "custom_id": "request-1",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": "Hello!"}],
            "max_tokens": 100
        }
    },
    {
        "custom_id": "request-2",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": "World!"}],
            "max_tokens": 100
        }
    }
]

with open("batch_requests.jsonl", "w") as f:
    for req in requests:
        f.write(json.dumps(req) + "\n")
```

### Submit Batch

```python
# Upload file
batch_file = client.files.create(
    file=open("batch_requests.jsonl", "rb"),
    purpose="batch"
)

# Create batch
batch = client.batches.create(
    input_file_id=batch_file.id,
    endpoint="/v1/chat/completions",
    completion_window="24h",
    metadata={"description": "Daily summaries"}
)

print(f"Batch ID: {batch.id}")
print(f"Status: {batch.status}")
```

### Check Status

```python
batch = client.batches.retrieve(batch.id)
print(f"Status: {batch.status}")
print(f"Completed: {batch.request_counts.completed}/{batch.request_counts.total}")

if batch.status == "completed":
    # Download results
    result_file = client.files.content(batch.output_file_id)
    results = result_file.text

    for line in results.strip().split("\n"):
        result = json.loads(line)
        print(f"{result['custom_id']}: {result['response']['body']['choices'][0]['message']['content']}")
```

### Batch Pricing

| Model | Regular Price | Batch Price (50% off) |
|-------|--------------|----------------------|
| gpt-4o | $2.50/$10.00 | $1.25/$5.00 |
| gpt-4o-mini | $0.15/$0.60 | $0.075/$0.30 |

---

## Realtime API

**WebSocket-based API for voice conversations**

### Connect

```python
import asyncio
import websockets
import json
import base64
import os

async def realtime_conversation():
    url = "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-12-17"
    headers = {
        "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
        "OpenAI-Beta": "realtime=v1"
    }

    async with websockets.connect(url, extra_headers=headers) as ws:
        # Configure session
        await ws.send(json.dumps({
            "type": "session.update",
            "session": {
                "modalities": ["text", "audio"],
                "voice": "alloy",
                "instructions": "You are a helpful assistant."
            }
        }))

        # Send user message
        await ws.send(json.dumps({
            "type": "conversation.item.create",
            "item": {
                "type": "message",
                "role": "user",
                "content": [{"type": "input_text", "text": "Hello!"}]
            }
        }))

        # Request response
        await ws.send(json.dumps({"type": "response.create"}))

        # Receive response
        async for message in ws:
            event = json.loads(message)
            if event["type"] == "response.audio_transcript.delta":
                print(event["delta"], end="", flush=True)
            elif event["type"] == "response.done":
                break

asyncio.run(realtime_conversation())
```

### Pricing

| Component | Price |
|-----------|-------|
| Audio input | $100.00 / 1M tokens |
| Audio output | $200.00 / 1M tokens |
| Text input | $5.00 / 1M tokens |
| Text output | $20.00 / 1M tokens |

---

## Fine-tuning

### Prepare Training Data

```jsonl
{"messages": [{"role": "system", "content": "You are an SDD expert."}, {"role": "user", "content": "What is SDD?"}, {"role": "assistant", "content": "SDD (Specification-Driven Development) is a methodology..."}]}
{"messages": [{"role": "user", "content": "How to write a spec?"}, {"role": "assistant", "content": "To write a spec, start with..."}]}
```

### Create Fine-tuning Job

```python
# Upload training file
training_file = client.files.create(
    file=open("training_data.jsonl", "rb"),
    purpose="fine-tune"
)

# Create fine-tuning job
job = client.fine_tuning.jobs.create(
    training_file=training_file.id,
    model="gpt-4o-mini-2024-07-18",
    hyperparameters={
        "n_epochs": 3,
        "batch_size": "auto",
        "learning_rate_multiplier": "auto"
    },
    suffix="sdd-expert"
)
```

### Monitor Job

```python
# Check status
job = client.fine_tuning.jobs.retrieve(job.id)
print(f"Status: {job.status}")

# List events
events = client.fine_tuning.jobs.list_events(job.id, limit=10)
for event in events.data:
    print(f"{event.created_at}: {event.message}")
```

### Use Fine-tuned Model

```python
response = client.chat.completions.create(
    model="ft:gpt-4o-mini-2024-07-18:org-xxx:sdd-expert:abc123",
    messages=[{"role": "user", "content": "Explain SDD phases"}]
)
```

### Pricing

| Model | Training | Input | Output |
|-------|----------|-------|--------|
| gpt-4o-mini-2024-07-18 | $25.00/1M tokens | $3.00/1M | $12.00/1M |
| gpt-4o-2024-08-06 | $25.00/1M tokens | $3.75/1M | $15.00/1M |

---

## Quick Commands

### curl Examples

```bash
# Create embedding
curl https://api.openai.com/v1/embeddings \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "text-embedding-3-small", "input": "Hello world"}'
```

---

## Related

- [openai-chat-completions.md](openai-chat-completions.md) - Chat API basics
- [openai-function-calling.md](openai-function-calling.md) - Tool use and structured outputs
- [openai-assistants.md](openai-assistants.md) - Assistants API
