---
slug: freelancer-handover-bundle-template
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: End-of-engagement handover bundle: repo URL, runbook, credentials index, future-work backlog, contact-of-record, sign-off pack, quiet-line clause — single zip-able artefact.
content_id: "e7b2fa3466344ac1"
complexity: medium
produces: checklist
est_tokens: 5200
tags: [pm, pro, freelance, handover, template, transition]
---
# Freelancer Handover Bundle Template

## Summary

**One-sentence:** End-of-engagement handover bundle: repo URL, runbook, credentials index, future-work backlog, contact-of-record, sign-off pack, quiet-line clause — single zip-able artefact.

**One-paragraph:** Freelancer Handover Bundle Template delivers a defensible checklist artefact for the pro PM cohort. It binds typed inputs to a strict output contract, enumerates known failure modes, and routes between optimistic and conservative variants via a decision tree. Downstream consumers (human reviewer or agent) accept the artefact without re-deriving the rationale because every claim cites an input by name.

**Ефективно для:**

- Solo P3 фрілансер, що закриває typical 6-12-тиж engagement.
- Two-person practice, що передає роботу client-side ops team або наступному vendor-у.
- Founder-PM на distressed-rescue, який має 30-денний quiet-line guarantee як стандарт.
- Outsource agency PMO, що стандартизує handover bundles across project portfolio.

## Applies If (ALL must hold)

- a freelance engagement is closing and deliverables will continue to be operated by client team
- a named receiver on the client side has authority to accept handover
- the engagement produced artefacts that need indexing (code, docs, creds, decisions)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- engagement is one-shot research with no operational handover — closure note is sufficient
- client refused handover — record refusal, exit, do not over-deliver
- deliverables are fully self-explanatory (single static site) and no runbook is needed

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
| `synthesize-freelancer_handover_bundle_template` | sonnet | per-instance judgment with bounded inputs |
| `review-for-stakes` | opus | cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/freelancer-handover-bundle-template.md` | checklist skeleton with required fields + 5-line header |
| `templates/freelancer-handover-bundle-template.schema.json` | JSON Schema for the output contract |
| `templates/_smoke-test.md` | minimum viable filled-in example |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-freelancer-handover-bundle-template.py` | enforce output-contract against template instance | after subagent returns, before downstream consumer reads |

## Related

- [[project-manager]]
- [[pm-traditional]]
- [[engagement-handover-playbook]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, stakes, recurrence) onto a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply or whether to skip the methodology entirely.
