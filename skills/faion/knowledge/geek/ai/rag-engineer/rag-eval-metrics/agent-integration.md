# Agent Integration — RAG Evaluation Metrics

## When to use
- Selecting which specific metrics to compute for a given RAG use case (Q&A vs document search vs chatbot)
- Implementing the retrieval quality layer of an eval pipeline (Precision@K, Recall@K, MRR, NDCG, Hit Rate)
- Implementing the generation quality layer (faithfulness, answer relevance, context relevance)
- Setting quality gates for CI/CD pipelines — failing a deployment if faithfulness drops below threshold
- Understanding RAGAS metric semantics before integrating the RAGAS library

## When NOT to use
- Replacing the full `rag-eval-methods` methodology — metrics are the measurement layer, not the eval framework
- Single-metric decision-making — no single metric fully characterizes RAG quality; always use a combination
- Production real-time scoring of every query — LLM-based metrics (faithfulness, relevance) are too slow and expensive at query time; use offline sampling instead

## Where it fails / limitations
- `precision_at_k` and `recall_at_k` require ground-truth relevant doc IDs — collecting these labels is expensive and requires human annotation or synthetic generation
- `ndcg_at_k` requires graded relevance scores (0-3 or 0-5), not just binary relevant/not-relevant — graded labels are even harder to collect than binary labels
- LLM-based `evaluate_faithfulness` using GPT-4o is $$$; at scale, switch to `gpt-4o-mini` (3x cheaper) and accept ~5% accuracy loss
- RAGAS metrics use OpenAI by default; swapping to a different LLM evaluator can change metric values significantly — results are not cross-LLM-comparable
- `hit_rate` is a binary metric and is insensitive to how many relevant documents were retrieved; a system that retrieves 1 relevant out of 20 possible scores the same as one that retrieves 18 out of 20
- `mean_reciprocal_rank` penalizes harshly when the first relevant doc is ranked 3rd or lower; for most RAG use cases with top-5 retrieval, MRR and Hit Rate are nearly equivalent

## Agentic workflow
An evaluation agent selects the appropriate metric set based on use case (Q&A → faithfulness + precision@5 + MRR; document search → NDCG@10 + recall@20; chatbot → context relevance + coherence). It runs retrieval metrics on labeled test sets using pure-Python implementations (no API cost). It then samples a subset (10-20%) of queries for LLM-based generation metrics to control cost. Results are aggregated and compared against stored baseline values; a regression detection agent flags any metric that dropped more than 5 percentage points.

### Recommended subagents
- `faion-sdd-executor-agent` — wires metric computation into the eval pipeline and sets quality gate thresholds
- Custom regression detection agent — compares current metric values against stored baseline and emits alerts on degradation

### Prompt pattern
```
You are a RAG metrics agent. Given: evaluation_results.json.
Compute aggregate metrics:
- retrieval: avg precision@5, recall@5, MRR, hit_rate
- generation: avg faithfulness, answer_relevance, context_relevance
- flag any metric below threshold: {faithfulness: 0.80, precision@5: 0.70, hit_rate: 0.90}
Return: {"metrics": {...}, "flags": [...], "recommendation": "..."}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ragas` | Full RAGAS suite (faithfulness, answer_relevancy, context_precision, context_recall) | `pip install ragas` / [docs](https://docs.ragas.io/) |
| `trulens-eval` | RAG Triad scoring with TruLens | `pip install trulens-eval` / [docs](https://www.trulens.org/) |
| `deepeval` | Metric-level evaluation with assertion style | `pip install deepeval` / [docs](https://docs.confident-ai.com/) |
| `numpy` | NDCG computation (DCG scoring) | stdlib in most envs / [docs](https://numpy.org/) |
| `openai` | LLM-judge for faithfulness/relevance prompts | `pip install openai` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| RAGAS | OSS | Yes | Best for RAGAS Triad; requires HF Datasets format |
| TruLens | OSS + cloud | Yes | RAG triad + custom feedback functions |
| DeepEval | OSS + SaaS | Yes | Unit-test assertions for individual metrics |
| LangSmith | SaaS | Yes | Built-in evaluators for RAG; stores metric history |
| Arize Phoenix | OSS + SaaS | Yes | LLM observability with metric dashboards |
| Weights & Biases | SaaS | Yes | Log metric runs for experiment tracking |

## Templates & scripts
See `templates.md` for `evaluate_faithfulness`, `evaluate_relevance`, and `evaluate_context_relevance` LLM-based implementations.

Complete retrieval metric suite (standalone, no external deps):
```python
from typing import List, Set, Dict
import numpy as np

def precision_at_k(retrieved: List[str], relevant: Set[str], k: int) -> float:
    return len(set(retrieved[:k]) & relevant) / k

def recall_at_k(retrieved: List[str], relevant: Set[str], k: int) -> float:
    return len(set(retrieved[:k]) & relevant) / len(relevant) if relevant else 0.0

def mean_reciprocal_rank(retrieved: List[str], relevant: Set[str]) -> float:
    for i, doc_id in enumerate(retrieved):
        if doc_id in relevant:
            return 1.0 / (i + 1)
    return 0.0

def hit_rate(retrieved: List[str], relevant: Set[str]) -> float:
    return 1.0 if any(d in relevant for d in retrieved) else 0.0

def ndcg_at_k(retrieved: List[str], relevance_scores: Dict[str, float], k: int) -> float:
    def dcg(scores):
        return sum((2**s - 1) / np.log2(i + 2) for i, s in enumerate(scores))
    actual = [relevance_scores.get(d, 0) for d in retrieved[:k]]
    ideal = sorted(relevance_scores.values(), reverse=True)[:k]
    idcg = dcg(ideal)
    return dcg(actual) / idcg if idcg > 0 else 0.0

def compute_retrieval_metrics(retrieved, relevant, k=5, relevance_scores=None):
    return {
        f"precision@{k}": precision_at_k(retrieved, relevant, k),
        f"recall@{k}": recall_at_k(retrieved, relevant, k),
        "mrr": mean_reciprocal_rank(retrieved, relevant),
        "hit_rate": hit_rate(retrieved, relevant),
        **({"ndcg@{k}": ndcg_at_k(retrieved, relevance_scores, k)} if relevance_scores else {})
    }
```

## Best practices
- Select metrics by use case, not by familiarity: Q&A → faithfulness + precision@5; search → NDCG@10 + recall@20; chatbot → context relevance + hit rate
- Always pair a retrieval metric with a generation metric — high precision@5 with low faithfulness indicates a generation problem, not retrieval
- Track all metrics over time, not just point-in-time — a metric trending downward over 2 weeks is actionable even if the current value is above threshold
- Use cost tiers: retrieval metrics (precision, recall, MRR) are free — run on every test; LLM-judge metrics (faithfulness) are expensive — run on 10-20% sample
- Set explicit numeric quality gates before deployment; "looks good" is not a quality gate; "faithfulness >= 0.80 AND precision@5 >= 0.70" is
- Never use a single metric as a deployment gate — a model can improve faithfulness while degrading retrieval recall

## AI-agent gotchas
- `precision_at_k` divides by k, not by number of retrieved docs — agents must pass the correct k matching the retrieval top-K, not the actual result count
- RAGAS `context_precision` requires ground_truth in the dataset even though it measures retrieval quality — confusing naming; read the RAGAS docs carefully
- RAGAS uses OpenAI for LLM-judge metrics by default; agents in environments without `OPENAI_API_KEY` will get a cryptic import/init error, not a clear auth failure
- `evaluate_faithfulness` LLM prompt returns `unsupported_claims` as a list — agents logging results must handle the case where this is an empty list (all claims supported), not null
- NDCG requires graded relevance scores — if only binary labels exist, set `relevance_scores = {doc_id: 1.0 for doc_id in relevant}` and NDCG degrades to AP (average precision)
- `mean_reciprocal_rank` returns 0.0 when no relevant doc is retrieved — agents computing macro-average MRR over a test set should distinguish this from MRR=0.0 due to ranking failures

## References
- [RAGAS Paper (arxiv)](https://arxiv.org/abs/2309.15217)
- [RAGAS Docs](https://docs.ragas.io/)
- [TruLens RAG Triad](https://www.trulens.org/trulens_eval/tracking/instrumentation/rag_triad/)
- [IR Evaluation Measures (Wikipedia)](https://en.wikipedia.org/wiki/Evaluation_measures_(information_retrieval))
- [NDCG Explained](https://en.wikipedia.org/wiki/Discounted_cumulative_gain)
