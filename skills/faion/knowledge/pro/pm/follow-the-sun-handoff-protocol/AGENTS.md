---
slug: follow-the-sun-handoff-protocol
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Async-cross-timezone delivery cadence: 24-hour rotation with anchored handoff windows, baton artefact (state + blockers + next-N tasks), owner-of-day, baton SLA.
content_id: "11f94e11af10c02c"
complexity: medium
produces: playbook-step
est_tokens: 5200
tags: [pm, pro, follow-the-sun, handoff, async, timezone, outsource]
---
# Follow-The-Sun Handoff Protocol

## Summary

**One-sentence:** Async-cross-timezone delivery cadence: 24-hour rotation with anchored handoff windows, baton artefact (state + blockers + next-N tasks), owner-of-day, baton SLA.

**One-paragraph:** Follow-The-Sun Handoff Protocol delivers a defensible playbook-step artefact for the pro PM cohort. It binds typed inputs to a strict output contract, enumerates known failure modes, and routes between optimistic and conservative variants via a decision tree. Downstream consumers (human reviewer or agent) accept the artefact without re-deriving the rationale because every claim cites an input by name.

**Ефективно для:**

- P4 outsource agency: EU + LATAM або APAC + NA, 24-hour follow-the-sun рішення.
- Distressed-project rescue, що додає second-shift команду до існуючої первинної.
- Open-source maintainer team з global contributors і потребою owner-of-day розкладу.
- Founder-PM з 2 розкиданими timezones, що тестує модель перед масштабуванням.

## Applies If (ALL must hold)

- team spans at least two non-overlapping timezones with under 2 hours overlap
- work is decomposable into tasks each closable within one timezone's working day
- single product / repo / workstream — not parallel independent streams
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- co-located or single-timezone team — protocol overhead unjustified
- tasks routinely span multiple days and cannot be checkpointed at handoff — fix decomposition first
- team has fewer than one engineer per timezone — protocol needs at least one named owner per zone

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
| `content/02-output-contract.xml` | essential | JSON Schema for the playbook-step + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: symptom + root-cause + fix | ~900 |
| `content/04-procedure.xml` | essential | step-by-step procedure with decision-gates | ~900 |
| `content/06-decision-tree.xml` | essential | root question → branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs` | haiku | template fill from typed inputs |
| `synthesize-follow_the_sun_handoff_protocol` | sonnet | per-instance judgment with bounded inputs |
| `review-for-stakes` | opus | cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/follow-the-sun-handoff-protocol.md` | playbook-step skeleton with required fields + 5-line header |
| `templates/follow-the-sun-handoff-protocol.schema.json` | JSON Schema for the output contract |
| `templates/_smoke-test.md` | minimum viable filled-in example |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-follow-the-sun-handoff-protocol.py` | enforce output-contract against template instance | after subagent returns, before downstream consumer reads |

## Related

- [[project-manager]]
- [[pm-traditional]]
- [[cross-timezone-standup-rotation]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, stakes, recurrence) onto a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply or whether to skip the methodology entirely.
