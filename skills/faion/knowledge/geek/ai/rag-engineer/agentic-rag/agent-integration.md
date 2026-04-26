# Agent Integration — Agentic RAG (RAG 2.0)

## When to use
- Questions require combining information from multiple disjoint documents (multi-hop QA).
- A single retrieval pass consistently returns insufficient or partially relevant context.
- The task involves research synthesis: explore → evaluate → refine → conclude.
- Fact-checking or compliance verification where exhaustive source coverage is required.
- Structured data (SQL/tables) must be combined with unstructured document retrieval.

## When NOT to use
- Single-turn factual lookup where standard RAG (one retrieval pass) suffices — agentic loop adds 3–5x latency and cost.
- Latency-critical user-facing queries (< 2s SLA) — agentic RAG typically takes 3–10s.
- When the corpus is well-structured and coverage is high; iterative retrieval gains are marginal.
- Untrusted or adversarial input corpora — iterative retrieval loops can be exploited via prompt injection in documents.

## Where it fails / limitations
- Iteration loops can diverge: the sufficiency check LLM may never say "YES", burning `max_iterations` budget.
- Query refinement can drift from the original intent after 2+ iterations — the refined query answers a different question.
- Cost scales super-linearly with iterations: 3 iterations = 3–5x the cost of single-pass RAG.
- Self-correction loops can amplify hallucinations if the verification LLM uses the same model as the generator.
- LangGraph orchestration adds dependency complexity; state schema bugs cause silent data loss between nodes.
- Sub-query decomposition produces overlapping sub-queries, leading to redundant context and inflated token usage.

## Agentic workflow
The planner subagent decomposes the query into 2–4 atomic sub-queries. The retriever subagent executes each sub-query against the vector store (in parallel where sub-queries are independent). A sufficiency judge evaluates whether the combined context answers the original question; if not, it generates a gap-filling refined query and triggers another retrieval round (max 3 rounds). The generator subagent synthesizes the final answer. A verifier subagent checks faithfulness against source chunks and flags ungrounded claims.

### Recommended subagents
- `query-planner` — Decomposes complex query into atomic sub-queries; returns JSON array.
- `iterative-retriever` — Retrieves, evaluates sufficiency, and refines query in a bounded loop.
- `rag-generator` — Synthesizes grounded answer from multi-hop context.
- `faithfulness-verifier` — Checks each claim in the answer against retrieved sources; flags hallucinations.

### Prompt pattern
```python
# Sufficiency check prompt (iterative-retriever subagent)
SUFFICIENCY_PROMPT = """
Original query: {original_query}

Retrieved context so far:
{context_summary}

Can this context fully answer the original query?
Respond with JSON: {{"sufficient": true/false, "missing": "description of what is missing"}}
"""

# Gap-filling query generation
REFINE_PROMPT = """
Original query: {original_query}
What is missing: {missing_description}

Generate a precise search query to retrieve the missing information.
Return only the query string.
"""
```

LangGraph wiring:
```python
workflow.add_conditional_edges(
    "verify",
    lambda s: "finish" if s["verified"] or s["iterations"] >= 3 else "plan",
    {"finish": END, "plan": "plan"}
)
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `langgraph` | Stateful agent graph for agentic RAG flows | `pip install langgraph` / langchain-ai.github.io/langgraph |
| `llama-index` | Agentic patterns: `ReActAgent`, `FunctionCallingAgent` | `pip install llama-index` / docs.llamaindex.ai |
| `ragas` | Evaluate agentic RAG: context recall, faithfulness | `pip install ragas` / docs.ragas.io |
| `dspy` | Self-optimizing RAG pipelines with teleprompters | `pip install dspy-ai` / dspy.ai |
| `openai` | Function calling for tool-using RAG agents | `pip install openai` / platform.openai.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| LangGraph Cloud | SaaS | Yes | Hosted stateful agentic graph execution |
| LlamaCloud | SaaS | Yes | Managed agentic parsing + multi-hop retrieval |
| Microsoft GraphRAG | OSS | Partial | Knowledge graph-based agentic RAG; complex setup |
| Cohere Rerank | SaaS | Yes | Reranking between iterative retrieval passes |
| Anthropic Messages API | SaaS | Yes | Best-in-class for agentic reasoning; use Sonnet for routing, Opus for synthesis |

## Templates & scripts
See `templates.md` for iterative retriever, LangGraph agentic RAG, and tool-using RAG templates.

Bounded iterative retrieval loop (under 40 lines):
```python
import json
import anthropic

client = anthropic.Anthropic()

def iterative_retrieve(query: str, vector_store, max_iter: int = 3) -> list:
    context = []
    current_query = query
    for i in range(max_iter):
        chunks = vector_store.search(current_query, k=5)
        context.extend(chunks)
        check = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=256,
            messages=[{"role": "user", "content":
                f"Query: {query}\nContext: {[c['text'][:200] for c in context]}\n"
                "Is context sufficient? JSON: {\"sufficient\": bool, \"missing\": str}"}]
        )
        result = json.loads(check.content[0].text)
        if result["sufficient"]:
            break
        refine = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=128,
            messages=[{"role": "user", "content":
                f"Missing: {result['missing']}\nGenerate search query. Return query only."}]
        )
        current_query = refine.content[0].text.strip()
    return context
```

## Best practices
- Cap iterations at 3; beyond that, log the failure and route to human review rather than continuing to burn budget.
- Use a cheaper model (Haiku or Sonnet) for sufficiency checks and query refinement; reserve Opus for final synthesis.
- Deduplicate context chunks between iterations using chunk IDs — the same chunk can appear in multiple retrieval passes.
- Track sub-query coverage: each sub-query should retrieve at least 1 high-confidence chunk; if not, flag the sub-query for query expansion.
- Cache sub-query results within a single agentic run — the same sub-query may recur across iterations.
- Run planning and independent sub-query retrievals in parallel to reduce latency.
- Log the full iteration trace (queries, sufficiency decisions, context state) for offline debugging.

## AI-agent gotchas
- Prompt injection via document content: an adversarial document can override the sufficiency prompt and claim context is sufficient when it is not — sanitize retrieved chunks before passing to judge models.
- The faithfulness verifier must use a different model (or at minimum a different temperature/run) from the generator — same model tends to confirm its own outputs.
- LangGraph state is passed by reference in some implementations; mutating state in a node can corrupt parallel branches.
- Iteration count is not the same as round-trip count — one iteration may spawn multiple parallel retrieval calls; bill accordingly.
- Human-in-loop checkpoint: when `faithfulness_verifier` returns > 2 ungrounded claims, do not surface the answer — either retrieve more context or escalate to a human.
- Query drift detection: compare the embedding cosine similarity between the original query and the refined query; if < 0.7, the refinement has drifted — reset to the original.

## References
- https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/ — LangGraph Agentic RAG tutorial
- https://docs.llamaindex.ai/en/stable/examples/agent/agentic_rag/ — LlamaIndex Agentic RAG patterns
- https://github.com/microsoft/graphrag — Microsoft GraphRAG
- https://docs.anthropic.com/en/docs/build-with-claude/tool-use — Anthropic tool use for agentic patterns
- https://arxiv.org/abs/2312.10997 — RAFT: Adapting Language Model to Domain Specific RAG
