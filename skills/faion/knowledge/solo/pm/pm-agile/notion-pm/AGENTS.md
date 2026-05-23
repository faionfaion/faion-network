---
slug: notion-pm
tier: solo
group: pm
domain: pm
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Solo / small-team Notion PM workspace: Projects + Tasks + Sprints databases with relations + rollups; single tasks DB across sprints; ≤20 properties.
content_id: "ae344d00cc415537"
complexity: medium
produces: spec
est_tokens: 4300
tags: ["notion", "pm-agile", "pm", "solo", "sprint", "database"]
---
# Notion PM

## Summary

**One-sentence:** Solo / small-team Notion PM workspace: Projects + Tasks + Sprints databases with relations + rollups; single tasks DB across sprints; ≤20 properties.

**One-paragraph:** Pins the Notion PM baseline: one Tasks database with Sprint as a relation field, one Projects database with rollups, four canonical views per DB, native automations bounded to property triggers, external automation via n8n for time-triggered jobs. Output is a versioned setup spec covering schemas + views + automation + API gotchas.

**Ефективно для:**

- Solo founder or 2-10-person team using Notion as PM + docs + wiki. Avoids the per-sprint-database trap and the 60-property bloat; sets up the workspace once for the year.

## Applies If (ALL must hold)

- Small agile team (2-10) using Notion as primary PM
- Sprint cadence exists (1w / 2w)
- Tasks queried programmatically via Notion API OR planning to ≤30 days

## Skip If (ANY kills it)

- Team >10 people — Notion DB performance degrades
- Strict SOC2/HIPAA compliance with field-level audit requirements
- Native burndown/velocity charts required — use Linear instead

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Notion workspace + integration token (admin) | config | Notion admin |
| Team roster + assignee identities (Notion or email) | table | people doc |
| Sprint cadence + start-day decision | doc | team agreement |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/pm/capacity-fit-calculator` | Peer methodology — reads Tasks DB rollups for velocity inputs. |
| `solo/pm/pm-agile/linear-issue-tracking` | Peer methodology — comparison baseline; Notion picks here, Linear there. |

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
| `draft-notion-pm` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-notion-pm` | haiku | Schema check + threshold checks; deterministic. |
| `review-notion-pm` | opus | Cross-cycle synthesis; high-stakes change to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/notion-pm.json` | JSON skeleton conforming to the output contract schema. |
| `templates/notion-pm.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-notion-pm.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[linear-issue-tracking]]
- [[capacity-fit-calculator]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
