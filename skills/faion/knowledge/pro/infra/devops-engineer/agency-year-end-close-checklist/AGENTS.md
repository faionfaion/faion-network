---
slug: agency-year-end-close-checklist
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a year-end-close artefact recording every checklist item with anchored source-of-truth, status, and aging on open items.
content_id: "e6291c32c2119fd4"
complexity: medium
produces: checklist
est_tokens: 4500
tags: [agency, checklist, year-end, operations, finops]
---
# Agency Year-End Close Checklist

## Summary

**One-sentence:** Produces a year-end-close artefact recording every checklist item with anchored source-of-truth, status, and aging on open items.

**One-paragraph:** `ops-financial-basics` is too thin to execute a real year-end close for a multi-contractor agency. This methodology pins a checklist where every item is anchored to a named source-of-truth (system + URL), capped within a time-box, and carries an aging counter. Skipped items require a written one-line reason. Output: a year-end-close artefact reviewable by an accountant or auditor.

**Ефективно для:**

- micro-agency (1-10 contractors) проходить рік кінець без проґавлених high-leverage items.
- ops-financial-basics занадто thin для multi-contractor agency річного closes.
- потрібен auditable trail: skipped items вимагають written reason.
- 30-90 хв weekly або 1-2 day annual time-box, з aging counter на open items.

## Applies If (ALL must hold)

- Agency operates a single legal entity for this cycle's close (multi-entity passes are split).
- Read access exists to billing, payroll, time-tracking, and cap-table source-of-truth systems.
- Calendar slot dedicated to the cycle (recurring meeting / focus block).
- Last cycle's artefact is filed where the current cycle can compare year-over-year.

## Skip If (ANY kills it)

- Cycle is mid-year midcheck, not annual close — different methodology.
- Agency is solo founder + 0 contractors — too thin for this checklist.
- Accountant already runs a tighter checklist — defer to theirs.
- Last cycle's artefact is missing AND cannot be reconstructed — fix that before this cycle.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Billing system credentials | read access | finance |
| Payroll system credentials | read access | finance |
| Time-tracking export | CSV | ops |
| Prior cycle's artefact | doc / git | filing system |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer` | parent role skill |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | >=5 testable rules with statement + rationale + source (5+ rules, includes r5-bound-scope) | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | ~900 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns with symptom/root-cause/fix | ~1000 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate per step | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree mapping observable signals to a rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `checklist_dry_run` | haiku | Walk every item against its anchored source |
| `anomaly_flag` | sonnet | Compare current cycle vs prior, flag deltas |
| `decision_synthesis` | opus | Consolidate flags into a corrective-action list |

## Templates

| File | Purpose |
|------|---------|
| `templates/checklist.md` | Year-end close checklist skeleton with anchored items |
| `templates/checklist.json` | JSON schema for the year-end close artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agency-year-end-close-checklist.py` | Validate produced artefact against the 02-output-contract.xml schema | After subagent returns, before downstream consumer reads |

## Related

- [[ops-financial-basics]]
- [[contractor-agreement-template-us-uk-eu]]
- [[action-item-stale-aging]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, owner, downstream consumer) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it before applying the Agency Year-End Close Checklist methodology when in doubt about scope or fit.
