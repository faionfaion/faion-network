---
slug: cross-timezone-standup-rotation
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Rotation schedule artefact for distributed standups: anchored handoff windows, named owners per timezone, 90-day refresh cadence, citation-traceable rationale.
content_id: "2628979af83fa9cc"
complexity: medium
produces: spec
est_tokens: 5200
tags: [pm, pro, timezone, standup, rotation, distributed]
---
# Cross Timezone Standup Rotation

## Summary

**One-sentence:** Rotation schedule artefact for distributed standups: anchored handoff windows, named owners per timezone, 90-day refresh cadence, citation-traceable rationale.

**One-paragraph:** Cross Timezone Standup Rotation delivers a defensible spec artefact for the pro PM cohort. It binds typed inputs to a strict output contract, enumerates known failure modes, and routes between optimistic and conservative variants via a decision tree. Downstream consumers (human reviewer or agent) accept the artefact without re-deriving the rationale because every claim cites an input by name.

**Ефективно для:**

- Distributed дев-команда з вікнами перекриття <3 годин і потребою в передачі owner-of-day.
- Outsource P4 (EU+LATAM/APAC+NA) — потрібен auditable handoff артефакт для клієнта.
- P6 multi-squad всередині однієї компанії, де standup переходить між клітинками.
- Команда, що готується до 24/7 on-call ротації і репетирує handoff-discipline.

## Applies If (ALL must hold)

- the team spans 2+ timezones with overlap window under 3 hours
- daily ceremony exists or is being established (standup, demo, async-update)
- downstream consumer reads the rotation artefact (ops, eng leads, client PM)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- single timezone or co-located team — rotation overhead unjustified
- ceremony itself is being deprecated — fix that first
- team size below 4 — informal handoff is cheaper
- regulatory rota schedule already mandated by HR or labour law

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| recent context for the triggering activity | log/doc/ticket | last 30 days |
| write-access to the artefact store | repo / wiki / decision log | team policy |
| named accountable owner downstream | handle / email / role | RACI / org chart |
| baseline conventions | CLAUDE.md / AGENTS.md / CONVENTIONS.md | repo root |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/project-manager` | parent role skill — operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | testable rules with statement + rationale + source | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the spec + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: symptom + root-cause + fix | ~900 |
| `content/04-procedure.xml` | essential | step-by-step procedure with decision-gates | ~900 |
| `content/05-examples.xml` | essential | worked example end-to-end | ~700 |
| `content/06-decision-tree.xml` | essential | root question → branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs` | haiku | template fill from typed inputs |
| `synthesize-cross_timezone_standup_rotation` | sonnet | per-instance judgment with bounded inputs |
| `review-for-stakes` | opus | cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/cross-timezone-standup-rotation.md` | spec skeleton with required fields + 5-line header |
| `templates/cross-timezone-standup-rotation.schema.json` | JSON Schema for the output contract |
| `templates/_smoke-test.md` | minimum viable filled-in example |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-cross-timezone-standup-rotation.py` | enforce output-contract against template instance | after subagent returns, before downstream consumer reads |

## Related

- [[project-manager]]
- [[pm-traditional]]
- [[follow-the-sun-handoff-protocol]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, stakes, recurrence) onto a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply or whether to skip the methodology entirely.
