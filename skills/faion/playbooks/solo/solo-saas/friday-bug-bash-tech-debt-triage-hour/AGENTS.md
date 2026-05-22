---
slug: friday-bug-bash-tech-debt-triage-hour
tier: solo
group: solo-saas
persona: P1
goal: operate-ritual
complexity: light
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "Inbox-zero on bug tracker: Sentry / GitHub issues grouped, severity-tagged, top-3 fixed or queued, debt list updated with one decision per item (fix now / accept / kill)."
content_id: 92bbf9cbbf1098d4
methodology_refs:
  - refactoring-patterns
  - technical-debt
  - tech-debt-basics
  - backlog-management
  - logging-patterns
  - feedback-management
  - tech-debt-management
  - technical-debt-management
  - feature-flags
  - architecture-decision-records
---

# Friday bug-bash & tech-debt triage hour

## Intent

Inbox-zero on bug tracker: Sentry / GitHub issues grouped, severity-tagged, top-3 fixed or queued, debt list updated with one decision per item (fix now / accept / kill).

## Scope

Inbox-zero on bug tracker: Sentry / GitHub issues grouped, severity-tagged, top-3 fixed or queued, debt list updated with one decision per item (fix now / accept / kill).

## Stages

### 1. Pull the open list

Get every bug + debt item in one view.

Tasks:
- Pull Sentry top-N issues by event count
- Pull GitHub issues tagged bug/debt
- Group duplicates and stale dups

Outputs:
- Unified bug+debt list
- Duplicate map
- Stale-cull list

Decision gate: Advance only when the list fits on one screen.

### 2. Severity + cost tag

Rate each item by user pain and fix cost.

Tasks:
- Tag severity (S0..S3) per item
- Estimate fix cost in tokens or hours of focus
- Mark the revenue-relevance per item

Outputs:
- Severity tags
- Cost estimates
- Revenue-relevance tags

Decision gate: Advance only when every item has all three tags.

### 3. Top-3 fix or queue

Fix top-3 today OR queue them with a date.

Tasks:
- Pick top-3 by severity x revenue
- Fix in-place if <=30 minutes each
- Queue the rest with a date and owner (always you)

Outputs:
- 3 fixes shipped OR queued
- Updated tracker
- Todays fix commits

Decision gate: Advance only when each top-3 has a status: fixed / queued / accepted.

### 4. Debt decision pass

One decision per debt item: fix now, accept, or kill.

Tasks:
- Walk the remaining debt list
- Stamp each item: fix-now / accept / kill
- Write a one-line rationale per kill

Outputs:
- Debt decision log
- Killed-debt rationales
- Accept-debt notes

Decision gate: Advance only when no debt item is left in to-think-about.

### 5. Update memories + signal

Stop the bug from coming back.

Tasks:
- Add the worst pattern to mistake memory
- Wire one new monitor/alert if the bug came from a blind spot
- Close the ritual with a tracker snapshot

Outputs:
- Mistake memory delta
- New alert config
- Closing tracker snapshot

Decision gate: Cycle closes when mistakes are written and snapshot is saved.

## Common pitfalls

- Skipping the decision-gate write-up to keep moving - closes the loop with vibes, not evidence.
- Treating each stages outputs as optional - every output is a gate input for the next stage.
- Letting one bad week stretch a fixed-cadence ritual into a quarterly one.

## Quality checklist

- Every stage has at least one referenced methodology that resolves under `knowledge/`.
- Every output is a real artefact, not a feeling.
- The final decision is a written commitment, not we will see.
