"""
State schemas for Agentic RAG workflows.
Usage: import and extend for your specific pipeline.
"""
from typing import TypedDict, List, Optional, Literal
from dataclasses import dataclass, field


class CorrectiveRAGState(TypedDict):
    """State for Corrective RAG with retry logic."""
    question: str
    documents: List[str]
    filtered_documents: List[str]
    generation: str
    web_search_needed: bool
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
    agent_results: dict       # {agent_name: [documents]}
    aggregated_documents: List[str]
    generation: str
    confidence_scores: dict   # {agent_name: confidence}


@dataclass
class RAGStateExtended:
    """Extended state with full tracking for production pipelines."""
    original_question: str
    current_query: str
    query_history: List[str] = field(default_factory=list)
    documents: List[str] = field(default_factory=list)
    relevant_documents: List[str] = field(default_factory=list)
    generation: str = ""
    generation_attempts: int = 0
    is_verified: bool = False
    verification_score: float = 0.0
    unsupported_claims: List[str] = field(default_factory=list)
    retries: int = 0
    max_retries: int = 3
    web_search_used: bool = False
    total_tokens_used: int = 0
