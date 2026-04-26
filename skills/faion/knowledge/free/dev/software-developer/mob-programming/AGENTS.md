# Mob Programming

## Summary

A team practice where all members work together on one task at one machine: a rotating Driver types only what the Navigator(s) dictate, and ideas must pass through someone else's hands before reaching the keyboard. Strong-style navigation, strict 5-10 minute rotation, and a written session goal are the three load-bearing constraints.

## Why

Mobs eliminate review-after-the-fact delays, knowledge silos, and unequal context distribution. Cycle time drops because decisions are made in real-time with full team context. The practice only works when rotation discipline is maintained — without it, drivers fatigue and navigators disengage, collapsing into a lecture with one person coding.

## When To Use

- High-stakes changes requiring multiple specialists simultaneously (payment flow, schema migration, security refactor).
- Onboarding: new engineer navigates while the team drives — knowledge transfers in hours.
- "Impossible" production bugs requiring frontend + backend + ops context simultaneously.
- Killing a knowledge silo when the only expert is leaving.
- Cross-team API contract design where decisions must stick.
- Spreading a new technique (TDD, hexagonal arch) across the team via kata.

## When NOT To Use

- Routine CRUD, typo fixes, dependency bumps — overhead exceeds benefit.
- Async teams with >3 time zones — coordination cost exceeds knowledge gain.
- Solo founder or two-person team — that is pairing, not mobbing.
- When >50% of time is spent waiting on builds or external APIs.
- Teams that have never paired — start with pairing for 2-4 weeks first.
- Tasks the team genuinely needs to parallelize to hit a deadline.

## Content

| File | What's inside |
|------|---------------|
| `content/01-rules.xml` | Strong-style navigation, rotation rules, session goal requirement, break cadence |
| `content/02-patterns.xml` | TDD mob, learning mob, bug-hunt mob, randori; physical and remote setup; disagreement resolution |
| `content/03-antipatterns.xml` | Tourist mob, expert dominance, no rotation, mobbing everything, no retrospective |

## Templates

| File | Purpose |
|------|---------|
| `templates/mob-session.sh` | Session bootstrapper: creates WIP branch, log file, draft PR, rotation bell |
