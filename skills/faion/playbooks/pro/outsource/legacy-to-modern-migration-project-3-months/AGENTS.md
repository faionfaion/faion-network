---
slug: legacy-to-modern-migration-project-3-months
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
summary: "Legacy-to-modern migration project (~3 months) — Vendor takes a multi-month migration: monolith to services, on-prem to cloud, or legacy stack (Struts / classic ASP / PHP4 / .NET Framework) to a cu..."
content_id: 56ed31464a948474
methodology_refs:
  - process-mining-automation
  - domain-driven-design
  - api-monitoring-alerting
  - microservices-circuit-breaker
  - lessons-learned
  - quality-gates-confidence
  - business-process-analysis
  - data-pipeline-design
  - api-monitoring-metrics
  - microservices-inter-service-comm
  - project-closure
  - task-creation-parallelization
  - data-analysis
  - distributed-patterns
  - clean-architecture
  - microservices-saga-pattern
  - risk-management
  - interface-analysis
  - event-driven-architecture
  - ddd-aggregates
  - backup-database-mysql-mongo
  - earned-value-management
  - strategy-analysis-change-strategy
  - microservices-architecture
  - ddd-anti-corruption-layer
  - backup-database-postgres
  - writing-implementation-plans
  - strategy-analysis-current-state
  - observability-architecture
  - ddd-domain-events
  - backup-verification-dr
  - architecture-decision-records
  - strategy-analysis-future-state
  - reliability-architecture
  - ddd-repositories
  - benefits-realization
  - code-review-cycle
---

# Legacy-to-modern migration project (~3 months)

## Context

This playbook covers the global flow for the persona `p4-outsource-specialist`. It applies whenever the trigger described in the scope below appears in the operator's workflow. The output is a written, auditable artefact pack, not a verbal hand-wave.

## Outcome

Vendor takes a multi-month migration: monolith to services, on-prem to cloud, or legacy stack (Struts / classic ASP / PHP4 / .NET Framework) to a current one. By project close: target system is live in production, traffic cut over with rollback proven, legacy decommission plan signed, performance and cost SLAs met. AI coding agent is used heavily but never trusted blind.

## Steps

### 1. Scope

Define the scope, exit criteria, and the people who must agree on success.

Tasks:
- Restate the scope outcome for this engagement in one sentence.
- Identify who owns the scope output and who must approve it.
- Produce the scope artefact in the agreed format.

Methodologies:
- `pro/ba/ba-core/process-mining-automation`
- `pro/dev/code-quality/domain-driven-design`
- `pro/dev/software-developer/api-monitoring-alerting`
- `pro/dev/software-developer/microservices-circuit-breaker`
- `pro/pm/pm-traditional/lessons-learned`
- `solo/sdd/sdd/quality-gates-confidence`

Decision gate: Advance to the next stage when the scope artefact is approved by the named owner; iterate if any blocker remains.

### 2. Discovery

Gather evidence about the current state, stakeholders, constraints, and prior data.

Tasks:
- Restate the discovery outcome for this engagement in one sentence.
- Identify who owns the discovery output and who must approve it.
- Produce the discovery artefact in the agreed format.

Methodologies:
- `pro/ba/ba-modeling/business-process-analysis`
- `pro/dev/software-architect/data-pipeline-design`
- `pro/dev/software-developer/api-monitoring-metrics`
- `pro/dev/software-developer/microservices-inter-service-comm`
- `pro/pm/pm-traditional/project-closure`
- `solo/sdd/sdd/task-creation-parallelization`

Decision gate: Advance to the next stage when the discovery artefact is approved by the named owner; iterate if any blocker remains.

### 3. Plan

Turn discovery output into a written plan with owners, sequence, and risk reserves.

Tasks:
- Restate the plan outcome for this engagement in one sentence.
- Identify who owns the plan output and who must approve it.
- Produce the plan artefact in the agreed format.

Methodologies:
- `pro/ba/ba-modeling/data-analysis`
- `pro/dev/software-architect/distributed-patterns`
- `pro/dev/software-developer/clean-architecture`
- `pro/dev/software-developer/microservices-saga-pattern`
- `pro/pm/pm-traditional/risk-management`

Decision gate: Advance to the next stage when the plan artefact is approved by the named owner; iterate if any blocker remains.

### 4. Execute

Run the plan in order of dependency; ship each output before moving on.

Tasks:
- Restate the execute outcome for this engagement in one sentence.
- Identify who owns the execute output and who must approve it.
- Produce the execute artefact in the agreed format.

Methodologies:
- `pro/ba/ba-modeling/interface-analysis`
- `pro/dev/software-architect/event-driven-architecture`
- `pro/dev/software-developer/ddd-aggregates`
- `pro/infra/cicd-engineer/backup-database-mysql-mongo`
- `pro/pm/project-manager/earned-value-management`

Decision gate: Advance to the next stage when the execute artefact is approved by the named owner; iterate if any blocker remains.

### 5. Verify

Check the work against the exit criteria with the people who signed off in Scope.

Tasks:
- Restate the verify outcome for this engagement in one sentence.
- Identify who owns the verify output and who must approve it.
- Produce the verify artefact in the agreed format.

Methodologies:
- `pro/ba/business-analyst/strategy-analysis-change-strategy`
- `pro/dev/software-architect/microservices-architecture`
- `pro/dev/software-developer/ddd-anti-corruption-layer`
- `pro/infra/cicd-engineer/backup-database-postgres`
- `solo/sdd/sdd-planning/writing-implementation-plans`

Decision gate: Advance to the next stage when the verify artefact is approved by the named owner; iterate if any blocker remains.

### 6. Communicate

Tell every stakeholder what changed, what's next, and what they own.

Tasks:
- Restate the communicate outcome for this engagement in one sentence.
- Identify who owns the communicate output and who must approve it.
- Produce the communicate artefact in the agreed format.

Methodologies:
- `pro/ba/business-analyst/strategy-analysis-current-state`
- `pro/dev/software-architect/observability-architecture`
- `pro/dev/software-developer/ddd-domain-events`
- `pro/infra/cicd-engineer/backup-verification-dr`
- `solo/sdd/sdd/architecture-decision-records`

Decision gate: Advance to the next stage when the communicate artefact is approved by the named owner; iterate if any blocker remains.

### 7. Close

Capture lessons, archive the artefacts, and trigger the next-step pipeline.

Tasks:
- Restate the close outcome for this engagement in one sentence.
- Identify who owns the close output and who must approve it.
- Produce the close artefact in the agreed format.

Methodologies:
- `pro/ba/business-analyst/strategy-analysis-future-state`
- `pro/dev/software-architect/reliability-architecture`
- `pro/dev/software-developer/ddd-repositories`
- `pro/pm/pm-traditional/benefits-realization`
- `solo/sdd/sdd/code-review-cycle`

Decision gate: Advance to the next stage when the close artefact is approved by the named owner; iterate if any blocker remains.

## Decision points

- Each stage has a written decision gate; do not advance unless the gate's owner has signed off in the artefact log.
- If a stage gate fails twice, escalate to the playbook's named maintainer before retrying.

## References

- `pro/ba/ba-core/process-mining-automation` — methodology cited inside the stages above.
- `pro/ba/ba-modeling/business-process-analysis` — methodology cited inside the stages above.
- `pro/ba/ba-modeling/data-analysis` — methodology cited inside the stages above.
- `pro/ba/ba-modeling/interface-analysis` — methodology cited inside the stages above.
- `pro/ba/business-analyst/strategy-analysis-change-strategy` — methodology cited inside the stages above.
- `pro/ba/business-analyst/strategy-analysis-current-state` — methodology cited inside the stages above.
