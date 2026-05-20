# FinTech / HIPAA compliance audit prep (4 weeks)

## Context

This playbook covers the global flow for the persona `p4-outsource-specialist`. It applies whenever the trigger described in the scope below appears in the operator's workflow. The output is a written, auditable artefact pack, not a verbal hand-wave.

## Outcome

Client triggers a compliance audit (SOC 2 mid-cycle, PCI DSS QSA, HIPAA, banking-core). By end of week 4 Daria's team has: gap analysis, remediated controls, evidence pack, control owners, audit-day runbook. The vendor's part of the audit passes without findings that escalate to the client steerco.

## Steps

### 1. Scope

Define the scope, exit criteria, and the people who must agree on success.

Tasks:
- Restate the scope outcome for this engagement in one sentence.
- Identify who owns the scope output and who must approve it.
- Produce the scope artefact in the agreed format.

Methodologies:
- `pro/ba/ba-core/requirements-traceability`
- `pro/infra/cicd-engineer/backup-basics`
- `pro/infra/cicd-engineer/security-dast`
- `pro/pm/pm-traditional/risk-register`

Decision gate: Advance to the next stage when the scope artefact is approved by the named owner; iterate if any blocker remains.

### 2. Discovery

Gather evidence about the current state, stakeholders, constraints, and prior data.

Tasks:
- Restate the discovery outcome for this engagement in one sentence.
- Identify who owns the discovery output and who must approve it.
- Produce the discovery artefact in the agreed format.

Methodologies:
- `pro/ba/ba-core/strategy-analysis`
- `pro/infra/cicd-engineer/backup-database-postgres`
- `pro/infra/cicd-engineer/security-policy-as-code`
- `pro/pm/project-manager/raci-matrix`

Decision gate: Advance to the next stage when the discovery artefact is approved by the named owner; iterate if any blocker remains.

### 3. Plan

Turn discovery output into a written plan with owners, sequence, and risk reserves.

Tasks:
- Restate the plan outcome for this engagement in one sentence.
- Identify who owns the plan output and who must approve it.
- Produce the plan artefact in the agreed format.

Methodologies:
- `pro/ba/business-analyst/strategy-analysis-current-state`
- `pro/infra/cicd-engineer/backup-verification-dr`
- `pro/infra/cicd-engineer/security-sast`

Decision gate: Advance to the next stage when the plan artefact is approved by the named owner; iterate if any blocker remains.

### 4. Execute

Run the plan in order of dependency; ship each output before moving on.

Tasks:
- Restate the execute outcome for this engagement in one sentence.
- Identify who owns the execute output and who must approve it.
- Produce the execute artefact in the agreed format.

Methodologies:
- `pro/ba/business-analyst/strategy-analysis-gap-analysis`
- `pro/infra/cicd-engineer/cicd-cert-rotation-pipeline`
- `pro/infra/cicd-engineer/security-supply-chain`

Decision gate: Advance to the next stage when the execute artefact is approved by the named owner; iterate if any blocker remains.

### 5. Verify

Check the work against the exit criteria with the people who signed off in Scope.

Tasks:
- Restate the verify outcome for this engagement in one sentence.
- Identify who owns the verify output and who must approve it.
- Produce the verify artefact in the agreed format.

Methodologies:
- `pro/dev/software-developer/api-monitoring-logging`
- `pro/infra/cicd-engineer/cicd-mtls-deployment`
- `pro/pm/pm-traditional/communications-management`

Decision gate: Advance to the next stage when the verify artefact is approved by the named owner; iterate if any blocker remains.

### 6. Communicate

Tell every stakeholder what changed, what's next, and what they own.

Tasks:
- Restate the communicate outcome for this engagement in one sentence.
- Identify who owns the communicate output and who must approve it.
- Produce the communicate artefact in the agreed format.

Methodologies:
- `pro/infra/cicd-engineer/azure-nsg-rules`
- `pro/infra/cicd-engineer/secrets-management`
- `pro/pm/pm-traditional/quality-management`

Decision gate: Advance to the next stage when the communicate artefact is approved by the named owner; iterate if any blocker remains.

### 7. Close

Capture lessons, archive the artefacts, and trigger the next-step pipeline.

Tasks:
- Restate the close outcome for this engagement in one sentence.
- Identify who owns the close output and who must approve it.
- Produce the close artefact in the agreed format.

Methodologies:
- `pro/infra/cicd-engineer/azure-private-link`
- `pro/infra/cicd-engineer/security-container-scanning`
- `pro/pm/pm-traditional/risk-management`

Decision gate: Advance to the next stage when the close artefact is approved by the named owner; iterate if any blocker remains.

## Decision points

- Each stage has a written decision gate; do not advance unless the gate's owner has signed off in the artefact log.
- If a stage gate fails twice, escalate to the playbook's named maintainer before retrying.

## References

- `pro/ba/ba-core/requirements-traceability` — methodology cited inside the stages above.
- `pro/ba/ba-core/strategy-analysis` — methodology cited inside the stages above.
- `pro/ba/business-analyst/strategy-analysis-current-state` — methodology cited inside the stages above.
- `pro/ba/business-analyst/strategy-analysis-gap-analysis` — methodology cited inside the stages above.
- `pro/dev/software-developer/api-monitoring-logging` — methodology cited inside the stages above.
- `pro/infra/cicd-engineer/azure-nsg-rules` — methodology cited inside the stages above.
