---
slug: pm-tech-lead-grooming-agenda
tier: geek
group: sdd
domain: sdd
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Generates a fixed-shape weekly grooming agenda (priorities x debt x capacity) for the PM + tech-lead duo.
content_id: "0d512e00f2fd7c27"
complexity: medium
produces: checklist
est_tokens: 3400
tags: ["sdd", "grooming", "backlog", "pm", "tech-lead"]
---
# PM + Tech-Lead Grooming Agenda

## Summary

**One-sentence:** Generates a fixed-shape weekly grooming agenda (priorities x debt x capacity) for the PM + tech-lead duo.

**One-paragraph:** PM + Tech-Lead Grooming Agenda produces a checklist that fixes a recurring decision in the sdd domain. It pins the artefact shape, attaches evidence, and blocks unfit inputs via the decision tree. Apply when the preconditions hold; otherwise the decision tree routes you to skip-this-methodology.

**Ефективно для:**

- Щотижневий PM + tech-lead grooming з повторюваною структурою.
- Tradeoff priorities vs tech-debt vs capacity у фіксованому форматі.
- Pre-sprint planning input: вийти зі зустрічі з готовим списком.
- Async grooming: tech-lead заповнює свою половину до зустрічі.
- Onboarding нового PM/tech-lead: одразу знає, як грумити.

## Applies If (ALL must hold)

- Team has a recurring PM + tech-lead grooming cadence (weekly or fortnightly).
- Backlog has both feature items and tech-debt items competing for capacity.
- Sprint capacity is finite and tradeoffs are made each cycle.

## Skip If (ANY kills it)

- Single-developer project — grooming is one person's own list.
- Backlog has no tech-debt entries — separate methodology applies.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Backlog snapshot | JSON / tool export | tracker |
| Tech-debt register | Markdown / JSON | tech lead |
| Capacity forecast | JSON | PM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[sprint-capacity-from-complexity-tags]] | capacity numbers come from complexity tags |
| [[tech-debt-slot-quota-policy]] | debt quota constraints input the agenda |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source + skip rule | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples | 700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | 600 |
| `content/04-procedure.xml` | essential | 5-step procedure with decision gates | 700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-pm-tech-lead-grooming-agenda` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/grooming-agenda.md` | Markdown agenda with 3 fixed blocks + decision column |
| `templates/grooming.schema.json` | JSON Schema for the agenda artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-pm-tech-lead-grooming-agenda.py` | Validate produced artefact against schema | CI on each artefact change; pre-commit |

## Related

- [[sprint-capacity-from-complexity-tags]]
- [[tech-debt-slot-quota-policy]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, infra availability, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
