---
id: local-llm-ollama
name: "Local LLM (Ollama)"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
version: "2.0.0"
updated: "2026-01"
---

# Local LLM with Ollama

## Overview

Ollama is an open-source platform for running Large Language Models (LLMs) locally. It bundles model weights, configuration, and data into a single Modelfile package (similar to Docker). Supports NVIDIA (CUDA), Apple Silicon (Metal), and AMD (ROCm) GPUs.

**Default endpoint:** `http://localhost:11434`

## When to Use

| Use Case | Benefit |
|----------|---------|
| Data privacy requirements | No external API calls |
| Offline/air-gapped environments | Full offline capability |
| High-volume tasks | Zero API costs |
| Development/testing | No rate limits |
| Custom fine-tuned models | Local deployment |
| Edge computing | Low latency |
| Compliance requirements | Data stays on-premise |

## Key Capabilities (2025-2026)

| Feature | Status |
|---------|--------|
| Chat/Generation API | Stable |
| OpenAI-compatible API | Stable |
| Tool/Function Calling | Stable |
| Structured Outputs (JSON Schema) | Stable |
| Vision Models | Stable |
| Embeddings | Stable |
| Streaming | Stable |
| MCP Integration | Stable |
| Multi-GPU Support | Stable |

## Model Categories

### General Purpose

| Model | Sizes | RAM Required | Best For |
|-------|-------|--------------|----------|
| Llama 4 | 109B, 400B | 64GB+ | Complex reasoning |
| Llama 3.3 | 70B | 48GB | High-quality general |
| Llama 3.2 | 1B, 3B | 4-8GB | Lightweight general |
| Llama 3.1 | 8B, 70B, 405B | 8-256GB | Balanced performance |
| Gemma 3 | 1B-27B | 2-32GB | Google's efficient models |
| Qwen 2.5 | 0.5B-72B | 2-64GB | Multilingual |
| Phi 4 | 14B | 16GB | Microsoft research |
| Mistral | 7B | 8GB | Fast, efficient |
| DeepSeek-R1 | 7B-671B | 8-512GB | Reasoning chains |

### Vision Models

| Model | Sizes | Capabilities |
|-------|-------|--------------|
| Llama 3.2 Vision | 11B, 90B | Image reasoning |
| Qwen 3 VL | 2B-235B | Advanced vision-language |
| Qwen 2.5 VL | 3B-72B | Flagship vision |
| LLaVA | 7B, 13B, 34B | Visual Q&A |
| Moondream | 1.8B | Edge vision |
| MiniCPM-V | 8B | Multimodal |

### Coding Models

| Model | Sizes | Specialization |
|-------|-------|----------------|
| DeepSeek Coder V2 | 16B, 236B | GPT-4 level coding |
| Qwen 2.5 Coder | 0.5B-32B | Code generation |
| CodeLlama | 7B-70B | Meta's code model |
| StarCoder 2 | 3B-15B | Open-source code |

### Embedding Models

| Model | Parameters | Dimensions | Use Case |
|-------|------------|------------|----------|
| nomic-embed-text | 137M | 768 | Large context |
| mxbai-embed-large | 335M | 1024 | High performance |
| bge-m3 | 567M | 1024 | Multilingual |
| all-minilm | 22M-33M | 384 | Lightweight |

### Small Models (Under 4GB)

| Model | Size | RAM | Best For |
|-------|------|-----|----------|
| Phi 4 Mini | 3.8B | 4GB | Function calling |
| TinyLlama | 1.1B | 2GB | Ultra-light |
| SmolLM 2 | 135M-1.7B | 1-3GB | Edge devices |
| Gemma 3n | e2b, e4b | 2-4GB | Everyday devices |

## File Structure

```
local-llm-ollama/
├── README.md           # This file
├── checklist.md        # Implementation checklist
├── examples.md         # Code examples (Python, async, streaming)
├── templates.md        # Modelfile and config templates
└── llm-prompts.md      # System prompts and prompt engineering
```

## Quick Start

```bash
# Install (Linux)
curl -fsSL https://ollama.com/install.sh | sh

# Start server
ollama serve

# Pull model
ollama pull llama3.1:8b

# Test
ollama run llama3.1:8b "Hello!"
```

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/generate` | POST | Text generation |
| `/api/chat` | POST | Chat completion |
| `/api/embeddings` | POST | Generate embeddings |
| `/api/tags` | GET | List models |
| `/api/pull` | POST | Download model |
| `/api/create` | POST | Create custom model |
| `/api/delete` | DELETE | Remove model |
| `/api/show` | POST | Model info |
| `/v1/chat/completions` | POST | OpenAI-compatible |

## Hardware Requirements

| Model Size | Min RAM | Recommended | GPU VRAM |
|------------|---------|-------------|----------|
| 1-3B | 4GB | 8GB | 4GB |
| 7-8B | 8GB | 16GB | 8GB |
| 13B | 16GB | 24GB | 12GB |
| 30B | 32GB | 48GB | 24GB |
| 70B | 48GB | 64GB | 48GB |
| 400B+ | 256GB+ | 512GB | 256GB+ |

## Best Practices

1. **Model Selection** - Match model size to available RAM/VRAM
2. **Quantization** - Use Q4/Q5 versions for memory savings (15-30% quality trade-off)
3. **Context Window** - 32k+ improves tool calling reliability
4. **Keep Models Loaded** - Avoid frequent model swaps
5. **Health Checks** - Monitor `/api/tags` for availability
6. **Timeouts** - Large models need 60-120s for first response

## Common Issues

| Issue | Solution |
|-------|----------|
| Model won't load | Check RAM, use smaller model or quantized version |
| Slow inference | Enable GPU, check CUDA/Metal detection |
| Server not responding | Run `ollama serve`, check port 11434 |
| Truncated output | Increase `num_ctx` in options |
| OOM errors | Reduce context window or batch size |
| Tool calling fails | Use 32k+ context, Llama 3.1+ recommended |

## References

- [Ollama Official Site](https://ollama.com/)
- [Ollama GitHub](https://github.com/ollama/ollama)
- [Ollama Model Library](https://ollama.com/library)
- [Ollama Python Library](https://github.com/ollama/ollama-python)
- [Tool Calling Docs](https://docs.ollama.com/capabilities/tool-calling)
- [Structured Outputs Blog](https://ollama.com/blog/structured-outputs)

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Ollama setup | haiku | Installation |
| Model loading | haiku | Configuration |
| Performance optimization | sonnet | Tuning expertise |
