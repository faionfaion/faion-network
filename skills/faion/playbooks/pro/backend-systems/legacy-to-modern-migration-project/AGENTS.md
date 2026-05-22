---
slug: legacy-to-modern-migration-project
tier: pro
group: backend-systems
persona: P4
goal: TBD
complexity: deep
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: Multi-month migration (monolith→services, on-prem→cloud, legacy stack→modern) → target system live with traffic cut over, rollback proven, legacy decom plan signed, performance + cost SLAs met, AI...
content_id: 46ec29e2f25f98a9
methodology_refs:
  - strategy-analysis-current-state
  - process-mining-automation
  - business-process-analysis
  - data-analysis
  - interface-analysis
  - strategy-analysis-future-state
  - strategy-analysis-change-strategy
  - microservices-architecture
  - event-driven-architecture
  - distributed-patterns
  - observability-architecture
  - reliability-architecture
  - domain-driven-design
  - clean-architecture
  - ddd-aggregates
  - ddd-anti-corruption-layer
  - ddd-domain-events
  - ddd-repositories
  - architecture-decision-records
  - strangler-fig-playbook-vendor
  - writing-implementation-plans
  - task-creation-parallelization
  - code-review-cycle
  - quality-gates-confidence
  - data-pipeline-design
  - microservices-inter-service-comm
  - microservices-circuit-breaker
  - microservices-saga-pattern
  - ai-agent-migration-prompt-pack
  - api-monitoring-metrics
  - api-monitoring-alerting
  - backup-database-mysql-mongo
  - backup-database-postgres
  - backup-verification-dr
  - risk-management
  - earned-value-management
  - data-reconciliation-checklist
  - benefits-realization
  - lessons-learned
  - project-closure
  - cutover-rollback-runbook-template
  - deploy-blue-green-canary
  - production-cicd-pipeline
---

# Legacy-to-modern migration project (~3 months)

**Persona:** P4 Outsource Specialist · **Tier:** pro · **Complexity:** deep · **Angle:** global

## Why this playbook exists

Multi-month migration (monolith→services, on-prem→cloud, legacy stack→modern) → target system live with traffic cut over, rollback proven, legacy decom plan signed, performance + cost SLAs met, AI agent leveraged but never trusted blind.

End-to-end migration project led by an outsource senior. Output: target system live in production, traffic cut over with rollback proven, legacy decom plan signed, performance + cost SLAs met. AI coding agent is used heavily but every change passes human review. Reconciliation evidence retained for audit.

Most outsource seniors improvise this flow — fine at one engagement, costly across five. This playbook fixes the chain: explicit stages, explicit decision-gates, written artifacts at every step, AI agents on a leash, no silent work absorption.

## How to run it

Walk the stages in order. Each stage has a decision-gate; do not advance until the gate condition is met in writing. A stranger should be able to read the artifacts and understand both *what* you did and *why* you advanced. Atomic stages are designed to be completed in a single sitting; deep stages span multiple sessions.

## Stage map

### Stage 1 — Current-state discovery

**Intent:** Inhale the legacy reality before designing the future.

**Tasks**
- Strategy-analysis: current state of business processes
- Process mining where logs exist
- Business process + data analysis
- Interface analysis on every integration boundary

**Outputs**
- Current-state architecture diagram
- Process inventory
- Interface inventory
- Data dictionary v1

**Decision gate**

Advance when the migration team can describe the legacy on a whiteboard from memory.

### Stage 2 — Target design

**Intent:** Design the smallest target architecture that satisfies the SLAs.

**Tasks**
- Future-state strategy + change strategy
- Architecture choices: microservices vs strangler vs lift-shift
- Apply DDD aggregates / events / repositories where useful
- Cross-cutting concerns: observability, reliability, anti-corruption layer
- Design event-driven boundaries where they cut coupling

**Outputs**
- Target architecture diagrams
- ADR set
- Migration approach memo (strangler vs other)

**Decision gate**

Advance when the target arch is explainable in one diagram + 5 ADRs.

### Stage 3 — Implementation plan

**Intent:** Sequence the work into independently shippable slices.

**Tasks**
- Write implementation plan with parallelisable slices
- Insert quality gates and code-review checkpoints
- Design data-pipeline strategy where applicable
- Inter-service communication contracts (saga, circuit breaker)
- Plan AI-agent usage envelope per slice

**Outputs**
- Implementation plan with slices
- Quality-gate checklist
- AI-agent prompt pack

**Decision gate**

Advance when slices are independently shippable AND review gates are explicit.

### Stage 4 — Build + dual-run

**Intent:** Build slices, dual-run with the legacy, reconcile constantly.

**Tasks**
- Implement slices in parallel where dependencies allow
- Reconciliation checks between legacy and target
- Backup posture for both systems during dual-run
- API monitoring (metrics + alerting) on the target
- Risk-management cycle each sprint

**Outputs**
- Reconciliation reports per slice
- Production-ready target system
- Backups for both systems

**Decision gate**

Advance when dual-run reconciliation is green for ≥1 full business cycle.

### Stage 5 — Cutover + decom

**Intent:** Cut traffic, prove rollback, decom the legacy.

**Tasks**
- Blue/green or canary cutover (link to existing playbook)
- Rollback drill before opening the floodgates
- Benefits-realisation review against SLAs
- Project-closure ceremony
- Lessons-learned retro for the next migration

**Outputs**
- Cutover runbook executed
- Rollback drill log
- Decom plan signed
- Benefits-realisation report

**Decision gate**

Engagement closes when 100% of traffic runs on target, rollback drill is logged, and legacy decom date is signed.

## Common pitfalls

- Re-architecting the business while you migrate — keeps the cutover date sliding
- Trusting AI-generated migration scripts without reconciliation — silent data loss
- Skipping the rollback drill because the team is exhausted — that's exactly when you need it

## Quality checklist

- Can we roll back in <1 hour if the cutover breaks?
- Did reconciliation prove the data, not just sample it?
- Did we measure the SLAs we promised, or the SLAs we found convenient?

## Related playbooks

- `deploy-blue-green-canary`
- `production-cicd-pipeline`
- `compliance-grade-feature-delivery`

## Gaps

These methodologies are referenced in the chain above but not yet materialised. They block promotion of this playbook from `draft` to `published`.

- `strangler-fig-playbook-vendor` (blocks stage 2)
- `ai-agent-migration-prompt-pack` (blocks stage 3)
- `data-reconciliation-checklist` (blocks stage 4)
- `cutover-rollback-runbook-template` (blocks stage 5)
- `deploy-blue-green-canary` (blocks stage 5)
- `production-cicd-pipeline` (blocks stage 5)
