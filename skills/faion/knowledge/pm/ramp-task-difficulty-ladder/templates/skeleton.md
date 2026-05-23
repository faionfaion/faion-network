<!--
purpose: Canonical ramp-task difficulty ladder skeleton — practitioners fill, never invent sections.
consumes: header.yaml frontmatter + backlog of candidate ramp tickets.
produces: A versioned, owned, evidence-anchored ladder spec.
depends-on: ../scripts/validate-ramp-task-difficulty-ladder.py.
token-budget-impact: ~800 tokens when filled.
-->

---
version: "1.0.0"
owner: "tech-lead:<person>"
last_reviewed: "2026-05-22"
trigger: "hire-signed"
evidence_root: "onboarding/"
review_cadence: "quarterly"
---

# Ramp Task Difficulty Ladder — <team-name>

## Trigger

<event/threshold/schedule that fires this ladder; e.g. "new dev start-date T-7">

## Ladder

| Rung | Ticket pattern | Expected duration | Buddy support | Evidence link |
|------|----------------|-------------------|---------------|---------------|
| 1 (read-only) | docs typo fix, dependency bump | < 1 day | full pairing | <PR / ticket> |
| 2 (single-file) | rename function, add log line | 1-2 days | pair on PR | <PR / ticket> |
| 3 (single-module) | new endpoint behind feature flag | 2-3 days | review on PR | <PR / ticket> |
| 4 (cross-module) | small refactor across 2 modules | 3-5 days | review on design | <PR / ticket> |
| 5 (feature slice) | end-to-end small feature | 5-10 days | check-in 2×/week | <PR / ticket> |

## Owner

<role:person>

## Outcome review

- Last run: <ISO date>
- Next due: <ISO date>
- Outcomes measured: <onboarding completion rate, time-to-first-PR, retention>

## Decisions / Actions / Next review

- <decision 1>
- <action 1, owner, deadline>
- Next review: <ISO date>
