# Dependency Slack Thresholds

## Summary

**One-sentence:** Policy artefact defining slip-to-escalate thresholds per dependency class: numeric tolerances (days/percent), owner, escalation route, review cadence.

**One-paragraph:** Dependency Slack Thresholds delivers a defensible decision-record artefact for the pro PM cohort. It binds typed inputs to a strict output contract, enumerates known failure modes, and routes between optimistic and conservative variants via a decision tree. Downstream consumers (human reviewer or agent) accept the artefact without re-deriving the rationale because every claim cites an input by name.

**Ефективно для:**

- P4 outsource з 2+ під-вендорами та handoff-милямі critical-path задачами.
- P6 multi-squad enterprise — між-командні залежності з історичними slip-event'ами.
- PMO, де RACI вже існує, але slip→escalate тригер не визначений кількісно.
- Програми з квартальною ритмікою, де handoff-discipline тестується щоквартально.

## Applies If (ALL must hold)

- two or more teams or vendors have hard interdependencies on critical-path tasks
- slip-on-promise events recur ≥1x per cycle and were previously handled ad-hoc
- named owner exists for the dependency contract on each side
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- single-team project with no cross-team handoffs — threshold artefact orphaned
- thresholds already set by a binding SLA / contract clause — defer to the contract
- team operates a continuous-pull model (no promised dates) — escalation needs a different trigger

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
| `content/02-output-contract.xml` | essential | JSON Schema for the decision-record + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: symptom + root-cause + fix | ~900 |
| `content/04-procedure.xml` | essential | step-by-step procedure with decision-gates | ~900 |
| `content/06-decision-tree.xml` | essential | root question → branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs` | haiku | template fill from typed inputs |
| `synthesize-dependency_slack_thresholds` | sonnet | per-instance judgment with bounded inputs |
| `review-for-stakes` | opus | cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/dependency-slack-thresholds.md` | decision-record skeleton with required fields + 5-line header |
| `templates/dependency-slack-thresholds.schema.json` | JSON Schema for the output contract |
| `templates/_smoke-test.md` | minimum viable filled-in example |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-dependency-slack-thresholds.py` | enforce output-contract against template instance | after subagent returns, before downstream consumer reads |

## Related

- [[project-manager]]
- [[pm-traditional]]
- [[escalation-decision-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, stakes, recurrence) onto a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply or whether to skip the methodology entirely.
