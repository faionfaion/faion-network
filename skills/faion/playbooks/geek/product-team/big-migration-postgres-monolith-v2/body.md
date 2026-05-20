# Big migration: Postgres major or monolith-to-services

## Context

Cross-quarter migration completes with zero data loss, rollback path proven, dual-stack period bounded, all squads informed. Output: pre-migration baseline, dual-write/shadow-read evidence, cutover runbook executed, post-migration audit clean.

## Outcome

By the end of this playbook, the operator has run the 6 stages below and produced the written decision artefact in the final stage.

Success criteria:

- All 6 stages have written outputs in the project record
- Each stage's decision gate was answered before advancing (yes / no in writing)
- Final stage produced the required written decision artifact
- Every methodology reference loaded cleanly via `faion get-content`

## Steps

### 1. Scope the Migration

What exactly is moving, and why.

Tasks:
- Define source-state, target-state, and the business reason
- Quantify risk: downtime, data loss, perf regression, dev velocity
- Decide rollback strategy upfront

Outputs:
- scope doc
- risk register
- rollback strategy

Decision gate: Advance only when scope and rollback are signed off by tech lead + PM.

### 2. Design the Cutover

Pick a migration shape: dual-write, big-bang, strangler.

Tasks:
- Pick the migration pattern with explicit tradeoffs
- Design data-migration scripts and verification queries
- Design dashboards to watch the cutover live

Outputs:
- pattern decision RFC
- migration + verification scripts
- cutover dashboards

Decision gate: Advance when the RFC is approved with no blocking comments.

### 3. Dry-Run in Staging

Do the migration where it doesn't hurt.

Tasks:
- Run the full migration against a prod-snapshot in staging
- Verify data parity with the verification queries
- Time the migration; resolve any step that took >2x estimate

Outputs:
- staging migration log
- parity report
- timing report

Decision gate: Advance only when staging migration runs clean and within budget.

### 4. Communicate & Schedule

No surprises for users or on-call.

Tasks:
- Pick the maintenance window; tell affected users in writing
- Brief on-call and stakeholders on the runbook
- Stage the rollback path on standby

Outputs:
- maintenance window comms
- on-call brief
- rollback on standby

Decision gate: Advance when comms have gone out at least 48h before window.

### 5. Cut Over

Do it. Watch the dashboards.

Tasks:
- Run the migration runbook step by step
- Verify parity post-cutover; gate users back in by cohort
- Hold position at the rollback decision point until parity is green

Outputs:
- runbook execution log
- parity verification
- rollback decision log

Decision gate: Advance only when post-cutover parity is signed off.

### 6. Stabilize & Retro

Don't declare victory too early.

Tasks:
- Watch dashboards for 1 week; fix regressions promptly
- Run a blameless retro on the migration
- Decide: tear down old system or run dual until milestone

Outputs:
- 1-week dashboard report
- retro doc
- decommission/dual-run memo

Decision gate: Required output: a written decommission or dual-run decision.

## Decision points

- Stage 1 (Scope the Migration): Advance only when scope and rollback are signed off by tech lead + PM.
- Stage 2 (Design the Cutover): Advance when the RFC is approved with no blocking comments.
- Stage 3 (Dry-Run in Staging): Advance only when staging migration runs clean and within budget.
- Stage 4 (Communicate & Schedule): Advance when comms have gone out at least 48h before window.
- Stage 5 (Cut Over): Advance only when post-cutover parity is signed off.
- Stage 6 (Stabilize & Retro): Required output: a written decommission or dual-run decision.

## References

- `inc-runbook-as-markdown-tagged-steps`
- `test-consumer-contract-from-spec`
- `test-golden-master-legacy-rewrite`
- `test-property-based-llm-invariants`
- `strategy-analysis-change-strategy`
- `strategy-analysis-current-state`
- `strategy-analysis-future-state`
- `strategy-analysis-gap-analysis`
- `microservices-design`
- `event-driven-architecture`
- `microservices-architecture`
- `observability-architecture`
- `quality-attributes-analysis`
- `reliability-architecture`
- `ddd-aggregates`
- `ddd-anti-corruption-layer`
- `microservices-circuit-breaker`
- `microservices-inter-service-comm`
- `microservices-saga-pattern`
- `microservices-service-boundaries`
- `argocd-gitops`
- `backup-database-mysql-mongo`
- `backup-database-postgres`
- `backup-kubernetes-velero`
- `backup-verification-dr`
- `dora-metrics`
- `gitops-progressive-delivery`
- `backup-strategies`
- `change-control`
- `communications-management`
- `lessons-learned`
- `project-closure`
- `risk-management`
- `risk-register`
- `wbs-creation`

Gaps (status: draft until empty):
- `strangler-pattern-checklist-product-dev-team` (see `gaps[]` in `playbook.yaml`)
- `dual-write-shadow-read-template` (see `gaps[]` in `playbook.yaml`)
