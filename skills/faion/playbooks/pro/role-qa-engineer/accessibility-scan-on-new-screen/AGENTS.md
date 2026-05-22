---
slug: accessibility-scan-on-new-screen
tier: pro
group: role-qa-engineer
persona: QA engineer / test lead in an indie or small-team product context.
goal: TBD
complexity: light
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: Accessibility scan on new screen. Catch the must-fix WCAG 2.2 violations on a new UI before it ships; do not pretend the automated scan is the full story.
content_id: ee5945f6f0183326
methodology_refs:
  - a11y-testing
  - regulatory-compliance-2026
  - testing-with-assistive-technology
  - wcag-22-compliance
---

# Accessibility scan on new screen

## Context

Catch the must-fix WCAG 2.2 violations on a new UI before it ships; do not pretend the automated scan is the full story.

## Outcome

By the time this playbook closes:

- Done-state achieved as described in the scope: Catch the must-fix WCAG 2.
- Decision doc signed: continue / iterate / kill, backed by evidence.
- Runbook + acceptance criteria in source control, handed to on-call / next owner.
- All must-fix issues from Harden / Pilot closed; nice-to-fix backlog ticketed.

## Steps

### 1. Audit

Get an honest map of where things stand today for: Accessibility scan on new screen.

Tasks:
- Inventory current state, owners, and recent incidents
- Identify the top 3 risks that block the desired outcome
- Surface unknowns and missing telemetry up front

Methodologies:
- `pro/ux/accessibility-specialist/a11y-testing`

Outputs:
- Written current-state map (1 page)
- Top-3 risk list with owners

### 2. Plan

Convert audit findings into a defensible execution plan with explicit cuts.

Tasks:
- Define done-state acceptance criteria
- Sequence the smallest set of changes that ship the outcome
- Cut everything that does not block the done state

Methodologies:
- `pro/ux/accessibility-specialist/regulatory-compliance-2026`

Outputs:
- 1-page plan with sequenced steps
- Non-goals list (what we are NOT doing)

### 3. Build

Land the first vertical slice end-to-end in a real environment.

Tasks:
- Implement the slice behind a flag or in a sandbox
- Wire telemetry from day one
- Get a real human (not just CI) to use it

Methodologies:
- `pro/ux/accessibility-specialist/testing-with-assistive-technology`

Outputs:
- Working slice in a non-prod environment
- Telemetry dashboard for the slice

### 4. Harden

Find the failure modes before users do.

Tasks:
- Run failure-mode tests against the slice (load, edge cases, abuse)
- Close every must-fix; ticket every nice-to-fix
- Re-run telemetry to confirm no regression

Methodologies:
- `pro/ux/accessibility-specialist/wcag-22-compliance`

Outputs:
- Failure-mode report + closure log
- Ticketed nice-to-fix backlog

### 5. Pilot

Run with a controlled blast radius before broad rollout.

Tasks:
- Roll out to a controlled subset (canary, beta team, single client)
- Measure against acceptance criteria with real traffic / real work
- Capture rollback signal in writing

Outputs:
- Pilot metrics vs. acceptance criteria
- Rollback decision criteria in writing

## Decision points

- **Audit** → Advance only if all top-3 risks have a named owner; otherwise re-scope.
- **Plan** → Advance if every plan item maps to an acceptance criterion; rewrite the plan otherwise.
- **Build** → Advance when the slice runs end-to-end with one real user; loop on Build otherwise.
- **Harden** → Advance only with zero open must-fixes; otherwise stay in Harden.
- **Pilot** → Advance if pilot meets all acceptance criteria; pause for fix or revert otherwise.

## References

- `pro/ux/accessibility-specialist/a11y-testing`
- `pro/ux/accessibility-specialist/regulatory-compliance-2026`
- `pro/ux/accessibility-specialist/testing-with-assistive-technology`
- `pro/ux/accessibility-specialist/wcag-22-compliance`
