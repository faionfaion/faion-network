# LangChain Methodology

> Orchestrate multi-step AI workflows using LangChain and LangGraph. Build production-ready chains, agents, and multi-agent systems.

## Overview

LangChain is the fastest way to build AI agents with standard tool calling architecture, provider-agnostic design, and middleware for customization. LangGraph is a lower-level framework for highly custom and controllable agents, designed for production-grade, long-running workflows.

**Current Versions:** LangChain 1.0+ / LangGraph 1.0+

## When to Use LangChain

| Use Case | Recommendation |
|----------|----------------|
| Simple chat with memory | LangChain chains |
| Standard tool calling agent | `create_react_agent()` |
| Complex control flow | LangGraph |
| Human-in-the-loop workflows | LangGraph |
| Multi-agent orchestration | LangGraph |
| Long-running tasks | LangGraph with checkpointing |
| Simple RAG pipeline | LangChain chains |
| Complex RAG with routing | LangGraph |

## When NOT to Use LangChain

| Scenario | Alternative |
|----------|-------------|
| Simple single LLM call | Direct API (OpenAI SDK, Anthropic SDK) |
| Document-centric RAG | LlamaIndex (better abstractions) |
| High-performance inference | vLLM, TGI, direct API |
| Browser-based agents | Direct tool use, no framework |
| Simple prompt templates | f-strings or Jinja2 |

## Key Concepts

### LCEL (LangChain Expression Language)

Modern declarative syntax for building chains using pipe operators.

```python
chain = prompt | model | parser
```

**Key Features:**
- Composable: Build complex chains from simple components
- Streamable: Native streaming support
- Async: First-class async support
- Traceable: Built-in observability with LangSmith
- Retry/Fallback: Built-in error handling

### LangGraph

Graph-based state machine framework for complex agent workflows.

**Key Features:**
- Durable State: Execution state persists automatically
- Checkpointing: Save and resume workflows
- Human-in-the-Loop: Pause for human review
- Time Travel: Debug by replaying states
- Subgraphs: Compose complex workflows

### Core Components

| Component | Purpose |
|-----------|---------|
| ChatPromptTemplate | Structure prompts with variables |
| ChatModel | LLM interface (OpenAI, Claude, etc.) |
| OutputParser | Parse LLM responses |
| Tool | External functionality for agents |
| Memory | Conversation history management |
| Retriever | Document retrieval for RAG |
| StateGraph | LangGraph workflow definition |

## Architecture Patterns

### Pattern Selection Guide

| Pattern | Use When | Complexity |
|---------|----------|------------|
| Sequential Chain | A then B then C | Low |
| Router Chain | Dynamic path selection | Medium |
| ReAct Agent | Tool use with reasoning | Medium |
| Plan-and-Execute | Multi-step tasks | High |
| Supervisor | Multiple specialized workers | High |
| Hierarchical | Teams of teams | Very High |

### Chain Patterns

```
Sequential:   prompt -> model -> parser
Router:       classifier -> [chain_a | chain_b | chain_c]
MapReduce:    [doc1, doc2, doc3] -> map -> reduce
Fallback:     primary -> fallback1 -> fallback2
```

### Agent Architectures

```
ReAct:           Thought -> Action -> Observation -> Repeat
Plan-Execute:    Plan -> Execute Step 1 -> ... -> Execute Step N
Supervisor:      Supervisor -> [Worker1 | Worker2] -> Synthesize
Debate:          Agent A -> Agent B -> Judge -> Repeat
```

## Installation

```bash
# Core (minimal)
pip install langchain-core

# Full LangChain
pip install langchain langchain-community

# LangGraph for agents
pip install langgraph

# Provider integrations
pip install langchain-openai langchain-anthropic langchain-google-genai

# Observability
pip install langsmith

# Vector stores
pip install langchain-chroma langchain-pinecone langchain-qdrant
```

## Environment Setup

```python
import os

# LLM API Keys
os.environ["OPENAI_API_KEY"] = "sk-..."
os.environ["ANTHROPIC_API_KEY"] = "sk-ant-..."

# LangSmith Tracing (recommended for production)
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "ls__..."
os.environ["LANGCHAIN_PROJECT"] = "my-project"
```

## LLM Tips for LangChain Development

### Effective Prompting for Chains

1. **Be Specific About Output Format**
   ```
   When building a chain, explicitly tell the LLM the expected output format.
   Use structured output (with_structured_output) for reliable parsing.
   ```

2. **Include Examples in Prompts**
   ```
   Few-shot examples improve consistency.
   Use SemanticSimilarityExampleSelector for dynamic selection.
   ```

3. **System Messages Matter**
   ```
   Define clear roles and constraints in system messages.
   Include output format instructions in system message.
   ```

### Debugging with LLMs

1. **Enable LangSmith Tracing**
   - Visualize chain execution
   - Identify bottlenecks
   - Debug unexpected outputs

2. **Use Verbose Mode**
   ```python
   chain.invoke({"input": "test"}, config={"callbacks": [StdOutCallbackHandler()]})
   ```

3. **Test Components Individually**
   ```python
   # Test prompt
   print(prompt.format(input="test"))

   # Test model
   response = model.invoke(prompt.format(input="test"))

   # Test parser
   parsed = parser.parse(response.content)
   ```

### Cost Optimization

| Strategy | Implementation |
|----------|----------------|
| Model Tiering | Use gpt-4o-mini for simple, gpt-4o for complex |
| Caching | Enable LangChain cache for repeated queries |
| Batching | Use `batch()` instead of multiple `invoke()` |
| Context Pruning | Summarize long conversations |
| Token Counting | Monitor with callbacks |

## Quick Reference

### Common Imports

```python
# Core
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables import RunnableParallel, RunnableLambda, RunnableBranch
from langchain_core.tools import tool

# Models
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

# LangGraph
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
```

### Chain Building

```python
# Basic chain
chain = prompt | model | StrOutputParser()

# With structured output
chain = prompt | model.with_structured_output(MySchema)

# With retry
chain = (prompt | model | parser).with_retry(stop_after_attempt=3)

# With fallback
chain = primary_chain.with_fallbacks([fallback_chain])
```

### Agent Creation

```python
# Simple ReAct agent
agent = create_react_agent(model, tools)

# With checkpointing
agent = create_react_agent(model, tools, checkpointer=MemorySaver())

# Custom LangGraph agent
graph = StateGraph(State)
graph.add_node("agent", agent_node)
graph.add_node("tools", tool_node)
graph.add_conditional_edges("agent", should_continue)
agent = graph.compile()
```

## Files in This Folder

| File | Purpose | Size Target |
|------|---------|-------------|
| [README.md](README.md) | Overview, concepts, when to use | 10-15 KB |
| [checklist.md](checklist.md) | Setup, design, deployment checklists | 8-12 KB |
| [examples.md](examples.md) | LCEL, LangGraph, RAG, tool examples | 20-35 KB |
| [templates.md](templates.md) | Reusable chain/agent templates | 15-25 KB |
| [llm-prompts.md](llm-prompts.md) | Prompts for LLM-assisted development | 10-15 KB |

## External Resources

### Official Documentation

- [LangChain Python Docs](https://python.langchain.com/docs/)
- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [LangSmith Docs](https://docs.smith.langchain.com/)
- [LangChain Hub](https://smith.langchain.com/hub)

### Tutorials

- [LangChain Quickstart](https://python.langchain.com/docs/tutorials/llm_chain/)
- [LangGraph Quickstart](https://langchain-ai.github.io/langgraph/tutorials/introduction/)
- [Building Agents](https://python.langchain.com/docs/tutorials/agents/)
- [RAG Tutorial](https://python.langchain.com/docs/tutorials/rag/)

### Reference

- [LCEL Primitives](https://python.langchain.com/docs/how_to/#langchain-expression-language-lcel)
- [LangGraph Concepts](https://langchain-ai.github.io/langgraph/concepts/)
- [Tool Calling](https://python.langchain.com/docs/how_to/tool_calling/)

## Migration Notes

### From Legacy LangChain

If using old patterns:

| Old Pattern | New Pattern |
|-------------|-------------|
| LLMChain | prompt \| model \| parser |
| AgentExecutor | LangGraph agent |
| ConversationChain | RunnableWithMessageHistory |
| SequentialChain | LCEL pipe chain |

### From Other Frameworks

| From | Key Differences |
|------|-----------------|
| LlamaIndex | LangChain focuses on chains/agents, LlamaIndex on RAG |
| AutoGen | LangChain offers more control, AutoGen more autonomous |
| Haystack | Similar concepts, different API design |

## Version Compatibility

| Package | Minimum Version | Recommended |
|---------|-----------------|-------------|
| langchain | 0.3.0 | 1.0+ |
| langchain-core | 0.3.0 | 1.0+ |
| langgraph | 0.2.0 | 1.0+ |
| Python | 3.9 | 3.11+ |

---

*LangChain Methodology v2.0*
*LangChain 1.0+ / LangGraph 1.0+*
*Part of faion-ml-engineer skill*

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Chain design | sonnet | Architecture pattern |
| Agent implementation | sonnet | Integration pattern |
| LangChain debugging | sonnet | Troubleshooting |
