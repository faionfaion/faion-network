# Azure DevOps Boards

## Summary

**One-sentence:** Azure DevOps Boards configuration spec (process template, hierarchy, board columns, WIP limits, area/iteration paths, REST API agent access) for Microsoft-stack enterprise teams.

**One-paragraph:** Microsoft's enterprise project management tool supporting four process templates (Basic, Agile, Scrum, CMMI) with a work-item hierarchy (Epic → Feature → User Story/PBI → Task), configurable Kanban boards, WIP limits, WIQL query language, and full REST API. Integrates natively with Azure Pipelines, Repos, and Test Plans. Agents operate via PAT-scoped REST API or `az boards` CLI; treat process-template definitions as YAML stored in version control.

**Ефективно для:**

- Microsoft-ecosystem організацій з Entra ID SSO + tenant governance.
- Regulated/audit-heavy проектів, що вимагають CMMI work-item types та повний audit trail.
- Команд із Azure Pipelines/Repos/Test Plans — Boards дає build, PR і release traceability.
- Portfolio reporting через Azure DevOps Analytics + Power BI.

## Applies If (ALL must hold)

- Organisation has an Azure DevOps Services or Server tenant with Entra ID.
- Team needs Boards + Pipelines/Repos integration (AB#&lt;id&gt; commit linking).
- Regulated workflow OR formal change-request governance required.
- Agents authenticated with scoped PAT (Work Items: Read &amp; Write, no Full-access).

## Skip If (ANY kills it)

- Pure GitHub stack — use GitHub Projects v2; avoid identity duplication.
- Engineering-only ≤10-person team — Linear is faster, lighter UI.
- Open-source or community project — ADO licensing assumes commercial accounts.
- Single-team lightweight Kanban — Trello / ClickUp ship in hours, not days.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| ADO project URL | `https://dev.azure.com/{org}/{project}` | platform admin |
| PAT (scoped: Work Items r/w, no full) | secret | 1Password / Azure Key Vault |
| Process template choice | enum {Basic, Agile, Scrum, CMMI} | governance decision |
| Area/Iteration tree | YAML | architecture team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[pm-tool-selection]] | Upstream decision picking ADO over Jira/Linear/etc. |
| [[jira-workflow-management]] | Peer reference for the alternative if Jira route is taken instead. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: template-inheritance, area-vs-iteration, WIP-limit, PAT-scope, AB-linking, skip-this-methodology | 950 |
| `content/02-output-contract.xml` | essential | JSON Schema for the config artefact (process, board columns, swimlanes, area/iteration tree) | 850 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 750 |
| `content/04-procedure.xml` | essential | 5-step procedure: pick template → import tree → configure board → wire PAT → validate | 800 |
| `content/06-decision-tree.xml` | essential | ADO vs alternatives + template choice routing | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `template-pick` | sonnet | Judgment over governance constraints vs team weight. |
| `tree-author` | haiku | Mechanical YAML emission for area/iteration tree. |
| `board-wire` | sonnet | WIP + swimlane + card-style synthesis. |
| `validate-and-commit` | haiku | Run the validator, commit the YAML. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ado-boards-config.yaml` | YAML skeleton for process + area/iteration + board columns + swimlanes. |
| `templates/wiql-saved-queries.yaml` | Example saved WIQL queries the team should ship from day 1. |
| `templates/sprint-planning.md.j2` | Sprint planning document — capacity, committed backlog, risks, DoD. |
| `templates/sprint-planning.md` | Sprint planning document — capacity, committed backlog, risks, DoD. Generated from `templates/sprint-planning.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/user-story.md.j2` | Azure DevOps user-story work item body (persona, criteria, dependencies). |
| `templates/user-story.md` | Azure DevOps user-story work item body (persona, criteria, dependencies). Generated from `templates/user-story.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-azure-devops-boards.py` | Validate the YAML config against the schema | Pre-commit on every config change |

## Related

- [[jira-workflow-management]]
- [[gitlab-boards]]
- [[pm-tool-selection]]
- [[cross-tool-migration]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps three observables (ecosystem ∈ Microsoft/GitHub/Atlassian, regulatory profile, team size) to apply / pick alternative / skip. Each leaf references a rule from `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/ado-boards-config.yaml`

```yaml
organization: REPLACE-org-slug
project: REPLACE-project-name
process_template: Agile   # Basic | Agile | Scrum | CMMI
area_tree:
  root: REPLACE-platform-root
  children:
    - REPLACE-team-a
    - REPLACE-team-b
iteration_tree:
  cadence: biweekly   # weekly | biweekly | monthly
  iterations:
    - REPLACE-2026-Q2-S1
    - REPLACE-2026-Q2-S2
board:
  columns:
    - name: New
      state_mapping: [New]
      wip_limit: null
    - name: Active
      state_mapping: [Active]
      wip_limit: 5
    - name: Resolved
      state_mapping: [Resolved]
      wip_limit: 3
    - name: Closed
      state_mapping: [Closed]
      wip_limit: null
  swimlanes:
    - Expedite
    - Default
    - Tech Debt
pat_scope_manifest:
  work_items_read_write: true
  full_access_forbidden: true
ab_linking_required: true
```

### `templates/wiql-saved-queries.yaml`

```yaml
queries:
  - name: My Active Work
    wiql: |
      SELECT [System.Id], [System.Title], [System.State]
      FROM WorkItems
      WHERE [System.AssignedTo] = @Me
        AND [System.State] IN ('Active', 'Resolved')
  - name: Over-WIP Active Cards
    wiql: |
      SELECT [System.Id], [System.Title], [System.AssignedTo]
      FROM WorkItems
      WHERE [System.State] = 'Active'
        AND [System.AreaPath] UNDER 'REPLACE-area-root'
  - name: Blocked Items (Tag-based)
    wiql: |
      SELECT [System.Id], [System.Title]
      FROM WorkItems
      WHERE [System.Tags] CONTAINS 'Blocked'
        AND [System.State] != 'Closed'
  - name: Missing AB-Link in Last 30d Commits
    description: |
      Use az repos pr list --status all | jq to find PRs without AB#<id> ref.
```
