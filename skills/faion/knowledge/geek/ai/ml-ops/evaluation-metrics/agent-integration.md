# Agent Integration — Evaluation Metrics

## When to use
- Implementing automated quality gates in a CI/CD pipeline for LLM-powered features
- Comparing two model versions or prompt variants before a production rollout
- Tracking metric trends over time in a production monitoring dashboard
- Building an evaluation harness that a subagent can run autonomously against a test dataset
- Selecting the right metric for a specific task type (classification, QA, summarization, code generation)

## When NOT to use
- The task has no quantifiable success criterion — open-ended creative generation requires human preference evaluation, not automated metrics
- Ground-truth labels are unavailable and cannot be synthesized with validation; BLEU/ROUGE without references are meaningless
- Exact match or BLEU are the only metrics for long-form generation — they punish valid paraphrases and correlate poorly with human judgment
- Safety metrics (toxicity, bias) are the sole gate for production decisions — automated safety metrics miss context-dependent harms and require human review

## Where it fails / limitations
- BLEU scores below 0.3 are unreliable discriminators between models — differences of 0.01-0.02 BLEU have no practical significance
- `semantic_similarity` using cosine of embeddings can score near 1.0 for antonyms if the embedding space collapses similar topics ("good" vs. "not good")
- `refusal_rate` using string patterns is brittle — models change refusal phrasing with version updates, causing false negatives
- `classification_f1` with `average='macro'` penalizes imbalanced datasets unfairly; use `weighted` for production traffic distributions
- The `code_pass_at_k` metric requires runnable test cases — agents cannot generate reliable test cases without domain knowledge validation
- Latency stats computed from a small sample (< 30 requests) are misleading for p95/p99 — these require 100+ samples to stabilize

## Agentic workflow
An agent using evaluation metrics should select 3-5 metrics matching the task type, run them against a fixed test dataset using the `aggregate_metrics` pattern, compare results to a pre-established baseline, and report pass/fail per metric against defined thresholds. For production monitoring, the agent samples live traffic, applies lightweight automated checks, and escalates to LLM-as-judge only for flagged samples to control cost.

### Recommended subagents
- `faion-sdd-executor-agent` — executes metric-selection and evaluation-run tasks from an SDD task card
- An evaluation subagent (custom) — takes a test dataset path, model endpoint, and metric list; returns a structured JSON summary using `create_metric_summary`

### Prompt pattern
```
Given this task type: {classification|qa|summarization|generation},
select the 3 most appropriate metrics from:
[exact_match, contains_match, bleu_score, rouge_score, semantic_similarity,
classification_f1, qa_f1, latency_stats, refusal_rate, safe_content_rate].
Return JSON: {"metrics": [str], "rationale": str, "thresholds": {"metric": float}}
```

```
Evaluate the following {N} model outputs against ground truth.
Apply metrics: {metric_list}.
Return: {"pass": bool, "summary": {metric: {mean, min, max}}, "failures": [case_idx]}
where pass=true only if all metric means exceed their thresholds.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `evaluate` (HuggingFace) | BLEU, ROUGE, accuracy, F1 in one library | `pip install evaluate` / [huggingface.co/docs/evaluate](https://huggingface.co/docs/evaluate) |
| `rouge-score` | ROUGE-1/2/L for summarization | `pip install rouge-score` / [github.com/google-research/google-research](https://github.com/google-research/google-research/tree/master/rouge) |
| `nltk` | BLEU, tokenization | `pip install nltk` / [nltk.org](https://www.nltk.org/) |
| `scikit-learn` | F1, accuracy, classification report | `pip install scikit-learn` / [scikit-learn.org](https://scikit-learn.org/) |
| `sentence-transformers` | Semantic similarity via embeddings | `pip install sentence-transformers` |
| `perspective` (Perspective API) | Toxicity scoring | [perspectiveapi.com](https://perspectiveapi.com/) — requires API key |
| `numpy` | Latency stats (percentiles) | `pip install numpy` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Langfuse | SaaS/OSS (MIT) | Yes — SDK + REST API | Store and query metric scores per trace |
| Braintrust | SaaS | Yes — evaluation SDK | Built-in metric library, dataset versioning |
| RAGAS | OSS | Yes — Python library | RAG-specific metrics (faithfulness, context precision) |
| OpenAI Evals | OSS | Yes — YAML/Python eval definitions | Standardized eval runner; good for regression testing |
| Arize Phoenix | SaaS/OSS | Yes — `phoenix.evals` module | LLM-as-judge evaluation with structured criteria |
| HuggingFace `evaluate` | OSS | Yes — programmatic API | 100+ metrics, reproducible implementations |
| Perspective API | SaaS | Yes — REST | Toxicity scores with attribute breakdown |

## Templates & scripts
See `templates.md` for full metric registry and evaluation runner templates.

Inline — task-type metric selector with threshold defaults:

```python
TASK_METRICS = {
    "classification": {
        "metrics": ["exact_match", "classification_f1"],
        "thresholds": {"exact_match": 0.80, "classification_f1": 0.75},
    },
    "qa": {
        "metrics": ["contains_match", "qa_f1", "semantic_similarity"],
        "thresholds": {"contains_match": 0.70, "qa_f1": 0.60, "semantic_similarity": 0.80},
    },
    "summarization": {
        "metrics": ["rouge_score"],
        "thresholds": {"rouge1_f": 0.35, "rouge2_f": 0.15, "rougeL_f": 0.30},
    },
    "generation": {
        "metrics": ["semantic_similarity", "refusal_rate"],
        "thresholds": {"semantic_similarity": 0.75, "refusal_rate": 0.05},
    },
}

def get_metrics_for_task(task_type: str) -> dict:
    return TASK_METRICS.get(task_type, TASK_METRICS["generation"])
```

## Best practices
- Always establish a baseline metric run against the current production model before evaluating a candidate — without a baseline, absolute numbers have no meaning
- Use at least 100 test cases for p95 latency and metric means to be statistically stable; fewer than 30 cases produces results with confidence intervals too wide to act on
- Combine automated metrics with a 5-10% human spot-check sample — automated metrics can plateau while human-judged quality degrades (or vice versa)
- Track metrics over time in a time-series store (Langfuse, W&B); a single evaluation snapshot is much less valuable than a trend
- For multi-label classification, always report per-class F1 alongside macro/weighted — a high weighted F1 can hide a complete failure on rare classes
- Weight output token cost in latency analysis — long outputs inflate wall-clock time; separate TTFT (time to first token) from total latency in streaming APIs
- Refusal rate thresholds depend on the prompt type; for safety-critical prompts a 95% refusal rate is correct, not a failure

## AI-agent gotchas
- BLEU and ROUGE use n-gram overlap — agents should not interpret a 0.01 difference as meaningful; these metrics require large test sets and aggregate interpretation
- `semantic_similarity` requires a consistent embedding model across runs; switching embedding models between baseline and candidate invalidates the comparison
- Latency benchmarks run from an agent loop include agent overhead (API call latency, parsing time) — isolate model latency by calling the model endpoint directly, not through an agent wrapper
- The `safe_content_rate` function loads `unitary/toxic-bert` on first call — agents running in serverless environments will time out on cold start; pre-warm or use the Perspective API instead
- Cost metrics require accurate token counts — agents that estimate tokens from character count (÷ 4) rather than tokenizer output will have 15-30% error on non-English text

## References
- [BLEU Score (Papineni et al., 2002)](https://www.aclweb.org/anthology/P02-1040.pdf)
- [ROUGE Score (Lin, 2004)](https://www.aclweb.org/anthology/W04-1013.pdf)
- [HuggingFace Evaluate](https://huggingface.co/docs/evaluate/)
- [Perspective API](https://perspectiveapi.com/)
- [RAGAS — RAG Evaluation](https://docs.ragas.io/)
- [OpenAI Evals](https://github.com/openai/evals)
- [HELM Benchmark](https://crfm.stanford.edu/helm/)
