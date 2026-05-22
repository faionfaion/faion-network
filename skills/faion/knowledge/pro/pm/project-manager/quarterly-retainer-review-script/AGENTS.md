---
slug: quarterly-retainer-review-script
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "3ce9cb28c133cbbc"
summary: A 45-minute scripted quarterly review call for retainer clients that converts utilization data into renewal commitment.
tags: [retainer, client-review, qbr, renewal, micro-agency, account-management]
---
# Quarterly Retainer Review Script

## Summary

**One-sentence:** A 45-minute scripted quarterly review call for retainer clients that converts utilization data into renewal commitment.

**One-paragraph:** Existing stakeholder-engagement methodology is generic; this gives a micro-agency founder (1-10 retainer clients) the exact talking points, slide order, and decision framework for a 45-min QBR (Quarterly Business Review). Mechanism: prepares a 6-slide deck driven by retainer utilization data (hours used vs. hours bought, %SLA met, scope creep delta), runs the call in 4 segments (data review 10 min → outcomes 15 min → blockers 10 min → renewal 10 min), captures explicit "continue / scale up / scope down / terminate" decision before hanging up, and emails a 1-page summary within 24h. Primary output: signed-off renewal decision + scope delta for next quarter.

## Applies If (ALL must hold)

- you operate a retainer-based service business (agency, consultancy, freelance) with ≥3 active retainer clients
- retainer contracts have a renewal/review cadence (monthly, quarterly, or semi-annually)
- you track hours, deliverables, and SLA adherence per client
- the client is the decision-maker for renewal (not a procurement gatekeeper)

## Skip If (ANY kills it)

- one-shot project work — use a project-closure script instead
- corporate enterprise sales-led renewal (procurement-driven, 90-day cycle) — use enterprise QBR template
- pre-launch / first quarter of a new retainer — use kickoff review instead
- retainer is < $2k/month — overhead exceeds value; use a 15-min email check-in
- client is delinquent on payments — collections call comes first, not a QBR

## Prerequisites (must be true before starting)

- retainer utilization data for the closing quarter (hours used, hours bought, % SLA met)
- previous QBR notes (if Q2+) — track promises kept vs. broken
- list of deliverables shipped this quarter with client-facing artifact links
- next-quarter capacity forecast (your team's hours available)
- client stakeholders confirmed on the calendar invite 5 business days ahead

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/gtm-strategist/ops-customer-success-metrics` | Source of utilization + SLA metrics consumed by the script |
| `pro/product/product-operations/account-health-scoring-model` | If implemented, feeds the green/yellow/red status used in slide 2 |
| `pro/pm/project-manager/cost-estimation` | Used to scope the "next quarter capacity" slide |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: 45-min cap, named decision exit, data over narrative, scope delta written, 24h follow-up | ~850 |
| `content/02-output-contract.xml` | essential | Slide-deck schema, decision-record schema, follow-up email schema, forbidden patterns | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes (data fishing, no-decision exit, advocacy spiral, anchored discount, surprise scope creep, missing follow-up) | ~850 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `slide_deck_first_draft` | sonnet | Bounded template fill from utilization data |
| `talking_points_draft` | sonnet | Per-segment bullet generation, low ambiguity |
| `decision_framework_synthesis` | opus | Cross-input judgment when data is mixed (high util + low NPS) |
| `follow_up_email_draft` | haiku | Template fill: decision + scope delta + next-quarter date |

## Templates

| File | Purpose |
|------|---------|
| `templates/qbr-deck.md` | 6-slide outline: cover / status / outcomes / blockers / renewal options / next quarter |
| `templates/qbr-talking-points.md` | Verbatim opening, transition, and closing lines for each segment |
| `templates/decision-record.json` | Renewal decision schema (continue / scale up / scope down / terminate) |
| `templates/follow-up-email.md` | 1-page recap email — sent within 24h of call |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/build-qbr-deck.py` | Pull utilization + SLA + deliverables → populate qbr-deck.md | 48h before QBR call |
| `scripts/validate-decision-record.py` | Verify decision-record.json has all required fields populated | Immediately after call |

## Related

- parent skill: `pro/pm/project-manager/`
- peer methodologies: `agency-pnl-tracker-template`, `account-health-scoring-model`, `cost-estimation`
- external: [Gainsight QBR Playbook](https://www.gainsight.com/guides/the-essential-guide-to-quarterly-business-reviews/) · [HBR - The Sales Conversation](https://hbr.org/2017/11/the-best-salespeople-know-when-to-stop-talking) · [ChartMogul renewal metrics](https://chartmogul.com/blog/saas-metrics/)
