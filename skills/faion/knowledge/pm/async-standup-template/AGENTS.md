# Async Standup Template

## Summary

**One-sentence:** Three-field written-Slack daily standup (Yesterday, Today, Blocker) for 1-3 person cross-timezone teams, with blocker-routing SLA and silence-detection rule.

**One-paragraph:** Replaces the verbal scrum standup for contractor and cross-timezone setups where synchronous meetings cost a half-day per person. Mechanism: one Slack thread per day in a dedicated channel; every contributor posts a strictly-shaped 3-field message within their local working window; blockers are auto-tagged and routed to a named owner with a 12-hour response SLA; missed posts trigger a silence-detector ping. Primary output: a daily searchable thread that the PM can scan in under 5 minutes plus a weekly digest.

**Ефективно для:**

- Контрактних команд 1-3 інженерів з timezone-gap ≥ 4 години.
- Аутсорс-команд, де "тиха" denysenkoдня важливіша за дисциплінарне керівництво.
- Solopreneur agency з ≥2 проектами одночасно, де щоденний sync неможливий.
- Розподілених open-source-команд з регулярним cadence.

## Applies If (ALL must hold)

- team_size ≤ 3 active contributors per project (or single-team within larger org).
- timezone_gap_between_any_two_members ≥ 4 hours.
- communication_platform ∈ {Slack, Microsoft Teams, Discord, Mattermost}.
- engagement_duration ≥ 2 weeks (one-shot tasks don't need a cadence).

## Skip If (ANY kills it)

- Team fully co-located in one timezone — verbal standup is faster.
- Team &gt; 6 people — needs Scrum daily or a different ceremony.
- Async-only deep-work norm (no expectation of same-day reply) — replace with weekly written update.
- Project &lt; 5 working days — standup overhead exceeds value.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Dedicated standup channel | Slack/Teams/Discord channel with pinned topic | platform admin |
| Blocker-owner roster | `{name → @-handle}` map | PM / engagement lead |
| Working-hours-per-contributor | timezone + window | contributor profile |
| Silence-detector job | scheduled task (Workflow Builder / GH Action) | platform admin |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[communications-management]] | Sets the comms-plan framing this template lives inside. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: shape, window, blocker-routing, silence-detection, weekly-digest, skip-this-methodology | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for post + digest, with valid/invalid/forbidden | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 700 |
| `content/06-decision-tree.xml` | essential | Apply/skip routing on observable signals | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `personal_standup_draft` | haiku | Template fill from a contributor's daily log; low cost. |
| `blocker_routing` | sonnet | Judgment on which @-owner gets the blocker. |
| `weekly_digest_synthesis` | sonnet | Cross-day synthesis across ≤5 days of threads. |

## Templates

| File | Purpose |
|------|---------|
| `templates/post.md` | Three-field daily-post skeleton with @-owner placeholder. |
| `templates/weekly-digest.md` | PM weekly recap skeleton with shipped / in-progress / blockers / missed-posters / next-week-risk. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-async-standup-template.py` | Validate a post or digest JSON against the schema | Pre-commit; CI on weekly-digest commit |

## Related

- [[communications-management]]
- [[lessons-learned]]
- [[delivery-sop-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps three observables (team_size, timezone_gap, expected_response_speed) to apply / skip-with-fallback / replace-with-weekly-update. Every leaf references a rule from `01-core-rules.xml`.
