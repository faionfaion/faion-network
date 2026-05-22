---
slug: security-review-of-a-new-dependency-or-service-edge
tier: pro
group: role-software-architect
persona: software architect
goal: govern-decide
complexity: medium
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: Done = a new external surface (lib, integration, public endpoint) is reviewed for STRIDE-style threats, secret-handling, authn/z model, and supply-chain provenance; either ships with mitigations +...
content_id: e39247d08fbb0153
methodology_refs:
  - sec-codeql-autofix-on-pr
  - sec-secrets-defense-in-depth
  - sec-trivy-pinned-supply-chain-scan
  - security-architecture
---

# Security review of a new dependency or service edge

**Persona:** software architect · **Tier:** pro · **Complexity:** medium · **Angle:** atomic

## Context

Done = a new external surface (lib, integration, public endpoint) is reviewed for STRIDE-style threats, secret-handling, authn/z model, and supply-chain provenance; either ships with mitigations + owner or is blocked.

This is a atomic-angle playbook. Medium complexity — expect the work to span multiple sessions if medium = deep, a focused interval if medium, and a single sitting if light. The persona is a software architect operating in a solo, team context.

## Outcome

Success is defined by these criteria, all attached as written artifacts before the playbook is considered closed:

- Security review of a new dependency or service edge ships with written success criteria met and evidence attached
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
- `geek/sdlc-ai/sec-codeql-autofix-on-pr` (tier: geek)

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
- `geek/sdlc-ai/sec-secrets-defense-in-depth` (tier: geek)

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
- `geek/sdlc-ai/sec-trivy-pinned-supply-chain-scan` (tier: geek)

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
- `solo/dev/software-architect/security-architecture` (tier: solo)

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
- `geek/sdlc-ai/sec-codeql-autofix-on-pr` (tier: geek)

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
- `geek/sdlc-ai/sec-codeql-autofix-on-pr` (tier: geek)

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

- `sec-codeql-autofix-on-pr` — `faion/knowledge/geek/sdlc-ai/sec-codeql-autofix-on-pr` (tier: geek)
- `sec-secrets-defense-in-depth` — `faion/knowledge/geek/sdlc-ai/sec-secrets-defense-in-depth` (tier: geek)
- `sec-trivy-pinned-supply-chain-scan` — `faion/knowledge/geek/sdlc-ai/sec-trivy-pinned-supply-chain-scan` (tier: geek)
- `security-architecture` — `faion/knowledge/solo/dev/software-architect/security-architecture` (tier: solo)

Gaps — methodologies referenced as future work, blocking promotion from `draft` to `published`:

- `stride-lite-checklist-for-architects` (expected tier: pro)
- `trust-boundary-diff-helper` (expected tier: pro)
