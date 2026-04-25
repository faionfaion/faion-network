# Agent Integration — Evaluation Framework

## When to use
- Building a reusable offline evaluation harness for LLM features that runs in CI before deployment
- Implementing LLM-as-judge to assess complex outputs where no ground-truth metric exists (helpfulness, coherence, instruction-following)
- Running pairwise A/B comparisons between two prompt versions or model versions
- Setting up a quality gate that blocks deployment if metric thresholds are not met
- Creating a production sampling evaluator that continuously monitors output quality

## When NOT to use
- The system has fewer than 30 test cases — `ModelEvaluator` results are statistically unreliable at this scale; build the dataset first
- The task requires human preference evaluation as the primary signal — LLM-as-judge has known biases (position bias, verbosity bias) and cannot substitute for user studies on subjective tasks
- Evaluation latency matters — `LLMJudge` makes one API call per evaluated case; at 1000 cases this adds significant wall-clock time and cost
- The output format is non-text (images, audio, structured data) — this framework handles text outputs only

## Where it fails / limitations
- `LLMJudge` returns scores from 1-5 with JSON parsing — if the judge model produces malformed JSON, the evaluation silently returns an error dict instead of raising; the caller must check for `error` keys
- Pairwise comparison has position bias: the response listed first tends to be preferred by LLM judges ~55-60% of the time; run comparisons with A/B and B/A ordering and average results
- `ModelEvaluator` sets `temperature` implicitly from model defaults; for reproducible evaluation always explicitly set `temperature=0` in the API call
- `_aggregate_results` uses simple mean for all metrics; for skewed distributions (e.g., latency) use median and p95
- The `ProductionEvaluator` stores all evaluation logs in memory — unbounded growth in a long-running process; add periodic flush to a persistent store
- `should_evaluate` uses `random.random()` which is not seeded — evaluation sample is not reproducible across runs; for debugging, set a random seed

## Agentic workflow
An agent driving evaluation should instantiate `ModelEvaluator` with a frozen test dataset and metric set, run evaluation at `temperature=0`, compare aggregate results against pre-defined thresholds, and return a pass/fail verdict with the metric summary. For LLM-as-judge, the agent should use `evaluate_batch` with 3-5 criteria relevant to the task type, then aggregate scores and flag cases below the threshold for human review. Production sampling can run as a background subagent that processes evaluation results and pushes alerts when quality drops.

### Recommended subagents
- `faion-sdd-executor-agent` — drives evaluation framework setup from an SDD task card
- A quality-gate subagent (custom) — runs `ModelEvaluator.evaluate()` against the CI test dataset, returns pass/fail verdict with full metric JSON for the CI system to consume
- An LLM-judge subagent (custom) — runs `LLMJudge.evaluate_batch()` on a sampled set of production outputs, returns cases with overall score < 3 for human review

### Prompt pattern
```
Evaluate this LLM output using the following criteria:
- accuracy: Does the response contain factually correct information?
- completeness: Does it address all parts of the user question?
- format: Does it follow the required output format: {format_spec}?

Input: {user_input}
Response: {model_output}
Reference (if available): {reference}

Return JSON: {"scores": {"criterion": {"score": 1-5, "explanation": str}}, "overall": float, "pass": bool}
where pass=true if overall >= 3.5.
```

```
Compare Response A and Response B for the following criterion: {criterion}.
Input: {user_input}
Response A: {output_a}
Response B: {output_b}

To avoid position bias, consider both orderings. Return:
{"winner": "A"|"B"|"tie", "confidence": 0.0-1.0, "explanation": str}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `openai` SDK | `ModelEvaluator` calls, `LLMJudge` via `response_format=json_object` | `pip install openai` |
| `anthropic` SDK | Use Claude as judge for less OpenAI self-serving bias | `pip install anthropic` / [docs.anthropic.com](https://docs.anthropic.com) |
| `ragas` | RAG-specific evaluation framework (faithfulness, context precision) | `pip install ragas` / [docs.ragas.io](https://docs.ragas.io/) |
| `evaluate` (HuggingFace) | Metric implementations compatible with `ModelEvaluator` | `pip install evaluate` |
| `deepeval` | Test-driven LLM evaluation framework | `pip install deepeval` / [deepeval.com](https://deepeval.com) |
| `pytest` | Run `ModelEvaluator` as part of CI test suite | `pip install pytest` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| OpenAI Evals | OSS | Yes — YAML/Python eval definitions | Standardized eval runner; integrates with OpenAI API |
| Braintrust | SaaS | Yes — SDK with eval primitives | Built-in LLM-as-judge, dataset versioning, CI integration |
| Langfuse | SaaS/OSS | Yes — `langfuse.evaluation` module | Attach scores to traces; human annotation UI |
| Arize Phoenix | SaaS/OSS | Yes — `phoenix.evals` | Strong LLM-as-judge templates for RAG and classification |
| PromptFoo | OSS | Yes — YAML config, CLI-driven | Fast offline eval with LLM-as-judge support |
| DeepEval | OSS + SaaS | Yes — pytest-style assertions | LLM metrics as unit tests; CI-friendly |

## Templates & scripts
See `templates.md` for full evaluation harness with CI integration.

Inline — minimal CI quality gate using `ModelEvaluator` (≤40 lines):

```python
import json
from openai import OpenAI
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class EvaluationCase:
    input: str
    expected_output: Optional[str] = None
    metadata: dict = None

def exact_match(input: str, actual: str, expected: Optional[str]) -> Optional[float]:
    if expected is None:
        return None
    return 1.0 if actual.strip() == expected.strip() else 0.0

def run_ci_gate(
    test_cases: List[EvaluationCase],
    system_prompt: str,
    thresholds: dict,
    model: str = "gpt-4o-mini",
) -> dict:
    client = OpenAI()
    results = []
    for case in test_cases:
        resp = client.chat.completions.create(
            model=model, temperature=0,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": case.input},
            ],
        )
        output = resp.choices[0].message.content
        metrics = {"exact_match": exact_match(case.input, output, case.expected_output)}
        results.append({"output": output, "metrics": metrics})
    means = {}
    for metric in thresholds:
        vals = [r["metrics"].get(metric) for r in results if isinstance(r["metrics"].get(metric), float)]
        means[metric] = sum(vals) / len(vals) if vals else 0.0
    passed = all(means.get(m, 0) >= t for m, t in thresholds.items())
    return {"passed": passed, "means": means, "thresholds": thresholds}
```

## Best practices
- Use `temperature=0` for all evaluation runs — stochastic outputs make metric comparisons between runs unreliable; save creative temperature for production
- For LLM-as-judge, use a more capable model than the one being evaluated — judge the output of `gpt-4o-mini` with `gpt-4o`; evaluating with the same model introduces self-preference bias
- Run pairwise comparisons with both orderings (A vs B and B vs A) and average the results — position bias is real and measurable (~5-10% swing)
- Include adversarial cases in the test set — cases where the model commonly fails (ambiguous instructions, edge cases, long inputs) are more valuable than easy cases for quality gating
- Separate `EvaluationCase` datasets by task type (classification, QA, generation) — mixing task types in one run makes metric aggregation meaningless
- Version test datasets in version control alongside prompt versions — changes to either should trigger a new evaluation run to detect regressions

## AI-agent gotchas
- `response_format={"type": "json_object"}` requires the word "JSON" to appear in the system or user prompt — LLM-as-judge prompts that don't include it will raise an API error
- `LLMJudge.evaluate_batch` makes synchronous API calls sequentially — at 100 cases with 1s latency each, this takes 100s; parallelize with `asyncio` or `concurrent.futures` for large batches
- JSON parsing of judge responses fails silently in the current implementation — add `try/except json.JSONDecodeError` around `json.loads()` and return a default "error" result
- The production `ProductionEvaluator` has a subtle bug: it only calls `LLMJudge` when `sample_rate < 0.05`, but compares `self.config.sample_rate` not the actual evaluated count — high-volume systems at 5% sample rate will never get judge scores
- Automated evaluation with LLM-as-judge is a human-in-loop breakpoint for critical decisions — agents should not autonomously block production deployments based solely on LLM judge scores without human review of the threshold calibration

## References
- [OpenAI Evals](https://github.com/openai/evals)
- [RAGAS — RAG Evaluation](https://docs.ragas.io/)
- [DeepEval](https://deepeval.com)
- [PromptFoo](https://github.com/promptfoo/promptfoo)
- [Braintrust Evaluation](https://www.braintrust.dev/docs/guides/evals)
- [Arize Phoenix Evals](https://docs.arize.com/phoenix/evaluation)
- [LLM-as-Judge (Zheng et al., 2023)](https://arxiv.org/abs/2306.05685)
