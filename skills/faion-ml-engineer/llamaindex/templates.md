# LlamaIndex Templates

Production-ready templates for common LlamaIndex patterns.

---

## Table of Contents

1. [Project Structure](#project-structure)
2. [Configuration Templates](#configuration-templates)
3. [Index Templates](#index-templates)
4. [Query Engine Templates](#query-engine-templates)
5. [Workflow Templates](#workflow-templates)
6. [Agent Templates](#agent-templates)
7. [API Templates](#api-templates)
8. [Testing Templates](#testing-templates)

---

## Project Structure

### Standard RAG Project

```
project/
├── src/
│   ├── __init__.py
│   ├── config.py           # Settings and configuration
│   ├── models.py           # Pydantic models
│   ├── loaders/
│   │   ├── __init__.py
│   │   └── document_loader.py
│   ├── indexing/
│   │   ├── __init__.py
│   │   ├── index_builder.py
│   │   └── node_parser.py
│   ├── retrieval/
│   │   ├── __init__.py
│   │   ├── retrievers.py
│   │   └── rerankers.py
│   ├── query/
│   │   ├── __init__.py
│   │   └── query_engine.py
│   └── api/
│       ├── __init__.py
│       ├── main.py         # FastAPI app
│       └── routes.py
├── data/
│   └── documents/          # Source documents
├── storage/
│   └── index/              # Persisted index
├── tests/
│   ├── conftest.py
│   ├── test_retrieval.py
│   └── test_responses.py
├── scripts/
│   ├── ingest.py           # Data ingestion script
│   └── evaluate.py         # Evaluation script
├── .env
├── pyproject.toml
└── README.md
```

---

## Configuration Templates

### config.py

```python
"""LlamaIndex configuration module."""

import os
from functools import lru_cache
from pydantic_settings import BaseSettings
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding


class AppSettings(BaseSettings):
    """Application settings from environment."""

    # API Keys
    openai_api_key: str
    anthropic_api_key: str | None = None

    # LLM Settings
    llm_model: str = "gpt-4o-mini"
    llm_temperature: float = 0.0
    llm_max_tokens: int = 1024

    # Embedding Settings
    embedding_model: str = "text-embedding-3-small"
    embedding_dimensions: int = 1536

    # Chunking Settings
    chunk_size: int = 512
    chunk_overlap: int = 50

    # Retrieval Settings
    similarity_top_k: int = 5
    rerank_top_n: int = 3

    # Storage Settings
    storage_dir: str = "./storage"
    data_dir: str = "./data/documents"

    # Vector Store
    vector_store_type: str = "chroma"  # chroma, qdrant, pinecone
    qdrant_url: str | None = None
    qdrant_api_key: str | None = None
    pinecone_api_key: str | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> AppSettings:
    """Get cached application settings."""
    return AppSettings()


def configure_llama_index(settings: AppSettings | None = None) -> None:
    """Configure LlamaIndex global settings."""
    if settings is None:
        settings = get_settings()

    # Set API key
    os.environ["OPENAI_API_KEY"] = settings.openai_api_key

    # Configure LLM
    Settings.llm = OpenAI(
        model=settings.llm_model,
        temperature=settings.llm_temperature,
        max_tokens=settings.llm_max_tokens,
    )

    # Configure embeddings
    Settings.embed_model = OpenAIEmbedding(
        model=settings.embedding_model,
        dimensions=settings.embedding_dimensions,
    )

    # Configure chunking
    Settings.chunk_size = settings.chunk_size
    Settings.chunk_overlap = settings.chunk_overlap


# Initialize on import
configure_llama_index()
```

### .env Template

```bash
# LLM Providers
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...

# LLM Configuration
LLM_MODEL=gpt-4o-mini
LLM_TEMPERATURE=0.0
LLM_MAX_TOKENS=1024

# Embedding Configuration
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_DIMENSIONS=1536

# Chunking
CHUNK_SIZE=512
CHUNK_OVERLAP=50

# Retrieval
SIMILARITY_TOP_K=5
RERANK_TOP_N=3

# Storage
STORAGE_DIR=./storage
DATA_DIR=./data/documents

# Vector Store (choose one)
VECTOR_STORE_TYPE=chroma

# Qdrant (if using)
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=

# Pinecone (if using)
PINECONE_API_KEY=
PINECONE_ENVIRONMENT=

# Observability
LANGFUSE_PUBLIC_KEY=
LANGFUSE_SECRET_KEY=
```

---

## Index Templates

### VectorStore Index Builder

```python
"""Index builder module."""

from pathlib import Path
from llama_index.core import (
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
    SimpleDirectoryReader,
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.vector_stores.qdrant import QdrantVectorStore
import chromadb
from qdrant_client import QdrantClient

from .config import get_settings, AppSettings


class IndexBuilder:
    """Build and manage vector store indexes."""

    def __init__(self, settings: AppSettings | None = None):
        self.settings = settings or get_settings()
        self._index: VectorStoreIndex | None = None

    def _get_vector_store(self):
        """Get configured vector store."""
        store_type = self.settings.vector_store_type

        if store_type == "chroma":
            db = chromadb.PersistentClient(
                path=f"{self.settings.storage_dir}/chroma"
            )
            collection = db.get_or_create_collection("documents")
            return ChromaVectorStore(chroma_collection=collection)

        elif store_type == "qdrant":
            client = QdrantClient(
                url=self.settings.qdrant_url,
                api_key=self.settings.qdrant_api_key,
            )
            return QdrantVectorStore(
                client=client,
                collection_name="documents",
            )

        else:
            raise ValueError(f"Unknown vector store type: {store_type}")

    def build_index(self, documents=None) -> VectorStoreIndex:
        """Build new index from documents."""
        # Load documents if not provided
        if documents is None:
            reader = SimpleDirectoryReader(
                input_dir=self.settings.data_dir,
                recursive=True,
                required_exts=[".pdf", ".docx", ".md", ".txt"],
            )
            documents = reader.load_data()
            print(f"Loaded {len(documents)} documents")

        # Parse into nodes
        parser = SentenceSplitter(
            chunk_size=self.settings.chunk_size,
            chunk_overlap=self.settings.chunk_overlap,
        )
        nodes = parser.get_nodes_from_documents(documents, show_progress=True)
        print(f"Created {len(nodes)} nodes")

        # Create storage context
        vector_store = self._get_vector_store()
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        # Build index
        self._index = VectorStoreIndex(
            nodes=nodes,
            storage_context=storage_context,
            show_progress=True,
        )

        # Persist
        self._index.storage_context.persist(persist_dir=self.settings.storage_dir)
        print(f"Index persisted to {self.settings.storage_dir}")

        return self._index

    def load_index(self) -> VectorStoreIndex:
        """Load existing index from storage."""
        storage_path = Path(self.settings.storage_dir)

        if not storage_path.exists():
            raise FileNotFoundError(
                f"Index not found at {storage_path}. Run build_index() first."
            )

        vector_store = self._get_vector_store()
        self._index = VectorStoreIndex.from_vector_store(vector_store)

        return self._index

    def get_index(self) -> VectorStoreIndex:
        """Get or load index."""
        if self._index is None:
            try:
                self._index = self.load_index()
            except FileNotFoundError:
                self._index = self.build_index()
        return self._index


# Singleton instance
_index_builder: IndexBuilder | None = None


def get_index_builder() -> IndexBuilder:
    """Get singleton index builder."""
    global _index_builder
    if _index_builder is None:
        _index_builder = IndexBuilder()
    return _index_builder


def get_index() -> VectorStoreIndex:
    """Get the current index."""
    return get_index_builder().get_index()
```

### Hybrid Index Builder

```python
"""Hybrid index with vector and keyword search."""

from llama_index.core import VectorStoreIndex
from llama_index.retrievers.bm25 import BM25Retriever
from llama_index.core.retrievers import QueryFusionRetriever
from llama_index.core.node_parser import SentenceSplitter

from .config import get_settings


class HybridIndexBuilder:
    """Build hybrid index with vector + BM25."""

    def __init__(self):
        self.settings = get_settings()
        self._index: VectorStoreIndex | None = None
        self._nodes: list = []

    def build(self, documents) -> tuple[VectorStoreIndex, list]:
        """Build index and store nodes for BM25."""
        parser = SentenceSplitter(
            chunk_size=self.settings.chunk_size,
            chunk_overlap=self.settings.chunk_overlap,
        )
        self._nodes = parser.get_nodes_from_documents(documents)
        self._index = VectorStoreIndex(self._nodes, show_progress=True)

        return self._index, self._nodes

    def get_hybrid_retriever(
        self,
        vector_weight: float = 0.6,
        bm25_weight: float = 0.4,
    ) -> QueryFusionRetriever:
        """Get hybrid retriever combining vector and BM25."""
        if self._index is None or not self._nodes:
            raise ValueError("Index not built. Call build() first.")

        # Vector retriever
        vector_retriever = self._index.as_retriever(
            similarity_top_k=self.settings.similarity_top_k * 2,
        )

        # BM25 retriever
        bm25_retriever = BM25Retriever.from_defaults(
            nodes=self._nodes,
            similarity_top_k=self.settings.similarity_top_k * 2,
        )

        # Fusion retriever
        return QueryFusionRetriever(
            retrievers=[bm25_retriever, vector_retriever],
            retriever_weights=[bm25_weight, vector_weight],
            num_queries=1,
            mode="reciprocal_rerank",
        )
```

---

## Query Engine Templates

### Standard Query Engine

```python
"""Query engine module."""

from llama_index.core import VectorStoreIndex
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SentenceTransformerRerank
from llama_index.core import get_response_synthesizer, PromptTemplate

from .config import get_settings
from .indexing.index_builder import get_index


class QueryEngineFactory:
    """Factory for creating query engines."""

    def __init__(self, index: VectorStoreIndex | None = None):
        self.settings = get_settings()
        self.index = index or get_index()

    def create_basic(self) -> RetrieverQueryEngine:
        """Create basic query engine."""
        return self.index.as_query_engine(
            similarity_top_k=self.settings.similarity_top_k,
            response_mode="compact",
        )

    def create_with_reranking(self) -> RetrieverQueryEngine:
        """Create query engine with reranking."""
        reranker = SentenceTransformerRerank(
            model="cross-encoder/ms-marco-MiniLM-L-2-v2",
            top_n=self.settings.rerank_top_n,
        )

        return self.index.as_query_engine(
            similarity_top_k=self.settings.similarity_top_k * 3,
            node_postprocessors=[reranker],
            response_mode="compact",
        )

    def create_with_custom_prompt(
        self,
        system_prompt: str | None = None,
    ) -> RetrieverQueryEngine:
        """Create query engine with custom prompt."""
        qa_prompt = PromptTemplate(
            f"""{system_prompt or 'You are a helpful assistant.'}

Use the following context to answer the question. If you cannot find the answer
in the context, say "I don't have enough information to answer that."

Context:
{{context_str}}

Question: {{query_str}}

Answer:"""
        )

        return self.index.as_query_engine(
            similarity_top_k=self.settings.similarity_top_k,
            text_qa_template=qa_prompt,
            response_mode="compact",
        )

    def create_streaming(self) -> RetrieverQueryEngine:
        """Create streaming query engine."""
        return self.index.as_query_engine(
            similarity_top_k=self.settings.similarity_top_k,
            streaming=True,
            response_mode="compact",
        )


# Convenience functions
def get_query_engine() -> RetrieverQueryEngine:
    """Get default query engine."""
    return QueryEngineFactory().create_with_reranking()
```

### Router Query Engine

```python
"""Multi-index router query engine."""

from llama_index.core.query_engine import RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector
from llama_index.core.tools import QueryEngineTool, ToolMetadata


def create_router_engine(
    index_configs: list[dict],
) -> RouterQueryEngine:
    """
    Create router query engine from multiple indexes.

    Args:
        index_configs: List of dicts with 'index', 'name', 'description'

    Example:
        configs = [
            {
                'index': tech_index,
                'name': 'technical_docs',
                'description': 'Technical documentation and API references'
            },
            {
                'index': business_index,
                'name': 'business_docs',
                'description': 'Business reports and financials'
            }
        ]
    """
    tools = []

    for config in index_configs:
        tool = QueryEngineTool(
            query_engine=config['index'].as_query_engine(
                similarity_top_k=5,
                response_mode="compact",
            ),
            metadata=ToolMetadata(
                name=config['name'],
                description=config['description'],
            ),
        )
        tools.append(tool)

    return RouterQueryEngine(
        selector=LLMSingleSelector.from_defaults(),
        query_engine_tools=tools,
        verbose=True,
    )
```

---

## Workflow Templates

### RAG Workflow

```python
"""Production RAG workflow."""

from pydantic import Field
from llama_index.core.workflow import (
    Workflow,
    StartEvent,
    StopEvent,
    step,
    Event,
    Context,
)
from llama_index.core import VectorStoreIndex, get_response_synthesizer
from llama_index.core.postprocessor import SentenceTransformerRerank


# Events
class QueryEvent(Event):
    """Initial query event."""
    query: str = Field(..., description="User query")
    filters: dict = Field(default_factory=dict, description="Optional filters")


class RetrievalEvent(Event):
    """Retrieved nodes event."""
    query: str
    nodes: list
    retrieval_time_ms: float


class RerankEvent(Event):
    """Reranked nodes event."""
    query: str
    nodes: list


class SynthesisEvent(Event):
    """Final response event."""
    response: str
    sources: list[dict]


# Workflow
class RAGWorkflow(Workflow):
    """Production RAG workflow with retrieval, reranking, and synthesis."""

    def __init__(
        self,
        index: VectorStoreIndex,
        top_k: int = 10,
        rerank_top_n: int = 5,
    ):
        super().__init__()
        self.index = index
        self.top_k = top_k
        self.rerank_top_n = rerank_top_n
        self.retriever = index.as_retriever(similarity_top_k=top_k)
        self.reranker = SentenceTransformerRerank(
            model="cross-encoder/ms-marco-MiniLM-L-2-v2",
            top_n=rerank_top_n,
        )
        self.synthesizer = get_response_synthesizer(response_mode="compact")

    @step
    async def retrieve(self, ctx: Context, ev: StartEvent) -> RetrievalEvent:
        """Retrieve relevant documents."""
        import time

        query = ev.query
        await ctx.set("query", query)

        start = time.time()
        nodes = await self.retriever.aretrieve(query)
        elapsed_ms = (time.time() - start) * 1000

        await ctx.set("retrieval_count", len(nodes))

        return RetrievalEvent(
            query=query,
            nodes=nodes,
            retrieval_time_ms=elapsed_ms,
        )

    @step
    async def rerank(self, ctx: Context, ev: RetrievalEvent) -> RerankEvent:
        """Rerank retrieved documents."""
        reranked = self.reranker.postprocess_nodes(
            ev.nodes,
            query_str=ev.query,
        )

        await ctx.set("rerank_count", len(reranked))

        return RerankEvent(
            query=ev.query,
            nodes=reranked,
        )

    @step
    async def synthesize(self, ctx: Context, ev: RerankEvent) -> StopEvent:
        """Synthesize final response."""
        response = await self.synthesizer.asynthesize(
            ev.query,
            nodes=ev.nodes,
        )

        # Extract sources
        sources = []
        for node in ev.nodes:
            sources.append({
                "text": node.text[:200] + "...",
                "score": node.score,
                "metadata": node.metadata,
            })

        result = {
            "response": str(response),
            "sources": sources,
            "metadata": {
                "retrieval_count": await ctx.get("retrieval_count"),
                "rerank_count": await ctx.get("rerank_count"),
            }
        }

        return StopEvent(result=result)


# Usage
async def query_with_workflow(
    index: VectorStoreIndex,
    query: str,
) -> dict:
    """Run RAG workflow."""
    workflow = RAGWorkflow(index)
    result = await workflow.run(query=query)
    return result
```

### Multi-Step Research Workflow

```python
"""Multi-step research workflow with iterations."""

from pydantic import Field
from llama_index.core.workflow import (
    Workflow, StartEvent, StopEvent, step, Event, Context
)


class ResearchQuery(Event):
    topic: str
    depth: int = 3  # Number of research iterations


class SearchResult(Event):
    query: str
    findings: list[str]
    iteration: int


class AnalysisResult(Event):
    findings: list[str]
    gaps: list[str]
    iteration: int


class FinalReport(Event):
    summary: str
    key_findings: list[str]
    sources: list[dict]


class ResearchWorkflow(Workflow):
    """Multi-iteration research workflow."""

    def __init__(self, index, llm):
        super().__init__()
        self.index = index
        self.llm = llm
        self.query_engine = index.as_query_engine(similarity_top_k=10)

    @step
    async def start_research(
        self, ctx: Context, ev: StartEvent
    ) -> SearchResult:
        """Initialize research."""
        await ctx.set("topic", ev.topic)
        await ctx.set("max_iterations", ev.depth)
        await ctx.set("all_findings", [])

        # Initial search
        response = await self.query_engine.aquery(ev.topic)
        findings = [str(response)]

        return SearchResult(
            query=ev.topic,
            findings=findings,
            iteration=1,
        )

    @step
    async def analyze_findings(
        self, ctx: Context, ev: SearchResult
    ) -> AnalysisResult | StopEvent:
        """Analyze findings and identify gaps."""
        all_findings = await ctx.get("all_findings", [])
        all_findings.extend(ev.findings)
        await ctx.set("all_findings", all_findings)

        max_iter = await ctx.get("max_iterations")
        if ev.iteration >= max_iter:
            # Generate final report
            return await self._generate_report(ctx, all_findings)

        # Identify gaps using LLM
        gaps_prompt = f"""
        Based on these findings about '{await ctx.get("topic")}':
        {ev.findings}

        What important aspects haven't been covered yet?
        List 2-3 follow-up questions.
        """
        gaps_response = await self.llm.acomplete(gaps_prompt)
        gaps = str(gaps_response).split("\n")[:3]

        return AnalysisResult(
            findings=ev.findings,
            gaps=gaps,
            iteration=ev.iteration,
        )

    @step
    async def follow_up_search(
        self, ctx: Context, ev: AnalysisResult
    ) -> SearchResult:
        """Search for gap information."""
        new_findings = []
        for gap in ev.gaps:
            if gap.strip():
                response = await self.query_engine.aquery(gap)
                new_findings.append(str(response))

        return SearchResult(
            query=", ".join(ev.gaps),
            findings=new_findings,
            iteration=ev.iteration + 1,
        )

    async def _generate_report(
        self, ctx: Context, findings: list[str]
    ) -> StopEvent:
        """Generate final research report."""
        topic = await ctx.get("topic")

        report_prompt = f"""
        Summarize the research findings about '{topic}':

        Findings:
        {chr(10).join(findings)}

        Provide:
        1. A concise summary (2-3 paragraphs)
        2. Key findings (bullet points)
        """

        report = await self.llm.acomplete(report_prompt)

        return StopEvent(result={
            "topic": topic,
            "summary": str(report),
            "iterations": await ctx.get("max_iterations"),
            "total_findings": len(findings),
        })
```

---

## Agent Templates

### Tool-Using Agent

```python
"""Tool-using agent template."""

from llama_index.core.agent import ReActAgent
from llama_index.core.tools import FunctionTool, QueryEngineTool, ToolMetadata
from llama_index.core import Settings


def create_tool_agent(
    index,
    custom_tools: list | None = None,
    system_prompt: str | None = None,
) -> ReActAgent:
    """
    Create a tool-using agent.

    Args:
        index: Vector index for knowledge base
        custom_tools: Additional function tools
        system_prompt: Custom system prompt
    """
    tools = []

    # Knowledge base tool
    kb_tool = QueryEngineTool.from_defaults(
        query_engine=index.as_query_engine(similarity_top_k=5),
        name="knowledge_base",
        description="Search the knowledge base for information. "
                    "Use this for factual questions about the domain.",
    )
    tools.append(kb_tool)

    # Add custom tools
    if custom_tools:
        tools.extend(custom_tools)

    return ReActAgent.from_tools(
        tools=tools,
        llm=Settings.llm,
        verbose=True,
        max_iterations=10,
        system_prompt=system_prompt or """You are a helpful assistant with access to tools.
        Always search the knowledge base before making claims.
        Be concise and accurate in your responses.""",
    )


# Example custom tools
def create_calculator_tool() -> FunctionTool:
    """Create a calculator tool."""
    def calculate(expression: str) -> str:
        """Evaluate a mathematical expression.

        Args:
            expression: Math expression like "2 + 2" or "100 * 0.2"

        Returns:
            Result as string
        """
        try:
            # Safe evaluation (in production, use a proper math parser)
            allowed_chars = set("0123456789+-*/.() ")
            if not all(c in allowed_chars for c in expression):
                return "Error: Invalid characters in expression"
            result = eval(expression)
            return str(result)
        except Exception as e:
            return f"Error: {e}"

    return FunctionTool.from_defaults(
        fn=calculate,
        name="calculator",
        description="Perform mathematical calculations",
    )


def create_date_tool() -> FunctionTool:
    """Create a date/time tool."""
    from datetime import datetime

    def get_current_date() -> str:
        """Get the current date and time.

        Returns:
            Current date and time in ISO format
        """
        return datetime.now().isoformat()

    return FunctionTool.from_defaults(
        fn=get_current_date,
        name="current_date",
        description="Get the current date and time",
    )
```

### Multi-Agent Workflow

```python
"""Multi-agent orchestration template."""

from llama_index.core.agent.workflow import AgentWorkflow, FunctionAgent
from llama_index.core.tools import QueryEngineTool, FunctionTool
from llama_index.core import Settings


def create_multi_agent_workflow(
    research_index,
    analysis_tools: list | None = None,
) -> AgentWorkflow:
    """
    Create a multi-agent workflow with specialized agents.

    Agents:
    - Researcher: Searches knowledge base
    - Analyst: Analyzes data and calculates
    - Writer: Synthesizes final output
    """
    # Research agent
    research_tool = QueryEngineTool.from_defaults(
        query_engine=research_index.as_query_engine(similarity_top_k=10),
        name="search",
        description="Search the knowledge base for information",
    )

    researcher = FunctionAgent(
        name="researcher",
        description="Researches topics and finds relevant information",
        tools=[research_tool],
        llm=Settings.llm,
        system_prompt="""You are a research specialist.
        Your job is to find accurate information from the knowledge base.
        Always cite your sources and be thorough.""",
        can_handoff_to=["analyst", "writer"],
    )

    # Analysis agent
    calc_tool = FunctionTool.from_defaults(
        fn=lambda expr: str(eval(expr)),
        name="calculate",
        description="Perform calculations",
    )

    analyst = FunctionAgent(
        name="analyst",
        description="Analyzes data and provides insights",
        tools=[calc_tool] + (analysis_tools or []),
        llm=Settings.llm,
        system_prompt="""You are a data analyst.
        Your job is to analyze information and provide insights.
        Use calculations when needed.""",
        can_handoff_to=["researcher", "writer"],
    )

    # Writer agent
    writer = FunctionAgent(
        name="writer",
        description="Writes clear, well-structured reports",
        tools=[],
        llm=Settings.llm,
        system_prompt="""You are a technical writer.
        Your job is to synthesize information into clear reports.
        Structure your output with headers and bullet points.""",
        can_handoff_to=["researcher", "analyst"],
    )

    return AgentWorkflow(
        agents=[researcher, analyst, writer],
        initial_agent="researcher",
    )


# Usage
async def run_research_task(workflow: AgentWorkflow, task: str) -> dict:
    """Run a research task through the multi-agent workflow."""
    result = await workflow.run(task=task)
    return {
        "result": result,
        "agents_used": workflow.get_execution_history(),
    }
```

---

## API Templates

### FastAPI Application

```python
"""FastAPI application template."""

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
import asyncio

from .config import configure_llama_index
from .indexing.index_builder import get_index
from .query.query_engine import QueryEngineFactory


# Models
class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000)
    top_k: int = Field(default=5, ge=1, le=20)
    stream: bool = Field(default=False)


class QueryResponse(BaseModel):
    response: str
    sources: list[dict]
    metadata: dict


class HealthResponse(BaseModel):
    status: str
    index_loaded: bool


# Lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    configure_llama_index()
    app.state.index = get_index()
    app.state.engine_factory = QueryEngineFactory(app.state.index)
    yield
    # Shutdown
    pass


# Application
app = FastAPI(
    title="RAG API",
    description="RAG-powered question answering API",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routes
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        index_loaded=app.state.index is not None,
    )


@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """Query the knowledge base."""
    try:
        engine = app.state.engine_factory.create_with_reranking()
        response = await engine.aquery(request.query)

        sources = []
        for node in response.source_nodes:
            sources.append({
                "text": node.text[:500],
                "score": float(node.score) if node.score else 0.0,
                "metadata": node.metadata,
            })

        return QueryResponse(
            response=str(response),
            sources=sources,
            metadata={
                "top_k": request.top_k,
                "source_count": len(sources),
            },
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query/stream")
async def query_stream(request: QueryRequest):
    """Stream query response."""
    async def generate():
        engine = app.state.engine_factory.create_streaming()
        response = await engine.aquery(request.query)

        async for text in response.async_response_gen():
            yield f"data: {text}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
    )


# Run with: uvicorn src.api.main:app --reload
```

---

## Testing Templates

### Conftest (Fixtures)

```python
"""Test fixtures."""

import pytest
import asyncio
from llama_index.core import VectorStoreIndex, Document


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def test_documents():
    """Create test documents."""
    return [
        Document(
            text="LlamaIndex is a data framework for LLM applications.",
            metadata={"source": "test", "category": "framework"},
        ),
        Document(
            text="RAG stands for Retrieval-Augmented Generation.",
            metadata={"source": "test", "category": "concept"},
        ),
        Document(
            text="Vector databases store embeddings for similarity search.",
            metadata={"source": "test", "category": "storage"},
        ),
    ]


@pytest.fixture(scope="session")
def test_index(test_documents):
    """Create test index."""
    return VectorStoreIndex.from_documents(test_documents)


@pytest.fixture
def query_engine(test_index):
    """Create test query engine."""
    return test_index.as_query_engine(similarity_top_k=2)
```

### Retrieval Tests

```python
"""Retrieval tests."""

import pytest


class TestRetrieval:
    """Test retrieval functionality."""

    def test_basic_retrieval(self, test_index):
        """Test basic retrieval returns nodes."""
        retriever = test_index.as_retriever(similarity_top_k=2)
        nodes = retriever.retrieve("What is LlamaIndex?")

        assert len(nodes) > 0
        assert nodes[0].score > 0

    def test_retrieval_relevance(self, test_index):
        """Test retrieval returns relevant results."""
        retriever = test_index.as_retriever(similarity_top_k=2)
        nodes = retriever.retrieve("What is RAG?")

        # Check that RAG document is in results
        texts = [n.text for n in nodes]
        assert any("RAG" in t for t in texts)

    @pytest.mark.asyncio
    async def test_async_retrieval(self, test_index):
        """Test async retrieval."""
        retriever = test_index.as_retriever(similarity_top_k=2)
        nodes = await retriever.aretrieve("vector databases")

        assert len(nodes) > 0


class TestQueryEngine:
    """Test query engine functionality."""

    def test_basic_query(self, query_engine):
        """Test basic query returns response."""
        response = query_engine.query("What is LlamaIndex?")

        assert response.response is not None
        assert len(response.response) > 0

    def test_query_has_sources(self, query_engine):
        """Test query returns source nodes."""
        response = query_engine.query("What is RAG?")

        assert len(response.source_nodes) > 0

    @pytest.mark.asyncio
    async def test_async_query(self, query_engine):
        """Test async query."""
        response = await query_engine.aquery("vector databases")

        assert response.response is not None
```

### Evaluation Tests

```python
"""Evaluation tests."""

import pytest
from llama_index.core.evaluation import FaithfulnessEvaluator


class TestEvaluation:
    """Test response quality."""

    @pytest.fixture
    def faithfulness_evaluator(self):
        """Create faithfulness evaluator."""
        from llama_index.core import Settings
        return FaithfulnessEvaluator(llm=Settings.llm)

    @pytest.mark.asyncio
    async def test_response_faithfulness(
        self,
        query_engine,
        faithfulness_evaluator,
    ):
        """Test that responses are grounded in context."""
        query = "What is LlamaIndex?"
        response = query_engine.query(query)

        result = faithfulness_evaluator.evaluate_response(
            query=query,
            response=response,
        )

        assert result.passing, f"Faithfulness failed: {result.feedback}"

    def test_no_hallucination(self, query_engine):
        """Test that unknown questions return appropriate response."""
        response = query_engine.query(
            "What is the price of uranium on Mars?"
        )

        # Should not confidently answer unknown questions
        response_lower = response.response.lower()
        assert any(phrase in response_lower for phrase in [
            "don't know",
            "no information",
            "not found",
            "cannot answer",
        ]) or len(response.source_nodes) == 0
```

---

*LlamaIndex Templates v2.0 - 2026-01-25*
