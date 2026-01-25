# ML Engineer Orchestrator

> **Entry Point:** Invoked via [/faion-net](../faion-net/CLAUDE.md) or directly as `/faion-ml-engineer`

## When to Use

- Any AI/ML engineering task
- Routes to specialized sub-skills automatically

## Overview

Orchestrates 5 specialized AI/ML sub-skills. Routes tasks based on intent.

**Sub-Skills:** 5 | **Total Methodologies:** 101

## Sub-Skills (5)

| Sub-Skill | Methodologies | Purpose |
|-----------|---------------|---------|
| [faion-llm-integration](../faion-llm-integration/SKILL.md) | 26 | LLM APIs, prompting, function calling |
| [faion-rag-engineer](../faion-rag-engineer/SKILL.md) | 22 | RAG, embeddings, vector search |
| [faion-ml-ops](../faion-ml-ops/SKILL.md) | 15 | Fine-tuning, evaluation, cost |
| [faion-ai-agents](../faion-ai-agents/SKILL.md) | 26 | Agents, multi-agent, MCP |
| [faion-multimodal-ai](../faion-multimodal-ai/SKILL.md) | 12 | Vision, image/video, speech |

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

## Files

| File | Purpose |
|------|---------|
| [SKILL.md](SKILL.md) | Orchestrator definition |
| [decision-framework.md](decision-framework.md) | ML choices framework |
| [llm-decision-framework.md](llm-decision-framework.md) | LLM provider selection |

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [faion-net](../faion-net/CLAUDE.md) | Parent orchestrator |
| [faion-software-developer](../faion-software-developer/CLAUDE.md) | Integrates ML into applications |
| [faion-devops-engineer](../faion-devops-engineer/CLAUDE.md) | Deploys ML models |
| [faion-claude-code](../faion-claude-code/CLAUDE.md) | MCP server setup |

---

<<<<<<< HEAD
## Structure

All files are now in the skill root (flat structure). Files with naming conflicts use prefixes:
- `ref-*` - reference files
- `meth-*` - methodology files

---

## Key Files

| File | Purpose | Lines |
|------|---------|-------|
| [SKILL.md](SKILL.md) | Skill definition, methodologies, quick reference, code patterns | ~360 |
| [openai-api.md](openai-api.md) | OpenAI API: GPT-4, DALL-E, Whisper, Assistants, Batch | ~1310 |
| [claude-api.md](claude-api.md) | Claude API: Messages, tool use, extended thinking, vision | ~1420 |
| [gemini-api.md](gemini-api.md) | Gemini API: Multimodal, grounding, code execution, 2M context | ~1150 |
| [embeddings.md](embeddings.md) | Text embeddings: model comparison, chunking, similarity | ~900 |
| [finetuning.md](finetuning.md) | LLM fine-tuning: LoRA, QLoRA, datasets, evaluation | ~990 |
| [langchain.md](langchain.md) | LangChain/LangGraph: chains, agents, memory, tools | ~1440 |
| [llamaindex.md](llamaindex.md) | LlamaIndex: document indexing, query engines, RAG | ~1210 |
| [vector-databases.md](vector-databases.md) | Vector DBs: Qdrant, Weaviate, Chroma, pgvector, Pinecone | ~1390 |
| [rag.md](rag.md) | RAG pipelines: build, query, evaluate modes | ~500 |
| [ref-agentic-rag.md](ref-agentic-rag.md) | Agentic RAG, AI Agents, MCP, LLM observability | ~300 |

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

See [meth-CLAUDE.md](meth-CLAUDE.md) for full listing.

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
=======
*ML Engineer Domain Skill v1.2*
>>>>>>> claude
