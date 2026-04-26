# LangChain Examples

Comprehensive examples for LCEL chains, LangGraph agents, RAG pipelines, and tool calling.

---

## Table of Contents

1. [LCEL Chain Examples](#lcel-chain-examples)
2. [LangGraph Agent Examples](#langgraph-agent-examples)
3. [RAG Examples](#rag-examples)
4. [Tool Calling Examples](#tool-calling-examples)
5. [Memory Examples](#memory-examples)
6. [Production Patterns](#production-patterns)

---

## LCEL Chain Examples

### Example 1: Basic Sequential Chain

Simple prompt -> model -> output pattern.

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# Components
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that speaks concisely."),
    ("human", "{input}")
])
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
parser = StrOutputParser()

# Chain with LCEL pipe syntax
chain = prompt | model | parser

# Invoke
result = chain.invoke({"input": "What is Python?"})
print(result)

# Stream
for chunk in chain.stream({"input": "What is Python?"}):
    print(chunk, end="", flush=True)

# Batch
results = chain.batch([
    {"input": "What is Python?"},
    {"input": "What is JavaScript?"}
])
```

### Example 2: Chain with Structured Output

Parse LLM output into Pydantic models.

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import List

# Define output schema
class MovieRecommendation(BaseModel):
    """Movie recommendation with reasoning."""
    title: str = Field(description="Movie title")
    year: int = Field(description="Release year")
    genre: str = Field(description="Primary genre")
    reason: str = Field(description="Why this movie fits the request")

class MovieList(BaseModel):
    """List of movie recommendations."""
    movies: List[MovieRecommendation] = Field(description="List of 3 movies")

# Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a movie recommendation expert."),
    ("human", "Recommend 3 movies similar to: {movie}")
])

# Model with structured output
model = ChatOpenAI(model="gpt-4o-mini")
structured_model = model.with_structured_output(MovieList)

# Chain
chain = prompt | structured_model

# Invoke - returns MovieList object
result = chain.invoke({"movie": "Inception"})
for movie in result.movies:
    print(f"{movie.title} ({movie.year}) - {movie.genre}")
    print(f"  Reason: {movie.reason}")
```

### Example 3: Router Chain

Route to different chains based on input classification.

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch, RunnableLambda
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

# Specialized prompts
math_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a math tutor. Solve step by step."),
    ("human", "{input}")
])

code_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a coding expert. Provide clean, commented code."),
    ("human", "{input}")
])

general_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{input}")
])

# Classification prompt
classifier_prompt = ChatPromptTemplate.from_messages([
    ("system", "Classify the query into: math, code, or general. Reply with just the category."),
    ("human", "{input}")
])

# Classifier chain
classifier = classifier_prompt | model | parser

# Specialized chains
math_chain = math_prompt | model | parser
code_chain = code_prompt | model | parser
general_chain = general_prompt | model | parser

# Full routing chain
def route(info: dict) -> str:
    classification = classifier.invoke({"input": info["input"]}).lower().strip()
    if "math" in classification:
        return math_chain.invoke(info)
    elif "code" in classification:
        return code_chain.invoke(info)
    else:
        return general_chain.invoke(info)

# Alternative: RunnableBranch (more explicit)
router = RunnableBranch(
    (lambda x: "math" in classifier.invoke(x).lower(), math_chain),
    (lambda x: "code" in classifier.invoke(x).lower(), code_chain),
    general_chain  # Default
)

# Use
result = RunnableLambda(route).invoke({"input": "Calculate 15% of 230"})
print(result)
```

### Example 4: Parallel Execution

Run multiple chains in parallel and combine results.

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnableLambda
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

# Individual analysis chains
summary_prompt = ChatPromptTemplate.from_template(
    "Summarize this text in 2 sentences:\n\n{text}"
)
sentiment_prompt = ChatPromptTemplate.from_template(
    "Analyze the sentiment (positive/negative/neutral) of this text:\n\n{text}"
)
keywords_prompt = ChatPromptTemplate.from_template(
    "Extract 5 keywords from this text as a comma-separated list:\n\n{text}"
)

summary_chain = summary_prompt | model | parser
sentiment_chain = sentiment_prompt | model | parser
keywords_chain = keywords_prompt | model | parser

# Parallel execution
analysis = RunnableParallel(
    summary=summary_chain,
    sentiment=sentiment_chain,
    keywords=keywords_chain
)

# Use
text = """
LangChain is a framework for developing applications powered by language models.
It enables applications that are context-aware and can reason about how to answer
based on the context provided. LangChain provides modular components, use-case
specific chains, and agent architectures for building sophisticated AI applications.
"""

result = analysis.invoke({"text": text})
print(f"Summary: {result['summary']}")
print(f"Sentiment: {result['sentiment']}")
print(f"Keywords: {result['keywords']}")
```

### Example 5: Chain with Retry and Fallback

Robust chain with error handling.

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

# Primary model (expensive, capable)
primary_model = ChatOpenAI(model="gpt-4o")

# Fallback models (cheaper, still capable)
fallback_1 = ChatOpenAI(model="gpt-4o-mini")
fallback_2 = ChatAnthropic(model="claude-3-haiku-20240307")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{input}")
])
parser = StrOutputParser()

# Chain with retry
primary_chain = (prompt | primary_model | parser).with_retry(
    stop_after_attempt=3,
    wait_exponential_jitter=True
)

# Fallback chains
fallback_chain_1 = prompt | fallback_1 | parser
fallback_chain_2 = prompt | fallback_2 | parser

# Combined with fallbacks
robust_chain = primary_chain.with_fallbacks([
    fallback_chain_1,
    fallback_chain_2
])

# This will:
# 1. Try primary (gpt-4o) with 3 retries
# 2. If still failing, try gpt-4o-mini
# 3. If still failing, try Claude Haiku
result = robust_chain.invoke({"input": "Explain quantum computing"})
```

### Example 6: Map-Reduce for Document Processing

Process multiple documents and combine results.

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnableLambda
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

# Map: Summarize each document
map_prompt = ChatPromptTemplate.from_template(
    "Summarize this document in 3 bullet points:\n\n{document}"
)
map_chain = map_prompt | model | parser

# Reduce: Combine summaries
reduce_prompt = ChatPromptTemplate.from_template(
    """Combine these document summaries into a coherent overview:

{summaries}

Provide a unified summary covering all key points."""
)
reduce_chain = reduce_prompt | model | parser

def map_reduce(documents: list[str]) -> str:
    """Map-reduce over documents."""
    # Map phase (could be parallelized with RunnableParallel for small batches)
    summaries = []
    for doc in documents:
        summary = map_chain.invoke({"document": doc})
        summaries.append(summary)

    # Reduce phase
    combined = reduce_chain.invoke({"summaries": "\n\n---\n\n".join(summaries)})
    return combined

# Alternative: Batch processing (more efficient)
def map_reduce_batch(documents: list[str]) -> str:
    """Map-reduce with batching."""
    # Map phase with batching
    inputs = [{"document": doc} for doc in documents]
    summaries = map_chain.batch(inputs, config={"max_concurrency": 5})

    # Reduce phase
    combined = reduce_chain.invoke({"summaries": "\n\n---\n\n".join(summaries)})
    return combined

# Use
documents = [
    "Document 1 content...",
    "Document 2 content...",
    "Document 3 content..."
]
overview = map_reduce_batch(documents)
print(overview)
```

---

## LangGraph Agent Examples

### Example 1: Simple ReAct Agent

Basic tool-using agent with prebuilt ReAct pattern.

```python
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
import httpx

# Define tools
@tool
def search_web(query: str) -> str:
    """Search the web for current information about a topic."""
    # Simplified - use actual search API in production
    return f"Search results for '{query}': [Simulated search results]"

@tool
def calculate(expression: str) -> str:
    """Calculate a mathematical expression. Use Python syntax."""
    try:
        # Safety: only allow basic math operations
        allowed_chars = set("0123456789+-*/().% ")
        if not all(c in allowed_chars for c in expression):
            return "Error: Only basic math operations allowed"
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {e}"

@tool
def get_weather(city: str) -> str:
    """Get current weather for a city."""
    # Simplified - use actual weather API in production
    return f"Weather in {city}: Sunny, 22C"

# Create agent
model = ChatOpenAI(model="gpt-4o-mini")
tools = [search_web, calculate, get_weather]

agent = create_react_agent(model, tools)

# Run
result = agent.invoke({
    "messages": [("human", "What's the weather in Paris and calculate 15% tip on $85")]
})

# Print conversation
for message in result["messages"]:
    if hasattr(message, 'content') and message.content:
        print(f"{message.type}: {message.content}")
```

### Example 2: Custom LangGraph Agent

Full control with custom state and nodes.

```python
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from typing import TypedDict, Annotated, Sequence
import operator
import json

# State definition
class AgentState(TypedDict):
    messages: Annotated[Sequence, operator.add]
    next_action: str

# Tools
@tool
def get_stock_price(symbol: str) -> str:
    """Get current stock price for a symbol like AAPL, GOOGL."""
    # Simulated prices
    prices = {"AAPL": 185.50, "GOOGL": 142.30, "MSFT": 378.90}
    price = prices.get(symbol.upper(), "Unknown")
    return f"{symbol.upper()} current price: ${price}"

@tool
def get_company_info(symbol: str) -> str:
    """Get company information for a stock symbol."""
    info = {
        "AAPL": "Apple Inc. - Technology company, market cap $2.9T",
        "GOOGL": "Alphabet Inc. - Technology company, market cap $1.7T"
    }
    return info.get(symbol.upper(), "Company not found")

tools = [get_stock_price, get_company_info]
model = ChatOpenAI(model="gpt-4o-mini").bind_tools(tools)

# Node: Agent decides what to do
def agent_node(state: AgentState) -> AgentState:
    """Agent decides next action."""
    response = model.invoke(state["messages"])

    # Determine next action
    if response.tool_calls:
        next_action = "tools"
    else:
        next_action = "end"

    return {
        "messages": [response],
        "next_action": next_action
    }

# Node: Execute tools
def tool_node(state: AgentState) -> AgentState:
    """Execute tool calls."""
    last_message = state["messages"][-1]
    tool_results = []

    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        # Find and execute tool
        for t in tools:
            if t.name == tool_name:
                result = t.invoke(tool_args)
                tool_results.append(
                    ToolMessage(content=result, tool_call_id=tool_call["id"])
                )
                break

    return {"messages": tool_results, "next_action": "agent"}

# Routing function
def should_continue(state: AgentState) -> str:
    return state["next_action"]

# Build graph
graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.add_node("tools", tool_node)

graph.set_entry_point("agent")
graph.add_conditional_edges(
    "agent",
    should_continue,
    {"tools": "tools", "end": END}
)
graph.add_edge("tools", "agent")

agent = graph.compile()

# Run
result = agent.invoke({
    "messages": [HumanMessage(content="Get me the stock price and company info for Apple")]
})

for msg in result["messages"]:
    print(f"{type(msg).__name__}: {msg.content[:100]}...")
```

### Example 3: Multi-Agent Supervisor

Supervisor routes tasks to specialized agents.

```python
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from typing import TypedDict, Annotated, Literal
import operator

# State
class SupervisorState(TypedDict):
    messages: Annotated[list, operator.add]
    next_worker: str
    task: str
    results: Annotated[list[str], operator.add]
    final_answer: str

model = ChatOpenAI(model="gpt-4o-mini")

# Supervisor: Routes to appropriate worker
def supervisor(state: SupervisorState) -> SupervisorState:
    """Decide which worker should handle the task."""
    prompt = f"""You are a supervisor managing a team. Based on the task, decide which worker should handle it.

Workers:
- researcher: For finding information, facts, and research
- analyst: For analyzing data, comparisons, and insights
- writer: For creating content, summaries, and reports

Task: {state['task']}
Previous results: {state.get('results', [])}

If the task is complete, respond with "DONE".
Otherwise, respond with just the worker name: researcher, analyst, or writer"""

    response = model.invoke(prompt)
    decision = response.content.strip().lower()

    if "done" in decision:
        return {"next_worker": "synthesizer"}
    elif "researcher" in decision:
        return {"next_worker": "researcher"}
    elif "analyst" in decision:
        return {"next_worker": "analyst"}
    elif "writer" in decision:
        return {"next_worker": "writer"}
    else:
        return {"next_worker": "synthesizer"}

# Worker: Researcher
def researcher(state: SupervisorState) -> SupervisorState:
    """Research information about the topic."""
    prompt = f"""You are a researcher. Find relevant information about:

Task: {state['task']}

Provide factual, well-researched information."""

    response = model.invoke(prompt)
    return {"results": [f"RESEARCH: {response.content}"]}

# Worker: Analyst
def analyst(state: SupervisorState) -> SupervisorState:
    """Analyze information and provide insights."""
    prompt = f"""You are an analyst. Analyze the following:

Task: {state['task']}
Available information: {state.get('results', [])}

Provide analytical insights and comparisons."""

    response = model.invoke(prompt)
    return {"results": [f"ANALYSIS: {response.content}"]}

# Worker: Writer
def writer(state: SupervisorState) -> SupervisorState:
    """Create content based on research and analysis."""
    prompt = f"""You are a writer. Create content based on:

Task: {state['task']}
Information: {state.get('results', [])}

Write clear, engaging content."""

    response = model.invoke(prompt)
    return {"results": [f"CONTENT: {response.content}"]}

# Synthesizer: Combine all results
def synthesizer(state: SupervisorState) -> SupervisorState:
    """Combine all worker outputs into final answer."""
    prompt = f"""Synthesize these results into a final, comprehensive answer:

Original task: {state['task']}

Results from team:
{chr(10).join(state.get('results', []))}

Provide a unified, well-structured response."""

    response = model.invoke(prompt)
    return {"final_answer": response.content}

# Routing
def route_to_worker(state: SupervisorState) -> str:
    return state["next_worker"]

# Build graph
graph = StateGraph(SupervisorState)

graph.add_node("supervisor", supervisor)
graph.add_node("researcher", researcher)
graph.add_node("analyst", analyst)
graph.add_node("writer", writer)
graph.add_node("synthesizer", synthesizer)

graph.set_entry_point("supervisor")

# Supervisor routes to workers
graph.add_conditional_edges(
    "supervisor",
    route_to_worker,
    {
        "researcher": "researcher",
        "analyst": "analyst",
        "writer": "writer",
        "synthesizer": "synthesizer"
    }
)

# Workers return to supervisor for next task
graph.add_edge("researcher", "supervisor")
graph.add_edge("analyst", "supervisor")
graph.add_edge("writer", "supervisor")
graph.add_edge("synthesizer", END)

multi_agent = graph.compile()

# Run
result = multi_agent.invoke({
    "task": "Compare Python and JavaScript for web development",
    "messages": [],
    "results": [],
    "final_answer": ""
})

print(result["final_answer"])
```

### Example 4: Agent with Human-in-the-Loop

Pause for human approval before sensitive actions.

```python
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from typing import TypedDict, Literal

# State
class HumanLoopState(TypedDict):
    request: str
    plan: str
    approved: bool
    result: str

model = ChatOpenAI(model="gpt-4o-mini")

# Node: Create plan
def create_plan(state: HumanLoopState) -> HumanLoopState:
    """Create a plan for the request."""
    prompt = f"""Create a detailed plan for this request:

Request: {state['request']}

List the steps you would take."""

    response = model.invoke(prompt)
    return {"plan": response.content}

# Node: Execute plan (after approval)
def execute_plan(state: HumanLoopState) -> HumanLoopState:
    """Execute the approved plan."""
    prompt = f"""Execute this plan:

Plan: {state['plan']}

Provide the results of executing each step."""

    response = model.invoke(prompt)
    return {"result": response.content}

# Routing based on approval
def check_approval(state: HumanLoopState) -> Literal["execute", "end"]:
    if state.get("approved", False):
        return "execute"
    return "end"

# Build graph
graph = StateGraph(HumanLoopState)

graph.add_node("plan", create_plan)
graph.add_node("execute", execute_plan)

graph.set_entry_point("plan")
graph.add_conditional_edges("plan", check_approval)
graph.add_edge("execute", END)

# Compile with checkpointing and interrupt
memory = MemorySaver()
agent = graph.compile(
    checkpointer=memory,
    interrupt_after=["plan"]  # Pause after planning
)

# First run - creates plan and stops
config = {"configurable": {"thread_id": "session-1"}}
result = agent.invoke(
    {"request": "Delete all test files from the project"},
    config
)

print("Plan created:")
print(result["plan"])
print("\nAgent paused. Review the plan above.")

# Human reviews and approves
# In a real app, this would be a UI interaction
user_approved = input("Approve this plan? (yes/no): ").lower() == "yes"

# Resume with approval status
if user_approved:
    result = agent.invoke(
        {"approved": True},
        config
    )
    print("\nExecution result:")
    print(result["result"])
else:
    print("Plan rejected. No action taken.")
```

### Example 5: Plan-and-Execute Agent

Create a plan first, then execute steps sequentially.

```python
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from typing import TypedDict, List
import re

# State
class PlanState(TypedDict):
    objective: str
    plan: List[str]
    current_step: int
    step_results: List[str]
    final_result: str

model = ChatOpenAI(model="gpt-4o-mini")

# Node: Create plan
def create_plan(state: PlanState) -> PlanState:
    """Create a step-by-step plan."""
    prompt = f"""Create a numbered plan to achieve this objective:

Objective: {state['objective']}

Create 3-5 clear, actionable steps. Format as:
1. Step one
2. Step two
..."""

    response = model.invoke(prompt)

    # Parse steps
    lines = response.content.strip().split('\n')
    steps = [line.strip() for line in lines if re.match(r'^\d+\.', line.strip())]

    return {"plan": steps, "current_step": 0, "step_results": []}

# Node: Execute current step
def execute_step(state: PlanState) -> PlanState:
    """Execute the current step."""
    current = state["plan"][state["current_step"]]
    context = "\n".join(state["step_results"]) if state["step_results"] else "None yet"

    prompt = f"""Execute this step:

Overall objective: {state['objective']}
Previous results: {context}

Current step: {current}

Execute this step and provide the result."""

    response = model.invoke(prompt)

    return {
        "step_results": [f"Step {state['current_step'] + 1}: {response.content}"],
        "current_step": state["current_step"] + 1
    }

# Node: Synthesize results
def synthesize(state: PlanState) -> PlanState:
    """Combine all step results into final answer."""
    prompt = f"""Synthesize these results into a final answer:

Objective: {state['objective']}

Completed steps:
{chr(10).join(state['step_results'])}

Provide a comprehensive final result."""

    response = model.invoke(prompt)
    return {"final_result": response.content}

# Routing: Check if more steps
def should_continue(state: PlanState) -> str:
    if state["current_step"] >= len(state["plan"]):
        return "synthesize"
    return "execute"

# Build graph
graph = StateGraph(PlanState)

graph.add_node("plan", create_plan)
graph.add_node("execute", execute_step)
graph.add_node("synthesize", synthesize)

graph.set_entry_point("plan")
graph.add_edge("plan", "execute")
graph.add_conditional_edges(
    "execute",
    should_continue,
    {"execute": "execute", "synthesize": "synthesize"}
)
graph.add_edge("synthesize", END)

plan_execute_agent = graph.compile()

# Run
result = plan_execute_agent.invoke({
    "objective": "Analyze the pros and cons of microservices architecture"
})

print("Final Result:")
print(result["final_result"])
```

---

## RAG Examples

### Example 1: Basic RAG Chain

Simple retrieval-augmented generation.

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. Load and split documents
loader = TextLoader("docs/knowledge_base.txt")
documents = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = splitter.split_documents(documents)

# 2. Create vector store
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

# 3. Create retriever
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)

# 4. RAG prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful assistant. Use the following context to answer the question.
If you don't know the answer based on the context, say "I don't have enough information to answer that."

Context:
{context}"""),
    ("human", "{question}")
])

model = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

# 5. RAG chain
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | model
    | parser
)

# Use
answer = rag_chain.invoke("What is the main topic of the document?")
print(answer)
```

### Example 2: RAG with Sources

Return answer with source citations.

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from pydantic import BaseModel, Field
from typing import List

# Output schema with sources
class AnswerWithSources(BaseModel):
    """Answer with source citations."""
    answer: str = Field(description="The answer to the question")
    sources: List[str] = Field(description="Sources used to generate the answer")
    confidence: float = Field(description="Confidence score 0-1")

# Setup (assuming vectorstore exists)
embeddings = OpenAIEmbeddings()
vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# Model with structured output
model = ChatOpenAI(model="gpt-4o-mini")
structured_model = model.with_structured_output(AnswerWithSources)

prompt = ChatPromptTemplate.from_messages([
    ("system", """Answer the question based on the context. Include:
1. A clear answer
2. Source citations (document names/sections)
3. Your confidence level (0-1)

Context:
{context}"""),
    ("human", "{question}")
])

def format_docs_with_sources(docs):
    formatted = []
    for i, doc in enumerate(docs, 1):
        source = doc.metadata.get("source", f"Document {i}")
        formatted.append(f"[{source}]: {doc.page_content}")
    return "\n\n".join(formatted)

# Chain that returns both answer and raw docs
rag_with_sources = (
    RunnableParallel(
        context=retriever | format_docs_with_sources,
        question=RunnablePassthrough(),
        docs=retriever
    )
    | RunnablePassthrough.assign(
        result=lambda x: (
            prompt | structured_model
        ).invoke({"context": x["context"], "question": x["question"]})
    )
)

# Use
result = rag_with_sources.invoke("What are the key features?")
print(f"Answer: {result['result'].answer}")
print(f"Sources: {result['result'].sources}")
print(f"Confidence: {result['result'].confidence}")
```

### Example 3: Conversational RAG

RAG with conversation history.

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# Setup
embeddings = OpenAIEmbeddings()
vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
model = ChatOpenAI(model="gpt-4o-mini")

# Contextualize question based on chat history
contextualize_prompt = ChatPromptTemplate.from_messages([
    ("system", """Given a chat history and the latest user question, formulate a standalone question
that can be understood without the chat history. Do NOT answer the question, just reformulate it
if needed, otherwise return it as is."""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}")
])

contextualize_chain = contextualize_prompt | model | StrOutputParser()

# Main RAG prompt
rag_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful assistant. Use the following context to answer questions.
If you don't know, say so.

Context:
{context}"""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}")
])

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# Contextualized retriever
def contextualized_question(input_dict):
    if input_dict.get("chat_history"):
        return contextualize_chain.invoke(input_dict)
    return input_dict["question"]

rag_chain = (
    RunnablePassthrough.assign(
        context=lambda x: format_docs(retriever.invoke(contextualized_question(x)))
    )
    | rag_prompt
    | model
    | StrOutputParser()
)

# Add message history
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

conversational_rag = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="chat_history"
)

# Use with session
config = {"configurable": {"session_id": "user-123"}}

# First question
answer1 = conversational_rag.invoke(
    {"question": "What is LangChain?"},
    config=config
)
print(f"A1: {answer1}")

# Follow-up (uses context from history)
answer2 = conversational_rag.invoke(
    {"question": "What are its main components?"},  # "its" refers to LangChain
    config=config
)
print(f"A2: {answer2}")
```

### Example 4: Hybrid Search RAG

Combine semantic and keyword search.

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load documents
loader = TextLoader("docs/knowledge_base.txt")
documents = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(documents)

# Semantic retriever (vector search)
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(chunks, embeddings)
semantic_retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# Keyword retriever (BM25)
bm25_retriever = BM25Retriever.from_documents(chunks)
bm25_retriever.k = 3

# Ensemble retriever (hybrid)
hybrid_retriever = EnsembleRetriever(
    retrievers=[semantic_retriever, bm25_retriever],
    weights=[0.6, 0.4]  # 60% semantic, 40% keyword
)

# RAG chain with hybrid retrieval
prompt = ChatPromptTemplate.from_messages([
    ("system", """Answer based on the context. Be specific and cite relevant parts.

Context:
{context}"""),
    ("human", "{question}")
])

model = ChatOpenAI(model="gpt-4o-mini")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

hybrid_rag = (
    {"context": hybrid_retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

# Use
answer = hybrid_rag.invoke("What are the API endpoints?")
print(answer)
```

---

## Tool Calling Examples

### Example 1: Basic Tool Definition

Different ways to define tools.

```python
from langchain_core.tools import tool, StructuredTool
from pydantic import BaseModel, Field
from typing import Optional

# Method 1: @tool decorator (simplest)
@tool
def search(query: str) -> str:
    """Search the web for information. Use for current events or facts."""
    return f"Search results for: {query}"

# Method 2: @tool with custom schema
class CalculatorInput(BaseModel):
    """Input for calculator."""
    expression: str = Field(description="Math expression to evaluate")
    precision: int = Field(default=2, description="Decimal places")

@tool(args_schema=CalculatorInput)
def calculate(expression: str, precision: int = 2) -> str:
    """Calculate a mathematical expression."""
    try:
        result = eval(expression)
        return f"{result:.{precision}f}"
    except Exception as e:
        return f"Error: {e}"

# Method 3: StructuredTool (most flexible)
class EmailInput(BaseModel):
    """Input for sending email."""
    to: str = Field(description="Recipient email address")
    subject: str = Field(description="Email subject")
    body: str = Field(description="Email body content")

def send_email_impl(to: str, subject: str, body: str) -> str:
    """Implementation of email sending."""
    # Actual implementation here
    return f"Email sent to {to} with subject: {subject}"

send_email = StructuredTool.from_function(
    func=send_email_impl,
    name="send_email",
    description="Send an email to someone",
    args_schema=EmailInput
)

# Method 4: Tool with error handling
from langchain_core.tools import ToolException

@tool(handle_tool_error=True)
def divide(a: float, b: float) -> str:
    """Divide a by b."""
    if b == 0:
        raise ToolException("Cannot divide by zero!")
    return str(a / b)

# Custom error handler
def custom_error_handler(error: ToolException) -> str:
    return f"Tool error: {error}. Please try with different inputs."

@tool(handle_tool_error=custom_error_handler)
def risky_operation(data: str) -> str:
    """A risky operation that might fail."""
    if not data:
        raise ToolException("Empty data provided")
    return f"Processed: {data}"
```

### Example 2: Tool Binding and Execution

Bind tools to models and handle calls.

```python
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

@tool
def get_weather(city: str) -> str:
    """Get current weather for a city."""
    weather_data = {
        "london": "Cloudy, 15C",
        "paris": "Sunny, 22C",
        "tokyo": "Rainy, 18C"
    }
    return weather_data.get(city.lower(), f"Weather data not available for {city}")

@tool
def get_time(timezone: str) -> str:
    """Get current time in a timezone like 'UTC', 'EST', 'PST'."""
    from datetime import datetime, timezone as tz
    # Simplified
    return f"Current time in {timezone}: {datetime.now().strftime('%H:%M')}"

# Bind tools to model
model = ChatOpenAI(model="gpt-4o-mini")
tools = [get_weather, get_time]
model_with_tools = model.bind_tools(tools)

# Tool execution loop
def execute_with_tools(query: str, max_iterations: int = 5) -> str:
    """Execute query with tool calling loop."""
    messages = [HumanMessage(content=query)]
    tool_map = {t.name: t for t in tools}

    for _ in range(max_iterations):
        response = model_with_tools.invoke(messages)
        messages.append(response)

        # Check for tool calls
        if not response.tool_calls:
            return response.content

        # Execute each tool call
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            if tool_name in tool_map:
                result = tool_map[tool_name].invoke(tool_args)
                messages.append(
                    ToolMessage(content=result, tool_call_id=tool_call["id"])
                )

    return "Max iterations reached"

# Use
result = execute_with_tools("What's the weather in Paris and what time is it in UTC?")
print(result)
```

### Example 3: Parallel Tool Execution

Execute multiple tools in parallel.

```python
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
import asyncio

@tool
async def fetch_stock(symbol: str) -> str:
    """Fetch stock price for a symbol."""
    await asyncio.sleep(0.1)  # Simulate API call
    prices = {"AAPL": 185.50, "GOOGL": 142.30, "MSFT": 378.90}
    return f"{symbol}: ${prices.get(symbol.upper(), 'N/A')}"

@tool
async def fetch_news(topic: str) -> str:
    """Fetch news for a topic."""
    await asyncio.sleep(0.1)  # Simulate API call
    return f"Latest news about {topic}: [Headlines here]"

async def parallel_tool_execution(queries: list[dict]) -> list[str]:
    """Execute multiple tool calls in parallel."""
    tasks = []
    for query in queries:
        tool_name = query["tool"]
        args = query["args"]

        if tool_name == "fetch_stock":
            tasks.append(fetch_stock.ainvoke(args))
        elif tool_name == "fetch_news":
            tasks.append(fetch_news.ainvoke(args))

    results = await asyncio.gather(*tasks)
    return results

# Use
async def main():
    queries = [
        {"tool": "fetch_stock", "args": {"symbol": "AAPL"}},
        {"tool": "fetch_stock", "args": {"symbol": "GOOGL"}},
        {"tool": "fetch_news", "args": {"topic": "tech"}}
    ]
    results = await parallel_tool_execution(queries)
    for r in results:
        print(r)

asyncio.run(main())
```

---

## Memory Examples

### Example 1: Conversation Buffer Memory

Store full conversation history.

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

# Define chain
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

model = ChatOpenAI(model="gpt-4o-mini")
chain = prompt | model | StrOutputParser()

# Memory store
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# Wrap with memory
chain_with_memory = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

# Use
config = {"configurable": {"session_id": "user-abc"}}

response1 = chain_with_memory.invoke(
    {"input": "My name is Alice and I work at Acme Corp"},
    config=config
)
print(f"Response 1: {response1}")

response2 = chain_with_memory.invoke(
    {"input": "What's my name and where do I work?"},
    config=config
)
print(f"Response 2: {response2}")

# View history
print("\nConversation history:")
for msg in store["user-abc"].messages:
    print(f"  {msg.type}: {msg.content[:50]}...")
```

### Example 2: Sliding Window Memory

Keep only recent messages.

```python
from langchain_core.messages import BaseMessage, trim_messages
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

# Token-based trimmer
trimmer = trim_messages(
    max_tokens=1000,
    strategy="last",  # Keep last messages
    token_counter=ChatOpenAI(model="gpt-4o-mini"),
    include_system=True  # Always keep system message
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder(variable_name="messages"),
])

model = ChatOpenAI(model="gpt-4o-mini")

# Chain with trimming
chain = trimmer | prompt | model | StrOutputParser()

# Use
messages = [
    {"role": "human", "content": "Hi, I'm learning Python"},
    {"role": "assistant", "content": "Great! Python is a wonderful language..."},
    {"role": "human", "content": "What's a list?"},
    {"role": "assistant", "content": "A list is a collection..."},
    # ... more messages
    {"role": "human", "content": "How do I use list comprehensions?"},
]

response = chain.invoke({"messages": messages})
print(response)
```

### Example 3: Summary Memory

Summarize old conversations to save tokens.

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage

class SummaryMemory:
    """Memory that summarizes old conversations."""

    def __init__(self, max_messages: int = 10):
        self.model = ChatOpenAI(model="gpt-4o-mini")
        self.max_messages = max_messages
        self.messages = []
        self.summary = ""

    def add_user_message(self, content: str):
        self.messages.append(HumanMessage(content=content))
        self._maybe_summarize()

    def add_ai_message(self, content: str):
        self.messages.append(AIMessage(content=content))
        self._maybe_summarize()

    def _maybe_summarize(self):
        if len(self.messages) > self.max_messages:
            # Summarize older half
            to_summarize = self.messages[:len(self.messages)//2]
            self.messages = self.messages[len(self.messages)//2:]

            # Create summary
            messages_text = "\n".join(
                f"{m.type}: {m.content}" for m in to_summarize
            )

            prompt = f"""Summarize this conversation, preserving key facts and context:

Previous summary: {self.summary}

New messages:
{messages_text}"""

            response = self.model.invoke(prompt)
            self.summary = response.content

    def get_context(self) -> str:
        """Get memory context for prompts."""
        context_parts = []
        if self.summary:
            context_parts.append(f"Conversation summary: {self.summary}")
        if self.messages:
            recent = "\n".join(
                f"{m.type}: {m.content}" for m in self.messages
            )
            context_parts.append(f"Recent messages:\n{recent}")
        return "\n\n".join(context_parts)

# Use
memory = SummaryMemory(max_messages=6)
memory.add_user_message("Hi, I'm John. I'm a software developer.")
memory.add_ai_message("Nice to meet you, John! What kind of software do you develop?")
memory.add_user_message("I mainly work on backend systems with Python.")
memory.add_ai_message("Python is excellent for backend development...")

# Get context for next prompt
context = memory.get_context()
print(context)
```

---

## Production Patterns

### Example 1: Cost-Aware Model Selection

Route to appropriate model based on complexity.

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

# Complexity classifier
class ComplexityAssessment(BaseModel):
    complexity: str = Field(description="low, medium, or high")
    reasoning: str = Field(description="Why this complexity level")

classifier_model = ChatOpenAI(model="gpt-4o-mini")
classifier = classifier_model.with_structured_output(ComplexityAssessment)

classifier_prompt = ChatPromptTemplate.from_template(
    """Assess the complexity of answering this query.
- low: Simple factual question, single concept
- medium: Requires some reasoning or multiple concepts
- high: Complex analysis, creative task, or multi-step reasoning

Query: {query}"""
)

# Model tiers
models = {
    "low": ChatOpenAI(model="gpt-4o-mini"),      # $0.15/$0.60 per 1M tokens
    "medium": ChatOpenAI(model="gpt-4o-mini"),   # Same, could be different
    "high": ChatOpenAI(model="gpt-4o")           # $2.50/$10 per 1M tokens
}

def cost_aware_chain(query: str) -> str:
    """Route to appropriate model based on complexity."""
    # Classify
    assessment = (classifier_prompt | classifier).invoke({"query": query})

    # Select model
    model = models[assessment.complexity]

    # Generate response
    response = model.invoke(query)

    return {
        "answer": response.content,
        "model_used": model.model_name,
        "complexity": assessment.complexity,
        "reasoning": assessment.reasoning
    }

# Use
result = cost_aware_chain("What is 2+2?")
print(f"Answer: {result['answer']}")
print(f"Model: {result['model_used']} (complexity: {result['complexity']})")

result = cost_aware_chain("Design a microservices architecture for an e-commerce platform")
print(f"Answer: {result['answer'][:100]}...")
print(f"Model: {result['model_used']} (complexity: {result['complexity']})")
```

### Example 2: Observability with Callbacks

Track execution metrics.

```python
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import time
from typing import Any, Dict, List

class MetricsCallbackHandler(BaseCallbackHandler):
    """Track execution metrics."""

    def __init__(self):
        self.metrics = {
            "llm_calls": 0,
            "total_tokens": 0,
            "latencies": [],
            "errors": []
        }
        self._start_time = None

    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs):
        self._start_time = time.time()
        self.metrics["llm_calls"] += 1

    def on_llm_end(self, response, **kwargs):
        if self._start_time:
            latency = time.time() - self._start_time
            self.metrics["latencies"].append(latency)

        if hasattr(response, 'llm_output') and response.llm_output:
            usage = response.llm_output.get('token_usage', {})
            self.metrics["total_tokens"] += usage.get('total_tokens', 0)

    def on_llm_error(self, error: Exception, **kwargs):
        self.metrics["errors"].append(str(error))

    def get_summary(self) -> dict:
        return {
            "llm_calls": self.metrics["llm_calls"],
            "total_tokens": self.metrics["total_tokens"],
            "avg_latency": sum(self.metrics["latencies"]) / len(self.metrics["latencies"]) if self.metrics["latencies"] else 0,
            "errors": len(self.metrics["errors"])
        }

# Use with chain
prompt = ChatPromptTemplate.from_template("Answer: {question}")
model = ChatOpenAI(model="gpt-4o-mini")
chain = prompt | model | StrOutputParser()

# Execute with metrics
metrics_handler = MetricsCallbackHandler()

result = chain.invoke(
    {"question": "What is Python?"},
    config={"callbacks": [metrics_handler]}
)

print(f"Answer: {result}")
print(f"Metrics: {metrics_handler.get_summary()}")
```

### Example 3: Caching for Cost Reduction

Cache repeated queries.

```python
from langchain_core.globals import set_llm_cache
from langchain_community.cache import InMemoryCache, SQLiteCache
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Option 1: In-memory cache (for development)
set_llm_cache(InMemoryCache())

# Option 2: SQLite cache (persists across restarts)
# set_llm_cache(SQLiteCache(database_path=".langchain_cache.db"))

# Setup chain
prompt = ChatPromptTemplate.from_template("Explain {concept} in simple terms.")
model = ChatOpenAI(model="gpt-4o-mini")
chain = prompt | model | StrOutputParser()

# First call - hits API
import time
start = time.time()
result1 = chain.invoke({"concept": "machine learning"})
print(f"First call: {time.time() - start:.2f}s")

# Second call - hits cache (instant)
start = time.time()
result2 = chain.invoke({"concept": "machine learning"})
print(f"Second call (cached): {time.time() - start:.2f}s")

# Results are identical
assert result1 == result2
```

### Example 4: Rate Limiting and Throttling

Control API request rates.

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableConfig
import asyncio
from asyncio import Semaphore

# Rate-limited batch processing
class RateLimitedProcessor:
    """Process items with rate limiting."""

    def __init__(self, max_concurrent: int = 5, delay_between: float = 0.1):
        self.semaphore = Semaphore(max_concurrent)
        self.delay = delay_between

        self.prompt = ChatPromptTemplate.from_template("Summarize: {text}")
        self.model = ChatOpenAI(model="gpt-4o-mini")
        self.chain = self.prompt | self.model | StrOutputParser()

    async def process_one(self, text: str) -> str:
        async with self.semaphore:
            result = await self.chain.ainvoke({"text": text})
            await asyncio.sleep(self.delay)  # Rate limiting delay
            return result

    async def process_batch(self, texts: list[str]) -> list[str]:
        tasks = [self.process_one(text) for text in texts]
        return await asyncio.gather(*tasks)

# Use
async def main():
    processor = RateLimitedProcessor(max_concurrent=3)

    texts = [
        "Article 1 content...",
        "Article 2 content...",
        "Article 3 content...",
        "Article 4 content...",
        "Article 5 content...",
    ]

    results = await processor.process_batch(texts)
    for i, result in enumerate(results):
        print(f"Summary {i+1}: {result[:50]}...")

asyncio.run(main())
```

---

*Examples v2.0 - LangChain 1.0+ / LangGraph 1.0+*
