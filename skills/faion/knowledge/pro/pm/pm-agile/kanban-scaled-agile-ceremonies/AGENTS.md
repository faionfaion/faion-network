---
slug: kanban-scaled-agile-ceremonies
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Alternative ceremony cadence for continuous-flow Kanban teams + scaled SAFe programs: replenishment, flow review, ART sync, PI planning windows, with WIP and lead-time metrics."
content_id: "62254c36095ab9ae"
complexity: medium
produces: playbook-step
est_tokens: 4600
tags: [kanban, safe, ceremonies, continuous-flow, scaled-agile]
---
# Kanban and SAFe Ceremonies

## Summary

**One-sentence:** Alternative ceremony cadence for continuous-flow Kanban teams + scaled SAFe programs: replenishment, flow review, ART sync, PI planning windows, with WIP and lead-time metrics.

**One-paragraph:** Kanban and SAFe Ceremonies defines the testable methodology that turns the recurring work named in this skill into a repeatable, auditable artefact. The methodology is grounded in 5 core rules (see `content/01-core-rules.xml`), a JSON-Schema output contract, 4 catalogued failure modes, a 5-step procedure, and a decision tree whose leaves all reference a rule id.

**Ефективно для:**

- Continuous-flow teams that find Scrum sprints harmful (interrupt-driven work).
- SAFe Agile Release Trains (ART) with 5-12 teams operating on a common cadence.
- Programs needing a written cadence to bridge multiple Scrum / Kanban teams.
- Operators tracking lead-time + throughput, not story-points + velocity.

## Applies If (ALL must hold)

- Team or program has decided NOT to use Scrum sprints.
- WIP-limit discipline is in place or about to be introduced.
- Flow metrics (lead time, cycle time, throughput) can be measured.
- Cadence owners (RTE for SAFe, Flow Manager for Kanban) are named.

## Skip If (ANY kills it)

- Team is happily on Scrum with predictable sprint velocity.
- Single team <5 people — SAFe ceremonies are overkill; lightweight Kanban is enough.
- Org cannot commit to a fixed cadence (PI window) — SAFe collapses without it.

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
| `kanban-scaled-agile-ceremonies_template_fill` | haiku | Bounded template fill, no judgement. |
| `kanban-scaled-agile-ceremonies_evidence_check` | sonnet | Bounded comparison + judgement on anchored evidence. |
| `kanban-scaled-agile-ceremonies_synthesis` | opus | Cross-input synthesis + final write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema (draft 2020-12) for the ceremony cadence artefact. |
| `templates/kanban-metrics.md` | Markdown skeleton for lead-time / cycle-time / throughput / WIP report. |
| `templates/cycle-stats.py` | Reference script computing cycle stats from issue events. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-kanban-scaled-agile-ceremonies.py` | Validate the artefact against the schema in `content/02-output-contract.xml`. | CI on each artefact change; pre-commit. |

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
