# Embedded Scratchpad Field

## Summary

**One-sentence:** Embeds a reasoning, plan_steps, evidence, or scratchpad field before the answer in structured-output schemas so the model externalises working notes inside strict JSON mode, lifting accuracy 30-60% on multi-step tasks.

**One-paragraph:** Before any non-trivial answer field, embed a scratchpad / plan_steps / reasoning / evidence field IN the schema. The model writes its working notes there before generating the answer. This is structured-output's equivalent of thinking tags but works even in strict JSON mode where free-form preambles are not allowed. AWS Bedrock guidance reports ~60% accuracy improvement on GSM8k by adding a single reasoning field; Tab-CoT papers show similar lifts on multi-criteria decisions.

**Ефективно для:** структурованого виводу під strict JSON, де модель має одночасно міркувати і повертати чисту JSON-форму — поле scratchpad дозволяє "подумати вголос" без порушення схеми.

## Applies If (ALL must hold)

- Strict JSON mode is in use (no free-form preamble allowed by the decoder).
- The downstream answer benefits from intermediate reasoning steps.
- The task has more than one logical reasoning hop.
- "Model commits before thinking" is an observed failure mode on the current task.

## Skip If (ANY kills it)

- Pure transformation tasks where reasoning adds latency without accuracy.
- Upstream model is already a reasoning model (o-series, Opus extended thinking) — paying twice.
- Trivial fields where the schema is already forcing the model through an enum.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Output schema | Pydantic BaseModel or JSON Schema | Application code |
| Sample tasks | List of inputs with expected answers | Evaluation set |
| Baseline accuracy | Number from running schema without scratchpad | Eval harness |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `field-descriptions-as-prompts` | Scratchpad descriptions must name WHAT to think about, not just "think". |
| `inverted-header-content-first` | Scratchpad-first is the most important application of field-order discipline. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Five testable rules: before-answer placement, name-by-task-type, length cap, descriptions, no-double-CoT | ~1000 |
| `content/02-output-contract.xml` | essential | Five variants (reasoning, plan_steps, evidence, scratchpad, tab_cot) with schemas | ~900 |
| `content/03-failure-modes.xml` | essential | Scratchpad-after-answer, multiple-competing-scratchpads, empty descriptions | ~700 |
| `content/06-decision-tree.xml` | essential | Pick the right variant for the task | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Add scratchpad to existing schema | haiku | Mechanical schema edit |
| Audit codebase schemas for missing scratchpads | sonnet | Pattern detection across files |
| Design tab-CoT for novel math/reasoning task | opus | Step-decomposition needs deeper analysis |

## Templates

| File | Purpose |
|------|---------|
| `templates/reasoning-before-verdict.py` | Pydantic schema with reasoning field before confidence and decision |
| `templates/_smoke-test.json` | Minimum valid verdict object for the validator |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-embedded-scratchpad-field.py` | Validates a schema instance and checks scratchpad placement | Pre-commit on schema changes |

## Related

- [[field-descriptions-as-prompts]]
- [[inverted-header-content-first]]
- [[confidence-thresholded-cascade]]

## Decision tree

See `content/06-decision-tree.xml`. The root question asks whether the task is multi-step and benefits from CoT. Branches then pick the scratchpad variant by task shape (decision → `reasoning`, multi-step → `plan_steps`, classification → `evidence`, math → `tab_cot`, free-form → `scratchpad`). Each leaf maps to a rule in `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/reasoning-before-verdict.py`

```python
"""Reasoning-before-verdict template.

Schema field order = autoregressive generation order. The reasoning field
appears first so the model writes its working notes before committing to
confidence and decision. Strict mode + this schema reliably lifts accuracy
on multi-criteria decision tasks vs an answer-only schema.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Verdict(BaseModel):
    model_config = ConfigDict(extra="forbid")

    reasoning: str = Field(
        description=(
            "Step-by-step analysis of the input against each criterion. "
            "Cap at 200 words. Cover: which criteria are met, which are "
            "borderline, which are missed."
        ),
        min_length=4,
        max_length=2000,
    )
    confidence: Literal["low", "medium", "high"] = Field(
        description="Confidence in the decision below; medium if any criterion is borderline."
    )
    decision: Literal["approve", "reject"] = Field(
        description="Final call. Must follow from reasoning above."
    )
```

### `templates/_smoke-test.json`

```json
{
  "_purpose": "smallest valid verdict object for the validator",
  "_consumes": "nothing",
  "_produces": "example Verdict matching the schema",
  "_depends_on": "content/01-core-rules.xml, content/02-output-contract.xml",
  "_token_budget_impact": "~80 tokens",
  "reasoning": "Three of four criteria are clearly met; the fourth is borderline but precedent supports approval.",
  "confidence": "medium",
  "decision": "approve"
}
```
