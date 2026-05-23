# GitLab Issue Boards

## Summary

**One-sentence:** GitLab Issue Board configuration spec (labels, milestones, iteration cadence, scoped labels for status, list scoping by assignee/milestone, REST API for agent automation).

**One-paragraph:** GitLab Issue Board configuration spec (labels, milestones, iteration cadence, scoped labels for status, list scoping by assignee/milestone, REST API for agent automation).

**Ефективно для:**

- GitLab-first команд, що уже мають Repos/CI/CD в одному tenant.
- Open-source проектів з public issue tracking.
- Teams, що використовують scoped labels для статус-машини.
- Self-hosted GitLab організацій із data-residency constraints.

## Applies If (ALL must hold)

- Team uses GitLab as the source-of-truth for code AND issues.
- Scoped labels available (GitLab Premium+ or self-hosted EE).
- Iterations enabled at group/project level.
- Agent authenticated with project-scoped token (api scope minimum).

## Skip If (ANY kills it)

- Team primarily on GitHub — use GitHub Projects v2.
- Microsoft stack — use ADO Boards.
- Free-tier GitLab without scoped labels — board becomes label soup.
- &lt;10 issues per month — overhead exceeds value.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Scope brief | Markdown | engagement intake |
| Stakeholder roster | table | PM |
| Historical reference data | csv / log | PMO data warehouse |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[pm-tool-selection]] | Why GitLab was picked over alternatives. |

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
| `label-taxonomy-author` | sonnet | Design scoped-label taxonomy for status, type, priority. |
| `milestone-cadence-setter` | haiku | Emit milestone tree for chosen cadence. |
| `board-list-wirer` | haiku | Wire board lists to scoped labels. |
| `api-token-issuer` | haiku | Issue project-scoped API token with api+read_repository minimum. |

## Templates

| File | Purpose |
|------|---------|
| `templates/gitlab-board-config.yaml` | Board config: lists, labels, milestones, iterations, token scope. |
| `templates/scoped-labels.yaml` | Standard scoped-label taxonomy (status::, type::, priority::). |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-gitlab-boards.py` | Validate the output artefact against the schema | Pre-commit on every artefact change |

## Related

- [[jira-workflow-management]]
- [[azure-devops-boards]]
- [[pm-tool-selection]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observables (gitlab_tier, scoped_labels_available, issue_volume_per_month) to apply / fall-back / skip. Each leaf references a rule from `01-core-rules.xml`.
