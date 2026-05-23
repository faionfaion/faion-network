---
slug: plg-metrics
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Metrics spec for PLG funnel: activation rate, TTV, free-to-paid conversion, PQL scoring, expansion revenue, NRR and cohort analysis \u2014 definitions, calculation, target ranges, named owner per metric."
content_id: "f2cc956123d370d9"
complexity: medium
produces: spec
est_tokens: 5000
tags: [plg, metrics, activation, pql, retention, marketing]
---
# PLG Metrics

## Summary

**One-sentence:** Metrics spec for PLG funnel: activation rate, TTV, free-to-paid conversion, PQL scoring, expansion revenue, NRR and cohort analysis — definitions, calculation, target ranges, named owner per metric.

**One-paragraph:** Metrics spec for PLG funnel: activation rate, TTV, free-to-paid conversion, PQL scoring, expansion revenue, NRR and cohort analysis — definitions, calculation, target ranges, named owner per metric. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Team runs PLG model (any: freemium / free-trial / reverse-trial).
- Named data / analytics owner can ship + maintain the metrics dashboard.
- Team has analytics infrastructure (Amplitude / Mixpanel / Heap / custom warehouse).

## Skip If (ANY kills it)

- Pre-PMF — focus on qualitative retention research.
- Sales-led product — PLG metrics don't transfer cleanly.
- No analytics infrastructure — instrument before defining the metric tree.

**Ефективно для:**

- PLG-команди що тільки впроваджують metrics-discipline (вперше structured tracking).
- Data analysts що пишуть першу PLG-metrics dashboard.
- Marketing leads що калібрують target ranges проти industry benchmarks.
- Аудит-ready середовища з вимогою evidence-anchored metric definitions.

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
| `pro/marketing/conversion-optimizer` | Parent CRO context — funnel + activation discipline. |
| `pro/marketing/growth-marketer` | Adjacent metric / experimentation context. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology end-to-end | 800 |
| `content/05-examples.xml` | essential | Worked example from input to filled artefact | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-spec` | haiku | Template fill from header + section list. |
| `populate-decisions` | sonnet | Per-section judgment + tradeoff selection. |
| `review-tradeoffs` | opus | Cross-decision synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Markdown skeleton with required sections (overview / decisions / tradeoffs / fitness functions / open questions). |
| `templates/_smoke-test.md` | Minimum viable filled-in instance. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-plg-metrics.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[plg-basics]]
- [[plg-implementation-guide]]
- [[plg-metrics]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
