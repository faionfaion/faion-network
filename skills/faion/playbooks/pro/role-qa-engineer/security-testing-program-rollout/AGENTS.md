---
slug: security-testing-program-rollout
tier: pro
group: role-qa-engineer
persona: QA engineer / test lead in an indie or small-team product context.
goal: build-ship
complexity: deep
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "Security testing program rollout. Done when: SAST + DAST + SCA + secrets scan wired as CI gates, dependency inventory + SBOM produced per build, threat-model refreshed for top services, OWASP-mappe..."
content_id: 7ab4525a4d9a2c58
methodology_refs:
  - sec-codeql-autofix-on-pr
  - sec-secrets-defense-in-depth
  - sec-trivy-pinned-supply-chain-scan
  - gitops-secrets-security
  - security-container-scanning
  - security-dast
  - security-policy-as-code
  - security-sast
  - security-supply-chain
  - api-rate-limiting
  - api-testing
  - api-gateway-security
  - security-architecture
  - security-testing
---

# Security testing program rollout

## Context

Done when: SAST + DAST + SCA + secrets scan wired as CI gates, dependency inventory + SBOM produced per build, threat-model refreshed for top services, OWASP-mapped abuse cases in automated test suite, pentest cadence agreed, and a vuln triage SLA + waiver workflow is enforced.

## Outcome

By the time this playbook closes:

- Done-state achieved as described in the scope: Done when: SAST + DAST + SCA + secrets scan wired as CI gates, dependency inventory + SBOM produced per build, threat-model refreshed for top services, OWASP-mapped abuse cases in automated test suite, pentest cadence agreed, and a vuln triage SLA + waiver workflow is enforced.
- Decision doc signed: continue / iterate / kill, backed by evidence.
- Runbook + acceptance criteria in source control, handed to on-call / next owner.
- All must-fix issues from Harden / Pilot closed; nice-to-fix backlog ticketed.

## Steps

### 1. Audit

Get an honest map of where things stand today for: Security testing program rollout.

Tasks:
- Inventory current state, owners, and recent incidents
- Identify the top 3 risks that block the desired outcome
- Surface unknowns and missing telemetry up front

Methodologies:
- `geek/sdlc-ai/sec-codeql-autofix-on-pr`

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
- `geek/sdlc-ai/sec-secrets-defense-in-depth`

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
- `geek/sdlc-ai/sec-trivy-pinned-supply-chain-scan`

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
- `pro/infra/cicd-engineer/gitops-secrets-security`

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
- `pro/infra/cicd-engineer/security-container-scanning`

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
- `pro/infra/cicd-engineer/security-dast`

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
- `pro/infra/cicd-engineer/security-policy-as-code`

Outputs:
- Runbook + on-call notes
- SLO + alert config in source control

### 8. Review

Close the loop with a written retro and clear next-cycle bets.

Tasks:
- Compile evidence trail + metrics from rollout
- Write retro: what worked, what didn't, what we are changing
- Decide explicit continue / iterate / kill for the next cycle

Methodologies:
- `pro/infra/cicd-engineer/security-sast`
- `pro/infra/cicd-engineer/security-supply-chain`
- `solo/dev/api-developer/api-rate-limiting`
- `solo/dev/api-developer/api-testing`
- `solo/dev/software-architect/api-gateway-security`
- `solo/dev/software-architect/security-architecture`
- `solo/dev/software-developer/security-testing`

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

- `geek/sdlc-ai/sec-codeql-autofix-on-pr`
- `geek/sdlc-ai/sec-secrets-defense-in-depth`
- `geek/sdlc-ai/sec-trivy-pinned-supply-chain-scan`
- `pro/infra/cicd-engineer/gitops-secrets-security`
- `pro/infra/cicd-engineer/security-container-scanning`
- `pro/infra/cicd-engineer/security-dast`
- `pro/infra/cicd-engineer/security-policy-as-code`
- `pro/infra/cicd-engineer/security-sast`
- `pro/infra/cicd-engineer/security-supply-chain`
- `solo/dev/api-developer/api-rate-limiting`
- `solo/dev/api-developer/api-testing`
- `solo/dev/software-architect/api-gateway-security`
- `solo/dev/software-architect/security-architecture`
- `solo/dev/software-developer/security-testing`

## Gaps

This playbook is `status: draft` and cannot publish until these methodology slugs are authored:

- `abuse-case-test-cookbook` — listed in gaps_for_this_playbook from source brainstorm
- `vuln-triage-sla-template` — listed in gaps_for_this_playbook from source brainstorm
- `pentest-prep-checklist` — listed in gaps_for_this_playbook from source brainstorm
- `threat-model-lite-workshop` — listed in gaps_for_this_playbook from source brainstorm
