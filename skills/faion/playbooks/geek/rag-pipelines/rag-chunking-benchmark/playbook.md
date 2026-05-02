---
name: rag-chunking-benchmark
description: Benchmark fixed-size, semantic, and recursive chunking on a 50-doc corpus to pick the best strategy by retrieval recall@5 and answer F1.
tier: geek
group: rag-pipelines
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a reproducible Python benchmark that ingests the same 50-document corpus through three chunking strategies — fixed 512-token windows, semantic sentence-boundary merging via `sentence-transformers`, and recursive character splitting via `langchain_text_splitters` — embeds all chunks into ChromaDB, runs a 30-question golden evaluation set, and prints a per-strategy score table of retrieval recall@5 and answer F1. The final decision rule selects the winning strategy automatically.

## Prerequisites

- Python 3.11+ with a virtual environment active.
- `pip install langchain-text-splitters langchain-community chromadb sentence-transformers openai tiktoken numpy` (or the project's `requirements.txt`).
- An OpenAI-compatible embedding API key (set `OPENAI_API_KEY` in your shell), or swap for `sentence-transformers` local embeddings — the benchmark supports both.
- A corpus of 50 `.txt` or `.md` documents in a folder `./corpus/`. The corpus may be your own domain docs; diversity (short paragraphs, long sections, tables as text) makes the benchmark meaningful.
- A golden evaluation set: `./golden_set.jsonl` — 30 lines, each `{"question": "...", "answer": "..."}`. You can bootstrap it with the generator in Step 2.
- Familiarity with ChromaDB collections and cosine similarity.

## Steps

1. Create the project scaffold:

```bash
mkdir rag-chunk-bench && cd rag-chunk-bench
mkdir corpus golden
touch benchmark.py scorer.py generate_golden.py
```

2. Generate a starter golden set from your corpus (skip if you have one already):

```python
# generate_golden.py
import json, pathlib, random, textwrap
from anthropic import Anthropic

client = Anthropic()
docs = list(pathlib.Path("corpus").glob("*.txt")) + list(pathlib.Path("corpus").glob("*.md"))
random.seed(42)
sample = random.sample(docs, min(15, len(docs)))

pairs = []
for doc in sample:
    text = doc.read_text()[:3000]
    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        messages=[{
            "role": "user",
            "content": (
                "Generate 2 factual Q&A pairs from the text below. "
                "Return JSON array: [{\"question\": ..., \"answer\": ...}]\n\n"
                f"{textwrap.shorten(text, 2000)}"
            ),
        }],
    )
    import json as _json
    try:
        pairs.extend(_json.loads(resp.content[0].text))
    except Exception:
        pass

pairs = pairs[:30]
with open("golden/golden_set.jsonl", "w") as f:
    for p in pairs:
        f.write(json.dumps(p) + "\n")
print(f"Wrote {len(pairs)} pairs to golden/golden_set.jsonl")
```

Run: `python generate_golden.py`

3. Write the three splitters in `benchmark.py`:

```python
# benchmark.py
from __future__ import annotations
import json, pathlib, os, re, textwrap
from dataclasses import dataclass
from typing import Literal

import chromadb
import numpy as np
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    TokenTextSplitter,
)
from sentence_transformers import SentenceTransformer

CORPUS_DIR = pathlib.Path("corpus")
GOLDEN_PATH = pathlib.Path("golden/golden_set.jsonl")
EMBED_MODEL = "text-embedding-3-small"
TOP_K = 5

StrategyName = Literal["fixed", "semantic", "recursive"]


def load_corpus() -> list[str]:
    docs = []
    for p in sorted(CORPUS_DIR.glob("*")):
        if p.suffix in {".txt", ".md"}:
            docs.append(p.read_text(encoding="utf-8"))
    assert docs, f"No documents found in {CORPUS_DIR}"
    return docs


def load_golden() -> list[dict]:
    pairs = [json.loads(l) for l in GOLDEN_PATH.read_text().splitlines() if l.strip()]
    assert pairs, "golden_set.jsonl is empty"
    return pairs


# --- Splitters ---

def fixed_chunks(docs: list[str]) -> list[str]:
    """512-token windows, 50-token overlap."""
    splitter = TokenTextSplitter(chunk_size=512, chunk_overlap=50)
    return splitter.split_text("\n\n".join(docs))


def semantic_chunks(docs: list[str], threshold: float = 0.85) -> list[str]:
    """Sentence-boundary merging: group consecutive sentences whose
    embedding cosine similarity stays above threshold."""
    model = SentenceTransformer("all-MiniLM-L6-v2")

    def _split_sentences(text: str) -> list[str]:
        return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]

    all_sentences = _split_sentences("\n\n".join(docs))
    if not all_sentences:
        return []

    embeddings = model.encode(all_sentences, batch_size=64, show_progress_bar=False)
    chunks, current = [], [all_sentences[0]]

    for i in range(1, len(all_sentences)):
        sim = float(np.dot(embeddings[i - 1], embeddings[i]) /
                    (np.linalg.norm(embeddings[i - 1]) * np.linalg.norm(embeddings[i]) + 1e-9))
        if sim >= threshold:
            current.append(all_sentences[i])
        else:
            chunks.append(" ".join(current))
            current = [all_sentences[i]]
    if current:
        chunks.append(" ".join(current))
    return chunks


def recursive_chunks(docs: list[str]) -> list[str]:
    """LangChain RecursiveCharacterTextSplitter: \\n\\n → \\n → sentence → word."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=120,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    return splitter.split_text("\n\n".join(docs))
```

4. Add the indexing + retrieval helpers to `benchmark.py`:

```python
def build_collection(name: str, chunks: list[str]) -> chromadb.Collection:
    ef = OpenAIEmbeddingFunction(
        api_key=os.environ["OPENAI_API_KEY"],
        model_name=EMBED_MODEL,
    )
    client = chromadb.Client()
    col = client.get_or_create_collection(name=name, embedding_function=ef)
    batch = 100
    for i in range(0, len(chunks), batch):
        sub = chunks[i : i + batch]
        col.add(
            documents=sub,
            ids=[f"{name}-{i + j}" for j in range(len(sub))],
        )
    return col


def retrieve(col: chromadb.Collection, question: str) -> list[str]:
    res = col.query(query_texts=[question], n_results=TOP_K)
    return res["documents"][0]
```

5. Add the scorer in `scorer.py`:

```python
# scorer.py
from __future__ import annotations
import re
from anthropic import Anthropic

_client = Anthropic()


def token_f1(prediction: str, reference: str) -> float:
    """Bag-of-words F1 between prediction and reference."""
    def _tokens(s: str) -> set[str]:
        return set(re.findall(r"\w+", s.lower()))

    pred_t, ref_t = _tokens(prediction), _tokens(reference)
    if not pred_t or not ref_t:
        return 0.0
    precision = len(pred_t & ref_t) / len(pred_t)
    recall = len(pred_t & ref_t) / len(ref_t)
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def answer_question(context_chunks: list[str], question: str) -> str:
    context = "\n\n---\n\n".join(context_chunks)
    resp = _client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=256,
        messages=[{
            "role": "user",
            "content": (
                f"Context:\n{context}\n\n"
                f"Question: {question}\n"
                "Answer concisely using only the context above."
            ),
        }],
    )
    return resp.content[0].text.strip()
```

6. Complete `benchmark.py` with the evaluation loop and decision rule:

```python
# (append to benchmark.py)
from scorer import answer_question, token_f1


@dataclass
class StrategyResult:
    name: str
    n_chunks: int
    recall_at_k: float
    answer_f1: float


def evaluate_strategy(
    name: StrategyName,
    chunks: list[str],
    golden: list[dict],
) -> StrategyResult:
    print(f"  Indexing {len(chunks)} chunks for '{name}'...")
    col = build_collection(name, chunks)

    recalls, f1s = [], []
    for item in golden:
        q, ref_ans = item["question"], item["answer"]
        retrieved = retrieve(col, q)

        # recall@5: does any retrieved chunk contain a meaningful token from the answer?
        ref_tokens = set(re.findall(r"\w+", ref_ans.lower()))
        hits = sum(
            1 for c in retrieved
            if len(ref_tokens & set(re.findall(r"\w+", c.lower()))) >= 3
        )
        recalls.append(1.0 if hits > 0 else 0.0)

        pred_ans = answer_question(retrieved, q)
        f1s.append(token_f1(pred_ans, ref_ans))

    return StrategyResult(
        name=name,
        n_chunks=len(chunks),
        recall_at_k=sum(recalls) / len(recalls),
        answer_f1=sum(f1s) / len(f1s),
    )


def pick_winner(results: list[StrategyResult]) -> StrategyResult:
    """Weighted score: 60% recall@5 + 40% answer F1."""
    return max(results, key=lambda r: 0.6 * r.recall_at_k + 0.4 * r.answer_f1)


if __name__ == "__main__":
    import re
    docs = load_corpus()
    golden = load_golden()

    strategies: list[tuple[StrategyName, list[str]]] = [
        ("fixed", fixed_chunks(docs)),
        ("semantic", semantic_chunks(docs)),
        ("recursive", recursive_chunks(docs)),
    ]

    results = []
    for name, chunks in strategies:
        r = evaluate_strategy(name, chunks, golden)
        results.append(r)

    print("\n=== Chunking Benchmark Results ===")
    print(f"{'Strategy':<12} {'Chunks':>7} {'Recall@5':>10} {'Ans F1':>9}")
    print("-" * 42)
    for r in results:
        print(f"{r.name:<12} {r.n_chunks:>7} {r.recall_at_k:>10.3f} {r.answer_f1:>9.3f}")

    winner = pick_winner(results)
    score = 0.6 * winner.recall_at_k + 0.4 * winner.answer_f1
    print(f"\nWinner: {winner.name}  (weighted score {score:.3f})")
    print("Decision: use this strategy for your corpus.")
```

7. Run the full benchmark:

```bash
python benchmark.py
```

Expected runtime: 3–8 minutes depending on corpus size and OpenAI API latency.

## Verify

Run the benchmark and check the final output block:

```
=== Chunking Benchmark Results ===
Strategy       Chunks   Recall@5    Ans F1
------------------------------------------
fixed             NNN      0.XXX     0.XXX
semantic          NNN      0.XXX     0.XXX
recursive         NNN      0.XXX     0.XXX

Winner: <strategy>  (weighted score X.XXX)
```

All three strategies must produce a score line with numeric values. Exit code must be 0:

```bash
python benchmark.py; echo "exit $?"
```

If recall@5 is 0.000 for all strategies, your golden set answers do not overlap with corpus text — regenerate with `generate_golden.py` against your actual corpus.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `chromadb.errors.InvalidCollectionException` on re-run | Collection name collision from previous run | Add `client.delete_collection(name)` before `get_or_create_collection`, or use a UUID suffix: `f"{name}-{uuid.uuid4().hex[:6]}"` |
| `sentence_transformers` download hangs at 0% | Firewall blocks Hugging Face CDN | Pre-download: `python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"` on a machine with internet access, then copy `~/.cache/huggingface/` |
| Recall@5 uniformly 1.0 for all strategies | Golden answers are trivial (single common words) | Audit `golden_set.jsonl`; answers should be 5–30 words from the corpus, not single-word labels |
| `TokenTextSplitter` raises `ImportError` | `tiktoken` not installed | `pip install tiktoken` |
| Semantic chunker produces 1 giant chunk | All sentences are highly similar (same topic all the way through) | Lower the `threshold` parameter from `0.85` to `0.70` in `semantic_chunks()` |
| OpenAI embedding cost too high for large corpus | 512-token chunks × 50 docs × 3 strategies = ~150k tokens | Switch `OpenAIEmbeddingFunction` to `chromadb.utils.embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")` for zero-cost local embeddings |
| Answer F1 near zero despite correct retrieval | LLM answers verbosely, diverging from reference phrasing | Switch `token_f1` to BERTScore or use `rouge-score` for semantic matching |

## Next

- `rag-eval-production-monitoring` — graduate from offline benchmarks to live A/B evaluation with production traffic once a winner is selected.
- Swap ChromaDB for Qdrant (see `geek/ai/rag-engineer/db-qdrant`) when corpus exceeds 100k chunks or you need filtered search on metadata.
- Add a reranking pass after retrieval (see `geek/ai/rag-engineer/reranking-two-stage`) to push recall@5 gains further before answer generation.

## References

- [knowledge/geek/ai/rag-engineer/chunking-basics](../../../knowledge/geek/ai/rag-engineer/chunking-basics) — defines fixed-size, semantic, and recursive chunking as the three primary strategies scored in this benchmark's evaluation loop
- [knowledge/geek/ai/rag-engineer/chunking-semantic](../../../knowledge/geek/ai/rag-engineer/chunking-semantic) — details the sentence-embedding similarity threshold logic replicated verbatim in `semantic_chunks()` at Step 3
- [knowledge/geek/ai/rag-engineer/embedding-chunking-strategies](../../../knowledge/geek/ai/rag-engineer/embedding-chunking-strategies) — explains why chunk boundaries affect embedding quality, backing the 512-token and 1200-char size choices in Steps 3 and 4
- [knowledge/geek/ai/rag-engineer/rag-eval-retrieval-metrics](../../../knowledge/geek/ai/rag-engineer/rag-eval-retrieval-metrics) — defines recall@K formally; this playbook implements the recall@5 computation in `evaluate_strategy()` at Step 6
- [knowledge/geek/ai/rag-engineer/rag-eval-pipeline](../../../knowledge/geek/ai/rag-engineer/rag-eval-pipeline) — provides the end-to-end offline eval scaffold (corpus → index → query → score) that this playbook's benchmark loop follows
