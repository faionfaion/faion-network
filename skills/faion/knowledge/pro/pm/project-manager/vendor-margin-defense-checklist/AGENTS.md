---
slug: vendor-margin-defense-checklist
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "3a4fb354b3df863f"
summary: A 6-pattern checklist that detects silent margin-eroding behaviours (silent scope creep, free analysis, missing change requests, AI rework loops, gold-plating, sympathy discounting) before they consume 10-20% of fixed-price project margin.
tags: [margin-defense, outsource, fixed-price, scope-creep, vendor]
---

# Vendor Margin Defense Checklist

## Summary

**One-sentence:** A 6-pattern checklist that detects silent margin-eroding behaviours (silent scope creep, free analysis, missing change requests, AI rework loops, gold-plating, sympathy discounting) before they consume 10-20% of fixed-price project margin.

**One-paragraph:** Fixed-price outsource engagements lose margin not to dramatic incidents but to slow leaks: a free 4-hour analysis call that should have been billable, a "small change" that doubled scope, an AI agent looping on rework because no one wrote the change request, the senior dev gold-plating a UI nobody asked for. This methodology codifies 6 detection patterns with weekly check-ins and a "margin-bleed alert" rule (any single bleed &gt; 5% of project margin → discuss with client within 48h). Output: `MarginBleedReport` with detected leaks + remediation actions. Built on Patrick McKenzie consulting essays and Jonathan Stark fixed-price playbook.

## Applies If (ALL must hold)

- engagement is fixed-price OR T&amp;M with a budget cap
- project duration ≥ 3 weeks (shorter doesn't accumulate enough patterns to detect)
- there is a written statement-of-work with deliverables
- there is at least one weekly client checkpoint

## Skip If (ANY kills it)

- engagement is open-ended T&amp;M with no cap — no margin to defend
- engagement is &lt; 2 weeks — overhead exceeds value
- client relationship is months-old retainer with high trust — pattern detection is noise
- engagement value &lt; $5k — overhead exceeds protected margin

## Prerequisites

- written statement-of-work with explicit deliverables list
- written change-request process (template + threshold for "small change")
- billable hours tracked against the project (per `solo-time-tracking-discipline`)
- baseline expected margin (from quote / proposal)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/project-manager/scope-creep-management` | Generic upstream; this is the bleed-specific complement |
| `solo/pm/project-manager/solo-time-tracking-discipline` | Provides the hours data feeding the bleed detector |
| `pro/comms/communicator/client-communication` | Used for the "discuss with client within 48h" alert action |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: 6-pattern coverage, weekly cadence, bleed alert threshold, written change request, billable-by-default | ~1000 |
| `content/02-output-contract.xml` | essential | `MarginBleedReport` schema with per-pattern severity | ~700 |
| `content/03-failure-modes.xml` | essential | 6 modes: noise tolerance, polite-tax, false free analysis | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `time_log_pattern_scan` | haiku | Mechanical detection against rules |
| `pattern_classification` | sonnet | Bounded judgment |
| `bleed_quantification` | sonnet | Cost math |
| `client_message_draft` | sonnet | Diplomatic but clear copy |

## Templates

| File | Purpose |
|------|---------|
| `templates/bleed-report.json` | Output schema |
| `templates/change-request.md` | Template the vendor can send when scope shifts |
| `templates/margin-alert-message.md` | Diplomatic client message for bleed &gt; 5% |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/weekly-bleed-scan.py` | Scans time logs + comms threads for 6 patterns | Friday end-of-week |
| `scripts/bleed-alert.py` | Triggers client-message draft when bleed &gt; 5% | After scan |

## Related

- parent skill: `pro/pm/project-manager/`
- peer methodologies: `scope-creep-management`, `solo-time-tracking-discipline`
- external: [Patrick McKenzie — Salary Negotiation / Consulting essays](https://www.kalzumeus.com/) · [Jonathan Stark — Hourly Billing Is Nuts](https://jonathanstark.com/hbinz) · [Blair Enns — Pricing Creativity](https://blairenns.com/) · [Brennan Dunn — Double Your Freelancing Rate](https://doubleyourfreelancing.com/)
