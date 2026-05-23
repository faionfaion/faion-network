---
slug: multi-touch-attribution-modeling
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Specifies a cross-channel multi-touch attribution model (first-touch + linear + position-based + time-decay) covering organic + email + community + dark-social, with reconciliation against GA4 and warehouse.
content_id: "33fe667229633eb6"
complexity: deep
produces: spec
est_tokens: 6500
tags: ["marketing", "attribution", "analytics", "multi-touch", "pro"]
---
# Multi-Touch Attribution Modeling

## Summary

**One-sentence:** Specifies a cross-channel multi-touch attribution model (first-touch + linear + position-based + time-decay) covering organic + email + community + dark-social, with reconciliation against GA4 and warehouse.

**One-paragraph:** Single-channel attribution (Meta-only or Google-only) is the cause of the 'attribution mess' growth marketers complain about. This methodology specs a multi-touch model across paid + organic + email + community + dark-social, with four model variants (first-touch, linear, position-based, time-decay) reconciled monthly against GA4 + warehouse, variance thresholds (>15% triggers re-investigation), and a defensible budget-reallocation surface. Output: attribution spec + reconciliation runbook + monthly variance report template.

**Ефективно для:**

- Growth marketer з paid + organic + email + community і 'attribution mess'.
- Quarterly budget reallocation: defensible numbers замість platform-self-reported.
- Reconciliation: чому Meta self-reports 200 conversions, GA4 показує 120.
- Audit dark-social: скільки 'direct/none' насправді з community / referrals.

## Applies If (ALL must hold)

- Cross-channel paid spend >= $5k/month OR organic + paid contribute roughly equally to pipeline.
- GA4 + warehouse pipeline exists (BigQuery or equivalent).
- Marketing owner accountable for budget allocation across channels.
- Pipeline horizon >= 30 days (multi-touch only matters with multi-touch funnels).

## Skip If (ANY kills it)

- Single-channel spend (e.g., only Meta) — last-click suffices.
- Pipeline < 7 days from first-touch to conversion — last-click is statistically equivalent.
- No GA4 or warehouse — collect events first; attribution layer needs anchor.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Inputs source-of-truth | system / dashboard / transcript | operator-managed |
| Prior artefact (if any) | Markdown / JSON / YAML | prior cycle |
| Named consumer for output | team contact / agent task | operator-managed |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/AGENTS.md` | parent group context (vocabulary, neighbours) |
| [[learnings-database-schema]] | shared cumulative-knowledge substrate (if available) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | >=5 testable rules with rationale + source | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid + forbidden patterns | ~1000 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns (symptom/root-cause/fix) | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs / actions / outputs / decision-gates | ~1100 |
| `content/05-examples.xml` | essential | One end-to-end worked example | ~900 |
| `content/06-decision-tree.xml` | essential | Decision tree mapping observable signals to a rule from 01-core-rules.xml | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applicability` | sonnet | Decision-tree application; bounded judgement. |
| `draft-multi-touch-attribution-modeling` | opus | Synthesis under output contract; final write-up. |
| `validate-output` | haiku | Mechanical schema check via scripts/validate-<slug>.py. |

## Templates

| File | Purpose |
|------|---------|
| `templates/spec.md` | Markdown spec skeleton |
| `templates/output.json` | JSON spec sidecar with __faion_header__ |
| `templates/_smoke-test.md` | Minimum viable filled spec |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-multi-touch-attribution-modeling.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns, before publish; pre-commit if artefact is git-tracked |

## Related

- [[ad-account-hygiene-checklist]]
- [[ads-attribution-models]]
- [[learnings-database-schema]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (inputs available, thresholds, gating prerequisites) to a concrete verdict, each leaf referencing a rule from `01-core-rules.xml`. Use it whenever multiple variants of the methodology look applicable, or when an upstream condition (e.g. positioning undefined, spend below threshold) makes the methodology a misfit.
