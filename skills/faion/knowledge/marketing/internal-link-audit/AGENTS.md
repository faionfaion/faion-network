# Internal Link Audit

## Summary

**One-sentence:** Generates a quarterly internal-link audit: per-page incoming counts, orphans, over-linked hubs, anchor-text distribution, rewire plan.

**One-paragraph:** Generates a quarterly internal-link audit: per-page incoming counts, orphans, over-linked hubs, anchor-text distribution, rewire plan. Use it when site має >=30 published content pages з topical structure. The methodology pins the artefact shape via JSON Schema in `content/02-output-contract.xml`, so a downstream agent can validate the output mechanically rather than by prose review.

**Ефективно для:**

- Site має >=30 published content pages з topical structure.
- Team operates >=1 topic cluster (pillar + >=5 cluster pages).
- Crawl access (Screaming Frog / Sitebulb / in-house) налаштований.
- Pre/post metrics commitment задокументовано.

## Applies If (ALL must hold)

- The site has at least 30 indexable content pages and at least one declared topic cluster (a pillar URL plus 5 or more cluster URLs).
- A crawler with JavaScript rendering and link-position classification (Screaming Frog, Sitebulb or in-house) can crawl the full host inside the audit period.
- The XML sitemap and the CMS published-page count are available to reconcile the crawl against.
- Google Search Console Performance data for the site is accessible for the 28 days before the period end.
- An editor with CMS access is named to own the rewire items and a re-measurement date at least 8 weeks out is acceptable.

## Skip If (ANY kills it)

- Fewer than 30 indexable pages or no declared cluster: fix links by hand while publishing and return when the site passes 30 pages.
- The crawler cannot render JavaScript or cannot export link position, so contextual counts cannot be separated from navigation and footer links.
- Search Console access is not available, so no pre/post baseline can be captured before the rewire ships.
- The team wants a list of orphans and hubs without committing a named person to rewire, redirect or deindex decisions.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Rendered crawl export | per-page rows: URL, status, indexability, canonical, plus inlinks with link position (content, navigation, footer, sidebar, breadcrumb) and anchor text | Screaming Frog, Sitebulb or in-house crawler, run inside the audit period |
| XML sitemap and CMS page count | URL count from the sitemap; published-page count from the CMS | site sitemap; CMS admin |
| Declared clusters | pillar URL plus 5 or more cluster URLs per cluster | content calendar / SEO lead |
| Analytics-only URLs | landing pages with sessions but no crawl inlinks | GA4 or equivalent |
| Search Console baseline | clicks, impressions, average position per URL for the 28 days before the period end | Google Search Console Performance report |
| `templates/internal-link-audit.report.md.j2` | report skeleton with the reconciliation, matrix, anchor, plan and baseline tables | this methodology |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/marketing/growth-marketer/AGENTS.md` | Parent skill vocabulary + neighbouring methodologies |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: crawl reconciled to sitemap, contextual counts exclude boilerplate, every orphan gets a decision, pillar-cluster reciprocity, descriptive anchors, links to final URL, fully specified rewire items, Search Console pre/post baseline | 2450 |
| `content/02-output-contract.xml` | essential | Draft-07 schema of the audit report: rendered crawl reconciled to sitemap and CMS with gaps over 5 percent explained, contextual vs boilerplate counts and hubs, orphans with one decision each, pillar-cluster matrix with incomplete flag, anchor-text distribution with generic anchors, hygiene findings, fully specified rewire plan, 28-day Search Console baseline and an 8-week re-measurement; valid and invalid reports; 8 forbidden patterns | 6750 |
| `content/03-failure-modes.xml` | essential | 3+ antipatterns with symptom/root-cause/fix | 950 |
| `content/04-procedure.xml` | essential | 8 steps: run and reconcile the crawl, split counts by link position, decide every orphan, build the cluster matrix, tabulate anchor text, list hygiene findings, write the rewire plan, capture the Search Console baseline and validate | 1750 |
| `content/05-examples.xml` | recommended | Complete report for a 412-page deliverability site (7.4 percent CMS gap explained, /blog hub, two orphan decisions, six-page cluster with two missing edges, four pasteable rewire items, three baselines, re-measurement 61 days out) with a note per value, plus a partial-crawl report and what the validator prints | 3450 |
| `content/06-decision-tree.xml` | essential | Decision tree: observable signals -> rule from 01-core-rules.xml | 650 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `gather-inputs` | haiku | Mechanical extraction from upstream artefacts |
| `apply-rules` | sonnet | Apply `01-core-rules.xml` + decision tree against state |
| `synthesise-output` | sonnet | Final artefact authoring matching `02-output-contract.xml` |
| `validate-output` | haiku | Run `scripts/validate-internal-link-audit.py` against the artefact |

## Templates

| File | Purpose |
|------|---------|
| `templates/internal-link-audit.report.md.j2` | Markdown report skeleton with 5-line header |
| `templates/internal-link-audit.report.md` | Markdown report skeleton with 5-line header Generated from `templates/internal-link-audit.report.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/internal-link-audit.example.json` | Example output JSON conforming to 02-output-contract.xml |
| `templates/_smoke-test.json` | Minimum viable filled-in artefact for the validator self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-internal-link-audit.py` | Validate produced artefact against `02-output-contract.xml` schema | After `synthesise-output`, before commit/publish |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `pro/marketing/growth-marketer/`
- [[ab-testing-setup]]
- [[north-star-metric]]
- [[activation-framework]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (artefact shape, freshness, scope) to either a `run-the-methodology` conclusion or a `skip-this-methodology` conclusion, with every leaf referencing a rule id from `01-core-rules.xml`. Use it when the operator is unsure whether this methodology applies to the current task.
