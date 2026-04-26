# Agent Integration — Model Evaluation

## When to use
- Selecting between two or more candidate models for a production use case
- Before promoting a prompt change or model upgrade to production
- After fine-tuning to verify quality improvement versus base model
- Setting up continuous monitoring that fires alerts when quality drifts below threshold
- Running A/B tests to compare a new model against the current production model

## When NOT to use
- The task is trivial and any capable model passes — skip formal evaluation, ship
- No baseline exists yet — gather production data first, then evaluate against it
- Purely synthetic benchmarks when the task domain is highly specific — use real query samples
- Budget does not allow for LLM-as-judge at scale — use cheaper automated metrics first

## Where it fails / limitations
- Benchmark saturation: MMLU and HumanEval are near-ceiling for top models; scores compress differences that matter in production
- Data contamination is endemic — models trained on benchmark data report inflated scores; LiveCodeBench and similar dynamic benchmarks partially mitigate this
- LLM-as-judge has evaluator bias — GPT-4 prefers GPT-4 outputs; Claude prefers Claude outputs; use multi-judge or human calibration to correct
- Automated metrics (BLEU, ROUGE) correlate poorly with human preference for open-ended generation
- Evaluation results on a static test set decay as production query distribution shifts — re-evaluate quarterly or after major user behavior changes
- Cost of evaluation scales with corpus size and LLM-as-judge usage — evaluating 10K samples with Claude as judge can cost $50–200

## Agentic workflow
Agents run evaluation in two modes: offline (batch over a test dataset) and online (sampling production traffic). For offline evaluation, an agent iterates the test dataset, calls the model under test, runs automated metrics and LLM-as-judge scoring, aggregates results, and writes a structured report. For online evaluation, an agent samples 1–5% of production requests, runs asynchronous quality scoring, and writes metrics to a monitoring dashboard. The agent must NOT make model selection decisions autonomously — it produces the report and hands off to a human.

### Recommended subagents
- `faion-sdd-executor-agent` — when evaluation is a gated quality step in an SDD feature pipeline
- General Claude (Sonnet) subagent — as LLM-as-judge evaluator for individual output scoring

### Prompt pattern
LLM-as-judge rubric prompt:
```xml
<evaluation>
  <role>Objective quality evaluator</role>
  <question>{question}</question>
  <reference>{reference_answer}</reference>
  <candidate>{model_output}</candidate>
  <criteria>
    - Factual accuracy (0-3): Does the answer contain verifiable facts matching the reference?
    - Completeness (0-3): Does the answer address all parts of the question?
    - Clarity (0-2): Is the answer concise and unambiguous?
    - Hallucination (0-2): Does the answer introduce false information not in reference?
  </criteria>
  <output>JSON: {"accuracy": N, "completeness": N, "clarity": N, "hallucination": N, "total": N, "reason": "..."}</output>
</evaluation>
```

```python
# Batch evaluation runner
import asyncio
from anthropic import AsyncAnthropic

client = AsyncAnthropic()

async def evaluate_sample(question: str, reference: str, candidate: str) -> dict:
    response = await client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=500,
        messages=[{"role": "user", "content": JUDGE_PROMPT.format(
            question=question, reference=reference, candidate=candidate
        )}],
    )
    return parse_json(response.content[0].text)

async def run_evaluation(dataset: list[dict]) -> list[dict]:
    tasks = [evaluate_sample(d["q"], d["ref"], d["output"]) for d in dataset]
    return await asyncio.gather(*tasks)
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ragas` | RAG-specific evaluation metrics | `pip install ragas` · docs.ragas.io |
| `deepeval` | Comprehensive LLM evaluation framework | `pip install deepeval` · deepeval.com |
| `lm-evaluation-harness` | Standard benchmark runner (EleutherAI) | `pip install lm-eval` · github.com/EleutherAI/lm-evaluation-harness |
| `openai/evals` | OpenAI eval framework | `pip install evals` · github.com/openai/evals |
| `trulens` | Feedback functions, RAG triad | `pip install trulens-eval` · trulens.org |
| `langsmith` | LLM tracing + eval | `pip install langsmith` · smith.langchain.com |
| `evidently` | Data/model drift monitoring | `pip install evidently` · evidentlyai.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| LangSmith | SaaS | Yes — SDK | Dataset management, LLM-as-judge, A/B comparison |
| Langfuse | SaaS/OSS | Yes — SDK | Open-source eval + tracing; dataset versioning |
| Braintrust | SaaS | Yes — SDK | Eval-centric platform; real-time scoring |
| Scale AI Eval | SaaS | Partial | Human annotation + automated metrics |
| Weights & Biases | SaaS/OSS | Yes — SDK | Experiment tracking; model comparison dashboards |
| Helicone | SaaS | Yes — proxy | Request logging + LLM evaluation; cost tracking |
| AWS Bedrock Model Eval | SaaS | Yes — AWS SDK | Native AWS; automatic and human eval |

## Templates & scripts
See `templates.md` for a full evaluation pipeline template with dataset management and reporting.

Inline: automated metric computation (< 40 lines):

```python
from rouge_score import rouge_scorer
from bert_score import score as bert_score
import numpy as np

def compute_metrics(predictions: list[str], references: list[str]) -> dict:
    scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
    rouge_scores = [scorer.score(ref, pred) for pred, ref in zip(predictions, references)]
    P, R, F1 = bert_score(predictions, references, lang="en", verbose=False)
    return {
        "rouge1_f": np.mean([s["rouge1"].fmeasure for s in rouge_scores]),
        "rouge2_f": np.mean([s["rouge2"].fmeasure for s in rouge_scores]),
        "rougeL_f": np.mean([s["rougeL"].fmeasure for s in rouge_scores]),
        "bert_f1": F1.mean().item(),
        "n_samples": len(predictions),
    }
```

## Best practices
- Build your evaluation dataset from real production queries, not synthetic ones — 200 samples minimum
- Always run at least two evaluation passes per output: automated metric + LLM-as-judge, and report both
- Use multiple judge models (GPT-4 + Claude) and average scores to reduce evaluator bias
- Version your test datasets alongside your model/prompt versions — evaluation results are only comparable if datasets match
- Report confidence intervals (bootstrap or standard error) for all aggregate scores — single-point estimates hide variance
- Separate retrieval evaluation from generation evaluation in RAG systems — a bad retrieval score masks good generation and vice versa
- Run evals in CI: block deployment if quality drops > 5% on core metrics versus the production baseline

## AI-agent gotchas
- LLM-as-judge is itself a model call — it has the same failure modes as the system under test; agents must handle judge API errors gracefully
- Agents running batch evaluation must rate-limit concurrent LLM calls — parallel evaluation of 1000 samples at 50 concurrent calls will hit API rate limits
- Self-evaluation (asking the same model that generated the answer to also judge it) is systematically biased toward its own outputs — always use a different judge model
- Evaluation agents should not cache LLM-as-judge results across prompt versions — stale evaluations from a prior prompt version will corrupt comparisons
- Automated metrics correlate poorly with human preference for generation tasks — agents reporting only ROUGE/BLEU scores may mislead stakeholders about actual quality

## References
- https://crfm.stanford.edu/helm/ (HELM)
- https://github.com/EleutherAI/lm-evaluation-harness
- https://github.com/openai/evals
- https://docs.ragas.io/
- https://deepeval.com/
- https://www.evidentlyai.com/llm-guide/llm-benchmarks
- https://huggingface.co/spaces/OpenEvals/evaluation-guidebook
