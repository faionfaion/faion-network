---
slug: accessibility-audit-on-one-screen
tier: solo
group: role-software-developer
persona: software developer
goal: TBD
complexity: light
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: One critical screen passes axe / Lighthouse a11y, keyboard-only test, and screen-reader spot-check. Issues found are either fixed or ticketed with severity.
content_id: af249d652c2015c5
methodology_refs:
  - e2e-testing
  - storybook-setup
  - accessibility
---

# Accessibility audit on one screen

**Persona:** software developer · **Tier:** solo · **Complexity:** light · **Angle:** atomic

## Context

One critical screen passes axe / Lighthouse a11y, keyboard-only test, and screen-reader spot-check. Issues found are either fixed or ticketed with severity.

This is a atomic-angle playbook. Light complexity — expect the work to span multiple sessions if light = deep, a focused interval if medium, and a single sitting if light. The persona is a software developer operating in a solo, team context.

## Outcome

Success is defined by these criteria, all attached as written artifacts before the playbook is considered closed:

- Accessibility audit on one screen ships with written success criteria met and evidence attached
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
- `free/dev/software-developer/e2e-testing` (tier: free)

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
- `free/dev/software-developer/storybook-setup` (tier: free)

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
- `solo/dev/frontend-developer/accessibility` (tier: solo)

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
- `solo/dev/frontend-developer/storybook-setup` (tier: solo)

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
- `solo/dev/software-developer/accessibility` (tier: solo)

## Decision points

- **After Step 1 (Frame).** Advance only after a peer can restate the problem in their own words and agree the criteria are testable.
- **After Step 2 (Plan).** Advance only when every task has a definition-of-done and the plan fits on one page.
- **After Step 3 (Execute).** Advance only when CI is green, the change is observable in staging, and rollback was rehearsed at least once.
- **After Step 4 (Verify).** Advance only when metrics meet the criteria and no regression alerts are open.
- **After Step 5 (Close).** Done when the decision doc is single-link shareable and the team can name the next checkpoint.

If any gate fails: stop, re-plan, and either re-enter the previous step or kill the workstream with a written rationale.

## References

Methodologies cited in this playbook (resolve via `faion get-content <slug>`):

- `e2e-testing` — `faion/knowledge/free/dev/software-developer/e2e-testing` (tier: free)
- `storybook-setup` — `faion/knowledge/free/dev/software-developer/storybook-setup` (tier: free)
- `accessibility` — `faion/knowledge/solo/dev/frontend-developer/accessibility` (tier: solo)
- `storybook-setup` — `faion/knowledge/solo/dev/frontend-developer/storybook-setup` (tier: solo)
- `accessibility` — `faion/knowledge/solo/dev/software-developer/accessibility` (tier: solo)

Gaps — methodologies referenced as future work, blocking promotion from `draft` to `published`:

- `a11y-audit-per-screen-checklist` (expected tier: solo)
- `wcag-severity-rubric` (expected tier: solo)
