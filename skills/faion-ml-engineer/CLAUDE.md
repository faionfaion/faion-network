# ML Engineer Domain Skill

## Overview

ML Engineer skill for AI/ML engineering activities. Covers LLM APIs (OpenAI, Claude, Gemini), embeddings, RAG systems, fine-tuning, vector databases, and AI frameworks (LangChain, LlamaIndex).

**Total:** 10 reference files, ~11,000 lines of technical documentation, 24 methodologies.

---

## Subfolders

| Folder | Description |
|--------|-------------|
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

## Methodologies

- **M-LLM-001 to M-LLM-006:** Prompt engineering, structured output, streaming, token optimization, error handling, rate limiting
- **M-EMB-001 to M-EMB-004:** Chunking strategies, similarity search, hybrid search, reranking
- **M-RAG-001 to M-RAG-006:** Document processing, index design, query processing, context assembly, response generation, evaluation
- **M-FT-001 to M-FT-004:** Dataset preparation, training configuration, evaluation metrics, deployment
- **M-AGT-001 to M-AGT-004:** Tool design, agent loop, memory management, multi-agent systems

---

## Agent

| Agent | Purpose |
|-------|---------|
| faion-ml-agent | AI/ML implementation and integration |

---

*ML Engineer Domain Skill v1.0*
