---
name: faion-ml-engineer
description: "ML Engineer orchestrator: routes to 5 specialized sub-skills (LLM integration, RAG, ML Ops, AI Agents, Multimodal). 101 total methodologies."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion, TodoWrite, Skill
---

# ML Engineer Orchestrator

**Communication: User's language. Code: English.**

## Purpose

Routes AI/ML tasks to specialized sub-skills. Orchestrates LLM integration, RAG, operations, agents, and multimodal AI.

## Sub-Skills (5)

| Sub-Skill | Purpose | Methodologies |
|-----------|---------|---------------|
| **faion-llm-integration** | LLM APIs, prompting, function calling | 26 |
| **faion-rag-engineer** | RAG systems, embeddings, vector search | 22 |
| **faion-ml-ops** | Fine-tuning, evaluation, cost, observability | 15 |
| **faion-ai-agents** | Autonomous agents, multi-agent, MCP | 26 |
| **faion-multimodal-ai** | Vision, image/video gen, speech, TTS | 12 |

**Total: 101 methodologies**

## Routing Logic

| Task Type | Route To |
|-----------|----------|
| OpenAI/Claude/Gemini API integration | faion-llm-integration |
| Prompt engineering, CoT, guardrails | faion-llm-integration |
| RAG pipeline, embeddings, chunking | faion-rag-engineer |
| Vector databases, hybrid search | faion-rag-engineer |
| Fine-tuning, LoRA, evaluation | faion-ml-ops |
| Cost optimization, observability | faion-ml-ops |
| Agents, multi-agent, LangChain | faion-ai-agents |
| MCP, agent architectures | faion-ai-agents |
| Vision, image/video generation | faion-multimodal-ai |
| Speech-to-text, TTS, voice | faion-multimodal-ai |

## Execution Protocol

<<<<<<< HEAD
| Reference | Content | Lines |
|-----------|---------|-------|
| [openai-api.md](openai-api.md) | GPT-4, DALL-E, Whisper, Assistants | ~1310 |
| [claude-api.md](claude-api.md) | Claude models, tool use, extended thinking | ~1420 |
| [gemini-api.md](gemini-api.md) | Gemini models, multimodal, grounding | ~1150 |
| [embeddings.md](embeddings.md) | Text embeddings, similarity, chunking | ~900 |
| [finetuning.md](finetuning.md) | Model fine-tuning, datasets, evaluation | ~990 |
| [langchain.md](langchain.md) | Chains, agents, memory, tools | ~1440 |
| [llamaindex.md](llamaindex.md) | Document indexing, query engines | ~1210 |
| [vector-databases.md](vector-databases.md) | Pinecone, Weaviate, Chroma, pgvector | ~1390 |
| [ref-agentic-rag.md](ref-agentic-rag.md) | Agentic RAG, AI Agents, LLM Management, MCP | ~300 |
=======
When a task arrives:
>>>>>>> claude

1. **Analyze task intent**
2. **Select appropriate sub-skill** (use routing table above)
3. **Invoke sub-skill** with Skill tool
4. **Return results** to caller

## Quick Reference

| Provider | Best For | Context | Sub-Skill |
|----------|----------|---------|-----------|
| OpenAI | General, vision, tools | 128K | faion-llm-integration |
| Claude | Long context, reasoning | 200K | faion-llm-integration |
| Gemini | Multimodal, 2M context | 2M | faion-llm-integration |
| Local | Privacy, offline | Varies | faion-llm-integration |

| Task | Sub-Skill |
|------|-----------|
| RAG pipeline | faion-rag-engineer |
| Vector DB (Qdrant, Weaviate) | faion-rag-engineer |
| Fine-tuning | faion-ml-ops |
| Cost optimization | faion-ml-ops |
| Agents (ReAct, multi-agent) | faion-ai-agents |
| LangChain/LlamaIndex | faion-ai-agents |
| Vision, image gen | faion-multimodal-ai |
| Speech, TTS | faion-multimodal-ai |

## Related Skills

| Skill | Relationship |
|-------|-------------|
| faion-software-developer | Application integration |
| faion-devops-engineer | Model deployment |

---

*ML Engineer Orchestrator v2.0*
*5 Sub-Skills | 101 Total Methodologies*
