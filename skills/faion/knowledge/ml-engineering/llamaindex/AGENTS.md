# LlamaIndex

## Summary

**One-sentence:** Produces a LlamaIndex RAG / agent pipeline: heterogeneous loaders → chunking → vector index → query engine with source citations and async Workflow event pipelines.

**One-paragraph:** Produces a LlamaIndex RAG / agent pipeline. LlamaIndex solves the document-retrieval problem the LLM SDK does not: heterogeneous document loaders, chunking strategies, vector + property-graph indexes, and answer synthesis with source citations. Its Workflow abstraction provides async-first, type-safe event pipelines that map directly to agent task queues and pause/resume for human-in-loop checkpoints.

**Ефективно для:** Дата-інженер для RAG over heterogeneous docs — fixed pipeline з loaders + chunk + index + cited query.

## Applies If (ALL must hold)

- Need RAG over heterogeneous document sources (PDF, HTML, DB, Notion, S3, ...).
- Source citations are a hard requirement (regulated / customer-facing).
- Python stack — LlamaIndex is Python-canonical.
- Have or can stand up a vector store (Qdrant, Pinecone, pgvector, Chroma).
- Want a Workflow event pipeline for pause/resume / HITL.

## Skip If (ANY kills it)

- Single-source plain-text RAG — provider-native RAG suffices.
- Need a graph-first knowledge model — use GraphRAG instead (or LlamaIndex PropertyGraphIndex).
- Non-Python stack — use a thinner native client.
- No source-citation requirement AND simple chunking — LangChain is leaner.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Source corpus | directory / db / api list | data team |
| Vector store | url + creds | infra |
| Chunk strategy | yaml (size, overlap) | ML lead |
| Provider choice | string | decision record |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer/llm-decision-framework` | Provider + RAG choice. |
| `geek/ai/ml-engineer/llm-observability-stack` | Trace ingestion + query. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules each with rationale + source. | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + self-check. | ~800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix. | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure: load → chunk → index → query → cite. | ~800 |
| `content/06-decision-tree.xml` | essential | Branch: vector vs property-graph + workflow vs query-engine. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-pipeline` | haiku | Fill rag_workflow.py + config.py from decisions. |
| `design-chunking` | sonnet | Choose chunk_size + overlap from doc shape. |
| `audit-retrieval` | opus | Cross-document retrieval-quality audit. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rag_workflow.py` | RAG Workflow with retrieval + synthesis + citations. |
| `templates/config.py` | Settings: embed model, chunk_size, top_k. |
| `templates/prompt-qa.txt` | QA prompt with source-citation policy. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-llamaindex.py` | Validate the pipeline config (loaders, chunk, index, citation policy). | Pre-merge of every LlamaIndex pipeline PR. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[graph-rag]] — graph-first alternative.
- [[langchain]] — alternative agent framework.
- [[llm-observability-stack]] — tracing.

## Decision tree

Decision tree at `content/06-decision-tree.xml` decides index type (vector / property-graph / hybrid) and pipeline shape (Workflow vs QueryEngine).

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/rag_workflow.py`

```python
"""

"""LlamaIndex RAG Workflow with typed events and parallel retrieval."""
from llama_index.core.workflow import (
    Event,
    StartEvent,
    StopEvent,
    Workflow,
    step,
    Context,
)
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.response_synthesizers import get_response_synthesizer
from pydantic import BaseModel
from typing import Optional


class QueryEvent(Event):
    query: str


class RetrievedEvent(Event):
    query: str
    nodes: list


class RAGWorkflow(Workflow):
    def __init__(self, index: VectorStoreIndex, similarity_top_k: int = 5, **kwargs):
        super().__init__(**kwargs)
        self.index = index
        self.similarity_top_k = similarity_top_k

    @step
    async def retrieve(self, ctx: Context, ev: StartEvent) -> RetrievedEvent:
        """Retrieve relevant nodes from the index."""
        query = ev.get("query")
        retriever = self.index.as_retriever(similarity_top_k=self.similarity_top_k)
        nodes = await retriever.aretrieve(query)
        return RetrievedEvent(query=query, nodes=nodes)

    @step
    async def synthesize(self, ctx: Context, ev: RetrievedEvent) -> StopEvent:
        """Synthesize answer from retrieved nodes."""
        synthesizer = get_response_synthesizer(response_mode="compact")
        response = await synthesizer.asynthesize(ev.query, nodes=ev.nodes)
        return StopEvent(result=str(response))


async def run_rag(index: VectorStoreIndex, query: str) -> str:
    """Execute RAG workflow and return answer."""
    workflow = RAGWorkflow(index=index, timeout=60)
    result = await workflow.run(query=query)
    return result
```

### `templates/config.py`

```python
"""

"""LlamaIndex storage and service context configuration."""
import os
from llama_index.core import Settings, StorageContext, load_index_from_storage
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.anthropic import Anthropic
from llama_index.embeddings.openai import OpenAIEmbedding


def configure_llamaindex(
    model: str = "claude-opus-4-5",
    embed_model: str = "text-embedding-3-large",
    chunk_size: int = 512,
    chunk_overlap: int = 64,
) -> None:
    """Set global LlamaIndex settings."""
    Settings.llm = Anthropic(model=model, api_key=os.environ["ANTHROPIC_API_KEY"])
    Settings.embed_model = OpenAIEmbedding(
        model=embed_model,
        api_key=os.environ["OPENAI_API_KEY"],
    )
    Settings.node_parser = SentenceSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    Settings.num_output = 1024
    Settings.context_window = 4096


def load_or_create_storage(persist_dir: str) -> StorageContext:
    """Load existing index or return empty storage context."""
    if os.path.exists(persist_dir):
        return StorageContext.from_defaults(persist_dir=persist_dir)
    return StorageContext.from_defaults()
```

### `templates/prompt-qa.txt`

```text
-->

You are a precise question-answering assistant. Answer questions based ONLY on the provided context.

Rules:
1. Answer directly from the context. Do not add information not present in the context.
2. If the context does not contain the answer, say: "I don't have enough information to answer that question."
3. Cite the source document when providing answers using the format: [Source: {filename}]
4. Keep answers concise — use bullet points for multi-part answers.
5. Do not speculate or extrapolate beyond what the context states.

Context:
{context_str}

Question: {query_str}

Answer:
```
