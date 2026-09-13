# Retro Facilitation Multistyle

## Summary

**One-sentence:** Five canonical retro formats (mad-sad-glad, 4Ls, sailboat, lean-coffee, anonymous-async) with named selection criteria per team state, plus an evidence-anchored outcome review so retros stop being folklore.

**One-paragraph:** scrum-ceremonies mentions retros generically; there is no facilitation playbook with multiple formats and selection criteria. Async cross-timezone teams (P4 outsource) need anonymous-async; stable product teams (P6) cycle formats to avoid fatigue. This methodology pins the artefact: a versioned per-retro instance with the chosen format, the selection rationale (team-state evidence), the action items it produced, the named owner of those actions, and the outcome review at the next retro that closes the loop on whether actions changed behaviour.

**Ефективно для:**

- Solo PM facilitating retros across an async/outsourced team.
- Stable product team cycling formats to avoid retro fatigue (≥3 instances/year).
- Documenting why a format was picked + whether it produced change.
- Replacing free-form retro notes with a reviewable artefact.

## Applies If (ALL must hold)

- The team runs at least 3 retros a year on an iteration of 5-31 days, so there is a next retro date to bind actions to and a previous instance to walk.
- The facilitator can state the team's distribution (async, hybrid, in-person), the participant timezones and whether everyone can be on one live call.
- The last two retro instances are on file with their formats and their card / attendance counts, so rotation and the fatigue signal can be judged.
- A tracker (GitHub, GitLab, Jira) is open during the retro so each action gets an issue or PR link before the timebox ends.
- An anonymous 1-5 poll and, for async teams, a form or board that stores no author identity are available.

## Skip If (ANY kills it)

- A one-shot retro or fewer than 3 a year: write a single retro doc; there is no previous instance to walk and no next retro to date actions against.
- No previous retro on record and the team cannot say its distribution: run one ad-hoc retro with the format card, then start versioned instances from the second.
- The line manager insists on sitting in the discussion or the team has no tracker for action links: the instance cannot pass the safety and action rules; fix the room first.
- A project post-mortem or incident review rather than an iteration retro: those have their own shape (blameless post-mortem), not the five formats here.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| The last two `RetroInstance` files (format, action items, participation counts) | JSON, this contract | this methodology (prior cycles) |
| Participant list with timezones (IANA names) and whether everyone can join one live call | roster | PM |
| Iteration length and the next retro date | calendar | PM |
| Kerth's Prime Directive text and an anonymous 1-5 safety poll | text + poll tool | `templates/format-card.md.j2` / PM |
| Tracker with issue / PR links creatable during the retro | GitHub / GitLab / Jira | platform |
| For async teams: a card form or board that stores no author identity | form / board | PM |
| Format card with the five formats and the selection rule | `templates/format-card.md.j2` | this methodology |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[retro-format-rotation-guide]] | Sibling guide that informs format choice across multiple retros. |
| [[status-report-templates-by-audience]] | Retro outputs flow into status reports. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: format matches distribution, rationale names state and history, fatigued team rotates, Prime Directive and safety check, previous actions reviewed first, 1-3 owned linked dated actions, anonymous-async window and clustering, timebox held | ~2200 |
| `content/02-output-contract.xml` | essential | Draft-07 schema for `RetroInstance`: format against distribution and fatigue with the previous two formats, rationale, Prime Directive and anonymous safety check with the below-3 switch, previous-action status walk, 1-3 owned / linked / dated actions, anonymous-async window and clustering, lean-coffee dot-votes, published timebox; valid + invalid examples, forbidden patterns | ~4650 |
| `content/03-failure-modes.xml` | essential | 6 modes: live format on async team, same format forever, action avalanche, no memory of previous actions, status meeting in disguise, timebox blowout | ~900 |
| `content/04-procedure.xml` | essential | 8 steps: record team state and the last two formats, choose the format and write the rationale, publish the timebox, Prime Directive and safety check, walk the previous actions, collect input per format (async window or lean-coffee dot-vote), close with 1-3 owned linked dated actions, validate and file | ~2000 |
| `content/05-examples.xml` | recommended | Complete anonymous-async instance for a Kyiv-Lisbon-London team with a note per non-obvious value, and a bad instance with the validator output and what the facilitator sees | ~2350 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `format_selection` | sonnet | Team-state judgement (async vs in-person, fatigue cycle). |
| `retro_facilitation_notes` | sonnet | Per-instance synthesis of team input. |
| `outcome_review_synthesis` | opus | Cross-cycle: did action items change behaviour? |

## Templates

| File | Purpose |
|------|---------|
| `templates/retro-instance.md.j2` | Per-retro instance template (format / actions / owner / review) |
| `templates/retro-instance.md` | Per-retro instance template (format / actions / owner / review) Generated from `templates/retro-instance.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/format-card.md.j2` | One-pager listing the 5 supported formats + selection criteria |
| `templates/format-card.md` | One-pager listing the 5 supported formats + selection criteria Generated from `templates/format-card.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-retro-facilitation-multistyle.py` | Validate retro instance against 02-output-contract schema | Pre-merge + next retro review |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[retro-format-rotation-guide]]
- [[status-report-templates-by-audience]]
- [[solo-burnout-tripwires]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes by team state, format choice, action-item evidence, owner naming, and outcome-review staleness onto a rule from `content/01-core-rules.xml`. Walk it before every retro.
