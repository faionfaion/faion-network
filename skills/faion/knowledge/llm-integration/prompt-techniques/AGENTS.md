# Advanced Prompt Techniques

## Summary

**One-sentence:** Production prompt-engineering toolkit — XML delimiters for injection safety, meta-prompting for optimisation, PromptChain for multi-step pipelines, PromptLibrary for versioning, and A/B harness for regression gating.

**One-paragraph:** Advanced prompting patterns, testing, and management strategies. Delimiters (XML tags, backticks) prevent injection and disambiguate sections. Meta-prompting uses an LLM to generate better prompts but produces model-specific outputs. PromptChain decouples discrete LLM steps. PromptLibrary versions prompts as committed YAML, enabling hot-fixes without redeploy. A/B tests are mandatory before promoting any prompt change to production.

**Ефективно для:** AI-інженера, що тримає продакшн-pipeline з ≥3 LLM-кроками — закриває петлю між prompt change, regression test і безпечним rollout.

## Applies If (ALL must hold)

- Prompt is underperforming and needs systematic improvement (meta-prompting + A/B).
- Pipeline has multiple discrete LLM steps to decouple into PromptChain.
- Project needs versioned PromptLibrary so prompts can be updated without code deploys.
- Need to validate prompt accuracy against a known test set before release.
- Prompt injection or delimiter confusion is causing failures.

## Skip If (ANY kills it)

- Single-call use case — `prompt-basics` is sufficient.
- No golden test set exists — meta-prompting and A/B both need ground truth.
- Latency budget &lt; 1s end-to-end — multi-call chains break it.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Existing PromptTemplate | code | `prompt-basics` |
| Golden test set | list[dict] with input + expected | curated by domain expert |
| LLM client | object | pipeline SDK init |
| Eval metric | callable | per-task accuracy / BLEU / F1 |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/llm-integration/prompt-basics` | PromptTemplate is the unit chained by PromptChain. |
| `geek/ai/llm-integration/openai-chat-completions` | The retry-client wraps every chain step. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: XML delimiters mandatory, meta-prompt outputs reviewed by human, chain step idempotency, A/B before promote, version YAML, regression block | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for PromptLibrary entry (slug, version, model, prompt, eval_score) | ~800 |
| `content/03-failure-modes.xml` | essential | 5 failure modes: model-specific meta-prompt, chain partial-failure, golden drift, untested promote, delimiter collision | ~900 |
| `content/04-procedure.xml` | deep | 7-step procedure: baseline → meta-prompt → A/B → diff → promote → snapshot → monitor | ~800 |
| `content/06-decision-tree.xml` | essential | Picks meta-prompting vs manual tuning, single-step vs chain | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `generate-meta-prompt` | opus | Cross-prompt synthesis; the model needs to understand failure modes. |
| `apply-meta-prompt` | sonnet | Domain-aware rewrite. |
| `score-ab-results` | haiku | Mechanical metric computation. |

## Templates

| File | Purpose |
|------|---------|
| `templates/prompt-library.yaml` | Schema for versioned PromptLibrary entries (slug, version, model, prompt, eval_score). |
| `templates/prompt-chain.py` | PromptChain class composing PromptTemplate steps with error propagation. |
| `templates/ab-test-harness.py` | A/B harness comparing two PromptLibrary versions against a golden set. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-prompt-techniques.py` | Validate a PromptLibrary entry JSON matches the output contract. | Pre-merge in CI; nightly drift scan. |

## Related

- [[prompt-basics]] — base PromptTemplate.
- [[chain-of-thought]] — one chaining pattern.
- [[structured-output-patterns]] — output-shape enforcement.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` picks (a) meta-prompting vs manual tuning by failure-mode count, (b) single PromptTemplate vs PromptChain by step independence, and (c) A/B vs replace by deployment risk. Use it before authoring any new prompt change.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/prompt-library.yaml`

```yaml
entries:
  - slug: summary-3-bullet
    version: v2
    model: gpt-4o-mini
    prompt: |
      You are a precise summariser.

      <document>
      {document}
      </document>

      Output:
      - Exactly 3 bullet points
      - Each bullet <= 15 words
      - Factual tone, no opinion
    eval_score: 0.92
    golden_set_id: summary-bench-2026q2
    created_at: "2026-05-22T12:00:00Z"
    owner: ml-eng:alice
    ab_record_id: ab_2026_05_21_summary_v1_v2

  - slug: sentiment-classifier
    version: v1
    model: gpt-4o-mini
    prompt: |
      You classify sentiment. Respond with ONLY one word from {positive, negative, neutral}.

      <text>{text}</text>
    eval_score: 0.95
    golden_set_id: sentiment-3way-2026
    created_at: "2026-04-10T09:00:00Z"
    owner: ml-eng:bob
```

### `templates/prompt-chain.py`

```python
"""
from dataclasses import dataclass
from typing import Callable, Any


@dataclass
class ChainStep:
    name: str
    template_render: Callable[[dict], list[dict]]
    output_key: str


def run_chain(steps: list[ChainStep], llm_call: Callable[[list[dict]], str], context: dict) -> dict:
    """Run an idempotent chain of LLM steps.

    `llm_call(messages)` -> content string (use the retry-client wrapper).
    Each step writes its output to `context[step.output_key]`.
    """
    ctx = dict(context)
    for step in steps:
        messages = step.template_render(ctx)
        if not messages or messages[0].get("role") != "system":
            raise ValueError(f"step {step.name}: rendered messages must start with system role")
        result = llm_call(messages)
        if step.output_key in ctx:
            raise KeyError(f"step {step.name}: output_key '{step.output_key}' would overwrite existing context entry")
        ctx[step.output_key] = result
    return ctx


def commit_sink(ctx: dict, sink: Callable[[dict], Any]) -> Any:
    """Run any external side-effects ONCE after the chain completes.

    Chain steps are idempotent transforms; the sink is the only place state changes.
    """
    return sink(ctx)
```

### `templates/ab-test-harness.py`

```python
"""
from dataclasses import dataclass, field
from typing import Callable
import statistics


@dataclass
class AbRecord:
    baseline_score: float
    candidate_score: float
    lift_pct: float
    per_case_regressions: list[tuple[int, float]] = field(default_factory=list)

    def passes_gate(self, max_per_case_regression_pct: float = 5.0, min_lift_pct: float = 0.0) -> bool:
        if self.lift_pct < min_lift_pct:
            return False
        return all(reg < max_per_case_regression_pct for _, reg in self.per_case_regressions)


def run_ab(
    baseline_render: Callable[[dict], list[dict]],
    candidate_render: Callable[[dict], list[dict]],
    golden_set: list[tuple[dict, str]],
    llm_call: Callable[[list[dict]], str],
    metric: Callable[[str, str], float],
) -> AbRecord:
    """Run A/B on golden set, return AbRecord with lift and per-case regression list."""
    baseline_scores, candidate_scores = [], []
    for i, (inputs, expected) in enumerate(golden_set):
        b = metric(llm_call(baseline_render(inputs)), expected)
        c = metric(llm_call(candidate_render(inputs)), expected)
        baseline_scores.append(b)
        candidate_scores.append(c)
    baseline = statistics.mean(baseline_scores)
    candidate = statistics.mean(candidate_scores)
    lift_pct = (candidate - baseline) * 100 if baseline else 0.0
    regressions = [
        (i, (b - c) * 100)
        for i, (b, c) in enumerate(zip(baseline_scores, candidate_scores))
        if c < b
    ]
    return AbRecord(baseline, candidate, lift_pct, regressions)
```
