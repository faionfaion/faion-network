# ML Engineer Domain Skill

## Overview

ML Engineer skill for AI/ML engineering activities. Covers LLM APIs (OpenAI, Claude, Gemini), embeddings, RAG systems, fine-tuning, vector databases, and AI frameworks (LangChain, LlamaIndex).

**Total:** 10 reference files, ~11,000 lines of technical documentation, 42 methodologies.

---

## Subfolders

| Folder | Description |
|--------|-------------|
| [methodologies/](methodologies/) | 42 methodology files (semantic naming) |
| [references/](references/) | Technical documentation for LLM APIs, embeddings, RAG, fine-tuning, frameworks, and vector databases |

---

## Key Files

| File | Purpose | Lines |
|------|---------|-------|
| [SKILL.md](SKILL.md) | Skill definition, methodologies, quick reference, code patterns | ~360 |
| [references/openai-api.md](references/openai-api.md) | OpenAI API: GPT-4, DALL-E, Whisper, Assistants, Batch | ~1310 |
| [references/claude-api.md](references/claude-api.md) | Claude API: Messages, tool use, extended thinking, vision | ~1420 |
| [references/gemini-api.md](references/gemini-api.md) | Gemini API: Multimodal, grounding, code execution, 2M context | ~1150 |
| [references/embeddings.md](references/embeddings.md) | Text embeddings: model comparison, chunking, similarity | ~900 |
| [references/finetuning.md](references/finetuning.md) | LLM fine-tuning: LoRA, QLoRA, datasets, evaluation | ~990 |
| [references/langchain.md](references/langchain.md) | LangChain/LangGraph: chains, agents, memory, tools | ~1440 |
| [references/llamaindex.md](references/llamaindex.md) | LlamaIndex: document indexing, query engines, RAG | ~1210 |
| [references/vector-databases.md](references/vector-databases.md) | Vector DBs: Qdrant, Weaviate, Chroma, pgvector, Pinecone | ~1390 |
| [references/rag.md](references/rag.md) | RAG pipelines: build, query, evaluate modes | ~500 |
| [references/best-practices-2026.md](references/best-practices-2026.md) | Agentic RAG, AI Agents, MCP, LLM observability | ~300 |

---

## Quick Reference

### LLM Provider Selection

| Provider | Best For | Context | Cost |
|----------|----------|---------|------|
| OpenAI | General purpose, vision, tools | 128K | $$$ |
| Claude | Long context, reasoning, safety | 200K | $$$ |
| Gemini | Multimodal, grounding, 2M context | 2M | $$ |
| Local (Ollama) | Privacy, no API costs | Varies | Free |

### Framework Selection

| Framework | Use Case |
|-----------|----------|
| LangChain | Complex chains, agents, many integrations |
| LlamaIndex | Document indexing, RAG, structured data |

### Vector Database Selection

| Database | Best For |
|----------|----------|
| Qdrant | Production self-hosted (recommended) |
| Weaviate | Knowledge graphs, hybrid search |
| Chroma | Local dev, prototyping |
| pgvector | Existing PostgreSQL integration |
| Pinecone | Fully managed, serverless |

---

## Methodologies (42)

See [methodologies/CLAUDE.md](methodologies/CLAUDE.md) for full listing.

**Categories:**
- **LLM API Integration (4):** openai-api-integration, claude-api-integration, gemini-api-integration, local-llm-ollama
- **RAG and Retrieval (7):** embedding-generation, vector-database-setup, rag-pipeline-design, rag-evaluation, hybrid-search, reranking, chunking-strategies
- **Fine-tuning (2):** fine-tuning-openai, fine-tuning-lora
- **Prompt Engineering (5):** prompt-engineering, chain-of-thought, tool-use-function-calling, structured-output, guardrails
- **Operations (3):** cost-optimization, model-evaluation, llm-observability
- **Frameworks (2):** langchain-patterns, llamaindex-patterns
- **Agents (4):** autonomous-agents, multi-agent-systems, ai-agent-patterns, multi-agent-design-patterns
- **Multimodal (6):** image-generation, image-analysis-vision, speech-to-text, text-to-speech, voice-agents, video-generation
- **Best Practices 2026 (9):** agentic-rag, decision-framework, mcp-model-context-protocol, ai-governance-compliance, graph-rag-advanced-retrieval, llm-observability-stack-2026, mcp-ecosystem-2026, eu-ai-act-compliance-2026, reasoning-first-architectures

---

## Agent

| Agent | Purpose |
|-------|---------|
| faion-ml-agent | AI/ML implementation and integration |

---

*ML Engineer Domain Skill v1.0*
