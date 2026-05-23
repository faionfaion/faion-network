---
slug: knowledge-sharing-ritual-set
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Weekly tech-talk + biweekly demo + monthly architecture review + quarterly skip-level ritual schedule that converts tribal knowledge into documented artefacts."
content_id: "239325b8f587307e"
complexity: medium
produces: playbook-step
est_tokens: 4200
tags: [pm, pro, knowledge-sharing, rituals, team-ops]
---
# Knowledge Sharing Ritual Set

## Summary

**One-sentence:** Weekly tech-talk + biweekly demo + monthly architecture review + quarterly skip-level ritual schedule that converts tribal knowledge into documented artefacts.

**One-paragraph:** Knowledge Sharing Ritual Set defines the testable methodology that turns the recurring work named in this skill into a repeatable, auditable artefact. The methodology is grounded in 5 core rules (see `content/01-core-rules.xml`), a JSON-Schema output contract, 4 catalogued failure modes, a 5-step procedure, and a decision tree whose leaves all reference a rule id.

**Ефективно для:**

- Team of 4-25 where critical knowledge lives in a few heads.
- PM/lead wants a defensible cadence rather than ad-hoc lunch-and-learn.
- Each ritual must emit a written artefact (notes, demo recording, ADR, action items).
- Skip-level signal needs a regular channel that's not 1:1 escalation.

## Applies If (ALL must hold)

- Team size between 4 and 25 (inclusive).
- At least one person other than the lead can present.
- A persistent storage location for ritual artefacts exists (wiki/repo).
- Lead has authority to block calendars for the rituals.

## Skip If (ANY kills it)

- Solo or duo team — ritual overhead exceeds value.
- Heavy crisis mode where adding calendar load harms throughput.
- Team already runs a working knowledge-sharing cadence with measured retention.

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
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft 2020-12) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `knowledge-sharing-ritual-set_template_fill` | haiku | Bounded template fill, no judgement. |
| `knowledge-sharing-ritual-set_evidence_check` | sonnet | Bounded comparison + judgement on anchored evidence. |
| `knowledge-sharing-ritual-set_synthesis` | opus | Cross-input synthesis + final write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema (draft 2020-12) for the ritual instance artefact. |
| `templates/ritual-notes.md` | Markdown skeleton for tech-talk / demo / arch-review notes. |
| `templates/skip-level-themes.md` | Markdown skeleton for anonymised skip-level theme aggregation. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-knowledge-sharing-ritual-set.py` | Validate the artefact against the schema in `content/02-output-contract.xml`. | CI on each artefact change; pre-commit. |

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
