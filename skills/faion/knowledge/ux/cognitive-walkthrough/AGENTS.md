# Cognitive Walkthrough

## Summary

**One-sentence:** Produces a cognitive-walkthrough report stepping through a known-correct action sequence and answering 4 questions per step about learnability.

**One-paragraph:** Structured expert-inspection method evaluating interface learnability: walk through a known-correct action sequence; for each step answer four questions — will the user try to achieve the right effect; will they notice the correct action is available; will they associate the action with the effect; will they see progress indicating success. Output is per-step Q1-Q4 + severity + recommendation, plus an executive rollup.

**Ефективно для:**

- First-use learnability evaluation: новий користувач без training.
- Cheaper than usability testing for early-stage flows.
- Surface label / discoverability проблеми перед recruiting тестерів.
- B2B / regulated tools де real-user testing коштує занадто дорого.

## Applies If (ALL must hold)

- Evaluating learnability for first-time users of a defined task.
- A canonical correct action sequence exists.
- Expert evaluators (2-3) are available to run the walkthrough.

## Skip If (ANY kills it)

- Mature product evaluation — heuristic evaluation or A/B test is better suited.
- Tasks without a canonical correct sequence — walkthrough is moot.
- Speed/efficiency evaluation — walkthrough measures learnability, not throughput.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Task definition | step-by-step correct sequence | PM |
| Target user profile | persona | research |
| 2-3 expert evaluators | names | team |
| UI to evaluate | prototype or production | design |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[personas]] | User profile sourced from personas |
| [[contextual-inquiry]] | Complement: contextual inquiry feeds task definitions |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure | 800 |
| `content/05-examples.xml` | essential | Worked example with note | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree routing to rules | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `primary-analysis` | sonnet | Domain-specific judgement. |
| `structured-output-assembly` | sonnet | Schema-conforming JSON build. |
| `validate` | haiku | Deterministic schema check. |

## Templates

| File | Purpose |
|------|---------|
| `templates/walkthrough-plan.md` | Walkthrough planning sheet: task, profile, evaluators, schedule |
| `templates/evaluation-form.md` | Per-step evaluation form with Q1-Q4 |
| `templates/summary-report.md` | Executive rollup of findings + severity counts |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-cognitive-walkthrough.py` | Validate artefact JSON against output schema | Pre-commit / CI on artefact change |

## Related

- [[personas]]
- [[contextual-inquiry]]
- [[accessibility-evaluation]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes from observable inputs to a rule-grounded conclusion, every leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
