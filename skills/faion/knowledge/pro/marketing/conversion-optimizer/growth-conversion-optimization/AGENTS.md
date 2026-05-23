---
slug: growth-conversion-optimization
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Research-driven CRO cycle for web funnels: measure drop-off, research why, hypothesize testably, run A/B to statistical significance (\u2265 95%, \u2265 100 conv/variant, \u2265 2 weeks), implement winners, and curate a reusable learnings library."
content_id: "b6a66eca006c1431"
complexity: deep
produces: spec
est_tokens: 5000
tags: [cro, growth, a-b-testing, statistical-significance, marketing]
---
# Growth Conversion Optimization

## Summary

**One-sentence:** Research-driven CRO cycle for web funnels: measure drop-off, research why, hypothesize testably, run A/B to statistical significance (≥ 95%, ≥ 100 conv/variant, ≥ 2 weeks), implement winners, and curate a reusable learnings library.

**One-paragraph:** Research-driven CRO cycle for web funnels: measure drop-off, research why, hypothesize testably, run A/B to statistical significance (≥ 95%, ≥ 100 conv/variant, ≥ 2 weeks), implement winners, and curate a reusable learnings library. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Team has ≥ 1000 users / week per variant cell.
- Team has analytics + experiment infrastructure (GA + Optimizely / VWO / GrowthBook).
- Named CRO owner can run the cycle end-to-end within 4-6 week windows.

## Skip If (ANY kills it)

- Traffic insufficient for A/B testing (< 500 users / week / variant) — apply qualitative research first.
- No experiment infrastructure — set up tooling before running A/B tests.
- Pre-PMF — focus on retention and qualitative product-fit research.

**Ефективно для:**

- Growth-команди з достатнім traffic для A/B testing (≥ 1000 users/wk на варіант).
- CRO managers що будують першу learnings library після 5-10 експериментів.
- Команди де experiment-discipline drift через 'looks like it's working' decisions без significance.
- Аудит-ready середовища з вимогою statistical-rigour evidence на winners.

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
| `scripts/validate-growth-conversion-optimization.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[funnel-basics-framework]]
- [[growth-conversion-optimization]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
