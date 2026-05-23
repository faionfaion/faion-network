---
slug: multi-project-allocation-tracker
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "30-minute resource allocation review artefact: per-person allocation across active projects, over/under-allocation flags, rebalancing proposals with named decision owners."
content_id: "811d998c1793b625"
complexity: medium
produces: spec
est_tokens: 4400
tags: [pm, pro, allocation, capacity, tracker]
---
# Multi Project Allocation Tracker

## Summary

**One-sentence:** 30-minute resource allocation review artefact: per-person allocation across active projects, over/under-allocation flags, rebalancing proposals with named decision owners.

**One-paragraph:** Multi Project Allocation Tracker defines the testable methodology that turns the recurring work named in this skill into a repeatable, auditable artefact. The methodology is grounded in 5 core rules (see `content/01-core-rules.xml`), a JSON-Schema output contract, 4 catalogued failure modes, a 5-step procedure, and a decision tree whose leaves all reference a rule id.

**Ефективно для:**

- PM running 3-10 concurrent projects with shared people.
- Recurring allocation conflicts ('Olena is on 4 projects this week').
- Weekly or biweekly review cadence is in place.
- Allocation source-of-truth (sheet, Float, Resource Guru) is accessible.

## Applies If (ALL must hold)

- >=3 active projects sharing >=1 person.
- PM has authority to negotiate rebalancing.
- A baseline of per-person weekly capacity (hours/days) exists.
- Prior cycle's allocation snapshot is accessible.

## Skip If (ANY kills it)

- Single project — no cross-project allocation to track.
- Fixed allocations with no expected change (e.g. dedicated teams) — review overhead does not pay back.
- Cannot access allocation source-of-truth.

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
| `content/05-examples.xml` | essential | One end-to-end worked example with trace | 600 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `multi-project-allocation-tracker_template_fill` | haiku | Bounded template fill, no judgement. |
| `multi-project-allocation-tracker_evidence_check` | sonnet | Bounded comparison + judgement on anchored evidence. |
| `multi-project-allocation-tracker_synthesis` | opus | Cross-input synthesis + final write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema (draft 2020-12) for the allocation snapshot artefact. |
| `templates/allocation-row.md` | Per-person allocation row skeleton. |
| `templates/rebalance-proposal.md` | Rebalance proposal skeleton. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-multi-project-allocation-tracker.py` | Validate the artefact against the schema in `content/02-output-contract.xml`. | CI on each artefact change; pre-commit. |

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
