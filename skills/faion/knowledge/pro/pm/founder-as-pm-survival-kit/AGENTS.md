---
slug: founder-as-pm-survival-kit
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Three keep-three-drop survival artefact for a micro-agency founder: must-keep PM tools (cadence, decisions, financial), drop-without-guilt list, weekly minimum ritual.
content_id: "0a2ef2db81a31af0"
complexity: light
produces: checklist
est_tokens: 5200
tags: [pm, pro, founder, survival, agency, minimalism]
---
# Founder-as-PM Survival Kit

## Summary

**One-sentence:** Three keep-three-drop survival artefact for a micro-agency founder: must-keep PM tools (cadence, decisions, financial), drop-without-guilt list, weekly minimum ritual.

**One-paragraph:** Founder-as-PM Survival Kit delivers a defensible checklist artefact for the pro PM cohort. It binds typed inputs to a strict output contract, enumerates known failure modes, and routes between optimistic and conservative variants via a decision tree. Downstream consumers (human reviewer or agent) accept the artefact without re-deriving the rationale because every claim cites an input by name.

**Ефективно для:**

- Founder-CEO мікро-агенції (≤5 people), що сам тримає PM-роль.
- Solopreneur з 2-3 одночасними engagement-ами без PMO support.
- Bootstrapper, що cuts ceremonies до мінімального tit-for-tat survival kit-у.
- Co-founder, що скидає PM-частину з технічного засновника на business засновника.

## Applies If (ALL must hold)

- the operator is a founder doing PM work without a dedicated PM hire
- the agency or product team is small (≤ 5 people including the founder)
- the founder is bottleneck for PM artefacts and time is the binding constraint
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team has a dedicated PM — the survival kit is for the no-PM case
- founder explicitly enjoys PM craft and wants depth not minimisation — use full pm-traditional
- regulatory or contractual obligations mandate PM artefacts the kit drops — keep them

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
| `synthesize-founder_as_pm_survival_kit` | sonnet | per-instance judgment with bounded inputs |
| `review-for-stakes` | opus | cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/founder-as-pm-survival-kit.md` | checklist skeleton with required fields + 5-line header |
| `templates/founder-as-pm-survival-kit.schema.json` | JSON Schema for the output contract |
| `templates/_smoke-test.md` | minimum viable filled-in example |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-founder-as-pm-survival-kit.py` | enforce output-contract against template instance | after subagent returns, before downstream consumer reads |

## Related

- [[project-manager]]
- [[pm-traditional]]
- [[founder-time-audit-tool]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, stakes, recurrence) onto a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply or whether to skip the methodology entirely.
