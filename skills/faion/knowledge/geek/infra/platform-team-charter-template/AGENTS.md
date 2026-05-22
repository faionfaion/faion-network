---
slug: platform-team-charter-template
tier: geek
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: "Platform team charter: mission, customers, scope/non-scope, paved-road services, SLAs, support model, success metrics, anti-charter (what we do NOT do)."
content_id: "8a0a6c15c41ec2fe"
complexity: medium
produces: spec
est_tokens: 4600
tags: [platform-team, charter, internal-developer-platform, sla, geek, infra]
---

# Platform Team Charter Template

## Summary

**One-sentence:** Platform team charter: mission, customers, scope/non-scope, paved-road services, SLAs, support model, success metrics, anti-charter (what we do NOT do).

**One-paragraph:** Platform team charter: mission, customers, scope/non-scope, paved-road services, SLAs, support model, success metrics, anti-charter (what we do NOT do). This methodology converts the inputs in Prerequisites into the artefact described in Output Contract, gated by the rules in 01-core-rules.xml and the decision tree in 06-decision-tree.xml.

**Ефективно для:** the kinds of tasks listed in 'Applies If' — primary use cases are teams shipping the artefact (`spec`) at a medium complexity level, where the failure modes in 03-failure-modes.xml are realistic risks worth the methodology's overhead.

## Applies If (ALL must hold)

- Org has ≥3 product teams sharing infra / tooling concerns.
- Engineering wants paved-road services with explicit ownership boundaries.
- Platform team is being formed OR being repositioned.

## Skip If (ANY kills it)

- Org is <20 engineers — full charter overhead; informal platform suffices.
- Sole-shop where 1 engineer owns everything.
- Existing charter is in steady-state operation — refresh, do not rewrite.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Stakeholder map | Markdown | platform lead |
| Existing services inventory | Spreadsheet | infra |
| SLA + support tier matrix | Markdown | this methodology |
| Anti-charter draft | Markdown | platform lead |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/software-architect/team-topologies-skills` | Team-Topologies framing of platform team. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 3-5 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | medium | 4-6 step procedure with input/action/output per step | ~900 |
| `content/05-examples.xml` | medium | One end-to-end worked example | ~800 |
| `content/06-decision-tree.xml` | essential | Decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `charter_draft` | sonnet | Bounded transform from inputs to charter sections. |
| `anti_charter_synthesis` | opus | Cross-stakeholder synthesis of 'we do NOT do'. |
| `metrics_pick` | sonnet | Pick 3-5 platform-health metrics. |

## Templates

| File | Purpose |
|------|---------|
| `templates/charter.md` | Charter sections: mission, customers, scope, anti-scope, services, SLA, metrics. |
| `templates/anti-charter.md` | What the platform team does NOT do. |
| `templates/service-catalogue.md` | Paved-road service list with SLAs. |
| `templates/_smoke-test.md` | Minimum-viable filled-in example (smoke test). |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-platform-team-charter-template.py` | Validate methodology output against `02-output-contract.xml` schema. | Pre-commit and CI before merge. |

## Related

- parent skill: `geek/infra/`
- `[[team-topologies-skills]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether platform-team-charter-template applies: root question — "Does the org have ≥3 product teams AND a dedicated platform team is forming or repositioning?". Branches lead to a specific core rule (e.g., `rule:r1`) when the methodology fits, or to a `skip-this-methodology` conclusion when it does not.
