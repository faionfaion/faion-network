---
slug: plg-implementation-guide
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "5-phase sequential PLG implementation roadmap: Foundation (Aha + TTV) \u2192 Free Tier Design \u2192 Activation Optimization \u2192 Monetization \u2192 Expansion. Each phase depends on prior instrumentation; running out-of-order causes false-confidence."
content_id: "00c2db2b9ac54a7b"
complexity: deep
produces: spec
est_tokens: 5000
tags: [plg, implementation, playbooks, aha-moment, pql, marketing]
---
# PLG Implementation Guide

## Summary

**One-sentence:** 5-phase sequential PLG implementation roadmap: Foundation (Aha + TTV) → Free Tier Design → Activation Optimization → Monetization → Expansion. Each phase depends on prior instrumentation; running out-of-order causes false-confidence.

**One-paragraph:** 5-phase sequential PLG implementation roadmap: Foundation (Aha + TTV) → Free Tier Design → Activation Optimization → Monetization → Expansion. Each phase depends on prior instrumentation; running out-of-order causes false-confidence. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- PLG model selected via plg-basics methodology.
- Engineering team has bandwidth for 12-16 weeks of phased rollout.
- Named PLG owner can sequence + sign-off each phase gate.

## Skip If (ANY kills it)

- PLG model not yet selected — run plg-basics first.
- Pre-PMF — phases assume basic activation works; pre-PMF teams should focus on value-prop.
- Already running mature PLG — apply plg-optimization-tactics instead.

**Ефективно для:**

- SaaS teams що мають PLG model decision але без operational rollout plan.
- Engineering leads що мапують ticket dependencies для quarterly OKRs.
- Marketing managers що пишуть першу phased PLG rollout spec.
- Аудит-ready середовища з вимогою sequenced phase-gate evidence.

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
| `scripts/validate-plg-implementation-guide.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[plg-basics]]
- [[plg-implementation-guide]]
- [[plg-metrics]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
