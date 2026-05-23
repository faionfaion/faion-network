---
slug: team-development
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Stage-diagnostic framework (Tuckman: Forming → Storming → Norming → Performing → Adjourning) paired with three artefacts — team charter, skills matrix, retrospective template.
content_id: "72883bf0b8bfe630"
complexity: medium
produces: spec
est_tokens: 4900
tags: [team-development, tuckman, team-performance, agile, leadership]
---
# Team Development

## Summary

**One-sentence:** Stage-diagnostic framework (Tuckman: Forming → Storming → Norming → Performing → Adjourning) paired with three artefacts — team charter, skills matrix, retrospective template.

**One-paragraph:** Stage-diagnostic framework (Tuckman: Forming → Storming → Norming → Performing → Adjourning) paired with three artefacts — team charter, skills matrix, retrospective template. The methodology applies in pm-agile contexts where the preconditions in `Applies If` hold and none of the `Skip If` triggers fire. Decision routing lives in `content/06-decision-tree.xml`; testable rules with rationale live in `content/01-core-rules.xml`; the validator at `scripts/validate-team-development.py` enforces the output contract.

**Ефективно для:**

- Building a new team and choosing facilitation appropriate to its current stage.
- Diagnosing why a Performing team has regressed to Storming after a merge.
- Auditing skill coverage with a written skills matrix.
- Onboarding a new member without resetting the team to Forming.

## Applies If (ALL must hold)

- Team is stable enough that stages are observable (≥3 weeks together).
- A team charter and skills matrix can be authored and maintained.
- Retrospectives are run regularly (≥1 per sprint or month).

## Skip If (ANY kills it)

- Team formed for a single sprint or one-week tiger team.
- Group is a working committee, not a delivery team.
- External staffing churn >50% per quarter — diagnose churn first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Team roster | CSV/YAML | PM |
| Skills inventory | skills × people matrix | team lead |
| Retro history (≥2) | Markdown | team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[scrum-ceremonies]] | retro cadence is the diagnostic instrument |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (incl. skip rule) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom/root-cause/fix triplets | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate | 800 |
| `content/05-examples.xml` | optional | End-to-end worked example | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `diagnose-stage` | sonnet | Judgement: retro signals → Tuckman stage. |
| `draft-charter` | sonnet | Draft working agreements from interviews. |
| `score-skill-coverage` | haiku | Mechanical coverage % per critical skill. |

## Templates

| File | Purpose |
|------|---------|
| `templates/retro.md` | Retro template with stage-aware prompts (Forming → Performing) |
| `templates/skills-matrix.md` | Skills × people matrix template with primary/secondary marks |
| `templates/team-charter.md` | Team charter template: purpose, working agreements, decision rights |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-team-development.py` | Validate the spec artefact against the schema in `02-output-contract.xml` | CI on each artefact change; pre-commit |

## Related

- [[scrum-ceremonies]]
- [[six-core-principles]]
- [[communications-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (preconditions, baseline presence, threshold pass/fail) to a concrete action; each leaf references a rule from `01-core-rules.xml`. Use it when in doubt about whether or how to apply this methodology to the case at hand.

