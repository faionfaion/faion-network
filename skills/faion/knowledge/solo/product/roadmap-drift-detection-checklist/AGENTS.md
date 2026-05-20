---
slug: roadmap-drift-detection-checklist
tier: solo
group: product
domain: product
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: Roadmap Drift Detection Checklist: a weekly PM-side diagnostic that scores roadmap-vs-actual drift before it silently erodes credibility.
content_id: "99463176e9ce4be7"
tags: [roadmap-drift-detection-checklist, product, solo]
---
# Roadmap Drift Detection Checklist

## Summary

**One-sentence:** A weekly 15-minute pulse-review checklist that scores roadmap-vs-actual drift across scope, schedule, and confidence and produces a delta record before drift becomes a stakeholder surprise.

**One-paragraph:** Roadmap-vs-actual drift is the silent killer of PM credibility; by the time stakeholders feel the gap, multiple weeks of compounding silent slippage have already happened. No existing methodology gives a PM a weekly diagnostic. This methodology fills the gap with a five-axis check (committed-vs-shipped scope, milestone date delta, confidence-band delta, dependency-status delta, and "narrative" delta — what the team is now saying vs. what the roadmap still says). Output is a single typed drift record per cycle that becomes the agenda for the Monday roadmap pulse review.

## Applies If (ALL must hold)

- there is a published roadmap (any format: doc, board, Gantt) covering the next 4–12 weeks
- at least one full reporting cycle has elapsed since the last drift check (default: 1 week)
- the PM has read access to current sprint/board status, shipped-changelog, and any active risk log
- tier == solo or higher

## Skip If (ANY kills it)

- the roadmap was published <7 days ago (nothing to drift against yet)
- the project is in an explicit "no-roadmap" discovery phase
- a formal change-control board already produces a weekly variance report covering the same axes — do not duplicate

## Prerequisites

- last week's drift record (or "n/a — first cycle")
- current roadmap snapshot (doc/board export, link, or version pin)
- shipped-this-week list (PRs merged, releases tagged, tasks moved to done)
- current risk / dependency log if one exists

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-manager` | parent role skill — provides operating context |
| `solo/product/product-planning` | roadmap-format conventions and confidence bands |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: cycle-cadence, five-axis-coverage, named-owner-per-delta, signed-confidence-delta, escalation-threshold | ~1100 |

## Related

- parent skill: `solo/product/product-manager`
- upstream playbook: `role-product-manager/Monday roadmap pulse review`
- sibling methodology: `solo/product/backlog-hygiene-cron-checklist`
