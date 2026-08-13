# Confidence-Thresholded Cascade

## Summary

**One-sentence:** Sends each request to a cheap model first, accepts when self-reported confidence clears a calibrated threshold, escalates otherwise, cutting cost 50-95% on mixed-difficulty traffic without quality regression.

**One-paragraph:** Send the request to a cheap model first. The cheap model returns an answer AND a confidence score. If confidence is above threshold, accept it; otherwise escalate to the expensive model. This is FrugalGPT's core insight — most production tasks are easy, and a calibrated cheap model can self-detect when it is out of its depth. Production deployments routinely report 50-95% cost reductions while matching or exceeding strong-model-only baselines on benchmarks.

**Ефективно для:** високооб'ємного трафіку класифікації, тріажу, FAQ-ботів, де якість виміряна евалом, а 70-90% запитів насправді тривіальні.

## Applies If (ALL must hold)

- High-volume traffic where cost dominates (chatbots, classifiers, batch processing).
- Task difficulty is mixed (some easy, some hard) so cascade has room to adapt.
- Latency tolerates one extra round-trip on the escalated fraction.
- Confidence is elicitable on the task (classification, factual extraction, structured output).

## Skip If (ANY kills it)

- Mission-critical decisions where any error has high cost — go straight to the strong model.
- Tasks where "confidence" is meaningless (creative writing, open-ended planning).
- Cold-start with no eval data — cheap model has not learned its limits yet.
- Latency-critical interactive flows where the second hop blows the user-perceived budget.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Eval set of 100+ tasks with ground truth | List of `{input, expected_output}` | Engineering eval pipeline |
| Cheap model output schema | Pydantic BaseModel with `reasoning`, `answer`, `confidence_0_to_1` | Application code |
| Strong model output schema | Pydantic BaseModel with `reasoning`, `answer` | Application code |
| Provider keys (cheap + strong) | Env vars or secret manager | Deployment config |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `embedded-scratchpad-field` | Reasoning must come before confidence in the cheap-model schema. |
| `enum-constraints-closed-vocabularies` | Closed answer sets stabilize confidence calibration. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Calibration + escalation rules (5 testable rules) | ~1000 |
| `content/02-output-contract.xml` | essential | CheapAnswer + StrongAnswer schemas, cascade contract | ~900 |
| `content/03-failure-modes.xml` | essential | Uncalibrated threshold, always-escalate, deep cascades | ~800 |
| `content/04-procedure.xml` | recommended | Eval → calibrate → deploy → monitor loop | ~900 |
| `content/05-examples.xml` | recommended | Customer-support, FAQ, code-review triage worked examples | ~700 |
| `content/06-decision-tree.xml` | essential | Should this task use cascade, single-strong, or three-level? | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Run the cheap leg of the cascade | haiku | This is the cheap model by definition |
| Run the escalated leg | sonnet or opus | Strong model picks up when the cheap leg defers |
| Calibrate threshold from eval data | sonnet | One-shot offline analysis, no loop |
| Design a new cascade for a new task | opus | Architectural tradeoffs across confidence elicitation, latency, cost |

## Templates

| File | Purpose |
|------|---------|
| `templates/two-level-cascade-pydantic.py` | Python implementation of two-level cascade with Pydantic + Anthropic client (covers core cascade pattern) |
| `templates/_smoke-test.json` | Minimum viable cheap-model output for self-test of the validator |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-confidence-thresholded-cascade.py` | Validates a cascade output schema and threshold settings | Pre-commit on any change to the cascade module |

## Related

- [[embedded-scratchpad-field]]
- [[enum-constraints-closed-vocabularies]]
- [[gateway-fallback-chain]]

## Decision tree

See `content/06-decision-tree.xml`. The root question asks whether the task has high volume AND elicitable confidence. The tree then branches by criticality (mission-critical → single-strong only) and by difficulty distribution (uniform → two-level enough; long-tail → three-level worth the cost). Each leaf maps to a concrete rule in `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/two-level-cascade-pydantic.py`

```python
"""Two-level cascade with Pydantic-validated cheap-model schema."""
from pydantic import BaseModel, Field
from anthropic import Anthropic

client = Anthropic()
THRESHOLD = 0.85


class CheapAnswer(BaseModel):
    reasoning: str
    answer: str
    confidence_0_to_1: float = Field(ge=0.0, le=1.0)
    requires_escalation: bool


class StrongAnswer(BaseModel):
    reasoning: str
    answer: str


def cascade(task: str) -> str:
    cheap = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=512,
        messages=[{"role": "user", "content": f"Task: {task}\nReturn STRICT JSON matching the CheapAnswer schema."}],
    )
    parsed = CheapAnswer.model_validate_json(cheap.content[0].text)
    if not parsed.requires_escalation and parsed.confidence_0_to_1 >= THRESHOLD:
        return parsed.answer
    strong = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=2048,
        messages=[{"role": "user", "content": f"Task: {task}\nReturn STRICT JSON matching the StrongAnswer schema."}],
    )
    return StrongAnswer.model_validate_json(strong.content[0].text).answer
```

### `templates/_smoke-test.json`

```json
{
  "_purpose": "smallest valid CheapAnswer for self-test",
  "_consumes": "nothing",
  "_produces": "example output matching content/02-output-contract.xml",
  "_depends_on": "content/01-core-rules.xml",
  "_token_budget_impact": "~80 tokens",
  "reasoning": "Smoke fixture for validator self-test; the input is trivial and the cheap model is highly confident.",
  "answer": "ok",
  "confidence_0_to_1": 0.92,
  "requires_escalation": false
}
```
