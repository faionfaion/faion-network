# LLM Decision Framework

## Summary

**One-sentence:** Produces an LLM-strategy ADR choosing prompt-engineering / RAG / fine-tuning / RAFT-hybrid against scored constraints (data freshness, accuracy, budget, latency, team).

**One-paragraph:** Produces an LLM-strategy ADR. Systematic framework for choosing the right LLM enhancement strategy — prompt engineering, RAG, fine-tuning, or RAFT (hybrid) — based on data freshness, accuracy requirements, budget, latency, and team constraints. Always score prompting first before investing in retrieval or training infrastructure; capture the score sheet in the ADR for auditable reversal later.

**Ефективно для:** ML лід на старті проекту — fixed ADR з оцінкою prompt/RAG/FT/RAFT, не давати рішенню затягтись хайпом.

## Applies If (ALL must hold)

- Starting a new LLM-powered feature OR re-evaluating an existing one.
- Choice between prompt-only, RAG, fine-tune, RAFT (RAG + fine-tune) is genuinely open.
- Stakeholders disagree on path — need an evidence-anchored decision.
- Org wants an auditable decision record for compliance / hiring / audit.
- Budget envelope known (one-off $ + recurring $/month).

## Skip If (ANY kills it)

- Decision already made and committed — skip; redo on material change.
- Single trivial feature with no recurring cost — over-engineering.
- Pre-revenue prototype phase — score lightly, revisit at growth.
- Constraints unstable (target moves weekly) — not enough signal to commit.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Use-case description | markdown | product |
| Constraints sheet (accuracy/freshness/latency/budget) | yaml | ML lead |
| Team skill inventory | markdown | engineering manager |
| Sample queries | jsonl | product |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer/finetuning` | Downstream for fine-tune branch. |
| `geek/ai/ml-engineer/llamaindex` | Downstream for RAG branch. |
| `geek/ai/ml-engineer/cost-optimization` | Cost-scoring inputs. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules each with rationale + source. | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + self-check. | ~800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix. | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure: gather-constraints → score-prompting → score-rag → score-ft → pick-and-write-adr. | ~700 |
| `content/06-decision-tree.xml` | essential | Branch by accuracy / freshness / budget / latency. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `score-prompting` | sonnet | Run prompting baseline on sample queries; record metric. |
| `score-rag` | sonnet | Stand up cheap RAG; score same queries. |
| `write-adr` | opus | Cross-cutting synthesis; surface real trade-offs. |

## Templates

| File | Purpose |
|------|---------|
| `templates/adr.md.j2` | ADR skeleton with score sheet + alternatives + consequences. |
| `templates/adr.md` | ADR skeleton with score sheet + alternatives + consequences. Generated from `templates/adr.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/decision-matrix.py` | Score → recommendation calculator. |
| `templates/prompt-requirements.txt` | Constraint-elicitation prompt. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-llm-decision-framework.py` | Validate the ADR (scores per option, chosen, rationale, alternatives). | Pre-merge of every LLM ADR PR. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[finetuning]] — downstream when FT chosen.
- [[llamaindex]] — downstream when RAG chosen.
- [[cost-optimization]] — input to budget scoring.

## Decision tree

Decision tree at `content/06-decision-tree.xml` walks (accuracy gap, data freshness, budget, latency, team skill) and lands on prompt / RAG / FT / RAFT.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/decision-matrix.py`

```python
"""

"""LLM architecture decision scoring matrix."""
from dataclasses import dataclass
from typing import Literal


@dataclass
class TaskProfile:
    """Profile of a task to route to the right LLM architecture."""
    example_count: int            # labeled training examples available
    knowledge_changes: bool       # does the knowledge update frequently?
    latency_budget_ms: int        # acceptable p50 latency
    monthly_calls: int            # expected API calls per month
    accuracy_required: float      # 0.0-1.0 required accuracy
    privacy_required: bool        # must not send data to 3rd party


def score_approach(profile: TaskProfile) -> dict[str, float]:
    """Score each approach 0-10 for this task profile."""
    scores: dict[str, float] = {
        "prompt_engineering": 0.0,
        "rag": 0.0,
        "fine_tuning": 0.0,
        "raft": 0.0,
    }

    # Prompt engineering: fast, no infra, limited by model capability
    scores["prompt_engineering"] = 8.0
    if profile.accuracy_required > 0.90:
        scores["prompt_engineering"] -= 3.0
    if profile.example_count > 100:
        scores["prompt_engineering"] -= 1.0

    # RAG: good for knowledge-intensive, frequently changing data
    scores["rag"] = 6.0
    if profile.knowledge_changes:
        scores["rag"] += 3.0
    if profile.example_count < 500:
        scores["rag"] += 1.0
    if profile.latency_budget_ms < 500:
        scores["rag"] -= 2.0

    # Fine-tuning: best for stable patterns, high volume, style/format
    scores["fine_tuning"] = 5.0
    if profile.example_count >= 1000:
        scores["fine_tuning"] += 3.0
    if profile.knowledge_changes:
        scores["fine_tuning"] -= 4.0
    if profile.monthly_calls > 100_000:
        scores["fine_tuning"] += 2.0
    if profile.privacy_required:
        scores["fine_tuning"] += 1.0

    # RAFT: combines RAG + fine-tuning for domain synthesis
    scores["raft"] = 4.0
    if profile.example_count >= 500 and profile.knowledge_changes:
        scores["raft"] += 4.0
    if profile.accuracy_required > 0.95:
        scores["raft"] += 2.0

    return {k: max(0.0, min(10.0, v)) for k, v in scores.items()}


def recommend(profile: TaskProfile) -> str:
    """Return the recommended approach for this task profile."""
    scores = score_approach(profile)
    return max(scores, key=lambda k: scores[k])
```

### `templates/prompt-requirements.txt`

```text
-->

You are an ML architect assistant. Help the user determine the correct LLM architecture for their task by gathering requirements and scoring approaches.

Step 1: Ask these questions one at a time (do not ask all at once):
1. Describe the task in one sentence — what does the model need to produce?
2. How many labeled input-output examples do you have (or can create within 2 weeks)?
3. Does the knowledge the model needs change frequently (weekly/monthly)?
4. What is the acceptable latency for a user-facing response (in milliseconds)?
5. What accuracy level is required — what failure rate is acceptable?
6. What is the monthly call volume expected?
7. Are there privacy constraints preventing sending data to third-party APIs?

Step 2: After gathering answers, score each approach:
- Prompt engineering: zero data, fast, limited accuracy ceiling
- RAG: best for frequently changing knowledge, needs vector DB infra
- Fine-tuning: needs 500+ examples, stable task, high volume
- RAFT: combines RAG+fine-tuning, highest quality, highest complexity

Step 3: Recommend ONE approach with clear rationale. Format:

RECOMMENDATION: [approach]

RATIONALE:
- [Primary reason based on their answers]
- [Why alternatives were ruled out]

NEXT STEPS:
1. [Concrete first action]
2. [Second action]
3. [Evaluation plan]

RISKS:
- [Main risk of the recommended approach]
- [Mitigation]

Do not recommend fine-tuning unless the user has confirmed 500+ examples and tried prompt engineering first.
```
