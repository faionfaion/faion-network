---
slug: methodology-contribution-flow-open-authorship
tier: pro
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: PR template, review rubric, signing/attribution policy, contributor-tier revenue-share for open contribution of faion methodologies.
content_id: "5c215bbf81b3d9df"
tags: [methodology-contribution-flow-open-authorship, sdlc-ai, pro]
---

# Methodology Contribution Flow (Open Authorship)

## Summary

**One-sentence:** PR template, review rubric, signing/attribution policy, contributor-tier revenue-share for open contribution of faion methodologies.

**One-paragraph:** P7 builds vertical agents on narrow domains and will produce methodology IP. Today no open contribution path. faion authoring is self-bottleneck. Output: PR template + review rubric + attribution + revenue-share policy.

## Applies If (ALL must hold)

- external contributor wants to add a methodology to faion
- topic falls within faion's tier coverage (free/solo/pro/geek)
- contributor accepts CLA-equivalent attribution terms

## Skip If (ANY kills it)

- internal faion content (different review path)
- minor edits / typo fixes (use lightweight PR)
- non-methodology contribution (skill structure, tooling)

## Prerequisites

- contributor has GitHub account + signed CLA
- topic checked against existing methodology + playbook list
- draft conforms to v2 methodology shape

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/sdlc-ai/methodology-contribution-flow` | parent skill — provides operating context for this methodology |
| `geek/sdlc-ai/methodology-contribution-flow` | peer methodology — produces inputs or consumes outputs |
| `pro/sdd/internal-rfc-template` | peer methodology — produces inputs or consumes outputs |

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

- parent skill: `geek/sdlc-ai/methodology-contribution-flow/`
- peer methodology: `geek/sdlc-ai/methodology-contribution-flow`
- peer methodology: `pro/sdd/internal-rfc-template`
- external: https://opensource.guide/how-to-contribute/; https://github.com/cla-assistant/cla-assistant; https://contributor-covenant.org/
