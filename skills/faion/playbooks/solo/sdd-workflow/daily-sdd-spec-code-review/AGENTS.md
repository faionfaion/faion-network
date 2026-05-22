---
slug: daily-sdd-spec-code-review
tier: solo
group: sdd-workflow
persona: P1
goal: build-ship
complexity: medium
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: Empty editor at 9am → one feature slice merged to staging by EOD.
content_id: c09d833430cf8b97
methodology_refs:
  - spec-requirements
  - writing-specifications
  - impl-plan-100k-rule
  - impl-plan-task-format
  - api-first-development
  - tdd-workflow
  - error-handling
  - code-review
  - code-review-basics
  - code-review-process
  - code-review-cycle
  - unit-testing
  - cd-basics
  - quality-gates-confidence
---

# Daily SDD spec to vibe-code to review cycle

**Playbook slug:** `daily-sdd-spec-code-review`  
**Tier:** solo  
**Complexity:** medium  
**Persona:** P1 — Solo SaaS Builder

## Intent

Empty editor at 9am → one feature slice merged to staging by EOD.

## Scope

Solo founder ships one feature slice to staging in a single focused day: spec written, code generated against acceptance criteria, self-review pass complete, PR merged, deploy verified. Exit artifact is staging URL with feature live.

### What this playbook covers

This is a structured chain of existing faion methodologies adapted for a single-operator SaaS founder. It assumes no team, no SRE rotation, no co-founder. Every stage ends with an explicit decision gate so the operator can tell whether to advance, iterate, or kill — solo founders drift fastest where stages don't end cleanly.

### Non-goals

- Multi-day epics — split first, then ship daily
- Major refactors — keep day's PR < 500 lines

### Prerequisites

- Spec or rough requirement available at start of day
- CI pipeline configured (cd-basics complete)

## Success criteria

The playbook is done when:
- 1-page spec written with explicit acceptance criteria
- Tests written or generated against acceptance criteria
- Self-review checklist completed
- PR merged to staging with feature flag
- Staging smoke pass within 1h of merge

## Stages

### Stage 1: Spec

**Intent:** Write what 'done' looks like before any code is generated.

**Tasks:**
- Write 1-paragraph intent
- List acceptance criteria
- Define non-goals

**Methodologies in chain:**
- `spec-requirements` → `solo/sdd/sdd-planning/spec-requirements`
- `writing-specifications` → `solo/sdd/sdd/writing-specifications`
- `impl-plan-100k-rule` → `solo/sdd/sdd-planning/impl-plan-100k-rule`
- `impl-plan-task-format` → `solo/sdd/sdd-planning/impl-plan-task-format`

**Outputs:**
- spec.md ≤1 page

**Decision gate:**
> Advance when acceptance criteria are atomic + checkable. Refuse to code with fuzzy spec.

### Stage 2: Generate

**Intent:** AI implements against the spec; founder steers, not types.

**Tasks:**
- Pass spec + repo context to AI
- Generate implementation
- Generate tests against acceptance criteria

**Methodologies in chain:**
- `api-first-development` → `solo/sdd/sdd/api-first-development`
- `tdd-workflow` → `free/dev/software-developer/tdd-workflow`
- `error-handling` → `free/dev/software-developer/error-handling`

**Outputs:**
- Implementation diff
- Test files

**Decision gate:**
> Advance when tests pass locally. Stay if tests fail or diff > 500 lines.

### Stage 3: Review

**Intent:** Self-review like a stranger would.

**Tasks:**
- Run self-review checklist
- Read every line once
- Run linter + typecheck

**Methodologies in chain:**
- `code-review` → `free/dev/code-quality/code-review`
- `code-review-basics` → `free/dev/code-quality/code-review-basics`
- `code-review-process` → `free/dev/code-quality/code-review-process`
- `code-review-cycle` → `solo/sdd/sdd/code-review-cycle`
- `unit-testing` → `free/dev/testing-developer/unit-testing`

**Outputs:**
- Review notes

**Decision gate:**
> Advance when checklist passes. If 3+ items fail, return to Generate.

### Stage 4: Ship

**Intent:** Merge with flag, deploy, verify on staging.

**Tasks:**
- Merge PR
- Deploy via cd-basics pipeline
- Smoke-test on staging URL

**Methodologies in chain:**
- `cd-basics` → `solo/dev/automation-tooling/cd-basics`
- `quality-gates-confidence` → `solo/sdd/sdd/quality-gates-confidence`

**Outputs:**
- Staging URL with feature live

**Decision gate:**
> Required output: feature works on staging URL. If smoke fails, hot-rollback flag.

## Common pitfalls

- Generating code before the spec is acceptance-criteria-clean — produces 90% of the wrong thing
- Skipping self-review because 'tests pass' — tests don't catch design drift

## Quality checklist (self-review)

- Is the spec the agent generated tests against the same spec a human would test against?
- Did I read every line of generated code, or did I just trust the diff?

## Related playbooks

- `ai-pair-coding-loop-solo`
- `deploy-day-staging-to-prod`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).
- **solo-pr-self-review-checklist** (tier `solo`, blocks stage 3) — Review stage needs explicit self-review checklist for one-person PRs
- **daily-ship-rubric** (tier `solo`, blocks stage 4) — Ship stage needs daily-cadence rubric (what counts as 'shipped today')

## CLI usage

```
faion get-content daily-sdd-spec-code-review --format md       # human-readable rendering
faion get-content daily-sdd-spec-code-review --format context  # agent-optimised context bundle
faion get-content daily-sdd-spec-code-review --format json     # raw structured form
```
