# Daily Standup AI Pre-Brief Template

## Summary

**One-sentence:** Spec for the AI pre-brief artefact (sections, data sources, length cap) that goes out 30 minutes before daily standup so the team arrives prepared.

**One-paragraph:** P6 teams need a concrete template for the AI pre-brief artefact — Faion's `pm-agile/scrum-ceremonies` is too high-level for the daily AI-augmented format. This methodology specifies the sections (yesterday's deltas, today's plan, blockers, anomalies), the data sources (Jira, GitHub PRs, CI signals, Slack), the length cap (≤400 words), and the send-time discipline (30 min before standup). Output: the pre-brief team members read before the meeting starts.

**Ефективно для:** PMs running daily standups with AI augmentation; scrum masters speeding up standup throughput; engineering managers reducing meeting waste.

## Applies If (ALL must hold)

- Team runs daily standups
- Data sources (Jira, GitHub, CI, Slack) are accessible via API
- Team will read a 400-word pre-brief 30 min before the meeting
- PM has budget for AI drafting

## Skip If (ANY kills it)

- Team does not run daily standups
- Data sources inaccessible
- Team rejects async pre-reads
- Standup already <10 minutes and effective — no need

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Last 24h Jira activity | API | Jira |
| Last 24h GitHub PR + CI signal | API | GitHub |
| Slack channel activity for the team | API | Slack |
| Per-engineer planned focus block (if available) | Calendar | team calendar |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/pm/project-manager` | parent role skill |
| [[ai-status-digest-pipeline]] | shares data extraction pattern |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON schema, valid + invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom + root cause + fix | ~800 |
| `content/06-decision-tree.xml` | essential | Decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `ingest_24h_activity` | haiku | Mechanical extraction |
| `draft_prebrief` | sonnet | Bounded synthesis within 400-word cap |
| `flag_anomalies` | sonnet | Bounded detection + escalation |

## Templates

| File | Purpose |
|------|---------|
| `templates/daily-standup-ai-prebrief-template.json` | JSON schema for the pre-brief |
| `templates/daily-standup-ai-prebrief-template.md` | Markdown pre-brief skeleton with all sections |
| `templates/_smoke-test.md` | Minimum-viable filled pre-brief |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-daily-standup-ai-prebrief-template.py` | Validate output against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/pm/`
- [[ai-status-digest-pipeline]]
- [[ai-sprint-planning-agent]]
- [[anti-theater-retro-guardrails]]

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether daily-standup-ai-prebrief-template applies: root question — "Does the team run a daily standup AND data sources are accessible AND team will read a pre-brief?". Branches lead to a specific core rule from `01-core-rules.xml` when the methodology fits, or to a `skip-methodology` conclusion when it does not. Rules referenced: r1-length-cap, r2-send-time, r3-typed-input, r4-anomaly-flagging, r5-named-owner, r6-versioned-record.
