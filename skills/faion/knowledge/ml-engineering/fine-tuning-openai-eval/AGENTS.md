# OpenAI Fine-Tuning Evaluation

## Summary

**One-sentence:** Produces an evaluation report comparing a fine-tuned OpenAI model to base on held-out test set using automated LLM-as-judge scoring and A/B comparison, with explicit pass/fail gate per metric.

**One-paragraph:** Produces an evaluation report comparing a fine-tuned OpenAI model to its base on a held-out test set. Combines automated LLM-as-judge scoring with A/B comparison on ≥2 task-relevant metrics. Eval MUST pass quality gates on accuracy / format compliance / human preference rate before deployment is approved. Each metric carries an explicit threshold, sample size, and confidence interval; the eval gate is binary per metric.

**Ефективно для:** ML інженер після fine-tune — fixed report з ft vs base ≥2 metrics; deploy лише при passed gate.

## Applies If (ALL must hold)

- Fine-tune job completed; model_id returned by OpenAI.
- Held-out test set (≥200 examples, never seen during training) is committed.
- Baseline scores on base model already recorded.
- Eval criteria documented (accuracy / format / preference / safety).
- LLM-as-judge prompt + grading rubric stable across runs.

## Skip If (ANY kills it)

- Fine-tune still running — wait for job completion.
- Held-out set leaked into training — re-split before eval.
- <200 examples in held-out — statistical noise dominates; collect more.
- Eval criteria undefined — define before running, not after.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Fine-tuned model ID | string (ft:...) | fine-tuning-openai-sft |
| Base model ID | string | ml-ops |
| Held-out test set | jsonl | eval team |
| LLM-as-judge rubric | markdown | eval team |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer/fine-tuning-openai-sft` | Supplies fine-tuned model_id. |
| `geek/ai/ml-engineer/llm-observability-stack` | Eval runs are traced for cost + latency. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules each with rationale + source. | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + self-check. | ~800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix. | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure: prepare-eval → run-ft → run-base → judge → gate-decision. | ~700 |
| `content/05-examples.xml` | medium | Worked example: tone classifier ft vs base on 300 held-out examples. | ~600 |
| `content/06-decision-tree.xml` | essential | Branch by metric pass/fail + threshold. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-eval-runner` | haiku | Wire prompts + model IDs into eval-runner. |
| `judge-with-llm` | sonnet | Run LLM-as-judge scoring per example. |
| `gate-decision` | opus | Cross-metric gate decision; surface borderline cases. |

## Templates

| File | Purpose |
|------|---------|
| `templates/openai-eval-runner.py` | Eval runner: takes ft + base IDs, runs on held-out, returns scores. |
| `templates/eval-report.md.j2` | Eval report skeleton with metrics + gate decision. |
| `templates/eval-report.md` | Eval report skeleton with metrics + gate decision. Generated from `templates/eval-report.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-fine-tuning-openai-eval.py` | Validate the eval report (scores, metrics, gate decision, CI). | Pre-merge of every eval report. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[fine-tuning-openai-sft]] — upstream.
- [[fine-tuning-openai-deployment]] — downstream; consumes the gate decision.
- [[llm-observability-stack]] — traces eval runs.

## Decision tree

Decision tree at `content/06-decision-tree.xml` decides per-metric pass/fail and the overall gate decision (deploy / hold / iterate).

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/openai-eval-runner.py`

```python
"""

# Stub — see methodology AGENTS.md ## Templates table.
```
