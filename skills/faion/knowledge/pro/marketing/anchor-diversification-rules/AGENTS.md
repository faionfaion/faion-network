---
slug: anchor-diversification-rules
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Codifies anchor-text and internal-link distribution rules for one content cluster: exact-match floor, branded mix, generic ceiling, hub-spoke ratios \u2014 a checklist artefact owned by the SEO-manager with a 60-min audit cadence."
content_id: "de0afb4bba551642"
complexity: medium
produces: checklist
est_tokens: 4200
tags: [seo, internal-links, anchor-text, growth-marketing, marketing]
---
# Anchor Diversification Rules

## Summary

**One-sentence:** Codifies anchor-text and internal-link distribution rules for one content cluster: exact-match floor, branded mix, generic ceiling, hub-spoke ratios — a checklist artefact owned by the SEO-manager with a 60-min audit cadence.

**One-paragraph:** Codifies anchor-text and internal-link distribution rules for one content cluster: exact-match floor, branded mix, generic ceiling, hub-spoke ratios — a checklist artefact owned by the SEO-manager with a 60-min audit cadence. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Cluster has ≥ 10 pages with internal links between them.
- Named SEO owner can spend 60 min per cluster on the audit and act on findings.
- Site is indexed by Google and tracked in Search Console — manual action risk is real.

## Skip If (ANY kills it)

- Cluster has < 5 pages — audit overhead does not pay back.
- All internal links are nav/footer (templated) — focus on body-link audit, not template.
- Site is staging / unindexed — fix indexing first.

**Ефективно для:**

- Команди з SEO-кластерами 10-30 сторінок що мають over-optimization ризик.
- SEO-менеджери що бігають 60-хвилинний audit на кластер раз у місяць.
- Сайти що отримали Google manual action за exact-match anchor-text spam.
- Аудит-ready середовища з вимогою evidence-anchored decisions на anchor distribution.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Versioned space for the artefact | Git repo / wiki with history | team |
| Named owner | Person + role | team / RACI |
| Trigger event | Event / threshold / schedule | operating cadence |
| Upstream methodologies in `Assumes Loaded` | Already routine for the role | team training |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/seo-manager` or `pro/marketing/growth-marketer` | Parent role context — SEO / growth discipline. |
| `solo/marketing/content-marketer` | Adjacent content production context. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `apply-checklist` | haiku | Per-item binary check against artefact. |
| `classify-decision` | sonnet | Mitigated / accepted / deferred / N-A judgment. |
| `escalate-stride-conflict` | opus | Cross-category interaction analysis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Checklist with category headings + decision-per-prompt rows. |
| `templates/_smoke-test.md` | Minimum viable filled-in instance. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-anchor-diversification-rules.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[cannibalization-detection-sop]]
- [[anchor-diversification-rules]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
