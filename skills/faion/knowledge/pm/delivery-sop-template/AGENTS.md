# Service Delivery SOP Template

## Summary

**One-sentence:** Template for a productized-service runbook: 5-15 named steps with explicit inputs, decision branches, quality gates, escalation paths, and time budgets a senior contractor can execute without founder QA.

**One-paragraph:** Template for a productized-service runbook: 5-15 named steps with explicit inputs, decision branches, quality gates, escalation paths, and time budgets a senior contractor can execute without founder QA.

**Ефективно для:**

- Solopreneur-агентств, що виходять з founder-as-bottleneck pattern.
- Сервісних бізнесів, де ту саму послугу повторюють ≥5 разів.
- Контрактних команд, що делегують виконання senior-фрилансеру.
- Productized-service бізнес-моделей з фіксованою ціною.

## Applies If (ALL must hold)

- Service delivered manually by founder ≥5 times.
- Median delivery is consistent enough to predict 80% of the work.
- Founder is the constraint — backlog grows because only founder can execute.
- Target operator is a senior contractor, NOT a junior needing training material.

## Skip If (ANY kills it)

- Service delivered &lt;5 times — no stable pattern yet.
- Service is fundamentally creative / strategic.
- Founder cannot articulate steps without 'it depends'.
- Target operator is junior — write a training manual instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Scope brief | Markdown | engagement intake |
| Stakeholder roster | table | PM |
| Historical reference data | csv / log | PMO data warehouse |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[change-control]] | SOP changes routed through CR for version control. |
| [[lessons-learned]] | SOP drift surfaced via retro. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + `skip-this-methodology` | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden | 850 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 750 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/05-examples.xml` | essential | one worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Apply/skip routing on observable signals | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `step-decomposition` | sonnet | Founder walkthrough transcript → named steps. |
| `decision-branch-extraction` | sonnet | Find 'it depends' moments, formalise as branch. |
| `quality-gate-synthesis` | opus | Cross-step composition into engagement-level acceptance. |
| `escalation-template-fill` | haiku | Fill named-escalation-owner per step. |

## Templates

| File | Purpose |
|------|---------|
| `templates/sop.md` | Runbook: frontmatter + 15-step skeleton with input/action/decision/output/gate. |
| `templates/step-record.json` | JSON for one SOP step. |
| `templates/escalation-map.md` | Edge-case branch → named escalation owner map. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-delivery-sop-template.py` | Validate the output artefact against the schema | Pre-commit on every artefact change |

## Related

- [[change-control]]
- [[communications-management]]
- [[lessons-learned]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observables (manual_delivery_count, target_operator_seniority, founder_can_articulate_steps) to apply / fall-back / skip. Each leaf references a rule from `01-core-rules.xml`.
