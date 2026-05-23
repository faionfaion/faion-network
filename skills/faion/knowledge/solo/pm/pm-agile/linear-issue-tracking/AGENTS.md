---
slug: linear-issue-tracking
tier: solo
group: pm
domain: pm
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Solo / small-team Linear setup: workspace, cycle policy, issue states, label taxonomy, Slack/GitHub linkages, automation hygiene.
content_id: "47d11764c93d3e16"
complexity: medium
produces: spec
est_tokens: 4100
tags: ["linear", "pm-agile", "pm", "solo", "issue-tracking"]
---
# Linear Issue Tracking (PM Agile)

## Summary

**One-sentence:** Solo / small-team Linear setup: workspace, cycle policy, issue states, label taxonomy, Slack/GitHub linkages, automation hygiene.

**One-paragraph:** Pins the Linear baseline for solo founders + small teams: one workspace, weekly cycles, canonical state set, ≤15 labels, GitHub + Slack integrations on. Output is a versioned spec covering setup + governance + agent-integration limits.

**Ефективно для:**

- Solo founder or 2-10-person team adopting Linear who wants to skip the rewrite-in-month-3 phase. One spec covering workspace shape, cycle policy, label taxonomy, integrations.

## Applies If (ALL must hold)

- Adopting Linear OR auditing existing Linear workspace
- Team size 1-10 (small enough for one workspace)
- Issues estimated in story points OR T-shirt sizes

## Skip If (ANY kills it)

- Already use Jira / GitHub Projects exclusively and not migrating
- Team size >25 — Linear architecture differs from enterprise
- Issues are not estimated AND not planning to start

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Team roster + roles | table | people doc |
| Existing repos / Slack channels to integrate | list | stack inventory |
| Cycle length decision (1w / 2w) | doc | team agreement |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/pm/capacity-fit-calculator` | Peer methodology — capacity computation reads Linear estimates. |
| `solo/pm/burndown-diagnosis-cheatsheet` | Peer methodology — burndown chart sourced from Linear cycle data. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules incl. skip-this-methodology + run-the-checklist | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-linear-issue-tracking` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-linear-issue-tracking` | haiku | Schema check + threshold checks; deterministic. |
| `review-linear-issue-tracking` | opus | Cross-cycle synthesis; high-stakes change to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/linear-issue-tracking.json` | JSON skeleton conforming to the output contract schema. |
| `templates/linear-issue-tracking.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-linear-issue-tracking.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[capacity-fit-calculator]]
- [[github-projects]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
