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

- At least three committed `RetroInstance` files exist for this team, each with its format, action-item count, participant count and silent-participant count.
- The team retros at least 4 times a year, so the no-repeat-in-3 rule and the 12-month lookback have cycles to work on.
- The PM can state the team's distribution (async, hybrid, in-person) and fatigue signal, and knows when each of the seven formats was last run for this team.
- A named person owns the guide and the next retro's outcome review will record the counts back into it.
- For async teams: a shared board or form with anonymous input and a window spanning every timezone is available.

## Skip If (ANY kills it)

- Fewer than three committed instances: record `skip: history < 3` and pick with the format card alone; the no-repeat rule has nothing to work on.
- The last two scheduled retros have no recorded counts: backfill them from the instances first; the stale detector is blind.
- Two consecutive rotations to non-stale formats raised neither actions nor contributors: rotation is suspended; run the morale pulse or burnout tripwires before picking again.
- A one-shot post-incident or post-launch retro: that is a blameless post-mortem, not a rotation slot.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| The three most recent committed `RetroInstance` files: format, action items, participants, silent participants | JSON, [[retro-facilitation-multistyle]] contract | this team's retro space |
| Last-used date per format for this team (all seven; never = null) | table | retro space history |
| Team state: distribution and fatigue signal | PM's read of the team | PM |
| Previous `RotationGuide` with its refresh trend and any escalation | JSON, this contract | this methodology (prior cycle) |
| Rotation rule card: no-repeat, async pool, stale detector, tie-breakers | `templates/rotation-rule-card.md.j2` | this methodology |
| Next retro's calendar slot and, for async teams, the anonymous board and timezone list | calendar, board | PM |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[retro-facilitation-multistyle]] | Per-retro facilitation methodology this guide schedules across. |
| [[status-report-templates-by-audience]] | Rotation health flows into status reports. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: history from committed instances, no repeat in last 3, async pool, three-signal stale detector, fatigued picks 12-month-unused format, rationale names history and tie-breaker, counts recorded per retro, two rotations without refresh escalate to team health | ~2200 |
| `content/02-output-contract.xml` | essential | Draft-07 schema for `RotationGuide`: three-instance committed history with counts or `skip`, last-used date per format, team state, stale detector findings with signal, refresh trend with team-health escalation, the pick with tie-breaker and exception, rationale naming history and state; valid + invalid examples, forbidden patterns | ~3800 |
| `content/03-failure-modes.xml` | essential | 6 modes: three sailboats, history from memory, live format for async team, blind stale detector, fatigued gets fourth-most-recent, morale treated as format | ~900 |
| `content/04-procedure.xml` | essential | 7 steps: read the committed history with counts or skip, run the stale detector, compute the refresh trend and escalate at two, pick inside the no-repeat and async rules, apply the fatigue lookback and tie-breaker, write the rationale and schedule, record the counts at the outcome review | ~1750 |
| `content/05-examples.xml` | recommended | Complete guide rotating a newly async platform team onto anonymous-async with a note per non-obvious value, and a bad guide (three sailboats from memory) with the validator output and what the PM sees | ~1800 |
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
| `templates/rotation-guide.md.j2` | Per-team rotation guide (history + next pick + rationale) |
| `templates/rotation-guide.md` | Per-team rotation guide (history + next pick + rationale) Generated from `templates/rotation-guide.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/rotation-rule-card.md.j2` | One-pager: rotation rule + stale-format detector |
| `templates/rotation-rule-card.md` | One-pager: rotation rule + stale-format detector Generated from `templates/rotation-rule-card.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-retro-format-rotation-guide.py` | Validate the rotation artefact against 02-output-contract schema | Before each next retro is scheduled |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[retro-facilitation-multistyle]]
- [[status-report-templates-by-audience]]
- [[solo-burnout-tripwires]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes by history length, last-3-format set, team-state, and outcome-review staleness onto a rule from `content/01-core-rules.xml`. Walk it before scheduling every next retro.
