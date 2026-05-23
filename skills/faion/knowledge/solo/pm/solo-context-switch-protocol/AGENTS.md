---
slug: solo-context-switch-protocol
tier: solo
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
content_id: "bc0cc0ce638a48aa"
summary: Daily Builder/Operator/Inbox mode-batching protocol with silenced notifications, 5-min handoff notes, and a weekly review that turns repeat violations into structural fixes.
complexity: light
produces: checklist
est_tokens: 3300
tags: [focus, solo, mode-batching, deep-work]
---
# Solo Context Switch Protocol

## Summary

**One-sentence:** A daily mode-batching protocol — Builder block, Operator block, Inbox block — with hard transitions and a one-page handoff note that compresses the context-switch tax to a few minutes.

**One-paragraph:** Weekly-review methodologies handle the strategic cadence. Nothing covers the in-day mode-switching cost, which is the single biggest solo-founder productivity leak. This methodology defines three named modes, the order in which they run, a 5-minute end-of-mode handoff note, and a hard rule that no Slack/email/Stripe-alert checking happens inside a Builder block. The protocol is fixed; only time-block windows are configurable.

**Ефективно для:**

- Solo founder splitting the day across building, customer support, and ops/admin.
- Day pattern that currently looks like "Twitter → email → tried to code → Slack".
- Calibrating Operator block length when repeat "urgent" interruptions break Builder time.
- Replacing willpower-based focus with system-based focus.

## Applies If (ALL must hold)

- Solo founder splitting the day across building, customer support, and ops/admin.
- A calendar exists and the founder can hold 90-minute blocks.
- Notifications can be silenced at OS level (do-not-disturb, focus, etc.).
- Founder is willing to commit to the protocol for at least 2 weeks before tuning.

## Skip If (ANY kills it)

- Live incident or P0 outage — the protocol is for normal days; incidents preempt it.
- Pre-product, no users, no inbox — only one mode is needed (Builder).
- Operating across multiple time zones with hard-scheduled customer calls all day — calendar-driven day; use a different operating model.
- Founder unwilling to silence notifications — the protocol fails by definition.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Calendar with recurring multi-block templates | calendar | founder |
| OS-level focus / do-not-disturb capability | OS | founder |
| Handoff-note template (notes app or markdown file) | template | founder |
| Documented incident-override list (P0 outage, charge dispute, security) | doc | founder |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[solo-burnout-tripwires]] | Weekly review of block violations feeds the broader burnout signal. |
| [[solo-time-tracking-discipline]] | Capture-at-boundary aligns with mode boundary; same hour boundaries. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: mode order, notification silence, handoff note, urgency override, weekly violations review | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for daily block log + valid/invalid examples + forbidden patterns | ~700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns: inbox-first, no-handoff, urgency-override-creep | ~600 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `handoff_note_compose` | haiku | Mechanical 3-question fill. |
| `weekly_violations_summary` | sonnet | Per-week pattern analysis (structural-fix vs willpower). |

## Templates

| File | Purpose |
|------|---------|
| `templates/daily-blocks.yaml` | Daily block schedule skeleton |
| `templates/handoff-note.md` | 5-minute handoff template |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-solo-context-switch-protocol.py` | Validate daily block log against 02-output-contract schema | End of day |

## Related

- [[solo-burnout-tripwires]]
- [[solo-time-tracking-discipline]]
- [[solo-rate-floor-calculator]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes by mode order, notification silence, handoff-note completeness, and weekly violation count onto a rule from `content/01-core-rules.xml`. Walk it at end of day for review and end of week for structural action.
