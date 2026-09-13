<!-- purpose: RAGPolicy skeleton with default signal slots + per-colour actions -->
<!-- consumes: incident corpus + reporting cadence -->
<!-- produces: scaffold consumed by set-thresholds -->
<!-- depends-on: content/01-core-rules.xml#r-threshold-numeric-with-comparator -->
<!-- token-budget-impact: ~160 tokens -->

# RAG Policy — <project>

**Owner:** <owner_role> / <owner_full_name>
**Reporting cadence:** N days (7 weekly, 14 fortnightly)
**Version:** <document_version>
**Last reviewed:** YYYY-MM-DD (within 90 days)

## Signals (one row per signal; thresholds numeric, red strictly beyond amber)

| signal_id | unit | input_source.system | input_source.query | comparator | amber_threshold | red_threshold | evidence |
|-----------|------|------|------|----|----|----|----------|
| schedule_variance_pct | percent | Jira | dashboard panel SV% = (EV - PV) / PV * 100 | gt | 10 | 20 | incident-2025-Q4-acme-overrun, policy://pmo/schedule-tolerance |
| budget_variance_pct | percent | finance export | saved export CV% | gt | 5 | 15 | policy://pmo/budget-tolerance |
| defect_escape_rate | ratio | Sentry | saved search prod new issues / releases | gt | 0.05 | 0.10 | postmortem-2026-Q1 |
| blockers_open_count | count | Jira | project = X AND flagged = Impediment AND status != Done | gte | 2 | 4 | baseline-2026-q1-blockers |

## Actions

- **Green:** continue the cadence; record value, version and last_reviewed
- **Amber:** step: PM runs a mid-week health check with the tech lead and posts findings in the status thread; deadline_hours: 72 (inside the cycle)
- **Red:** playbook: distressed-project-rescue; first_step: sponsor notified and rescue playbook opened; within_hours: 4; fires_at: compute_time

## Review log

| logged_at | kind | person | review: version_after, signals_removed, signals_justified, signals_added_or_tightened (with new anchor) / override: cycle_date, computed_colour, reported_colour, reason |
|-----------|------|--------|--------|
| YYYY-MM-DD | review \| override | ... | ... |

## Colour history (one row per cycle, worst signal wins)

| computed_at | policy_version | policy_last_reviewed | values per signal | computed_colour | reported_colour | red_escalated_at |
|-------------|----------------|----------------------|-------------------|-----------------|-----------------|------------------|
| YYYY-MM-DD | 1.0.0 | YYYY-MM-DD | signal_id=value, ... | green \| amber \| red | same unless an override entry exists; a Red is never reported lower | YYYY-MM-DDThh:mm when Red |

<!-- Rules:
- Every threshold MUST be numeric with a comparator, in the query's unit (no "significant", "material").
- red_threshold MUST lie strictly beyond amber_threshold in the comparator's direction (lt signals: red is the smaller number).
- input_source MUST name a system and a repeatable query; schedule and budget signals are percent variances against plan.
- Every signal MUST cite >= 1 anchor: incident-<id>, postmortem-<id>, policy://<path>, baseline-<id>.
- Project colour = worst signal; an override needs a review_log entry and never lowers a Red.
- actions.red names a playbook and an hour bound and fires at compute time; actions.amber has a deadline inside the cycle.
- Review within 90 days: remove or justify silent signals, add one per unflagged incident, bump version.
-->
