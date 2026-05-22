---
slug: rfc-production-feature-delivery
tier: geek
group: product-team
persona: p6-product-dev-team
goal: build-ship
complexity: deep
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: One product bet travels from approved RFC to live production behind feature flag with telemetry + on-call ready. All handoffs (PM brief → BA reqs → Architect design → Dev implementation → QA verifi...
content_id: 669b38728c0ea65f
methodology_refs:
  - claude-md-creation
  - llm-friendly-architecture
  - ai-assisted-specification-writing
  - gov-approval-token-signed-jwt
  - gov-conventional-commits-enforced
  - gov-sonarqube-ai-code-gate
  - inc-runbook-as-markdown-tagged-steps
  - kb-agents-md-context-pyramid
  - lint-precommit-floor
  - lint-ruff-and-biome-as-default
  - mr-error-tracker-draft-pr
  - mr-graph-vs-diff-reviewer
  - mr-slash-command-surface
  - task-agent-drafts-spec-before-coding
  - task-plan-mode-locked-execution
  - task-spec-kit-three-step
  - task-worktree-runtime-isolation
  - test-consumer-contract-from-spec
  - test-mutation-feedback-loop
  - test-property-based-llm-invariants
  - test-self-healing-locators-audited
  - test-tdd-red-green-split-agents
  - acceptance-criteria
  - elicitation-techniques
  - requirements-prioritization
  - requirements-traceability
  - requirements-validation
  - use-case-modeling
  - user-story-mapping
  - clean-architecture
  - domain-driven-design
  - event-driven-architecture
  - microservices-architecture
  - quality-attributes-analysis
  - argocd-gitops
  - gitops-progressive-delivery
  - grafana-basics
  - prometheus-monitoring
  - continuous-discovery-habits
  - experimentation-at-scale
  - feedback-management
  - minimum-product-frameworks
  - mlp-planning
  - product-analytics
  - opportunity-solution-trees
---

# RFC → Production: feature delivery (3-6 weeks)

## Context

One product bet travels from approved RFC to live production behind feature flag with telemetry + on-call ready. All handoffs (PM brief → BA reqs → Architect design → Dev implementation → QA verification → DevOps deploy → PdM rollout) are auditable. Output: shipped feature, runbook, dashboards, post-launch review scheduled.

## Outcome

By the end of this playbook, the operator has run the 6 stages below and produced the written decision artefact in the final stage.

Success criteria:

- All 6 stages have written outputs in the project record
- Each stage's decision gate was answered before advancing (yes / no in writing)
- Final stage produced the required written decision artifact
- Every methodology reference loaded cleanly via `faion get-content`

## Steps

### 1. RFC

Decide the design before any prod code.

Tasks:
- Write the RFC: problem, proposed design, alternatives, tradeoffs
- Review with architecture + affected teams; collect comments
- Resolve every blocking comment in writing

Outputs:
- RFC doc
- review comments + resolutions
- approval signoff

Decision gate: Advance only when RFC is approved with no blocking comments open.

### 2. Spec & Tasks

Translate the RFC into shippable tasks.

Tasks:
- Convert RFC into spec.md with acceptance criteria
- Break into tasks ≤2 days each with owners
- Plan the rollout (feature flag, migration, rollback)

Outputs:
- spec.md
- task tree with owners
- rollout plan

Decision gate: Advance when every task has a clear AC and a named owner.

### 3. Build

Implement against the spec; PRs go through review.

Tasks:
- Implement tasks in dependency order
- Open PRs against a feature branch; review with tests
- Keep CI green continuously

Outputs:
- merged PRs
- passing CI
- demo-able feature branch

Decision gate: Advance when every spec AC is implemented and PR-reviewed.

### 4. Test in Production-like Env

No surprises on rollout day.

Tasks:
- Run integration and load tests against staging
- Run the rollback drill once
- Sign off the staging report with QA + on-call

Outputs:
- staging test report
- rollback drill log
- QA + on-call signoff

Decision gate: Advance only when staging passes AND rollback drill ran clean.

### 5. Rollout

Ship behind a flag, watch the dashboards.

Tasks:
- Roll out to 1%, then 10%, then 100% on the flag
- Watch error/latency/business dashboards at each step
- Pause or roll back on any threshold breach

Outputs:
- rollout log per cohort
- dashboard snapshots
- pause/rollback decisions

Decision gate: Advance when feature is at 100% with green dashboards for 24h.

### 6. Post-Launch

Close the loop or kill the feature.

Tasks:
- Measure against the RFC's success metrics
- Run a blameless retro if any incident occurred
- Decide: keep / iterate / kill

Outputs:
- success-metric report
- retro doc if needed
- keep/iterate/kill memo

Decision gate: Required output: a written keep/iterate/kill decision.

## Decision points

- Stage 1 (RFC): Advance only when RFC is approved with no blocking comments open.
- Stage 2 (Spec & Tasks): Advance when every task has a clear AC and a named owner.
- Stage 3 (Build): Advance when every spec AC is implemented and PR-reviewed.
- Stage 4 (Test in Production-like Env): Advance only when staging passes AND rollback drill ran clean.
- Stage 5 (Rollout): Advance when feature is at 100% with green dashboards for 24h.
- Stage 6 (Post-Launch): Required output: a written keep/iterate/kill decision.

## References

- `claude-md-creation`
- `llm-friendly-architecture`
- `ai-assisted-specification-writing`
- `ai-assisted-specification-writing`
- `gov-approval-token-signed-jwt`
- `gov-conventional-commits-enforced`
- `gov-sonarqube-ai-code-gate`
- `inc-runbook-as-markdown-tagged-steps`
- `kb-agents-md-context-pyramid`
- `lint-precommit-floor`
- `lint-ruff-and-biome-as-default`
- `mr-error-tracker-draft-pr`
- `mr-graph-vs-diff-reviewer`
- `mr-slash-command-surface`
- `task-agent-drafts-spec-before-coding`
- `task-plan-mode-locked-execution`
- `task-spec-kit-three-step`
- `task-worktree-runtime-isolation`
- `test-consumer-contract-from-spec`
- `test-mutation-feedback-loop`
- `test-property-based-llm-invariants`
- `test-self-healing-locators-audited`
- `test-tdd-red-green-split-agents`
- `acceptance-criteria`
- `elicitation-techniques`
- `requirements-prioritization`
- `requirements-traceability`
- `requirements-validation`
- `use-case-modeling`
- `user-story-mapping`
- `clean-architecture`
- `domain-driven-design`
- `event-driven-architecture`
- `microservices-architecture`
- `quality-attributes-analysis`
- `argocd-gitops`
- `gitops-progressive-delivery`
- `grafana-basics`
- `prometheus-monitoring`
- `continuous-discovery-habits`
- `experimentation-at-scale`
- `feedback-management`
- `minimum-product-frameworks`
- `mlp-planning`
- `product-analytics`
- `opportunity-solution-trees`

Gaps (status: draft until empty):
- `rfc-template-product-dev-team` (see `gaps[]` in `playbook.yaml`)
- `feature-flag-rollout-runbook` (see `gaps[]` in `playbook.yaml`)
