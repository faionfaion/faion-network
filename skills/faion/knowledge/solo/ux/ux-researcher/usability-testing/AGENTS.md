---
slug: usability-testing
tier: solo
group: ux
domain: ux
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Run moderated or unmoderated usability sessions with five-plus representative users on prioritised tasks to surface friction with severity ratings and recommended fixes.
content_id: "a6fd93373f75147c"
complexity: deep
produces: report
est_tokens: 4400
tags: ["usability", "user-testing", "task-success", "severity-rating", "ux-research"]
---
# Usability Testing

## Summary

**One-sentence:** Run moderated or unmoderated usability sessions with five-plus representative users on prioritised tasks to surface friction with severity ratings and recommended fixes.

**One-paragraph:** Run moderated or unmoderated usability sessions with five-plus representative users on prioritised tasks to surface friction with severity ratings and recommended fixes.

**Ефективно для:**

- Solo founders or small teams shipping under time pressure.
- Cross-functional reviewers needing a shared, evidence-grounded artefact.
- Methodology owners maintaining quality gates over time.
- Subagent pipelines that need a deterministic output shape.

## Applies If (ALL must hold)

- A flow is shipping or has shipped and needs evidence-based prioritisation of fixes.
- A specific user task is more important than overall qualitative impression.
- Stakeholders need observed behavioural data, not surveys or opinions.
- Five-plus representative users can be recruited within two weeks.
- The team will act on findings: triage, fix, retest.

## Skip If (ANY kills it)

- Exploratory discovery — run user interviews instead.
- Prototype too low-fidelity to surface real interaction friction.
- Internal-only tool where the test moderator is also the only user.
- No budget or recruitment channel for representative participants.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Test plan with tasks | markdown | Test-plan template |
| Working prototype or live build | url / figma | Engineering or design |
| Recruitment screener | form | Research ops |
| Consent and recording forms | pdf | Legal review |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ux-researcher/user-interviews` | Provides persona vocabulary for task framing. |
| `solo/ux/ux-ui-designer/heuristic-evaluation` | Sets baseline issues to cross-reference. |

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
| `templates/usability-testing.json` | JSON skeleton conforming to the output contract schema. |
| `templates/usability-testing.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-usability-testing.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[heuristic-evaluation]]
- [[user-interviews]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
