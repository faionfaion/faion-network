# Nomad Async Ops Stack

## Summary

**One-sentence:** Generates a nomad-ops spec — offline-tolerant editor stack, timezone-aware payment ops schedule, async customer-support SLA — so a digital-nomad solo founder operates from flaky wifi without dropped balls.

**One-paragraph:** Generates a nomad-ops spec — offline-tolerant editor stack, timezone-aware payment ops schedule, async customer-support SLA — so a digital-nomad solo founder operates from flaky wifi without dropped balls.

**Ефективно для:**

- Solo founder on Bali / Mexico City / Lisbon wifi.
- Indie hacker rotating across N small bets while traveling.
- Customer-support SLA across 12h timezone delta.

## Applies If (ALL must hold)

- Operator works async ≥80% of the week.
- Internet uptime is <99% (frequent disconnects expected).
- Operator crosses ≥3 timezones / quarter.
- Customer base spans ≥2 timezones (≥6h apart).

## Skip If (ANY kills it)

- Operator is desk-bound with stable wifi — overhead exceeds value.
- Team has ≥2 people who can cover gaps — standard on-call applies.
- Greenfield prototype with no customers.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Operator timezone schedule | yaml | calendar with TZ annotations |
| Customer timezone distribution | json | support ticket TZ histogram |
| Editor + sync tool inventory | list | iA Writer / Obsidian / git |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| solo-deploy-checklist | Deploy ritual under flaky wifi. |
| sentry-alert-routing-for-solos | Alert routing in operator-local quiet hours. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-offline-first-editor, r2-tz-aware-payment-windows, r3-support-sla-async, r4-named-owner, r5-version-and-review | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the Nomad Async Ops Stack artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: cloud-only-editor, missed-payment-window, over-promised-sla | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure for end-to-end application | 800 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Maps observable inputs to rule ids in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-nomad-async-ops-stack` | opus | High-stakes synthesis — sets the artefact baseline. |
| `validate-nomad-async-ops-stack` | sonnet | Bounded structural check against the output contract. |
| `review-nomad-async-ops-stack` | sonnet | Per-section critique against rules + failure modes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/nomad-async-ops-stack.json` | JSON skeleton matching the output contract. |
| `templates/nomad-async-ops-stack.md` | Markdown skeleton with required fields. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-nomad-async-ops-stack.py` | Validate Nomad Async Ops Stack output JSON against the schema. | After subagent returns, before downstream consumer reads. |

## Related

- [[solo-deploy-checklist]]
- [[sentry-alert-routing-for-solos]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input fields to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, the verdict label, and which template variant to fill.
