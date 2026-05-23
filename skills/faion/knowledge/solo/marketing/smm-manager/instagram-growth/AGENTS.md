---
slug: instagram-growth
tier: solo
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Generates a Reels-first IG growth playbook-step (1-2 Reels/day + daily Stories + 30-min DM-funnel engagement) with a DM trigger that converts visits to qualified leads."
content_id: "614049a97a9066fa"
complexity: medium
produces: playbook-step
est_tokens: 4200
tags: [instagram, reels, growth, dm-funnel, social-media]
---

# Instagram Growth

## Summary

**One-sentence:** Generates a Reels-first IG growth playbook-step (1-2 Reels/day + daily Stories + 30-min DM-funnel engagement) with a DM trigger that converts visits to qualified leads.

**Ефективно для:** Solo creators using IG for audience-to-pipeline conversion (not branding), where Reels output is sporadic and Stories are skipped, and DMs are not yet a funnel stage.

**One-paragraph:** IG growth in 2026 is Reels-anchored. This methodology produces a daily playbook-step: 1-2 Reels per day on a single content pillar, daily Stories driving DM CTAs, 30 minutes of focused engagement, and a DM trigger phrase converting profile visits to qualified leads. Output is a 4-week content batch + DM trigger script consumed by the operator's scheduler.

## Applies If (ALL must hold)

- Operator can shoot/edit ≥1 Reel/day for 90 days.
- A single content pillar (one niche, one ICP) is decided.
- DM-funnel is a goal (lead capture, not pure brand).
- Operator runs the account personally (not via agency).

## Skip If (ANY kills it)

- B2B sale where decision-makers are not on IG — pick LinkedIn.
- Niche regulated against direct outreach (e.g., medical/legal advice).
- Operator cannot show face / voice on Reels — the format requires presence.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| content pillar (one niche + one ICP) | string | founder decision |
| 4-week Reel script batch (≥28 scripts) | batch | internal generator |
| DM trigger phrase + lead-magnet asset | string + file | lead-magnet library |
| daily 30-min engagement slot | calendar block | self-managed |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/marketing/smm-manager/growth-social-media-strategy` | PACE umbrella. |
| `solo/marketing/smm-manager/threads-growth` | Adjacent Meta-platform. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations + JSON schema | ~800 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs/actions/outputs | ~700 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `batch_reel_scripts` | sonnet | 28 hook+payoff scripts on one pillar. |
| `score_dm_lead_quality` | haiku | Bounded scoring on DM thread. |
| `review_pillar_drift` | opus | Cross-week pillar-consistency audit. |

## Templates

| File | Purpose |
|---|---|
| `templates/instagram-growth.json` | JSON Schema for the output contract. |
| `templates/instagram-growth.md` | Markdown skeleton with the required fields. |
| `templates/_smoke-test.json` | Minimum viable filled-in example (passes the validator). |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-instagram-growth.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[growth-social-media-strategy]] — PACE umbrella.
- [[threads-growth]] — adjacent Meta-platform discipline.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).
