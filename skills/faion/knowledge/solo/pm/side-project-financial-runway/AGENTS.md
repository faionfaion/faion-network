---
slug: side-project-financial-runway
tier: solo
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Personal-runway math for the day-job-plus-side-project indie hacker — realistic burn, 12-month leave-job trigger, geo-arbitrage scenario, stress-tested for flat / declining MRR, quarterly revisit.
content_id: "0f3f9027f25ab50b"
complexity: medium
produces: report
est_tokens: 4400
tags: [side-project-financial-runway, pm, solo]
---

# Side-Project Financial Runway

## Summary

**One-sentence:** Personal-runway model for the indie hacker working a day job: explicit burn (incl. taxes, health, savings), 12-month leave-job trigger gated by MRR / burn ratio, geo-arbitrage scenario, and stress tests for flat / -20% MRR.

**One-paragraph:** Pricing methodologies cover product economics; this one covers the indie hacker's *life* economics. Naive runway models exclude taxes, health insurance, and savings, then propose leave-job moves on 6 months of "burn coverage" that doesn't exist. This methodology requires all-category burn, a 12-month minimum runway combined with MRR ≥ 30% of burn AND positive 3-month growth before the trigger fires, an alternative geo-arbitrage scenario (Lisbon / Mexico City / Chiang Mai), and stress tests for the case where MRR plateaus. Output: a runway model artefact + a leave-job decision verdict + a quarterly review pointer.

**Ефективно для:**

- Indie hacker working a day job while building side SaaS.
- Quarterly review when burn, MRR, or savings change materially.
- Pre-leave-job decision check before pulling the trigger.
- Modelling the geo-arbitrage path before committing to a relocation.

## Applies If (ALL must hold)

- Indie hacker working a day job while building a side SaaS.
- Ambition to go full-time on the side product.
- Personal + business finances are realistic, not aspirational.
- Quarterly review block exists on the calendar.

## Skip If (ANY kills it)

- Founder already full-time on the product — different rubric (full-time runway).
- Side-project is a hobby with no income goal.
- Founder has VC + unlimited runway (different math).
- Founder cannot honestly enumerate burn — defer until inputs exist.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Monthly personal expenses (all categories) | sheet | operator |
| Monthly business expenses | sheet | operator |
| Savings buffer + emergency fund | sheet | operator |
| Current MRR + 6-month trend | dashboard | operator |
| Jurisdictional tax + benefit assumptions | ADR | tax advisor |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[solo-rate-floor-calculator]] | If still doing freelance income, the floor feeds runway. |
| [[solo-mrr-dashboard-template]] | MRR input comes from the canonical MRR dashboard. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: realistic burn, 12-month + 30% MRR trigger, geo-arbitrage scenario, stress test, quarterly revisit | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for runway model + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 5 modes: too-early leave, missing health, no stress test, geo-arbitrage off table, quarterly skip | ~900 |
| `content/04-procedure.xml` | essential | 5-step procedure: collect → compute → scenarios → trigger evaluation → quarterly diary | ~800 |
| `content/05-examples.xml` | essential | Worked example: $9k/mo burn, $3k MRR, 18mo savings | ~800 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `inputs_summary` | haiku | Template fill from operator-provided figures. |
| `synthesize_decision` | sonnet | Per-instance judgement; bounded inputs. |
| `compliance_review` | opus | Cross-input synthesis when stakes are high (actual quit). |

## Templates

| File | Purpose |
|------|---------|
| `templates/runway-model.json` | Runway model skeleton |
| `templates/burn-checklist.md` | All-categories burn checklist |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-side-project-financial-runway.py` | Validate runway artefact against 02-output-contract schema | Quarterly review + before any leave-job decision |

## Related

- [[solo-rate-floor-calculator]]
- [[solo-mrr-dashboard-template]]
- [[solo-burnout-tripwires]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes by runway months, MRR / burn ratio, MRR growth, geo-arbitrage scenario presence, and stress-test presence onto a rule from `content/01-core-rules.xml`. Walk it before any quit-day-job conversation.
