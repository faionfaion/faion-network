---
slug: weekly-arch-review-agenda-template
tier: geek
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: "Fixed-form weekly architecture review agenda: 5 named items (incoming ADRs, fitness functions, drift signals, debt review, next-week pre-briefs) with decision-output gate."
content_id: "498d55955d3ce4b3"
complexity: light
produces: checklist
est_tokens: 2900
tags: [architecture, review, agenda, weekly, adr, geek]
---

# Weekly Architecture Review Agenda Template

## Summary

**One-sentence:** Fixed-form weekly architecture review agenda: 5 named items (incoming ADRs, fitness functions, drift signals, debt review, next-week pre-briefs) with decision-output gate.

**One-paragraph:** Fixed-form weekly architecture review agenda: 5 named items (incoming ADRs, fitness functions, drift signals, debt review, next-week pre-briefs) with decision-output gate. This methodology converts the inputs in Prerequisites into the artefact described in Output Contract, gated by the rules in 01-core-rules.xml and the decision tree in 06-decision-tree.xml.

**Ефективно для:** the kinds of tasks listed in 'Applies If' — primary use cases are teams shipping the artefact (`checklist`) at a light complexity level, where the failure modes in 03-failure-modes.xml are realistic risks worth the methodology's overhead.

## Applies If (ALL must hold)

- Team has a named architect or architecture council.
- ADRs are produced regularly (≥1/month).
- There is appetite to make architecture review a recurring ritual.

## Skip If (ANY kills it)

- Architecture decisions are made ad hoc by the founding team — review is overhead.
- Team is <4 engineers — review degenerates into status standup.
- ADR cadence is <1/quarter — there is nothing to review weekly.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Open ADR list | Markdown / Linear | ADR repo |
| Fitness-function dashboard | Grafana / static report | architecture-fitness-functions |
| Tech-debt board | Linear / Jira / Markdown | tech-debt-basics |
| 60-min weekly slot | calendar | all senior engineers |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/software-architect/retro-adr-workflow` | Source of ADR drafts reviewed. |
| `pro/dev/software-architect/architecture-fitness-functions` | Source of fitness signals reviewed. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 3-5 antipatterns with symptom/root-cause/fix | ~800 |
| `content/06-decision-tree.xml` | essential | Decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `agenda_prebrief_compose` | sonnet | Compose the 5-item brief 24h pre-meeting. |
| `decision_log_draft` | sonnet | Write the decision log after the meeting. |
| `adr_spawn_check` | opus | Decide which items become ADRs. |

## Templates

| File | Purpose |
|------|---------|
| `templates/agenda.md` | Five-item agenda template with empty-state defaults. |
| `templates/decision-log-entry.md` | Shape of one decision-log entry. |
| `templates/prebrief.md` | 1-page brief sent 24h pre-meeting. |
| `templates/_smoke-test.md` | Minimum-viable filled-in example (smoke test). |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-weekly-arch-review-agenda-template.py` | Validate methodology output against `02-output-contract.xml` schema. | Pre-commit and CI before merge. |

## Related

- parent skill: `geek/dev/`
- `[[retro-adr-workflow]]`
- `[[architecture-fitness-functions]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether weekly-arch-review-agenda-template applies: root question — "Does the team produce ≥1 ADR per month AND have a named architect?". Branches lead to a specific core rule (e.g., `rule:r1`) when the methodology fits, or to a `skip-this-methodology` conclusion when it does not.
