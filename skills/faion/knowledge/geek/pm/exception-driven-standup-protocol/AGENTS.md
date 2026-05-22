---
slug: exception-driven-standup-protocol
tier: geek
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: "Replaces status-theatre standups with an exception-driven protocol — AI pre-brief surfaces blockers, humans only speak when they own one."
content_id: "035514aa78b29312"
complexity: medium
produces: playbook-step
est_tokens: 3400
tags: [pm, standup, exception-driven, distributed-teams, ai-prebrief]
---
# Exception Driven Standup Protocol

## Summary

**One-sentence:** Replaces status-theatre standups with an exception-driven protocol — AI pre-brief surfaces blockers, humans only speak when they own one.

**One-paragraph:** Replaces status-theatre standups with an exception-driven protocol — AI pre-brief surfaces blockers, humans only speak when they own one. The methodology is anchored to a single named consumer (a PM, EM, portfolio owner, or downstream agent) and a fixed-shape artefact that downstream review can sign off without re-deriving reasoning. Inputs are explicit, evidence is anchored, and the artefact carries `version`, `owner`, and `last_reviewed` so it remains a living operating tool rather than folklore. Outputs that fail the contract are rejected at validation time, not at executive review.

**Ефективно для:** Distributed-PM-у — 15-min standup перетворюється на 5-min, бо озвучуються тільки блокери, не статус-театр.

## Applies If (ALL must hold)

- Team is distributed across >= 2 time zones OR async-first.
- Daily standup currently consumes >= 75 minutes/week across the team.
- Tracker is the source of truth (Jira / Linear / GitHub Projects) with status fields kept current.
- A named PM or scrum-master owns the protocol.

## Skip If (ANY kills it)

- Team < 4 people — direct conversation is cheaper than a protocol.
- Tracker is stale (>3-day lag) — pre-brief will be wrong; fix tracker hygiene first.
- Team explicitly prefers ritual standups (cultural preference) — do not force this protocol.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Tracker API key | secret | Jira / Linear / GitHub Projects |
| Standup channel | Slack/Teams | team comms |
| Pre-brief schedule | cron | standup time minus 15 min |
| Named protocol owner | person | PM or scrum-master |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/pm/project-manager/1on1-template-managers` | Companion ritual for personal blockers. |
| `geek/pm/pm-agile/ai-assisted-velocity-anomaly-detection` | Anomaly signals feed the pre-brief. |

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
| `tracker-query-prebrief` | haiku | Structured tracker query — template work. |
| `anomaly-summarisation` | sonnet | Bounded judgement: which signals are exception-worthy. |
| `escalation-write-up` | opus | Cross-team narrative when blocker spans roles. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Pre-brief skeleton: blocker list + anomaly highlights + 'speak only if your name is here' section. |
| `templates/header.yaml` | Frontmatter contract: owner, version, last_reviewed for the produced artefact. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-exception-driven-standup-protocol.py` | Validate produced artefact against the JSON Schema in `02-output-contract.xml`. | Pre-merge and on every artefact refresh. |

## Related

- [[ai-assisted-velocity-anomaly-detection]]
- [[1on1-template-managers]]
- [[ai-pm-tool-integration-recipes]]

## Decision tree

The mandatory decision tree at `content/06-decision-tree.xml` Decides whether the protocol fits (distributed + fresh tracker + >=75 min/wk standup), is blocked (stale tracker), or skipped (co-located / short standups). Run before the first pre-brief is wired up.
