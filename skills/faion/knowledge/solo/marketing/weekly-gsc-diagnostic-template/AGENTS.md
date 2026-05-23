---
slug: weekly-gsc-diagnostic-template
tier: solo
group: marketing
domain: marketing
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Weekly Search Console review template: top movers, query intent shift, indexation health, action — turns GSC numbers into a one-page verdict.
content_id: "13393509123578fc"
complexity: medium
produces: spec
est_tokens: 4300
tags: ["weekly-gsc-diagnostic-template", "marketing", "seo", "search-console", "solo"]
---
# Weekly GSC Diagnostic Template

## Summary

**One-sentence:** Weekly Search Console review template: top movers, query intent shift, indexation health, action — turns GSC numbers into a one-page verdict.

**One-paragraph:** Search Console dumps numbers; founders need a verdict. This methodology pins a weekly 60-min ritual that produces a one-page report: top click/impression winners and losers, query-intent shift, indexation health, ≥1 named action with owner. Output is a versioned spec ready for the next-week comparison.

**Ефективно для:**

- Solo SEO operator with ≥50 ranking pages who opens GSC every Monday, stares at the chart, and closes it without writing anything down. Needs a 60-min ritual that ends with one decision.

## Applies If (ALL must hold)

- Site has ≥50 ranking pages in GSC
- GSC property verified ≥30 days ago (data settled)
- Founder has 60 min/week to review

## Skip If (ANY kills it)

- <50 ranking pages — noise dominates signal
- GSC verified <30 days ago — data unreliable
- Paid traffic dominates — use ppc-diagnostic instead

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| GSC property URL | URL | Search Console |
| Last week's GSC export (Performance report, 7 days) | CSV | Search Console export |
| Indexation status (pages discovered/indexed/excluded) | table | GSC Coverage report |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/seo-manager` | Parent skill — provides the broader SEO operating context. |
| `pro/marketing/conversion-optimizer` | Peer methodology — downstream of GSC diagnostic when query→landing-page intent shifts. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules incl. skip-this-methodology + run-the-checklist | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-weekly-gsc-diagnostic-template` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-weekly-gsc-diagnostic-template` | haiku | Schema check + threshold checks; deterministic. |
| `review-weekly-gsc-diagnostic-template` | opus | Cross-cycle synthesis; high-stakes change to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/weekly-gsc-diagnostic-template.json` | JSON skeleton conforming to the output contract schema. |
| `templates/weekly-gsc-diagnostic-template.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-weekly-gsc-diagnostic-template.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[weekly-growth-review-rhythm]]
- [[growth-newsletter-growth]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
