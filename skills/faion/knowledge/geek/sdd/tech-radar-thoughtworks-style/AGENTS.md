---
slug: tech-radar-thoughtworks-style
tier: geek
group: sdd
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: `tech-radar.md` with Adopt / Trial / Assess / Hold quadrants — the shared opinion past-5-devs teams need before 7 state-mgmt libs ship.
content_id: "290144f7bf962b44"
tags: [tech-radar-thoughtworks-style, sdd, geek]
---

# Tech Radar (ThoughtWorks-style)

## Summary

**One-sentence:** `tech-radar.md` with Adopt / Trial / Assess / Hold quadrants — the shared opinion past-5-devs teams need before 7 state-mgmt libs ship.

**One-paragraph:** Companies past 5 devs need a tech-radar (Adopt/Trial/Assess/Hold). Without it: PRs introduce 7 different state-mgmt libs because no shared opinion exists. faion has no methodology for authoring or maintaining one. Output: tech-radar template + quarterly review process + decision authority.

## Applies If (ALL must hold)

- engineering team ≥5
- decisions about libraries / patterns recur
- named tech leadership with authority

## Skip If (ANY kills it)

- team <5 — over-engineered
- team is constrained to a single tech stack (no choices to make)
- team uses TW's hosted radar — augment, don't duplicate

## Prerequisites

- list of current technologies in active use
- named radar maintainers (≥2 for rotation)
- review cadence agreement

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/sdd/sdd` | parent skill — provides operating context for this methodology |
| `solo/dev/architecture-decision-records` | peer methodology — produces inputs or consumes outputs |
| `geek/sdlc-ai/methodology-contribution-flow-open-authorship` | peer methodology — produces inputs or consumes outputs |

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
- peer methodology: `solo/dev/architecture-decision-records`
- peer methodology: `geek/sdlc-ai/methodology-contribution-flow-open-authorship`
- peer methodology: `pro/dev/team-rfc-process-for-devs`
- external: https://www.thoughtworks.com/radar; https://www.thoughtworks.com/radar/how-to-byor
