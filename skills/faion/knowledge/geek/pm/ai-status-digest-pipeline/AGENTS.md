---
slug: ai-status-digest-pipeline
tier: geek
group: pm
domain: pm
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: "Pipeline that wires Jira + GitHub + Slack + budget sheet into an AI-drafted weekly status digest with red-yellow-green auto-classification, owner-signed before send."
content_id: "d9998db7f490888e"
complexity: deep
produces: report
est_tokens: 2900
tags: [status-digest, ai-pipeline, comms, async, pm, geek]
---

# AI Status Digest Pipeline

## Summary

**One-sentence:** Pipeline that wires Jira + GitHub + Slack + budget sheet into an AI-drafted weekly status digest with red-yellow-green auto-classification, owner-signed before send.

**One-paragraph:** communications-management provides a comms-plan template; nothing wires actual data sources into an AI-drafted weekly digest with red-yellow-green auto-classification. This methodology specifies the pipeline: typed inputs (Jira velocity, GitHub PR throughput, Slack signal, budget burn), per-area RYG classifier with thresholds, AI-drafted digest, owner sign-off gate before send. Output: a weekly status digest the sponsor can read in under 5 minutes.

**Ефективно для:** PMs running async cross-timezone delivery; program managers reporting to steering committees; agencies sending client status emails.

## Applies If (ALL must hold)

- Project runs async across timezones
- Data sources (Jira, GitHub, Slack, budget) are accessible via API or export
- Sponsor / steering committee wants weekly status
- PM has budget for AI drafting (token cost is justified)

## Skip If (ANY kills it)

- Single timezone, small team — async digest is overkill
- Data sources inaccessible — pipeline cannot run
- Sponsor wants only verbal updates — written digest will not be read
- Compliance requires manual drafting (legal review) — automation conflict

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Jira velocity + ticket activity (last 7 days) | API | Jira |
| GitHub PR throughput (last 7 days) | API | GitHub |
| Slack signal (channel activity, anomalies) | API | Slack |
| Budget burn-rate vs plan | Sheet | finance ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/pm/project-manager` | parent role skill |
| [[ai-risk-aging-agent]] | feeds risk section |

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
| `ingest_data_sources` | haiku | Mechanical extraction |
| `classify_ryg` | sonnet | Bounded per-area RYG with thresholds |
| `draft_digest` | sonnet | Bounded synthesis |
| `executive_summary` | opus | Cross-area narrative for sponsor |

## Templates

| File | Purpose |
|------|---------|
| `templates/ai-status-digest-pipeline.json` | JSON schema for the digest output |
| `templates/ai-status-digest-pipeline.md` | Markdown digest skeleton with RYG sections |
| `templates/_smoke-test.json` | Minimum-viable filled digest |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-status-digest-pipeline.py` | Validate output against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/pm/`
- [[ai-risk-aging-agent]]
- [[ai-sprint-planning-agent]]
- [[client-trust-rebuild-comms-templates]]

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether ai-status-digest-pipeline applies: root question — "Is the project async with accessible data sources AND a sponsor expecting weekly written status?". Branches lead to a specific core rule from `01-core-rules.xml` when the methodology fits, or to a `skip-methodology` conclusion when it does not. Rules referenced: r1-bound-scope, r2-typed-input, r3-ryg-thresholds-declared, r4-owner-sign-off, r5-llm-grounding, r6-versioned-record.
