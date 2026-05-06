---
name: faion-ml-engineer
description: "ML/AI orchestrator: LLM integration, RAG, ML Ops, agents, multimodal."
tier: geek
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion, TodoWrite, Skill
---
> Part of **faion** umbrella — read on-demand, not individually invocable.

# ML Engineer Orchestrator

**Communication: User's language. Code: English.**

## Purpose

Routes AI/ML tasks to specialized sub-skills. Orchestrates LLM integration, RAG, operations, agents, and multimodal AI.

---

## Context Discovery

### Auto-Investigation

Check for existing AI/ML setup:

| Signal | How to Check | What It Tells Us |
|--------|--------------|------------------|
| `openai` in dependencies | `Grep("openai", "**/requirements.txt")` | OpenAI SDK used |
| `anthropic` in dependencies | `Grep("anthropic", "**/requirements.txt")` | Claude SDK used |
| `langchain` in dependencies | `Grep("langchain", "**/requirements.txt")` | LangChain framework |
| `llamaindex` in dependencies | `Grep("llama-index", "**/requirements.txt")` | LlamaIndex framework |
| Vector DB config | `Grep("qdrant\|chroma\|pinecone\|weaviate", "**/*")` | Vector DB setup exists |
| Embedding models | `Grep("embed\|embedding", "**/*.py")` | Embeddings used |
| `.env` with API keys | `Grep("OPENAI_API_KEY\|ANTHROPIC_API_KEY", "**/.env*")` | Which APIs configured |

### Discovery Questions

Use `AskUserQuestion` to understand AI/ML requirements.

#### Q1: AI/ML Goal

```yaml
question: "What do you want to achieve with AI/ML?"
header: "Goal"
multiSelect: false
options:
  - label: "Use LLM APIs (chat, generation)"
    description: "Integrate OpenAI, Claude, or Gemini"
  - label: "Build RAG system (knowledge base)"
    description: "Search and retrieve from documents"
  - label: "Create AI agent (autonomous tasks)"
    description: "Agent that uses tools and reasons"
  - label: "Fine-tune a model"
    description: "Train model on custom data"
  - label: "Add vision/image/voice"
    description: "Multimodal AI capabilities"
```

**Routing:**
- "LLM APIs" → `Skill(faion-llm-integration)`
- "RAG system" → `Skill(faion-rag-engineer)`
- "AI agent" → `Skill(faion-ai-agents)`
- "Fine-tune" → `Skill(faion-ml-ops)`
- "Multimodal" → `Skill(faion-multimodal-ai)`

#### Q2: LLM Provider Preference (if LLM task)

```yaml
question: "Which LLM provider do you prefer?"
header: "Provider"
multiSelect: false
options:
  - label: "OpenAI (GPT-4)"
    description: "Best general purpose, good tools support"
  - label: "Anthropic (Claude)"
    description: "Best for long context, reasoning, safety"
  - label: "Google (Gemini)"
    description: "Multimodal, 2M context, grounding"
  - label: "Local (Ollama)"
    description: "Privacy, no API costs, offline"
  - label: "Not sure / recommend"
    description: "I'll suggest based on your use case"
```

#### Q3: Data Situation (if RAG or fine-tuning)

```yaml
question: "What data do you have?"
header: "Data"
multiSelect: true
options:
  - label: "Documents (PDF, markdown, text)"
    description: "Unstructured text content"
  - label: "Structured data (database, CSV)"
    description: "Tabular or relational data"
  - label: "Code repositories"
    description: "Source code to search/understand"
  - label: "Conversation logs"
    description: "Chat history, support tickets"
```

**Routing:**
- "Documents" → RAG with chunking strategies
- "Structured data" → Text-to-SQL or structured RAG
- "Code repos" → Code embeddings, AST-aware chunking
- "Conversations" → Fine-tuning dataset prep

#### Q4: Deployment Requirements

```yaml
question: "How will this be deployed?"
header: "Deploy"
multiSelect: false
options:
  - label: "API endpoint (backend service)"
    description: "Part of web application"
  - label: "CLI tool"
    description: "Command-line interface"
  - label: "Batch processing"
    description: "Process data in bulk"
  - label: "Real-time/streaming"
    description: "Live interactions, low latency"
```

**Context impact:**
- "API endpoint" → Async patterns, rate limiting, caching
- "CLI tool" → Simple integration, local models option
- "Batch processing" → Cost optimization, parallel processing
- "Real-time" → Streaming responses, edge deployment

---

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

When a task arrives:

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

## Methodologies (70)

Orchestrator-local methodology folders co-located with this KB.

**Agents (8):**
- `ai-agent-patterns`: Core agent design patterns
- `agents-framework-selection`: Pick LangChain / LlamaIndex / native
- `agents-react-pattern`: ReAct reasoning + acting loop
- `agents-memory-system`: Short / long memory layers
- `agents-safety-guardrails`: Agent-level safety controls
- `agents-production-deployment`: Deploy agents to prod
- `multi-agent-systems`: Multi-agent coordination
- `multi-agent-design-patterns`: Hierarchical, peer, sequential

**RAG & Retrieval (6):**
- `rag`: RAG fundamentals
- `rag-pipeline-design`: End-to-end pipeline shape
- `rag-evaluation`: Eval metrics, frameworks
- `agentic-rag`: Agent-driven retrieval
- `graph-rag`: Knowledge-graph augmented RAG
- `hybrid-search`: Vector + keyword search
- `reranking`: Cross-encoder reranking
- `chunking-strategies`: Chunking patterns

**Embeddings (5):**
- `embedding-generation`: Generate vectors via API
- `embeddings-provider-apis`: OpenAI / Voyage / Cohere
- `embeddings-model-selection`: Pick model by task / cost
- `embeddings-batch-and-cache`: Batching and cache layer
- `embeddings-evaluation`: Eval embedding quality
- `embeddings-production-ops`: Run embeddings in prod

**Vector Databases (6):**
- `vector-databases`: Comparison and selection
- `vector-db-setup-dev`: Local / dev setup
- `vector-db-setup-prod`: Production deployment
- `vector-db-index-tuning`: Index params, recall vs latency
- `vector-db-monitoring`: Health, drift, freshness
- `vector-db-security`: Auth, isolation, encryption

**LLM Providers (3):**
- `openai-api`: OpenAI SDK integration
- `claude-api`: Anthropic SDK integration
- `gemini-api`: Google AI SDK integration

**Prompt Engineering (5):**
- `prompt-engineering-fundamentals`: Structure, few-shot
- `prompt-engineering-reasoning`: CoT, ToT, reflection
- `prompt-engineering-production`: Versioning, templates
- `prompt-engineering-evaluation`: Test prompts at scale
- `prompt-engineering-security`: Injection / jailbreak defense
- `chain-of-thought`: CoT reasoning patterns
- `structured-output`: JSON / schema-constrained output
- `tool-use-function-calling`: Tool definitions, dispatch

**MCP (5):**
- `mcp-architecture`: Protocol architecture
- `mcp-server-implementation`: Build an MCP server
- `mcp-client-integration`: Connect Claude Code / clients
- `mcp-dev-prompts`: Prompts inside MCP servers
- `mcp-security`: Auth, capability scopes

**Guardrails (5):**
- `guardrails-concepts`: Why and what to guard
- `guardrails-ai-framework`: Guardrails AI library
- `guardrails-nemo`: NVIDIA NeMo Guardrails
- `guardrails-custom-pipeline`: Build custom guardrail chain
- `guardrails-testing`: Red-team and regression tests

**Fine-tuning (6):**
- `fine-tuning-lora`: LoRA / QLoRA workflow
- `fine-tuning-openai-data-prep`: Dataset shaping
- `fine-tuning-openai-sft`: Supervised fine-tuning
- `fine-tuning-openai-dpo`: Preference tuning
- `fine-tuning-openai-eval`: Eval before / after
- `fine-tuning-openai-deployment`: Ship fine-tuned model

**Ollama / Local (6):**
- `ollama-setup-models`: Install and pull models
- `ollama-deployment`: Production deployment
- `ollama-python-client`: Python integration
- `ollama-prompt-engineering`: Local-model prompting
- `ollama-tool-calling`: Tool calling on local LLMs
- `ollama-agent-integration`: Use Ollama inside an agent

**Vision (5):**
- `vision-provider-selection`: Pick vision provider
- `vision-document-extraction`: PDF / form extraction
- `vision-classification-moderation`: Tagging, moderation
- `vision-accessibility`: Alt-text, screen-reader support
- `vision-agentic-pipeline`: Agent-driven vision pipeline

**Video Generation (4):**
- `video-generation-provider-selection`: Pick provider
- `video-generation-prompt-engineering`: Prompt for video
- `video-generation-async-api`: Long-running async jobs
- `video-generation-production-service`: Production service

**Speech (1):**
- `speech-to-text`: STT providers, streaming

**Governance (2):**
- `ai-governance-compliance`: Org-level governance
- `eu-ai-act-compliance`: EU AI Act tiers, duties
- `reasoning-first-architectures`: Extended-thinking design

## Related Skills

| Skill | Relationship |
|-------|-------------|
| faion-software-developer | Application integration |
| faion-devops-engineer | Model deployment |

---

*ML Engineer Orchestrator v2.0*
*5 Sub-Skills | 101 Total Methodologies*
