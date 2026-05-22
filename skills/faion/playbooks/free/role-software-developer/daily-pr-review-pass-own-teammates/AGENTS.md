---
slug: daily-pr-review-pass-own-teammates
tier: free
group: role-software-developer
persona: software developer
goal: TBD
complexity: light
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "Inbox-zero on review queue: every assigned PR has either an approve, a concrete change request, or a documented block. Own PRs are rebased, CI-green, and re-requested."
content_id: 8e9ccdeec6870224
methodology_refs:
  - code-review-basics
  - code-review-process
  - code-coverage
  - code-review
  - documentation
  - error-handling
  - trunk-based-ci-gates
  - tech-debt-management
---

# Daily PR review pass (own + teammates)

**Persona:** software developer · **Tier:** free · **Complexity:** light · **Angle:** atomic

## Context

Inbox-zero on review queue: every assigned PR has either an approve, a concrete change request, or a documented block. Own PRs are rebased, CI-green, and re-requested.

This is a atomic-angle playbook. Light complexity — expect the work to span multiple sessions if light = deep, a focused interval if medium, and a single sitting if light. The persona is a software developer operating in a solo, team context.

## Outcome

Success is defined by these criteria, all attached as written artifacts before the playbook is considered closed:

- Daily PR review pass (own + teammates) ships with written success criteria met and evidence attached
- Baseline → post-change metric delta recorded against the relevant quality attribute
- Rollback path rehearsed at least once and documented in the runbook
- Decision doc (continue / iterate / revert) signed off by named owner

## Steps

Walk the stages in order. Do not advance until each stage's decision gate is met in writing.

### Step 1 — Frame

**Intent.** Name the problem in writing and set explicit success criteria.

**Tasks**
- Write a one-paragraph problem statement tied to a quality attribute or user outcome
- List concrete success criteria (measurable, observable, time-bounded)
- Identify the smallest credible scope that still moves the needle

**Outputs**
- Problem brief
- Success-criteria list
- Scope boundary

**Backed by methodology**
- `free/dev/code-quality/code-review-basics` (tier: free)
- `free/dev/software-developer/error-handling` (tier: free)

### Step 2 — Plan

**Intent.** Decompose into a sequenced backlog with explicit decision points.

**Tasks**
- Break the work into tasks of ≤1 day each, with dependencies named
- Mark reversible vs irreversible (one-way-door) decisions
- Define rollback / kill conditions for each major step

**Outputs**
- Task plan
- Decision log skeleton
- Rollback playbook

**Backed by methodology**
- `free/dev/code-quality/code-review-process` (tier: free)
- `solo/dev/automation-tooling/trunk-based-ci-gates` (tier: solo)

### Step 3 — Execute

**Intent.** Ship the change behind safe deployment controls.

**Tasks**
- Implement the plan in small, individually shippable steps
- Keep all changes behind feature flags or branch-by-abstraction where reversible
- Update tests + docs in the same change set, never as a follow-up

**Outputs**
- Shipped change set
- Updated tests + docs

**Backed by methodology**
- `free/dev/software-developer/code-coverage` (tier: free)
- `solo/dev/code-quality/tech-debt-management` (tier: solo)

### Step 4 — Verify

**Intent.** Prove the change cleared the success criteria with evidence.

**Tasks**
- Run targeted tests + smoke on the most-trafficked surfaces
- Compare post-change metrics against the baseline captured earlier
- Capture user / operator feedback within the first 48 hours

**Outputs**
- Verification report
- Metric delta vs baseline

**Backed by methodology**
- `free/dev/software-developer/code-review` (tier: free)

### Step 5 — Close

**Intent.** Lock in the gain: documentation, learnings, and a single decision artifact.

**Tasks**
- Write the decision / outcome doc (continue / iterate / revert) with evidence trail
- Update ADRs, runbooks, and pattern memory with what changed
- Schedule the next review checkpoint or archive the workstream

**Outputs**
- Decision doc
- Updated ADR / runbook / memory entry

**Backed by methodology**
- `free/dev/software-developer/documentation` (tier: free)

## Decision points

- **After Step 1 (Frame).** Advance only after a peer can restate the problem in their own words and agree the criteria are testable.
- **After Step 2 (Plan).** Advance only when every task has a definition-of-done and the plan fits on one page.
- **After Step 3 (Execute).** Advance only when CI is green, the change is observable in staging, and rollback was rehearsed at least once.
- **After Step 4 (Verify).** Advance only when metrics meet the criteria and no regression alerts are open.
- **After Step 5 (Close).** Done when the decision doc is single-link shareable and the team can name the next checkpoint.

If any gate fails: stop, re-plan, and either re-enter the previous step or kill the workstream with a written rationale.

## References

Methodologies cited in this playbook (resolve via `faion get-content <slug>`):

- `code-review-basics` — `faion/knowledge/free/dev/code-quality/code-review-basics` (tier: free)
- `code-review-process` — `faion/knowledge/free/dev/code-quality/code-review-process` (tier: free)
- `code-coverage` — `faion/knowledge/free/dev/software-developer/code-coverage` (tier: free)
- `code-review` — `faion/knowledge/free/dev/software-developer/code-review` (tier: free)
- `documentation` — `faion/knowledge/free/dev/software-developer/documentation` (tier: free)
- `error-handling` — `faion/knowledge/free/dev/software-developer/error-handling` (tier: free)
- `trunk-based-ci-gates` — `faion/knowledge/solo/dev/automation-tooling/trunk-based-ci-gates` (tier: solo)
- `tech-debt-management` — `faion/knowledge/solo/dev/code-quality/tech-debt-management` (tier: solo)

Gaps — methodologies referenced as future work, blocking promotion from `draft` to `published`:

- `pr-review-rubric-by-blast-radius` (expected tier: free)
- `ai-generated-code-review-checklist` (expected tier: free)
