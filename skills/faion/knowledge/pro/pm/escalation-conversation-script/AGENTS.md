---
slug: escalation-conversation-script
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Verbal conversation playbook: scripted opener with acknowledgement-first, 3 de-escalation patterns, verbal→written switch triggers, 3 dated follow-ups, authority guardrail.
content_id: "7eb996cc134cfffa"
complexity: medium
produces: playbook-step
est_tokens: 5200
tags: [pm, pro, escalation, communication, conversation, de-escalation]
---
# Escalation Conversation Script

## Summary

**One-sentence:** Verbal conversation playbook: scripted opener with acknowledgement-first, 3 de-escalation patterns, verbal→written switch triggers, 3 dated follow-ups, authority guardrail.

**One-paragraph:** Escalation Conversation Script delivers a defensible playbook-step artefact for the pro PM cohort. It binds typed inputs to a strict output contract, enumerates known failure modes, and routes between optimistic and conservative variants via a decision tree. Downstream consumers (human reviewer or agent) accept the artefact without re-deriving the rationale because every claim cites an input by name.

**Ефективно для:**

- PM/CSM, що тримає client-facing escalation хоча б 1x на місяць.
- Outsource lead на P4-engagement: vendor miss, missed milestone, client serious-concern call.
- Founder-as-PM, що сам веде складні розмови з клієнтами без CCM/Account Manager.
- Solo консультант: distressed-project rescue, де перший дзвінок визначає, чи врятуєш relationship.

## Applies If (ALL must hold)

- the PM regularly handles cross-organisation conversations under pressure (client unhappy, vendor late, executive escalating)
- the PM has at least one decision lever (re-scope, re-plan, replace vendor, refund, fire customer)
- conversations recur often enough that improvisation is expensive (≥1/month)
- a written follow-up channel exists where commitments can be logged

## Skip If (ANY kills it)

- internal-only stakeholders where the PM has authority and rapport — informal flow is faster
- hostage-negotiation-level conflict requiring legal counsel — escalate to legal/exec, not a script

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
| `synthesize-escalation_conversation_script` | sonnet | per-instance judgment with bounded inputs |
| `review-for-stakes` | opus | cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/escalation-conversation-script.md` | playbook-step skeleton with required fields + 5-line header |
| `templates/escalation-conversation-script.schema.json` | JSON Schema for the output contract |
| `templates/_smoke-test.md` | minimum viable filled-in example |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-escalation-conversation-script.py` | enforce output-contract against template instance | after subagent returns, before downstream consumer reads |

## Related

- [[project-manager]]
- [[pm-traditional]]
- [[escalation-decision-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, stakes, recurrence) onto a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply or whether to skip the methodology entirely.
