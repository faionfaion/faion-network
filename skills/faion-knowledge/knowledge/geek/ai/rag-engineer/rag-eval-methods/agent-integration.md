# Agent Integration — RAG Evaluation Methods

## When to use
- Before deploying a RAG system to production — establishing baseline quality scores
- After any pipeline change (chunking strategy, top-K, model swap) to detect regressions
- Comparing two RAG configurations (A/B testing different chunk sizes, embedding models, or rerankers)
- Generating synthetic test datasets from the document corpus when no labeled data exists
- Setting up continuous evaluation to catch quality drift in production

## When NOT to use
- Proof-of-concept phase with no labeled data and no budget for LLM-based evaluation — defer until validation stage
- High-frequency real-time evaluation of every query in production — use lightweight metrics (latency, hit rate, user signals) instead; reserve LLM eval for sampled batches
- When the test set is smaller than 20 questions — statistical noise dominates; results are not actionable
- When ground truth answers are unavailable and the domain is too specialized for synthetic generation to be reliable

## Where it fails / limitations
- Synthetic question generation (LLM-generated Q&A) has a positivity bias — the LLM generates questions the document can answer well, not the hard edge-case questions that fail in production
- LLM evaluators (faithfulness, relevance scoring) have their own biases and can disagree with human judgment on 20-30% of cases
- RAGAS metrics require `ground_truth` answers — without them, only `faithfulness` and `answer_relevancy` are computable
- A/B test framework in the README compares latency but not quality metrics — extending it requires full eval integration per configuration
- Production `RAGMonitor` relies on user feedback signals which are sparse in most apps; anomaly detection thresholds need corpus-specific calibration
- Cost at scale: evaluating 1000 questions with GPT-4o at $0.01/eval = $10; at 10K questions = $100; budget-based sampling is mandatory

## Agentic workflow
A test-generation agent samples N documents from the corpus and prompts an LLM to produce question/answer/source-quote triples. A validation agent runs these questions through the production RAG pipeline, collects answers and retrieved contexts, and passes them to the evaluation agent. The evaluation agent computes retrieval metrics (precision@5, MRR) and generation metrics (faithfulness, relevance) via LLM scoring or RAGAS, then writes aggregated results to a JSON report. Human review of the report is required before any pipeline change is merged to production.

### Recommended subagents
- `faion-sdd-executor-agent` — builds the evaluation pipeline scaffolding (test generation, eval runner, export)
- Custom test-generation agent — generates diverse question types (factual, comparative, reasoning) with difficulty labels
- Custom eval-runner agent — batches eval calls with budget awareness and progress checkpointing

### Prompt pattern
```
You are a test-set generator. Given: document (text, max 2000 chars).
Generate one test case per question type: factual, comparative, reasoning.
For each: {"question": "...", "answer": "...", "source_quote": "...", "type": "...", "difficulty": "easy|medium|hard"}
Return: JSON array of 3 test cases.
Constraint: questions must be answerable ONLY from the provided document.
```

```
You are a RAG evaluator. Given: question, answer, context (retrieved chunks), ground_truth.
Compute:
- faithfulness (0-1): fraction of answer claims supported by context
- answer_relevance (0-1): how completely the answer addresses the question
- context_relevance (0-1): fraction of context that is relevant to the question
Return: {"faithfulness": X, "answer_relevance": Y, "context_relevance": Z, "explanation": "..."}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ragas` | RAGAS framework (faithfulness, relevancy, precision, recall) | `pip install ragas` / [docs](https://docs.ragas.io/) |
| `datasets` (HuggingFace) | Dataset format required by RAGAS | `pip install datasets` / [docs](https://huggingface.co/docs/datasets) |
| `openai` | LLM-based evaluation prompts | `pip install openai` / [docs](https://platform.openai.com/docs/) |
| `trulens-eval` | TruLens RAG triad evaluation | `pip install trulens-eval` / [docs](https://www.trulens.org/) |
| `deepeval` | Unit test-style RAG evaluation | `pip install deepeval` / [docs](https://docs.confident-ai.com/) |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| RAGAS | OSS | Yes — Python library | Gold standard for RAG eval; requires HF Dataset format |
| TruLens | OSS + cloud dashboard | Yes | RAG triad (context relevance, groundedness, answer relevance) |
| DeepEval | OSS + SaaS | Yes | Unit-test framework for LLM outputs; CI integration |
| LangSmith | SaaS | Yes | LangChain-native eval + tracing; stores runs for comparison |
| Weights & Biases | SaaS | Yes — W&B Tables | Log eval results as runs for comparison and regression tracking |
| Arize Phoenix | OSS + SaaS | Yes | LLM observability + eval; good for production monitoring |

## Templates & scripts
See `templates.md` for `RAGEvaluator`, `RAGABTest`, and `RAGMonitor` class implementations.

Minimal RAGAS integration (25 lines):
```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from datasets import Dataset

def run_ragas_eval(questions, answers, contexts, ground_truths):
    """
    questions: list[str]
    answers: list[str]
    contexts: list[list[str]]  — list of retrieved chunks per question
    ground_truths: list[str]
    """
    dataset = Dataset.from_dict({
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths
    })
    result = evaluate(
        dataset,
        metrics=[faithfulness, answer_relevancy, context_precision, context_recall]
    )
    return dict(result)  # {"faithfulness": 0.87, "answer_relevancy": 0.91, ...}
```

## Best practices
- Maintain a versioned test set in source control — test set drift is as dangerous as model drift
- Include at least 20% hard or edge-case questions in the test set — easy questions mask retrieval failures on ambiguous queries
- Stratify test set by document source and question type; aggregate metrics hide per-source degradation
- Run evaluation on every config change, not just weekly — even chunking parameter tweaks can degrade precision@5 significantly
- Use `cost_efficient_evaluation` (budget-based sampling) for routine CI checks; run the full test suite only for release decisions
- Establish numeric quality gates before deployment: e.g., faithfulness > 0.8, precision@5 > 0.7 — otherwise eval is informational only

## AI-agent gotchas
- RAGAS `evaluate()` calls OpenAI internally by default — agents must ensure `OPENAI_API_KEY` is set in the environment before invoking; missing key causes a cryptic error, not a clear auth error
- RAGAS `contexts` field expects `list[list[str]]` (list of lists), not `list[str]` — passing a flat list causes silent incorrect metric computation
- LLM-generated test cases must be manually spot-checked before use — the generator LLM sometimes creates questions the document does not actually answer (hallucinated source quotes)
- `RAGABTest.compare_results()` as shown in the README only compares latency, not quality; agents must extend it with the RAGAS eval loop to be useful for config comparison
- Production `RAGMonitor.detect_anomalies()` uses hardcoded thresholds (latency > 5.0s, negative_feedback > 10) — agents deploying this must calibrate these against actual production baselines
- DeepEval and TruLens require a running eval server or cloud account for some features; agents in air-gapped environments should fall back to the custom LLM-prompt evaluation pattern

## References
- [RAGAS Paper (arxiv)](https://arxiv.org/abs/2309.15217)
- [RAGAS Documentation](https://docs.ragas.io/)
- [TruLens RAG Triad](https://www.trulens.org/trulens_eval/tracking/instrumentation/rag_triad/)
- [LlamaIndex Evaluation](https://docs.llamaindex.ai/en/stable/module_guides/evaluating/)
- [LangChain Evaluation](https://python.langchain.com/docs/guides/evaluation/)
- [DeepEval Docs](https://docs.confident-ai.com/)
- [RAG Evaluation - Pinecone Blog](https://www.pinecone.io/learn/rag-evaluation/)
