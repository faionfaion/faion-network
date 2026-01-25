---
name: faion-langchain-basics
user-invocable: false
description: "LangChain basics: core concepts, installation, chain patterns, prompts, parsers"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(python:*), Bash(pip:*)
---

# LangChain Basics

**Communication: User's language. Docs/code: English.**

## Purpose

Core LangChain concepts, installation, chain patterns, prompt engineering, and output parsing.

## When to Use

- Building sequential AI pipelines
- Creating prompt templates
- Parsing structured outputs
- Router and fallback chains
- Basic streaming

---

# Section 1: Core Concepts

## LangChain vs LangGraph

| Component | Purpose | Use When |
|-----------|---------|----------|
| **LangChain** | Chains, prompts, memory | Simple sequential pipelines |
| **LangGraph** | State machines, agents | Complex control flow, agents |

**Recommendation:** Use LangGraph for new projects. LangChain for simple chains.

## Installation

```bash
# Core packages
pip install langchain langchain-core langchain-community

# LangGraph for agents
pip install langgraph

# Provider-specific
pip install langchain-openai langchain-anthropic langchain-google-genai

# Observability
pip install langsmith
```

## Environment Setup

```python
import os

# LLM API keys
os.environ["OPENAI_API_KEY"] = "sk-..."
os.environ["ANTHROPIC_API_KEY"] = "sk-ant-..."

# LangSmith tracing (optional but recommended)
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "ls__..."
os.environ["LANGCHAIN_PROJECT"] = "my-project"
```

---

# Section 2: Chain Patterns

## Pattern 1: Sequential Chain

Simple A → B → C pipeline.

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

# Define components
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{input}")
])
model = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

# Chain using LCEL (LangChain Expression Language)
chain = prompt | model | parser

# Invoke
result = chain.invoke({"input": "What is LangChain?"})
```

## Pattern 2: Router Chain

Route to different chains based on input.

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableBranch, RunnableLambda

# Define specialized chains
math_prompt = ChatPromptTemplate.from_template("Solve this math problem: {input}")
code_prompt = ChatPromptTemplate.from_template("Write code for: {input}")
general_prompt = ChatPromptTemplate.from_template("Answer: {input}")

math_chain = math_prompt | model | parser
code_chain = code_prompt | model | parser
general_chain = general_prompt | model | parser

# Router function
def route(info: dict) -> str:
    topic = info.get("topic", "").lower()
    if "math" in topic:
        return "math"
    elif "code" in topic:
        return "code"
    return "general"

# Create router
branch = RunnableBranch(
    (lambda x: route(x) == "math", math_chain),
    (lambda x: route(x) == "code", code_chain),
    general_chain  # Default
)

# Use
result = branch.invoke({"input": "2 + 2", "topic": "math"})
```

## Pattern 3: MapReduce Chain

Process multiple items in parallel, then combine.

```python
from langchain_core.runnables import RunnableParallel

# Map: process each document
summarize_prompt = ChatPromptTemplate.from_template(
    "Summarize this document in 2 sentences:\n\n{document}"
)
summarize_chain = summarize_prompt | model | parser

# Reduce: combine summaries
combine_prompt = ChatPromptTemplate.from_template(
    "Combine these summaries into a coherent overview:\n\n{summaries}"
)
combine_chain = combine_prompt | model | parser

# MapReduce function
def map_reduce(documents: list[str]) -> str:
    # Map phase
    summaries = [summarize_chain.invoke({"document": doc}) for doc in documents]

    # Reduce phase
    combined = combine_chain.invoke({"summaries": "\n\n".join(summaries)})
    return combined

# With parallel execution
from langchain_core.runnables import RunnableParallel

def parallel_map(documents: list[str]) -> list[str]:
    parallel = RunnableParallel({
        f"doc_{i}": summarize_chain for i, _ in enumerate(documents)
    })
    inputs = {f"doc_{i}": {"document": doc} for i, doc in enumerate(documents)}
    results = parallel.invoke(inputs)
    return list(results.values())
```

## Pattern 4: Fallback Chain

Try primary, fall back to secondary on failure.

```python
from langchain_core.runnables import RunnableWithFallbacks

# Primary (expensive, high quality)
primary = ChatOpenAI(model="gpt-4o") | parser

# Fallback (cheaper, faster)
fallback = ChatOpenAI(model="gpt-4o-mini") | parser

# Chain with fallback
robust_chain = primary.with_fallbacks([fallback])

# Will try gpt-4o first, then gpt-4o-mini if it fails
result = robust_chain.invoke("Complex question...")
```

---

# Section 3: Prompt Templates

## Basic Templates

```python
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder
)

# Simple template
simple = ChatPromptTemplate.from_template("Translate to French: {text}")

# With system message
chat = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful translator."),
    ("human", "Translate to {language}: {text}")
])

# With message history placeholder
with_history = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])
```

## Few-Shot Templates

```python
from langchain_core.prompts import FewShotChatMessagePromptTemplate

examples = [
    {"input": "2 + 2", "output": "4"},
    {"input": "5 * 3", "output": "15"},
]

example_prompt = ChatPromptTemplate.from_messages([
    ("human", "{input}"),
    ("ai", "{output}")
])

few_shot = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples
)

final_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a calculator."),
    few_shot,
    ("human", "{input}")
])
```

## Dynamic Few-Shot Selection

```python
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

examples = [
    {"input": "happy", "output": "sad"},
    {"input": "tall", "output": "short"},
    {"input": "fast", "output": "slow"},
    {"input": "rich", "output": "poor"},
]

selector = SemanticSimilarityExampleSelector.from_examples(
    examples,
    OpenAIEmbeddings(),
    Chroma,
    k=2  # Select 2 most relevant examples
)

dynamic_few_shot = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    example_selector=selector
)

# Will select most relevant examples for "big"
result = dynamic_few_shot.invoke({"input": "big"})
```

---

# Section 4: Output Parsers

## String Parser

```python
from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()
chain = prompt | model | parser
```

## JSON Parser

```python
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

class Answer(BaseModel):
    answer: str = Field(description="The answer")
    confidence: float = Field(description="Confidence 0-1")

parser = JsonOutputParser(pydantic_object=Answer)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer questions with confidence score."),
    ("human", "{question}\n\n{format_instructions}")
])

chain = prompt.partial(format_instructions=parser.get_format_instructions()) | model | parser
```

## Structured Output (Recommended)

```python
from langchain_core.pydantic_v1 import BaseModel, Field

class SearchQuery(BaseModel):
    """Search query parameters."""
    query: str = Field(description="The search query")
    filters: list[str] = Field(default=[], description="Filters to apply")
    limit: int = Field(default=10, description="Max results")

# Use with_structured_output for reliable parsing
structured_model = model.with_structured_output(SearchQuery)

result = structured_model.invoke("Find Python tutorials, limit 5")
# Returns: SearchQuery(query="Python tutorials", filters=[], limit=5)
```

## Streaming Parser

```python
from langchain_core.output_parsers import JsonOutputParser

parser = JsonOutputParser()

chain = prompt | model | parser

# Stream partial results
for chunk in chain.stream({"input": "Generate a complex JSON"}):
    print(chunk)  # Partial JSON as it's generated
```

---

# Section 5: Streaming

## Basic Streaming

```python
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o", streaming=True)

# Stream tokens
for chunk in model.stream("Tell me a story"):
    print(chunk.content, end="", flush=True)
```

## Chain Streaming

```python
chain = prompt | model | parser

# Stream final output
for chunk in chain.stream({"input": "Hello"}):
    print(chunk, end="", flush=True)

# Stream events (more detailed)
async for event in chain.astream_events({"input": "Hello"}, version="v2"):
    if event["event"] == "on_chat_model_stream":
        print(event["data"]["chunk"].content, end="")
```

---

# Section 6: Error Handling

## Retry Logic

```python
from langchain_core.runnables import RunnableRetry
from tenacity import retry, stop_after_attempt, wait_exponential

# Built-in retry
chain_with_retry = chain.with_retry(
    stop_after_attempt=3,
    wait_exponential_jitter=True
)

# Custom retry with tenacity
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10)
)
def robust_invoke(chain, input):
    return chain.invoke(input)
```

## Fallback Chains

```python
from langchain_core.runnables import RunnableWithFallbacks

primary = ChatOpenAI(model="gpt-4o")
fallback_1 = ChatOpenAI(model="gpt-4o-mini")
fallback_2 = ChatOpenAI(model="gpt-3.5-turbo")

robust_model = primary.with_fallbacks([fallback_1, fallback_2])
```

---

# Section 7: Best Practices

## Debugging with LangSmith

```python
import os

# Enable tracing
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "ls__..."
os.environ["LANGCHAIN_PROJECT"] = "my-project"

# Add metadata for filtering
chain = prompt | model | parser

result = chain.invoke(
    {"input": "Hello"},
    config={
        "metadata": {"user_id": "123", "feature": "chat"},
        "tags": ["production", "v2"]
    }
)
```

## Cost Optimization

```python
from langchain_community.callbacks import get_openai_callback

# Track costs
with get_openai_callback() as cb:
    result = chain.invoke({"input": "Hello"})
    print(f"Tokens: {cb.total_tokens}")
    print(f"Cost: ${cb.total_cost:.4f}")

# Use cheaper models for simple tasks
cheap_model = ChatOpenAI(model="gpt-4o-mini")
expensive_model = ChatOpenAI(model="gpt-4o")

def select_model(complexity: str):
    if complexity == "simple":
        return cheap_model
    return expensive_model
```

## Latency Reduction

```python
from langchain_core.runnables import RunnableParallel

# Parallel execution
parallel = RunnableParallel({
    "summary": summarize_chain,
    "keywords": extract_keywords_chain,
    "sentiment": sentiment_chain
})

# All three run in parallel
result = parallel.invoke({"text": "Long document..."})

# Caching
from langchain.cache import InMemoryCache
from langchain.globals import set_llm_cache

set_llm_cache(InMemoryCache())

# Use streaming for perceived speed
for chunk in chain.stream({"input": "Hello"}):
    yield chunk
```

---

# Quick Reference

## Chain Types

| Pattern | Use Case | Example |
|---------|----------|---------|
| Sequential | A then B | prompt \| model \| parser |
| Router | Dynamic routing | RunnableBranch |
| MapReduce | Process + combine | Parallel map, then reduce |
| Fallback | Resilience | with_fallbacks() |

---

*faion-langchain-basics v1.0*
*LangChain 0.3.x*
*Covers: core concepts, chains, prompts, parsers, streaming, error handling*
