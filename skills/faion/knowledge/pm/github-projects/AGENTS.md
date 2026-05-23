# GitHub Projects

## Summary

**One-sentence:** Solo / small-team GitHub Projects (v2) setup: 1-2 Projects max, repository-linked, custom fields ≤8, automations via GraphQL or workflows.

**One-paragraph:** Pins the GitHub Projects v2 baseline: one Project per outcome (not per repo), repository-linked, ≤8 custom fields, GraphQL/workflow automations bounded to property changes. Output is a versioned spec keeping the Project lean enough to outlast year 1.

**Ефективно для:**

- Solo founder or 2-10 engineers using GitHub as primary code + tracker. One Project that ties issues + PRs across repos without HubSpot-style sprawl.

## Applies If (ALL must hold)

- Code lives in ≥1 GitHub repo
- Team size 1-10 engineers
- Issues + PRs tracked in GitHub (or planning to consolidate)

## Skip If (ANY kills it)

- Engineering team >25 — GitHub Projects v2 UI gets sluggish
- Non-engineering workflow (sales/ops) — pick Trello / Linear instead
- Already on Linear / Jira + not migrating

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| GitHub org + repo admin access | config | GitHub admin |
| Team roster + GitHub handles | table | people doc |
| Outcome / initiative list | doc | roadmap |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/pm/pm-agile/linear-issue-tracking` | Peer methodology — comparison baseline; GitHub picks here, Linear there. |
| `solo/pm/capacity-fit-calculator` | Peer methodology — capacity reads GitHub Project iteration data. |

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
| `draft-github-projects` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-github-projects` | haiku | Schema check + threshold checks; deterministic. |
| `review-github-projects` | opus | Cross-cycle synthesis; high-stakes change to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/github-projects.json` | JSON skeleton conforming to the output contract schema. |
| `templates/github-projects.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-github-projects.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[linear-issue-tracking__pm-agile]]
- [[capacity-fit-calculator]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
