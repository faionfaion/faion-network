---
slug: project-integration
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: The PM as integrator ensures that decisions in scope, schedule, cost, quality, risk, resources, communications, and procurement are consistent and mutually reinforcing.
content_id: "e52338361d3020d7"
tags: [project-integration, change-control, status-reporting, project-charter, baseline-management]
---
# Project Integration Management

## Summary

**One-sentence:** The PM as integrator ensures that decisions in scope, schedule, cost, quality, risk, resources, communications, and procurement are consistent and mutually reinforcing.

**One-paragraph:** The PM as integrator ensures that decisions in scope, schedule, cost, quality, risk, resources, communications, and procurement are consistent and mutually reinforcing. All component plans live as typed YAML/JSON artifacts in git; status RAG is computed from measurable variance thresholds, never from opinion; and every baseline change goes through a documented change-control PR. Agents propose; sponsors approve baseline changes.

## Applies If (ALL must hold)

- Multi-team / multi-vendor programs where decisions in one area routinely affect another
- Regulated programs where the Project Charter is a contractual artifact requiring version control
- Hybrid agile+waterfall environments with component plans in different tools needing a single source of truth
- Portfolio PMO reporting where dozens of projects feed the same status rollup
- Integrated Change Control when a change request affects more than one baseline

## Skip If (ANY kills it)

- Solo or duo teams — overhead exceeds value; a one-page README and a kanban board cover integration
- Pure agile single-team with one product backlog — Scrum already integrates work; bolting on PMBoK integration creates conflict
- Pre-charter exploratory spikes — formalising integration too early kills learning
- Portfolios where project owners refuse to share artifacts in a common format — fix governance first

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `pro/pm/pm-traditional/`
