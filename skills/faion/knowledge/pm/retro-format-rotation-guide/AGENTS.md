# Retro Format Rotation Guide

## Summary

**One-sentence:** A cross-retro rotation guide that picks the next format from {start-stop-continue, sailboat, 4ls, timeline, anonymous-async} based on the previous 3 formats, team state, and a stale-format detector.

**One-paragraph:** scrum-ceremonies covers the existence of retros; no playbook for picking the *next* format. Teams default to one format and retro fatigue sets in within 4-6 cycles — output drops, contributors disengage, action items dry up. This guide tracks the last-3-retro history per team, applies a rotation rule (no format used twice in last 3), and emits the recommended next format with a one-line rationale. Outcome review at the following retro confirms whether the rotation refreshed signal.

**Ефективно для:**

- Solo PM running retros for the same team ≥4 times/year.
- Detecting retro fatigue early (action-item count dropping cycle-over-cycle).
- Pairing with retro-facilitation-multistyle to remove the "what format this time?" friction.
- Quarterly retro-rotation health check.

## Applies If (ALL must hold)

- Team has run ≥3 retros under the PM's facilitation (history exists).
- PM facilitates ≥4 retros per year for this team.
- PM owns the rotation artefact (or escalates ownership).
- Team uses a version-controlled or wiki space hosting the history.

## Skip If (ANY kills it)

- First-ever retro for the team — no rotation needed.
- Team has run &lt; 3 retros — defer until history exists.
- One-shot retro (post-incident, post-launch) — different rubric.
- No named owner — defer until ownership is resolved.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Last 3 retro instances with format + outcome | repo path | PM |
| Team-state input (distribution + fatigue) | doc | PM |
| Named owner for the rotation guide | identity | PM |
| Outcome-review cadence published | calendar | PM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[retro-facilitation-multistyle]] | Per-retro facilitation methodology this guide schedules across. |
| [[status-report-templates-by-audience]] | Rotation health flows into status reports. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules — explicit trigger, bounded output, evidence-anchored, named owner, iteration loop | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for the rotation guide artefact + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 6 known failure modes with detector + repair | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `history_read` | haiku | Pull last-3 retro instances + outcome counts. |
| `rotation_pick` | sonnet | Apply the rotation rule + team state to the next format. |
| `health_check` | opus | Cross-cycle synthesis: is rotation refreshing signal? |

## Templates

| File | Purpose |
|------|---------|
| `templates/rotation-guide.md` | Per-team rotation guide (history + next pick + rationale) |
| `templates/rotation-rule-card.md` | One-pager: rotation rule + stale-format detector |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-retro-format-rotation-guide.py` | Validate the rotation artefact against 02-output-contract schema | Before each next retro is scheduled |

## Related

- [[retro-facilitation-multistyle]]
- [[status-report-templates-by-audience]]
- [[solo-burnout-tripwires]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes by history length, last-3-format set, team-state, and outcome-review staleness onto a rule from `content/01-core-rules.xml`. Walk it before scheduling every next retro.
