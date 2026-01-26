# Agentic RAG Templates

Reusable templates for building agentic RAG systems.

## 1. State Schema Templates

### Basic Agentic RAG State

```python
from typing import TypedDict, List, Optional, Literal
from dataclasses import dataclass, field


class AgenticRAGState(TypedDict):
    """Minimal state for agentic RAG."""
    question: str
    documents: List[str]
    generation: str


class CorrectiveRAGState(TypedDict):
    """State for Corrective RAG with retry logic."""
    question: str
    documents: List[str]
    filtered_documents: List[str]
    generation: str
    web_search_needed: bool
    query_rewrite_needed: bool
    current_query: str
    retries: int
    max_retries: int


class AdaptiveRAGState(TypedDict):
    """State for Adaptive RAG with complexity routing."""
    question: str
    complexity: Literal["simple", "moderate", "complex"]
    retrieval_strategy: Literal["none", "single", "multi_hop"]
    documents: List[str]
    hop_count: int
    max_hops: int
    generation: str


class MultiAgentRAGState(TypedDict):
    """State for multi-agent orchestration."""
    question: str
    routing_decision: str
    agent_results: dict  # {agent_name: [documents]}
    aggregated_documents: List[str]
    generation: str
    confidence_scores: dict  # {agent_name: confidence}
```

### Extended State with Metadata

```python
@dataclass
class RAGStateExtended:
    """Extended state with full tracking."""
    # Query
    original_question: str
    current_query: str
    query_history: List[str] = field(default_factory=list)

    # Retrieval
    documents: List[str] = field(default_factory=list)
    document_scores: List[float] = field(default_factory=list)
    document_sources: List[str] = field(default_factory=list)

    # Grading
    relevant_documents: List[str] = field(default_factory=list)
    irrelevant_count: int = 0

    # Generation
    generation: str = ""
    generation_attempts: int = 0

    # Verification
    is_verified: bool = False
    verification_score: float = 0.0
    unsupported_claims: List[str] = field(default_factory=list)

    # Control
    retries: int = 0
    max_retries: int = 3
    web_search_used: bool = False
    total_tokens_used: int = 0

    # Timing
    start_time: float = 0.0
    retrieval_time: float = 0.0
    generation_time: float = 0.0
```

## 2. Pydantic Schema Templates

### Query Routing

```python
from pydantic import BaseModel, Field
from typing import Literal, List, Optional


class RouteQuery(BaseModel):
    """Query routing decision."""
    datasource: Literal[
        "vectorstore",
        "web_search",
        "direct_response",
        "api",
        "hybrid"
    ]
    reasoning: str = Field(description="Why this route was chosen")
    confidence: float = Field(ge=0, le=1, description="Routing confidence")
    fallback_source: Optional[str] = Field(
        default=None,
        description="Backup source if primary fails"
    )


class MultiSourceRoute(BaseModel):
    """Route to multiple sources."""
    sources: List[Literal["vectorstore", "web_search", "api"]]
    primary_source: str
    reasoning: str
    parallel_execution: bool = Field(
        default=True,
        description="Whether to query sources in parallel"
    )
```

### Document Grading

```python
class GradeDocument(BaseModel):
    """Document relevance grade."""
    binary_score: Literal["yes", "no"]
    relevance_score: float = Field(ge=0, le=1)
    reasoning: str = Field(description="Why this score")
    key_information: Optional[str] = Field(
        default=None,
        description="Key info extracted if relevant"
    )


class GradeBatch(BaseModel):
    """Batch document grading."""
    grades: List[GradeDocument]
    overall_quality: Literal["high", "medium", "low"]
    recommendation: Literal["proceed", "rewrite_query", "web_search"]
```

### Query Rewriting

```python
class RewriteQuery(BaseModel):
    """Query rewrite result."""
    rewritten_query: str
    strategy: Literal[
        "synonym_expansion",
        "specificity_increase",
        "specificity_decrease",
        "decomposition",
        "rephrasing"
    ]
    sub_queries: List[str] = Field(default_factory=list)
    expected_improvement: str


class QueryDecomposition(BaseModel):
    """Complex query decomposition."""
    original_query: str
    sub_queries: List[str]
    execution_order: List[int]
    dependencies: dict  # {query_idx: [depends_on_idx]}
```

### Complexity Assessment

```python
class ComplexityAssessment(BaseModel):
    """Query complexity assessment."""
    complexity: Literal["simple", "moderate", "complex"]
    reasoning: str
    requires_retrieval: bool
    estimated_hops: int = Field(ge=0, le=5)
    recommended_sources: List[str]
    estimated_tokens: int


class SufficiencyCheck(BaseModel):
    """Context sufficiency assessment."""
    is_sufficient: bool
    missing_information: List[str]
    confidence: float = Field(ge=0, le=1)
    recommendation: Literal[
        "generate",
        "retrieve_more",
        "rewrite_query",
        "web_search",
        "clarify"
    ]
```

### Verification

```python
class VerificationResult(BaseModel):
    """Answer verification result."""
    is_grounded: bool
    grounding_score: float = Field(ge=0, le=1)
    unsupported_claims: List[str]
    contradictions: List[str]
    missing_nuance: List[str]
    suggested_corrections: List[str]
    verified_answer: str


class HallucinationCheck(BaseModel):
    """Hallucination detection."""
    has_hallucination: bool
    hallucinated_claims: List[str]
    severity: Literal["none", "minor", "major", "critical"]
    corrected_text: str
```

## 3. LangGraph Workflow Templates

### Basic Corrective RAG

```python
from langgraph.graph import StateGraph, END
from typing import Literal


def create_corrective_rag_workflow():
    """Create basic Corrective RAG workflow."""

    workflow = StateGraph(CorrectiveRAGState)

    # Add nodes
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("grade_documents", grade_documents_node)
    workflow.add_node("rewrite_query", rewrite_query_node)
    workflow.add_node("web_search", web_search_node)
    workflow.add_node("generate", generate_node)

    # Set entry point
    workflow.set_entry_point("retrieve")

    # Add edges
    workflow.add_edge("retrieve", "grade_documents")

    workflow.add_conditional_edges(
        "grade_documents",
        decide_after_grading,
        {
            "generate": "generate",
            "rewrite": "rewrite_query",
            "web_search": "web_search"
        }
    )

    workflow.add_edge("rewrite_query", "retrieve")
    workflow.add_edge("web_search", "generate")
    workflow.add_edge("generate", END)

    return workflow.compile()


def decide_after_grading(state: CorrectiveRAGState) -> Literal["generate", "rewrite", "web_search"]:
    """Decide next step after grading."""
    if len(state["filtered_documents"]) >= 2:
        return "generate"
    elif state["retries"] < state["max_retries"]:
        return "rewrite"
    else:
        return "web_search"
```

### Adaptive RAG with Complexity Routing

```python
def create_adaptive_rag_workflow():
    """Create Adaptive RAG with complexity-based routing."""

    workflow = StateGraph(AdaptiveRAGState)

    # Add nodes
    workflow.add_node("classify_complexity", classify_complexity_node)
    workflow.add_node("direct_answer", direct_answer_node)
    workflow.add_node("single_retrieval", single_retrieval_node)
    workflow.add_node("multi_hop_retrieval", multi_hop_retrieval_node)
    workflow.add_node("generate", generate_node)

    # Set entry point
    workflow.set_entry_point("classify_complexity")

    # Route based on complexity
    workflow.add_conditional_edges(
        "classify_complexity",
        route_by_complexity,
        {
            "direct": "direct_answer",
            "single": "single_retrieval",
            "multi_hop": "multi_hop_retrieval"
        }
    )

    workflow.add_edge("direct_answer", END)
    workflow.add_edge("single_retrieval", "generate")
    workflow.add_edge("multi_hop_retrieval", "generate")
    workflow.add_edge("generate", END)

    return workflow.compile()


def route_by_complexity(state: AdaptiveRAGState) -> Literal["direct", "single", "multi_hop"]:
    """Route based on complexity classification."""
    if state["complexity"] == "simple":
        return "direct"
    elif state["complexity"] == "moderate":
        return "single"
    else:
        return "multi_hop"
```

### Full Self-Correcting RAG

```python
def create_self_correcting_rag_workflow():
    """Create full self-correcting RAG with verification."""

    workflow = StateGraph(RAGStateExtended)

    # Add all nodes
    workflow.add_node("route_query", route_query_node)
    workflow.add_node("retrieve_vector", retrieve_vector_node)
    workflow.add_node("retrieve_web", retrieve_web_node)
    workflow.add_node("retrieve_api", retrieve_api_node)
    workflow.add_node("grade_documents", grade_documents_node)
    workflow.add_node("check_sufficiency", check_sufficiency_node)
    workflow.add_node("rewrite_query", rewrite_query_node)
    workflow.add_node("generate", generate_node)
    workflow.add_node("verify", verify_node)
    workflow.add_node("finalize", finalize_node)

    # Entry point
    workflow.set_entry_point("route_query")

    # Routing edges
    workflow.add_conditional_edges(
        "route_query",
        get_retrieval_source,
        {
            "vectorstore": "retrieve_vector",
            "web_search": "retrieve_web",
            "api": "retrieve_api"
        }
    )

    # After retrieval -> grade
    workflow.add_edge("retrieve_vector", "grade_documents")
    workflow.add_edge("retrieve_web", "grade_documents")
    workflow.add_edge("retrieve_api", "grade_documents")

    # After grading -> check sufficiency
    workflow.add_edge("grade_documents", "check_sufficiency")

    # Sufficiency decision
    workflow.add_conditional_edges(
        "check_sufficiency",
        decide_after_sufficiency,
        {
            "generate": "generate",
            "rewrite": "rewrite_query",
            "web_fallback": "retrieve_web"
        }
    )

    # Rewrite loops back
    workflow.add_edge("rewrite_query", "route_query")

    # Generate -> verify
    workflow.add_edge("generate", "verify")

    # Verification decision
    workflow.add_conditional_edges(
        "verify",
        decide_after_verification,
        {
            "finalize": "finalize",
            "regenerate": "generate"
        }
    )

    workflow.add_edge("finalize", END)

    return workflow.compile()
```

## 4. Configuration Templates

### Environment Configuration

```python
from pydantic_settings import BaseSettings
from typing import Literal, Optional


class AgenticRAGConfig(BaseSettings):
    """Configuration for Agentic RAG system."""

    # LLM Settings
    llm_provider: Literal["openai", "anthropic", "google"] = "openai"
    llm_model: str = "gpt-4o"
    llm_temperature: float = 0.0
    llm_max_tokens: int = 4096

    # Retrieval Settings
    vector_store: Literal["qdrant", "weaviate", "chroma", "pinecone"] = "qdrant"
    embedding_model: str = "text-embedding-3-small"
    retrieval_k: int = 5
    relevance_threshold: float = 0.7

    # Agentic Settings
    max_retries: int = 3
    max_hops: int = 5
    enable_web_search: bool = True
    web_search_provider: str = "tavily"

    # Verification
    enable_verification: bool = True
    verification_threshold: float = 0.8

    # Observability
    enable_tracing: bool = True
    trace_provider: str = "langsmith"

    class Config:
        env_prefix = "AGENTIC_RAG_"
```

### Agent Configuration

```python
from dataclasses import dataclass
from typing import List, Callable


@dataclass
class AgentConfig:
    """Configuration for a specialized agent."""
    name: str
    description: str
    retriever: any
    llm: any
    tools: List[str]
    max_iterations: int = 3
    timeout_seconds: int = 30


@dataclass
class OrchestratorConfig:
    """Configuration for orchestrator agent."""
    agents: List[AgentConfig]
    routing_strategy: Literal["llm", "classifier", "hybrid"] = "llm"
    parallel_execution: bool = True
    aggregation_strategy: Literal["rank", "merge", "vote"] = "rank"
    fallback_agent: Optional[str] = None
```

## 5. Node Function Templates

### Standard Node Pattern

```python
from typing import Dict, Any


def node_template(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Standard node function template.

    Args:
        state: Current workflow state

    Returns:
        Updated state (only changed fields)
    """
    # 1. Extract needed state
    input_field = state.get("input_field", "")

    # 2. Perform operation
    try:
        result = perform_operation(input_field)
    except Exception as e:
        # Handle error
        return {
            "error": str(e),
            "error_node": "node_template"
        }

    # 3. Return updated state
    return {
        "output_field": result,
        "node_completed": "node_template"
    }
```

### Retrieval Node

```python
def retrieve_node(state: CorrectiveRAGState) -> Dict[str, Any]:
    """Retrieve documents from vector store."""
    query = state.get("current_query") or state["question"]

    try:
        documents = vector_store.similarity_search(
            query=query,
            k=config.retrieval_k
        )
        return {
            "documents": [doc.page_content for doc in documents],
            "document_scores": [doc.metadata.get("score", 0) for doc in documents]
        }
    except Exception as e:
        return {
            "documents": [],
            "retrieval_error": str(e)
        }
```

### Grading Node

```python
def grade_documents_node(state: CorrectiveRAGState) -> Dict[str, Any]:
    """Grade documents for relevance."""
    question = state["question"]
    documents = state["documents"]

    filtered = []
    for doc in documents:
        grade = document_grader.grade(question, doc)
        if grade.binary_score == "yes":
            filtered.append(doc)

    return {
        "filtered_documents": filtered,
        "web_search_needed": len(filtered) < 2,
        "query_rewrite_needed": len(filtered) == 0
    }
```

### Generation Node

```python
def generate_node(state: CorrectiveRAGState) -> Dict[str, Any]:
    """Generate answer from documents."""
    question = state["question"]
    documents = state.get("filtered_documents") or state["documents"]

    context = "\n\n".join(documents)
    prompt = f"""Answer based on context only.

Context:
{context}

Question: {question}

Answer:"""

    generation = llm.invoke(prompt)

    return {
        "generation": generation.content,
        "generation_attempts": state.get("generation_attempts", 0) + 1
    }
```

## 6. Error Handling Templates

### Retry Decorator

```python
import functools
import time
from typing import TypeVar, Callable

T = TypeVar("T")


def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exceptions: tuple = (Exception,)
) -> Callable:
    """Retry decorator with exponential backoff."""

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> T:
            delay = base_delay
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_retries:
                        time.sleep(min(delay, max_delay))
                        delay *= 2

            raise last_exception

        return wrapper
    return decorator
```

### Fallback Handler

```python
from typing import Optional, List


class FallbackHandler:
    """Handle failures with fallback strategies."""

    def __init__(
        self,
        primary_retriever,
        fallback_retrievers: List,
        llm
    ):
        self.primary = primary_retriever
        self.fallbacks = fallback_retrievers
        self.llm = llm

    def retrieve_with_fallback(
        self,
        query: str,
        k: int = 5
    ) -> List[str]:
        """Retrieve with automatic fallback."""
        # Try primary
        try:
            docs = self.primary.retrieve(query, k=k)
            if docs:
                return docs
        except Exception:
            pass

        # Try fallbacks
        for fallback in self.fallbacks:
            try:
                docs = fallback.retrieve(query, k=k)
                if docs:
                    return docs
            except Exception:
                continue

        # Last resort: LLM without retrieval
        return []
```
