---
slug: library-evaluation-rubric
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Maintenance health (last commit, open-issue trend, bus factor), license, bundle-size impact, security history, ecosystem fit — picking THIS library, not just build vs buy.
content_id: "d9978bbe1c028747"
tags: [library-evaluation-rubric, dev, solo]
---

# Library Evaluation Rubric

## Summary

**One-sentence:** Maintenance health (last commit, open-issue trend, bus factor), license, bundle-size impact, security history, ecosystem fit — picking THIS library, not just build vs buy.

**One-paragraph:** `decision-tree-build-vs-buy` is too coarse — answers build vs buy, not WHICH library. Output: rubric + scored candidate list + decision record.

## Applies If (ALL must hold)

- developer about to add a new dependency
- dependency adds ≥1 transitive package OR new attack surface
- alternatives exist (≥2 plausible libraries)

## Skip If (ANY kills it)

- trivial dependency with established standard (e.g., 'lodash' for JS in 2020)
- build-vs-buy already decided as 'build'
- single-vendor lock decision already made

## Prerequisites

- list of 2-5 candidate libraries
- access to library's GitHub / package registry metadata
- ability to run bundle-size analysis

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/software-developer` | parent skill — provides operating context for this methodology |
| `solo/dev/software-developer` | peer methodology — produces inputs or consumes outputs |
| `solo/dev/decision-tree-build-vs-buy` | peer methodology — produces inputs or consumes outputs |

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

- parent skill: `solo/dev/software-developer/`
- peer methodology: `solo/dev/software-developer`
- peer methodology: `solo/dev/decision-tree-build-vs-buy`
- peer methodology: `solo/dev/automation-tooling`
- external: https://snyk.io/advisor/; https://npmtrends.com/; https://libraries.io/
