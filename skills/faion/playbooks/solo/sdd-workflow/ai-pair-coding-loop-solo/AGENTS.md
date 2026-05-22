---
slug: ai-pair-coding-loop-solo
tier: solo
group: sdd-workflow
persona: P1
goal: TBD
complexity: deep
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: AI-implemented feature with risk of vibe-coded breakage → repeatable per-feature spec→AI→review→ship loop without quality regression.
content_id: bac3f82f77eeae4f
methodology_refs:
  - spec-requirements
  - writing-specifications
  - feature-flags-rollout-targeting
  - tdd-workflow
  - code-review-basics
  - code-review-cycle
  - task-creation-parallelization
---

# AI-pair coding loop for solo SaaS

**Playbook slug:** `ai-pair-coding-loop-solo`  
**Tier:** solo  
**Complexity:** deep  
**Persona:** P1 — Solo SaaS Builder

## Intent

AI-implemented feature with risk of vibe-coded breakage → repeatable per-feature spec→AI→review→ship loop without quality regression.

## Scope

Solo founder runs a repeatable feature loop: clean spec → AI implements → strict diff review → tests + shipping. The loop does NOT degrade into vibe-coded breakage even after weeks of usage. Exit artifact is a daily-usable workflow that another founder could follow.

### What this playbook covers

This is a structured chain of existing faion methodologies adapted for a single-operator SaaS founder. It assumes no team, no SRE rotation, no co-founder. Every stage ends with an explicit decision gate so the operator can tell whether to advance, iterate, or kill — solo founders drift fastest where stages don't end cleanly.

### Non-goals

- Multi-agent orchestration — single AI pair only here
- Auto-deploy from AI — human gates remain

### Prerequisites

- AI coding tool live (Claude Code, Cursor, or similar)
- Spec discipline in place (writing-specifications complete)

## Success criteria

The playbook is done when:
- Spec written before any AI prompt issued
- Context window curated: only relevant files passed
- Diff size kept <500 lines per AI iteration
- Tests generated AND validated against spec (not just 'passes')
- Self-code-review protocol followed pre-merge

## Stages

### Stage 1: Spec

**Intent:** Acceptance criteria, non-goals, file targets — before any AI prompt.

**Tasks:**
- Write spec (criteria + non-goals)
- List target files
- Write success test cases

**Methodologies in chain:**
- `spec-requirements` → `solo/sdd/sdd-planning/spec-requirements`
- `writing-specifications` → `solo/sdd/sdd-planning/writing-specifications`

**Outputs:**
- spec.md ready

**Decision gate:**
> Advance when criteria are atomic + checkable. Refuse to prompt AI with fuzzy spec.

### Stage 2: Curate context

**Intent:** Pass only what the AI needs. No giant codebase dumps.

**Tasks:**
- List files the AI must see
- Strip unrelated context
- Add memory / patterns relevant to feature

**Methodologies in chain:**
- (no resolved methodologies — see gaps below)

**Outputs:**
- Context bundle

**Decision gate:**
> Advance when context fits the model's window with headroom. Refuse 'just include everything'.

### Stage 3: Prompt + iterate

**Intent:** AI implements; founder steers. Small diffs only.

**Tasks:**
- Issue first prompt with spec + context
- Limit diff to <500 lines per iteration
- Iterate with explicit feedback

**Methodologies in chain:**
- `feature-flags-rollout-targeting` → `solo/dev/automation-tooling/feature-flags-rollout-targeting`

**Outputs:**
- Implementation diff

**Decision gate:**
> Advance when feature works locally. Stay if AI produces unfocused output — re-prompt with sharper spec.

### Stage 4: Validate tests

**Intent:** Generated tests must test the spec — not the implementation.

**Tasks:**
- Read every test
- Verify each test matches an acceptance criterion
- Add missing cases

**Methodologies in chain:**
- `tdd-workflow` → `free/dev/software-developer/tdd-workflow`

**Outputs:**
- Validated test files

**Decision gate:**
> Advance when test↔criterion mapping is 1:1. Refuse 'tests pass' without coverage check.

### Stage 5: Self-review

**Intent:** Read the AI's diff like a stranger would.

**Tasks:**
- Run self-code-review protocol
- Check for known anti-patterns
- Sign off OR push back

**Methodologies in chain:**
- `code-review-basics` → `free/dev/code-quality/code-review-basics`
- `code-review-cycle` → `solo/sdd/sdd/code-review-cycle`
- `task-creation-parallelization` → `solo/sdd/sdd/task-creation-parallelization`

**Outputs:**
- Reviewed PR

**Decision gate:**
> Required output: signed self-review. Refuse to merge unread AI diffs.

## Common pitfalls

- Skipping spec because 'AI will figure it out' — produces wrong feature fast
- Merging large AI diffs unread — accumulates quiet breakage

## Quality checklist (self-review)

- Did the AI test the spec, or test what it happened to implement?
- Could I roll this PR back in one revert, or did I cram 5 features into one?

## Related playbooks

- `daily-sdd-spec-code-review`
- `deploy-day-staging-to-prod`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).
- **ai-pair-coding-prompt-patterns** (tier `solo`, blocks stage 3) — Prompt+iterate stage needs canonical prompt patterns for solo SaaS
- **context-window-curation-for-coding-agents** (tier `solo`, blocks stage 2) — Curate-context stage needs concrete curation rules
- **ai-diff-size-discipline** (tier `solo`, blocks stage 3) — Prompt+iterate stage needs explicit rules to keep diffs small
- **ai-generated-test-validation** (tier `solo`, blocks stage 4) — Validate-tests stage needs protocol to distinguish 'tests pass' from 'tests test the spec'
- **solo-self-code-review-protocol** (tier `solo`, blocks stage 5) — Self-review stage needs explicit one-person review protocol

## CLI usage

```
faion get-content ai-pair-coding-loop-solo --format md       # human-readable rendering
faion get-content ai-pair-coding-loop-solo --format context  # agent-optimised context bundle
faion get-content ai-pair-coding-loop-solo --format json     # raw structured form
```
