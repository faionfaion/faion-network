# Small Team Comms Rhythm

## Summary

**One-sentence:** A minimal 2-to-3-person comms cadence — async daily pulse + weekly 30-minute sync + monthly direction check — sized for a founder-as-PM team with no scrum master, no formal stakeholder matrix, and no patience for ceremony.

**One-paragraph:** Existing PM content assumes either a formal communications-management plan (overkill for 2-3 people) or a scrum team with ceremonies (assumes a scrum master). The corpus has nothing for "the founder is the PM and the second person is the senior IC and there is no scrum master." That is the most common micro-agency reality. This methodology names the three load-bearing rituals (async daily pulse, ≤30-min weekly sync, ≤45-min monthly direction check), what each must produce, the founder-not-presenter rule (founder is one voice among 2-3, not moderator), and the absolute graduation trigger at team-size ≥ 4.

**Ефективно для:**

- Founder + 1-2 ICs, no scrum master, continuous client shipping.
- Resisting scope-bloat of comms ceremony at micro-agency scale.
- Explicit graduation trigger: 4+ people → adopt formal PM/agile methodology.
- Async pulses preserve working hours; sync slots stay surgical.

## Applies If (ALL must hold)

- Team is 2 or 3 people total (including founder).
- No dedicated PM or scrum master exists or is planned.
- Team ships continuously with clients or users counting on them.
- Tier == pro or higher.

## Skip If (ANY kills it)

- Team is ≥ 4 people — graduate to `pm-agile` or formal PM methodology.
- Dedicated PM is in place — use formal comms-management methodology.
- Work is async-only with no real-time overlap — different rhythm needed.
- No founder identity — methodology assumes founder-led decisions.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Team roster (2-3 people) | YAML | founder |
| Async channel (Slack thread / Notion doc) | tool | platform |
| Weekly sync calendar slot | calendar | founder |
| Monthly direction check slot | calendar | founder |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[remote-1-1-async-fallback]] | Async pulse pattern reused for cross-tz / leave cases. |
| [[team-morale-pulse-survey]] | Cannot run at this team size (anonymity broken); use direct 1:1s instead. |
| [[retro-action-success-criteria-template]] | Direction check feeds into action items with success criteria. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: three rituals only, founder-not-presenter, async-by-default, ≤30-min weekly, graduation trigger | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for `CommsRhythmConfig` + per-cycle log | ~800 |
| `content/03-failure-modes.xml` | essential | 6 modes: founder broadcast, ritual creep, daily standup zoom, agenda-less sync, missed graduation, async fatigue | ~900 |
| `content/04-procedure.xml` | medium | 5-step: declare config → run daily pulse → weekly sync → monthly check → graduation watch | ~600 |
| `content/06-decision-tree.xml` | essential | Tree: team_size + ritual_count + sync_duration → run / repair / graduate | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pulse-compose` | haiku | Fixed text. |
| `sync-agenda-curate` | sonnet | Light judgment on prioritisation. |
| `direction-synthesise` | sonnet | Cross-month synthesis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | CommsRhythmConfig skeleton + cycle log table |
| `templates/header.yaml` | Frontmatter schema |
| `templates/_smoke-test.json` | Minimum viable filled `CommsRhythmConfig` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-small-team-comms-rhythm.py` | Validate: team_size ≤ 3, ritual count == 3, weekly_minutes ≤ 30, founder-not-presenter | Pre-merge |
| `scripts/staleness-check.py` | Flag configs whose `last_reviewed` > 90 days | Weekly cron |

## Related

- [[remote-1-1-async-fallback]]
- [[retro-action-success-criteria-template]]
- [[team-development]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps team_size + ritual_count + sync_duration to run / repair / graduate. Every leaf references a rule from `01-core-rules.xml`.
