# Architecture-as-code repository — continuous maintenance with monthly review

**Persona:** software architect · **Tier:** geek · **Complexity:** medium · **Angle:** global

## Context

Treat the architecture itself as a versioned artifact. Done = the architecture repo is the single source of truth for ADRs, C4 models, fitness functions, and runbooks, kept current via monthly cadence and AI-assisted reviewers; design drift is caught before it lands.

This is a global-angle playbook. Medium complexity — expect the work to span multiple sessions if medium = deep, a focused interval if medium, and a single sitting if light. The persona is a software architect operating in a solo, team context.

## Outcome

Success is defined by these criteria, all attached as written artifacts before the playbook is considered closed:

- Architecture-as-code repository — continuous maintenance with monthly review ships with written success criteria met and evidence attached
- Baseline → post-change metric delta recorded against the relevant quality attribute
- Rollback path rehearsed at least once and documented in the runbook
- Decision doc (continue / iterate / revert) signed off by named owner

## Steps

Walk the stages in order. Do not advance until each stage's decision gate is met in writing.

### Step 1 — Frame

**Intent.** Name the problem in writing and set explicit success criteria.

**Tasks**
- Write a one-paragraph problem statement tied to a quality attribute or user outcome
- List concrete success criteria (measurable, observable, time-bounded)
- Identify the smallest credible scope that still moves the needle

**Outputs**
- Problem brief
- Success-criteria list
- Scope boundary

**Backed by methodology**
- `geek/sdd/sdd-planning/ai-assisted-specification-writing` (tier: geek)
- `geek/sdlc-ai/lint-megalinter-polyglot` (tier: geek)
- `solo/dev/software-architect/c4-model` (tier: solo)
- `solo/sdd/sdd/writing-design-documents` (tier: solo)

### Step 2 — Assess

**Intent.** Inventory current state vs target with evidence, not opinion.

**Tasks**
- Run a structured assessment of the affected system (code, tests, docs, ops surface)
- Capture baseline metrics that the work will need to beat
- List the top 5 risks and one mitigation per risk

**Outputs**
- Current-state inventory
- Baseline metrics
- Risk register

**Backed by methodology**
- `geek/sdd/sdd/ai-assisted-specification-writing` (tier: geek)
- `geek/sdlc-ai/lint-precommit-floor` (tier: geek)
- `solo/sdd/sdd/living-documentation` (tier: solo)
- `solo/sdd/sdd/writing-specifications` (tier: solo)

### Step 3 — Plan

**Intent.** Decompose into a sequenced backlog with explicit decision points.

**Tasks**
- Break the work into tasks of ≤1 day each, with dependencies named
- Mark reversible vs irreversible (one-way-door) decisions
- Define rollback / kill conditions for each major step

**Outputs**
- Task plan
- Decision log skeleton
- Rollback playbook

**Backed by methodology**
- `geek/sdlc-ai/gov-conventional-commits-enforced` (tier: geek)
- `geek/sdlc-ai/mr-codemod-refactor-agent` (tier: geek)
- `solo/sdd/sdd/mistake-memory` (tier: solo)
- `solo/sdd/sdd/yaml-frontmatter` (tier: solo)

### Step 4 — Execute

**Intent.** Ship the change behind safe deployment controls.

**Tasks**
- Implement the plan in small, individually shippable steps
- Keep all changes behind feature flags or branch-by-abstraction where reversible
- Update tests + docs in the same change set, never as a follow-up

**Outputs**
- Shipped change set
- Updated tests + docs

**Backed by methodology**
- `geek/sdlc-ai/kb-agents-md-context-pyramid` (tier: geek)
- `geek/sdlc-ai/mr-graph-vs-diff-reviewer` (tier: geek)
- `solo/sdd/sdd/pattern-memory` (tier: solo)

### Step 5 — Verify

**Intent.** Prove the change cleared the success criteria with evidence.

**Tasks**
- Run targeted tests + smoke on the most-trafficked surfaces
- Compare post-change metrics against the baseline captured earlier
- Capture user / operator feedback within the first 48 hours

**Outputs**
- Verification report
- Metric delta vs baseline

**Backed by methodology**
- `geek/sdlc-ai/kb-codebase-rag-symbol-chunked` (tier: geek)
- `geek/sdlc-ai/task-spec-kit-three-step` (tier: geek)
- `solo/sdd/sdd/reflexion-learning` (tier: solo)

### Step 6 — Close

**Intent.** Lock in the gain: documentation, learnings, and a single decision artifact.

**Tasks**
- Write the decision / outcome doc (continue / iterate / revert) with evidence trail
- Update ADRs, runbooks, and pattern memory with what changed
- Schedule the next review checkpoint or archive the workstream

**Outputs**
- Decision doc
- Updated ADR / runbook / memory entry

**Backed by methodology**
- `geek/sdlc-ai/kb-versioned-agent-memory-files` (tier: geek)
- `solo/dev/software-architect/architecture-decision-records` (tier: solo)
- `solo/sdd/sdd/sdd-workflow-overview` (tier: solo)

## Decision points

- **After Step 1 (Frame).** Advance only after a peer can restate the problem in their own words and agree the criteria are testable.
- **After Step 2 (Assess).** Advance only when baselines are recorded and risks have owners.
- **After Step 3 (Plan).** Advance only when every task has a definition-of-done and the plan fits on one page.
- **After Step 4 (Execute).** Advance only when CI is green, the change is observable in staging, and rollback was rehearsed at least once.
- **After Step 5 (Verify).** Advance only when metrics meet the criteria and no regression alerts are open.
- **After Step 6 (Close).** Done when the decision doc is single-link shareable and the team can name the next checkpoint.

If any gate fails: stop, re-plan, and either re-enter the previous step or kill the workstream with a written rationale.

## References

Methodologies cited in this playbook (resolve via `faion get-content <slug>`):

- `ai-assisted-specification-writing` — `faion/knowledge/geek/sdd/sdd-planning/ai-assisted-specification-writing` (tier: geek)
- `ai-assisted-specification-writing` — `faion/knowledge/geek/sdd/sdd/ai-assisted-specification-writing` (tier: geek)
- `gov-conventional-commits-enforced` — `faion/knowledge/geek/sdlc-ai/gov-conventional-commits-enforced` (tier: geek)
- `kb-agents-md-context-pyramid` — `faion/knowledge/geek/sdlc-ai/kb-agents-md-context-pyramid` (tier: geek)
- `kb-codebase-rag-symbol-chunked` — `faion/knowledge/geek/sdlc-ai/kb-codebase-rag-symbol-chunked` (tier: geek)
- `kb-versioned-agent-memory-files` — `faion/knowledge/geek/sdlc-ai/kb-versioned-agent-memory-files` (tier: geek)
- `lint-megalinter-polyglot` — `faion/knowledge/geek/sdlc-ai/lint-megalinter-polyglot` (tier: geek)
- `lint-precommit-floor` — `faion/knowledge/geek/sdlc-ai/lint-precommit-floor` (tier: geek)
- `mr-codemod-refactor-agent` — `faion/knowledge/geek/sdlc-ai/mr-codemod-refactor-agent` (tier: geek)
- `mr-graph-vs-diff-reviewer` — `faion/knowledge/geek/sdlc-ai/mr-graph-vs-diff-reviewer` (tier: geek)
- `task-spec-kit-three-step` — `faion/knowledge/geek/sdlc-ai/task-spec-kit-three-step` (tier: geek)
- `architecture-decision-records` — `faion/knowledge/solo/dev/software-architect/architecture-decision-records` (tier: solo)
- `c4-model` — `faion/knowledge/solo/dev/software-architect/c4-model` (tier: solo)
- `living-documentation` — `faion/knowledge/solo/sdd/sdd/living-documentation` (tier: solo)
- `mistake-memory` — `faion/knowledge/solo/sdd/sdd/mistake-memory` (tier: solo)
- `pattern-memory` — `faion/knowledge/solo/sdd/sdd/pattern-memory` (tier: solo)
- `reflexion-learning` — `faion/knowledge/solo/sdd/sdd/reflexion-learning` (tier: solo)
- `sdd-workflow-overview` — `faion/knowledge/solo/sdd/sdd/sdd-workflow-overview` (tier: solo)
- `writing-design-documents` — `faion/knowledge/solo/sdd/sdd/writing-design-documents` (tier: solo)
- `writing-specifications` — `faion/knowledge/solo/sdd/sdd/writing-specifications` (tier: solo)
- `yaml-frontmatter` — `faion/knowledge/solo/sdd/sdd/yaml-frontmatter` (tier: solo)

Gaps — methodologies referenced as future work, blocking promotion from `draft` to `published`:

- `architecture-repo-scaffolding-template` (expected tier: geek)
- `fitness-function-pattern-pack` (expected tier: geek)
- `adr-decay-detector-agent` (expected tier: geek)
