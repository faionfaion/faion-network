# ML Engineer

> **Entry point:** `/faion-net` — invoke for automatic routing.

AI/ML orchestrator: LLM APIs, RAG, fine-tuning, agents, multimodal AI.

## Sub-Skills

| Sub-Skill | Focus | Methodologies |
|-----------|-------|---------------|
| [faion-llm-integration](../faion-llm-integration/CLAUDE.md) | OpenAI, Claude, Gemini APIs, prompting | 20 |
| [faion-rag-engineer](../faion-rag-engineer/CLAUDE.md) | RAG, embeddings, vector DBs | 18 |
| [faion-ml-ops](../faion-ml-ops/CLAUDE.md) | Fine-tuning, evaluation, cost | 15 |
| [faion-ai-agents](../faion-ai-agents/CLAUDE.md) | Agents, multi-agent, MCP | 15 |
| [faion-multimodal-ai](../faion-multimodal-ai/CLAUDE.md) | Vision, image/video, speech | 12 |

**Total:** 80 methodologies

## Routing

| Task Type | Sub-Skill |
|-----------|-----------|
| OpenAI/Claude/Gemini API | faion-llm-integration |
| Prompts, CoT, guardrails | faion-llm-integration |
| RAG, embeddings, chunking | faion-rag-engineer |
| Vector DBs, hybrid search | faion-rag-engineer |
| Fine-tuning, LoRA | faion-ml-ops |
| Cost, evaluation, observability | faion-ml-ops |
| Agents, LangChain, LlamaIndex | faion-ai-agents |
| MCP, agent architectures | faion-ai-agents |
| Vision, image/video gen | faion-multimodal-ai |
| Speech, TTS, voice | faion-multimodal-ai |

## Quick Reference

**LLM Provider Selection:**

| Provider | Best For | Context |
|----------|----------|---------|
| OpenAI | General purpose, vision, tools | 128K |
| Claude | Long context, reasoning, safety | 200K |
| Gemini | Multimodal, grounding | 2M |
| Local (Ollama) | Privacy, no API costs | Varies |

**Vector Database Selection:**

| Database | Best For |
|----------|----------|
| Qdrant | Production self-hosted |
| Weaviate | Knowledge graphs, hybrid search |
| Chroma | Local dev, prototyping |
| pgvector | Existing PostgreSQL |
| Pinecone | Fully managed, serverless |

## Files

| File | Purpose |
|------|---------|
| [SKILL.md](SKILL.md) | Orchestrator definition |
| [decision-framework/](decision-framework/README.md) | ML/model selection framework (checklist, examples, templates, prompts) |
| [llm-decision-framework/](llm-decision-framework/README.md) | LLM architecture decisions (RAG vs fine-tuning, deployment strategies, cost analysis) |
| [cost-optimization/](cost-optimization/README.md) | Cost optimization (routing, caching, batching, tokens) |
| [finetuning/](finetuning/README.md) | Fine-tuning guide (LoRA, QLoRA, frameworks) |
| [fine-tuning-openai/](fine-tuning-openai/README.md) | OpenAI fine-tuning (GPT-4.1, SFT, DPO, evaluation) |
| [model-evaluation/](model-evaluation/README.md) | Model evaluation (benchmarks, LLM-as-judge, A/B testing) |
| [llm-observability/](llm-observability/README.md) | LLM observability (Langfuse, LangSmith, tracing, monitoring) |
| [llm-observability-stack/](llm-observability-stack/README.md) | Observability stack (OTEL, Prometheus, Grafana, integration patterns) |
| [image-generation/](image-generation/README.md) | Image generation (DALL-E 3, Stable Diffusion, Flux, prompts) |
| [video-generation/](video-generation/README.md) | Video generation (Runway, Luma, Sora, Veo, text-to-video) |
| [text-to-speech/](text-to-speech/README.md) | TTS (OpenAI, ElevenLabs, voice cloning, streaming) |
| [voice-agents/](voice-agents/README.md) | Voice agents (real-time, telephony, Retell, LiveKit, Vapi) |
| [eu-ai-act-compliance/](eu-ai-act-compliance/README.md) | EU AI Act compliance (risk classification, documentation, templates) |
| [ai-governance-compliance/](ai-governance-compliance/README.md) | AI governance (model governance, audit trails, responsible AI, compliance) |
| [reasoning-first-architectures/](reasoning-first-architectures/README.md) | Reasoning models (o3, Claude ET, DeepSeek R1, CoT, extended thinking) |
| [vector-database-setup/](vector-database-setup/README.md) | Vector DB setup, deployment, configuration, production hardening |
| [vector-databases/](vector-databases/README.md) | Vector DB comparison, selection, code examples |

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [faion-software-developer](../faion-software-developer/CLAUDE.md) | Integrates ML into applications |
| [faion-devops-engineer](../faion-devops-engineer/CLAUDE.md) | Deploys ML models |
| [faion-claude-code](../faion-claude-code/CLAUDE.md) | MCP server setup |
