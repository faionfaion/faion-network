# Agent Integration — Agentic RAG (RAG 2.0)

## When to use
- Queries require multi-hop reasoning across documents (e.g., "What is the CEO's policy on X, and how does it relate to the legal regulation Y?")
- Single-shot retrieval consistently fails for complex or ambiguous questions
- The knowledge base spans multiple heterogeneous sources (internal docs, web, APIs, databases)
- Self-correction is essential: the system must detect irrelevant retrievals and retry rather than hallucinating
- Complex domains (legal, medical, financial) where one retrieval miss produces costly wrong answers

## When NOT to use
- Simple factual Q&A with a single knowledge base and high recall — standard RAG is faster and cheaper
- Latency budget under 2 seconds — agentic loops with reflection add 2-10x more turns than static RAG
- The orchestration infrastructure does not exist yet — build standard RAG first, then layer agentic behavior on top
- Cost constraints are tight — multi-hop retrieval multiplies token usage per query (each agent turn = one LLM call)

## Where it fails / limitations
- Infinite loops: a poorly graded relevance check can cause the agent to retry indefinitely without converging
- Compounding errors: each query rewrite degrades from the original intent; after 3+ rewrites, the agent may be searching for something unrelated
- Latency is non-deterministic: 3-10 retrieval hops can take 5-30 seconds; users need a streaming progress indicator
- Coordination overhead: multi-agent architectures require robust message-passing and shared state — distributed failures are hard to debug
- Relevance grader hallucination: the grader LLM may incorrectly mark relevant documents as irrelevant, silently dropping good context
- Tool call failures in the retrieval loop are not automatically retried by the LLM — the orchestrator must implement retry logic

## Agentic workflow
An orchestrator agent receives the query and runs an adaptive decision: simple queries go straight to a single retrieval call; complex queries trigger decomposition into sub-queries. Each sub-query is sent to a retrieval subagent that fetches candidates, grades relevance, and returns `{chunks, relevance_scores}`. If a sub-query returns no relevant chunks, the query rewriter rewrites and retries (max 2 times). The orchestrator synthesizes all sub-answers into a final response, then the response verifier validates factual grounding before returning to the user.

### Recommended subagents
- `retrieval-grader` subagent — receives a query + document, outputs `{relevant: bool, score: float, reason: str}`
- `query-rewriter` subagent — receives a failed query + previous results, outputs a reformulated query string
- `response-verifier` subagent — checks that every factual claim in the final answer cites at least one retrieved chunk

### Prompt pattern
```
# Relevance grader prompt
You are a relevance grader. Given the query and document below, output JSON:
{"relevant": true|false, "score": 0.0-1.0, "reason": "<one sentence>"}
Grade strictly: only mark relevant if the document directly addresses the query.

Query: {query}
Document: {document_text}
```

```python
# CRAG loop skeleton
def corrective_rag(query: str, max_retries: int = 2) -> str:
    for attempt in range(max_retries + 1):
        chunks = retriever.retrieve(query, top_k=10)
        relevant = [c for c in chunks if grader.grade(query, c).relevant]
        if len(relevant) >= 3:
            return synthesizer.generate(query, relevant)
        if attempt < max_retries:
            query = rewriter.rewrite(query, chunks)
    # Fallback: web search
    web_results = web_search(query)
    return synthesizer.generate(query, web_results)
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `llama-index` | AgentRunner, RouterQueryEngine, SubQuestionQueryEngine | `pip install llama-index` — [docs.llamaindex.ai](https://docs.llamaindex.ai/) |
| `langchain` | CRAG chains, LangGraph for stateful agentic RAG | `pip install langchain langgraph` |
| `langgraph` | Graph-based agent state machines | `pip install langgraph` — [langchain-ai.github.io/langgraph](https://langchain-ai.github.io/langgraph/) |
| `anthropic` | Claude API for agent reasoning steps | `pip install anthropic` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| LlamaIndex AgentRunner | OSS | Yes — Python | Built-in ReAct + tool-use loop for RAG |
| LangGraph | OSS | Yes — Python | State machine for CRAG/Adaptive RAG workflows |
| Weaviate | SaaS + OSS | Yes | Native hybrid search; multi-tenant; GraphQL API |
| Qdrant | SaaS + OSS | Yes | Fast; filterable; supports named collections per agent |
| Cohere Rerank | SaaS | Yes — REST | Reranking step in the grading phase |
| Tavily | SaaS | Yes — REST | Web search tool for fallback retrieval |
| Langfuse | SaaS + OSS | Yes | Trace multi-hop agent loops; see per-turn costs |

## Templates & scripts
See `templates.md` for full CRAG and Adaptive RAG pipeline templates.

Inline: Adaptive RAG complexity classifier (< 30 lines):

```python
import json
import anthropic

client = anthropic.Anthropic()

def classify_query_complexity(query: str) -> str:
    """Returns 'simple' | 'moderate' | 'complex'"""
    response = client.messages.create(
        model="claude-haiku-3-5-20241022",
        max_tokens=64,
        messages=[{
            "role": "user",
            "content": (
                f"Classify this query complexity as 'simple', 'moderate', or 'complex'. "
                f"Output JSON only: {{\"complexity\": \"...\"}}\nQuery: {query}"
            ),
        }],
    )
    return json.loads(response.content[0].text)["complexity"]
```

## Best practices
- Cap retries at 2 per sub-query — beyond 2 rewrites, precision drops; fall back to web search instead
- Use a cheap model (Haiku) for relevance grading and query rewriting; reserve Sonnet/Opus for final synthesis
- Implement parallel retrieval for independent sub-queries — fan out, wait for all results, then aggregate; reduces total latency by 50-70%
- Log every agent turn with: query, retrieved chunks, grading decision, and rewrite — essential for debugging where the pipeline diverges
- Set a hard token budget per agentic loop: if cumulative tokens exceed 50K, abort and return a partial answer rather than running indefinitely
- For multi-agent architectures, give each agent a strict contract (input schema + output schema) and validate at the boundary — message schema drift is the #1 source of silent multi-agent failures

## AI-agent gotchas
- Grader LLM also hallucinates: the relevance grader may mark a document relevant because it shares topic vocabulary, not because it answers the query — add a stricter "does this document directly answer the query?" check
- Infinite loop via rewriting toward the wrong target: if the rewriter changes the query semantics too aggressively, subsequent retrievals miss the original user intent entirely — keep the original query alongside the rewritten one and compare retrieved sets
- Human-in-loop checkpoint: for high-stakes domains (legal, medical), insert a human review step before the final synthesized answer is returned — the agent can surface top-3 candidate answers for expert selection
- State corruption in multi-agent coordination: if one agent crashes mid-loop and state is not persisted, the orchestrator may restart with partial context; always checkpoint agent state to durable storage between hops
- Response verifier is itself an LLM: it can fail to detect hallucinations if the hallucinated content is plausibly worded — treat verifier output as a probabilistic signal, not a guarantee

## References
- [Agentic RAG Survey (arXiv 2025)](https://arxiv.org/abs/2501.09136)
- [LlamaIndex: Agentic Retrieval](https://www.llamaindex.ai/blog/rag-is-dead-long-live-agentic-retrieval)
- [Weaviate: What is Agentic RAG](https://weaviate.io/blog/what-is-agentic-rag)
- [NVIDIA: Traditional RAG vs Agentic RAG](https://developer.nvidia.com/blog/traditional-rag-vs-agentic-rag-why-ai-agents-need-dynamic-knowledge-to-get-smarter/)
- [LangGraph documentation](https://langchain-ai.github.io/langgraph/)
- [Comprehensive Agentic RAG Workflow](https://sajalsharma.com/posts/comprehensive-agentic-rag/)
