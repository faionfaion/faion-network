# Ai Assisted Velocity Anomaly Detection

## Summary

**One-sentence:** Detects velocity anomalies (commit volume, PR latency, ticket cycle time) with explicit thresholds + remediation paths — before the sprint review reveals them.

**One-paragraph:** Detects velocity anomalies (commit volume, PR latency, ticket cycle time) with explicit thresholds + remediation paths — before the sprint review reveals them. The methodology is anchored to a single named consumer (a PM, EM, portfolio owner, or downstream agent) and a fixed-shape artefact that downstream review can sign off without re-deriving reasoning. Inputs are explicit, evidence is anchored, and the artefact carries `version`, `owner`, and `last_reviewed` so it remains a living operating tool rather than folklore. Outputs that fail the contract are rejected at validation time, not at executive review.

**Ефективно для:** PM/EM-у — щоб velocity-зрив був помічений у тиждень-1, не на demo.

## Applies If (ALL must hold)

- Team runs sprints (1-3 weeks) with a tracker as source of truth.
- Historical velocity baseline exists (≥6 sprints).
- Commit + PR data is available via API (GitHub / GitLab).
- Named PM/EM owns the response when an anomaly fires.

## Skip If (ANY kills it)

- Team < 4 people — sample size too small; manual feel is more accurate.
- Tracker is stale — anomaly detection on stale data fires false positives.
- Team uses #NoEstimates — velocity is not the team's primary signal.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Tracker velocity export | API/CSV | Jira / Linear |
| Git commit + PR feed | API | GitHub / GitLab |
| Baseline of ≥6 sprints | CSV | tracker history |
| Threshold-calibration document | Markdown | owner-authored |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/pm/pm-agile/ai-assisted-backlog-deduplication` | Sibling AI-assist pipeline pattern. |
| `geek/pm/exception-driven-standup-protocol` | Anomaly signals feed the pre-brief. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules every application enforces | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + self-check | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix | ~900 |
| `content/06-decision-tree.xml` | essential | Root question → branches → conclusions (rule refs) | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `metric-pull` | haiku | Pure API pull. |
| `z-score-compute` | haiku | Closed-form math. |
| `anomaly-narrative` | sonnet | Bounded synthesis: was it a real anomaly or a known event? |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.py` | Python skeleton: pull velocity + PR metrics, compute z-scores against baseline, emit anomaly JSON. |
| `templates/header.yaml` | Frontmatter contract: owner, version, last_reviewed for the produced artefact. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-assisted-velocity-anomaly-detection.py` | Validate produced artefact against the JSON Schema in `02-output-contract.xml`. | Pre-merge and on every artefact refresh. |

## Related

- [[ai-assisted-backlog-deduplication]]
- [[exception-driven-standup-protocol]]
- [[ai-pm-tool-integration-recipes]]

## Decision tree

The mandatory decision tree at `content/06-decision-tree.xml` Decides whether to run weekly anomaly detection (≥6 baseline + ≥4 team + fresh tracker + owner), block until baseline exists, or skip (small team / stale tracker). Run before the first detection cron is enabled.
