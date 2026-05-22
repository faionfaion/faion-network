---
slug: pair-programming
tier: free
group: dev
domain: dev
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-net]
summary: Produces a pair-programming session protocol (chosen mode, role rotation cadence, Strong-Style rules when AI is navigator, Pomodoro pacing, silent-retro session.md) so two-person work compounds rather than splits.
content_id: "320bd3547e385721"
complexity: light
produces: checklist
est_tokens: 2700
tags: [pairing, programming, ai, strong-style, pomodoro]
---
# Pair Programming (incl. AI-navigator)

## Summary

**One-sentence:** Produces a pair-programming session protocol (chosen mode, role rotation cadence, Strong-Style rules when AI is navigator, Pomodoro pacing, silent-retro session.md) so two-person work compounds rather than splits.

**One-paragraph:** Two programmers share one workstation: Driver writes; Navigator reviews and thinks strategically. Four modes: classic Driver-Navigator, Ping-Pong (TDD), Strong-Style ("idea must pass through the other person's hands"), and Tour-Guide (expert narrates to newcomer). With an AI agent, the human is always physically the driver; the agent emits one bounded instruction per turn, explains why, waits for result. Restate Strong-Style every ~10 turns or the AI reverts to full-file dumps. Pomodoro: 25/5; switch roles at breaks; max 4-6 hours/day. End with silent retro committed to session.md.

**Ефективно для:** onboarding, hard problems, AI-assisted coding where the human stays in control, knowledge transfer, code reviews via TDD ping-pong.

## Applies If (ALL must hold)

- Two participants (one may be an AI agent).
- Task benefits from continuous review (complex, ambiguous, learning).
- Both can sustain 2-6 hours of focused pairing.
- A shared editor or screen.

## Skip If (ANY kills it)

- Routine parallelisable work — split tasks instead.
- One participant is purely passive — pair becomes solo + spectator.
- Time pressure where independent execution is faster.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Session mode | classic / ping-pong / strong-style / tour-guide | session lead |
| Roster | 2 names (human, human or AI) | session lead |
| session.md | Markdown file | repo / scratch |
| Pomodoro app | timer | shared |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[mob-programming]]` | 3+ person extension; preconditions overlap. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 rules: Strong-style, AI-navigator constraints, restate every 10 turns, fixed mode per session, Pomodoro, short prompts, silent retro | ~700 |
| `content/02-output-contract.xml` | essential | Session-protocol JSON Schema | ~500 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns: passive navigator, AI emitting full files, mode-switching mid-session | ~500 |
| `content/06-decision-tree.xml` | essential | Root: "Is this complex work suitable for continuous review?" | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| AI as navigator | opus | One instruction per turn — needs solid reasoning to pick. |
| session.md retro | sonnet | Summarisation. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pair-session.sh` | Pomodoro timer + role-switch reminder script. |
| `templates/strong-style-prompt.txt` | Prompt setting Strong-Style rules for an AI navigator. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-pair-programming.py` | Validates protocol JSON has mode + roster + retro plan. | Pre-session. |

## Related

- parent skill: `free/dev/software-developer/`
- `[[mob-programming]]` — 3+ participant variant

## Decision tree

The decision tree at `content/06-decision-tree.xml` checks: two participants, complex/learning task, mode chosen.
