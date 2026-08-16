# Jira Workflow Management

## Summary

**One-sentence:** Configure Jira projects for Scrum/Kanban/JSM teams: issue type schemes, workflow states/transitions, automation rules, JQL queries, board configuration, API token scope.

**One-paragraph:** Configure Jira projects for Scrum/Kanban/JSM teams: issue type schemes, workflow states/transitions, automation rules, JQL queries, board configuration, API token scope.

**Ефективно для:**

- Команд, що уже на Atlassian-стеку (Confluence + Jira + Bitbucket).
- Enterprise проектів, що потребують fine-grained permissions per role.
- JSM-команд, що поєднують service-desk з dev workflow.
- Scaled-Agile (SAFe) розгортань з кількома команд-рівнями.

## Applies If (ALL must hold)

- Team uses Atlassian Cloud or Data Center with admin access.
- Workflow customisation needed beyond default Scrum/Kanban.
- API token scoped to minimum (read:jira-work + write:jira-work).
- JQL queries can be authored or imported.

## Skip If (ANY kills it)

- &lt;10-person engineering-only team — Linear is faster.
- GitHub-first team — use GitHub Projects v2.
- Microsoft stack — use ADO Boards.
- Free-tier Jira with strict limits — workflow customisation blocked.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Scope brief | Markdown | engagement intake |
| Stakeholder roster | table | PM |
| Historical reference data | csv / log | PMO data warehouse |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[pm-tool-selection]] | Why Jira was picked. |
| [[change-control]] | Workflow changes routed through CR. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + `skip-this-methodology` | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden | 850 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 750 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Apply/skip routing on observable signals | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `issue-type-scheme-author` | sonnet | Design issue-type scheme + screens. |
| `workflow-designer` | sonnet | States + transitions + conditions + validators. |
| `automation-rule-author` | haiku | Emit Jira automation rule YAML. |
| `jql-query-author` | haiku | Compose saved JQL queries. |

## Templates

| File | Purpose |
|------|---------|
| `templates/jira-workflow.yaml` | Workflow definition: states, transitions, conditions, validators. |
| `templates/jql-queries.yaml` | Day-1 saved JQL queries. |
| `templates/automation-rules.yaml` | Automation rule set. |
| `templates/definition-of-done.md.j2` | Jira Definition of Done checklist — code, testing, docs, acceptance gates. |
| `templates/definition-of-done.md` | Jira Definition of Done checklist — code, testing, docs, acceptance gates. Generated from `templates/definition-of-done.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/sprint-plan.md.j2` | Sprint planning document — capacity, committed items, risks, sprint-level DoD. |
| `templates/sprint-plan.md` | Sprint planning document — capacity, committed items, risks, sprint-level DoD. Generated from `templates/sprint-plan.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-jira-workflow-management.py` | Validate the output artefact against the schema | Pre-commit on every artefact change |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[azure-devops-boards]]
- [[gitlab-boards]]
- [[pm-tool-selection]]
- [[cross-tool-migration]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observables (atlassian_tier, team_size, workflow_complexity) to apply / fall-back / skip. Each leaf references a rule from `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/jira-workflow.yaml`

```yaml
name: REPLACE-workflow-name
statuses:
  - name: To Do
    category: New
  - name: In Progress
    category: Indeterminate
  - name: Code Review
    category: Indeterminate
  - name: Done
    category: Done
transitions:
  - name: Start
    from: To Do
    to: In Progress
    conditions:
      - type: role
        role: Developers
  - name: Submit for review
    from: In Progress
    to: Code Review
    validators:
      - type: field-required
        field: pull_request
  - name: Approve
    from: Code Review
    to: Done
    conditions:
      - type: role
        role: Reviewers
```

### `templates/jql-queries.yaml`

```yaml
filters:
  - name: My Active
    jql: assignee = currentUser() AND statusCategory != Done
  - name: Sprint Burn
    jql: sprint in openSprints() AND project = REPLACE
  - name: Stale In-Progress
    jql: status = "In Progress" AND updated < -7d
  - name: Code Review Backlog
    jql: status = "Code Review" AND assignee in membersOf("Reviewers")
```

### `templates/automation-rules.yaml`

```yaml
rules:
  - name: auto-assign-bug
    scope: project
    rate_limit_per_min: 60
    trigger:
      type: issue-created
      jql: type = Bug
    action:
      type: assign
      to: lead-of(component)
  - name: stale-warn
    scope: project
    rate_limit_per_min: 30
    trigger:
      type: scheduled
      cron: "0 9 * * MON"
    action:
      type: comment
      body: "Stale > 7 days — please update or close."
```
