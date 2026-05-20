---
slug: internal-link-audit
tier: pro
group: marketing
domain: growth-marketer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: SOP for auditing and rewiring internal links across a content site to support topic clusters, distribute authority, and surface orphan pages.
content_id: "395667c72a6c13fa"
tags: [seo, internal-linking, topic-cluster, audit, orphan-pages, link-equity]
---
# Internal Link Audit

## Summary

**One-sentence:** SOP for auditing and rewiring internal links across a content site to support topic clusters, distribute authority, and surface orphan pages.

**One-paragraph:** SEO methodologies often stop at off-site link building, but topic-cluster strategy stands or falls on internal linking discipline — and few teams have a recurring audit. This methodology defines a quarterly audit: crawl the site, build the internal-link graph, compute per-page incoming-link counts, flag orphans (0 internal links), flag over-linked hubs (&gt; 200 internal links), audit anchor-text distribution per cluster, and produce a rewire plan. Mechanism: tooling-agnostic workflow (Screaming Frog / Sitebulb / in-house crawler), cluster-pillar adjacency graph, anchor-text rubric per cluster, and a change-batch with documented before/after metrics. Primary output: a rewire plan with prioritized link additions / removals, paired with a pre/post metrics commitment to verify the rewire moved cluster ranking.

## Applies If (ALL must hold)

- site has ≥ 30 published content pages with topical structure
- team operates ≥ 1 topic cluster (pillar + ≥ 5 cluster pages)
- crawl tooling available (Screaming Frog, Sitebulb, Ahrefs, Semrush, in-house)
- analytics has 90+ days of organic search baseline
- a content-ops owner exists with publish permissions

## Skip If (ANY kills it)

- pure single-product landing site (no content layer)
- &lt; 30 pages — manual review beats audit overhead
- e-commerce category structure where internal linking is driven by faceted nav (use ecommerce-specific SOP)
- site under active migration (URL changes pending) — audit after migration settles
- regulated content (medical / legal disclaimers) where editorial change requires legal sign-off

## Prerequisites (must be true before starting)

- complete site URL list (sitemap.xml + crawl)
- exported internal-link graph (source URL, target URL, anchor text)
- topic-cluster map (pillar pages + cluster member pages)
- 90-day organic baseline per cluster (rankings, impressions, clicks)
- change-batch staging environment OR PR-based editing workflow

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/seo-manager/topical-authority` | Cluster structure that internal linking reinforces |
| `pro/marketing/growth-marketer/aarrr-pirate-metrics` | Optional baseline tracking |
| `pro/marketing/growth-marketer/seo-techniques` | Companion off-site link-building methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: pillar-to-cluster adjacency, orphan elimination, anchor diversity, no over-linked hubs, before/after metrics | ~1000 |
| `content/02-output-contract.xml` | essential | Rewire plan schema, per-page action list, pre/post commitments | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes (cascade re-link, anchor mono-tagging, orphan recreate, etc.) | ~1100 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `crawl_normalizer` | haiku | Convert crawler export to standard graph format |
| `orphan_detector` | haiku | Find pages with 0 incoming internal links |
| `anchor_text_classifier` | sonnet | Tag anchors as exact-match, partial, generic, branded |
| `rewire_plan_synth` | opus | Synthesize per-cluster rewire plan, prioritize by impact |
| `before_after_metrics_designer` | sonnet | Define metrics to validate rewire |

## Templates

| File | Purpose |
|------|---------|
| `templates/rewire-plan.md` | Per-page action list (add / remove / change anchor) |
| `templates/anchor-rubric.md` | Anchor-text diversity scoring rubric |
| `templates/cluster-adjacency-map.md` | Pillar + cluster member map |
| `templates/before-after-metrics.md` | Pre/post tracking commitment |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/link-graph-builder.py` | Build internal-link graph from crawler CSV | Audit start |
| `scripts/orphan-finder.py` | List pages with 0 incoming internal links | Audit start |
| `scripts/anchor-diversity-report.py` | Per-cluster anchor distribution | Audit middle |
| `scripts/rewire-validator.py` | Diff before/after graph; verify changes applied | Post-rewire |

## Related

- parent skill: `pro/marketing/growth-marketer/`
- peer methodologies: `topical-authority`, `seo-techniques`
- external: [Screaming Frog docs](https://www.screamingfrog.co.uk/seo-spider/) · [Ahrefs internal-link guide](https://ahrefs.com/blog/internal-links-for-seo/)
