# RAG Pipeline

## Summary

**One-sentence:** Builds an end-to-end RAG pipeline (ingest → retrieve → rerank → generate) with cited answers and a launch-gate at MRR&gt;0.7 and faithfulness&gt;0.9.

**One-paragraph:** A Retrieval-Augmented Generation pipeline ingests documents (load → chunk → embed → store), retrieves relevant chunks for a query (embed → vector search → rerank), and generates a grounded answer with source citations. Key invariants: chunk quality bounds retrieval quality; hybrid search is the default; reranking is required for production accuracy; evaluate with MRR&gt;0.7 and faithfulness&gt;0.9 before launch.

**Ефективно для:** команд, які будують AI-помічника на приватному/часто-оновлюваному корпусі і потребують грунтованих відповідей із цитатами.

## Applies If (ALL must hold)

- Agent must answer questions grounded in a private or frequently-updated corpus.
- Hallucination on domain-specific topics is unacceptable.
- Knowledge assistant over PDFs / docs / wikis / code.
- Citation / source attribution is required for compliance or user trust.

## Skip If (ANY kills it)

- Document set is tiny (&lt;50 chunks) and fits in context — stuff the full context instead.
- Questions are purely general knowledge — RAG adds latency with no accuracy gain.
- Data is real-time (stock prices, live APIs) — use live tool calls.
- Latency budget &lt; 200ms — embed + retrieve overhead exceeds SLA.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Document corpus | PDF / md / txt / html | ingestion job |
| Vector DB credentials | env | infra |
| Embedding model | provider | embedding-models |
| Reranker | cross-encoder or API | reranking-models |
| Eval test set | JSONL {query, expected_ids} | rag-eval-test-set-generation |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `geek/ai/rag-engineer/rag-architecture` | Architecture decisions feed this build. |
| `geek/ai/rag-engineer/chunking-basics` | Chunking quality bounds retrieval. |
| `geek/ai/rag-engineer/vector-database-setup` | Backend choice. |
| `geek/ai/rag-engineer/reranking-two-stage` | Production reranker. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: chunk + metadata, hybrid default, rerank top-20→5, context order, answer-only-from-context, MRR/faithfulness gate | ~1100 |
| `content/02-output-contract.xml` | essential | JSON schema for one RAG answer (text + citations[] + faithfulness + metrics) | ~800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: lost-in-the-middle, hallucinated citations, no eval gate, post-index metadata add | ~800 |
| `content/04-procedure.xml` | medium | 6-step build procedure | ~900 |
| `content/06-decision-tree.xml` | essential | Tree picking RAG vs context-stuffing vs agentic-RAG | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Chunk + embed corpus | haiku | Mechanical batch. |
| Generate cited answer | sonnet | Quality grounding. |
| Faithfulness scoring | sonnet | Judge-style eval. |
| Architecture decisions | opus | Trade-offs. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rag-pipeline.py.tmpl` | End-to-end skeleton: ingest, retrieve, rerank, generate. |
| `templates/answer-prompt.txt` | "Answer ONLY from the provided context" system prompt with citation format. |
| `templates/_smoke-test.py` | Minimal end-to-end smoke test. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

- [[rag-architecture]]
- [[rag-implementation]]
- [[rag-eval-strategy]]
- [[reranking-two-stage]]

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` picks the right approach: root question — "Does the corpus fit a single context window AND token-cost is acceptable?". Branches lead to context-stuffing (small corpus), standard RAG (default), or agentic-RAG (multi-hop questions). Each leaf references a core rule.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/rag-pipeline.py.tmpl`

```python
from typing import List, Dict


def ingest(corpus_path: str, chunk_size: int = 1024, overlap: int = 200) -> List[Dict]:
    # TODO replace with unstructured or llama-index loader
    chunks: List[Dict] = []
    return chunks


def embed_and_store(chunks: List[Dict], vector_store) -> None:
    for batch in _batched(chunks, 256):
        vector_store.upsert(batch)


def retrieve_hybrid(query: str, vector_store, k: int = 20) -> List[Dict]:
    return vector_store.hybrid_search(query, k=k)


def rerank(query: str, candidates: List[Dict], reranker, top_k: int = 5) -> List[Dict]:
    return reranker.rerank(query, candidates, top_k=top_k)


def generate(query: str, chunks: List[Dict], llm, prompt_template: str) -> Dict:
    # Highest-score-first ordering enforced (rule r4)
    context = "\n\n".join(
        f"[{c['chunk_id']} | {c['source']} p.{c.get('page', '?')}]\n{c['text']}" for c in chunks
    )
    out = llm.complete(prompt_template.format(query=query, context=context))
    return {"answer": out["text"], "raw_citations": out.get("citations", [])}


def validate_citations(raw_citations: List[Dict], chunks: List[Dict]) -> List[Dict]:
    valid_ids = {c["chunk_id"] for c in chunks}
    validated = []
    for c in raw_citations:
        validated.append({**c, "validated": c.get("chunk_id") in valid_ids})
    return validated


def faithfulness(answer: str, chunks: List[Dict], judge) -> float:
    return float(judge.faithfulness(answer, chunks))


def run(query: str, vector_store, reranker, llm, judge, prompt_template: str) -> Dict:
    cands = retrieve_hybrid(query, vector_store, k=20)
    top = rerank(query, cands, reranker, top_k=5)
    g = generate(query, top, llm, prompt_template)
    cits = validate_citations(g["raw_citations"], top)
    score = faithfulness(g["answer"], top, judge)
    return {
        "query": query,
        "answer": g["answer"],
        "citations": cits,
        "retrieval": {"top_k": 20, "rerank_top_k": 5, "latency_ms": 0.0},
        "faithfulness": score,
        "fallback_to_no_answer": score < 0.5,
    }


def _batched(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i : i + n]
```

### `templates/answer-prompt.txt`

```text
You are a careful retrieval-augmented assistant.

Rules:
1. Answer ONLY from the provided context blocks. If the context does not contain the answer, reply exactly: "I don't have enough information in the provided sources to answer that."
2. Cite every factual claim with [Source: filename, page N]. The filename must appear in the context.
3. Do not introduce facts that are not in the context, even if they are widely known.
4. Be concise. Two-to-five sentences unless the question explicitly asks for more detail.

Question:
{query}

Context (ranked, highest relevance first):
{context}

Answer:
```

### `templates/_smoke-test.py`

```python
from rag_pipeline import run  # rename .tmpl -> .py


class FakeVS:
    def hybrid_search(self, q, k):
        return [{"chunk_id": f"c{i}", "source": "doc.md", "page": i, "text": f"chunk {i} about {q}", "score": 1 - 0.1 * i} for i in range(k)]


class FakeRerank:
    def rerank(self, q, c, top_k):
        return c[:top_k]


class FakeLLM:
    def complete(self, prompt):
        return {"text": "Answer [Source: doc.md, page 0].", "citations": [{"source": "doc.md", "page": 0, "chunk_id": "c0"}]}


class FakeJudge:
    def faithfulness(self, a, c):
        return 0.95


if __name__ == "__main__":
    out = run("test", FakeVS(), FakeRerank(), FakeLLM(), FakeJudge(), "Q: {query}\nC: {context}")
    assert out["faithfulness"] > 0.9
    assert out["citations"][0]["validated"] is True
    print(out)
```
