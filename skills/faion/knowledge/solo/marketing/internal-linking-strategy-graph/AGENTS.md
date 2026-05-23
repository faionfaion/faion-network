---
slug: internal-linking-strategy-graph
tier: solo
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Hub-spoke internal-link graph for a solo content site — 1 hub per topic, ≥4 spokes per hub, anchor diversity, ≥2 inbound links per spoke, zero orphans.
content_id: "07d7b8c973f075c1"
complexity: medium
produces: spec
est_tokens: 4500
tags: [seo, internal-links, hub-spoke, topical-authority, link-equity]
---
# Internal Linking Strategy Graph

## Summary

**One-sentence:** Hub-spoke internal-link graph for a solo content site — 1 hub per topic, ≥4 spokes per hub, diversified anchor text, ≥2 inbound links per spoke, zero orphan pages.

**One-paragraph:** `growth-seo-link-building` covers external link acquisition; internal linking — the cheapest SEO lever a solopreneur owns — has no per-site methodology. This graph spec pins the topology: one hub page per topic cluster, ≥4 spokes per hub linking back to the hub, ≥2 inbound links per spoke from sibling spokes, no orphans (every page has ≥1 inbound from within the cluster). Anchor text is diversified across ≥3 surface forms per target to avoid over-optimisation. Output is the graph spec + a per-page link audit + orphan list + anchor-diversity report.

**Ефективно для:**

- Solo content sites with 30-300 indexed pages clustered into 3-10 topics.
- Surfacing orphan pages that get traffic from search but no internal authority.
- Sites preparing for a quarterly content audit (paired with [[internal-link-rotation-schedule]]).
- E-E-A-T topical-authority builds where internal structure carries the cluster.

## Applies If (ALL must hold)

- Site has ≥30 indexed content pages organised (or organisable) into topic clusters.
- Operator can edit posts to insert/remove internal links (CMS access).
- A crawler exists or can be wired (Screaming Frog, Ahrefs, custom Python).
- Operator has assigned at least one hub candidate per planned cluster.

## Skip If (ANY kills it)

- Site is &lt;30 pages — internal linking adds noise without payoff at that scale.
- Site is a transactional store with no editorial content (PLP/PDP only).
- Operator cannot edit pages (locked CMS, third-party blog).
- The "cluster" boundaries are not meaningful — every page is a one-off.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Crawl export with URL + in-links + out-links | CSV | Screaming Frog / similar |
| Topic-cluster assignment per page | CSV | content strategist |
| Hub candidate per cluster | URL | content strategist |
| Anchor-text inventory per target URL | CSV | crawler export |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[internal-link-rotation-schedule]] | Sibling methodology; this graph spec produces the audit list it consumes. |
| [[hook-bank-template]] | Anchor-text variants benefit from hook patterns. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: 1 hub per topic, ≥4 spokes, ≥2 inbound per spoke, no orphans, anchor diversity ≥3, hub-link from every spoke | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for graph spec + audit report + valid/invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: orphans-untouched, exact-match-overload, hub-bloat, missing-hub-backlinks | 700 |
| `content/04-procedure.xml` | essential | 6-step procedure: crawl → cluster → assign hubs → audit links → emit fixes → re-crawl | 800 |
| `content/05-examples.xml` | essential | Worked example: 120-page solo site with 6 clusters and 11 orphans found | 700 |
| `content/06-decision-tree.xml` | essential | Tree routing observables → rule id | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `crawl_normalise` | haiku | Mechanical CSV transform. |
| `cluster_assignment` | sonnet | Topic-tag judgement with cluster boundaries. |
| `anchor_diversity_check` | haiku | Set-cardinality arithmetic. |
| `fix_emission` | sonnet | Generate add-link / remove-link diffs per page. |

## Templates

| File | Purpose |
|------|---------|
| `templates/graph-spec.yaml` | Hub-spoke graph spec skeleton |
| `templates/audit-report.md` | Per-cluster audit findings markdown |
| `templates/_smoke-test.json` | Minimum viable graph + audit for validator self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-internal-linking-strategy-graph.py` | Validate graph spec + audit against 02-output-contract schema | Pre-commit / quarterly audit |

## Related

- [[internal-link-rotation-schedule]]
- [[hook-bank-template]]
- [[in-issue-ad-format-library]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps page count, cluster definitions, hub assignment, and CMS access to a rule from `01-core-rules.xml`, telling the agent whether to publish the audit, block on a missing constraint, or skip the methodology. Walk it on every fresh quarterly audit; do not cache outcomes across audits.
