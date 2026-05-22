---
slug: quarterly-okr-cascade-weekly-review-v2
tier: geek
group: product-team
persona: p6-product-dev-team
goal: TBD
complexity: medium
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "Company OKR -> team OKR -> personal OKR with weekly check-ins and a quarterly blameless retro. Output: every dev knows what their work ladders to"
content_id: 69856e331aea83cb
methodology_refs:
  - reporting-basics
  - okr-setting
---

# Quarterly OKR cascade, weekly review, post-quarter retro

## Context

Company OKR -> team OKR -> personal OKR with weekly check-ins and a quarterly blameless retro. Output: every dev knows what their work ladders to

## Outcome

By the end of this playbook, the operator has run the 4 stages below and produced the written decision artefact in the final stage.

Success criteria:

- All 4 stages have written outputs in the project record
- Each stage's decision gate was answered before advancing (yes / no in writing)
- Final stage produced the required written decision artifact
- Every methodology reference loaded cleanly via `faion get-content`

## Steps

### 1. Cascade

Translate company OKRs to team and individual.

Tasks:
- Team leads draft team OKRs aligned to company OKRs
- Each IC drafts personal commitments aligned to team OKRs
- Manager + IC align in 1:1

Outputs:
- team OKRs
- IC commitments
- alignment 1:1 notes

Decision gate: Advance only when every IC has commitments tied to a team OKR.

### 2. Weekly OKR Check-In

Lightweight; signal-based.

Tasks:
- Each team posts confidence (0.0-1.0) per KR weekly
- Manager spots dropping confidence and unblocks
- Track moving averages, not single weeks

Outputs:
- weekly confidence post
- unblock log
- trend chart

Decision gate: Advance only when 12 consecutive weekly posts exist by quarter end.

### 3. Mid-Quarter Adjustment

Course-correct, don't pretend.

Tasks:
- Mid-quarter, score every KR honestly
- Adjust scope where confidence is sustained <0.3
- Communicate adjustments to the company

Outputs:
- mid-quarter score
- scope adjustments
- company-comms post

Decision gate: Advance only when adjustments are written down.

### 4. Quarter Retro

Score, learn, reset.

Tasks:
- Final score per KR with evidence
- Retro on what dragged outcomes
- Feed insights into next quarter's planning

Outputs:
- final KR scores
- retro doc
- input deck for next planning

Decision gate: Required output: a published retro doc fed into next planning.

## Decision points

- Stage 1 (Cascade): Advance only when every IC has commitments tied to a team OKR.
- Stage 2 (Weekly OKR Check-In): Advance only when 12 consecutive weekly posts exist by quarter end.
- Stage 3 (Mid-Quarter Adjustment): Advance only when adjustments are written down.
- Stage 4 (Quarter Retro): Required output: a published retro doc fed into next planning.

## References

- `reporting-basics`
- `okr-setting`

Gaps (status: draft until empty):
- `okr-cascade-multi-level` (see `gaps[]` in `playbook.yaml`)
- `personal-okr-1on1-template` (see `gaps[]` in `playbook.yaml`)
- `okr-weekly-check-in-template` (see `gaps[]` in `playbook.yaml`)
- `mid-quarter-pivot-gate` (see `gaps[]` in `playbook.yaml`)
- `blameless-retrospective-facilitation` (see `gaps[]` in `playbook.yaml`)
- `okr-carry-over-rules` (see `gaps[]` in `playbook.yaml`)
