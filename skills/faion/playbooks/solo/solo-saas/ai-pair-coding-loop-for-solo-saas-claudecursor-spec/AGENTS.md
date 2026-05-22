---
slug: ai-pair-coding-loop-for-solo-saas-claudecursor-spec
tier: solo
group: solo-saas
persona: P1
goal: build-ship
complexity: deep
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: Solo founder ships a feature in a clean spec → AI-implement → review → ship cycle that does NOT degrade into vibe-coded breakage.
content_id: ba7828a496b3c5e1
methodology_refs:
  - code-review-basics
  - tdd-workflow
  - feature-flags-rollout-targeting
  - spec-requirements
  - writing-specifications
  - code-review-cycle
  - task-creation-parallelization
---

# AI-pair coding loop for solo SaaS (Claude/Cursor + Spec)

## Intent

Solo founder ships a feature in a clean spec → AI-implement → review → ship cycle that does NOT degrade into vibe-coded breakage.

## Scope

Solo founder ships a feature in a clean spec → AI-implement → review → ship cycle that does NOT degrade into vibe-coded breakage. Output: a repeatable per-feature workflow Alex runs every day.

## Stages

### 1. Spec the slice

Spec is the brief - no agent runs without it.

Tasks:
- Write the spec with concrete AC
- Pin the relevant context paths
- Confirm scope fits the agents context window

Outputs:
- slice-spec.md
- Context path list
- Estimated token budget

Decision gate: Advance only when scope <=100k tokens of context.

### 2. Context curation

Feed only the files the agent actually needs.

Tasks:
- List the files in scope (no folder dumps)
- Strip irrelevant tests, fixtures, deps
- Add the patterns/mistake memory snippet

Outputs:
- Curated context manifest
- Token estimate vs budget
- Memory snippets

Decision gate: Advance only when curated context is below the agents safe limit.

### 3. Diff-size discipline

Cap the agent diff so you can still review it.

Tasks:
- Set a max diff size (e.g. <=400 lines)
- Ask for one logical change per pass
- Reject and re-prompt if diff balloons

Outputs:
- Diff size rule
- Re-prompt log
- Final diff under cap

Decision gate: Advance only when diff is under cap AND focused on one concern.

### 4. TDD pass

Tests first, code second - even with the agent.

Tasks:
- Ask the agent to generate failing tests first
- Verify tests map to AC
- Have agent generate the implementation against tests

Outputs:
- Failing test commit
- Implementation commit
- Green test run

Decision gate: Advance only when tests cover every AC and pass.

### 5. Self-code review

Solo PR review using a written rubric.

Tasks:
- Walk the self-code-review rubric
- Flag any agent-ese code (over-abstraction, unused helpers)
- Refactor in place if needed

Outputs:
- Review checklist
- Refactor notes
- Final commit

Decision gate: Advance only when no rubric item is red.

### 6. Validate AI-generated tests

Confirm the tests actually test something.

Tasks:
- Mutate the implementation to force a failure
- Confirm at least one test catches it
- Strip any tautological tests

Outputs:
- Mutation pass log
- Stripped tautological tests
- Coverage delta

Decision gate: Advance only when mutation catches the regression.

### 7. Ship + flag

Ship the slice safely with rollback ready.

Tasks:
- Merge to main behind a flag
- Deploy to staging then prod
- Verify AC on prod with the flag rolled out

Outputs:
- Merged PR
- Staging + prod deploys
- AC verification on prod

Decision gate: Advance only when production AC pass for the rollout cohort.

### 8. Lessons to memory

Lock the agent-loop lessons so they compound.

Tasks:
- Update agent-prompt patterns with what worked
- Update mistake memory with traps
- Add a context-curation note for next time

Outputs:
- Pattern memory delta
- Mistake memory delta
- Context curation note

Decision gate: Cycle closes when memories are committed.

### 9. Re-prime tomorrow

Set up the next slice while context is hot.

Tasks:
- Identify the next slice
- Pre-write the next spec stub
- Stage the context manifest for tomorrow

Outputs:
- Tomorrows slice name
- Spec stub
- Staged manifest

Decision gate: Cycle closes when tomorrows first 20 minutes are pre-loaded.

## Common pitfalls

- Skipping the decision-gate write-up to keep moving - closes the loop with vibes, not evidence.
- Treating each stages outputs as optional - every output is a gate input for the next stage.
- Letting one bad week stretch a fixed-cadence ritual into a quarterly one.

## Quality checklist

- Every stage has at least one referenced methodology that resolves under `knowledge/`.
- Every output is a real artefact, not a feeling.
- The final decision is a written commitment, not we will see.
