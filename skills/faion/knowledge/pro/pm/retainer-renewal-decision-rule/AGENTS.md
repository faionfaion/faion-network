---
slug: retainer-renewal-decision-rule
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Quarterly retainer renewal decision rule — named inputs (revenue, hours used, margin, NPS, strategic-fit) with numeric thresholds → keep / upsell / kill / renegotiate; cuts emotional re-sign of loss-making clients.
content_id: "d8a788d204c3174a"
complexity: medium
produces: decision-record
est_tokens: 3400
tags: [pm, pro, retainer, decision-rule, micro-agency, renewal]
---
# Retainer Renewal Decision Rule

## Summary

**One-sentence:** A typed decision rule for quarterly retainer renewal per client: named numeric inputs (realised margin %, hours-vs-cap utilisation, client NPS, strategic-fit score) with published thresholds → keep / upsell / renegotiate / kill, cutting inertia-driven re-signs of loss-making clients.

**One-paragraph:** Founders re-sign retainers out of inertia. The conversation gets emotional, the numbers stay vague, and a 12-month loss-making client survives another year. This methodology pins inputs + thresholds: per-client `RetainerDecision` carries realised margin %, utilisation %, NPS (or proxy), and strategic-fit (1-5), with explicit thresholds that route to keep / upsell / renegotiate / kill. Output is versioned + signed; "kept" rows must cite the threshold path, not "client likes us". Quarterly review consumes outcome data to recalibrate thresholds.

**Ефективно для:**

- Quarterly retainer review per client at micro-agency / solo-founder scale.
- Cutting inertia re-signs of loss-making clients with a defensible rule.
- Sponsor / partner conversation: "we declined renewal because thresholds A/B fired".
- Annual review: recalibrate thresholds against actual outcomes.

## Applies If (ALL must hold)

- Founder runs a retainer book with ≥ 3 active retainer clients.
- Per-client margin + utilisation + NPS data available.
- Founder has authority to keep / upsell / kill without partner sign-off.
- Quarterly review cadence is published and observable.

## Skip If (ANY kills it)

- < 3 retainer clients — bespoke conversation cheaper than rule-driven.
- Founder lacks margin data — instrument first (`vendor-margin-defense-checklist`).
- Regulated context with mandated retention rules — adopt that template.
- No named owner.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Per-client P&L | CSV / accounting export | finance |
| Utilisation report | Harvest / Toggl export | time tracker |
| Client NPS / pulse | survey export | client-success |
| Last quarter RetainerDecision records | JSON | this methodology |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[vendor-margin-defense-checklist]] | Margin signal feeds the realised margin % input. |
| [[saas-stack-audit-micro-agency]] | Tool sprawl per client surfaces hidden cost. |
| [[retainer-vs-project-rubric]] | Sibling rubric used for new-engagement decisions. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: named inputs, published thresholds, default action, recorded call, review on failure | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for `RetainerDecision` + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | 6 modes: cargo-cult, ownership ambiguity, drift, leakage, no outcome review, trigger drift | ~900 |
| `content/04-procedure.xml` | medium | 5-step: collect inputs → apply thresholds → record + sign → quarterly review → calibrate | ~600 |
| `content/06-decision-tree.xml` | essential | Tree: margin / utilisation / NPS / strategic-fit thresholds → keep / upsell / renegotiate / kill | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `collect-inputs` | haiku | Mechanical pull from finance + tracker + survey. |
| `apply-thresholds` | haiku | Mechanical comparison. |
| `outcome-review-synthesis` | opus | Cross-quarter calibration with judgment. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | RetainerDecision skeleton |
| `templates/header.yaml` | Frontmatter schema |
| `templates/_smoke-test.json` | Minimum viable filled `RetainerDecision` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-retainer-renewal-decision-rule.py` | Validate `RetainerDecision`: named inputs, numeric thresholds, evidence, owner | Pre-merge |
| `scripts/staleness-check.py` | Flag records whose `last_reviewed` > 90 days | Weekly cron |

## Related

- [[vendor-margin-defense-checklist]]
- [[retainer-vs-project-rubric]]
- [[saas-stack-audit-micro-agency]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps named inputs (realised_margin_pct, utilisation_pct, nps, strategic_fit) to keep / upsell / renegotiate / kill. Every leaf references a rule from `01-core-rules.xml`.
