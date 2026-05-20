---
slug: edge-and-cdn-strategy
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Edge compute (Cloudflare Workers / Lambda@Edge / Fastly Compute), cache key design, origin shielding, edge auth — the strategy gcp-storage-cdn is missing.
content_id: "4ed645f7ed991d84"
tags: [edge-and-cdn-strategy, infra, pro]
---

# Edge and CDN Strategy

## Summary

**One-sentence:** Edge compute (Cloudflare Workers / Lambda@Edge / Fastly Compute), cache key design, origin shielding, edge auth — the strategy gcp-storage-cdn is missing.

**One-paragraph:** Only gcp-storage-cdn exists. No methodology on edge compute, cache key design, origin shielding, edge auth. Output: edge platform pick + cache key policy + origin-shield plan + auth pattern.

## Applies If (ALL must hold)

- global product or audience (≥3 continents OR ≥10% traffic outside primary region)
- p95 latency target <200ms global
- team has authority to introduce edge compute or new CDN

## Skip If (ANY kills it)

- single-region product with no global traffic
- compliance overrides forcing single-region (e.g., regulated data residency)
- team has zero observability — cannot reason about edge effects

## Prerequisites

- current CDN + origin architecture diagram
- request volume + geographic distribution
- list of compute use cases for edge (auth, A/B, redirects, image)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer` | parent skill — provides operating context for this methodology |
| `pro/infra/cicd-engineer` | peer methodology — produces inputs or consumes outputs |
| `pro/infra/infrastructure-engineer` | peer methodology — produces inputs or consumes outputs |

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

- parent skill: `pro/infra/devops-engineer/`
- peer methodology: `pro/infra/cicd-engineer`
- peer methodology: `pro/infra/infrastructure-engineer`
- peer methodology: `solo/infra/server-craft`
- external: https://developers.cloudflare.com/workers/; https://docs.aws.amazon.com/lambda/latest/dg/lambda-edge.html; https://docs.fastly.com/products/compute
