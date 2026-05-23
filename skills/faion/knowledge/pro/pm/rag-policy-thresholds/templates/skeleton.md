<!-- purpose: RAGPolicy skeleton with default signal slots + per-colour actions -->
<!-- consumes: incident corpus + reporting cadence -->
<!-- produces: scaffold consumed by set-thresholds -->
<!-- depends-on: content/01-core-rules.xml#r2-bounded-output -->
<!-- token-budget-impact: ~160 tokens -->

# RAG Policy — [Project]

**Owner:** [role] / [person]
**Trigger:** weekly_status | fortnightly_status | monthly_status
**Reporting cadence:** N days
**Version:** [semver]
**Last reviewed:** YYYY-MM-DD

## Signals

| signal_id | input_source | amber_threshold | red_threshold | comparator | evidence |
|-----------|--------------|----|----|----|----------|
| schedule_variance_pct | Jira velocity | 10 | 20 | gt | incident-2025-Q4 |
| budget_variance_pct | finance export | 5 | 15 | gt | policy://pmo/budget |
| defect_escape_rate | Sentry | 0.05 | 0.10 | gt | postmortem-2026-Q1 |
| blockers_count | Jira filter | 2 | 4 | gt | retrospective-S13 |

## Actions

- **Green:** continue normal cadence
- **Amber:** PM schedules mid-week health-check; surface in next sync with evidence
- **Red:** fire distressed-project-rescue playbook; sponsor notified within 4h

<!-- Rules:
- Every threshold MUST be numeric (no "significant", "material").
- Every signal MUST cite ≥1 evidence anchor (incident, postmortem, policy).
- Actions.red MUST be concrete and time-bounded.
-->
