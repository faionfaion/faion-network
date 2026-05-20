# Accessibility audit + test automation

## Context

Done when: WCAG 2.2 AA conformance baseline measured, automated a11y scans wired into CI for changed components, manual screen-reader + keyboard checks scheduled per release, an a11y backlog is prioritised by user-blocking severity, and a no-regression budget is enforced in PR review.

## Outcome

By the time this playbook closes:

- Done-state achieved as described in the scope: Done when: WCAG 2.
- Decision doc signed: continue / iterate / kill, backed by evidence.
- Runbook + acceptance criteria in source control, handed to on-call / next owner.
- All must-fix issues from Harden / Pilot closed; nice-to-fix backlog ticketed.

## Steps

### 1. Audit

Get an honest map of where things stand today for: Accessibility audit + test automation.

Tasks:
- Inventory current state, owners, and recent incidents
- Identify the top 3 risks that block the desired outcome
- Surface unknowns and missing telemetry up front

Methodologies:
- `pro/ux/accessibility-specialist/a11y-basics`

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
- `pro/ux/accessibility-specialist/a11y-testing`

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
- `pro/ux/accessibility-specialist/accessibility-first-design`

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
- `pro/ux/accessibility-specialist/ada-title-ii-compliance-2026`

Outputs:
- Failure-mode report + closure log
- Ticketed nice-to-fix backlog

### 5. Pilot

Run with a controlled blast radius before broad rollout.

Tasks:
- Roll out to a controlled subset (canary, beta team, single client)
- Measure against acceptance criteria with real traffic / real work
- Capture rollback signal in writing

Methodologies:
- `pro/ux/accessibility-specialist/cognitive-inclusion-design`

Outputs:
- Pilot metrics vs. acceptance criteria
- Rollback decision criteria in writing

### 6. Rollout

Move from pilot to general availability with confidence.

Tasks:
- Stage the rollout in defined cohorts / regions / risk bands
- Hold each stage open until telemetry is clean
- Communicate state to stakeholders at each step

Methodologies:
- `pro/ux/accessibility-specialist/regulatory-compliance-2026`

Outputs:
- Rollout log (cohort-by-cohort)
- Stakeholder update record

### 7. Operate

Hand off as a steady-state operation, not a hero ticket.

Tasks:
- Document the runbook for on-call
- Define the SLO + alert + escalation chain
- Schedule the next review cycle

Methodologies:
- `pro/ux/accessibility-specialist/testing-with-assistive-technology`
- `pro/ux/accessibility-specialist/wcag-22-compliance`
- `pro/ux/ux-ui-designer/accessibility-evaluation`
- `solo/dev/automation-tooling/playwright-automation`
- `solo/dev/automation-tooling/testing-js-ts-frontend`

Outputs:
- Runbook + on-call notes
- SLO + alert config in source control

## Decision points

- **Audit** → Advance only if all top-3 risks have a named owner; otherwise re-scope.
- **Plan** → Advance if every plan item maps to an acceptance criterion; rewrite the plan otherwise.
- **Build** → Advance when the slice runs end-to-end with one real user; loop on Build otherwise.
- **Harden** → Advance only with zero open must-fixes; otherwise stay in Harden.
- **Pilot** → Advance if pilot meets all acceptance criteria; pause for fix or revert otherwise.
- **Rollout** → Advance to the next cohort only after the previous is stable for the agreed window.
- **Operate** → Advance when on-call can resolve the top-3 likely incidents without the original author.

## References

- `pro/ux/accessibility-specialist/a11y-basics`
- `pro/ux/accessibility-specialist/a11y-testing`
- `pro/ux/accessibility-specialist/accessibility-first-design`
- `pro/ux/accessibility-specialist/ada-title-ii-compliance-2026`
- `pro/ux/accessibility-specialist/cognitive-inclusion-design`
- `pro/ux/accessibility-specialist/regulatory-compliance-2026`
- `pro/ux/accessibility-specialist/testing-with-assistive-technology`
- `pro/ux/accessibility-specialist/wcag-22-compliance`
- `pro/ux/ux-ui-designer/accessibility-evaluation`
- `solo/dev/automation-tooling/playwright-automation`
- `solo/dev/automation-tooling/testing-js-ts-frontend`

## Gaps

This playbook is `status: draft` and cannot publish until these methodology slugs are authored:

- `a11y-storybook-coverage-pattern` — listed in gaps_for_this_playbook from source brainstorm
- `at-manual-review-script` — listed in gaps_for_this_playbook from source brainstorm
- `a11y-no-regression-pr-gate` — listed in gaps_for_this_playbook from source brainstorm
