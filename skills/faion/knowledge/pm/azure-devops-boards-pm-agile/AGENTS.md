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

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

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
| `templates/user-story.md.j2` | Markdown template for a Scrum user story (As a / I want / So that, AC). |
| `templates/user-story.md` | Markdown template for a Scrum user story (As a / I want / So that, AC). Generated from `templates/user-story.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `pro/pm/` (see neighbouring methodologies).
- [[launch-raci-template]]
- [[reporting-basics]]
- external: industry references cited inline in `content/01-core-rules.xml`.

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input
preconditions, source-of-truth access, named-consumer presence) onto a concrete
verdict — apply the methodology, downgrade to draft, or skip — with each leaf
referencing a rule id from `content/01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/output-schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.net/schemas/azure-devops-boards.json",
  "type": "object",
  "required": [
    "project_id",
    "process_template",
    "area_paths",
    "iteration_paths",
    "boards"
  ],
  "properties": {
    "project_id": {
      "type": "string"
    },
    "process_template": {
      "enum": [
        "Basic",
        "Agile",
        "Scrum",
        "CMMI"
      ]
    },
    "area_paths": {
      "type": "array",
      "minItems": 1
    },
    "iteration_paths": {
      "type": "array",
      "minItems": 1
    },
    "boards": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "team",
          "columns"
        ],
        "properties": {
          "team": {
            "type": "string"
          },
          "columns": {
            "type": "array",
            "minItems": 2,
            "items": {
              "type": "object",
              "required": [
                "name",
                "state"
              ]
            }
          },
          "swimlanes": {
            "type": "array"
          }
        }
      }
    },
    "shared_queries": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "path",
          "wiql"
        ]
      }
    }
  }
}
```

### `templates/create-story.sh`

```bash
# create-story.sh — create a User Story work item via Azure DevOps REST API.
#
# Required environment variables:
#   ADO_ORG   — organization name (e.g. myorg)
#   ADO_PROJ  — project name (e.g. MyProject)
#   ADO_PAT   — Personal Access Token (api scope)
#
# Usage:
#   ADO_ORG=myorg ADO_PROJ=MyProject ADO_PAT=<token> \
#       bash create-story.sh "Title of story" "MyProject\\Release 1\\Sprint 1" "MyProject\\Backend"
#
# Arguments:
#   $1  Title
#   $2  Iteration path (backslash-separated, e.g. "MyProject\\Sprint 1")
#   $3  Area path (backslash-separated, e.g. "MyProject\\Backend")
set -euo pipefail

ORG="${ADO_ORG:?ADO_ORG required}"
PROJ="${ADO_PROJ:?ADO_PROJ required}"
PAT="${ADO_PAT:?ADO_PAT required}"

TITLE="${1:?Argument 1: title required}"
ITERATION="${2:?Argument 2: iteration_path required}"
AREA="${3:?Argument 3: area_path required}"

B64=$(printf ':%s' "$PAT" | base64 -w0)

curl -fsS -X POST \
  -H "Content-Type: application/json-patch+json" \
  -H "Authorization: Basic $B64" \
  -d "[
    {\"op\":\"add\",\"path\":\"/fields/System.Title\",\"value\":\"$TITLE\"},
    {\"op\":\"add\",\"path\":\"/fields/System.IterationPath\",\"value\":\"$ITERATION\"},
    {\"op\":\"add\",\"path\":\"/fields/System.AreaPath\",\"value\":\"$AREA\"}
  ]" \
  "https://dev.azure.com/${ORG}/${PROJ}/_apis/wit/workitems/\$User%20Story?api-version=7.0"
```
