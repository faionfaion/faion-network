---
slug: daily-sdd-spec-vibe-code-review-cycle
tier: solo
group: solo-saas
persona: P1
goal: TBD
complexity: medium
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "One feature slice shipped to staging in a single focused day: spec written, code generated against acceptance, self-review pass complete, PR merged, deploy verified."
content_id: 25265efa5eb69f22
methodology_refs:
  - code-review
  - impl-plan-100k-rule
  - writing-specifications
  - code-review-process
  - impl-plan-task-format
  - error-handling
  - spec-requirements
  - tdd-workflow
  - api-first-development
  - unit-testing
  - code-review-cycle
  - cd-basics
  - quality-gates-confidence
---

# Daily SDD spec → vibe-code → review cycle

## Intent

One feature slice shipped to staging in a single focused day: spec written, code generated against acceptance, self-review pass complete, PR merged, deploy verified.

## Scope

One feature slice shipped to staging in a single focused day: spec written, code generated against acceptance, self-review pass complete, PR merged, deploy verified.

## Stages

### 1. Spec the slice

Write the spec before touching code.

Tasks:
- Write a tight one-feature spec with acceptance criteria
- List explicit non-goals for this slice
- Identify the smallest staging-deployable unit

Outputs:
- slice-spec.md
- Non-goals list
- Acceptance criteria table

Decision gate: Advance only when spec fits one screen AND every AC is testable.

### 2. Generate against acceptance

Use the AI agent with the spec as the brief, not vibes.

Tasks:
- Feed the spec + relevant context to the coding agent
- Constrain the diff size to one logical change
- Ask for tests against the acceptance criteria first

Outputs:
- Generated diff
- Generated tests
- Agent transcript log

Decision gate: Advance only when diff is reviewable in <=10 minutes and tests cover all AC.

### 3. Self-code review

Solo PR review using a written rubric, not gut.

Tasks:
- Walk the self-code-review rubric line by line
- Tag any debt deferral explicitly
- Re-run lint, types, and the relevant test scope

Outputs:
- Review checklist filled
- Debt-deferral notes
- Green CI on the branch

Decision gate: Advance only when all rubric items are green or explicitly deferred with a ticket.

### 4. Ship to staging

Push the slice behind a flag where risky.

Tasks:
- Deploy to staging with the feature flag default-off
- Run the staging smoke checks
- Verify the AC manually against staging

Outputs:
- Staging deploy URL
- Smoke check log
- AC verification notes

Decision gate: Advance only when all AC pass on staging.

### 5. Merge + production gate

Merge with a clear deploy decision.

Tasks:
- Squash-merge to main with a tight commit message
- Decide flag rollout strategy (canary / all-users / off)
- Trigger production deploy

Outputs:
- Merged PR
- Deploy decision note
- Production health snapshot

Decision gate: Advance only when production health is green for 15 minutes post-deploy.

### 6. Daily-ship rubric

Close the day with a one-line ship verdict.

Tasks:
- Score the day against the daily-ship rubric
- Log what slipped or got cut
- Pick tomorrows first slice while context is hot

Outputs:
- Daily ship score
- Slip log
- Tomorrows first-slice brief

Decision gate: Cycle closes when daily score is written and the next slice is named.

## Common pitfalls

- Skipping the decision-gate write-up to keep moving - closes the loop with vibes, not evidence.
- Treating each stages outputs as optional - every output is a gate input for the next stage.
- Letting one bad week stretch a fixed-cadence ritual into a quarterly one.

## Quality checklist

- Every stage has at least one referenced methodology that resolves under `knowledge/`.
- Every output is a real artefact, not a feeling.
- The final decision is a written commitment, not we will see.
