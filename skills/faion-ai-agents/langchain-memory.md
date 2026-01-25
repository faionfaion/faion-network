---
name: faion-langchain-memory
user-invocable: false
description: "LangChain memory: conversation buffer, summary, vector, entity, LangGraph workflows"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(python:*), Bash(pip:*)
---

# LangChain Memory & Workflows

**Communication: User's language. Docs/code: English.**

## Purpose

Memory management in conversational AI and LangGraph workflow orchestration.

## When to Use

- Building conversational AI with memory
- Implementing stateful workflows
- Creating human-in-the-loop systems
- Managing conversation history
- Building complex state machines

---

# Section 1: Memory Types

## Type 1: Conversation Buffer Memory

Store full conversation history.

```python
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# Create store
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# Wrap chain with memory
chain_with_memory = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

# Use with session
result = chain_with_memory.invoke(
    {"input": "My name is Alice"},
    config={"configurable": {"session_id": "user-123"}}
)

# Later in same session
result = chain_with_memory.invoke(
    {"input": "What's my name?"},
    config={"configurable": {"session_id": "user-123"}}
)
# Returns: "Your name is Alice"
```

## Type 2: Conversation Summary Memory

Summarize old messages to save tokens.

```python
from langchain.memory import ConversationSummaryMemory
from langchain_openai import ChatOpenAI

summary_llm = ChatOpenAI(model="gpt-4o-mini")

class SummaryMemory:
    def __init__(self, llm, max_messages: int = 10):
        self.llm = llm
        self.max_messages = max_messages
        self.messages = []
        self.summary = ""

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

        if len(self.messages) > self.max_messages:
            self._summarize()

    def _summarize(self):
        # Summarize oldest half
        to_summarize = self.messages[:len(self.messages)//2]
        remaining = self.messages[len(self.messages)//2:]

        messages_text = "\n".join(
            f"{m['role']}: {m['content']}" for m in to_summarize
        )

        prompt = f"""Summarize this conversation:
        Previous summary: {self.summary}

        New messages:
        {messages_text}
        """

        response = self.llm.invoke(prompt)
        self.summary = response.content
        self.messages = remaining

    def get_context(self) -> str:
        recent = "\n".join(
            f"{m['role']}: {m['content']}" for m in self.messages
        )
        return f"Summary: {self.summary}\n\nRecent:\n{recent}"
```

## Type 3: Vector Store Memory

Retrieve relevant past interactions via semantic search.

```python
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

class VectorMemory:
    def __init__(self, collection_name: str = "memory"):
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = Chroma(
            collection_name=collection_name,
            embedding_function=self.embeddings
        )

    def add_interaction(self, human: str, assistant: str, metadata: dict = None):
        """Store a conversation turn."""
        text = f"Human: {human}\nAssistant: {assistant}"
        self.vectorstore.add_texts(
            texts=[text],
            metadatas=[metadata or {}]
        )

    def get_relevant(self, query: str, k: int = 3) -> list[str]:
        """Retrieve relevant past interactions."""
        docs = self.vectorstore.similarity_search(query, k=k)
        return [doc.page_content for doc in docs]

    def get_context(self, current_query: str) -> str:
        """Get memory context for prompt."""
        relevant = self.get_relevant(current_query)
        if not relevant:
            return ""
        return "Relevant past interactions:\n" + "\n---\n".join(relevant)

# Usage
memory = VectorMemory()
memory.add_interaction(
    "What's the capital of France?",
    "The capital of France is Paris."
)

# Later
context = memory.get_context("Tell me about French cities")
# Returns relevant past interaction about Paris
```

## Type 4: Entity Memory

Track entities mentioned in conversation.

```python
from langchain_openai import ChatOpenAI

class EntityMemory:
    def __init__(self, llm):
        self.llm = llm
        self.entities = {}

    def extract_entities(self, text: str) -> dict:
        """Extract entities from text."""
        prompt = f"""Extract named entities from this text.
        Return as JSON: {{"entity_name": "entity_info"}}

        Text: {text}
        """
        response = self.llm.invoke(prompt)
        return parse_json(response.content)

    def update(self, text: str):
        """Update entity store with new information."""
        new_entities = self.extract_entities(text)
        for name, info in new_entities.items():
            if name in self.entities:
                # Merge information
                self.entities[name] = self._merge(self.entities[name], info)
            else:
                self.entities[name] = info

    def get_context(self, entities: list[str]) -> str:
        """Get context for specific entities."""
        relevant = {k: v for k, v in self.entities.items() if k in entities}
        return f"Known entities: {relevant}"
```

---

# Section 2: Memory Comparison

## Memory Types Comparison

| Type | Token Cost | Best For | Pros | Cons |
|------|-----------|----------|------|------|
| **Buffer** | High | Short conversations | Simple, exact recall | Token limit issues |
| **Summary** | Medium | Long conversations | Scalable | May lose details |
| **Vector** | Low per query | Large history | Semantic search | Setup complexity |
| **Entity** | Medium | Entity-focused | Structured info | Requires extraction |

## Selection Guide

```python
def select_memory_type(conversation_length: int, focus: str) -> str:
    """Select appropriate memory type."""

    # Short conversation
    if conversation_length < 10:
        return "buffer"

    # Entity-focused
    if focus == "entities":
        return "entity"

    # Long conversation, semantic search needed
    if conversation_length > 50:
        return "vector"

    # Long conversation, sequential
    return "summary"
```

---

# Section 3: LangGraph Workflows

## State Definition

```python
from typing import TypedDict, Annotated, List
import operator

class WorkflowState(TypedDict):
    # Simple fields
    input: str
    output: str

    # Accumulating field (appends instead of replaces)
    messages: Annotated[List[str], operator.add]

    # Optional field
    error: str | None

# Usage: {"messages": ["new"]} adds to existing messages
```

## Node Functions

```python
from langgraph.graph import StateGraph, END

def process_node(state: WorkflowState) -> WorkflowState:
    """Process the input."""
    result = f"Processed: {state['input']}"
    return {
        "output": result,
        "messages": [f"Processed input: {state['input']}"]
    }

def validate_node(state: WorkflowState) -> WorkflowState:
    """Validate the output."""
    if "error" in state["output"].lower():
        return {"error": "Validation failed"}
    return {"messages": ["Validation passed"]}

def finalize_node(state: WorkflowState) -> WorkflowState:
    """Finalize the workflow."""
    return {"messages": ["Workflow complete"]}
```

## Conditional Edges

```python
def should_continue(state: WorkflowState) -> str:
    """Determine next node based on state."""
    if state.get("error"):
        return "error_handler"
    if len(state.get("messages", [])) > 10:
        return END
    return "process"

# Build graph
graph = StateGraph(WorkflowState)

graph.add_node("process", process_node)
graph.add_node("validate", validate_node)
graph.add_node("finalize", finalize_node)
graph.add_node("error_handler", error_handler)

graph.set_entry_point("process")
graph.add_edge("process", "validate")
graph.add_conditional_edges(
    "validate",
    should_continue,
    {
        "process": "process",
        "error_handler": "error_handler",
        END: END
    }
)
graph.add_edge("finalize", END)
graph.add_edge("error_handler", END)

workflow = graph.compile()
```

## Human-in-the-Loop

```python
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, END

# Create checkpointer for persistence
memory = MemorySaver()

def get_approval(state: WorkflowState) -> WorkflowState:
    """Node that requires human approval."""
    return {"messages": ["Waiting for approval..."]}

def execute_action(state: WorkflowState) -> WorkflowState:
    """Execute after approval."""
    return {"output": "Action executed", "messages": ["Done"]}

# Build graph with interrupt
graph = StateGraph(WorkflowState)
graph.add_node("get_approval", get_approval)
graph.add_node("execute", execute_action)

graph.set_entry_point("get_approval")
graph.add_edge("get_approval", "execute")
graph.add_edge("execute", END)

# Compile with interrupt before execute
workflow = graph.compile(
    checkpointer=memory,
    interrupt_before=["execute"]
)

# First run - stops at interrupt
config = {"configurable": {"thread_id": "1"}}
result = workflow.invoke({"input": "Do something"}, config)

# Resume after approval
result = workflow.invoke(None, config)  # Continues from checkpoint
```

## Subgraphs

```python
from langgraph.graph import StateGraph

# Define subgraph
def create_research_subgraph():
    graph = StateGraph(WorkflowState)
    graph.add_node("search", search_node)
    graph.add_node("analyze", analyze_node)
    graph.set_entry_point("search")
    graph.add_edge("search", "analyze")
    return graph.compile()

research_subgraph = create_research_subgraph()

# Use in main graph
main = StateGraph(WorkflowState)
main.add_node("research", research_subgraph)
main.add_node("synthesize", synthesize_node)

main.set_entry_point("research")
main.add_edge("research", "synthesize")
main.add_edge("synthesize", END)

main_workflow = main.compile()
```

## Exception Handling in Graphs

```python
from langgraph.graph import StateGraph, END

class SafeState(TypedDict):
    input: str
    output: str
    error: str | None

def safe_node(state: SafeState) -> SafeState:
    try:
        result = risky_operation(state["input"])
        return {"output": result}
    except Exception as e:
        return {"error": str(e)}

def error_handler(state: SafeState) -> SafeState:
    """Handle errors gracefully."""
    return {"output": f"Error occurred: {state['error']}"}

def route_on_error(state: SafeState) -> str:
    if state.get("error"):
        return "error_handler"
    return "next_node"

graph = StateGraph(SafeState)
graph.add_node("risky", safe_node)
graph.add_node("error_handler", error_handler)
graph.add_node("next_node", next_node)

graph.add_conditional_edges("risky", route_on_error)
```

## LangGraph Streaming

```python
from langgraph.graph import StateGraph

# Stream node outputs
for state in workflow.stream({"input": "Hello"}):
    print(f"Node: {list(state.keys())[0]}")
    print(f"Output: {list(state.values())[0]}")

# Stream with mode
for chunk in workflow.stream(
    {"input": "Hello"},
    stream_mode="values"  # or "updates", "debug"
):
    print(chunk)
```

---

# Quick Reference

## Memory Selection

| Conversation Type | Recommended Memory |
|-------------------|-------------------|
| < 10 messages | Buffer |
| 10-50 messages | Summary |
| > 50 messages | Vector |
| Entity tracking | Entity |
| Complex context | Vector + Entity |

## LangGraph Patterns

| Pattern | Use Case |
|---------|----------|
| Linear workflow | Sequential processing |
| Conditional routing | Dynamic decisions |
| Human-in-loop | Approval workflows |
| Subgraphs | Modular composition |
| Error handling | Fault tolerance |

---

*faion-langchain-memory v1.0*
*LangChain 0.3.x / LangGraph 0.2.x*
*Covers: memory types, conversation management, LangGraph workflows, state machines*
