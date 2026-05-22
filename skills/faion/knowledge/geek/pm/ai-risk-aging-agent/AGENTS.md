---
slug: ai-risk-aging-agent
tier: geek
group: pm
domain: pm
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: "Daily report from an agent that ingests the project risk register, scores each risk on staleness, ownership response rate, and dependent-task count, and updates the register with aged-or-stale flags."
content_id: "8da66f7f67581ed2"
complexity: deep
produces: report
est_tokens: 2900
tags: [risk-management, ai-agent, pm, distressed-project, geek]
---

# AI Risk Aging Agent

## Summary

**One-sentence:** Daily report from an agent that ingests the project risk register, scores each risk on staleness, ownership response rate, and dependent-task count, and updates the register with aged-or-stale flags.

**One-paragraph:** Risk-management and risk-register are PMBOK narratives; nothing runs a daily agent that detects when risks are aging out of relevance, when their owners have not responded, or when their dependent-task count has changed. This methodology specifies the agent: typed input (risk register YAML, ticket activity, owner directory), bounded transformation (per-risk scoring on staleness × response × dependents), and a daily report that surfaces the top-N aged risks plus recommended actions (refresh, escalate, retire).

**Ефективно для:** PMs running distressed-project rescues; program managers tracking multi-team risk; PMOs standardising risk hygiene.

## Applies If (ALL must hold)

- Project is in active distress or rescue mode (90-day turnaround)
- Risk register exists in machine-readable form (YAML / CSV / tool API)
- Owner directory with handles or emails is reachable
- Daily cadence is acceptable to the project sponsor

## Skip If (ANY kills it)

- Project is in steady state with stable risk register — daily is overkill
- Risk register lives only in slides / Word — agent input not feasible
- Single-risk crisis — focus on the crisis, not aging

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Risk register | YAML / CSV | PM tool export |
| Ticket activity log (last 30 days) | CSV / API | Jira / Linear / GitHub |
| Owner directory | YAML | team wiki |
| Dependency map (risk → tasks) | YAML | PM tool |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/pm/project-manager` | parent role skill |

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
| `ingest_register_and_activity` | haiku | Mechanical extraction |
| `score_risks` | sonnet | Bounded per-risk scoring |
| `draft_action_recommendations` | sonnet | Bounded recommendations |
| `executive_summary` | opus | Cross-risk narrative for sponsor |

## Templates

| File | Purpose |
|------|---------|
| `templates/ai-risk-aging-agent.json` | JSON schema for the daily risk report |
| `templates/ai-risk-aging-agent.md` | Markdown skeleton with daily report structure |
| `templates/_smoke-test.json` | Minimum-viable filled report |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-risk-aging-agent.py` | Validate output against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/pm/`
- [[ai-sprint-planning-agent]]
- [[ai-status-digest-pipeline]]

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether ai-risk-aging-agent applies: root question — "Is the project in active rescue AND the risk register machine-readable AND owners reachable?". Branches lead to a specific core rule from `01-core-rules.xml` when the methodology fits, or to a `skip-methodology` conclusion when it does not. Rules referenced: r1-bound-scope, r2-typed-input, r3-named-owner, r4-staleness-threshold, r5-llm-grounding, r6-versioned-record.
