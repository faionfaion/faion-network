---
slug: foreign-client-kickoff-checklist
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: 30-item kickoff checklist for 2-week foreign-client onboarding: stakeholder map, comms cadence, decision-makers, holiday calendar, payment terms, IP regime, escalation route.
content_id: "15a994b544c413fd"
complexity: medium
produces: checklist
est_tokens: 5200
tags: [pm, pro, kickoff, foreign-client, checklist, onboarding]
---
# Foreign Client Kickoff Checklist

## Summary

**One-sentence:** 30-item kickoff checklist for 2-week foreign-client onboarding: stakeholder map, comms cadence, decision-makers, holiday calendar, payment terms, IP regime, escalation route.

**One-paragraph:** Foreign Client Kickoff Checklist delivers a defensible checklist artefact for the pro PM cohort. It binds typed inputs to a strict output contract, enumerates known failure modes, and routes between optimistic and conservative variants via a decision tree. Downstream consumers (human reviewer or agent) accept the artefact without re-deriving the rationale because every claim cites an input by name.

**Ефективно для:**

- P4 outsource agency, що запускає 6-12-тиж проект з новим foreign-client.
- Solo фрілансер, що приймає US/EU клієнта і не може дозволити missing-info ризик.
- Founder-PM на першому international engagement: timezone, holidays, IP regime, payment cycle.
- PMO template owner, що стандартизує kickoff across 5-15 active engagements.

## Applies If (ALL must hold)

- a new foreign-client engagement is starting and a kickoff window of 1-2 weeks exists
- the engagement is large enough that kickoff overhead is justified (≥ 4 weeks of work)
- the PM has authority to gather + record kickoff inputs
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- engagement is under 2 weeks — full kickoff checklist overhead unjustified
- this is the third+ engagement with the same client — reuse prior checklist, skip from-scratch run
- kickoff was already done informally and recorded elsewhere — do not duplicate

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
| `content/02-output-contract.xml` | essential | JSON Schema for the checklist + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: symptom + root-cause + fix | ~900 |
| `content/04-procedure.xml` | essential | step-by-step procedure with decision-gates | ~900 |
| `content/06-decision-tree.xml` | essential | root question → branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs` | haiku | template fill from typed inputs |
| `synthesize-foreign_client_kickoff_checklist` | sonnet | per-instance judgment with bounded inputs |
| `review-for-stakes` | opus | cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/foreign-client-kickoff-checklist.md` | checklist skeleton with required fields + 5-line header |
| `templates/foreign-client-kickoff-checklist.schema.json` | JSON Schema for the output contract |
| `templates/_smoke-test.md` | minimum viable filled-in example |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-foreign-client-kickoff-checklist.py` | enforce output-contract against template instance | after subagent returns, before downstream consumer reads |

## Related

- [[project-manager]]
- [[pm-traditional]]
- [[foreign-client-etiquette-playbook]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, stakes, recurrence) onto a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply or whether to skip the methodology entirely.
