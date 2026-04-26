"""
Pydantic schemas for Agentic RAG structured outputs.
Use with .with_structured_output() or instructor.
"""
from pydantic import BaseModel, Field
from typing import Literal, List, Optional


class RouteQuery(BaseModel):
    """Query routing decision."""
    datasource: Literal["vectorstore", "web_search", "direct_response", "api", "hybrid"]
    reasoning: str = Field(description="Why this route was chosen")
    confidence: float = Field(ge=0, le=1, description="Routing confidence")
    fallback_source: Optional[str] = Field(default=None, description="Backup if primary fails")


class GradeDocument(BaseModel):
    """Document relevance grade."""
    binary_score: Literal["yes", "no"]
    relevance_score: float = Field(ge=0, le=1)
    reasoning: str = Field(description="Why this score")
    key_information: Optional[str] = Field(default=None, description="Key info if relevant")


class RewriteQuery(BaseModel):
    """Query rewrite result."""
    rewritten_query: str
    strategy: Literal["synonym_expansion", "specificity_increase", "specificity_decrease",
                      "decomposition", "rephrasing"]
    sub_queries: List[str] = Field(default_factory=list)
    expected_improvement: str


class SufficiencyCheck(BaseModel):
    """Context sufficiency assessment."""
    is_sufficient: bool
    missing_information: List[str]
    confidence: float = Field(ge=0, le=1)
    recommendation: Literal["generate", "retrieve_more", "rewrite_query", "web_search", "clarify"]


class VerificationResult(BaseModel):
    """Answer verification result."""
    is_grounded: bool
    grounding_score: float = Field(ge=0, le=1)
    unsupported_claims: List[str]
    contradictions: List[str]
    verified_answer: str


class ComplexityAssessment(BaseModel):
    """Query complexity for Adaptive RAG routing."""
    complexity: Literal["simple", "moderate", "complex"]
    reasoning: str
    requires_retrieval: bool
    estimated_hops: int = Field(ge=0, le=5)
    recommended_sources: List[str]
