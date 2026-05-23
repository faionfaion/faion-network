---
slug: engagement-handover-playbook
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Outsource handover artefact: knowledge-transfer matrix, sign-off pack, 30-day quiet-line guarantee, repo + creds + runbook + future-work index for client or next vendor.
content_id: "7754d4d83d3fc47d"
complexity: deep
produces: playbook-step
est_tokens: 5200
tags: [pm, pro, handover, outsource, transition, p4]
---
# Engagement Handover Playbook

## Summary

**One-sentence:** Outsource handover artefact: knowledge-transfer matrix, sign-off pack, 30-day quiet-line guarantee, repo + creds + runbook + future-work index for client or next vendor.

**One-paragraph:** Engagement Handover Playbook delivers a defensible playbook-step artefact for the pro PM cohort. It binds typed inputs to a strict output contract, enumerates known failure modes, and routes between optimistic and conservative variants via a decision tree. Downstream consumers (human reviewer or agent) accept the artefact without re-deriving the rationale because every claim cites an input by name.

**Ефективно для:**

- P4 outsource фрілансер/агенція, що завершує 6-12-тижневий engagement.
- Vendor transition (зміна постачальника на client side) з 30-денним quiet-line guarantee.
- Engagement з PCI/HIPAA/regulated scope — knowledge transfer має бути auditable.
- Solo-консультант, що передає 'one-throat-to-choke' роботу in-house команді.

## Applies If (ALL must hold)

- vendor or freelancer engagement is closing within the next 4 weeks
- deliverables will continue to be operated by client team or another vendor
- named receiver exists on the other side with authority to accept sign-off
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- engagement is being terminated for cause without handover scope — defer to legal/MSA
- deliverables are a one-shot artefact with no ongoing operation — closure ≠ handover
- client explicitly refused handover and accepted as-is — record refusal, exit

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
| `synthesize-engagement_handover_playbook` | sonnet | per-instance judgment with bounded inputs |
| `review-for-stakes` | opus | cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/engagement-handover-playbook.md` | playbook-step skeleton with required fields + 5-line header |
| `templates/engagement-handover-playbook.schema.json` | JSON Schema for the output contract |
| `templates/_smoke-test.md` | minimum viable filled-in example |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-engagement-handover-playbook.py` | enforce output-contract against template instance | after subagent returns, before downstream consumer reads |

## Related

- [[project-manager]]
- [[pm-traditional]]
- [[freelancer-handover-bundle-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, stakes, recurrence) onto a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply or whether to skip the methodology entirely.
