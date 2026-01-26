# Agentic RAG (RAG 2.0)

> Agent-driven retrieval with query routing, self-correction, and iterative refinement.

## Overview

Agentic RAG transcends traditional RAG by embedding autonomous AI agents into the retrieval pipeline. These agents leverage reflection, planning, tool use, and multi-agent collaboration to dynamically manage retrieval strategies and iteratively refine contextual understanding.

## Traditional RAG vs Agentic RAG

| Aspect | Traditional RAG | Agentic RAG |
|--------|-----------------|-------------|
| Retrieval | Single-shot, fixed | Multi-hop, dynamic |
| Pipeline | Static, sequential | Adaptive, conditional |
| Self-correction | None | Iterative refinement |
| Query handling | Pass-through | Routing, rewriting |
| Context validation | None | Relevance grading |
| Tool access | Vector search only | Multiple tools, APIs |
| Reasoning | Minimal | Planning, reflection |

## Core Agentic Patterns

### 1. Reflection

Agents iteratively evaluate and refine outputs through self-feedback mechanisms to identify errors and inconsistencies.

```
Query → Generate → Self-Critique → Refine → Validate → Output
```

### 2. Planning

Decompose complex tasks into manageable subtasks, supporting multi-hop reasoning.

```
Complex Query → Decompose → Sub-queries → Retrieve Each → Synthesize
```

### 3. Tool Use

Extend capabilities by interacting with external tools, APIs, and computational resources.

```
Query → Tool Selection → Execute Tool → Validate Result → Continue/Retry
```

### 4. Multi-Agent Collaboration

Distribute specialized tasks across multiple agents that communicate and share intermediate results.

```
Query → Orchestrator → [Agent A, Agent B, Agent C] → Aggregate → Output
```

## System Architectures

### Single-Agent Router

Centralized agent manages retrieval across multiple knowledge sources.

```
                    ┌─────────────────┐
                    │   Router Agent  │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│  Vector Search  │ │   Web Search    │ │      APIs       │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

**Best for:** Well-defined tasks, limited integration requirements

### Multi-Agent Systems

Specialized agents handle distinct retrieval types in parallel.

```
                    ┌─────────────────┐
                    │   Orchestrator  │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ Knowledge Agent │ │   Web Agent     │ │   API Agent     │
└────────┬────────┘ └────────┬────────┘ └────────┬────────┘
         ▼                   ▼                   ▼
   Vector DBs          Web Search            External APIs
```

**Best for:** Complex queries, multiple specialized data sources

### Corrective RAG (CRAG)

Self-correcting system with specialized agents.

```
Query → Retrieve → Grade Relevance → [Sufficient? → Generate]
                                   → [Insufficient? → Rewrite Query → Re-retrieve]
                                   → [Ambiguous? → Web Search → Augment]
```

**Agents:**
1. **Context Retrieval Agent** - Initial document retrieval
2. **Relevance Evaluation Agent** - Grade document relevance
3. **Query Refinement Agent** - Rewrite failed queries
4. **External Knowledge Agent** - Web search fallback
5. **Response Synthesis Agent** - Final answer generation

### Adaptive RAG

Classifier assesses query complexity and selects appropriate strategy.

| Query Complexity | Strategy |
|------------------|----------|
| Simple/Factual | Direct LLM response (no retrieval) |
| Moderate | Single-step retrieval |
| Complex | Multi-step reasoning with iterative retrieval |

### Graph-Based RAG

Combines knowledge graphs with document retrieval.

- **Agent-G:** Modular retriever banks with critic modules
- **GeAR:** Graph expansion with autonomous strategy selection

## Agentic RAG Loop

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   Query → Think → Route → Retrieve → Grade                  │
│                                        │                    │
│              ┌─────────────────────────┼─────────────────┐  │
│              │                         ▼                 │  │
│              │           ┌─────────────────────┐         │  │
│              │           │   Sufficient?       │         │  │
│              │           └──────────┬──────────┘         │  │
│              │                      │                    │  │
│              │         Yes ─────────┴─────────── No      │  │
│              │          │                        │       │  │
│              │          ▼                        ▼       │  │
│              │    Generate Answer         Refine Query   │  │
│              │          │                        │       │  │
│              │          ▼                        │       │  │
│              │       Verify                      │       │  │
│              │          │                        │       │  │
│              │          ▼                        │       │  │
│              │       Output                 Loop Back ───┘  │
│              │                                              │
│              └──────────────────────────────────────────────┘
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Key Components

### Query Router

Routes queries to appropriate retrieval sources based on query type.

| Query Type | Route To |
|------------|----------|
| Domain-specific | Vector store |
| Current events | Web search |
| Calculations | Calculator tool |
| General knowledge | Direct LLM response |
| Personal data | API (email, calendar) |

### Document Grader

Evaluates retrieved document relevance before generation.

| Score | Action |
|-------|--------|
| Relevant | Include in context |
| Irrelevant | Discard, trigger re-retrieval |
| Partial | Include with lower weight |

### Query Rewriter

Reformulates queries when initial retrieval fails.

**Strategies:**
- Add synonyms or related terms
- Adjust specificity (broaden/narrow)
- Rephrase for target content type
- Decompose into sub-queries

### Response Verifier

Validates generated answers against source documents.

**Checks:**
- Factual grounding in sources
- Hallucination detection
- Completeness of answer
- Contradiction detection

## Use Cases

| Domain | Application |
|--------|-------------|
| Financial Analysis | Multi-source research, compliance checking |
| Medical Research | Literature synthesis, clinical guidelines |
| Legal Review | Contract analysis, case law research |
| Customer Support | Multi-system query resolution |
| Research | Academic paper synthesis |

## Limitations and Considerations

| Challenge | Mitigation |
|-----------|------------|
| Added latency | Parallel retrieval, caching |
| Unreliability | Robust failure handling, fallbacks |
| Coordination overhead | Clear agent responsibilities |
| Cost | Token optimization, adaptive complexity |

## Files in This Folder

| File | Purpose |
|------|---------|
| [README.md](README.md) | This overview |
| [checklist.md](checklist.md) | Implementation checklist |
| [examples.md](examples.md) | Code examples |
| [templates.md](templates.md) | Reusable templates |
| [llm-prompts.md](llm-prompts.md) | Prompts for agents |

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [faion-rag-engineer](../../faion-rag-engineer/CLAUDE.md) | Base RAG patterns |
| [faion-ai-agents](../../faion-ai-agents/CLAUDE.md) | Agent architectures |
| [faion-llm-integration](../../faion-llm-integration/CLAUDE.md) | LLM APIs, function calling |

## Sources

- [Agentic RAG Survey (arXiv)](https://arxiv.org/abs/2501.09136)
- [Weaviate: What is Agentic RAG](https://weaviate.io/blog/what-is-agentic-rag)
- [LlamaIndex: Agentic Retrieval](https://www.llamaindex.ai/blog/rag-is-dead-long-live-agentic-retrieval)
- [NVIDIA: Traditional RAG vs Agentic RAG](https://developer.nvidia.com/blog/traditional-rag-vs-agentic-rag-why-ai-agents-need-dynamic-knowledge-to-get-smarter/)
- [Comprehensive Agentic RAG Workflow](https://sajalsharma.com/posts/comprehensive-agentic-rag/)
