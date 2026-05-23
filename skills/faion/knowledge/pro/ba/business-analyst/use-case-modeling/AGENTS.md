---
slug: use-case-modeling
tier: pro
group: business-analyst
domain: ba
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Defines actor-goal-scenario use cases — main success path, alternate flows, exception flows, preconditions, postconditions — that downstream teams turn into stories, tests, and screens.
content_id: "a3ebedf043b095d1"
complexity: medium
produces: spec
est_tokens: 2800
tags: [use-case, actor, scenario, requirements, modeling]
---
# Use Case Modeling

## Summary

**One-sentence:** A structured actor-goal-scenario spec with main success path, alternates, exceptions, and pre/postconditions consumed by story-mapping, testing, and UI design.

**One-paragraph:** Use cases beat free-form requirements when behaviour matters more than data. This methodology produces a use-case spec with: named actor, goal, preconditions, main success scenario (numbered steps), alternate flows, exception flows, postconditions, frequency. The output feeds user-story mapping, test design, and UI flow design. Every step references an actor + system response.

**Ефективно для:**

- Behaviour-heavy systems (workflows, approvals, transactions).
- Pre-build phase when test design is starting.
- Cross-team alignment when one team writes stories and another writes tests.
- Audit-relevant flows where exception paths drive compliance.

## Applies If (ALL must hold)

- the system has identifiable actors with goals
- behaviour matters more than entity structure for the slice in question
- downstream consumer is story-mapping / test design / UI design
- named approver exists

## Skip If (ANY kills it)

- the requirement is pure data-shape — use a data model instead
- the requirement is a single screen with no flow — use a wireframe
- team prefers BDD-only and use cases would duplicate effort

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| business-need spec | MD / wiki | strategy-analysis-business-need |
| actor list | CSV / wiki | stakeholder-analysis |
| named approver | org chart | PM / BA |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[stakeholder-analysis]] | Source of named actors with goals. |
| [[strategy-analysis-business-need]] | Anchors the use case to a measurable outcome. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: actor-goal-scenario, numbered steps, named preconditions, ≥1 alternate flow, ≥1 exception flow | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for use-case spec: actor, goal, preconditions, main + alternate + exception flows, postconditions, frequency | 800 |
| `content/03-failure-modes.xml` | essential | 5 failure modes: actor = system, narrative prose instead of steps, missing exceptions, frequency unset, unowned approval | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: identify actor + goal → main path → alternates → exceptions → review with actor | 700 |
| `content/05-examples.xml` | essential | Worked example: customer login + 2FA exception flow | 600 |
| `content/06-decision-tree.xml` | essential | Tree on behaviour vs data + actor clarity + downstream consumer | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `actor_extraction` | sonnet | Extract actor list from prerequisites. |
| `main_path_draft` | sonnet | Numbered steps for happy path. |
| `exception_enumeration` | sonnet | Identify likely exceptions per step. |
| `review_with_actor` | haiku | Mechanical readback transcription. |

## Templates

| File | Purpose |
|------|---------|
| `templates/use-case.md` | Markdown skeleton with all required sections. |
| `templates/exception-flows.csv` | Header for exception-flow rows. |
| `templates/_smoke-test.md` | Minimum viable use case. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-use-case-modeling.py` | Validates use-case spec against the JSON Schema. | Before approver sign-off; pre-commit. |

## Related

- [[user-story-mapping]]
- [[stakeholder-analysis]]
- [[strategy-analysis-business-need]]
- [[definition-of-done-library]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input completeness, ownership clarity, regulatory context, scope size) to a rule from `01-core-rules.xml`. Use it when in doubt about whether to run, skip, or split this methodology.
