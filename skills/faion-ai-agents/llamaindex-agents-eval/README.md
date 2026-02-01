---
name: faion-llamaindex-agents-eval
user-invocable: false
description: "LlamaIndex: agents, evaluation, production patterns, LlamaCloud"
---

# LlamaIndex: Agents & Evaluation

**Agents, Evaluation, Production Patterns, and LlamaCloud Integration**

Part of the LlamaIndex skill series. See also:
- [llamaindex-basics.md](llamaindex-basics.md) - Installation, data connectors, node parsers
- [llamaindex-indexes-queries.md](llamaindex-indexes-queries.md) - Indexes, query engines, retrievers

---

## Quick Reference

| Component | Purpose |
|-----------|---------|
| **Agents** | Autonomous reasoning with tool use |
| **Evaluation** | Measure retrieval and response quality |
| **Production Patterns** | Caching, streaming, async, observability |
| **LlamaCloud** | Managed parsing and indexing |

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
    description="Search the knowledge base for information",
)

# Custom function tool
def calculate_sum(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

calc_tool = FunctionTool.from_defaults(fn=calculate_sum)

# Create agent
agent = ReActAgent.from_tools(
    tools=[query_tool, calc_tool],
    llm=llm,
    verbose=True,
)

response = agent.chat("What is the total if I add the revenue numbers?")
```

### OpenAI Agent

```python
from llama_index.agent.openai import OpenAIAgent

agent = OpenAIAgent.from_tools(
    tools=[query_tool, calc_tool],
    llm=OpenAI(model="gpt-4o"),
    verbose=True,
    system_prompt="You are a helpful financial analyst.",
)

response = agent.chat("Summarize Q1 performance and calculate growth rate")
```

### Agent with Memory

```python
from llama_index.core.memory import ChatMemoryBuffer

memory = ChatMemoryBuffer.from_defaults(token_limit=4096)

agent = ReActAgent.from_tools(
    tools=[query_tool],
    memory=memory,
    verbose=True,
)

# Maintains conversation history
agent.chat("Tell me about RAG")
agent.chat("How does it compare to fine-tuning?")  # Has context
```

### Multi-Agent Orchestration

```python
from llama_index.core.agent import FunctionCallingAgentWorker
from llama_index.core.agent import AgentRunner

# Worker 1: Research
research_worker = FunctionCallingAgentWorker.from_tools(
    tools=[research_query_tool],
    llm=llm,
)

# Worker 2: Analysis
analysis_worker = FunctionCallingAgentWorker.from_tools(
    tools=[analysis_query_tool, calc_tool],
    llm=llm,
)

# Orchestrator
from llama_index.core.agent import MultiAgentRunner

runner = MultiAgentRunner(
    workers={
        "research": research_worker,
        "analysis": analysis_worker,
    },
    orchestrator_prompt="Route research questions to research agent, analytical questions to analysis agent.",
)

response = runner.chat("Research market trends and analyze growth potential")
```

---

## Evaluation

### Retrieval Evaluation

```python
from llama_index.core.evaluation import (
    RetrieverEvaluator,
    generate_question_context_pairs,
)

# Generate evaluation dataset
qa_dataset = generate_question_context_pairs(
    nodes=nodes[:50],
    llm=llm,
    num_questions_per_chunk=2,
)

# Evaluate retriever
retriever = index.as_retriever(similarity_top_k=5)
evaluator = RetrieverEvaluator.from_metric_names(
    ["mrr", "hit_rate"],
    retriever=retriever,
)

results = await evaluator.aevaluate_dataset(qa_dataset)
print(f"MRR: {results.mean_mrr}")
print(f"Hit Rate: {results.mean_hit_rate}")
```

### Response Evaluation

```python
from llama_index.core.evaluation import (
    FaithfulnessEvaluator,
    RelevancyEvaluator,
    CorrectnessEvaluator,
)

# Faithfulness: Is answer grounded in context?
faithfulness_evaluator = FaithfulnessEvaluator(llm=llm)

# Relevancy: Is answer relevant to question?
relevancy_evaluator = RelevancyEvaluator(llm=llm)

# Correctness: Is answer correct? (needs ground truth)
correctness_evaluator = CorrectnessEvaluator(llm=llm)

# Evaluate single response
query_engine = index.as_query_engine()
response = query_engine.query("What is RAG?")

faithfulness_result = faithfulness_evaluator.evaluate_response(
    query="What is RAG?",
    response=response,
)
print(f"Faithful: {faithfulness_result.passing}")
print(f"Score: {faithfulness_result.score}")
print(f"Feedback: {faithfulness_result.feedback}")

relevancy_result = relevancy_evaluator.evaluate_response(
    query="What is RAG?",
    response=response,
)
print(f"Relevant: {relevancy_result.passing}")
```

### Batch Evaluation

```python
from llama_index.core.evaluation import BatchEvalRunner

# Prepare test questions
eval_questions = [
    "What is RAG?",
    "How does vector search work?",
    "What is chunking?",
]

# Run batch evaluation
runner = BatchEvalRunner(
    evaluators={
        "faithfulness": faithfulness_evaluator,
        "relevancy": relevancy_evaluator,
    },
    workers=4,
)

eval_results = await runner.aevaluate_queries(
    query_engine=query_engine,
    queries=eval_questions,
)

# Aggregate results
for metric, results in eval_results.items():
    scores = [r.score for r in results]
    print(f"{metric}: {sum(scores)/len(scores):.2f}")
```

### Pairwise Evaluation

```python
from llama_index.core.evaluation import PairwiseComparisonEvaluator

evaluator = PairwiseComparisonEvaluator(llm=llm)

# Compare two query engines
result = evaluator.evaluate(
    query="Explain RAG architecture",
    response=response_a,
    second_response=response_b,
)

print(f"Winner: {result.value}")  # A, B, or TIE
print(f"Reason: {result.feedback}")
```

---

## Production Patterns

### Caching

```python
from llama_index.core import Settings
from llama_index.core.llms import MockLLM

# LLM response caching
from llama_index.core.callbacks import LlamaDebugHandler

# Enable caching for embeddings
Settings.embed_model.cache_folder = "./embedding_cache"

# Persistent index storage
from llama_index.core import StorageContext, load_index_from_storage

# Save
index.storage_context.persist(persist_dir="./storage")

# Load
storage_context = StorageContext.from_defaults(persist_dir="./storage")
index = load_index_from_storage(storage_context)
```

### Streaming

```python
# Streaming responses
query_engine = index.as_query_engine(streaming=True)
streaming_response = query_engine.query("Explain RAG")

for text in streaming_response.response_gen:
    print(text, end="", flush=True)
```

### Async Operations

```python
import asyncio

# Async query
async def query_async():
    response = await query_engine.aquery("What is RAG?")
    return response

# Batch async queries
async def batch_queries(queries: list[str]):
    tasks = [query_engine.aquery(q) for q in queries]
    responses = await asyncio.gather(*tasks)
    return responses

# Run
responses = asyncio.run(batch_queries([
    "What is RAG?",
    "How does chunking work?",
    "Explain vector search",
]))
```

### Observability

```python
from llama_index.core.callbacks import CallbackManager, LlamaDebugHandler

# Debug handler
debug_handler = LlamaDebugHandler(print_trace_on_end=True)
callback_manager = CallbackManager([debug_handler])

Settings.callback_manager = callback_manager

# Now all operations are traced
query_engine = index.as_query_engine()
response = query_engine.query("What is RAG?")

# Get trace
print(debug_handler.get_llm_inputs_outputs())

# Integration with observability platforms
# pip install llama-index-instrumentation-langfuse
from llama_index.instrumentation.langfuse import LangfuseInstrumentation

instrumentation = LangfuseInstrumentation(
    public_key="pk-...",
    secret_key="sk-...",
)
Settings.instrumentation = instrumentation
```

### Error Handling

```python
from llama_index.core.llms import ChatMessage

try:
    response = query_engine.query("What is RAG?")
except Exception as e:
    # Fallback response
    response = "I'm sorry, I couldn't process your question. Please try again."

# Retry with exponential backoff
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def query_with_retry(question: str):
    return query_engine.query(question)
```

---

## LlamaCloud Integration

### LlamaParse (Document Processing)

```python
from llama_parse import LlamaParse

# Advanced PDF parsing with OCR and table extraction
parser = LlamaParse(
    api_key="llx-...",
    result_type="markdown",
    num_workers=4,
    verbose=True,
)

documents = parser.load_data("./complex_document.pdf")
```

### LlamaCloud Index

```python
from llama_index.indices.managed.llama_cloud import LlamaCloudIndex

# Create managed index
index = LlamaCloudIndex.from_documents(
    documents,
    name="my_index",
    project_name="my_project",
    api_key="llx-...",
)

# Query
query_engine = index.as_query_engine()
response = query_engine.query("What is RAG?")
```

---

## Common Pitfalls

| Issue | Solution |
|-------|----------|
| **Low retrieval quality** | Increase top_k, add reranking, tune chunk size |
| **Hallucinations** | Use faithfulness eval, stricter prompts, lower temperature |
| **Slow queries** | Use async, caching, reduce chunk overlap |
| **Missing context** | Increase chunk size, use hierarchical parsing |
| **Cost too high** | Use smaller embedding model, cache embeddings |
| **Index too large** | Use metadata filtering, partition by topic |

---

## References

- [LlamaIndex Documentation](https://docs.llamaindex.ai/)
- [LlamaHub Connectors](https://llamahub.ai/)
- [LlamaIndex GitHub](https://github.com/run-llama/llama_index)
- [LlamaCloud](https://cloud.llamaindex.ai/)

---

## Related Files

- [llamaindex-basics.md](llamaindex-basics.md) - Installation, data connectors, node parsers
- [llamaindex-indexes-queries.md](llamaindex-indexes-queries.md) - Indexes, query engines, retrievers
- [langchain.md](langchain.md) - LangChain orchestration and chains
- [vector-databases.md](vector-databases.md) - Vector database operations
- [embeddings.md](embeddings.md) - Embedding models

---

*LlamaIndex Agents & Evaluation v1.0*
## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Generate tool definitions from API | haiku | Mechanical transformation |
| Review agent reasoning chains | sonnet | Requires logic analysis |
| Design multi-agent orchestration | opus | Complex coordination patterns |

