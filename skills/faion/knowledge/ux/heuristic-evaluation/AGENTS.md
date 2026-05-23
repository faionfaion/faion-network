# Heuristic Evaluation

## Summary

**One-sentence:** Have three to five evaluators independently score a UI against the ten Nielsen heuristics with severity ratings, then synthesise a deduplicated prioritised issue list.

**One-paragraph:** Have three to five evaluators independently score a UI against the ten Nielsen heuristics with severity ratings, then synthesise a deduplicated prioritised issue list.

**Ефективно для:**

- Solo founders or small teams shipping under time pressure.
- Cross-functional reviewers needing a shared, evidence-grounded artefact.
- Methodology owners maintaining quality gates over time.
- Subagent pipelines that need a deterministic output shape.

## Applies If (ALL must hold)

- An interface is shippable and benefits from a quick expert review.
- Three to five qualified evaluators can spend two-plus hours on it.
- Severity-ranked actionable issue list is the desired output.
- Team will triage and address findings within the next sprint.
- User-research data is unavailable or supplements heuristic findings later.

## Skip If (ANY kills it)

- User-research data already isolates the friction points — go fix them.
- Single evaluator available — inter-rater coverage will be poor.
- Pre-IA wireframes — heuristics need a real interaction model.
- Findings will not be triaged — review becomes documentation theatre.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Stable UI to evaluate | url / figma | Product owner |
| Nielsen 10-heuristic cheat sheet | markdown | Researcher |
| Severity-rating rubric | markdown | Researcher |
| Synthesis spreadsheet | xlsx | Researcher |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ux-ui-designer/consistency-standards` | Heuristic 4 references the design system. |
| `solo/ux/ux-researcher/usability-testing` | Behavioural data refines or refutes heuristic findings. |

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
| `templates/heuristic-evaluation.json` | JSON skeleton conforming to the output contract schema. |
| `templates/heuristic-evaluation.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-heuristic-evaluation.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[usability-testing]]
- [[design-critique]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
