# Mob Programming

## Summary

**One-sentence:** Produces a mob-programming session checklist (Driver/Navigator strong-style, 5-10 min rotation, written Done definition, parking lot, retrospective) so the whole team learns one task at one machine without knowledge silos.

**One-paragraph:** Whole team at one machine: rotating Driver types only what the Navigator dictates ("ideas must pass through someone else's hands before reaching the keyboard"). Strong-style navigation, strict 5-10 minute rotation, written single-sentence Done definition before the session, 75-90 minute breaks, time-boxed disagreements (2 min then try one), parking lot for off-topic items, written retrospective after every session. Eliminates handoff delays and knowledge silos by making the team produce together.

**Ефективно для:** onboarding new hires, untangling complex legacy code, decisions that affect multiple owners, knowledge transfer when a senior is leaving, teaching a new pattern by doing it together.

## Applies If (ALL must hold)

- 3-6 people can dedicate a full session to one task.
- One shared workstation (physical room) or one shared screen (remote).
- Team accepts strict 5-10 minute rotation and strong-style navigation.
- Task has a single-sentence Done definition writable before start.

## Skip If (ANY kills it)

- Independent parallelisable work — split tasks instead, save mob for unknowns.
- Routine work the team has done many times — no learning payoff.
- Group >6 — boredom; consider Ensemble or splitting into mobs.
- Cannot articulate Done before start — clarify scope first.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Done definition | one sentence | session lead / PM |
| Roster + rotation order | list of names | session lead |
| Timer | physical / app | shared |
| Parking lot doc | text file | shared |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[pair-programming]]` | Strong-style navigation is shared between mob and pair; preconditions overlap. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: strong style, intent-level navigation, 5-10 min rotation, written Done, breaks, retro, time-boxed disagreements, parking lot | ~700 |
| `content/02-output-contract.xml` | essential | Required session-checklist shape + retrospective doc shape | ~500 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns: backseat-driver mode, no rotation, no retro | ~500 |
| `content/06-decision-tree.xml` | essential | Root: "Is this a learning/complex task with 3-6 willing people?" | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Generate session checklist | haiku | Boilerplate. |
| Author Done definition | sonnet | Needs concise framing. |
| Triage rotation breakdowns | sonnet | Pattern-match symptoms. |

## Templates

| File | Purpose |
|------|---------|
| `templates/mob-session.sh` | Visible-timer + agenda + rotation helper script. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-mob-programming.py` | Validates that a session checklist has Done definition + rotation + retro plan. | Pre-session start. |

## Related

- parent skill: `free/dev/software-developer/`
- `[[pair-programming]]` — two-person variant

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters: 3-6 people present yes/no, complex/learning task yes/no, single-sentence Done writable yes/no.
