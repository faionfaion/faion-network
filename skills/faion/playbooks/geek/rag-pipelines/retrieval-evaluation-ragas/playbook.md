---
name: retrieval-evaluation-ragas
description: Build a 50-item eval set and run RAGAS metrics with a Langfuse CI gate for faithfulness ≥ 0.85 and context_precision ≥ 0.70.
tier: geek
group: rag-pipelines
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a reproducible RAG evaluation pipeline: a 50-item eval dataset (question, ground-truth-answer, ground-truth-contexts), RAGAS scores computed against your live pipeline, traces visible in Langfuse, and a CI gate that blocks merges when faithfulness drops below 0.85 or context_precision below 0.70.

## Prerequisites

- Python 3.11+ with `ragas>=0.1.20`, `langfuse>=2.25`, `langchain-anthropic>=0.3`, `datasets>=2.19` installed.
- A running RAG pipeline that accepts a question string and returns `answer` + `contexts` (list of retrieved text chunks).
- An Anthropic API key (`ANTHROPIC_API_KEY`) for RAGAS LLM judge calls.
- A Langfuse project with `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `LANGFUSE_HOST` set in your environment.
- Familiarity with the RAGAS metric taxonomy — context_precision, context_recall, faithfulness, answer_relevancy. See References.

## Steps

1. Install evaluation dependencies into your virtual environment:

   ```bash
   pip install "ragas>=0.1.20" "langfuse>=2.25" "langchain-anthropic>=0.3" "datasets>=2.19"
   ```

2. Create `eval/build_dataset.py` to assemble the 50-item eval set. Each row needs `question`, `ground_truth` (the correct answer), and `reference_contexts` (list of strings that *should* be retrieved):

   ```python
   # eval/build_dataset.py
   from datasets import Dataset

   RAW: list[dict] = [
       {
           "question": "What is the maximum context window of claude-opus-4-7?",
           "ground_truth": "200,000 tokens",
           "reference_contexts": [
               "claude-opus-4-7 supports a 200k token context window as of 2026.",
           ],
       },
       # ... 49 more rows covering your domain
   ]

   def build() -> Dataset:
       return Dataset.from_list(RAW)

   if __name__ == "__main__":
       ds = build()
       ds.save_to_disk("eval/dataset")
       print(f"Saved {len(ds)} rows → eval/dataset")
   ```

   Populate all 50 rows with real questions drawn from your support tickets, product FAQs, or domain knowledge base — not synthetic placeholders.

3. Create `eval/run_pipeline.py` to query your live RAG pipeline for each eval row and collect `answer` + `contexts`:

   ```python
   # eval/run_pipeline.py
   from datasets import Dataset, load_from_disk
   from your_rag_module import query_rag  # replace with your RAG entrypoint

   def collect_responses(ds: Dataset) -> Dataset:
       answers, contexts = [], []
       for row in ds:
           result = query_rag(row["question"])
           answers.append(result["answer"])
           contexts.append(result["contexts"])  # list[str]
       return ds.add_column("answer", answers).add_column("contexts", contexts)

   if __name__ == "__main__":
       ds = load_from_disk("eval/dataset")
       ds = collect_responses(ds)
       ds.save_to_disk("eval/dataset_with_responses")
       print(f"Collected responses for {len(ds)} rows")
   ```

4. Create `eval/score.py` to run RAGAS and push traces to Langfuse:

   ```python
   # eval/score.py
   import os
   from datasets import load_from_disk
   from langchain_anthropic import ChatAnthropic
   from ragas import evaluate
   from ragas.metrics import (
       context_precision,
       context_recall,
       faithfulness,
       answer_relevancy,
   )
   from ragas.integrations.langfuse import LangfuseCallbackHandler

   THRESHOLDS = {
       "faithfulness": 0.85,
       "context_precision": 0.70,
   }

   def main() -> int:
       ds = load_from_disk("eval/dataset_with_responses")

       langfuse_handler = LangfuseCallbackHandler(
           public_key=os.environ["LANGFUSE_PUBLIC_KEY"],
           secret_key=os.environ["LANGFUSE_SECRET_KEY"],
           host=os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com"),
           trace_name="ragas-eval",
       )

       llm = ChatAnthropic(
           model="claude-sonnet-4-6",
           callbacks=[langfuse_handler],
       )

       result = evaluate(
           dataset=ds,
           metrics=[context_precision, context_recall, faithfulness, answer_relevancy],
           llm=llm,
           callbacks=[langfuse_handler],
       )

       print("\n=== RAGAS scores ===")
       for metric, score in result.items():
           flag = "PASS" if score >= THRESHOLDS.get(metric, 0) else "FAIL"
           print(f"  {metric:<30} {score:.4f}  [{flag}]")

       failed = [
           m for m, threshold in THRESHOLDS.items()
           if result.get(m, 0) < threshold
       ]
       if failed:
           print(f"\nCI GATE FAILED: {failed}")
           return 1
       print("\nCI GATE PASSED")
       return 0

   if __name__ == "__main__":
       raise SystemExit(main())
   ```

5. Run the pipeline locally to confirm all three scripts execute without error:

   ```bash
   python eval/build_dataset.py
   python eval/run_pipeline.py
   python eval/score.py
   ```

6. Add a CI step to your GitHub Actions workflow (`.github/workflows/rag-eval.yml`):

   ```yaml
   name: RAG Eval

   on:
     pull_request:
       branches: [main]

   jobs:
     ragas:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: actions/setup-python@v5
           with:
             python-version: "3.11"
         - run: pip install -r requirements-eval.txt
         - run: python eval/build_dataset.py
         - run: python eval/run_pipeline.py
           env:
             ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
         - run: python eval/score.py
           env:
             ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
             LANGFUSE_PUBLIC_KEY: ${{ secrets.LANGFUSE_PUBLIC_KEY }}
             LANGFUSE_SECRET_KEY: ${{ secrets.LANGFUSE_SECRET_KEY }}
             LANGFUSE_HOST: https://cloud.langfuse.com
   ```

7. Create `requirements-eval.txt` pinning eval-specific deps separate from your main `requirements.txt`:

   ```
   ragas>=0.1.20
   langfuse>=2.25
   langchain-anthropic>=0.3
   datasets>=2.19
   ```

## Verify

Run the scoring script and confirm exit code 0:

```bash
python eval/score.py; echo "Exit: $?"
```

Expected output ends with:

```
  faithfulness                   0.8821  [PASS]
  context_precision              0.7340  [PASS]

CI GATE PASSED
Exit: 0
```

In Langfuse, navigate to your project → Traces → filter by `trace_name=ragas-eval` — you should see one trace per eval row with LLM calls and RAGAS judge scores attached as scores.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `KeyError: 'contexts'` from RAGAS | Column named differently (e.g. `retrieved_chunks`) | Rename column in `run_pipeline.py` output to `contexts` before passing to `evaluate()` |
| `faithfulness` returns `NaN` | RAGAS LLM judge received empty `contexts` list | Ensure `query_rag()` always returns at least one context string; add a guard: `contexts = contexts or ["[no context retrieved]"]` |
| Langfuse traces not appearing | Wrong `LANGFUSE_HOST` (self-hosted vs. cloud) | Set `LANGFUSE_HOST` to your actual Langfuse instance URL; default is `https://cloud.langfuse.com` |
| CI gate passes locally but fails in CI | Non-deterministic retrieval across environments | Pin your embedding model version and Qdrant/pgvector index snapshot used in CI; use `deterministic=True` if your retriever supports it |
| `RateLimitError` during long eval runs | 50 LLM judge calls hitting Anthropic rate limits | Add `asyncio.sleep(0.5)` between rows, or use RAGAS `batch_size=5` parameter if available in your version |

## Next

- Add `rag-eval-ab-testing` — compare two retrieval strategies (BM25 vs. dense) on the same 50-item set using RAGAS delta scoring.
- Add production monitoring with `rag-eval-production-monitoring` — stream live queries into a Langfuse dataset and re-run RAGAS nightly.
- Upgrade the LLM judge from `claude-sonnet-4-6` to `claude-opus-4-7` for higher-precision faithfulness scoring on ambiguous answers.

## References

- [knowledge/geek/ai/rag-engineer/rag-eval-retrieval-metrics](../../../knowledge/geek/ai/rag-engineer/rag-eval-retrieval-metrics) — defines context_precision and context_recall formulas used directly in Step 4 metric selection
- [knowledge/geek/ai/rag-engineer/rag-eval-test-set-generation](../../../knowledge/geek/ai/rag-engineer/rag-eval-test-set-generation) — sampling strategies for constructing the 50-item question/ground-truth corpus in Step 2
- [knowledge/geek/ai/ml-ops/llm-observability-stack-2026](../../../knowledge/geek/ai/ml-ops/llm-observability-stack-2026) — Langfuse integration pattern applied in Step 4 for trace capture and score attachment
