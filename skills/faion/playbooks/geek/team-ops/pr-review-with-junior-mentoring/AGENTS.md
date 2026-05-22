---
slug: pr-review-with-junior-mentoring
tier: geek
group: team-ops
persona: P6
goal: operate-ritual
complexity: medium
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: Routine PR review → paired senior+junior session where AI handles the mechanical floor and human time goes to design + judgment.
content_id: 2310c60bf79d9614
methodology_refs:
  - lint-precommit-floor
  - lint-autofix-vs-flag-decision-rule
  - lint-staged-only-not-whole-tree
  - sec-codeql-autofix-on-pr
  - sec-secrets-defense-in-depth
  - code-review
  - code-review-process
  - code-review-basics
  - pair-programming
  - mr-graph-vs-diff-reviewer
  - code-review-cycle
  - quality-gates-confidence
  - pattern-memory
  - mistake-memory
  - reflexion-learning
---

# PR review with junior present (mentoring loop)

**Playbook slug:** `pr-review-with-junior-mentoring`
**Tier:** geek
**Complexity:** medium
**Persona:** P6 — Product-Dev Team

## Intent

Routine PR review → paired senior+junior session where AI handles the mechanical floor and human time goes to design + judgment.

## Scope

Senior + junior pair on a single PR review. AI bot pre-runs lint / security / test-coverage on the diff so the human time is freed for design, naming, boundaries, and judgment. Senior narrates *why* on each comment. Junior leaves with a written next-PR checklist captured from the session. Mistakes go to mistake-memory; patterns to pattern-memory.

### What this playbook covers

Three stages: clear mechanical noise with AI, hold a narrated paired review, capture the lesson durably. The chain treats mentoring as the goal — not throughput. A normal-speed review with a junior watching is theatre; this playbook trades speed for transfer. The retro at the end ensures the senior also learns about their own mentoring.

### Non-goals

- Speeding up reviews — this is intentionally slower than a normal review
- Hiring screen reviews — see `hiring-screen-take-home-review`
- Architectural review — see `weekly-architectural-review`

### Prerequisites

- Junior has read the team's code-review-basics methodology
- AI bot pre-runs lint + security + coverage on PRs
- Pre-commit + autofix wired so trivial issues never reach review

## Success criteria

The playbook is done when:
- PR reviewed end-to-end with senior narrating reasoning
- Junior next-PR checklist written down (≥5 concrete items)
- Pattern-memory updated with reusable insights
- Mistake-memory updated where junior's first instincts were wrong
- Pair-programming retro logged

## Stages

### Stage 1: Pre-review — AI floor

**Intent:** AI clears the mechanical noise; humans review what's left.

**Methodologies in chain:**
- `lint-precommit-floor` → `geek/sdlc-ai/lint-precommit-floor`
- `lint-autofix-vs-flag-decision-rule` → `geek/sdlc-ai/lint-autofix-vs-flag-decision-rule`
- `lint-staged-only-not-whole-tree` → `geek/sdlc-ai/lint-staged-only-not-whole-tree`
- `sec-codeql-autofix-on-pr` → `geek/sdlc-ai/sec-codeql-autofix-on-pr`
- `sec-secrets-defense-in-depth` → `geek/sdlc-ai/sec-secrets-defense-in-depth`

**Decision gate:**
> Advance only after pre-commit + CodeQL autofix have run. Senior should not be reading whitespace.

### Stage 2: Paired review session

**Intent:** Senior narrates; junior asks; reviewer-graph-vs-diff perspective applied.

**Methodologies in chain:**
- `code-review` → `free/dev/code-quality/code-review`
- `code-review-process` → `free/dev/code-quality/code-review-process`
- `code-review-basics` → `free/dev/code-quality/code-review-basics`
- `pair-programming` → `free/dev/code-quality/pair-programming`
- `mr-graph-vs-diff-reviewer` → `geek/sdlc-ai/mr-graph-vs-diff-reviewer`
- `code-review-cycle` → `solo/sdd/sdd/code-review-cycle`
- `quality-gates-confidence` → `solo/sdd/sdd/quality-gates-confidence`

**Decision gate:**
> Advance once junior can summarise the senior's reasoning back unaided. If not, slow down — the session failed its primary goal.

### Stage 3: Capture + close

**Intent:** Convert the session into durable assets: junior's checklist + team memory.

**Methodologies in chain:**
- `pattern-memory` → `solo/sdd/sdd/pattern-memory`
- `mistake-memory` → `solo/sdd/sdd/mistake-memory`
- `reflexion-learning` → `solo/sdd/sdd/reflexion-learning`

**Decision gate:**
> Required output: written checklist. Verbal mentoring without artefact = lesson lost by next PR.

## Common pitfalls

- Senior overrides without explanation — junior learns compliance, not judgment
- AI noise not pre-cleared — human time burned on whitespace
- No artefact at the end — junior's next PR repeats the same misses
- Treating the session as a normal-speed review — defeats the mentoring goal

## Quality checklist (self-review)

- Can the junior write down what the senior taught them?
- Did at least one comment include "because X, not Y" reasoning?
- Did anything from the session end up in pattern-memory?

## Related playbooks

- `weekly-architectural-review`
- `biweekly-retro-mistake-memory`
- `hire-onboard-product-dev-2-weeks`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).
- **pr-mentoring-session-protocol** (tier `geek`, blocks stage 2) — Paired-review stage needs a written mentoring-session protocol with explicit narration prompts
- **junior-next-pr-checklist-template** (tier `geek`, blocks stage 3) — Capture stage needs a checklist template the junior can fill in during the session

## CLI usage

```
faion get-content pr-review-with-junior-mentoring --format md       # human-readable rendering
faion get-content pr-review-with-junior-mentoring --format context  # agent-optimised context bundle
faion get-content pr-review-with-junior-mentoring --format json     # raw structured form
```
