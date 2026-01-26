# Google Gemini API

**Complete Guide to Google Gemini API for Multimodal AI Applications (2025-2026)**

> **Entry point:** `/faion-net` - invoke for automatic routing.

---

## Quick Reference

| Area | Key Elements |
|------|--------------|
| **Models** | Gemini 3 Pro/Flash, 2.0 Flash, 1.5 Pro (2M context), 1.5 Flash |
| **Multimodal** | Text, images, video (native), audio (native), PDFs, code |
| **Function Calling** | Tool declarations, parallel calls, multimodal responses |
| **Live API** | Real-time voice/video, WebSocket streaming, VAD |
| **Code Execution** | Python sandbox, charts, data analysis |
| **Grounding** | Google Search, document retrieval |
| **Caching** | Context caching for 75% cost reduction |
| **Embeddings** | text-embedding-004, multimodal embeddings |

---

## Model Overview (January 2026)

| Model | Context | Strengths | Use Cases |
|-------|---------|-----------|-----------|
| **Gemini 3 Pro** | 1M+ | Most intelligent, reasoning, thinking | Complex tasks, agents |
| **Gemini 3 Flash** | 1M+ | Fast + smart, dynamic thinking | Production apps |
| **Gemini 2.0 Flash** | 1M | Fast, multimodal, agentic | Real-time apps, agents |
| **Gemini 1.5 Pro** | 2M | Largest context, balanced | Long documents, codebases |
| **Gemini 1.5 Flash** | 1M | Cost-effective, fast | High-volume, production |
| **Gemini 1.5 Flash-8B** | 1M | Smallest, cheapest | Simple tasks, edge |

### Model Selection

```
Need reasoning/intelligence? -> Gemini 3 Pro
Need speed + intelligence?   -> Gemini 3 Flash
Need fastest response?       -> Gemini 2.0 Flash
Need largest context?        -> Gemini 1.5 Pro (2M tokens)
Need cost efficiency?        -> Gemini 1.5 Flash-8B
```

---

## Gemini 3 New Features

### Dynamic Thinking

Gemini 3 uses dynamic thinking by default. Control reasoning depth with `thinking_level`:

| Level | Description | Best For |
|-------|-------------|----------|
| `low` | Minimize latency/cost | Simple tasks |
| `medium` (Flash) | Balanced reasoning | General use |
| `high` (default) | Maximum reasoning depth | Complex problems |
| `minimal` (Flash) | No thinking | Speed-critical |

### Media Resolution Control

Control token allocation per image/video frame with `media_resolution`:

| Resolution | Use Case |
|------------|----------|
| `low` | Simple images, cost savings |
| `medium` | PDFs (often saturates here) |
| `high` | Detailed images (recommended) |
| `ultra-high` | Maximum fidelity |

### Thought Signatures

Encrypted reasoning representations for multi-turn conversations. **Required** even when thinking level is minimal.

### Multimodal Function Responses

Function responses can now include images, videos, PDFs alongside text.

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
pip install google-cloud-aiplatform
gcloud auth application-default login
```

```python
import vertexai
from vertexai.generative_models import GenerativeModel

vertexai.init(project="your-project-id", location="us-central1")
model = GenerativeModel("gemini-1.5-pro")
```

---

## Core Capabilities

| Capability | File |
|------------|------|
| Chat conversations | [examples.md](examples.md) |
| Multimodal (image/video/audio) | [examples.md](examples.md) |
| Streaming responses | [examples.md](examples.md) |
| Function calling | [examples.md](examples.md) |
| Live API (real-time) | [examples.md](examples.md) |
| Context caching | [examples.md](examples.md) |
| Embeddings | [examples.md](examples.md) |

---

## Files in This Folder

| File | Purpose |
|------|---------|
| [README.md](README.md) | Overview and quick reference |
| [checklist.md](checklist.md) | Implementation checklist |
| [examples.md](examples.md) | Code examples for all features |
| [templates.md](templates.md) | Copy-paste templates |
| [llm-prompts.md](llm-prompts.md) | Prompts for AI assistants |

---

## Pricing (January 2026)

### Google AI Studio

| Model | Input (per 1M) | Output (per 1M) |
|-------|----------------|-----------------|
| Gemini 3 Pro | $1.25 | $5.00 |
| Gemini 3 Flash | $0.10 | $0.40 |
| Gemini 2.0 Flash | $0.10 | $0.40 |
| Gemini 1.5 Pro | $1.25 / $2.50 | $5.00 / $10.00 |
| Gemini 1.5 Flash | $0.075 / $0.15 | $0.30 / $0.60 |

### Context Caching

| Model | Cached Price | Savings |
|-------|--------------|---------|
| Gemini 1.5 Pro | $0.3125 | 75% |
| Gemini 1.5 Flash | $0.01875 | 75% |

### Free Tier

| Model | RPM | RPD |
|-------|-----|-----|
| Gemini 3 Flash | 10 | 1,000 |
| Gemini 2.0 Flash | 10 | 1,000 |
| Gemini 1.5 Flash | 15 | 1,500 |
| Gemini 1.5 Pro | 2 | 50 |

---

## Best Practices

### Prompt Engineering

1. **Be specific** - Clear instructions, expected format
2. **Use examples** - Few-shot prompting improves accuracy
3. **System instructions** - Set consistent behavior
4. **Structured output** - Use JSON mode for parsing

### Gemini 3 Prompting

1. **Simplified prompts** - Gemini 3 handles simpler prompts better
2. **Default temperature** - Use default 1.0, remove explicit settings
3. **Let it think** - Use appropriate thinking level for task complexity

### Performance

1. **Choose right model** - Flash for speed, Pro for quality
2. **Use caching** - For repeated large contexts (75% savings)
3. **Batch requests** - When possible
4. **Stream responses** - For better UX

### Security

1. **Never expose API keys** - Use environment variables
2. **Validate inputs** - Sanitize user content
3. **Check safety ratings** - Handle blocked content
4. **Use Vertex AI** - For enterprise compliance

---

## API Comparison

| Feature | Gemini | OpenAI GPT-4 | Claude |
|---------|--------|--------------|--------|
| Max Context | 2M tokens | 128K tokens | 200K tokens |
| Native Video | Yes | No | No |
| Native Audio | Yes | Via Whisper | No |
| Live API | Yes | Realtime API | No |
| Code Execution | Yes | Via tools | No |
| Search Grounding | Yes | Via tools | Via tools |
| Context Caching | Yes | No | Yes |

---

## Sources

- [Google AI Studio](https://aistudio.google.com/)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Gemini 3 Developer Guide](https://ai.google.dev/gemini-api/docs/gemini-3)
- [Live API](https://ai.google.dev/gemini-api/docs/live)
- [Function Calling](https://ai.google.dev/gemini-api/docs/function-calling)
- [Vertex AI Generative AI](https://cloud.google.com/vertex-ai/generative-ai/docs)
- [Google AI Python SDK](https://github.com/google-gemini/generative-ai-python)
- [Gemini Cookbook](https://github.com/google-gemini/gemini-api-cookbook)

---

*Last updated: 2026-01-25*
