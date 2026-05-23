---
slug: competitor-creative-scrape-ai
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "AI-assisted pipeline that scrapes competitor ad creatives (Meta Ad Library / TikTok / LinkedIn), classifies them by hook/visual/CTA, and produces a weekly CRO-experiment-ready report with named owner and 90-day retention."
content_id: "8403968219e662a8"
complexity: medium
produces: report
est_tokens: 5000
tags: [growth-marketing, creative-scraping, ai-pipeline, competitive-intel, marketing]
---
# Competitor Creative Scrape AI

## Summary

**One-sentence:** AI-assisted pipeline that scrapes competitor ad creatives (Meta Ad Library / TikTok / LinkedIn), classifies them by hook/visual/CTA, and produces a weekly CRO-experiment-ready report with named owner and 90-day retention.

**One-paragraph:** AI-assisted pipeline that scrapes competitor ad creatives (Meta Ad Library / TikTok / LinkedIn), classifies them by hook/visual/CTA, and produces a weekly CRO-experiment-ready report with named owner and 90-day retention. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Team runs paid acquisition on Meta / TikTok / LinkedIn ad platforms.
- Team has ≥ 3 named direct competitors with active ad spend.
- Named CRO owner can act on the weekly report within 5 business days.

## Skip If (ANY kills it)

- No paid acquisition channel — creative-scrape inspiration has no use surface.
- No identified competitor list — define competitors before automating the scrape.
- Team has < 1 hr/week to read the report — automate other parts of the pipeline first.

**Ефективно для:**

- Growth-команди що ведуть weekly CRO experiment cadence на primary landing page.
- Performance marketers що потребують hook inspiration кожні 5-7 днів.
- Команди з 3-5 ключовими конкурентами що активно рекламуються в Meta / TikTok.
- Аудит-ready середовища з вимогою evidence-anchored creative claims.

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
| `content/05-examples.xml` | essential | Worked example from input to filled artefact | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-report` | haiku | Template fill from header + section list. |
| `populate-evidence` | sonnet | Per-row evidence link + summary judgment. |
| `outcome-synthesis` | opus | Cross-cycle synthesis of outcome impact. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Report skeleton with frontmatter + sections + evidence anchors per row. |
| `templates/_smoke-test.md` | Minimum viable filled-in instance. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-competitor-creative-scrape-ai.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[competitor-creative-scrape-ai]]
- [[content-distribution-orchestration]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
