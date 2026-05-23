# User Interviews

## Summary

**One-sentence:** Plan, recruit, conduct, and synthesise one-to-one semi-structured interviews with target users to surface jobs-to-be-done, mental models, and unmet needs.

**One-paragraph:** Plan, recruit, conduct, and synthesise one-to-one semi-structured interviews with target users to surface jobs-to-be-done, mental models, and unmet needs.

**Ефективно для:**

- Solo founders or small teams shipping under time pressure.
- Cross-functional reviewers needing a shared, evidence-grounded artefact.
- Methodology owners maintaining quality gates over time.
- Subagent pipelines that need a deterministic output shape.

## Applies If (ALL must hold)

- Discovery phase for a new feature or product line — the team lacks ground truth.
- Persona document is more than 12 months old or based on opinion.
- A flow performs poorly and the team needs to know why, not just where.
- Pricing or positioning work needs evidence on willingness to pay and alternatives.
- At least five representative users can be recruited within three weeks.

## Skip If (ANY kills it)

- Behaviour-only question — instrument analytics or run a usability test instead.
- Internal tool where the same designer is also the only user.
- No budget for incentives or recruitment, leading to convenience sampling.
- Question can be answered by an existing report or industry study.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Research question + decision driven | markdown | Product manager |
| Recruitment screener | form | Research ops |
| Interview guide | markdown | Researcher |
| Consent and recording forms | pdf | Legal review |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ux-researcher/journey-mapping` | Journey stages structure interview probe topics. |
| `solo/ux/ux-researcher/usability-testing` | Behavioural findings cross-validate stated needs. |

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
| `templates/user-interviews.json` | JSON skeleton conforming to the output contract schema. |
| `templates/user-interviews.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-user-interviews.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[journey-mapping]]
- [[usability-testing]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
