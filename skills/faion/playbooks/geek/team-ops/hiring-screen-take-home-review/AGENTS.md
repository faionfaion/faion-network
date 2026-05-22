---
slug: hiring-screen-take-home-review
tier: geek
group: team-ops
persona: P6
goal: TBD
complexity: medium
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: Candidate take-home / live coding → apples-to-apples rubric score (lint + sec + tests floor identical to team standard).
content_id: 45c6fc1bc9d17e62
methodology_refs:
  - lint-megalinter-polyglot
  - lint-precommit-floor
  - sec-codeql-autofix-on-pr
  - code-review-basics
  - structured-interview-design
  - star-interview-framework
  - star-interview-method
  - interview-methods
---

# Hiring screen / take-home review

**Playbook slug:** `hiring-screen-take-home-review`
**Tier:** geek
**Complexity:** medium
**Persona:** P6 — Product-Dev Team

## Intent

Candidate take-home / live coding → apples-to-apples rubric score (lint + sec + tests floor identical to team standard).

## Scope

A candidate submits a take-home or completes a live coding loop. Reviewer scores against a fixed structured-interview rubric. AI bot runs the candidate's code through the same lint / security / test floors the team uses on its own PRs to make signal apples-to-apples. Bias check is run on rubric scoring before any decision is committed.

### What this playbook covers

Three stages: AI floor, structured rubric, bias check + decision. The chain enforces *identical-bar*: the candidate's code passes (or fails) the same gates as the team's own PRs. Anything else is unfair to both the candidate and the team. STAR notes and bias check are non-negotiable.

### Non-goals

- Sourcing + posting — separate funnel
- Offer + negotiation — out of scope
- Onboarding — see `hire-onboard-product-dev-2-weeks`

### Prerequisites

- Structured interview rubric agreed by team
- Lint / sec / test floor identical to team standard
- Bias-check protocol in place

## Success criteria

The playbook is done when:
- Candidate code run through identical CI floor as internal PRs
- Rubric score with line-item evidence
- Bias-check completed on scoring
- STAR-method interview notes captured
- Hire / no-hire / next-round decision with reasoning

## Stages

### Stage 1: Run candidate code through team floor

**Intent:** AI bot lints + scans + runs tests at the same bar as team PRs.

**Methodologies in chain:**
- `lint-megalinter-polyglot` → `geek/sdlc-ai/lint-megalinter-polyglot`
- `lint-precommit-floor` → `geek/sdlc-ai/lint-precommit-floor`
- `sec-codeql-autofix-on-pr` → `geek/sdlc-ai/sec-codeql-autofix-on-pr`
- `code-review-basics` → `free/dev/code-quality/code-review-basics`

**Decision gate:**
> Advance to human review only after the floor has run. Don't read whitespace.

### Stage 2: Structured interview + rubric scoring

**Intent:** Score with a structured interview rubric; capture STAR evidence.

**Methodologies in chain:**
- `structured-interview-design` → `pro/comms/hr-recruiter/structured-interview-design`
- `star-interview-framework` → `pro/comms/hr-recruiter/star-interview-framework`
- `star-interview-method` → `pro/comms/hr-recruiter/star-interview-method`
- `interview-methods` → `pro/comms/hr-recruiter/interview-methods`

**Decision gate:**
> Advance only when every rubric line has an evidence quote. Vibes-only entries get rewritten.

### Stage 3: Bias check + decision

**Intent:** Bias-check the scoring before committing the verdict.

**Methodologies in chain:**
- `interview-methods` → `pro/comms/hr-recruiter/interview-methods`

**Decision gate:**
> Required: written decision + bias check. Skipping bias check defaults to status-quo team shape.

## Common pitfalls

- Reading the submission before the AI floor has run — surfaces personal preferences before objective signal
- Rubric scoring without evidence quotes — bias creeps in
- Skipping bias check on "obvious" decisions — these are the riskiest
- Different bar for candidates vs internal PRs — invalidates the comparison

## Quality checklist (self-review)

- Did the floor run identically to a team PR?
- Can each rubric score be traced to a quote / artifact?
- Did the bias check actually look for patterns, not check a box?

## Related playbooks

- `hire-onboard-product-dev-2-weeks`
- `hire-to-productive-60-days-in-house`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).
- **take-home-rubric-template** (tier `geek`, blocks stage 2) — Structured-interview stage needs a take-home rubric template tuned for product-dev hiring
- **ai-pre-screen-bias-guardrails** (tier `geek`, blocks stage 3) — Bias-check stage needs explicit AI guardrails so screening doesn't amplify training-data bias

## CLI usage

```
faion get-content hiring-screen-take-home-review --format md       # human-readable rendering
faion get-content hiring-screen-take-home-review --format context  # agent-optimised context bundle
faion get-content hiring-screen-take-home-review --format json     # raw structured form
```
