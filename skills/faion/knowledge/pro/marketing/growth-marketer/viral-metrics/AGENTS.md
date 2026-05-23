---
slug: viral-metrics
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Locked-formula viral metric set: K = i * c, viral cycle time, retention-adjusted K, branch coefficient — each with canonical SQL and weekly measurement cadence.
content_id: "9f1741fc37ef3093"
complexity: medium
produces: config
est_tokens: 4200
tags: [viral, k-factor, referrals, growth, viral-cycle-time]
---
# Viral Metrics and K-factor

## Summary

**One-sentence:** Locked-formula viral metric set: K = i * c, viral cycle time, retention-adjusted K, branch coefficient — each with canonical SQL and weekly measurement cadence.

**One-paragraph:** Locked-formula viral metric set: K = i * c, viral cycle time, retention-adjusted K, branch coefficient — each with canonical SQL and weekly measurement cadence. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

**Ефективно для:**

- Команди що running виральний loop і потребують locked metric definitions.
- Перед optimizing K-factor — спершу confirm formula consistency.
- Якщо два reports показують різні K — це consolidation cue.
- Як audit existing viral instrumentation pre-quarter.

## Applies If (ALL must hold)

- Виральний loop активний > 4 weeks — є dataset для measurement.
- Event log fixates invite-sent + invite-converted events за user_id.
- Team здатний на SQL / metrics-store definitions.

## Skip If (ANY kills it)

- Pre-launch viral — нечого мерити.
- Pure content marketing без direct invite mechanic — це attribution problem, не viral metrics.
- K-factor < 0.05 і stable — instrumentation overkill; fix loop first.

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
| `pro/marketing/growth-marketer` | Parent role context. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-artefact` | haiku | Template fill from header + section list. |
| `draft-rationale` | sonnet | Per-decision rationale + rejected alternatives. |
| `review-tradeoffs` | opus | Cross-decision synthesis + reversibility judgment. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config-skeleton.md` | Viral Metrics and K-factor skeleton — fill per artefact, do not commit free-form output. |
| `templates/_smoke-test.md` | Minimum viable filled-in Viral Metrics and K-factor. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-viral-metrics.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[viral-loops]]
- [[viral-optimization]]
- [[retention-metrics]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
