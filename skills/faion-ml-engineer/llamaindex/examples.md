# LlamaIndex Examples

Comprehensive code examples for LlamaIndex features.

---

## Table of Contents

1. [Data Loading](#data-loading)
2. [Index Creation](#index-creation)
3. [Query Engines](#query-engines)
4. [Retrievers](#retrievers)
5. [Workflows](#workflows)
6. [Agents](#agents)
7. [Evaluation](#evaluation)
8. [Production Patterns](#production-patterns)

---

## Data Loading

### SimpleDirectoryReader

```python
from llama_index.core import SimpleDirectoryReader

# Basic usage
documents = SimpleDirectoryReader("./data").load_data()
print(f"Loaded {len(documents)} documents")

# With filtering
documents = SimpleDirectoryReader(
    input_dir="./data",
    recursive=True,
    required_exts=[".pdf", ".docx", ".md", ".txt"],
    exclude_hidden=True,
    filename_as_id=True,
).load_data()

# Specific files only
documents = SimpleDirectoryReader(
    input_files=["./doc1.pdf", "./doc2.txt"]
).load_data()

# With custom metadata
def file_metadata_func(file_path: str) -> dict:
    return {
        "file_path": file_path,
        "file_name": file_path.split("/")[-1],
        "category": "technical" if "tech" in file_path else "general"
    }

documents = SimpleDirectoryReader(
    input_dir="./data",
    file_metadata=file_metadata_func,
).load_data()
```

### Web Page Reader

```python
from llama_index.readers.web import SimpleWebPageReader, BeautifulSoupWebReader

# Simple web pages
reader = SimpleWebPageReader(html_to_text=True)
documents = reader.load_data(
    urls=[
        "https://docs.llamaindex.ai/",
        "https://example.com/docs"
    ]
)

# Complex HTML with BeautifulSoup
reader = BeautifulSoupWebReader()
documents = reader.load_data(
    urls=["https://example.com"],
    custom_hostname="example.com"
)
```

### Database Reader

```python
from llama_index.readers.database import DatabaseReader
from sqlalchemy import create_engine

engine = create_engine("postgresql://user:pass@localhost/db")

reader = DatabaseReader(engine=engine)

# Load from SQL query
documents = reader.load_data(
    query="SELECT id, title, content FROM articles WHERE published = true"
)

# Each row becomes a document
for doc in documents:
    print(f"ID: {doc.metadata.get('id')}")
    print(f"Content: {doc.text[:100]}...")
```

### GitHub Repository Reader

```python
from llama_index.readers.github import GithubRepositoryReader

reader = GithubRepositoryReader(
    github_token="ghp_...",
    owner="owner",
    repo="repo",
    filter_file_extensions=[".py", ".md", ".rst"],
    verbose=True,
)

# Load specific branch
documents = reader.load_data(branch="main")

# With path filtering
documents = reader.load_data(
    branch="main",
    filter_directories=["src", "docs"],
)
```

### LlamaParse (Advanced PDF Parsing)

```python
from llama_parse import LlamaParse

# Initialize parser
parser = LlamaParse(
    api_key="llx-...",
    result_type="markdown",  # or "text"
    num_workers=4,
    verbose=True,
    language="en",
)

# Parse PDF with OCR and table extraction
documents = parser.load_data("./complex_report.pdf")

# Use with SimpleDirectoryReader
from llama_index.core import SimpleDirectoryReader

reader = SimpleDirectoryReader(
    input_dir="./docs",
    file_extractor={".pdf": parser},
)
documents = reader.load_data()
```

---

## Index Creation

### VectorStoreIndex (In-Memory)

```python
from llama_index.core import VectorStoreIndex, Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

# Configure settings
Settings.llm = OpenAI(model="gpt-4o-mini", temperature=0)
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")

# Create index from documents
index = VectorStoreIndex.from_documents(
    documents,
    show_progress=True,
)

# Create from nodes (pre-processed)
from llama_index.core.node_parser import SentenceSplitter

parser = SentenceSplitter(chunk_size=512, chunk_overlap=50)
nodes = parser.get_nodes_from_documents(documents)
index = VectorStoreIndex(nodes)
```

### VectorStoreIndex with Qdrant

```python
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

# Local Qdrant (development)
client = QdrantClient(path="./qdrant_data")

# Remote Qdrant (production)
# client = QdrantClient(
#     url="https://your-cluster.qdrant.io",
#     api_key="your-api-key",
# )

vector_store = QdrantVectorStore(
    client=client,
    collection_name="my_documents",
)

storage_context = StorageContext.from_defaults(vector_store=vector_store)

# Create new index
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context,
    show_progress=True,
)

# Load existing index
index = VectorStoreIndex.from_vector_store(
    vector_store=vector_store,
)
```

### VectorStoreIndex with Chroma

```python
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb

# Persistent storage
db = chromadb.PersistentClient(path="./chroma_db")
collection = db.get_or_create_collection("documents")

vector_store = ChromaVectorStore(chroma_collection=collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context,
)
```

### PropertyGraphIndex (Knowledge Graph)

```python
from llama_index.core import PropertyGraphIndex
from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore
from llama_index.core.indices.property_graph import (
    SimpleLLMPathExtractor,
    ImplicitPathExtractor,
)

# With Neo4j
graph_store = Neo4jPropertyGraphStore(
    username="neo4j",
    password="password",
    url="bolt://localhost:7687",
    database="neo4j",
)

# Define extractors
kg_extractors = [
    SimpleLLMPathExtractor(
        llm=Settings.llm,
        max_paths_per_chunk=10,
    ),
    ImplicitPathExtractor(),
]

# Create index
index = PropertyGraphIndex.from_documents(
    documents,
    kg_extractors=kg_extractors,
    property_graph_store=graph_store,
    show_progress=True,
)

# Query with different retrievers
from llama_index.core.indices.property_graph import (
    LLMSynonymRetriever,
    VectorContextRetriever,
)

synonym_retriever = LLMSynonymRetriever(index)
vector_retriever = VectorContextRetriever(index)

# Combine retrievers
query_engine = index.as_query_engine(
    sub_retrievers=[synonym_retriever, vector_retriever],
)

response = query_engine.query("What entities are related to AI?")
```

### Index Persistence

```python
from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage

# Save index
index.storage_context.persist(persist_dir="./storage")

# Load index
storage_context = StorageContext.from_defaults(persist_dir="./storage")
index = load_index_from_storage(storage_context)
```

---

## Query Engines

### Basic Query Engine

```python
# Simple query engine
query_engine = index.as_query_engine(
    similarity_top_k=5,
    response_mode="compact",
)

response = query_engine.query("What is RAG?")

# Access response data
print(f"Answer: {response.response}")
print(f"Sources: {len(response.source_nodes)}")

for i, node in enumerate(response.source_nodes):
    print(f"\n--- Source {i+1} (score: {node.score:.3f}) ---")
    print(f"Text: {node.text[:200]}...")
    print(f"Metadata: {node.metadata}")
```

### Streaming Response

```python
query_engine = index.as_query_engine(
    streaming=True,
    similarity_top_k=5,
)

streaming_response = query_engine.query("Explain the architecture")

# Print as it generates
for text in streaming_response.response_gen:
    print(text, end="", flush=True)
```

### Response Modes

```python
# Compact (default) - fast, single LLM call
query_engine = index.as_query_engine(
    response_mode="compact",
    similarity_top_k=5,
)

# Refine - iterative refinement, higher quality
query_engine = index.as_query_engine(
    response_mode="refine",
    similarity_top_k=10,
)

# Tree summarize - hierarchical, good for many chunks
query_engine = index.as_query_engine(
    response_mode="tree_summarize",
    similarity_top_k=20,
)

# No text - return only source nodes
query_engine = index.as_query_engine(
    response_mode="no_text",
)
response = query_engine.query("Find relevant documents")
# response.source_nodes contains retrieved chunks
```

### Custom Prompts

```python
from llama_index.core import PromptTemplate

# Custom QA prompt
qa_prompt = PromptTemplate(
    """You are an expert assistant. Answer the question based only on the context provided.

Context:
{context_str}

Question: {query_str}

Guidelines:
- Be concise and specific
- Cite sources when possible
- Say "I don't know" if the context doesn't contain the answer

Answer:"""
)

# Custom refine prompt
refine_prompt = PromptTemplate(
    """Given the original answer and additional context, improve the answer.

Original Answer: {existing_answer}

Additional Context: {context_msg}

Question: {query_str}

Refined Answer:"""
)

query_engine = index.as_query_engine(
    text_qa_template=qa_prompt,
    refine_template=refine_prompt,
    response_mode="refine",
)
```

### SubQuestionQueryEngine

```python
from llama_index.core.query_engine import SubQuestionQueryEngine
from llama_index.core.tools import QueryEngineTool, ToolMetadata

# Create tools from different indices
tools = [
    QueryEngineTool(
        query_engine=tech_index.as_query_engine(),
        metadata=ToolMetadata(
            name="technical_docs",
            description="Technical documentation and API references",
        ),
    ),
    QueryEngineTool(
        query_engine=business_index.as_query_engine(),
        metadata=ToolMetadata(
            name="business_docs",
            description="Business reports, financials, and strategy",
        ),
    ),
]

# Create sub-question engine
query_engine = SubQuestionQueryEngine.from_defaults(
    query_engine_tools=tools,
    use_async=True,
    verbose=True,
)

# Complex question decomposed into sub-questions
response = query_engine.query(
    "Compare the technical roadmap with Q3 financial projections"
)
```

### RouterQueryEngine

```python
from llama_index.core.query_engine import RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector, LLMMultiSelector

# Single selector - routes to one engine
query_engine = RouterQueryEngine(
    selector=LLMSingleSelector.from_defaults(),
    query_engine_tools=tools,
    verbose=True,
)

# Multi selector - can route to multiple engines
query_engine = RouterQueryEngine(
    selector=LLMMultiSelector.from_defaults(),
    query_engine_tools=tools,
)

response = query_engine.query("What are our Q3 revenue numbers?")
```

### SQL Query Engine

```python
from llama_index.core import SQLDatabase
from llama_index.core.query_engine import NLSQLTableQueryEngine
from sqlalchemy import create_engine

engine = create_engine("postgresql://user:pass@localhost/db")
sql_database = SQLDatabase(engine, include_tables=["users", "orders", "products"])

# Natural language to SQL
query_engine = NLSQLTableQueryEngine(
    sql_database=sql_database,
    tables=["users", "orders"],
)

response = query_engine.query(
    "How many orders were placed last month by premium users?"
)
print(f"SQL: {response.metadata.get('sql_query')}")
print(f"Answer: {response.response}")
```

---

## Retrievers

### Basic Vector Retriever

```python
from llama_index.core.retrievers import VectorIndexRetriever

retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=10,
)

nodes = retriever.retrieve("What is machine learning?")

for node in nodes:
    print(f"Score: {node.score:.3f}")
    print(f"Text: {node.text[:100]}...")
    print(f"Metadata: {node.metadata}")
    print("---")
```

### Hybrid Retriever (BM25 + Vector)

```python
from llama_index.retrievers.bm25 import BM25Retriever
from llama_index.core.retrievers import QueryFusionRetriever

# BM25 (keyword) retriever
bm25_retriever = BM25Retriever.from_defaults(
    nodes=nodes,
    similarity_top_k=10,
)

# Vector retriever
vector_retriever = index.as_retriever(similarity_top_k=10)

# Fusion retriever with reciprocal rank
hybrid_retriever = QueryFusionRetriever(
    retrievers=[bm25_retriever, vector_retriever],
    retriever_weights=[0.4, 0.6],
    num_queries=1,
    mode="reciprocal_rerank",
)

nodes = hybrid_retriever.retrieve("machine learning applications")
```

### Auto-Merging Retriever (Hierarchical)

```python
from llama_index.core.node_parser import HierarchicalNodeParser, get_leaf_nodes
from llama_index.core.retrievers import AutoMergingRetriever
from llama_index.core.storage.docstore import SimpleDocumentStore

# Create hierarchical nodes
parser = HierarchicalNodeParser.from_defaults(
    chunk_sizes=[2048, 512, 128]  # Parent -> child hierarchy
)
nodes = parser.get_nodes_from_documents(documents)
leaf_nodes = get_leaf_nodes(nodes)

# Store all nodes for relationship tracking
docstore = SimpleDocumentStore()
docstore.add_documents(nodes)

# Index only leaf nodes
storage_context = StorageContext.from_defaults(docstore=docstore)
index = VectorStoreIndex(leaf_nodes, storage_context=storage_context)

# Auto-merging retriever
retriever = AutoMergingRetriever(
    index.as_retriever(similarity_top_k=12),
    storage_context=storage_context,
    simple_ratio_thresh=0.5,  # Merge if >50% children retrieved
)

# Returns parent nodes when enough children match
nodes = retriever.retrieve("detailed explanation of the architecture")
```

### Reranking

```python
from llama_index.core.postprocessor import SentenceTransformerRerank
from llama_index.postprocessor.cohere_rerank import CohereRerank

# Local cross-encoder reranking
reranker = SentenceTransformerRerank(
    model="cross-encoder/ms-marco-MiniLM-L-2-v2",
    top_n=5,
)

# Cohere reranking (API)
# reranker = CohereRerank(api_key="...", top_n=5, model="rerank-v3.5")

# Apply to query engine
query_engine = index.as_query_engine(
    similarity_top_k=20,  # Retrieve more initially
    node_postprocessors=[reranker],  # Rerank to top 5
)
```

### Metadata Filtering

```python
from llama_index.core.vector_stores import (
    MetadataFilter,
    MetadataFilters,
    FilterOperator,
)

# Define filters
filters = MetadataFilters(
    filters=[
        MetadataFilter(
            key="category",
            value="technical",
            operator=FilterOperator.EQ,
        ),
        MetadataFilter(
            key="year",
            value=2024,
            operator=FilterOperator.GTE,
        ),
    ],
    condition="and",  # or "or"
)

# Apply to retriever
retriever = index.as_retriever(
    similarity_top_k=10,
    filters=filters,
)

nodes = retriever.retrieve("latest technical updates")
```

---

## Workflows

### Basic Workflow

```python
from llama_index.core.workflow import (
    Workflow,
    StartEvent,
    StopEvent,
    step,
    Event,
)
from pydantic import Field

# Define custom events
class QueryEvent(Event):
    query: str = Field(..., description="User query")

class RetrievalEvent(Event):
    nodes: list = Field(..., description="Retrieved nodes")
    query: str = Field(..., description="Original query")

# Define workflow
class RAGWorkflow(Workflow):
    def __init__(self, index):
        super().__init__()
        self.index = index
        self.retriever = index.as_retriever(similarity_top_k=5)

    @step
    async def retrieve(self, ev: StartEvent) -> RetrievalEvent:
        """Retrieve relevant documents."""
        query = ev.query
        nodes = await self.retriever.aretrieve(query)
        return RetrievalEvent(nodes=nodes, query=query)

    @step
    async def synthesize(self, ev: RetrievalEvent) -> StopEvent:
        """Generate response from retrieved nodes."""
        from llama_index.core import get_response_synthesizer

        synthesizer = get_response_synthesizer(response_mode="compact")
        response = await synthesizer.asynthesize(ev.query, nodes=ev.nodes)
        return StopEvent(result=str(response))

# Run workflow
workflow = RAGWorkflow(index)
result = await workflow.run(query="What is RAG?")
print(result)
```

### Workflow with Context (State Sharing)

```python
from llama_index.core.workflow import Context

class StatefulWorkflow(Workflow):
    @step
    async def step1(self, ctx: Context, ev: StartEvent) -> IntermediateEvent:
        # Store in context
        await ctx.set("original_query", ev.query)
        await ctx.set("step1_result", "processed")
        return IntermediateEvent(data="step1 complete")

    @step
    async def step2(self, ctx: Context, ev: IntermediateEvent) -> StopEvent:
        # Retrieve from context
        query = await ctx.get("original_query")
        step1 = await ctx.get("step1_result")
        return StopEvent(result=f"Query: {query}, Step1: {step1}")
```

### Parallel Event Processing

```python
class ParallelWorkflow(Workflow):
    @step
    async def start(self, ev: StartEvent) -> SearchEvent | AnalyzeEvent:
        # Emit multiple events for parallel processing
        self.send_event(SearchEvent(query=ev.query))
        self.send_event(AnalyzeEvent(query=ev.query))
        return None  # Don't return, events sent separately

    @step
    async def search(self, ev: SearchEvent) -> SearchResultEvent:
        results = await self.perform_search(ev.query)
        return SearchResultEvent(results=results)

    @step
    async def analyze(self, ev: AnalyzeEvent) -> AnalysisResultEvent:
        analysis = await self.perform_analysis(ev.query)
        return AnalysisResultEvent(analysis=analysis)

    @step
    async def combine(
        self,
        ctx: Context,
        ev: SearchResultEvent | AnalysisResultEvent
    ) -> StopEvent | None:
        # Collect both events before proceeding
        events = ctx.collect_events(ev, [SearchResultEvent, AnalysisResultEvent])
        if events is None:
            return None  # Wait for both events

        search_result, analysis_result = events
        combined = f"Search: {search_result.results}, Analysis: {analysis_result.analysis}"
        return StopEvent(result=combined)
```

### Workflow with Loops

```python
class IterativeWorkflow(Workflow):
    @step
    async def start(self, ctx: Context, ev: StartEvent) -> ProcessEvent:
        await ctx.set("iteration", 0)
        await ctx.set("max_iterations", 5)
        return ProcessEvent(data=ev.data)

    @step
    async def process(self, ctx: Context, ev: ProcessEvent) -> ProcessEvent | StopEvent:
        iteration = await ctx.get("iteration")
        max_iterations = await ctx.get("max_iterations")

        # Process data
        result = self.process_data(ev.data)

        # Check completion condition
        if self.is_complete(result) or iteration >= max_iterations:
            return StopEvent(result=result)

        # Continue iterating
        await ctx.set("iteration", iteration + 1)
        return ProcessEvent(data=result)
```

---

## Agents

### ReAct Agent

```python
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import QueryEngineTool, FunctionTool

# Query engine tool
query_tool = QueryEngineTool.from_defaults(
    query_engine=index.as_query_engine(),
    name="knowledge_base",
    description="Search the knowledge base for information about products and services",
)

# Function tool
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression.

    Args:
        expression: Mathematical expression to evaluate (e.g., "2 + 2 * 3")

    Returns:
        Result of the calculation
    """
    try:
        result = eval(expression)  # In production, use safe eval
        return str(result)
    except Exception as e:
        return f"Error: {e}"

calc_tool = FunctionTool.from_defaults(
    fn=calculate,
    name="calculator",
    description="Perform mathematical calculations",
)

# Create agent
agent = ReActAgent.from_tools(
    tools=[query_tool, calc_tool],
    llm=Settings.llm,
    verbose=True,
    max_iterations=10,
)

# Chat
response = agent.chat("What is the price of Product X and what's 20% discount?")
print(response)

# Continue conversation (has memory)
response = agent.chat("And what about Product Y?")
```

### OpenAI Function Calling Agent

```python
from llama_index.agent.openai import OpenAIAgent
from llama_index.llms.openai import OpenAI

agent = OpenAIAgent.from_tools(
    tools=[query_tool, calc_tool],
    llm=OpenAI(model="gpt-4o"),
    verbose=True,
    system_prompt="""You are a helpful assistant specializing in product information.
    Always search the knowledge base before answering product questions.
    Be concise and accurate.""",
)

response = agent.chat("Tell me about the enterprise plan features and pricing")
```

### Agent with Custom Memory

```python
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.memory import VectorMemory

# Simple buffer memory
memory = ChatMemoryBuffer.from_defaults(token_limit=4096)

# Vector memory (for long conversations)
# memory = VectorMemory.from_defaults(
#     vector_store=None,  # Uses in-memory by default
#     embed_model=Settings.embed_model,
#     retriever_kwargs={"similarity_top_k": 3},
# )

agent = ReActAgent.from_tools(
    tools=[query_tool],
    memory=memory,
    verbose=True,
)

# Conversation is maintained
agent.chat("My name is Alice")
response = agent.chat("What's my name?")  # Will remember
```

### AgentWorkflow (Multi-Agent)

```python
from llama_index.core.agent.workflow import AgentWorkflow, FunctionAgent

# Define specialized agents
research_agent = FunctionAgent(
    name="researcher",
    description="Researches information from the knowledge base",
    tools=[query_tool],
    llm=Settings.llm,
    system_prompt="You are a research assistant. Find and summarize relevant information.",
)

analysis_agent = FunctionAgent(
    name="analyst",
    description="Analyzes data and provides insights",
    tools=[calc_tool],
    llm=Settings.llm,
    system_prompt="You are a data analyst. Analyze numbers and provide insights.",
)

writer_agent = FunctionAgent(
    name="writer",
    description="Writes reports and summaries",
    tools=[],
    llm=Settings.llm,
    system_prompt="You are a technical writer. Create clear, well-structured reports.",
)

# Create multi-agent workflow
workflow = AgentWorkflow(
    agents=[research_agent, analysis_agent, writer_agent],
    initial_agent="researcher",
)

# Run with handoffs between agents
result = await workflow.run(
    task="Research our Q3 performance, analyze the growth rate, and write a summary"
)
print(result)
```

### Orchestrator Pattern

```python
from llama_index.core.agent import FunctionCallingAgent
from llama_index.core.tools import QueryEngineTool

# Create sub-agents as tools
research_tool = QueryEngineTool.from_defaults(
    query_engine=research_agent.as_query_engine(),
    name="research_agent",
    description="Use for research tasks and finding information",
)

analysis_tool = QueryEngineTool.from_defaults(
    query_engine=analysis_agent.as_query_engine(),
    name="analysis_agent",
    description="Use for data analysis and calculations",
)

# Orchestrator agent
orchestrator = FunctionCallingAgent.from_tools(
    tools=[research_tool, analysis_tool],
    llm=OpenAI(model="gpt-4o"),
    system_prompt="""You are an orchestrator that coordinates specialized agents.
    For research questions, delegate to the research_agent.
    For analysis questions, delegate to the analysis_agent.
    Combine their outputs to provide comprehensive answers.""",
)

response = await orchestrator.achat(
    "Research market trends and analyze our competitive position"
)
```

---

## Evaluation

### Retrieval Evaluation

```python
from llama_index.core.evaluation import (
    RetrieverEvaluator,
    generate_question_context_pairs,
)

# Generate test dataset from documents
qa_dataset = generate_question_context_pairs(
    nodes=nodes[:50],  # Use subset for efficiency
    llm=Settings.llm,
    num_questions_per_chunk=2,
)

print(f"Generated {len(qa_dataset.queries)} questions")

# Evaluate retriever
retriever = index.as_retriever(similarity_top_k=5)
evaluator = RetrieverEvaluator.from_metric_names(
    ["mrr", "hit_rate"],
    retriever=retriever,
)

# Run evaluation
results = await evaluator.aevaluate_dataset(qa_dataset)

print(f"MRR: {results.mean_mrr:.3f}")
print(f"Hit Rate: {results.mean_hit_rate:.3f}")
```

### Response Evaluation

```python
from llama_index.core.evaluation import (
    FaithfulnessEvaluator,
    RelevancyEvaluator,
    CorrectnessEvaluator,
)

# Create evaluators
faithfulness_evaluator = FaithfulnessEvaluator(llm=Settings.llm)
relevancy_evaluator = RelevancyEvaluator(llm=Settings.llm)

# Query and evaluate
query_engine = index.as_query_engine()
query = "What is the main purpose of the product?"
response = query_engine.query(query)

# Faithfulness: Is the answer grounded in the context?
faith_result = faithfulness_evaluator.evaluate_response(
    query=query,
    response=response,
)
print(f"Faithful: {faith_result.passing}")
print(f"Score: {faith_result.score}")
print(f"Feedback: {faith_result.feedback}")

# Relevancy: Is the answer relevant to the question?
rel_result = relevancy_evaluator.evaluate_response(
    query=query,
    response=response,
)
print(f"Relevant: {rel_result.passing}")
print(f"Score: {rel_result.score}")
```

### Batch Evaluation

```python
from llama_index.core.evaluation import BatchEvalRunner

# Test questions
eval_questions = [
    "What is RAG?",
    "How does vector search work?",
    "What are the main features?",
    "How to get started?",
]

# Create batch runner
runner = BatchEvalRunner(
    evaluators={
        "faithfulness": faithfulness_evaluator,
        "relevancy": relevancy_evaluator,
    },
    workers=4,
)

# Run batch evaluation
eval_results = await runner.aevaluate_queries(
    query_engine=query_engine,
    queries=eval_questions,
)

# Aggregate results
for metric, results in eval_results.items():
    scores = [r.score for r in results if r.score is not None]
    avg_score = sum(scores) / len(scores) if scores else 0
    print(f"{metric}: {avg_score:.3f}")
```

### Pairwise Comparison

```python
from llama_index.core.evaluation import PairwiseComparisonEvaluator

evaluator = PairwiseComparisonEvaluator(llm=Settings.llm)

# Compare two different configurations
query = "Explain the architecture"
response_a = engine_a.query(query)
response_b = engine_b.query(query)

result = evaluator.evaluate(
    query=query,
    response=response_a,
    second_response=response_b,
)

print(f"Winner: {result.value}")  # "A", "B", or "TIE"
print(f"Reason: {result.feedback}")
```

---

## Production Patterns

### Async Operations

```python
import asyncio

# Async query
async def query_async(question: str):
    return await query_engine.aquery(question)

# Batch async queries
async def batch_queries(questions: list[str]):
    tasks = [query_engine.aquery(q) for q in questions]
    responses = await asyncio.gather(*tasks)
    return responses

# Run
responses = asyncio.run(batch_queries([
    "What is RAG?",
    "How does chunking work?",
    "Explain vector search",
]))
```

### Retry Logic

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
)
async def query_with_retry(question: str):
    return await query_engine.aquery(question)

# Usage
try:
    response = await query_with_retry("What is RAG?")
except Exception as e:
    response = "Sorry, I couldn't process your request."
```

### Observability

```python
from llama_index.core.callbacks import CallbackManager, LlamaDebugHandler
from llama_index.core import Settings

# Debug handler for development
debug_handler = LlamaDebugHandler(print_trace_on_end=True)
callback_manager = CallbackManager([debug_handler])
Settings.callback_manager = callback_manager

# Now all operations are traced
response = query_engine.query("What is RAG?")

# Get LLM inputs/outputs
print(debug_handler.get_llm_inputs_outputs())

# Langfuse integration for production
from llama_index.callbacks.langfuse import LangfuseCallbackHandler

langfuse_handler = LangfuseCallbackHandler(
    public_key="pk-...",
    secret_key="sk-...",
    host="https://cloud.langfuse.com",
)
Settings.callback_manager = CallbackManager([langfuse_handler])
```

### Caching

```python
# Embedding cache
Settings.embed_model.cache_folder = "./embedding_cache"

# Index persistence (automatic caching)
index.storage_context.persist(persist_dir="./storage")

# Redis cache for responses (custom implementation)
import redis
import hashlib
import json

redis_client = redis.Redis(host="localhost", port=6379, db=0)

def cached_query(question: str, ttl: int = 3600):
    cache_key = hashlib.md5(question.encode()).hexdigest()

    # Check cache
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)

    # Query and cache
    response = query_engine.query(question)
    result = {
        "response": str(response),
        "sources": [n.text[:100] for n in response.source_nodes]
    }

    redis_client.setex(cache_key, ttl, json.dumps(result))
    return result
```

### Structured Output

```python
from pydantic import BaseModel, Field
from llama_index.core.output_parsers import PydanticOutputParser

class ProductInfo(BaseModel):
    """Product information extracted from documents."""
    name: str = Field(description="Product name")
    description: str = Field(description="Brief description")
    features: list[str] = Field(description="Key features")
    price: float | None = Field(description="Price if available")

output_parser = PydanticOutputParser(output_cls=ProductInfo)

query_engine = index.as_query_engine(
    output_parser=output_parser,
)

response = query_engine.query("Extract information about Product X")
product: ProductInfo = response.response
print(f"Name: {product.name}")
print(f"Features: {product.features}")
```

---

*LlamaIndex Examples v2.0 - 2026-01-25*
