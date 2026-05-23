<!-- purpose: CommsRhythmConfig skeleton -->
<!-- consumes: team roster + cadence preferences -->
<!-- produces: scaffold consumed by pulse-compose step -->
<!-- depends-on: content/01-core-rules.xml#r1-three-rituals-only -->
<!-- token-budget-impact: ~120 tokens -->

# Small Team Comms Rhythm — [team_id]

**Owner:** [founder role] / [person]
**Team size:** 2 or 3 (HARD cap)
**Version:** [semver]
**Last reviewed:** YYYY-MM-DD

## Rituals (exactly 3)

| ritual_id | name | mode | duration_minutes_cap |
|-----------|------|------|----------------------|
| daily_pulse | Async daily pulse (3 lines: did / next / blocked) | async | 5 |
| weekly_sync | Weekly sync (≤30 min; agenda 24h ahead) | sync | 30 |
| monthly_direction | Monthly direction check (≤45 min) | sync | 45 |

## Cycle log (per ritual occurrence)

| cycle_iso | ritual_id | founder_only | agenda_published_24h |
|-----------|-----------|--------------|----------------------|
| 2026-W20 | weekly_sync | false | true |

## Graduation watch

- current team_size: 2
- graduate when team_size >= 4 → adopt formal PM / agile methodology within next monthly check.
