# Azure DevOps Boards

## Summary

**One-sentence:** Azure DevOps Boards project configuration: pick process template (Basic / Agile / Scrum / CMMI), set up area/iteration paths, WIQL queries, board columns, swimlanes.

**One-paragraph:** Azure DevOps Boards defines the testable methodology that turns the recurring work named in this skill into a repeatable, auditable artefact. The methodology is grounded in 6 core rules (see `content/01-core-rules.xml`), a JSON-Schema output contract, 4 catalogued failure modes, a 5-step procedure, and a decision tree whose leaves all reference a rule id.

**Ефективно для:**

- Microsoft-stack shop using Azure Pipelines / Repos / Test Plans already.
- Enterprise where CMMI compliance reporting is required.
- Multi-team setup with hierarchical area paths and iteration paths.
- Need queries that join work-items, builds, and releases via WIQL.

## Applies If (ALL must hold)

- Org has an Azure DevOps Services / Server tenant with a project provisioned.
- Project admin role (or higher) is available to choose the process template.
- Team agrees on Scrum / Agile / Basic / CMMI before configuration begins.
- Area + iteration hierarchies can be expressed as 2-3 levels.

## Skip If (ANY kills it)

- Team is already on Jira / Linear / GitHub Projects — switching has migration cost not warranted by Boards alone.
- Project is single-team, <5 people — Basic process is overkill; use any lightweight tool.
- Process template choice would force a rewrite of existing work-item types — defer to a migration ADR.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Source-of-truth data | tool export / sheet / API | upstream system named in this methodology |
| Prior cycle's artefact (if any) | json / md | repo / wiki where artefacts persist |
| Named consumer | person / agent | engagement charter |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies). |
| `pro/sdd/AGENTS.md` if present | SDD discipline for the artefact lifecycle (status flow, owners, review). |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft 2020-12) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `azure-devops-boards_template_fill` | haiku | Bounded template fill, no judgement. |
| `azure-devops-boards_evidence_check` | sonnet | Bounded comparison + judgement on anchored evidence. |
| `azure-devops-boards_synthesis` | opus | Cross-input synthesis + final write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema (draft 2020-12) for the Azure DevOps Boards configuration artefact. |
| `templates/create-story.sh` | Bash helper to create a User Story work item via REST API. |
| `templates/user-story.md` | Markdown template for a Scrum user story (As a / I want / So that, AC). |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-azure-devops-boards.py` | Validate the artefact against the schema in `content/02-output-contract.xml`. | CI on each artefact change; pre-commit. |

## Related

- parent skill: `pro/pm/` (see neighbouring methodologies).
- [[launch-raci-template]]
- [[reporting-basics]]
- external: industry references cited inline in `content/01-core-rules.xml`.

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input
preconditions, source-of-truth access, named-consumer presence) onto a concrete
verdict — apply the methodology, downgrade to draft, or skip — with each leaf
referencing a rule id from `content/01-core-rules.xml`.
