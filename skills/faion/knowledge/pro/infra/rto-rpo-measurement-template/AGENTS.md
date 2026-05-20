---
slug: rto-rpo-measurement-template
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: RTO/RPO Measurement Template: turns DR drills from theatre into a measurable observation by defining the log format and timestamp checkpoints that produce actual RTO/RPO numbers.
content_id: "eca37e0c581ca39c"
tags: [rto-rpo-measurement-template, infra, pro]
---
# RTO/RPO Measurement Template

## Summary

**One-sentence:** A typed log format with mandatory timestamp checkpoints that turns a DR drill into a measured RTO/RPO observation, comparable to the committed paper number and to prior drills.

**One-paragraph:** Most teams know their committed RTO/RPO and have run drills, yet cannot tell you the actual observed RTO from last quarter's drill within ±30 minutes. That is because nobody captured the timestamps as the drill unfolded — they captured a narrative. This methodology defines the eight mandatory checkpoints (drill-start, failure-injected, detection-recognised, decision-to-failover, failover-begin, primary-traffic-restored, data-loss-window-measured, drill-closed), the time source policy (one authoritative clock, UTC), and the post-drill reconciliation that produces signed RTO and RPO observations. Output is a per-drill measurement record that can be charted across drills and compared against the committed numbers.

## Applies If (ALL must hold)

- a DR drill (tabletop, partial, or full failover) is being planned or run
- the team has a committed RTO/RPO target to measure against
- a single named drill conductor is appointed
- tier == pro or higher

## Skip If (ANY kills it)

- the drill is purely communications (no actual failover) — use a tabletop log, not this measurement template
- the system has no defined failover path (RTO/RPO is undefined; fix that first)
- the drill is shorter than the system's natural detection latency — measurement would be invalid

## Prerequisites

- committed RTO and RPO numbers per system in scope
- single authoritative time source (NTP server, or one operator's monotonic clock) declared before drill start
- drill conductor + at least one independent observer (not part of the failover team)
- prior measurement record (if any) for trend comparison

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/dr-drill-script-template` | the drill structure these timestamps annotate |
| `pro/infra/dr-drill-scenario-library` | upstream scenario catalog |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: eight-checkpoints, one-clock, independent-observer, data-loss-windowed, post-drill-reconciliation, target-vs-actual-delta | ~1200 |

## Related

- parent skill: `pro/infra/devops-engineer`
- upstream playbook: `role-devops-engineer/Disaster-recovery drill + plan refresh (4 weeks)`
- companion methodology: `pro/infra/rto-rpo-tracking-board`
