# Design Critique

## Summary

**One-sentence:** Run a structured design critique session that ties feedback to design goals and user evidence so designers leave with concrete next actions, not opinions.

**One-paragraph:** Run a structured design critique session that ties feedback to design goals and user evidence so designers leave with concrete next actions, not opinions.

**Ефективно для:**

- Solo founders or small teams shipping under time pressure.
- Cross-functional reviewers needing a shared, evidence-grounded artefact.
- Methodology owners maintaining quality gates over time.
- Subagent pipelines that need a deterministic output shape.

## Applies If (ALL must hold)

- Design artefact has stated goals and at least one persona reference.
- Critique can be held with three to six relevant reviewers.
- Designer wants actionable feedback, not approval.
- Time-box of 45 to 90 minutes is feasible.
- Decisions made in the session will be logged and revisited.

## Skip If (ANY kills it)

- Reviewers cannot reference the user or the goal — feedback will be taste-driven.
- Goal is to get sign-off, not feedback — use a decision review instead.
- Designer is not present to defend or capture rationale.
- Group is larger than seven — split into focused mini-critiques.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Design artefact | figma / pdf | Designer |
| Goal and persona reference | markdown | Product brief |
| Critique rubric | markdown | Design ops |
| Decision log template | markdown | Design ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ux-ui-designer/heuristic-evaluation` | Heuristics anchor objective critique points. |
| `solo/ux/ux-researcher/usability-testing` | Behaviour data, when available, sharpens the conversation. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules + run/skip rules | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-artefact` | sonnet | Section-by-section judgement against the rubric. |
| `lint-and-validate` | haiku | Deterministic schema validation + forbidden-pattern check. |
| `final-review` | opus | Cross-section coherence and stakeholder readiness. |

## Templates

| File | Purpose |
|------|---------|
| `templates/design-critique.json` | JSON skeleton conforming to the output contract schema. |
| `templates/design-critique.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-design-critique.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[heuristic-evaluation]]
- [[usability-testing]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
