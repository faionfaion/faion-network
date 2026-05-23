---
slug: async-standup-methodology
tier: solo
group: pm
domain: pm
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Daily 3-question async standup over Slack/Discord/Notion: yesterday / today / blockers — replaces 15-min sync while preserving visibility.
content_id: "bd542ca157a5c66c"
complexity: medium
produces: spec
est_tokens: 3900
tags: ["async-standup", "pm", "remote", "solo", "rituals"]
---
# Async Standup Methodology

## Summary

**One-sentence:** Daily 3-question async standup over Slack/Discord/Notion: yesterday / today / blockers — replaces 15-min sync while preserving visibility.

**One-paragraph:** Pins a daily async standup format that produces a structured digest the founder/team can scan in 60 seconds. Three named fields, fixed time, public channel, response window. Output: a per-day artefact (one row per teammate) with blockers extracted into a separate watch list.

**Ефективно для:**

- Distributed team of 2-10 (or solo with contractors) whose sync standup costs more than it produces. Replaces the daily 15-min Zoom with a 3-question Slack thread that still surfaces blockers within 24h.

## Applies If (ALL must hold)

- Team distributed across ≥2 time zones OR fully async by policy
- ≥2 people contributing daily (solo founder + ≥1 contractor)
- A shared chat channel exists (Slack / Discord / Telegram / Notion)

## Skip If (ANY kills it)

- Solo founder with no recurring collaborators — no audience for the artefact
- Team already runs successful synchronous standup
- Critical-incident response phase — needs synchronous coordination

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Channel name + members list | config | Slack/Discord admin |
| Time-zone matrix of participants | table | team roster |
| Standup time-window policy (post-by HH:MM in each tz) | doc | team agreement |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/pm/project-manager/freelancer-personal-crm-minimal` | Peer methodology — captures contractor follow-ups blockers identify. |
| `solo/pm/project-manager/action-item-carryover-tracker` | Peer methodology — owns carry-over from blockers list. |

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
| `draft-async-standup-methodology` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-async-standup-methodology` | haiku | Schema check + threshold checks; deterministic. |
| `review-async-standup-methodology` | opus | Cross-cycle synthesis; high-stakes change to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/async-standup-methodology.json` | JSON skeleton conforming to the output contract schema. |
| `templates/async-standup-methodology.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-async-standup-methodology.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[pm-1on1-template-engineering-design]]
- [[action-item-carryover-tracker]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
