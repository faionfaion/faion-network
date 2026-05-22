---
slug: oncall-handoff-protocol
tier: geek
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: "Structured on-call handoff: open incidents, pending follow-ups, known-quiet-period plans, paged-but-not-resolved items, escalation contacts, fatigue note."
content_id: "702a59640c339abd"
complexity: light
produces: checklist
est_tokens: 2900
tags: [on-call, handoff, incident, rotation, geek, infra]
---

# On-Call Handoff Protocol

## Summary

**One-sentence:** Structured on-call handoff: open incidents, pending follow-ups, known-quiet-period plans, paged-but-not-resolved items, escalation contacts, fatigue note.

**One-paragraph:** Structured on-call handoff: open incidents, pending follow-ups, known-quiet-period plans, paged-but-not-resolved items, escalation contacts, fatigue note. This methodology converts the inputs in Prerequisites into the artefact described in Output Contract, gated by the rules in 01-core-rules.xml and the decision tree in 06-decision-tree.xml.

**Ефективно для:** the kinds of tasks listed in 'Applies If' — primary use cases are teams shipping the artefact (`checklist`) at a light complexity level, where the failure modes in 03-failure-modes.xml are realistic risks worth the methodology's overhead.

## Applies If (ALL must hold)

- On-call rotation has ≥2 engineers handing off between shifts.
- Recent shift handled ≥1 paging incident OR has open follow-up items.

## Skip If (ANY kills it)

- Single-engineer on-call with no handoff partner (sit-back rotation).
- Fully automated triage with no human shift — no handoff to do.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Incident tracker | Jira / PagerDuty / Linear | ops |
| Shift overlap slot | calendar | 15 min minimum |
| Handoff template | Markdown | this methodology |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/infra/on-call-rotation-setup` | Defines the rotation this protocol handed-off within. |
| `pro/infra/devops-engineer/incident-response-playbook` | Active incidents may still be in motion. |

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
| `handoff_compose` | haiku | Bounded template fill. |
| `escalation_check` | sonnet | Decide whether anything needs same-day exec briefing. |

## Templates

| File | Purpose |
|------|---------|
| `templates/handoff.md` | Structured handoff checklist. |
| `templates/fatigue-note.md` | Outgoing engineer fatigue + rest signal. |
| `templates/_smoke-test.md` | Minimum-viable filled-in example (smoke test). |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-oncall-handoff-protocol.py` | Validate methodology output against `02-output-contract.xml` schema. | Pre-commit and CI before merge. |

## Related

- parent skill: `geek/infra/`
- `[[on-call-rotation-setup]]`
- `[[incident-response-playbook]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether oncall-handoff-protocol applies: root question — "Did the shift have ≥1 paging incident OR open follow-ups?". Branches lead to a specific core rule (e.g., `rule:r1`) when the methodology fits, or to a `skip-this-methodology` conclusion when it does not.
