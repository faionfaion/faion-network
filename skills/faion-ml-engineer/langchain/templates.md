# LangChain Templates

Production-ready templates for chains, agents, callbacks, and configuration.

---

## Table of Contents

1. [Chain Templates](#chain-templates)
2. [Agent Templates](#agent-templates)
3. [Callback Handler Templates](#callback-handler-templates)
4. [Configuration Templates](#configuration-templates)
5. [Testing Templates](#testing-templates)

---

## Chain Templates

### Template 1: Standard Chain with Error Handling

```python
"""
Standard LangChain chain template with:
- Structured output
- Retry logic
- Fallback models
- Observability
"""
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from pydantic import BaseModel, Field
from typing import Optional
import os

# Configuration
class ChainConfig:
    """Chain configuration."""
    PRIMARY_MODEL = os.getenv("PRIMARY_MODEL", "gpt-4o-mini")
    FALLBACK_MODEL = os.getenv("FALLBACK_MODEL", "claude-3-haiku-20240307")
    TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0"))
    MAX_RETRIES = int(os.getenv("LLM_MAX_RETRIES", "3"))


# Output schema (customize for your use case)
class ChainOutput(BaseModel):
    """Structured output from the chain."""
    result: str = Field(description="The main result")
    confidence: float = Field(default=1.0, description="Confidence score 0-1")
    metadata: Optional[dict] = Field(default=None, description="Additional metadata")


def create_chain(
    system_prompt: str,
    use_structured_output: bool = False,
    output_schema: type[BaseModel] = None
):
    """
    Create a production-ready chain.

    Args:
        system_prompt: System message for the LLM
        use_structured_output: Whether to parse output as Pydantic model
        output_schema: Pydantic model for structured output

    Returns:
        Configured chain ready for invocation
    """
    # Prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}")
    ])

    # Primary model
    primary_model = ChatOpenAI(
        model=ChainConfig.PRIMARY_MODEL,
        temperature=ChainConfig.TEMPERATURE
    )

    # Fallback model
    fallback_model = ChatAnthropic(
        model=ChainConfig.FALLBACK_MODEL,
        temperature=ChainConfig.TEMPERATURE
    )

    # Output handling
    if use_structured_output and output_schema:
        primary = primary_model.with_structured_output(output_schema)
        fallback = fallback_model.with_structured_output(output_schema)
    else:
        primary = primary_model | StrOutputParser()
        fallback = fallback_model | StrOutputParser()

    # Chain with retry and fallback
    chain = (
        prompt
        | primary.with_retry(stop_after_attempt=ChainConfig.MAX_RETRIES)
    ).with_fallbacks([prompt | fallback])

    return chain


# Usage example
if __name__ == "__main__":
    # Simple string output
    simple_chain = create_chain(
        system_prompt="You are a helpful assistant. Be concise."
    )
    result = simple_chain.invoke({"input": "What is Python?"})
    print(f"Simple: {result}")

    # Structured output
    structured_chain = create_chain(
        system_prompt="Analyze the query and provide a detailed response.",
        use_structured_output=True,
        output_schema=ChainOutput
    )
    result = structured_chain.invoke({"input": "Explain machine learning"})
    print(f"Structured: {result}")
```

### Template 2: RAG Chain

```python
"""
RAG (Retrieval Augmented Generation) chain template.
"""
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, Optional
from pydantic import BaseModel, Field


class RAGConfig:
    """RAG configuration."""
    EMBEDDING_MODEL = "text-embedding-3-small"
    LLM_MODEL = "gpt-4o-mini"
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 50
    RETRIEVAL_K = 4
    PERSIST_DIR = "./vectorstore"


class RAGResponse(BaseModel):
    """RAG response with sources."""
    answer: str = Field(description="The answer to the question")
    sources: List[str] = Field(description="Source documents used")
    confidence: float = Field(description="Confidence in answer")


class RAGChain:
    """Production RAG chain."""

    def __init__(
        self,
        persist_directory: str = RAGConfig.PERSIST_DIR,
        collection_name: str = "default"
    ):
        self.embeddings = OpenAIEmbeddings(model=RAGConfig.EMBEDDING_MODEL)
        self.llm = ChatOpenAI(model=RAGConfig.LLM_MODEL, temperature=0)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=RAGConfig.CHUNK_SIZE,
            chunk_overlap=RAGConfig.CHUNK_OVERLAP
        )

        # Initialize or load vectorstore
        self.vectorstore = Chroma(
            collection_name=collection_name,
            embedding_function=self.embeddings,
            persist_directory=persist_directory
        )

        self.retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": RAGConfig.RETRIEVAL_K}
        )

        # Build chain
        self._build_chain()

    def _build_chain(self):
        """Build the RAG chain."""
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful assistant. Answer questions based on the provided context.
If the context doesn't contain enough information, say so.
Always cite your sources when possible.

Context:
{context}"""),
            ("human", "{question}")
        ])

        def format_docs(docs):
            return "\n\n".join(
                f"[{doc.metadata.get('source', 'Unknown')}]: {doc.page_content}"
                for doc in docs
            )

        self.chain = (
            RunnableParallel(
                context=self.retriever | format_docs,
                question=RunnablePassthrough(),
                docs=self.retriever
            )
            | RunnablePassthrough.assign(
                answer=lambda x: (self.prompt | self.llm | StrOutputParser()).invoke({
                    "context": x["context"],
                    "question": x["question"]
                })
            )
        )

    def add_documents(self, texts: List[str], metadatas: List[dict] = None):
        """Add documents to the vectorstore."""
        from langchain_core.documents import Document

        docs = []
        for i, text in enumerate(texts):
            metadata = metadatas[i] if metadatas else {"source": f"doc_{i}"}
            # Split into chunks
            chunks = self.text_splitter.split_text(text)
            for chunk in chunks:
                docs.append(Document(page_content=chunk, metadata=metadata))

        self.vectorstore.add_documents(docs)

    def query(self, question: str) -> dict:
        """Query the RAG chain."""
        result = self.chain.invoke(question)
        return {
            "answer": result["answer"],
            "sources": [doc.metadata.get("source", "Unknown") for doc in result["docs"]],
            "documents": result["docs"]
        }


# Usage example
if __name__ == "__main__":
    rag = RAGChain(collection_name="my_docs")

    # Add documents
    rag.add_documents(
        texts=["Document 1 content...", "Document 2 content..."],
        metadatas=[{"source": "doc1.pdf"}, {"source": "doc2.pdf"}]
    )

    # Query
    result = rag.query("What is the main topic?")
    print(f"Answer: {result['answer']}")
    print(f"Sources: {result['sources']}")
```

### Template 3: Conversational Chain with Memory

```python
"""
Conversational chain with message history.
"""
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from typing import Dict, Optional
import redis
import json


class ConversationConfig:
    """Conversation configuration."""
    MODEL = "gpt-4o-mini"
    MAX_HISTORY_LENGTH = 20
    REDIS_URL = "redis://localhost:6379"


# In-memory store (for development)
class InMemoryHistoryStore:
    """In-memory conversation history store."""

    def __init__(self):
        self._store: Dict[str, InMemoryChatMessageHistory] = {}

    def get_history(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in self._store:
            self._store[session_id] = InMemoryChatMessageHistory()
        return self._store[session_id]

    def clear_history(self, session_id: str):
        if session_id in self._store:
            del self._store[session_id]


# Redis store (for production)
class RedisHistoryStore:
    """Redis-backed conversation history store."""

    def __init__(self, redis_url: str = ConversationConfig.REDIS_URL):
        self._redis = redis.from_url(redis_url)

    def get_history(self, session_id: str) -> BaseChatMessageHistory:
        from langchain_community.chat_message_histories import RedisChatMessageHistory
        return RedisChatMessageHistory(
            session_id=session_id,
            url=ConversationConfig.REDIS_URL
        )

    def clear_history(self, session_id: str):
        self._redis.delete(f"message_store:{session_id}")


class ConversationalChain:
    """Conversational chain with memory."""

    def __init__(
        self,
        system_prompt: str = "You are a helpful assistant.",
        history_store: Optional[InMemoryHistoryStore] = None
    ):
        self.history_store = history_store or InMemoryHistoryStore()

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])

        self.model = ChatOpenAI(
            model=ConversationConfig.MODEL,
            temperature=0.7
        )

        self.chain = self.prompt | self.model | StrOutputParser()

        self.chain_with_history = RunnableWithMessageHistory(
            self.chain,
            self.history_store.get_history,
            input_messages_key="input",
            history_messages_key="history"
        )

    def chat(self, message: str, session_id: str) -> str:
        """Send a message and get a response."""
        config = {"configurable": {"session_id": session_id}}
        return self.chain_with_history.invoke({"input": message}, config=config)

    def clear_session(self, session_id: str):
        """Clear conversation history for a session."""
        self.history_store.clear_history(session_id)


# Usage example
if __name__ == "__main__":
    conversation = ConversationalChain(
        system_prompt="You are a friendly assistant helping with Python questions."
    )

    session = "user-123"

    # Multi-turn conversation
    print(conversation.chat("Hi! I'm learning Python.", session))
    print(conversation.chat("What's a good first project?", session))
    print(conversation.chat("How long would that take to build?", session))

    # Clear and start fresh
    conversation.clear_session(session)
```

### Template 4: Router Chain

```python
"""
Router chain that directs queries to specialized handlers.
"""
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableBranch
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import Callable, Dict, Optional
from enum import Enum


class RouteCategory(str, Enum):
    """Query categories for routing."""
    TECHNICAL = "technical"
    GENERAL = "general"
    CREATIVE = "creative"
    CODING = "coding"


class RouteDecision(BaseModel):
    """Router decision."""
    category: RouteCategory = Field(description="The category of the query")
    reasoning: str = Field(description="Why this category was chosen")


class RouterChain:
    """Chain that routes queries to specialized handlers."""

    def __init__(self):
        self.classifier = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        self.handlers: Dict[RouteCategory, Callable] = {}

        # Build classifier chain
        classifier_prompt = ChatPromptTemplate.from_messages([
            ("system", """Classify the user query into one of these categories:
- technical: Technical questions about systems, architecture, etc.
- general: General knowledge questions
- creative: Creative writing, brainstorming, ideas
- coding: Code-related questions, debugging, implementation

Respond with the category and your reasoning."""),
            ("human", "{query}")
        ])

        self.classifier_chain = (
            classifier_prompt
            | self.classifier.with_structured_output(RouteDecision)
        )

        # Default handlers
        self._setup_default_handlers()

    def _setup_default_handlers(self):
        """Set up default category handlers."""
        model = ChatOpenAI(model="gpt-4o-mini")
        parser = StrOutputParser()

        # Technical handler
        technical_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a technical expert. Provide detailed, accurate technical explanations."),
            ("human", "{query}")
        ])
        self.handlers[RouteCategory.TECHNICAL] = technical_prompt | model | parser

        # General handler
        general_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a knowledgeable assistant. Provide clear, helpful answers."),
            ("human", "{query}")
        ])
        self.handlers[RouteCategory.GENERAL] = general_prompt | model | parser

        # Creative handler
        creative_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a creative assistant. Be imaginative and inspiring."),
            ("human", "{query}")
        ])
        self.handlers[RouteCategory.CREATIVE] = creative_prompt | model | parser

        # Coding handler
        coding_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert programmer. Provide clean, well-documented code with explanations."),
            ("human", "{query}")
        ])
        self.handlers[RouteCategory.CODING] = coding_prompt | model | parser

    def register_handler(self, category: RouteCategory, handler: Callable):
        """Register a custom handler for a category."""
        self.handlers[category] = handler

    def invoke(self, query: str) -> dict:
        """Route and process the query."""
        # Classify
        decision = self.classifier_chain.invoke({"query": query})

        # Route to handler
        handler = self.handlers.get(decision.category, self.handlers[RouteCategory.GENERAL])
        response = handler.invoke({"query": query})

        return {
            "response": response,
            "category": decision.category.value,
            "reasoning": decision.reasoning
        }


# Usage example
if __name__ == "__main__":
    router = RouterChain()

    queries = [
        "What is a microservices architecture?",
        "Write a Python function to sort a list",
        "Give me ideas for a birthday party theme",
        "Who was Napoleon?"
    ]

    for query in queries:
        result = router.invoke(query)
        print(f"Query: {query}")
        print(f"Category: {result['category']}")
        print(f"Response: {result['response'][:100]}...")
        print()
```

---

## Agent Templates

### Template 1: ReAct Agent with Custom Tools

```python
"""
Production ReAct agent with custom tools and error handling.
"""
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool, ToolException
from pydantic import BaseModel, Field
from typing import Optional, List
import httpx
import os


class AgentConfig:
    """Agent configuration."""
    MODEL = os.getenv("AGENT_MODEL", "gpt-4o-mini")
    MAX_ITERATIONS = int(os.getenv("AGENT_MAX_ITERATIONS", "10"))


# Tool definitions
class SearchInput(BaseModel):
    """Search input schema."""
    query: str = Field(description="Search query")
    max_results: int = Field(default=5, description="Maximum results to return")


@tool(args_schema=SearchInput)
def search_web(query: str, max_results: int = 5) -> str:
    """Search the web for current information.

    Use this tool when you need to find current information,
    facts, or data that you don't know.
    """
    try:
        # Replace with actual search implementation
        # e.g., Tavily, SerpAPI, etc.
        return f"Search results for '{query}': [Implement actual search]"
    except Exception as e:
        raise ToolException(f"Search failed: {e}")


@tool
def calculate(expression: str) -> str:
    """Calculate a mathematical expression.

    Use this for any math calculations. Use Python syntax.
    Examples: "2 + 2", "10 * 5", "100 / 4", "2 ** 8"
    """
    try:
        # Safe evaluation
        allowed_chars = set("0123456789+-*/().% ")
        if not all(c in allowed_chars for c in expression):
            return "Error: Only basic math operations allowed"
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Calculation error: {e}"


@tool
def get_weather(city: str, units: str = "celsius") -> str:
    """Get current weather for a city.

    Args:
        city: City name (e.g., "London", "New York")
        units: Temperature units ("celsius" or "fahrenheit")
    """
    try:
        # Replace with actual weather API
        return f"Weather in {city}: Sunny, 22{units[0].upper()}"
    except Exception as e:
        raise ToolException(f"Weather API error: {e}")


class ProductionAgent:
    """Production-ready ReAct agent."""

    def __init__(
        self,
        tools: List = None,
        system_prompt: str = None,
        enable_memory: bool = True
    ):
        self.model = ChatOpenAI(
            model=AgentConfig.MODEL,
            temperature=0
        )

        self.tools = tools or [search_web, calculate, get_weather]

        self.system_prompt = system_prompt or """You are a helpful assistant with access to tools.

Guidelines:
1. Think step-by-step before acting
2. Use tools when needed, but don't overuse them
3. If a tool fails, try an alternative approach
4. Be concise in your final answers"""

        # Checkpointer for memory
        self.checkpointer = MemorySaver() if enable_memory else None

        # Create agent
        self.agent = create_react_agent(
            self.model,
            self.tools,
            state_modifier=self.system_prompt,
            checkpointer=self.checkpointer
        )

    def invoke(
        self,
        message: str,
        session_id: str = "default",
        max_iterations: int = None
    ) -> dict:
        """Invoke the agent with a message."""
        config = {
            "configurable": {"thread_id": session_id},
            "recursion_limit": max_iterations or AgentConfig.MAX_ITERATIONS
        }

        result = self.agent.invoke(
            {"messages": [("human", message)]},
            config=config
        )

        # Extract final response
        final_message = result["messages"][-1]

        return {
            "response": final_message.content,
            "messages": result["messages"],
            "tool_calls": [
                msg for msg in result["messages"]
                if hasattr(msg, 'tool_calls') and msg.tool_calls
            ]
        }

    def stream(self, message: str, session_id: str = "default"):
        """Stream agent execution."""
        config = {"configurable": {"thread_id": session_id}}

        for event in self.agent.stream(
            {"messages": [("human", message)]},
            config=config,
            stream_mode="values"
        ):
            yield event


# Usage example
if __name__ == "__main__":
    agent = ProductionAgent()

    # Single query
    result = agent.invoke(
        "What's the weather in Paris and calculate 15% of $120",
        session_id="user-123"
    )
    print(f"Response: {result['response']}")

    # Follow-up (uses memory)
    result = agent.invoke(
        "What about London?",
        session_id="user-123"
    )
    print(f"Follow-up: {result['response']}")
```

### Template 2: Custom LangGraph Agent

```python
"""
Custom LangGraph agent with full control over execution flow.
"""
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage
from langchain_core.tools import tool
from typing import TypedDict, Annotated, Sequence, Literal
import operator


# State definition
class AgentState(TypedDict):
    """Agent state."""
    messages: Annotated[Sequence, operator.add]
    iteration: int
    max_iterations: int


# Tools
@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"


@tool
def analyze(data: str) -> str:
    """Analyze data and provide insights."""
    return f"Analysis of: {data}"


TOOLS = [search, analyze]
TOOL_MAP = {t.name: t for t in TOOLS}


class CustomAgent:
    """Custom LangGraph agent."""

    def __init__(self, system_prompt: str = None, max_iterations: int = 10):
        self.model = ChatOpenAI(model="gpt-4o-mini").bind_tools(TOOLS)
        self.max_iterations = max_iterations

        self.system_prompt = system_prompt or "You are a helpful assistant with tools."

        self._build_graph()

    def _build_graph(self):
        """Build the agent graph."""
        graph = StateGraph(AgentState)

        # Add nodes
        graph.add_node("agent", self._agent_node)
        graph.add_node("tools", self._tool_node)

        # Set entry point
        graph.set_entry_point("agent")

        # Add edges
        graph.add_conditional_edges(
            "agent",
            self._should_continue,
            {"continue": "tools", "end": END}
        )
        graph.add_edge("tools", "agent")

        # Compile with checkpointer
        self.graph = graph.compile(checkpointer=MemorySaver())

    def _agent_node(self, state: AgentState) -> dict:
        """Agent decision node."""
        # Add system message if first iteration
        messages = list(state["messages"])
        if state["iteration"] == 0:
            messages = [SystemMessage(content=self.system_prompt)] + messages

        # Get model response
        response = self.model.invoke(messages)

        return {
            "messages": [response],
            "iteration": state["iteration"] + 1
        }

    def _tool_node(self, state: AgentState) -> dict:
        """Tool execution node."""
        last_message = state["messages"][-1]
        tool_results = []

        for tool_call in last_message.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            if tool_name in TOOL_MAP:
                try:
                    result = TOOL_MAP[tool_name].invoke(tool_args)
                except Exception as e:
                    result = f"Tool error: {e}"

                tool_results.append(
                    ToolMessage(
                        content=result,
                        tool_call_id=tool_call["id"]
                    )
                )

        return {"messages": tool_results}

    def _should_continue(self, state: AgentState) -> Literal["continue", "end"]:
        """Determine if agent should continue."""
        last_message = state["messages"][-1]

        # Check iteration limit
        if state["iteration"] >= state["max_iterations"]:
            return "end"

        # Check for tool calls
        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            return "continue"

        return "end"

    def invoke(self, message: str, session_id: str = "default") -> dict:
        """Invoke the agent."""
        config = {"configurable": {"thread_id": session_id}}

        result = self.graph.invoke(
            {
                "messages": [HumanMessage(content=message)],
                "iteration": 0,
                "max_iterations": self.max_iterations
            },
            config=config
        )

        return {
            "response": result["messages"][-1].content,
            "iterations": result["iteration"],
            "messages": result["messages"]
        }


# Usage
if __name__ == "__main__":
    agent = CustomAgent()
    result = agent.invoke("Search for Python best practices and analyze the results")
    print(f"Response: {result['response']}")
    print(f"Iterations: {result['iterations']}")
```

### Template 3: Multi-Agent System

```python
"""
Multi-agent system with supervisor orchestration.
"""
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from typing import TypedDict, Annotated, List, Literal
import operator


# Shared state
class TeamState(TypedDict):
    """Team state."""
    task: str
    messages: Annotated[List, operator.add]
    next_agent: str
    results: Annotated[List[str], operator.add]
    final_output: str
    iteration: int


class MultiAgentTeam:
    """Multi-agent team with supervisor."""

    def __init__(self, max_iterations: int = 5):
        self.model = ChatOpenAI(model="gpt-4o-mini")
        self.max_iterations = max_iterations
        self._build_graph()

    def _supervisor(self, state: TeamState) -> dict:
        """Supervisor decides which agent to call next."""
        prompt = f"""You are a supervisor managing a team.

Task: {state['task']}
Completed work: {state.get('results', [])}
Iteration: {state['iteration']} / {self.max_iterations}

Decide which worker to assign next:
- researcher: For gathering information
- analyst: For analyzing data
- writer: For creating content
- FINISH: If the task is complete

Respond with just the worker name or FINISH."""

        response = self.model.invoke(prompt)
        decision = response.content.strip().lower()

        if "finish" in decision or state["iteration"] >= self.max_iterations:
            return {"next_agent": "synthesizer"}

        for agent in ["researcher", "analyst", "writer"]:
            if agent in decision:
                return {"next_agent": agent, "iteration": state["iteration"] + 1}

        return {"next_agent": "synthesizer"}

    def _researcher(self, state: TeamState) -> dict:
        """Researcher agent."""
        prompt = f"Research this task: {state['task']}\nProvide factual information."
        response = self.model.invoke(prompt)
        return {"results": [f"RESEARCH: {response.content}"]}

    def _analyst(self, state: TeamState) -> dict:
        """Analyst agent."""
        context = "\n".join(state.get("results", []))
        prompt = f"Analyze this:\nTask: {state['task']}\nContext: {context}"
        response = self.model.invoke(prompt)
        return {"results": [f"ANALYSIS: {response.content}"]}

    def _writer(self, state: TeamState) -> dict:
        """Writer agent."""
        context = "\n".join(state.get("results", []))
        prompt = f"Write about:\nTask: {state['task']}\nContext: {context}"
        response = self.model.invoke(prompt)
        return {"results": [f"WRITING: {response.content}"]}

    def _synthesizer(self, state: TeamState) -> dict:
        """Synthesize final output."""
        context = "\n\n".join(state.get("results", []))
        prompt = f"Create a final comprehensive response:\nTask: {state['task']}\nWork completed:\n{context}"
        response = self.model.invoke(prompt)
        return {"final_output": response.content}

    def _route(self, state: TeamState) -> str:
        """Route to next agent."""
        return state["next_agent"]

    def _build_graph(self):
        """Build the multi-agent graph."""
        graph = StateGraph(TeamState)

        # Add nodes
        graph.add_node("supervisor", self._supervisor)
        graph.add_node("researcher", self._researcher)
        graph.add_node("analyst", self._analyst)
        graph.add_node("writer", self._writer)
        graph.add_node("synthesizer", self._synthesizer)

        # Set entry
        graph.set_entry_point("supervisor")

        # Routing
        graph.add_conditional_edges(
            "supervisor",
            self._route,
            {
                "researcher": "researcher",
                "analyst": "analyst",
                "writer": "writer",
                "synthesizer": "synthesizer"
            }
        )

        # Workers return to supervisor
        for worker in ["researcher", "analyst", "writer"]:
            graph.add_edge(worker, "supervisor")

        graph.add_edge("synthesizer", END)

        self.graph = graph.compile()

    def invoke(self, task: str) -> dict:
        """Execute the multi-agent task."""
        result = self.graph.invoke({
            "task": task,
            "messages": [],
            "results": [],
            "final_output": "",
            "iteration": 0,
            "next_agent": ""
        })

        return {
            "output": result["final_output"],
            "work_done": result["results"],
            "iterations": result["iteration"]
        }


# Usage
if __name__ == "__main__":
    team = MultiAgentTeam()
    result = team.invoke("Create a comprehensive guide on Python best practices")
    print(f"Output: {result['output'][:500]}...")
    print(f"Work items: {len(result['work_done'])}")
```

---

## Callback Handler Templates

### Template 1: Logging Callback

```python
"""
Comprehensive logging callback handler.
"""
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult
from typing import Any, Dict, List, Optional
import logging
import json
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("langchain")


class LoggingCallbackHandler(BaseCallbackHandler):
    """Log all LangChain events."""

    def __init__(self, log_level: int = logging.INFO):
        self.log_level = log_level
        self.run_id = None

    def on_llm_start(
        self,
        serialized: Dict[str, Any],
        prompts: List[str],
        **kwargs
    ):
        self.run_id = kwargs.get("run_id")
        logger.log(self.log_level, f"LLM Start | Run: {self.run_id}")
        logger.log(self.log_level, f"  Model: {serialized.get('name', 'unknown')}")
        logger.log(self.log_level, f"  Prompts: {len(prompts)}")

    def on_llm_end(self, response: LLMResult, **kwargs):
        logger.log(self.log_level, f"LLM End | Run: {self.run_id}")
        if response.llm_output:
            usage = response.llm_output.get("token_usage", {})
            logger.log(self.log_level, f"  Tokens: {usage}")

    def on_llm_error(self, error: Exception, **kwargs):
        logger.error(f"LLM Error | Run: {self.run_id} | {error}")

    def on_chain_start(
        self,
        serialized: Dict[str, Any],
        inputs: Dict[str, Any],
        **kwargs
    ):
        logger.log(self.log_level, f"Chain Start | {serialized.get('name', 'unknown')}")

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs):
        logger.log(self.log_level, f"Chain End | Keys: {list(outputs.keys())}")

    def on_chain_error(self, error: Exception, **kwargs):
        logger.error(f"Chain Error | {error}")

    def on_tool_start(
        self,
        serialized: Dict[str, Any],
        input_str: str,
        **kwargs
    ):
        logger.log(self.log_level, f"Tool Start | {serialized.get('name', 'unknown')}")
        logger.log(self.log_level, f"  Input: {input_str[:100]}...")

    def on_tool_end(self, output: str, **kwargs):
        logger.log(self.log_level, f"Tool End | Output: {output[:100]}...")

    def on_tool_error(self, error: Exception, **kwargs):
        logger.error(f"Tool Error | {error}")


# Usage
handler = LoggingCallbackHandler()
# chain.invoke({"input": "test"}, config={"callbacks": [handler]})
```

### Template 2: Metrics Callback

```python
"""
Metrics collection callback handler.
"""
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult
from typing import Any, Dict, List
from dataclasses import dataclass, field
from datetime import datetime
import time


@dataclass
class ExecutionMetrics:
    """Execution metrics container."""
    llm_calls: int = 0
    tool_calls: int = 0
    chain_calls: int = 0
    total_tokens: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_latency_ms: float = 0
    errors: List[str] = field(default_factory=list)
    timestamps: List[datetime] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "llm_calls": self.llm_calls,
            "tool_calls": self.tool_calls,
            "chain_calls": self.chain_calls,
            "total_tokens": self.total_tokens,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "avg_latency_ms": self.total_latency_ms / max(self.llm_calls, 1),
            "error_count": len(self.errors)
        }


class MetricsCallbackHandler(BaseCallbackHandler):
    """Collect execution metrics."""

    def __init__(self):
        self.metrics = ExecutionMetrics()
        self._start_times: Dict[str, float] = {}

    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs):
        run_id = str(kwargs.get("run_id", ""))
        self._start_times[run_id] = time.time()
        self.metrics.llm_calls += 1
        self.metrics.timestamps.append(datetime.now())

    def on_llm_end(self, response: LLMResult, **kwargs):
        run_id = str(kwargs.get("run_id", ""))
        if run_id in self._start_times:
            latency = (time.time() - self._start_times[run_id]) * 1000
            self.metrics.total_latency_ms += latency
            del self._start_times[run_id]

        if response.llm_output:
            usage = response.llm_output.get("token_usage", {})
            self.metrics.total_tokens += usage.get("total_tokens", 0)
            self.metrics.prompt_tokens += usage.get("prompt_tokens", 0)
            self.metrics.completion_tokens += usage.get("completion_tokens", 0)

    def on_llm_error(self, error: Exception, **kwargs):
        self.metrics.errors.append(f"LLM: {str(error)}")

    def on_chain_start(self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs):
        self.metrics.chain_calls += 1

    def on_chain_error(self, error: Exception, **kwargs):
        self.metrics.errors.append(f"Chain: {str(error)}")

    def on_tool_start(self, serialized: Dict[str, Any], input_str: str, **kwargs):
        self.metrics.tool_calls += 1

    def on_tool_error(self, error: Exception, **kwargs):
        self.metrics.errors.append(f"Tool: {str(error)}")

    def get_metrics(self) -> dict:
        return self.metrics.to_dict()

    def reset(self):
        self.metrics = ExecutionMetrics()
        self._start_times.clear()


# Usage
metrics_handler = MetricsCallbackHandler()
# Run chain with handler
# chain.invoke({"input": "test"}, config={"callbacks": [metrics_handler]})
# print(metrics_handler.get_metrics())
```

---

## Configuration Templates

### Template 1: Environment Configuration

```python
"""
Environment-based configuration for LangChain applications.
"""
import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class LLMConfig:
    """LLM configuration."""
    provider: str = os.getenv("LLM_PROVIDER", "openai")
    model: str = os.getenv("LLM_MODEL", "gpt-4o-mini")
    temperature: float = float(os.getenv("LLM_TEMPERATURE", "0"))
    max_tokens: Optional[int] = int(os.getenv("LLM_MAX_TOKENS", "0")) or None
    timeout: int = int(os.getenv("LLM_TIMEOUT", "30"))

    # API keys
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    google_api_key: str = os.getenv("GOOGLE_API_KEY", "")


@dataclass
class VectorStoreConfig:
    """Vector store configuration."""
    provider: str = os.getenv("VECTORSTORE_PROVIDER", "chroma")
    persist_directory: str = os.getenv("VECTORSTORE_PERSIST_DIR", "./vectorstore")
    collection_name: str = os.getenv("VECTORSTORE_COLLECTION", "default")

    # Provider-specific
    pinecone_api_key: str = os.getenv("PINECONE_API_KEY", "")
    pinecone_environment: str = os.getenv("PINECONE_ENV", "")
    qdrant_url: str = os.getenv("QDRANT_URL", "http://localhost:6333")


@dataclass
class ObservabilityConfig:
    """Observability configuration."""
    langsmith_enabled: bool = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
    langsmith_api_key: str = os.getenv("LANGCHAIN_API_KEY", "")
    langsmith_project: str = os.getenv("LANGCHAIN_PROJECT", "default")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")


@dataclass
class AppConfig:
    """Application configuration."""
    llm: LLMConfig
    vectorstore: VectorStoreConfig
    observability: ObservabilityConfig

    @classmethod
    def from_env(cls) -> "AppConfig":
        return cls(
            llm=LLMConfig(),
            vectorstore=VectorStoreConfig(),
            observability=ObservabilityConfig()
        )


# Factory function for LLM
def create_llm(config: LLMConfig = None):
    """Create LLM from configuration."""
    config = config or LLMConfig()

    if config.provider == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=config.model,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            timeout=config.timeout
        )
    elif config.provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(
            model=config.model,
            temperature=config.temperature,
            max_tokens=config.max_tokens
        )
    elif config.provider == "google":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            model=config.model,
            temperature=config.temperature
        )
    else:
        raise ValueError(f"Unknown provider: {config.provider}")


# Usage
if __name__ == "__main__":
    config = AppConfig.from_env()
    llm = create_llm(config.llm)
    print(f"Created LLM: {config.llm.provider}/{config.llm.model}")
```

### Template 2: YAML Configuration

```yaml
# config.yaml - LangChain application configuration

llm:
  provider: openai
  model: gpt-4o-mini
  temperature: 0
  max_tokens: null
  timeout: 30
  fallback:
    provider: anthropic
    model: claude-3-haiku-20240307

vectorstore:
  provider: chroma
  persist_directory: ./data/vectorstore
  collection: documents
  embedding_model: text-embedding-3-small

chain:
  max_retries: 3
  retry_delay: 1.0

agent:
  max_iterations: 10
  tools:
    - search
    - calculator
    - weather

observability:
  langsmith_enabled: true
  project: my-project
  log_level: INFO
```

```python
"""
YAML configuration loader.
"""
import yaml
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class LLMSettings:
    provider: str
    model: str
    temperature: float
    max_tokens: Optional[int]
    timeout: int


@dataclass
class VectorStoreSettings:
    provider: str
    persist_directory: str
    collection: str
    embedding_model: str


@dataclass
class AgentSettings:
    max_iterations: int
    tools: List[str]


def load_config(path: str = "config.yaml") -> dict:
    """Load configuration from YAML file."""
    with open(path, "r") as f:
        return yaml.safe_load(f)


def get_llm_settings(config: dict) -> LLMSettings:
    """Extract LLM settings from config."""
    llm = config.get("llm", {})
    return LLMSettings(
        provider=llm.get("provider", "openai"),
        model=llm.get("model", "gpt-4o-mini"),
        temperature=llm.get("temperature", 0),
        max_tokens=llm.get("max_tokens"),
        timeout=llm.get("timeout", 30)
    )


# Usage
config = load_config()
llm_settings = get_llm_settings(config)
```

---

## Testing Templates

### Template 1: Chain Unit Tests

```python
"""
Unit tests for LangChain chains.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from langchain_core.messages import AIMessage


class TestChain:
    """Test suite for chain functionality."""

    @pytest.fixture
    def mock_llm(self):
        """Create a mock LLM."""
        mock = MagicMock()
        mock.invoke.return_value = AIMessage(content="Test response")
        return mock

    def test_chain_basic_invoke(self, mock_llm):
        """Test basic chain invocation."""
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_core.output_parsers import StrOutputParser

        prompt = ChatPromptTemplate.from_template("Test: {input}")
        chain = prompt | mock_llm | StrOutputParser()

        result = chain.invoke({"input": "hello"})

        assert result == "Test response"
        mock_llm.invoke.assert_called_once()

    def test_chain_with_structured_output(self):
        """Test chain with structured output."""
        from pydantic import BaseModel

        class Output(BaseModel):
            answer: str
            confidence: float

        mock_model = MagicMock()
        mock_model.with_structured_output.return_value = MagicMock()
        mock_model.with_structured_output.return_value.invoke.return_value = Output(
            answer="Test",
            confidence=0.9
        )

        result = mock_model.with_structured_output(Output).invoke("test")

        assert isinstance(result, Output)
        assert result.answer == "Test"
        assert result.confidence == 0.9

    @pytest.mark.parametrize("input_text,expected_contains", [
        ("hello", "response"),
        ("goodbye", "response"),
    ])
    def test_chain_various_inputs(self, mock_llm, input_text, expected_contains):
        """Test chain with various inputs."""
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_core.output_parsers import StrOutputParser

        prompt = ChatPromptTemplate.from_template("{input}")
        chain = prompt | mock_llm | StrOutputParser()

        result = chain.invoke({"input": input_text})

        assert "response" in result.lower()


class TestToolExecution:
    """Test tool execution."""

    def test_tool_basic_execution(self):
        """Test basic tool execution."""
        from langchain_core.tools import tool

        @tool
        def add(a: int, b: int) -> str:
            """Add two numbers."""
            return str(a + b)

        result = add.invoke({"a": 2, "b": 3})
        assert result == "5"

    def test_tool_error_handling(self):
        """Test tool error handling."""
        from langchain_core.tools import tool, ToolException

        @tool(handle_tool_error=True)
        def failing_tool(x: str) -> str:
            """A tool that fails."""
            raise ToolException("Test error")

        result = failing_tool.invoke({"x": "test"})
        assert "error" in result.lower()


# Run with: pytest tests/test_chains.py -v
```

### Template 2: Integration Tests

```python
"""
Integration tests for LangChain applications.
"""
import pytest
import os


# Skip if no API key
pytestmark = pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY not set"
)


class TestIntegration:
    """Integration tests with real LLM."""

    @pytest.fixture
    def llm(self):
        """Create real LLM for integration tests."""
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model="gpt-4o-mini", temperature=0)

    @pytest.mark.integration
    def test_simple_chain_integration(self, llm):
        """Test simple chain with real LLM."""
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_core.output_parsers import StrOutputParser

        prompt = ChatPromptTemplate.from_template(
            "Answer in one word: What is 2 + 2?"
        )
        chain = prompt | llm | StrOutputParser()

        result = chain.invoke({})

        assert "4" in result or "four" in result.lower()

    @pytest.mark.integration
    def test_structured_output_integration(self, llm):
        """Test structured output with real LLM."""
        from pydantic import BaseModel, Field

        class MathResult(BaseModel):
            answer: int = Field(description="The numeric answer")
            explanation: str = Field(description="Brief explanation")

        structured_llm = llm.with_structured_output(MathResult)

        result = structured_llm.invoke("What is 5 * 5?")

        assert isinstance(result, MathResult)
        assert result.answer == 25

    @pytest.mark.integration
    @pytest.mark.slow
    def test_agent_integration(self, llm):
        """Test agent with real LLM."""
        from langgraph.prebuilt import create_react_agent
        from langchain_core.tools import tool

        @tool
        def multiply(a: int, b: int) -> str:
            """Multiply two numbers."""
            return str(a * b)

        agent = create_react_agent(llm, [multiply])

        result = agent.invoke({
            "messages": [("human", "What is 7 times 8?")]
        })

        final_message = result["messages"][-1].content
        assert "56" in final_message


# Run with: pytest tests/test_integration.py -v -m integration
```

---

*Templates v2.0 - LangChain 1.0+ / LangGraph 1.0+*
