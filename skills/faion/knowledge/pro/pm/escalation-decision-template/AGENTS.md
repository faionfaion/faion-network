---
slug: escalation-decision-template
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: One-page decision artefact for an upcoming escalation: 2-3 costed options, tradeoffs, recommended path, the single ask, dated decision-window — produced before the meeting.
content_id: "dc56223037c91113"
complexity: medium
produces: decision-record
est_tokens: 5200
tags: [pm, pro, escalation, template, decision-record, stakeholder]
---
# Escalation Decision Template

## Summary

**One-sentence:** One-page decision artefact for an upcoming escalation: 2-3 costed options, tradeoffs, recommended path, the single ask, dated decision-window — produced before the meeting.

**One-paragraph:** Escalation Decision Template delivers a defensible decision-record artefact for the pro PM cohort. It binds typed inputs to a strict output contract, enumerates known failure modes, and routes between optimistic and conservative variants via a decision tree. Downstream consumers (human reviewer or agent) accept the artefact without re-deriving the rationale because every claim cites an input by name.

**Ефективно для:**

- PM, що іде в розмову з execu з 2-3 option + recommended path.
- P4 outsource specialist перед client-side serious-concern call — потрібен 1-pager заздалегідь.
- Founder-as-PM, який не може зайти в room без recorded options + clear ask.
- PMO, що вимагає auditable decision-record на кожну escalation вище gold-line.

## Applies If (ALL must hold)

- an escalation conversation is scheduled within the next 5 business days
- the PM has authority to bring options (not just status) to the stakeholder
- a written record will be saved for the post-meeting follow-up
- stakeholder is senior enough that options + ask must precede free discussion

## Skip If (ANY kills it)

- the conversation is a status update — no decision required, template overhead unjustified
- the decision is already made and the meeting is execution-only — record the decision elsewhere
- options are constrained by a contract clause leaving zero choice — defer to the contract owner

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
| `synthesize-escalation_decision_template` | sonnet | per-instance judgment with bounded inputs |
| `review-for-stakes` | opus | cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/escalation-decision-template.md` | decision-record skeleton with required fields + 5-line header |
| `templates/escalation-decision-template.schema.json` | JSON Schema for the output contract |
| `templates/_smoke-test.md` | minimum viable filled-in example |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-escalation-decision-template.py` | enforce output-contract against template instance | after subagent returns, before downstream consumer reads |

## Related

- [[project-manager]]
- [[pm-traditional]]
- [[escalation-conversation-script]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, stakes, recurrence) onto a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply or whether to skip the methodology entirely.
