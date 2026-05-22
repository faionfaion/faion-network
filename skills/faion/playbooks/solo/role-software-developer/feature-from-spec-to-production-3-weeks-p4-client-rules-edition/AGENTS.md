---
slug: feature-from-spec-to-production-3-weeks-p4-client-rules-edition
tier: solo
group: role-software-developer
persona: "Outsource developer shipping a client-issued ticket end-to-end on the client's repo"
goal: build-ship
complexity: medium
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "Outsource dev takes a client ticket from AC to tagged release on the client's repo, inside the client's conventions, review, and audit trail."
content_id: 6846f7881fc759f2
methodology_refs:
  - code-decomposition-patterns
  - code-review-process
  - code-review
  - e2e-testing
  - error-handling
  - integration-testing
  - language-framework-guide
  - tdd-workflow
  - kb-agents-md-context-pyramid
  - lint-precommit-floor
  - lint-staged-only-not-whole-tree
  - mr-graph-vs-diff-reviewer
  - task-agent-drafts-spec-before-coding
  - api-monitoring-logging
  - api-monitoring-metrics
  - cd-pipelines
  - continuous-delivery
  - architecture-decision-records
  - api-documentation
  - api-versioning
  - contract-first-development
  - feature-flags
  - trunk-based-development
  - task-creation-template-guide
  - writing-implementation-plans
  - api-first-development
  - code-review-cycle
  - living-documentation
  - mistake-memory
  - pattern-memory
  - quality-gates-confidence
  - reflexion-learning
  - task-creation-parallelization
  - writing-design-documents
  - writing-specifications
---

# Feature from spec to production (3 weeks, P4 client-rules edition)

## Context

Outsource developer ships a single feature on a client's codebase across 3 weeks. Covers conventions intake, spec draft, test plan, implementation, code review, contract + integration testing, observability, and release. Done when the feature is tagged in the client's repo and a post-deploy verification check has passed.

## Outcome

Client AC -> tagged production release on client repo, inside client conventions. Outsource dev takes a client ticket from AC to tagged release on the client's repo, inside the client's conventions, review, and audit trail.

## Steps

1. **Intake client conventions.** Speak the client's code before writing. Tasks: Read existing AGENTS.md / CONTRIBUTING / style guides; Capture review process + sign-off authority; Document the convention pyramid.
2. **Spec + test plan.** Agree on what + how to verify before coding. Tasks: Draft spec from AC (task-agent-drafts-spec-before-coding); Write test plan tied to AC; Get client sign-off.
3. **Contract-first.** Lock API contracts early. Tasks: Write API contracts + versioning notes; Add contract tests; Document with API docs.
4. **Implement TDD.** Tests lead the code. Tasks: Red-green-refactor per task; Stage lint only on changed files; Surface decomposition risks early.
5. **Test layers.** Unit + integration + e2e covered. Tasks: Add integration tests; Add e2e tests for critical flows; Update API docs + ADRs as needed.
6. **Client code review.** Pass review per client rules. Tasks: Open MR with graph context (not raw diff); Follow client review etiquette; Iterate on review notes.
7. **Ship + verify.** Tagged release + production verified. Tasks: Merge behind feature flag if available; Trigger CD pipeline + verify; Tag the release + post changelog.
8. **Memory + retro.** Carry forward what worked. Tasks: Capture engagement patterns in memory; Note mistakes for future avoidance; Run a lightweight reflexion pass.

## Decision points

- **After Intake client conventions:** Advance only when conventions are written down.
- **After Spec + test plan:** Advance only after client sign-off.
- **After Contract-first:** Advance only when contract tests are green.
- **After Implement TDD:** Advance only when tests are green on changed surface.
- **After Test layers:** Advance only when integration + e2e are green.
- **After Client code review:** Advance only after explicit approval.
- **After Ship + verify:** Advance only when production verification passes.
- **After Memory + retro:** Done when memory is updated.

## References

- `faion/knowledge/free/dev/code-quality/code-decomposition-patterns`
- `faion/knowledge/free/dev/code-quality/code-review-process`
- `faion/knowledge/free/dev/software-developer/code-review`
- `faion/knowledge/free/dev/software-developer/e2e-testing`
- `faion/knowledge/free/dev/software-developer/error-handling`
- `faion/knowledge/free/dev/software-developer/integration-testing`
- `faion/knowledge/free/dev/software-developer/language-framework-guide`
- `faion/knowledge/free/dev/software-developer/tdd-workflow`
- `faion/knowledge/geek/sdlc-ai/kb-agents-md-context-pyramid`
- `faion/knowledge/geek/sdlc-ai/lint-precommit-floor`
- `faion/knowledge/geek/sdlc-ai/lint-staged-only-not-whole-tree`
- `faion/knowledge/geek/sdlc-ai/mr-graph-vs-diff-reviewer`
- `faion/knowledge/geek/sdlc-ai/task-agent-drafts-spec-before-coding`
- `faion/knowledge/pro/dev/software-developer/api-monitoring-logging`
- `faion/knowledge/pro/dev/software-developer/api-monitoring-metrics`
- `faion/knowledge/solo/dev/automation-tooling/cd-pipelines`
- `faion/knowledge/solo/dev/automation-tooling/continuous-delivery`
- `faion/knowledge/solo/dev/software-architect/architecture-decision-records`
- `faion/knowledge/solo/dev/software-developer/api-documentation`
- `faion/knowledge/solo/dev/software-developer/api-versioning`
- `faion/knowledge/solo/dev/software-developer/contract-first-development`
- `faion/knowledge/solo/dev/software-developer/feature-flags`
- `faion/knowledge/solo/dev/software-developer/trunk-based-development`
- `faion/knowledge/solo/sdd/sdd-planning/task-creation-template-guide`
- `faion/knowledge/solo/sdd/sdd-planning/writing-implementation-plans`
- `faion/knowledge/solo/sdd/sdd/api-first-development`
- `faion/knowledge/solo/sdd/sdd/code-review-cycle`
- `faion/knowledge/solo/sdd/sdd/living-documentation`
- `faion/knowledge/solo/sdd/sdd/mistake-memory`
- `faion/knowledge/solo/sdd/sdd/pattern-memory`
- `faion/knowledge/solo/sdd/sdd/quality-gates-confidence`
- `faion/knowledge/solo/sdd/sdd/reflexion-learning`
- `faion/knowledge/solo/sdd/sdd/task-creation-parallelization`
- `faion/knowledge/solo/sdd/sdd/writing-design-documents`
- `faion/knowledge/solo/sdd/sdd/writing-specifications`
- Related: `greenfield-service-from-scaffold-to-first-production-deploy-8-weeks-p6-product-t`
