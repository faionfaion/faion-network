---
slug: qa-automation-framework-migration-cypress-to-playwright
tier: solo
group: role-qa-engineer
persona: QA engineer / test lead in an indie or small-team product context.
goal: TBD
complexity: deep
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "QA automation framework migration (Cypress to Playwright). Done when: every active Cypress spec is either ported to Playwright, deleted as obsolete, or explicitly waived; CI runs only Playwright; f..."
content_id: babe5c21efff6e70
methodology_refs:
  - e2e-testing
  - mocking-strategies
  - test-fixtures
  - testing-patterns
  - test-self-healing-locators-audited
  - playwright-automation
  - testing-js-ts-frontend
---

# QA automation framework migration (Cypress to Playwright)

## Context

Done when: every active Cypress spec is either ported to Playwright, deleted as obsolete, or explicitly waived; CI runs only Playwright; flake rate is equal or better; wall-time is equal or better; team has new auth patterns + page-objects + fixtures; old framework removed from the repo and CI config.

## Outcome

By the time this playbook closes:

- Done-state achieved as described in the scope: Done when: every active Cypress spec is either ported to Playwright, deleted as obsolete, or explicitly waived; CI runs only Playwright; flake rate is equal or better; wall-time is equal or better; team has new auth patterns + page-objects + fixtures; old framework removed from the repo and CI config.
- Decision doc signed: continue / iterate / kill, backed by evidence.
- Runbook + acceptance criteria in source control, handed to on-call / next owner.
- All must-fix issues from Harden / Pilot closed; nice-to-fix backlog ticketed.

## Steps

### 1. Audit

Get an honest map of where things stand today for: QA automation framework migration (Cypress to Playwright).

Tasks:
- Inventory current state, owners, and recent incidents
- Identify the top 3 risks that block the desired outcome
- Surface unknowns and missing telemetry up front

Methodologies:
- `free/dev/testing-developer/e2e-testing`

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
- `free/dev/testing-developer/mocking-strategies`

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
- `free/dev/testing-developer/test-fixtures`

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
- `free/dev/testing-developer/testing-patterns`

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
- `geek/sdlc-ai/test-self-healing-locators-audited`

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
- `solo/dev/automation-tooling/playwright-automation`

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
- `solo/dev/automation-tooling/testing-js-ts-frontend`

Outputs:
- Runbook + on-call notes
- SLO + alert config in source control

### 8. Review

Close the loop with a written retro and clear next-cycle bets.

Tasks:
- Compile evidence trail + metrics from rollout
- Write retro: what worked, what didn't, what we are changing
- Decide explicit continue / iterate / kill for the next cycle

Outputs:
- Retro doc with evidence
- Continue / iterate / kill decision for next cycle

## Decision points

- **Audit** → Advance only if all top-3 risks have a named owner; otherwise re-scope.
- **Plan** → Advance if every plan item maps to an acceptance criterion; rewrite the plan otherwise.
- **Build** → Advance when the slice runs end-to-end with one real user; loop on Build otherwise.
- **Harden** → Advance only with zero open must-fixes; otherwise stay in Harden.
- **Pilot** → Advance if pilot meets all acceptance criteria; pause for fix or revert otherwise.
- **Rollout** → Advance to the next cohort only after the previous is stable for the agreed window.
- **Operate** → Advance when on-call can resolve the top-3 likely incidents without the original author.
- **Review** → A written decision is mandatory; no 'see how it goes'.

## References

- `free/dev/testing-developer/e2e-testing`
- `free/dev/testing-developer/mocking-strategies`
- `free/dev/testing-developer/test-fixtures`
- `free/dev/testing-developer/testing-patterns`
- `geek/sdlc-ai/test-self-healing-locators-audited`
- `solo/dev/automation-tooling/playwright-automation`
- `solo/dev/automation-tooling/testing-js-ts-frontend`

## Gaps

This playbook is `status: draft` and cannot publish until these methodology slugs are authored:

- `e2e-framework-migration-playbook` — listed in gaps_for_this_playbook from source brainstorm
- `parallel-run-coverage-diff` — listed in gaps_for_this_playbook from source brainstorm
- `page-object-conventions-2026` — listed in gaps_for_this_playbook from source brainstorm
