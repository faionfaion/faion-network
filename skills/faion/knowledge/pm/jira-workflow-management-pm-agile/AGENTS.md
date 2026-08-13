# Jira Workflow Management

## Summary

**One-sentence:** Jira project setup config: issue-type scheme, workflow state machine, transition rules, automation policies, JQL conventions for Scrum and Kanban teams.

**One-paragraph:** Jira Workflow Management defines the testable methodology that turns the recurring work named in this skill into a repeatable, auditable artefact. The methodology is grounded in 6 core rules (see `content/01-core-rules.xml`), a JSON-Schema output contract, 4 catalogued failure modes, a 5-step procedure, and a decision tree whose leaves all reference a rule id.

**Ефективно для:**

- Atlassian-stack shops using Jira Cloud or Server as the primary tracker.
- Multi-team programs where workflow consistency matters across boards.
- Teams whose automation needs go beyond default Jira behaviour (cross-issue links, SLA timers).
- Engineers building dashboards on JQL queries that must remain stable.

## Applies If (ALL must hold)

- Jira admin role available for workflow + scheme changes.
- Team has agreed on a single workflow per issue-type (Story, Bug, Task, Epic).
- Naming convention for projects + components has been decided up-front.
- Automation rules budget (Jira Cloud free tier limits) is acceptable.

## Skip If (ANY kills it)

- Team is migrating to Linear / GitHub Projects — defer Jira config to the migration ADR.
- Single-team, <10 issues/week — default Jira workflows are good enough.
- Workflow change would require migrating thousands of existing issues — defer to a migration plan.

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
| `jira-workflow-management_template_fill` | haiku | Bounded template fill, no judgement. |
| `jira-workflow-management_evidence_check` | sonnet | Bounded comparison + judgement on anchored evidence. |
| `jira-workflow-management_synthesis` | opus | Cross-input synthesis + final write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema (draft 2020-12) for the Jira workflow configuration artefact. |
| `templates/workflow-states.yaml` | Canonical Scrum + Kanban workflow states + transitions in YAML. |
| `templates/bulk-transition.py` | Reference script for safe bulk transitions via Jira REST API. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

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

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/output-schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.net/schemas/jira-workflow-management.json",
  "type": "object",
  "required": [
    "project_id",
    "issue_types",
    "workflow",
    "automation_rules",
    "shared_filters"
  ],
  "properties": {
    "project_id": {
      "type": "string"
    },
    "issue_types": {
      "type": "array",
      "minItems": 2,
      "items": {
        "type": "object",
        "required": [
          "name",
          "workflow_id"
        ]
      }
    },
    "workflow": {
      "type": "object",
      "required": [
        "statuses",
        "transitions"
      ],
      "properties": {
        "statuses": {
          "type": "array",
          "items": {
            "type": "object",
            "required": [
              "name",
              "category"
            ],
            "properties": {
              "category": {
                "enum": [
                  "to-do",
                  "in-progress",
                  "done"
                ]
              }
            }
          }
        },
        "transitions": {
          "type": "array",
          "items": {
            "type": "object",
            "required": [
              "from",
              "to",
              "name"
            ]
          }
        }
      }
    },
    "automation_rules": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "namespace",
          "version",
          "trigger",
          "action"
        ]
      }
    },
    "shared_filters": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "id",
          "jql",
          "owner"
        ]
      }
    }
  }
}
```

### `templates/workflow-states.yaml`

```yaml
# Standard development workflow states and transitions for Jira.
# Use as input to workflow-author agent or import via Jira admin API.
# Maximum 7 statuses; every transition has a screen; no global transition to Done.

statuses:
  - name: "To Do"
    category: "To Do"
  - name: "In Progress"
    category: "In Progress"
  - name: "Code Review"
    category: "In Progress"
  - name: "QA Testing"
    category: "In Progress"
  - name: "Done"
    category: "Done"

transitions:
  - name: "Start Work"
    from: ["To Do"]
    to: "In Progress"
    screen: "Transition Screen"
    validators:
      - type: "FieldRequired"
        field: "Assignee"

  - name: "Submit for Review"
    from: ["In Progress"]
    to: "Code Review"
    screen: "Review Screen"
    validators:
      - type: "FieldRequired"
        field: "Story Points"

  - name: "Request Changes"
    from: ["Code Review"]
    to: "In Progress"
    screen: "Transition Screen"

  - name: "Approve"
    from: ["Code Review"]
    to: "QA Testing"
    screen: "Transition Screen"

  - name: "Fail QA"
    from: ["QA Testing"]
    to: "In Progress"
    screen: "QA Feedback Screen"

  - name: "Pass QA"
    from: ["QA Testing"]
    to: "Done"
    screen: "Done Screen"
    validators:
      - type: "FieldRequired"
        field: "Resolution"
```

### `templates/bulk-transition.py`

```python
"""


"""bulk_jql_transition.py — bulk-transition Jira issues matching a JQL query.

Rate-limited to 5 req/s with Retry-After handling.

Usage:
    JIRA_USER=me@example.com JIRA_TOKEN=<api_token> JIRA_BASE=https://myorg.atlassian.net \\
        python3 bulk-transition.py "project = PROJ AND status = 'To Do'" "21"

Arguments:
    jql        JQL query identifying issues to transition
    tid        Transition ID (get from /rest/api/3/issue/{key}/transitions)
"""
from __future__ import annotations

import os
import sys
import time

import requests

S = requests.Session()
S.auth = (os.environ["JIRA_USER"], os.environ["JIRA_TOKEN"])
BASE = os.environ["JIRA_BASE"].rstrip("/")


def transition(key: str, tid: str) -> None:
    r = S.post(
        f"{BASE}/rest/api/3/issue/{key}/transitions",
        json={"transition": {"id": tid}},
    )
    if r.status_code == 429:
        wait = int(r.headers.get("Retry-After", 5))
        time.sleep(wait)
        return transition(key, tid)
    r.raise_for_status()


def main() -> int:
    jql = sys.argv[1]
    tid = sys.argv[2]
    start_at = 0
    total_done = 0

    while True:
        r = S.get(
            f"{BASE}/rest/api/3/search",
            params={
                "jql": jql,
                "fields": "key",
                "startAt": start_at,
                "maxResults": 100,
            },
        )
        r.raise_for_status()
        data = r.json()
        issues = data["issues"]
        if not issues:
            break
        for it in issues:
            key = it["key"]
            transition(key, tid)
            total_done += 1
            print(f"  transitioned {key} ({total_done})")
            time.sleep(0.2)  # max ~5 req/s
        start_at += len(issues)
        if start_at >= data["total"]:
            break

    print(f"Done. Transitioned {total_done} issues.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```
