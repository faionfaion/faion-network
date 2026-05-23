<!-- purpose: RetroActionItem skeleton with mandatory success criteria fields -->
<!-- consumes: retro raw notes + telemetry sources -->
<!-- produces: scaffold consumed by derive-threshold -->
<!-- depends-on: content/01-core-rules.xml#r1-fixed-shape -->
<!-- token-budget-impact: ~130 tokens -->

# Retro Actions — Sprint S{N}

**Owner:** [team-lead role] / [person]
**Version:** [semver]
**Last reviewed:** YYYY-MM-DD

## Actions

| action_id | experiment | input_signal | measurement_source | threshold | deadline_sprint | owner_role | outcome_verdict |
|-----------|------------|--------------|--------------------|-----------|-----------------|------------|------------------|
| S14-1 | Rotate PR-review-day Fri; cap reviewer WIP at 5 | cycle_time_p95_days | Jira filter | reduce 4d→3d by S15 | S15 | tech-lead | pending |

<!-- Rules:
- experiment >= 20 chars; falsifiable hypothesis with named intervention.
- threshold MUST be numeric / measurable.
- owner_role from stakeholder register (not "team").
- deadline_sprint matches ^S[0-9]+$.
- outcome_verdict updated at deadline.
-->
