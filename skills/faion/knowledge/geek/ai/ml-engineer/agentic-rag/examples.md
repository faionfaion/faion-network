# Agentic RAG Code Examples

## 1. Basic Agentic RAG Pattern

```python
"""
Basic Agentic RAG with iterative retrieval and self-correction.
"""
from typing import List, Optional
from dataclasses import dataclass, field
from enum import Enum


class RetrievalStatus(Enum):
    SUFFICIENT = "sufficient"
    INSUFFICIENT = "insufficient"
    NEEDS_CLARIFICATION = "needs_clarification"


@dataclass
class RetrievalResult:
    documents: List[str]
    scores: List[float]
    query_used: str


@dataclass
class AgentState:
    original_query: str
    current_query: str
    context: List[str] = field(default_factory=list)
    retrieval_history: List[RetrievalResult] = field(default_factory=list)
    attempts: int = 0
    max_attempts: int = 3


class AgenticRAG:
    """
    Core agentic RAG implementation with self-correction loop.
    """

    def __init__(
        self,
        retriever,
        llm,
        relevance_threshold: float = 0.7,
        max_attempts: int = 3
    ):
        self.retriever = retriever
        self.llm = llm
        self.relevance_threshold = relevance_threshold
        self.max_attempts = max_attempts

    def answer(self, query: str) -> str:
        """Main entry point for answering queries."""
        state = AgentState(
            original_query=query,
            current_query=query,
            max_attempts=self.max_attempts
        )

        while state.attempts < state.max_attempts:
            state.attempts += 1

            # Step 1: Retrieve
            result = self._retrieve(state.current_query)
            state.retrieval_history.append(result)

            # Step 2: Grade relevance
            relevant_docs = self._grade_documents(
                state.original_query,
                result.documents,
                result.scores
            )

            # Step 3: Check sufficiency
            state.context.extend(relevant_docs)
            status = self._check_sufficiency(state.original_query, state.context)

            if status == RetrievalStatus.SUFFICIENT:
                break

            # Step 4: Refine query for next iteration
            state.current_query = self._refine_query(
                state.original_query,
                state.current_query,
                state.context
            )

        # Step 5: Generate answer
        answer = self._generate(state.original_query, state.context)

        # Step 6: Verify answer
        verified_answer = self._verify(answer, state.context)

        return verified_answer

    def _retrieve(self, query: str) -> RetrievalResult:
        """Retrieve documents for query."""
        docs, scores = self.retriever.retrieve(query, k=5)
        return RetrievalResult(
            documents=docs,
            scores=scores,
            query_used=query
        )

    def _grade_documents(
        self,
        query: str,
        documents: List[str],
        scores: List[float]
    ) -> List[str]:
        """Grade and filter documents by relevance."""
        relevant = []
        for doc, score in zip(documents, scores):
            if score >= self.relevance_threshold:
                relevant.append(doc)
            else:
                # Use LLM to grade borderline documents
                if self._llm_grade(query, doc):
                    relevant.append(doc)
        return relevant

    def _llm_grade(self, query: str, document: str) -> bool:
        """Use LLM to grade document relevance."""
        prompt = f"""Grade if this document is relevant to the query.
Query: {query}
Document: {document}
Respond with only 'yes' or 'no'."""
        response = self.llm.generate(prompt)
        return response.strip().lower() == "yes"

    def _check_sufficiency(
        self,
        query: str,
        context: List[str]
    ) -> RetrievalStatus:
        """Check if context is sufficient to answer query."""
        prompt = f"""Can the following context fully answer this query?
Query: {query}
Context: {' '.join(context[:3])}
Respond with: SUFFICIENT, INSUFFICIENT, or NEEDS_CLARIFICATION"""
        response = self.llm.generate(prompt)
        return RetrievalStatus(response.strip().lower())

    def _refine_query(
        self,
        original: str,
        current: str,
        context: List[str]
    ) -> str:
        """Refine query based on retrieved context."""
        prompt = f"""The current query did not retrieve sufficient information.
Original query: {original}
Current query: {current}
Retrieved context: {' '.join(context[:2])}
Generate a refined query to find missing information."""
        return self.llm.generate(prompt).strip()

    def _generate(self, query: str, context: List[str]) -> str:
        """Generate answer from context."""
        prompt = f"""Answer the question based on the context.
Question: {query}
Context: {' '.join(context)}
Answer:"""
        return self.llm.generate(prompt)

    def _verify(self, answer: str, context: List[str]) -> str:
        """Verify answer is grounded in context."""
        prompt = f"""Verify this answer is factually grounded in the context.
Answer: {answer}
Context: {' '.join(context)}
If any claims are not supported, remove them. Return verified answer."""
        return self.llm.generate(prompt)
```

## 2. Query Router with Structured Output

```python
"""
Query router using structured outputs for reliable routing.
"""
from pydantic import BaseModel, Field
from typing import Literal
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


class RouteQuery(BaseModel):
    """Route query to appropriate data source."""
    datasource: Literal["vectorstore", "web_search", "direct_response", "api"]
    reasoning: str = Field(description="Reasoning for routing decision")
    confidence: float = Field(ge=0, le=1, description="Confidence in routing")


class QueryRouter:
    """Routes queries to appropriate retrieval sources."""

    def __init__(self, llm: ChatOpenAI):
        self.llm = llm.with_structured_output(RouteQuery)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a query router. Route queries to the best source:

- vectorstore: Domain-specific content, documentation, internal knowledge
- web_search: Current events, recent news, real-time information
- direct_response: General knowledge, definitions, simple facts
- api: User-specific data (email, calendar, CRM)

Consider query intent, required freshness, and domain specificity."""),
            ("human", "Route this query: {query}")
        ])
        self.chain = self.prompt | self.llm

    def route(self, query: str) -> RouteQuery:
        """Route query to appropriate source."""
        return self.chain.invoke({"query": query})


# Usage
router = QueryRouter(ChatOpenAI(model="gpt-4o-mini"))
result = router.route("What were the Q3 2024 earnings for Apple?")
print(f"Route to: {result.datasource}")
print(f"Reasoning: {result.reasoning}")
print(f"Confidence: {result.confidence}")
```

## 3. Document Grader

```python
"""
Document grader with binary and graded relevance scoring.
"""
from pydantic import BaseModel, Field
from typing import Literal, List
from langchain_core.prompts import ChatPromptTemplate


class GradeDocument(BaseModel):
    """Grade document relevance."""
    binary_score: Literal["yes", "no"]
    relevance_score: float = Field(ge=0, le=1)
    reasoning: str


class DocumentGrader:
    """Grades retrieved documents for relevance."""

    def __init__(self, llm):
        self.llm = llm.with_structured_output(GradeDocument)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a relevance grader. Assess if a document
is relevant to answering a user question.

Consider:
- Direct relevance to the question
- Factual information that helps answer
- Context that provides necessary background

Be strict: only mark as relevant if it directly helps answer."""),
            ("human", """Question: {question}

Document: {document}

Grade the document's relevance.""")
        ])
        self.chain = self.prompt | self.llm

    def grade(self, question: str, document: str) -> GradeDocument:
        """Grade a single document."""
        return self.chain.invoke({
            "question": question,
            "document": document
        })

    def grade_batch(
        self,
        question: str,
        documents: List[str],
        threshold: float = 0.7
    ) -> List[str]:
        """Grade multiple documents, return relevant ones."""
        relevant = []
        for doc in documents:
            grade = self.grade(question, doc)
            if grade.binary_score == "yes" and grade.relevance_score >= threshold:
                relevant.append(doc)
        return relevant
```

## 4. Query Rewriter with Strategies

```python
"""
Query rewriter with multiple rewriting strategies.
"""
from pydantic import BaseModel, Field
from typing import Literal, List
from langchain_core.prompts import ChatPromptTemplate


class RewrittenQuery(BaseModel):
    """Rewritten query with strategy used."""
    rewritten_query: str
    strategy_used: Literal[
        "synonym_expansion",
        "specificity_adjustment",
        "decomposition",
        "context_incorporation"
    ]
    sub_queries: List[str] = Field(default_factory=list)


class QueryRewriter:
    """Rewrites queries to improve retrieval."""

    def __init__(self, llm):
        self.llm = llm.with_structured_output(RewrittenQuery)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a query rewriter. Improve the query for better retrieval.

Strategies:
1. synonym_expansion: Add synonyms and related terms
2. specificity_adjustment: Make more specific or broader as needed
3. decomposition: Break into sub-queries for complex questions
4. context_incorporation: Use retrieved context to refine

Choose the best strategy based on why retrieval may have failed."""),
            ("human", """Original query: {original_query}
Current query: {current_query}
Retrieved context (may be empty or irrelevant): {context}
Rewrite attempts so far: {attempt_count}

Rewrite the query to improve retrieval.""")
        ])
        self.chain = self.prompt | self.llm

    def rewrite(
        self,
        original_query: str,
        current_query: str,
        context: str = "",
        attempt_count: int = 1
    ) -> RewrittenQuery:
        """Rewrite query for better retrieval."""
        return self.chain.invoke({
            "original_query": original_query,
            "current_query": current_query,
            "context": context[:1000] if context else "No relevant context found.",
            "attempt_count": attempt_count
        })
```

## 5. Corrective RAG with LangGraph

```python
"""
Corrective RAG implementation using LangGraph.
"""
from typing import TypedDict, List, Literal
from langgraph.graph import StateGraph, END


class CRAGState(TypedDict):
    """State for Corrective RAG workflow."""
    question: str
    documents: List[str]
    generation: str
    web_search_needed: bool
    retries: int
    max_retries: int


def retrieve(state: CRAGState) -> CRAGState:
    """Retrieve documents from vector store."""
    question = state["question"]
    documents = vector_store.similarity_search(question, k=4)
    return {
        **state,
        "documents": [doc.page_content for doc in documents]
    }


def grade_documents(state: CRAGState) -> CRAGState:
    """Grade retrieved documents for relevance."""
    question = state["question"]
    documents = state["documents"]

    filtered_docs = []
    web_search_needed = False

    for doc in documents:
        grade = document_grader.grade(question, doc)
        if grade.binary_score == "yes":
            filtered_docs.append(doc)

    if len(filtered_docs) < 2:
        web_search_needed = True

    return {
        **state,
        "documents": filtered_docs,
        "web_search_needed": web_search_needed
    }


def web_search(state: CRAGState) -> CRAGState:
    """Perform web search for additional context."""
    question = state["question"]
    web_results = tavily_search.search(question, max_results=3)

    documents = state["documents"]
    for result in web_results:
        documents.append(result["content"])

    return {
        **state,
        "documents": documents,
        "web_search_needed": False
    }


def generate(state: CRAGState) -> CRAGState:
    """Generate answer from documents."""
    question = state["question"]
    documents = state["documents"]

    context = "\n\n".join(documents)
    generation = rag_chain.invoke({
        "question": question,
        "context": context
    })

    return {
        **state,
        "generation": generation
    }


def decide_to_generate(state: CRAGState) -> Literal["web_search", "generate"]:
    """Decide whether to generate or search web."""
    if state["web_search_needed"]:
        return "web_search"
    return "generate"


# Build graph
workflow = StateGraph(CRAGState)

workflow.add_node("retrieve", retrieve)
workflow.add_node("grade_documents", grade_documents)
workflow.add_node("web_search", web_search)
workflow.add_node("generate", generate)

workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "grade_documents")
workflow.add_conditional_edges(
    "grade_documents",
    decide_to_generate,
    {
        "web_search": "web_search",
        "generate": "generate"
    }
)
workflow.add_edge("web_search", "generate")
workflow.add_edge("generate", END)

# Compile
crag_app = workflow.compile()

# Usage
result = crag_app.invoke({
    "question": "What is the latest on quantum computing?",
    "documents": [],
    "generation": "",
    "web_search_needed": False,
    "retries": 0,
    "max_retries": 2
})
```

## 6. Adaptive RAG with Complexity Classification

```python
"""
Adaptive RAG that adjusts strategy based on query complexity.
"""
from pydantic import BaseModel
from typing import Literal
from enum import Enum


class QueryComplexity(str, Enum):
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"


class ComplexityAssessment(BaseModel):
    """Query complexity assessment."""
    complexity: Literal["simple", "moderate", "complex"]
    reasoning: str
    requires_retrieval: bool
    estimated_hops: int


class AdaptiveRAG:
    """
    Adaptive RAG that adjusts strategy based on query complexity.
    """

    def __init__(self, llm, retriever, web_search):
        self.llm = llm
        self.retriever = retriever
        self.web_search = web_search
        self.complexity_classifier = llm.with_structured_output(ComplexityAssessment)

    def classify_complexity(self, query: str) -> ComplexityAssessment:
        """Classify query complexity."""
        prompt = f"""Assess the complexity of this query:

Query: {query}

Complexity levels:
- simple: Can be answered from general knowledge, no retrieval needed
- moderate: Requires single-step retrieval from one source
- complex: Requires multi-hop reasoning, multiple sources

Estimate how many retrieval "hops" are needed (0-5)."""

        return self.complexity_classifier.invoke(prompt)

    def answer(self, query: str) -> str:
        """Answer query with adaptive strategy."""
        assessment = self.classify_complexity(query)

        if assessment.complexity == QueryComplexity.SIMPLE:
            return self._direct_answer(query)

        elif assessment.complexity == QueryComplexity.MODERATE:
            return self._single_hop_answer(query)

        else:
            return self._multi_hop_answer(query, assessment.estimated_hops)

    def _direct_answer(self, query: str) -> str:
        """Answer directly without retrieval."""
        return self.llm.invoke(f"Answer this question: {query}")

    def _single_hop_answer(self, query: str) -> str:
        """Single retrieval step."""
        docs = self.retriever.retrieve(query, k=3)
        context = "\n".join([d.page_content for d in docs])
        return self.llm.invoke(
            f"Context: {context}\n\nQuestion: {query}\n\nAnswer:"
        )

    def _multi_hop_answer(self, query: str, max_hops: int) -> str:
        """Multi-hop iterative retrieval."""
        context = []
        current_query = query

        for hop in range(max_hops):
            # Retrieve
            docs = self.retriever.retrieve(current_query, k=3)
            context.extend([d.page_content for d in docs])

            # Check if we have enough
            if self._is_sufficient(query, context):
                break

            # Generate follow-up query
            current_query = self._generate_followup(query, context)

        # Generate final answer
        return self.llm.invoke(
            f"Context: {' '.join(context)}\n\nQuestion: {query}\n\nAnswer:"
        )

    def _is_sufficient(self, query: str, context: List[str]) -> bool:
        """Check if context is sufficient."""
        prompt = f"""Is this context sufficient to fully answer the question?
Question: {query}
Context: {' '.join(context[:3])}
Answer yes or no."""
        return "yes" in self.llm.invoke(prompt).lower()

    def _generate_followup(self, original: str, context: List[str]) -> str:
        """Generate follow-up query for next hop."""
        prompt = f"""What additional information is needed to answer this question?
Question: {original}
Already retrieved: {' '.join(context[:2])}
Generate a follow-up query."""
        return self.llm.invoke(prompt)
```

## 7. Multi-Agent RAG System

```python
"""
Multi-agent RAG with specialized retrieval agents.
"""
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass


@dataclass
class AgentResult:
    agent_name: str
    documents: List[str]
    confidence: float
    metadata: Dict[str, Any]


class SpecializedAgent:
    """Base class for specialized retrieval agents."""

    def __init__(self, name: str, retriever, llm):
        self.name = name
        self.retriever = retriever
        self.llm = llm

    def retrieve(self, query: str) -> AgentResult:
        raise NotImplementedError


class VectorSearchAgent(SpecializedAgent):
    """Agent for vector store retrieval."""

    def retrieve(self, query: str) -> AgentResult:
        docs = self.retriever.similarity_search(query, k=5)
        return AgentResult(
            agent_name=self.name,
            documents=[d.page_content for d in docs],
            confidence=0.9,
            metadata={"source": "vector_store"}
        )


class WebSearchAgent(SpecializedAgent):
    """Agent for web search."""

    def retrieve(self, query: str) -> AgentResult:
        results = self.retriever.search(query, max_results=5)
        return AgentResult(
            agent_name=self.name,
            documents=[r["content"] for r in results],
            confidence=0.7,
            metadata={"source": "web"}
        )


class APIAgent(SpecializedAgent):
    """Agent for API-based retrieval."""

    def retrieve(self, query: str) -> AgentResult:
        # Call external API
        response = self.retriever.query(query)
        return AgentResult(
            agent_name=self.name,
            documents=[response.get("content", "")],
            confidence=0.8,
            metadata={"source": "api", "api_name": self.retriever.name}
        )


class OrchestratorAgent:
    """
    Master orchestrator that coordinates specialized agents.
    """

    def __init__(
        self,
        agents: List[SpecializedAgent],
        llm,
        router
    ):
        self.agents = {a.name: a for a in agents}
        self.llm = llm
        self.router = router

    def retrieve(self, query: str) -> List[str]:
        """Orchestrate retrieval across agents."""
        # Step 1: Route query to determine which agents to use
        routing = self.router.route(query)
        selected_agents = self._select_agents(routing)

        # Step 2: Run agents in parallel
        results = self._run_agents_parallel(query, selected_agents)

        # Step 3: Aggregate and rank results
        aggregated = self._aggregate_results(query, results)

        return aggregated

    def _select_agents(self, routing) -> List[SpecializedAgent]:
        """Select agents based on routing decision."""
        agent_mapping = {
            "vectorstore": "vector_agent",
            "web_search": "web_agent",
            "api": "api_agent"
        }
        agent_name = agent_mapping.get(routing.datasource)
        if agent_name and agent_name in self.agents:
            return [self.agents[agent_name]]
        return list(self.agents.values())  # Use all if unsure

    def _run_agents_parallel(
        self,
        query: str,
        agents: List[SpecializedAgent]
    ) -> List[AgentResult]:
        """Run multiple agents in parallel."""
        results = []
        with ThreadPoolExecutor(max_workers=len(agents)) as executor:
            futures = {
                executor.submit(agent.retrieve, query): agent
                for agent in agents
            }
            for future in as_completed(futures, timeout=10):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    agent = futures[future]
                    print(f"Agent {agent.name} failed: {e}")
        return results

    def _aggregate_results(
        self,
        query: str,
        results: List[AgentResult]
    ) -> List[str]:
        """Aggregate and rank results from all agents."""
        all_docs = []
        for result in results:
            for doc in result.documents:
                all_docs.append({
                    "content": doc,
                    "confidence": result.confidence,
                    "source": result.agent_name
                })

        # Sort by confidence and deduplicate
        all_docs.sort(key=lambda x: x["confidence"], reverse=True)
        seen = set()
        unique_docs = []
        for doc in all_docs:
            content_hash = hash(doc["content"][:100])
            if content_hash not in seen:
                seen.add(content_hash)
                unique_docs.append(doc["content"])

        return unique_docs[:10]

    def answer(self, query: str) -> str:
        """Full answer pipeline."""
        documents = self.retrieve(query)
        context = "\n\n".join(documents)
        return self.llm.invoke(
            f"Context:\n{context}\n\nQuestion: {query}\n\nAnswer:"
        )
```

## 8. Response Verifier with Grounding Check

```python
"""
Response verifier that checks answer grounding in sources.
"""
from pydantic import BaseModel, Field
from typing import List, Literal


class VerificationResult(BaseModel):
    """Result of answer verification."""
    is_grounded: bool
    confidence: float = Field(ge=0, le=1)
    unsupported_claims: List[str]
    suggested_corrections: List[str]
    verified_answer: str


class ResponseVerifier:
    """Verifies that generated answers are grounded in source documents."""

    def __init__(self, llm):
        self.llm = llm.with_structured_output(VerificationResult)
        self.prompt = """You are a fact-checker. Verify the answer is grounded in context.

For each claim in the answer:
1. Check if it's supported by the context
2. Flag unsupported claims
3. Suggest corrections if needed

Context:
{context}

Answer to verify:
{answer}

Return verification result."""

    def verify(
        self,
        answer: str,
        context: List[str]
    ) -> VerificationResult:
        """Verify answer against source context."""
        return self.llm.invoke(
            self.prompt.format(
                context="\n\n".join(context),
                answer=answer
            )
        )

    def verify_and_correct(
        self,
        answer: str,
        context: List[str],
        max_attempts: int = 2
    ) -> str:
        """Verify and iteratively correct answer."""
        for attempt in range(max_attempts):
            result = self.verify(answer, context)

            if result.is_grounded and result.confidence >= 0.8:
                return result.verified_answer

            # Use verified answer for next iteration
            answer = result.verified_answer

        return answer
```
