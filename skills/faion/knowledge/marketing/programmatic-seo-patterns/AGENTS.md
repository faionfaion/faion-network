# Programmatic SEO Patterns

## Summary

**One-sentence:** Produces a programmatic-SEO program plan: data source + template + intent-to-template map + indexability tiers + internal-link graph + thin-content guards.

**One-paragraph:** Programmatic SEO is the dominant SaaS growth lever (Webflow, Tinybird, Levels.fyi, Clay, Apollo). Template-driven pages backed by structured data: comparison pages, tool listings, location pages. Methodology gates the program on data quality, mandates intent-template fit (no comparison template for listing intent), enforces thin-content thresholds (≥300 unique words + ≥2 unique data points + schema markup or noindex), tiers indexability by data depth, and requires an internal-link graph (orphans waste crawl budget).

**Ефективно для:**

- SaaS / product з broad audience + structured data domain.
- Marketing capacity для templates + data pipeline maintenance.
- Competitive SEO landscape, де long-tail wins.
- Internal-link graph + thin-content guards + indexability tiers.

## Applies If (ALL must hold)

- SaaS / product with broad audience + structured data domain.
- Marketing capacity to build templates + maintain data pipeline.
- Competitive SEO landscape where long-tail wins.
- Internal-linking discipline + thin-content guards.

## Skip If (ANY kills it)

- Narrow B2B with no template-able pages.
- Regulated content (medical, financial) requiring per-page review.
- No structured data source — cannot template.
- Site authority too low to absorb new template inventory (DR <30).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Data source | DB / API / feed | data team |
| CMS / SSG capable of templated generation | stack doc | engineering |
| GSC + analytics access | dashboard | platform owner |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/seo-manager` | SEO baseline (technical + content) must be in place. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules for programmatic-seo-patterns | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | 1300 |
| `content/04-procedure.xml` | essential | 5-step procedure | 950 |
| `content/05-examples.xml` | medium | One worked end-to-end example | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule ref | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `intent-template-map` | sonnet | Per-intent template assignment. |
| `tier-classification` | haiku | Apply data-depth thresholds. |
| `link-graph-design` | sonnet | Sibling + parent pattern choice. |

## Templates

| File | Purpose |
|------|---------|
| `templates/program-plan.md.j2` | Programmatic-SEO program plan Markdown skeleton. |
| `templates/program-plan.md` | Programmatic-SEO program plan Markdown skeleton. Generated from `templates/program-plan.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/program-plan.json` | Schema-conformant sample artefact used by validator self-test. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-programmatic-seo-patterns.py` | Validate output artefact against the JSON Schema in `content/02-output-contract.xml` | Pre-commit hook + CI on every methodology PR |

## Related

- [[growth-paid-acquisition]]
- [[topic-cluster-architecture-with-eeat]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from one observable (do preconditions hold?) and maps each branch to a concrete `<conclusion ref="rule-id">` from `01-core-rules.xml`. Use it whenever the operator must choose between applying this methodology, deferring, or routing to a sibling.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/program-plan.json`

```json
{
  "data_source": {
    "provider": "internal_db",
    "refresh_cadence_days": 30,
    "quality_pct": 95
  },
  "intent_template_map": [
    {
      "intent": "comparison",
      "template_id": "tpl-vs"
    },
    {
      "intent": "listing",
      "template_id": "tpl-list"
    }
  ],
  "thin_content_threshold": {
    "min_words": 300,
    "min_data_points": 2,
    "schema_required": true
  },
  "indexability_tiers": {
    "tier_1": "indexed+sitemap",
    "tier_2": "indexed",
    "tier_3": "noindex"
  },
  "internal_link_graph": {
    "sibling_pattern": "category-siblings-5",
    "parent_pattern": "category-parent-1"
  },
  "owner": "seo-lead@faion.net"
}
```
