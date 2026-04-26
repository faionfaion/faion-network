# LlamaIndex RAG Framework

**Build Production-Ready RAG Pipelines and Agentic Systems (2025-2026)**

---

## Overview

LlamaIndex is a data framework for building LLM applications that connect to custom data sources. It evolved from a pure RAG framework to a comprehensive platform for building agentic systems with data-aware capabilities.

**Core Mission:** Enable LLMs to understand and reason over your private data.

---

## Key Concepts

### 1. Data Connectors (Readers)

Load data from various sources into LlamaIndex Documents.

| Connector | Description |
|-----------|-------------|
| SimpleDirectoryReader | Files from local directories |
| WebPageReader | Web pages and URLs |
| NotionPageReader | Notion pages and databases |
| DatabaseReader | SQL databases |
| GithubRepositoryReader | GitHub repositories |
| LlamaHub (1500+) | Third-party connectors |

### 2. Indexes

Data structures that organize your documents for efficient retrieval.

| Index Type | Use Case | Strength |
|------------|----------|----------|
| **VectorStoreIndex** | Semantic search | Most versatile, default choice |
| **PropertyGraphIndex** | Entity relationships | Complex reasoning, GraphRAG |
| **KeywordTableIndex** | Exact keyword matching | Lexical search (BM25) |
| **SummaryIndex** | Full document context | Small docs, summarization |
| **TreeIndex** | Hierarchical structure | Multi-level summarization |

### 3. Query Engines

Process queries and synthesize responses from retrieved context.

| Engine | Description |
|--------|-------------|
| **Basic QueryEngine** | Standard RAG: retrieve + synthesize |
| **RouterQueryEngine** | Routes to appropriate sub-engine |
| **SubQuestionQueryEngine** | Decomposes complex queries |
| **SQLQueryEngine** | Natural language to SQL |

### 4. Workflows (Event-Driven Architecture)

Event-driven, async-first workflow engine for multi-step AI processes.

```python
from llama_index.core.workflow import Workflow, StartEvent, StopEvent, step

class RAGWorkflow(Workflow):
    @step
    async def retrieve(self, ev: StartEvent) -> RetrieveEvent:
        nodes = await self.retriever.aretrieve(ev.query)
        return RetrieveEvent(nodes=nodes)

    @step
    async def synthesize(self, ev: RetrieveEvent) -> StopEvent:
        response = await self.synthesizer.asynthesize(ev.query, ev.nodes)
        return StopEvent(result=response)
```

**Key Benefits:**
- Async-first design integrates with FastAPI
- Event-driven for complex control flows
- Stateful: launch, pause, resume workflows
- Type-safe with Pydantic events

### 5. AgentWorkflow (Multi-Agent Orchestration)

Pre-configured workflow for building AI agent systems.

```python
from llama_index.core.agent.workflow import AgentWorkflow

workflow = AgentWorkflow(
    agents=[research_agent, analysis_agent, writing_agent],
    initial_state={"task": "research_topic"}
)
```

**Patterns:**
- Single-agent with tools
- Multi-agent with handoffs
- Orchestrator pattern (meta-agent selects sub-agents)
- Hierarchical agent teams

### 6. Evaluation

Measure retrieval and response quality.

| Metric | Description |
|--------|-------------|
| **Faithfulness** | Is answer grounded in context? |
| **Relevancy** | Is answer relevant to question? |
| **Correctness** | Is answer factually correct? |
| **MRR/Hit Rate** | Retrieval quality metrics |

---

## When to Use LlamaIndex

### Best Fit

| Scenario | Why LlamaIndex |
|----------|----------------|
| Document Q&A | Best-in-class RAG pipeline |
| Enterprise search | Indexing + hybrid retrieval |
| Knowledge bases | Multiple index types |
| Contract/legal analysis | PropertyGraphIndex for entities |
| Research assistants | Agentic RAG with multi-step reasoning |
| Analytics dashboards | SQL + vector hybrid queries |

### LlamaIndex vs Alternatives

| Aspect | LlamaIndex | LangChain | Custom |
|--------|------------|-----------|--------|
| **Focus** | Data/retrieval first | Orchestration first | Full control |
| **RAG** | Excellent | Good | Manual |
| **Agents** | Good (AgentWorkflow) | Excellent (LangGraph) | Manual |
| **Learning curve** | Medium | Medium | High |
| **Document parsing** | Excellent (LlamaParse) | Basic | Manual |
| **When to choose** | Document-heavy apps | Complex workflows | Maximum flexibility |

**Recommendation:**
- Start with LlamaIndex for document-centric applications
- Use LangChain for complex multi-tool orchestration
- Combine both: LlamaIndex for retrieval, LangChain for chains

---

## LLM Usage Tips

### Provider Selection

| Provider | Best For | Context Window |
|----------|----------|----------------|
| OpenAI (gpt-4o) | General purpose, function calling | 128K |
| Claude (claude-3-5-sonnet) | Long context, reasoning | 200K |
| Gemini (gemini-2.0-flash) | Speed, cost efficiency | 1M |
| Local (Ollama) | Privacy, no API costs | Model-dependent |

### Configuration Best Practices

```python
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

# Recommended defaults
Settings.llm = OpenAI(model="gpt-4o-mini", temperature=0)
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
Settings.chunk_size = 512
Settings.chunk_overlap = 50
```

### Cost Optimization

1. **Use smaller models for simple tasks** (gpt-4o-mini vs gpt-4o)
2. **Cache embeddings** to avoid recomputation
3. **Use async** for parallel processing
4. **Batch queries** when possible
5. **Consider local embeddings** for high-volume apps

### Token Management

- Track usage with callbacks
- Set `max_tokens` appropriately
- Use streaming for long responses
- Consider context window limits when setting `similarity_top_k`

---

## Architecture Overview

```
                          LlamaIndex Architecture

Documents                Processing               Storage
    |                        |                       |
    v                        v                       v
+--------+             +-----------+           +----------+
| Reader |  -------->  | Node      |  ------>  | Index    |
+--------+             | Parser    |           | (Vector) |
                       +-----------+           +----------+
                            |                       |
                            v                       v
                       +----------+            +----------+
                       | Metadata |            | Vector   |
                       | Extract  |            | Store    |
                       +----------+            +----------+

Query Processing
    |
    v
+-------+     +----------+     +-----------+     +----------+
| Query | --> | Retriever| --> | Reranker  | --> | Response |
+-------+     +----------+     +-----------+     | Synth.   |
                                                 +----------+
                                                      |
                                                      v
                                                 +----------+
                                                 | Response |
                                                 +----------+
```

---

## Installation

### Core Package

```bash
pip install llama-index
```

### With Integrations

```bash
# LLM providers
pip install llama-index-llms-openai
pip install llama-index-llms-anthropic
pip install llama-index-llms-ollama

# Embeddings
pip install llama-index-embeddings-openai
pip install llama-index-embeddings-huggingface

# Vector stores
pip install llama-index-vector-stores-qdrant
pip install llama-index-vector-stores-chroma
pip install llama-index-vector-stores-pinecone

# Workflows (standalone)
pip install llama-index-workflows

# Document parsing
pip install llama-parse
```

### Verify Installation

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
print("LlamaIndex installed successfully!")
```

---

## Quick Start

```python
import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

# Setup
os.environ["OPENAI_API_KEY"] = "sk-..."
Settings.llm = OpenAI(model="gpt-4o-mini")
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")

# Load and index
documents = SimpleDirectoryReader("./data").load_data()
index = VectorStoreIndex.from_documents(documents)

# Query
query_engine = index.as_query_engine(similarity_top_k=5)
response = query_engine.query("What is the main topic?")
print(response)
```

---

## External Links

### Official Resources

- [LlamaIndex Documentation](https://docs.llamaindex.ai/)
- [LlamaIndex Python API](https://developers.llamaindex.ai/python/)
- [LlamaIndex GitHub](https://github.com/run-llama/llama_index)
- [LlamaHub (Connectors)](https://llamahub.ai/)
- [LlamaCloud](https://cloud.llamaindex.ai/)

### Tutorials & Guides

- [LlamaIndex Blog](https://www.llamaindex.ai/blog)
- [Building Performant RAG](https://developers.llamaindex.ai/python/framework/optimizing/production_rag/)
- [AgentWorkflow Introduction](https://www.llamaindex.ai/blog/introducing-agentworkflow-a-powerful-system-for-building-ai-agent-systems)
- [Workflows 1.0 Announcement](https://www.llamaindex.ai/blog/announcing-workflows-1-0-a-lightweight-framework-for-agentic-systems)
- [Property Graph Index Guide](https://docs.llamaindex.ai/en/stable/module_guides/indexing/lpg_index_guide/)

### Community

- [LlamaIndex Discord](https://discord.gg/llamaindex)
- [GitHub Discussions](https://github.com/run-llama/llama_index/discussions)

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [faion-rag-engineer](../../faion-rag-engineer/CLAUDE.md) | RAG patterns, vector DBs |
| [faion-ai-agents](../../faion-ai-agents/CLAUDE.md) | Agent architectures |
| [faion-llm-integration](../../faion-llm-integration/CLAUDE.md) | LLM provider setup |

---

## Files in This Directory

| File | Description |
|------|-------------|
| [README.md](README.md) | This file - overview and concepts |
| [checklist.md](checklist.md) | Setup and deployment checklists |
| [examples.md](examples.md) | Code examples for all features |
| [templates.md](templates.md) | Production-ready templates |
| [llm-prompts.md](llm-prompts.md) | Prompts for LLM-assisted development |

---

*LlamaIndex Skill v2.0 - 2026-01-25*
*RAG and Agentic Framework for Production AI Applications*

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Index creation | sonnet | Data structure design |
| Query optimization | sonnet | Performance tuning |
| Custom node parser | sonnet | Component customization |
