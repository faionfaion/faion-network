# Agent Integration — RAG Evaluation

## When to use
- Before promoting a RAG pipeline to production — validate retrieval recall and generation faithfulness
- After changing chunking strategy, embedding model, or vector DB configuration — check for regression
- Comparing two embedding models for the same corpus — use Precision@K and MRR to decide
- Diagnosing user complaints about wrong or hallucinated answers — isolate retrieval vs generation failure
- Setting up continuous production monitoring — lightweight faithfulness + hit rate metrics sampled per hour

## When NOT to use
- No ground truth queries exist and the domain is too specialized to generate synthetic ones reliably
- The pipeline is a prototype and the chunking/embedding strategy is still changing daily — evaluate after it stabilizes
- Budget is insufficient for LLM-as-judge at scale — use automated metrics only as a proxy until budget allows
- The primary goal is latency optimization, not quality — profiling tools are more appropriate

## Where it fails / limitations
- RAGAS metrics require an LLM to score faithfulness and relevance — evaluation cost scales with corpus and query volume
- Faithfulness > 0.85 is achievable in controlled tests but degrades when retrieved chunks contain contradictory information
- Ground truth creation is expensive and slow — 100 annotated query-document pairs takes significant human time
- LLM-as-judge scores vary between runs (±3–5%) — report means and standard deviations, not single-run scores
- Retrieval metrics (Precision, Recall) require relevance labels; without them you are limited to approximate heuristics
- Evaluation set distribution drift: a test set from month 1 may not represent user queries at month 6

## Agentic workflow
A RAG evaluation agent runs in four steps: (1) load the evaluation dataset (query, expected_answer, source_docs), (2) run the RAG pipeline under test to get retrieved_chunks and generated_answer, (3) compute retrieval metrics from chunk labels and generation metrics via LLM-as-judge, (4) write a structured report with per-metric scores, failure examples, and recommendations. Separation of retrieval and generation evaluation is critical — failures must be attributed to the right component for the fix to be targeted.

### Recommended subagents
- `faion-sdd-executor-agent` — when RAG evaluation is a quality gate in an SDD feature lifecycle
- General Claude (Sonnet) subagent — as LLM-as-judge for faithfulness and answer relevance scoring

### Prompt pattern
Faithfulness judge prompt:
```xml
<faithfulness-eval>
  <question>{question}</question>
  <context>{retrieved_chunks}</context>
  <answer>{generated_answer}</answer>
  <task>
    Identify each factual claim in the answer.
    For each claim: determine if it is directly supported by the context.
    Score: supported_claims / total_claims.
    Return JSON: {"score": 0.0-1.0, "claims": [{"claim": "...", "supported": true|false}]}
  </task>
</faithfulness-eval>
```

```python
# RAGAS evaluation runner
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from datasets import Dataset

eval_data = {
    "question": questions,
    "answer": generated_answers,
    "contexts": retrieved_chunks_per_question,
    "ground_truth": reference_answers,
}
dataset = Dataset.from_dict(eval_data)
result = evaluate(
    dataset,
    metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
)
print(result.to_pandas())
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ragas` | RAG-specific metric suite | `pip install ragas` · docs.ragas.io |
| `trulens-eval` | TruLens RAG triad evaluation | `pip install trulens-eval` · trulens.org |
| `deepeval` | DeepEval RAG metrics (faithfulness, NDCG) | `pip install deepeval` · deepeval.com |
| `langsmith` | RAG tracing + dataset-based eval | `pip install langsmith` · smith.langchain.com |
| `qdrant-client` | For retrieval hit-rate testing against Qdrant | `pip install qdrant-client` |
| `rank-bm25` | BM25 baseline for retrieval comparison | `pip install rank-bm25` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Langfuse | SaaS/OSS | Yes — SDK | RAG tracing, dataset upload, evaluation runs |
| LangSmith | SaaS | Yes — SDK | Dataset management, LLM-as-judge eval pipeline |
| Braintrust | SaaS | Yes — SDK | Real-time RAG eval with scoring functions |
| Arize Phoenix | OSS | Yes — SDK | RAG observability; retrieval span tracking |
| AWS Bedrock Eval | SaaS | Yes — AWS SDK | Built-in RAG evaluation for Bedrock pipelines |
| Vertex AI Eval | SaaS | Yes — gCloud SDK | Native GCP RAG evaluation |
| TruEra | SaaS | Yes — API | Enterprise RAG quality and fairness monitoring |

## Templates & scripts
See `templates.md` for full RAGAS evaluation pipeline with dataset generation and reporting.

Inline: hit rate and MRR calculator for retrieval (< 40 lines):

```python
def compute_retrieval_metrics(
    retrieved_doc_ids: list[list[str]],
    relevant_doc_ids: list[list[str]],
    k: int = 10,
) -> dict:
    hit_rates, mrr_scores, precision_scores = [], [], []
    for retrieved, relevant in zip(retrieved_doc_ids, relevant_doc_ids):
        relevant_set = set(relevant)
        top_k = retrieved[:k]
        # Hit rate
        hit = any(doc in relevant_set for doc in top_k)
        hit_rates.append(float(hit))
        # MRR
        mrr = 0.0
        for rank, doc in enumerate(top_k, 1):
            if doc in relevant_set:
                mrr = 1.0 / rank
                break
        mrr_scores.append(mrr)
        # Precision@K
        hits_in_k = sum(1 for doc in top_k if doc in relevant_set)
        precision_scores.append(hits_in_k / k)
    return {
        f"hit_rate@{k}": sum(hit_rates) / len(hit_rates),
        f"mrr@{k}": sum(mrr_scores) / len(mrr_scores),
        f"precision@{k}": sum(precision_scores) / len(precision_scores),
    }
```

## Best practices
- Evaluate retrieval and generation separately — a high faithfulness score with low hit rate means the model is hallucinating consistently, not retrieving well
- Target these baselines before production: faithfulness > 0.85, answer relevance > 0.90, hit rate > 0.90
- Build your ground truth dataset from real user queries, not synthetic questions — at minimum 100 samples
- Run evaluation after every chunking or embedding change — these are the highest-impact variables for retrieval quality
- Use context precision (relevant chunks / total retrieved chunks) as a proxy for retrieval efficiency — lower precision means LLM context is polluted with noise
- Automate evaluation in CI with a minimum score gate: block merge if faithfulness drops > 5% vs main

## AI-agent gotchas
- RAGAS `faithfulness` metric makes multiple LLM calls per sample (claim extraction + support checking) — evaluation of 100 samples can cost $5–20 in Claude/GPT-4 calls
- Agents generating synthetic ground truth (question-answer pairs from documents) should use a different model than the one being evaluated — using the same model creates a self-fulfilling evaluation
- RAGAS `context_recall` requires ground truth answers to compute — without them the metric is unavailable; agents must check dataset completeness before running
- Evaluation agents running RAGAS asynchronously must handle rate limits from the judge LLM separately from the pipeline LLM
- Retrieval metrics require document IDs — if your vector DB returns raw text chunks without stable IDs, compute IDs as hash(content) before evaluation
- Do not conflate RAGAS faithfulness (grounded in retrieved context) with factual accuracy (correct against world knowledge) — a faithful answer can still be factually wrong if the retrieved context is wrong

## References
- https://docs.ragas.io/
- https://arxiv.org/abs/2309.15217 (RAGAS paper)
- https://www.pinecone.io/learn/rag-evaluation/
- https://qdrant.tech/blog/rag-evaluation-guide/
- https://docs.llamaindex.ai/en/stable/module_guides/evaluating/
- https://trulens.org/
- https://arize.com/blog-course/rag-evaluation/
