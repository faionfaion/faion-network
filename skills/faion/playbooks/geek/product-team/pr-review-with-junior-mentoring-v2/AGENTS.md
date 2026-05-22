---
slug: pr-review-with-junior-mentoring-v2
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
summary: Senior + junior pair on a single PR review session. Senior narrates the why behind each comment; AI bot pre-runs the diff to surface obvious lint/security/test-coverage issues so the human time goe...
content_id: c5d09c312806bdd1
methodology_refs:
  - code-review
  - code-review-process
  - pair-programming
  - lint-autofix-vs-flag-decision-rule
  - lint-precommit-floor
  - lint-staged-only-not-whole-tree
  - mr-graph-vs-diff-reviewer
  - sec-codeql-autofix-on-pr
  - sec-secrets-defense-in-depth
  - code-review-cycle
  - mistake-memory
  - pattern-memory
  - quality-gates-confidence
  - reflexion-learning
---

# PR review with junior present (mentoring loop)

## Context

Senior + junior pair on a single PR review session. Senior narrates the why behind each comment; AI bot pre-runs the diff to surface obvious lint/security/test-coverage issues so the human time goes to design + judgment. Junior leaves with a concrete next-PR checklist.

## Outcome

By the end of this playbook, the operator has run the 4 stages below and produced the written decision artefact in the final stage.

Success criteria:

- All 4 stages have written outputs in the project record
- Each stage's decision gate was answered before advancing (yes / no in writing)
- Final stage produced the required written decision artifact
- Every methodology reference loaded cleanly via `faion get-content`

## Steps

### 1. Set Mentoring Intent

Review and teach at the same time.

Tasks:
- Pair the junior with a senior reviewer for the cycle
- Define the teach-list: 2-3 patterns to coach per PR
- Agree the review tone: rigor without bruising

Outputs:
- pair assignment
- teach-list per PR
- review-tone rules

Decision gate: Advance only when both reviewer and junior have signed on to the loop.

### 2. Review Together

Walk through the PR live.

Tasks:
- Junior presents the PR: intent, design, tradeoffs
- Senior asks questions before suggesting fixes
- Capture coaching notes inline in the PR thread

Outputs:
- PR walkthrough notes
- coaching comments
- fix list

Decision gate: Advance when junior can articulate the design decisions unaided.

### 3. Iterate & Merge

Junior owns the fixes; senior verifies.

Tasks:
- Junior addresses every comment with code + reasoning
- Senior verifies fix quality, not just code change
- Merge when bar is met

Outputs:
- iteration log
- merge decision
- merged PR

Decision gate: Advance only when merge bar is met.

### 4. Retro & Track

Mentoring needs a memory.

Tasks:
- Capture lessons in the junior's growth doc
- Tag patterns that need re-coaching in future PRs
- Decide next coaching focus

Outputs:
- growth-doc entry
- pattern-tag list
- next-focus memo

Decision gate: Required output: an updated junior growth doc per PR.

## Decision points

- Stage 1 (Set Mentoring Intent): Advance only when both reviewer and junior have signed on to the loop.
- Stage 2 (Review Together): Advance when junior can articulate the design decisions unaided.
- Stage 3 (Iterate & Merge): Advance only when merge bar is met.
- Stage 4 (Retro & Track): Required output: an updated junior growth doc per PR.

## References

- `code-review`
- `code-review-process`
- `pair-programming`
- `lint-autofix-vs-flag-decision-rule`
- `lint-precommit-floor`
- `lint-staged-only-not-whole-tree`
- `mr-graph-vs-diff-reviewer`
- `sec-codeql-autofix-on-pr`
- `sec-secrets-defense-in-depth`
- `code-review-cycle`
- `mistake-memory`
- `pattern-memory`
- `quality-gates-confidence`
- `reflexion-learning`

Gaps (status: draft until empty):
- `pr-mentoring-session-protocol` (see `gaps[]` in `playbook.yaml`)
- `junior-next-pr-checklist-template` (see `gaps[]` in `playbook.yaml`)
