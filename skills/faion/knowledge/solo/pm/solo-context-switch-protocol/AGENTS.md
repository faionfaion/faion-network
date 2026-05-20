---
slug: solo-context-switch-protocol
tier: solo
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
content_id: "bc0cc0ce638a48aa"
summary: Opinionated mode-batching protocol for the solo founder day — separates building from inbox/support/ops to cut context-switch cost from hours to minutes.
---
# Solo Context Switch Protocol

## Summary

**One-sentence:** A daily mode-batching protocol — Builder block, Operator block, Inbox block — with hard transitions and a one-page handoff note that compresses the context-switch tax to a few minutes.

**One-paragraph:** Weekly-review-solo handles the strategic cadence. Nothing in faion covers the in-day mode-switching cost, which is the single biggest solo-founder productivity leak. This methodology defines three named modes, the order in which they run, a 5-minute end-of-mode handoff note (what was open, what is next, what the next mode must remember), and a hard rule that no Slack/email/Stripe-alert checking happens inside a Builder block. The protocol is fixed; only the time blocks are configurable. Anchored to "Solo founder operating system (weekly cadence + focus discipline)" — the pain Alex (canonical persona) stated as primary.

## Applies If (ALL must hold)

- Solo founder splitting the day across building, customer support, and ops/admin.
- A calendar exists and the founder can hold 90-minute blocks.
- Notifications can be silenced at OS level (do-not-disturb, focus, etc.).
- Founder is willing to commit to the protocol for at least 2 weeks before tuning.

## Skip If (ANY kills it)

- Live incident or P0 outage — the protocol is for normal days; incidents preempt it.
- Pre-product, no users, no inbox — only one mode is needed (Builder); the protocol is overkill.
- Operating across multiple time zones with hard-scheduled customer calls all day — block-based mode batching is incompatible with calendar-driven day; use a different operating model.

## Prerequisites

- Calendar with the ability to recur multi-block templates.
- OS-level focus / do-not-disturb capability.
- A handoff-note template (in a notes app or markdown file).

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/pm/AGENTS.md` | Parent group context |
| `solo/pm/burndown-diagnosis-cheatsheet` if present | Sibling — diagnoses when the protocol fails |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules every day's blocks enforce | ~900 |

## Related

- parent skill: `solo/pm/`
- triggering activity: `p1-solo-saas-builder/Solo founder operating system (weekly cadence + focus discipline)`
- adjacent: `solo/sdd/daily-ship-rubric`, `solo/pm/burnout-tripwires`
