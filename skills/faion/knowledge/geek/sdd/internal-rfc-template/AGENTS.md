---
slug: internal-rfc-template
tier: geek
group: sdd
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Light-weight Request-for-Comments for proposals NOT yet decisions — more open than ADR, less heavy than design-doc.
content_id: "5b794da3d3216159"
tags: [internal-rfc-template, sdd, geek]
---

# Internal RFC Template

## Summary

**One-sentence:** Light-weight Request-for-Comments for proposals NOT yet decisions — more open than ADR, less heavy than design-doc.

**One-paragraph:** Solo/Pro have design-docs and ADR. In-house teams need a lighter RFC for proposals NOT yet decisions. Covers: motivation, proposal, alternatives, open questions, status (draft/discussion/accepted/rejected/superseded). Output: RFC template + lifecycle + retirement policy.

## Applies If (ALL must hold)

- team ≥5 with shared decisions to make
- team has authority to standardize a doc format
- decisions exist that ADR is too final for (need open discussion phase)

## Skip If (ANY kills it)

- team uses Pull Requests as RFC vehicle already
- decisions all flow from one tech lead (no comment-needed)
- fully heavyweight RFC process exists (don't duplicate)

## Prerequisites

- shared doc store (GitHub Discussions, Outline, Notion)
- named RFC editor or rotation
- decision-makers identified per topic area

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/sdd/sdd` | parent skill — provides operating context for this methodology |
| `pro/dev/team-rfc-process-for-devs` | peer methodology — produces inputs or consumes outputs |
| `solo/dev/architecture-decision-records` | peer methodology — produces inputs or consumes outputs |

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

- parent skill: `solo/sdd/sdd/`
- peer methodology: `pro/dev/team-rfc-process-for-devs`
- peer methodology: `solo/dev/architecture-decision-records`
- external: https://github.com/rust-lang/rfcs/blob/master/text/0002-rfc-process.md (Rust RFC); https://oxide.computer/blog/rfd-1-requests-for-discussion (Oxide RFD)
