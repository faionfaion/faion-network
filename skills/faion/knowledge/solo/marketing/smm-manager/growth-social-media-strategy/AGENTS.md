---
slug: growth-social-media-strategy
tier: solo
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Produces a PACE strategy spec (Platform → Audience → Content → Engagement) that picks ≤2 primary platforms and locks one weekly atomization loop for a solo operator."
content_id: "3f695d18e318a26c"
complexity: medium
produces: spec
est_tokens: 4600
tags: [social-media, strategy, PACE, calendar, audience]
---

# Growth Social Media Strategy

## Summary

**One-sentence:** Produces a PACE strategy spec (Platform → Audience → Content → Engagement) that picks ≤2 primary platforms and locks one weekly atomization loop for a solo operator.

**Ефективно для:** Solo operators spread across five platforms with zero compounding traction — needs the discipline pivot from 'be everywhere' to 'one atomization loop'.

**One-paragraph:** Solo operators lose traction by trying to be everywhere. The PACE spec forces ≤2 primary platforms picked on Audience + Time-fit criteria, a weekly atomization loop (one long-form → 5 shorter cuts), and an engagement quota that scales with the size of the audience. Output is a 12-week strategy spec consumed by the content calendar + scheduler.

## Applies If (ALL must hold)

- Solo operator runs all content alone (no team).
- Operator has audience-growth or pipeline goals (not vanity reach).
- Operator can produce one long-form piece per week as the atomization seed.

## Skip If (ANY kills it)

- Operator has no clear ICP yet — pick ICP first, strategy after.
- Operator wants daily output on 4+ platforms — that's a content-team brief, not solo.
- Goal is paid-ads acquisition only — switch to paid-acquisition methodology.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| ICP definition (segment + pain + buying trigger) | single page | internal positioning doc |
| audience-fit matrix per platform candidate | scoring sheet | internal research |
| weekly time budget (hours) | integer | self-managed |
| long-form seed (blog / podcast / video) chosen | string | founder decision |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/marketing/smm-manager/growth-linkedin-strategy` | Single-platform branch when LinkedIn chosen. |
| `solo/marketing/smm-manager/growth-twitter-x-growth` | Single-platform branch when X chosen. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations + JSON schema | ~800 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs/actions/outputs | ~700 |
| `content/05-examples.xml` | essential | One worked end-to-end example | ~600 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `score_platforms_for_icp` | sonnet | Per-instance judgement on fit. |
| `draft_atomization_plan` | sonnet | Long-form → 5-cut decomposition. |
| `review_for_burnout_risk` | opus | Cross-cutting capacity check. |

## Templates

| File | Purpose |
|---|---|
| `templates/growth-social-media-strategy.json` | JSON Schema for the output contract. |
| `templates/growth-social-media-strategy.md` | Markdown skeleton with the required fields. |
| `templates/_smoke-test.json` | Minimum viable filled-in example (passes the validator). |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-growth-social-media-strategy.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[growth-linkedin-strategy]] — LinkedIn-only branch.
- [[growth-twitter-x-growth]] — X-only branch.
- [[solo-content-calendar-template]] — downstream calendar.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).
