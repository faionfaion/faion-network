---
name: faion-gemini-basics
user-invocable: false
description: "Gemini API basics: models, setup, text generation, streaming, chat"
---

# Gemini API Basics

**Core concepts, setup, text generation, streaming, and chat conversations.**

---

## Quick Reference

| Area | Key Elements |
|------|--------------|
| **Models** | Gemini 2.0 Flash, 1.5 Pro (2M context), 1.5 Flash, Ultra |
| **Use Cases** | Text generation, chat, JSON output, streaming |
| **Features** | Large context, fast inference, structured output |
| **Pricing** | Free tier available, context caching saves 75% |

---

## Model Overview

### Available Models (January 2026)

| Model | Context Window | Strengths | Use Cases |
|-------|----------------|-----------|-----------|
| **Gemini 2.0 Flash** | 1M tokens | Fastest, multimodal, agentic | Real-time apps, agents |
| **Gemini 2.0 Flash Thinking** | 1M tokens | Reasoning, chain-of-thought | Complex reasoning, math |
| **Gemini 1.5 Pro** | 2M tokens | Largest context, balanced | Long documents, codebases |
| **Gemini 1.5 Flash** | 1M tokens | Cost-effective, fast | High-volume, production |
| **Gemini 1.5 Flash-8B** | 1M tokens | Smallest, cheapest | Simple tasks, edge |
| **Gemini Ultra** | 128K tokens | Most capable | Complex multimodal tasks |

### Model Selection Guide

```
Need fastest response? → Gemini 2.0 Flash
Need reasoning? → Gemini 2.0 Flash Thinking
Need largest context? → Gemini 1.5 Pro (2M tokens)
Need cost efficiency? → Gemini 1.5 Flash-8B
Need best quality? → Gemini Ultra
```

---

## Installation & Setup

### Python SDK

```bash
pip install google-generativeai
```

### Authentication

```python
import google.generativeai as genai

# Option 1: API Key (Google AI Studio)
genai.configure(api_key="YOUR_API_KEY")

# Option 2: Environment variable
# export GOOGLE_API_KEY="your-api-key"
genai.configure()
```

### Vertex AI Setup

```bash
# Install Vertex AI SDK
pip install google-cloud-aiplatform

# Authenticate with Google Cloud
gcloud auth application-default login
```

```python
import vertexai
from vertexai.generative_models import GenerativeModel

vertexai.init(project="your-project-id", location="us-central1")
model = GenerativeModel("gemini-1.5-pro")
```

---

## Basic Text Generation

### Simple Request

```python
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel("gemini-2.0-flash")

response = model.generate_content("Explain quantum computing in simple terms")
print(response.text)
```

### With Generation Config

```python
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config={
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",  # or "application/json"
    }
)

response = model.generate_content("Write a product description for a smartwatch")
```

### JSON Output

```python
import json

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config={
        "response_mime_type": "application/json",
        "response_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "price": {"type": "number"},
                "features": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["name", "price"]
        }
    }
)

response = model.generate_content("Create a product listing for wireless earbuds")
product = json.loads(response.text)
```

---

## Streaming

### Text Streaming

```python
model = genai.GenerativeModel("gemini-2.0-flash")

response = model.generate_content(
    "Write a long story about space exploration",
    stream=True
)

for chunk in response:
    print(chunk.text, end="", flush=True)
```

### Chat Streaming

```python
model = genai.GenerativeModel("gemini-1.5-pro")
chat = model.start_chat()

response = chat.send_message("Tell me about Mars", stream=True)

for chunk in response:
    print(chunk.text, end="")
```

### Async Streaming

```python
import asyncio
import google.generativeai as genai

async def stream_response():
    model = genai.GenerativeModel("gemini-2.0-flash")

    response = await model.generate_content_async(
        "Explain machine learning",
        stream=True
    )

    async for chunk in response:
        print(chunk.text, end="")

asyncio.run(stream_response())
```

---

## Chat Conversations

### Basic Chat

```python
model = genai.GenerativeModel("gemini-1.5-pro")
chat = model.start_chat()

response = chat.send_message("Hello! I'm learning Python.")
print(response.text)

response = chat.send_message("What should I learn first?")
print(response.text)

response = chat.send_message("Show me an example")
print(response.text)

# Access history
for message in chat.history:
    print(f"{message.role}: {message.parts[0].text}")
```

### Chat with System Instruction

```python
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    system_instruction="""You are a helpful Python tutor.
    Always provide code examples.
    Explain concepts step by step.
    Use beginner-friendly language."""
)

chat = model.start_chat()
response = chat.send_message("What are decorators?")
```

---

## Safety Settings

### Harm Categories

| Category | Description |
|----------|-------------|
| `HARM_CATEGORY_HARASSMENT` | Harassment content |
| `HARM_CATEGORY_HATE_SPEECH` | Hate speech |
| `HARM_CATEGORY_SEXUALLY_EXPLICIT` | Sexually explicit content |
| `HARM_CATEGORY_DANGEROUS_CONTENT` | Dangerous content |

### Block Thresholds

| Threshold | Description |
|-----------|-------------|
| `BLOCK_NONE` | Always show content |
| `BLOCK_LOW_AND_ABOVE` | Block low probability and above |
| `BLOCK_MEDIUM_AND_ABOVE` | Block medium probability and above (default) |
| `BLOCK_ONLY_HIGH` | Block only high probability |

### Configuring Safety

```python
from google.generativeai.types import HarmCategory, HarmBlockThreshold

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    safety_settings={
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }
)

# Check safety ratings in response
response = model.generate_content("Your prompt")

if response.prompt_feedback.block_reason:
    print(f"Blocked: {response.prompt_feedback.block_reason}")
else:
    for rating in response.candidates[0].safety_ratings:
        print(f"{rating.category}: {rating.probability}")
```

---

## Error Handling

### Common Errors

```python
from google.generativeai.types import StopCandidateException, BlockedPromptException

try:
    response = model.generate_content("Your prompt")
    print(response.text)

except BlockedPromptException as e:
    print(f"Prompt blocked: {e}")

except StopCandidateException as e:
    print(f"Generation stopped: {e}")
    # Access partial response
    if e.args and e.args[0].content:
        print(f"Partial: {e.args[0].content.parts[0].text}")

except Exception as e:
    print(f"Error: {e}")
```

### Rate Limits

```python
import time
from google.api_core.exceptions import ResourceExhausted

def generate_with_retry(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            return model.generate_content(prompt)
        except ResourceExhausted:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Rate limited, waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
```

---

## Pricing (January 2026)

### Google AI Studio (API Key)

| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|-------|----------------------|------------------------|
| Gemini 2.0 Flash | $0.10 | $0.40 |
| Gemini 1.5 Pro | $1.25 (<128K) / $2.50 (>128K) | $5.00 (<128K) / $10.00 (>128K) |
| Gemini 1.5 Flash | $0.075 (<128K) / $0.15 (>128K) | $0.30 (<128K) / $0.60 (>128K) |
| Gemini 1.5 Flash-8B | $0.0375 | $0.15 |

### Context Caching Discount

| Model | Cached Input Price | Savings |
|-------|-------------------|---------|
| Gemini 1.5 Pro | $0.3125 (<128K) | 75% |
| Gemini 1.5 Flash | $0.01875 (<128K) | 75% |

### Free Tier

| Model | Free Requests/Minute | Free Requests/Day |
|-------|---------------------|-------------------|
| Gemini 1.5 Flash | 15 | 1,500 |
| Gemini 1.5 Pro | 2 | 50 |
| Gemini 2.0 Flash | 10 | 1,000 |

---

## Best Practices

### Prompt Engineering

1. **Be specific** - Clear instructions, expected format
2. **Use examples** - Few-shot prompting improves accuracy
3. **System instructions** - Set consistent behavior
4. **Structured output** - Use JSON mode for parsing

### Performance

1. **Choose right model** - Flash for speed, Pro for quality
2. **Use caching** - For repeated large contexts
3. **Batch requests** - When possible
4. **Stream responses** - For better UX

### Cost Optimization

1. **Use Flash models** - 10x cheaper than Pro
2. **Enable caching** - 75% savings on large contexts
3. **Limit output tokens** - Set max_output_tokens
4. **Compress prompts** - Remove unnecessary text

### Security

1. **Never expose API keys** - Use environment variables
2. **Validate inputs** - Sanitize user content
3. **Check safety ratings** - Handle blocked content
4. **Use Vertex AI** - For enterprise compliance

---


## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Gemini API authentication | haiku | Setup |
| Model capabilities | sonnet | Capability analysis |

## Sources

- [Google AI Studio](https://aistudio.google.com/)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Google AI Python SDK](https://github.com/google-gemini/generative-ai-python)

---

*Part of faion-ml-engineer skill*
*Last updated: 2026-01-23*
