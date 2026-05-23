# Timezone Overlap Handoff Protocol

## Summary

**One-sentence:** Timezone Overlap Handoff Protocol: produces a versioned, owner-signed artefact that closes the gap 'p4-outsource-specialist/Cross-timezone async daily standup'.

**One-paragraph:** Addresses the gap surfaced by 'p4-outsource-specialist/Cross-timezone async daily standup': How to structure 2-3 hour overlap window between offshore + onshore so blockers move that day instead of slipping 24h. Generic stakeholder-comms is too abstract. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a timezone overlap handoff protocol artefact (decision record, checklist, score sheet, or report).

**Ефективно для:**

- Cross-timezone async daily standup потребує structured handoff-протоколу.
- Команда у трьох таймзонах втрачає контекст між handoff-точками.
- Engagement-manager хоче signed протокол замість "ми синхронізуємось в чаті".

## Applies If (ALL must hold)

- task is an instance of 'p4-outsource-specialist/Cross-timezone async daily standup' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working timezone overlap handoff protocol artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'p4-outsource-specialist/Cross-timezone async daily standup' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/pm` | parent domain group — provides operating context for Timezone Overlap Handoff Protocol |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules grounded in the cited gap | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples | 700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/05-examples.xml` | medium | One worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/timezone-overlap-handoff-protocol.md` | Filled artefact skeleton conforming to 02-output-contract.xml |
| `templates/timezone-overlap-handoff-protocol.schema.json` | JSON Schema for the artefact (mirrors content/02-output-contract.xml) |
| `templates/_smoke-test.md` | Minimum-viable filled-in version exercised by scripts/validate-timezone-overlap-handoff-protocol.py --self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-timezone-overlap-handoff-protocol.py` | Validate artefact against 02-output-contract.xml schema. Exit 0/1/2. | After subagent returns; pre-commit on artefact change. |

## Related

- parent skill: `pro/pm/`
- upstream playbook: `p4-outsource-specialist/Cross-timezone async daily standup`
- pro/pm/p4-outsource-specialist

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (preconditions hold, inputs typed, rules pass) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it before producing the artefact to confirm the methodology applies and the rules pass.
