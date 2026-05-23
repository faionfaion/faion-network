---
slug: growth-press-coverage
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Relationship-driven press outreach: tier journalists (Tier-3 niche first), research beat + recent articles, craft newsworthy angle, send personalized pitch <150 words.
content_id: "d8ca812bd8cb62c4"
complexity: deep
produces: playbook-step
est_tokens: 4200
tags: [press, pr, journalists, pitch, coverage]
---
# Press & PR Coverage

## Summary

**One-sentence:** Relationship-driven press outreach: tier journalists (Tier-3 niche first), research beat + recent articles, craft newsworthy angle, send personalized pitch <150 words.

**One-paragraph:** Relationship-driven press outreach: tier journalists (Tier-3 niche first), research beat + recent articles, craft newsworthy angle, send personalized pitch <150 words. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

**Ефективно для:**

- Перед product launch / major release — press wave спершу за Tier-3.
- Founder-led PR (no PR firm) — методологія є substitute для $5-10k/mo retainer.
- При milestones (funding, launch, milestone metric) — coverage compounds.
- Як continuous flow: 1 pitch на тиждень, монотонно.

## Applies If (ALL must hold)

- Newsworthy event (launch, funding, milestone, data, partnership) у наступних 30 днях.
- Founder / spokesperson доступний для interviews + quick turnarounds (24-48h).
- CRM / spreadsheet для journalist tracking + follow-ups.

## Skip If (ANY kills it)

- Nothing actually newsworthy — manufactured news fails 95%+ of time.
- Founder unavailable for follow-up calls / quotes — pitch lands then dies.
- Pure local/niche product needing only community channels — press irrelevant.

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
| `pro/marketing/gtm-strategist` | Parent role context. |

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
| `templates/playbook-step-skeleton.md` | Press & PR Coverage skeleton — fill per artefact, do not commit free-form output. |
| `templates/_smoke-test.md` | Minimum viable filled-in Press & PR Coverage. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-growth-press-coverage.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[growth-product-hunt-launch]]
- [[growth-hacker-news-launch]]
- [[agency-niche-positioning]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
