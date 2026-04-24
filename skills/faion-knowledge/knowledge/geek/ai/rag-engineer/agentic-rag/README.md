---
id: agentic-rag
name: "Agentic RAG (RAG 2.0)"
domain: ML
skill: faion-ml-engineer
category: "best-practices-2026"
---

# Agentic RAG (RAG 2.0)

## Overview

Traditional RAG performs single retrieval with fixed pipeline. Agentic RAG uses LLM agents for iterative retrieval, self-correction, and reasoning.

**Key Innovation:** LLM decides what to retrieve, when to stop, and how to refine queries based on retrieved context.

## Traditional vs Agentic RAG

| Aspect | Traditional RAG | Agentic RAG |
|--------|----------------|-------------|
| **Retrieval** | Single pass | Multi-hop, iterative |
| **Pipeline** | Fixed sequence | Dynamic, adaptive |
| **Correction** | None | Self-correction loops |
| **Context** | Stuff all results | Selective retrieval |
| **Reasoning** | Limited | Tool use, planning |
| **Query** | Static | Refined based on results |

## Agentic RAG Architecture

```
User Query
    ↓
[Planning Agent]
    ↓
Decompose into sub-queries
    ↓
[Retrieval Agent] ← Iterative loop
    ↓              ↑
Retrieve chunks    |
    ↓              |
[Evaluation Agent] |
    ↓              |
Sufficient? -------┘ (No → refine query)
    ↓ Yes
[Generation Agent]
    ↓
Generate answer
    ↓
[Verification Agent]
    ↓
Verify with sources → Final answer
```

## Core Patterns

### 1. Iterative Retrieval

```python
from typing import List, Dict
import openai

class IterativeRetriever:
    """Multi-hop retrieval with LLM-guided query refinement."""

    def __init__(self, vector_store, max_iterations: int = 3):
        self.vector_store = vector_store
        self.max_iterations = max_iterations

    def retrieve(self, query: str) -> List[Dict]:
        """Iteratively retrieve until sufficient context."""
        context = []
        current_query = query

        for i in range(self.max_iterations):
            # Retrieve chunks
            chunks = self.vector_store.search(current_query, k=5)
            context.extend(chunks)

            # Check sufficiency
            if self._is_sufficient(query, context):
                break

            # Refine query based on gaps
            current_query = self._refine_query(query, context)

        return context

    def _is_sufficient(self, original_query: str, context: List[Dict]) -> bool:
        """LLM evaluates if context is sufficient."""
        prompt = f"""
Query: {original_query}

Retrieved context:
{self._format_context(context)}

Is this context sufficient to answer the query?
Answer YES or NO with brief reason.
"""
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        answer = response.choices[0].message.content
        return answer.strip().upper().startswith("YES")

    def _refine_query(self, original_query: str, context: List[Dict]) -> str:
        """Generate refined query to fill gaps."""
        prompt = f"""
Original query: {original_query}

Context retrieved so far:
{self._format_context(context)}

What information is still missing? Generate a refined search query
to retrieve the missing information. Return ONLY the query.
"""
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        return response.choices[0].message.content.strip()

    def _format_context(self, context: List[Dict]) -> str:
        return "\n\n".join([c["text"][:200] for c in context])
```

### 2. Query Decomposition

```python
class QueryDecomposer:
    """Break complex queries into sub-queries."""

    def decompose(self, query: str) -> List[str]:
        """Decompose into atomic sub-queries."""
        prompt = f"""
Decompose this complex query into 2-4 simpler sub-queries that can
be answered independently:

Query: {query}

Return sub-queries as a JSON array of strings.
"""
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0
        )

        import json
        result = json.loads(response.choices[0].message.content)
        return result.get("sub_queries", [query])

    def retrieve_for_subqueries(
        self,
        sub_queries: List[str],
        vector_store
    ) -> Dict[str, List[Dict]]:
        """Retrieve context for each sub-query."""
        results = {}
        for sq in sub_queries:
            results[sq] = vector_store.search(sq, k=5)
        return results
```

### 3. Self-Correction Loop

```python
class SelfCorrectingRAG:
    """RAG with answer verification and correction."""

    def __init__(self, vector_store, max_corrections: int = 2):
        self.vector_store = vector_store
        self.max_corrections = max_corrections

    def answer(self, query: str) -> Dict:
        """Generate answer with self-correction."""
        # Initial retrieval
        context = self.vector_store.search(query, k=10)

        for attempt in range(self.max_corrections + 1):
            # Generate answer
            answer = self._generate(query, context)

            # Verify answer
            is_valid, feedback = self._verify(query, answer, context)

            if is_valid:
                return {
                    "answer": answer,
                    "attempts": attempt + 1,
                    "verified": True
                }

            # Retrieve additional context based on feedback
            additional = self.vector_store.search(feedback, k=5)
            context.extend(additional)

        return {
            "answer": answer,
            "attempts": self.max_corrections + 1,
            "verified": False
        }

    def _generate(self, query: str, context: List[Dict]) -> str:
        """Generate answer from context."""
        context_text = "\n\n".join([c["text"] for c in context])

        prompt = f"""
Context:
{context_text}

Query: {query}

Answer based ONLY on the context above. If information is missing, say so.
"""
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        return response.choices[0].message.content

    def _verify(self, query: str, answer: str, context: List[Dict]) -> tuple:
        """Verify answer quality and identify gaps."""
        context_text = "\n\n".join([c["text"] for c in context])

        prompt = f"""
Query: {query}
Answer: {answer}
Context: {context_text}

Verify:
1. Is answer supported by context?
2. Are there factual errors?
3. Is information missing?

Return JSON:
{{"valid": true/false, "feedback": "what to search for if invalid"}}
"""
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0
        )

        import json
        result = json.loads(response.choices[0].message.content)
        return result.get("valid", False), result.get("feedback", "")
```

### 4. Tool-Using Agent

```python
from typing import Callable, List, Dict

class ToolUsingRAG:
    """Agentic RAG with tool selection."""

    def __init__(self):
        self.tools = {
            "vector_search": self._vector_search,
            "keyword_search": self._keyword_search,
            "sql_query": self._sql_query,
            "web_search": self._web_search,
        }

    def answer(self, query: str) -> str:
        """Answer query using appropriate tools."""
        context = []

        for _ in range(3):  # Max 3 tool calls
            # Select tool
            tool_name = self._select_tool(query, context)

            if tool_name == "generate_answer":
                break

            # Execute tool
            result = self.tools[tool_name](query)
            context.append({
                "tool": tool_name,
                "result": result
            })

        # Generate final answer
        return self._generate_final(query, context)

    def _select_tool(self, query: str, context: List[Dict]) -> str:
        """LLM selects next tool to use."""
        tools_desc = """
Available tools:
- vector_search: Semantic search in document database
- keyword_search: Exact keyword matching
- sql_query: Query structured data
- web_search: Search external web
- generate_answer: Generate final answer (when sufficient info)
"""

        context_summary = "\n".join([
            f"{c['tool']}: {str(c['result'])[:100]}" for c in context
        ])

        prompt = f"""
{tools_desc}

Query: {query}
Information gathered: {context_summary}

Which tool should be used next? Return ONLY the tool name.
"""
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        return response.choices[0].message.content.strip()

    def _vector_search(self, query: str) -> List[Dict]:
        # Implementation
        pass

    def _keyword_search(self, query: str) -> List[Dict]:
        # Implementation
        pass

    def _sql_query(self, query: str) -> List[Dict]:
        # Implementation
        pass

    def _web_search(self, query: str) -> List[Dict]:
        # Implementation
        pass

    def _generate_final(self, query: str, context: List[Dict]) -> str:
        # Implementation
        pass
```

## LangGraph Implementation

```python
from langgraph.graph import Graph, END
from typing import TypedDict

class AgentState(TypedDict):
    query: str
    sub_queries: List[str]
    context: List[Dict]
    answer: str
    verified: bool

def plan(state: AgentState) -> AgentState:
    """Decompose query."""
    decomposer = QueryDecomposer()
    state["sub_queries"] = decomposer.decompose(state["query"])
    return state

def retrieve(state: AgentState) -> AgentState:
    """Retrieve for all sub-queries."""
    all_context = []
    for sq in state["sub_queries"]:
        chunks = vector_store.search(sq, k=5)
        all_context.extend(chunks)
    state["context"] = all_context
    return state

def generate(state: AgentState) -> AgentState:
    """Generate answer."""
    # Generate answer logic
    state["answer"] = "..."
    return state

def verify(state: AgentState) -> AgentState:
    """Verify answer quality."""
    # Verification logic
    state["verified"] = True
    return state

def should_refine(state: AgentState) -> str:
    """Route: refine or finish."""
    return "finish" if state["verified"] else "refine"

# Build graph
workflow = Graph()
workflow.add_node("plan", plan)
workflow.add_node("retrieve", retrieve)
workflow.add_node("generate", generate)
workflow.add_node("verify", verify)

workflow.set_entry_point("plan")
workflow.add_edge("plan", "retrieve")
workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", "verify")
workflow.add_conditional_edges(
    "verify",
    should_refine,
    {"finish": END, "refine": "plan"}
)

app = workflow.compile()
```

## Use Cases

| Use Case | Why Agentic RAG | Pattern |
|----------|----------------|---------|
| **Multi-hop QA** | Requires combining info from multiple sources | Query decomposition |
| **Research synthesis** | Needs iterative exploration | Iterative retrieval |
| **Fact-checking** | Requires verification against sources | Self-correction |
| **Complex analytics** | Needs structured + unstructured data | Tool-using agent |
| **Legal compliance** | Requires exhaustive source checking | Verification loops |

## Best Practices

1. **Limit iterations** - Cap at 3-5 to control latency/cost
2. **Cache aggressively** - Cache sub-query results
3. **Use fast models** - gpt-4o-mini for routing, gpt-4o for final generation
4. **Log decisions** - Track tool selections for debugging
5. **Set timeouts** - Prevent infinite loops

## Performance Metrics

| Metric | Traditional RAG | Agentic RAG |
|--------|----------------|-------------|
| **Accuracy** | 65-75% | 80-90% |
| **Latency** | 1-2s | 3-8s |
| **Cost** | $0.001/query | $0.005-0.01/query |
| **Hallucination** | 15-20% | 5-10% |

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Analyze and assess | sonnet | Evaluation and planning |
| Execute implementation | haiku | Apply established patterns |
| Review and validate | sonnet | Quality assurance |
| Strategic decision | opus | Novel scenarios |
| Optimize and refine | haiku | Performance tuning |
| Document approach | haiku | Create documentation |

## Sources

- [LangGraph Agentic RAG Tutorial](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/)
- [OpenAI Cookbook: Advanced RAG](https://cookbook.openai.com/examples/how_to_build_an_agent)
- [Microsoft GraphRAG](https://github.com/microsoft/graphrag)
- [LlamaIndex Agentic Patterns](https://docs.llamaindex.ai/en/stable/examples/agent/agentic_rag/)
- [Anthropic: Tool Use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
