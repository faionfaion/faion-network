# Customer Journey Mapping

## Summary

**One-sentence:** Map the end-to-end customer journey across stages, touchpoints, actions, emotions, and pain points so cross-functional teams can spot friction no single team owns.

**One-paragraph:** Map the end-to-end customer journey across stages, touchpoints, actions, emotions, and pain points so cross-functional teams can spot friction no single team owns.

**Ефективно для:**

- Solo founders or small teams shipping under time pressure.
- Cross-functional reviewers needing a shared, evidence-grounded artefact.
- Methodology owners maintaining quality gates over time.
- Subagent pipelines that need a deterministic output shape.

## Applies If (ALL must hold)

- Designing or auditing a multi-channel customer experience that spans more than one team.
- Onboarding flows show high drop-off and the team needs to attribute friction to a stage.
- Aligning marketing, product, and support around a single picture of the user lifecycle.
- Validating that a new feature improves a real user goal end-to-end, not just a single screen.
- Producing a baseline for measuring before/after improvements over multiple sprints.

## Skip If (ANY kills it)

- Single-screen change with no upstream/downstream touchpoints — use a wireframe review.
- No qualitative or quantitative data on real users — map will be opinion-driven.
- Team will not commit to follow-up work on identified pain points.
- Stakeholders refuse to attend co-creation sessions — solo journey maps drift quickly.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Persona document | markdown | User-research output |
| Behavioural analytics export | csv | Product analytics tool |
| Support ticket sample | csv | Support tool export |
| Stakeholder interview notes | markdown | Cross-functional research |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ux-researcher/user-interviews` | Quotes and pain points populate the emotion lane. |
| `solo/ux/ux-ui-designer/competitive-analysis` | Benchmarks anchor the opportunity column. |

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
| `templates/journey-mapping.json` | JSON skeleton conforming to the output contract schema. |
| `templates/journey-mapping.md` | Markdown skeleton for human-readable artefact rendering. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

- [[user-interviews]]
- [[usability-testing]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/journey-mapping.json`

```json
{
  "artefact_id": "journey-mapping-example",
  "scope": "Scope of the spec \u2014 one paragraph.",
  "decisions": [
    "item-1",
    "item-2",
    "item-3"
  ],
  "stakeholders": [
    "item-1",
    "item-2"
  ],
  "open_questions": [
    "item-1"
  ],
  "version": "1.0.0",
  "last_reviewed": "2026-05-23",
  "lint_status": "pass",
  "owner": "@solo-founder"
}
```
