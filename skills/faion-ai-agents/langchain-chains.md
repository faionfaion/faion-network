# LangChain Chains

**Part of:** [langchain.md](langchain.md)

## Chain Patterns

### Pattern 1: Sequential Chain

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

### Pattern 2: Router Chain

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

### Pattern 3: MapReduce Chain

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

### Pattern 4: Fallback Chain

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

## Prompt Templates

### Basic Templates

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

### Few-Shot Templates

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

### Dynamic Few-Shot Selection

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

## Output Parsers

### String Parser

```python
from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()
chain = prompt | model | parser
```

### JSON Parser

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

### Structured Output (Recommended)

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

### Streaming Parser

```python
from langchain_core.output_parsers import JsonOutputParser

parser = JsonOutputParser()

chain = prompt | model | parser

# Stream partial results
for chunk in chain.stream({"input": "Generate a complex JSON"}):
    print(chunk)  # Partial JSON as it's generated
```

## Error Handling

### Retry Logic

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

### Fallback Chains

```python
from langchain_core.runnables import RunnableWithFallbacks

primary = ChatOpenAI(model="gpt-4o")
fallback_1 = ChatOpenAI(model="gpt-4o-mini")
fallback_2 = ChatOpenAI(model="gpt-3.5-turbo")

robust_model = primary.with_fallbacks([fallback_1, fallback_2])
```

## Streaming

### Basic Streaming

```python
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o", streaming=True)

# Stream tokens
for chunk in model.stream("Tell me a story"):
    print(chunk.content, end="", flush=True)
```

### Chain Streaming

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

*Part of faion-langchain-skill v1.0*
*See also: [langchain-agents-architectures.md](langchain-agents-architectures.md), [langchain-agents-multi-agent.md](langchain-agents-multi-agent.md), [langchain-memory.md](langchain-memory.md), [langchain-workflows.md](langchain-workflows.md)*
