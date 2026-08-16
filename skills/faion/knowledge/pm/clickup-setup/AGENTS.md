# ClickUp Setup

## Summary

**One-sentence:** Solo / small-team ClickUp baseline: hierarchy (Workspace → Space → Folder → List → Task), custom statuses ≤7, automations ≤10.

**One-paragraph:** Pins a ClickUp workspace skeleton: one Workspace, ≤3 Spaces (eng / ops / sales), Folder-per-project, List-per-sprint or pipeline, canonical 7-state custom-status set, ≤10 automations, ClickApps trimmed to essentials. Output is a versioned spec preventing the 'every-feature-on' bloat ClickUp is famous for.

**Ефективно для:**

- Solo founder or small team adopting ClickUp who wants to skip the 6-month feature-bloat phase. One spec covering hierarchy, statuses, automations, and ClickApps to keep on.

## Applies If (ALL must hold)

- Adopting ClickUp OR auditing existing ClickUp workspace
- Team size 1-15
- Multiple workflow types in scope (eng + ops + sales) OR single but expanding

## Skip If (ANY kills it)

- Engineering-only team — Linear is a better fit
- Team size >25 — ClickUp gets unwieldy
- Already on Asana / Notion exclusively and not migrating

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Team roster + role list | table | people doc |
| Existing workspace / Spaces (if migrating) | list | ClickUp admin |
| Workflow inventory (one workflow per team segment) | doc | ops doc |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `solo/pm/pm-agile/linear-issue-tracking` | Peer methodology — comparison baseline; ClickUp picks here, Linear there. |
| `solo/pm/capacity-fit-calculator` | Peer methodology — capacity computation reads ClickUp time-estimates. |

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
| `draft-clickup-setup` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-clickup-setup` | haiku | Schema check + threshold checks; deterministic. |
| `review-clickup-setup` | opus | Cross-cycle synthesis; high-stakes change to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/clickup-setup.json` | JSON skeleton conforming to the output contract schema. |
| `templates/clickup-setup.md.j2` | Markdown skeleton for human-readable artefact rendering. |
| `templates/clickup-setup.md` | Markdown skeleton for human-readable artefact rendering. Generated from `templates/clickup-setup.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-clickup-setup.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[linear-issue-tracking-pm-agile]]
- [[capacity-fit-calculator]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/clickup-setup.json`

```json
{
  "artefact_id": "clickup-setup-2026-q2",
  "version": "1.0.0",
  "last_reviewed": "2026-05-23",
  "workspace_url": "https://app.clickup.com/123",
  "spaces": [
    "eng",
    "ops",
    "sales"
  ],
  "statuses": [
    "backlog",
    "todo",
    "in-progress",
    "blocked",
    "review",
    "done",
    "cancelled"
  ],
  "automations_count": 7,
  "clickapps": [
    "time-tracking",
    "custom-fields",
    "dependencies",
    "sprints"
  ],
  "views_per_list": 4,
  "owner": "@ruslan"
}
```
