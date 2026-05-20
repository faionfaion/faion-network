---
slug: vendor-eval-framework
tier: geek
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Scoring matrix + trial protocol + rollback gate for in-house team buying $50-500/mo SaaS (Datadog vs Grafana, Linear vs Jira, Vercel vs Netlify).
content_id: "7f5ab29b42322748"
tags: [vendor-eval-framework, pm, geek]
---

# Vendor Evaluation Framework

## Summary

**One-sentence:** Scoring matrix + trial protocol + rollback gate for in-house team buying $50-500/mo SaaS (Datadog vs Grafana, Linear vs Jira, Vercel vs Netlify).

**One-paragraph:** build-vs-buy exists at solo tier. For in-house team buying $50-500/mo SaaS, there is no scoring matrix, trial protocol, rollback gate. Output: rubric + trial plan + rollback policy.

## Applies If (ALL must hold)

- team buying or replacing a SaaS vendor
- spend $50-500/month
- ≥2 plausible candidates

## Skip If (ANY kills it)

- trivial purchase under $50/month (over-engineered)
- enterprise procurement with formal RFP (different process)
- vendor mandated by parent company

## Prerequisites

- list of 2-5 candidate vendors
- scoring rubric (4-6 axes)
- trial sandbox capability

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/pm-agile` | parent skill — provides operating context for this methodology |
| `solo/dev/library-evaluation-rubric` | peer methodology — produces inputs or consumes outputs |
| `pro/product/vendor-evaluation-scorecard` | peer methodology — produces inputs or consumes outputs |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules | ~900 |
| `content/02-output-contract.xml` | essential | required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high |

## Related

- parent skill: `pro/pm/pm-agile/`
- peer methodology: `solo/dev/library-evaluation-rubric`
- peer methodology: `pro/product/vendor-evaluation-scorecard`
- peer methodology: `solo/dev/decision-tree-build-vs-buy`
- external: https://www.gartner.com/en/insights/sourcing-procurement; https://www.softwareadvice.com/buyers-guides
