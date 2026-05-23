---
slug: solo-content-calendar-template
tier: solo
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Produces a 12-row content-calendar spec — one shippable asset per week pinned to a ranked ICP pain — with a Friday-draft cadence gate and quarterly retirement of stale rows."
content_id: "b8c8ad778492f598"
complexity: light
produces: spec
est_tokens: 3000
tags: [content, calendar, solo, cadence, icp]
---

# Solo Content Calendar Template

## Summary

**One-sentence:** Produces a 12-row content-calendar spec — one shippable asset per week pinned to a ranked ICP pain — with a Friday-draft cadence gate and quarterly retirement of stale rows.

**Ефективно для:** Solo operators where content cadence drifts because there's no aim — needs the discipline of one row per week, one bet, one channel.

**One-paragraph:** Existing content-calendar playbooks describe how a team plans a quarter. Solo founders need a stripped-down version: one row per week, one asset per row, pinned to a specific ICP pain. The template defines required columns, a forcing rule that next week's row must be drafted by Friday or this week's writing block becomes backfill, and a quarterly review that retires assets whose pain reference is no longer in the top-5 ICP problems.

## Applies If (ALL must hold)

- Solo founder with a documented ICP (or willing to commit to one within 1 week).
- Content is a chosen growth channel (SEO/build-in-public/newsletter/social).
- Founder commits one writing block per week.
- An ICP pain-ladder document exists (or icp-fit-scorecard-solo loaded).

## Skip If (ANY kills it)

- Pre-ICP — define the ICP first; cadence without aim wastes content.
- Content is not a growth channel (paid-only acquisition).
- Founder cannot commit a recurring weekly block — calendar will die.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| ICP pain ladder (top-5 ranked pains) | markdown | internal research bank |
| chosen primary channel | enum | founder decision |
| weekly writing block (calendar hold) | calendar block | self-managed |
| 12-week horizon decision | boolean | founder decision |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/marketing/icp-fit-scorecard-solo` | Source of pain ladder. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations + JSON schema | ~800 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `seed_12_row_calendar` | sonnet | Per-instance row planning. |
| `score_pain_alignment` | haiku | Bounded scoring on top-5 pains. |
| `review_quarterly_retire` | opus | Cross-quarter retirement decisions. |

## Templates

| File | Purpose |
|---|---|
| `templates/solo-content-calendar-template.json` | JSON Schema for the output contract. |
| `templates/solo-content-calendar-template.md` | Markdown skeleton with the required fields. |
| `templates/_smoke-test.json` | Minimum viable filled-in example (passes the validator). |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-solo-content-calendar-template.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[icp-fit-scorecard-solo]] — pain-ladder source.
- [[swipe-file-tweet-hooks]] — atomic hook reuse.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).
