---
slug: handover-to-client-in-house-team-3-weeks
tier: pro
group: outsource
persona: P4
goal: TBD
complexity: deep
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "Handover to client in-house team (3 weeks) — Engagement is ending. By the end of week 3, the client's in-house team is operating the product alone: code, runbooks, ADRs, on-call rota, training vide..."
content_id: 29e22040fc758659
methodology_refs:
  - solution-assessment
  - cicd-tls-renewal-automation
  - project-closure
  - 30-60-90-day-plan
  - secrets-management
  - scope-management
  - onboarding
  - devops-aws-monitoring-dr
  - architecture-decision-records
  - onboarding-30-day
  - grafana-dashboards
  - design-docs-patterns
  - onboarding-60-90-day
  - prometheus-monitoring
  - living-documentation
  - api-monitoring-alerting
  - benefits-realization
  - api-monitoring-logging
  - lessons-learned
---

# Handover to client in-house team (3 weeks)

## Context

This playbook covers the global flow for the persona `p4-outsource-specialist`. It applies whenever the trigger described in the scope below appears in the operator's workflow. The output is a written, auditable artefact pack, not a verbal hand-wave.

## Outcome

Engagement is ending. By the end of week 3, the client's in-house team is operating the product alone: code, runbooks, ADRs, on-call rota, training videos and a 90-day defect SLA are in their hands. Daria gets a referenceable, signed acceptance letter.

## Steps

### 1. Scope

Define the scope, exit criteria, and the people who must agree on success.

Tasks:
- Restate the scope outcome for this engagement in one sentence.
- Identify who owns the scope output and who must approve it.
- Produce the scope artefact in the agreed format.

Methodologies:
- `pro/ba/ba-core/solution-assessment`
- `pro/infra/cicd-engineer/cicd-tls-renewal-automation`
- `pro/pm/pm-traditional/project-closure`

Decision gate: Advance to the next stage when the scope artefact is approved by the named owner; iterate if any blocker remains.

### 2. Discovery

Gather evidence about the current state, stakeholders, constraints, and prior data.

Tasks:
- Restate the discovery outcome for this engagement in one sentence.
- Identify who owns the discovery output and who must approve it.
- Produce the discovery artefact in the agreed format.

Methodologies:
- `pro/comms/hr-recruiter/30-60-90-day-plan`
- `pro/infra/cicd-engineer/secrets-management`
- `pro/pm/pm-traditional/scope-management`

Decision gate: Advance to the next stage when the discovery artefact is approved by the named owner; iterate if any blocker remains.

### 3. Plan

Turn discovery output into a written plan with owners, sequence, and risk reserves.

Tasks:
- Restate the plan outcome for this engagement in one sentence.
- Identify who owns the plan output and who must approve it.
- Produce the plan artefact in the agreed format.

Methodologies:
- `pro/comms/hr-recruiter/onboarding`
- `pro/infra/devops-engineer/devops-aws-monitoring-dr`
- `solo/sdd/sdd/architecture-decision-records`

Decision gate: Advance to the next stage when the plan artefact is approved by the named owner; iterate if any blocker remains.

### 4. Execute

Run the plan in order of dependency; ship each output before moving on.

Tasks:
- Restate the execute outcome for this engagement in one sentence.
- Identify who owns the execute output and who must approve it.
- Produce the execute artefact in the agreed format.

Methodologies:
- `pro/comms/hr-recruiter/onboarding-30-day`
- `pro/infra/devops-engineer/grafana-dashboards`
- `solo/sdd/sdd/design-docs-patterns`

Decision gate: Advance to the next stage when the execute artefact is approved by the named owner; iterate if any blocker remains.

### 5. Verify

Check the work against the exit criteria with the people who signed off in Scope.

Tasks:
- Restate the verify outcome for this engagement in one sentence.
- Identify who owns the verify output and who must approve it.
- Produce the verify artefact in the agreed format.

Methodologies:
- `pro/comms/hr-recruiter/onboarding-60-90-day`
- `pro/infra/devops-engineer/prometheus-monitoring`
- `solo/sdd/sdd/living-documentation`

Decision gate: Advance to the next stage when the verify artefact is approved by the named owner; iterate if any blocker remains.

### 6. Communicate

Tell every stakeholder what changed, what's next, and what they own.

Tasks:
- Restate the communicate outcome for this engagement in one sentence.
- Identify who owns the communicate output and who must approve it.
- Produce the communicate artefact in the agreed format.

Methodologies:
- `pro/dev/software-developer/api-monitoring-alerting`
- `pro/pm/pm-traditional/benefits-realization`

Decision gate: Advance to the next stage when the communicate artefact is approved by the named owner; iterate if any blocker remains.

### 7. Close

Capture lessons, archive the artefacts, and trigger the next-step pipeline.

Tasks:
- Restate the close outcome for this engagement in one sentence.
- Identify who owns the close output and who must approve it.
- Produce the close artefact in the agreed format.

Methodologies:
- `pro/dev/software-developer/api-monitoring-logging`
- `pro/pm/pm-traditional/lessons-learned`

Decision gate: Advance to the next stage when the close artefact is approved by the named owner; iterate if any blocker remains.

## Decision points

- Each stage has a written decision gate; do not advance unless the gate's owner has signed off in the artefact log.
- If a stage gate fails twice, escalate to the playbook's named maintainer before retrying.

## References

- `pro/ba/ba-core/solution-assessment` — methodology cited inside the stages above.
- `pro/comms/hr-recruiter/30-60-90-day-plan` — methodology cited inside the stages above.
- `pro/comms/hr-recruiter/onboarding` — methodology cited inside the stages above.
- `pro/comms/hr-recruiter/onboarding-30-day` — methodology cited inside the stages above.
- `pro/comms/hr-recruiter/onboarding-60-90-day` — methodology cited inside the stages above.
- `pro/dev/software-developer/api-monitoring-alerting` — methodology cited inside the stages above.
