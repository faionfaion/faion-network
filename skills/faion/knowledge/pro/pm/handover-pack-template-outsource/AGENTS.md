---
slug: handover-pack-template-outsource
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Mid-engagement handover pack spec for an outsource specialist rotating to a peer or in-house owner; covers context, decisions, contacts, open issues, runbooks, acceptance gate."
content_id: "c5b243b088fe1949"
complexity: medium
produces: spec
est_tokens: 4600
tags: [pm, pro, outsource, handover, knowledge-transfer]
---
# Handover Pack Template Outsource

## Summary

**One-sentence:** Mid-engagement handover pack spec for an outsource specialist rotating to a peer or in-house owner; covers context, decisions, contacts, open issues, runbooks, acceptance gate.

**One-paragraph:** Handover Pack Template Outsource defines the testable methodology that turns the recurring work named in this skill into a repeatable, auditable artefact. The methodology is grounded in 6 core rules (see `content/01-core-rules.xml`), a JSON-Schema output contract, 4 catalogued failure modes, a 5-step procedure, and a decision tree whose leaves all reference a rule id.

**Ефективно для:**

- Outsource specialist rotating off mid-engagement (not at final close).
- Receiving engineer is a peer or in-house team without prior context.
- Engagement runs >3 months and has accumulated decisions worth carrying forward.
- A named acceptance reviewer can sign off on the pack before rotation closes.

## Applies If (ALL must hold)

- Engagement is active and rotation date is within 14 days.
- Specialist has authority to publish documentation in the engagement's primary doc location.
- Receiving owner is identified (no orphan handovers).
- Source-of-truth for decisions (PR history, ADRs, transcripts) is accessible.

## Skip If (ANY kills it)

- Final project close-out — use PMI project-closure templates instead.
- Specialist has been on the engagement <2 weeks (no accumulated tacit knowledge worth handing).
- Receiving owner is not identified — defer until owner is named.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Source-of-truth data | tool export / sheet / API | upstream system named in this methodology |
| Prior cycle's artefact (if any) | json / md | repo / wiki where artefacts persist |
| Named consumer | person / agent | engagement charter |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies). |
| `pro/sdd/AGENTS.md` if present | SDD discipline for the artefact lifecycle (status flow, owners, review). |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft 2020-12) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output | 800 |
| `content/05-examples.xml` | essential | One end-to-end worked example with trace | 600 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `handover-pack-template-outsource_template_fill` | haiku | Bounded template fill, no judgement. |
| `handover-pack-template-outsource_evidence_check` | sonnet | Bounded comparison + judgement on anchored evidence. |
| `handover-pack-template-outsource_synthesis` | opus | Cross-input synthesis + final write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema (draft 2020-12) for the handover pack artefact. |
| `templates/handover-pack.md` | Markdown skeleton for the pack: cover + decisions + open issues + runbooks + contacts + acceptance gate. |
| `templates/acceptance-request.md` | Email/message template requesting the receiver's written acknowledgement. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-handover-pack-template-outsource.py` | Validate the artefact against the schema in `content/02-output-contract.xml`. | CI on each artefact change; pre-commit. |

## Related

- parent skill: `pro/pm/` (see neighbouring methodologies).
- [[launch-raci-template]]
- [[reporting-basics]]
- external: industry references cited inline in `content/01-core-rules.xml`.

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input
preconditions, source-of-truth access, named-consumer presence) onto a concrete
verdict — apply the methodology, downgrade to draft, or skip — with each leaf
referencing a rule id from `content/01-core-rules.xml`.
