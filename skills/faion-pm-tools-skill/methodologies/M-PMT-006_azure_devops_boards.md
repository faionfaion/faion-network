# M-PMT-006: Azure DevOps Boards

## Metadata

| Field | Value |
|-------|-------|
| **ID** | M-PMT-006 |
| **Category** | PM Tools |
| **Difficulty** | Intermediate |
| **Agent** | faion-pm-agent |
| **Skill** | faion-pm-tools-skill |

---

## Problem

Enterprise teams using Azure DevOps need:
- Structured work item hierarchy (Epics, Features, Stories, Tasks)
- Sprint planning with velocity tracking
- Integration with Azure Pipelines and Repos
- Custom processes for specific workflows
- Advanced reporting and analytics

## Framework

### 1. Azure DevOps Hierarchy

**Organization structure:**

```
Organization (company)
└── Project (product/team)
    ├── Boards (work items)
    ├── Repos (Git)
    ├── Pipelines (CI/CD)
    ├── Test Plans
    └── Artifacts
```

**Work item hierarchy:**

```
Epic (strategic initiative)
└── Feature (capability)
    └── User Story / Product Backlog Item (PBI)
        └── Task (work)
            └── Bug (defect)
```

**Process templates:**

| Template | Best For | Hierarchy |
|----------|----------|-----------|
| **Agile** | Scrum teams | Epic → Feature → User Story → Task |
| **Scrum** | Pure Scrum | Epic → Feature → PBI → Task |
| **CMMI** | Regulated industries | Epic → Feature → Requirement → Task |
| **Basic** | Simple projects | Issue → Task |

### 2. Board Configuration

**Kanban board columns:**

```
New → Approved → Committed → In Progress → Review → Done
```

**Column configuration:**

| Column | WIP Limit | Definition of Done |
|--------|-----------|-------------------|
| New | - | Created, not triaged |
| Approved | 10 | Triaged, estimated |
| Committed | 8 | Assigned to sprint |
| In Progress | 5 | Active development |
| Review | 3 | PR submitted |
| Done | - | Deployed, accepted |

**Swimlanes:**

```
Board Configuration:
├── Swimlane: Expedite (priority)
├── Swimlane: Standard
└── Swimlane: Tech Debt
```

**Card styles:**

```yaml
# Highlight overdue items
- condition: "Due Date < @Today"
  style:
    backgroundColor: "#FFB6C1"  # Light red

# Highlight blocked items
- condition: "Tags contains 'Blocked'"
  style:
    backgroundColor: "#FFA500"  # Orange
    titleColor: "#FFFFFF"
```

### 3. Sprints and Iterations

**Iteration path structure:**

```
Project\
├── Backlog
├── 2026\
│   ├── Q1\
│   │   ├── Sprint 1 (Jan 1-14)
│   │   ├── Sprint 2 (Jan 15-28)
│   │   └── Sprint 3 (Jan 29 - Feb 11)
│   └── Q2\
│       ├── Sprint 7
│       └── ...
```

**Sprint planning:**

| Element | Description |
|---------|-------------|
| Capacity | Team hours available |
| Velocity | Average points/sprint |
| Forecast | When backlog completes |

**Setting team capacity:**

```
Team Member: Alice
├── Days Off: Jan 20
├── Capacity per Day: 6 hours
├── Activity: Development (100%)

Team Member: Bob
├── Days Off: None
├── Capacity per Day: 6 hours
├── Activity: Development (70%), Testing (30%)
```

### 4. Queries

**WIQL (Work Item Query Language):**

```sql
-- My active work items
SELECT [System.Id], [System.Title], [System.State]
FROM WorkItems
WHERE [System.AssignedTo] = @Me
  AND [System.State] <> 'Done'
  AND [System.State] <> 'Closed'
ORDER BY [Microsoft.VSTS.Common.Priority] ASC

-- Sprint backlog
SELECT [System.Id], [System.Title], [System.State], [System.AssignedTo]
FROM WorkItems
WHERE [System.IterationPath] = @CurrentIteration
  AND [System.WorkItemType] IN ('User Story', 'Bug', 'Task')
ORDER BY [Microsoft.VSTS.Common.BacklogPriority] ASC

-- Bugs by severity
SELECT [System.Id], [System.Title], [Microsoft.VSTS.Common.Severity]
FROM WorkItems
WHERE [System.WorkItemType] = 'Bug'
  AND [System.State] <> 'Closed'
ORDER BY [Microsoft.VSTS.Common.Severity] ASC

-- Stale items (not updated in 7 days)
SELECT [System.Id], [System.Title], [System.ChangedDate]
FROM WorkItems
WHERE [System.State] = 'In Progress'
  AND [System.ChangedDate] < @Today - 7
ORDER BY [System.ChangedDate] ASC

-- Items without estimates
SELECT [System.Id], [System.Title]
FROM WorkItems
WHERE [System.WorkItemType] = 'User Story'
  AND [Microsoft.VSTS.Scheduling.StoryPoints] = ''
  AND [System.State] <> 'Done'
```

**Query folders:**

```
Shared Queries/
├── Team/
│   ├── Sprint Backlog
│   ├── Active Bugs
│   └── Blocked Items
├── Reporting/
│   ├── Velocity
│   └── Bug Trends
└── Personal/
    └── My Work
```

### 5. REST API

**Authentication:**

```bash
# Personal Access Token (Base64)
PAT="user:pat_token"
AUTH=$(echo -n $PAT | base64)

curl -X GET \
  -H "Authorization: Basic $AUTH" \
  "https://dev.azure.com/{org}/{project}/_apis/wit/workitems/123?api-version=7.1"
```

**Common operations:**

```python
import requests
import base64

class AzureDevOpsClient:
    def __init__(self, org: str, project: str, pat: str):
        self.org = org
        self.project = project
        self.base_url = f"https://dev.azure.com/{org}/{project}"
        auth = base64.b64encode(f":{pat}".encode()).decode()
        self.headers = {
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/json"
        }

    def _get(self, endpoint: str, params: dict = None):
        url = f"{self.base_url}/_apis{endpoint}"
        params = params or {}
        params["api-version"] = "7.1"
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def _post(self, endpoint: str, data):
        url = f"{self.base_url}/_apis{endpoint}?api-version=7.1"
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def _patch(self, endpoint: str, data):
        url = f"{self.base_url}/_apis{endpoint}?api-version=7.1"
        headers = {**self.headers, "Content-Type": "application/json-patch+json"}
        response = requests.patch(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    # Work Items
    def get_work_item(self, id: int, expand: str = "all"):
        return self._get(f"/wit/workitems/{id}", {"$expand": expand})

    def create_work_item(self, work_item_type: str, fields: dict):
        """Create work item using JSON Patch format"""
        data = [
            {"op": "add", "path": f"/fields/{key}", "value": value}
            for key, value in fields.items()
        ]
        return self._post(f"/wit/workitems/${work_item_type}", data)

    def update_work_item(self, id: int, updates: dict):
        """Update work item fields"""
        data = [
            {"op": "add", "path": f"/fields/{key}", "value": value}
            for key, value in updates.items()
        ]
        return self._patch(f"/wit/workitems/{id}", data)

    # Queries
    def run_query(self, wiql: str):
        """Run WIQL query"""
        data = {"query": wiql}
        result = self._post("/wit/wiql", data)
        return result

    def get_query_results(self, wiql: str, fields: list = None):
        """Run query and fetch work items"""
        query_result = self.run_query(wiql)
        if not query_result.get("workItems"):
            return []

        ids = [wi["id"] for wi in query_result["workItems"][:200]]
        fields = fields or ["System.Id", "System.Title", "System.State"]

        return self._get("/wit/workitems", {
            "ids": ",".join(map(str, ids)),
            "fields": ",".join(fields)
        })["value"]

    # Iterations
    def get_iterations(self, team: str = None):
        team = team or f"{self.project} Team"
        return self._get(f"/{team}/_apis/work/teamsettings/iterations")

    def get_current_iteration(self, team: str = None):
        iterations = self.get_iterations(team)
        for iteration in iterations.get("value", []):
            if iteration.get("attributes", {}).get("timeFrame") == "current":
                return iteration
        return None


# Usage
client = AzureDevOpsClient("my-org", "my-project", "pat_token")

# Get work item
item = client.get_work_item(123)
print(f"{item['id']}: {item['fields']['System.Title']}")

# Create user story
new_story = client.create_work_item("User Story", {
    "System.Title": "Implement OAuth login",
    "System.Description": "Add Google OAuth support",
    "Microsoft.VSTS.Scheduling.StoryPoints": 5,
    "System.AreaPath": "MyProject\\Backend",
    "System.IterationPath": "MyProject\\2026\\Q1\\Sprint 1"
})

# Query active bugs
bugs = client.get_query_results("""
    SELECT [System.Id], [System.Title], [Microsoft.VSTS.Common.Severity]
    FROM WorkItems
    WHERE [System.WorkItemType] = 'Bug'
      AND [System.State] <> 'Closed'
""")

# Update work item
client.update_work_item(123, {
    "System.State": "In Progress",
    "System.AssignedTo": "alice@company.com"
})
```

### 6. Azure Pipelines Integration

**Auto-update work items on build:**

```yaml
# azure-pipelines.yml
trigger:
  - main

pool:
  vmImage: 'ubuntu-latest'

steps:
  - task: UpdateWorkItem@1
    inputs:
      workItemId: '$(workItemId)'
      updateRule: |
        {
          "System.State": "In Progress"
        }
    condition: succeeded()

  - script: echo "Build completed"

  - task: UpdateWorkItem@1
    inputs:
      workItemId: '$(workItemId)'
      updateRule: |
        {
          "System.State": "Done",
          "System.History": "Deployed in build $(Build.BuildNumber)"
        }
    condition: succeeded()
```

**Link work items to builds:**

```yaml
# Commit message triggers
git commit -m "Fixed login bug #123"
git commit -m "Implements feature AB#456"
```

**Release gates:**

```yaml
# Check work item state before deploy
- task: QueryWorkItems@0
  inputs:
    queryType: 'wiql'
    query: |
      SELECT [System.Id]
      FROM WorkItems
      WHERE [System.WorkItemType] = 'Bug'
        AND [System.State] = 'Active'
        AND [System.Tags] CONTAINS 'Release-Blocker'
    failOnEmpty: false
```

### 7. Analytics and Reporting

**Built-in widgets:**

| Widget | Purpose | Data Source |
|--------|---------|-------------|
| Burndown | Sprint progress | Iteration |
| Velocity | Story points trend | Completed work |
| Cumulative Flow | Work item states over time | Board |
| Lead Time | Time from created to done | Work items |
| Cycle Time | Time in active states | Work items |

**Power BI integration:**

```
Data Connection:
├── Connect: Analytics views
├── Select: Stories completed
├── Fields:
│   ├── Date
│   ├── Story Points
│   ├── State
│   └── Iteration Path
└── Visualization: Trend chart
```

**Custom analytics views:**

```yaml
# Create custom view
Name: "Sprint Metrics"
Work items:
  - User Story
  - Bug
Fields:
  - Work Item ID
  - Title
  - State
  - Story Points
  - Completed Date
  - Cycle Time Days
History:
  - Rolling 30 days
```

---

## Templates

### Project Setup Checklist

```markdown
## Azure DevOps Project Setup

### Project Configuration
- [ ] Project created with correct process template
- [ ] Team(s) configured
- [ ] Area paths defined
- [ ] Iteration paths created (sprints)

### Board Configuration
- [ ] Columns configured
- [ ] WIP limits set
- [ ] Swimlanes defined
- [ ] Card styles configured
- [ ] Definition of Done for each column

### Work Item Customization
- [ ] Custom fields added (if needed)
- [ ] Work item templates created
- [ ] Rules configured

### Queries
- [ ] Sprint backlog query
- [ ] Active bugs query
- [ ] My work query
- [ ] Query folders organized

### Dashboards
- [ ] Team dashboard created
- [ ] Burndown widget added
- [ ] Velocity widget added
- [ ] Bug trends widget added

### Integrations
- [ ] Azure Repos linked
- [ ] Azure Pipelines configured
- [ ] Slack/Teams notifications
- [ ] Work item linking rules
```

### Work Item Templates

**User Story template:**

```markdown
## Description
As a [user type], I want [capability] so that [benefit].

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Technical Notes
<!-- Implementation details -->

## Design
<!-- Link to designs or mockups -->

## Dependencies
<!-- Related work items or external dependencies -->
```

**Bug template:**

```markdown
## Summary
<!-- Brief description -->

## Environment
- OS:
- Browser:
- Build Version:

## Steps to Reproduce
1.
2.
3.

## Expected Result
<!-- What should happen -->

## Actual Result
<!-- What actually happens -->

## Severity
- [ ] 1 - Critical (system down)
- [ ] 2 - High (major feature broken)
- [ ] 3 - Medium (workaround exists)
- [ ] 4 - Low (cosmetic)

## Screenshots/Logs
<!-- Attach evidence -->
```

---

## Examples

### Example 1: Scrum Team Setup

**Project:** ProductApp (Scrum process)

**Team:** ProductApp Team (8 members)

**Iterations:**
```
ProductApp\
├── 2026\
│   ├── Sprint 1 (Jan 1-14)
│   ├── Sprint 2 (Jan 15-28)
│   ├── Sprint 3 (Jan 29 - Feb 11)
│   └── ...
```

**Board columns:**
| New | Approved | Committed | Active | Resolved | Closed |
|-----|----------|-----------|--------|----------|--------|

**Capacity planning:**
- Sprint length: 2 weeks
- Team velocity: 40 story points
- Daily capacity: 6 hours/person

### Example 2: Enterprise Multi-Team

**Project:** EnterpriseProduct

**Teams:**
- Platform Team (Area: Platform)
- Mobile Team (Area: Mobile)
- QA Team (Area: Testing)

**Shared iterations:**
```
EnterpriseProduct\
├── Release 2.0\
│   ├── Sprint 2.0.1
│   ├── Sprint 2.0.2
│   └── Sprint 2.0.3
```

**Portfolio-level:**
- Epics managed at portfolio level
- Features assigned to teams
- Delivery Plans for cross-team visibility

---

## Common Mistakes

| Mistake | Impact | Solution |
|---------|--------|----------|
| Wrong process template | Mismatched hierarchy | Choose template carefully upfront |
| No iteration paths | No sprint planning | Create iteration hierarchy |
| Missing capacity | Poor planning | Set team capacity |
| Complex queries | Slow performance | Simplify, use indexed fields |
| No work item links | Lost traceability | Link PRs, commits, builds |

---

## Next Steps

1. Create project with appropriate process template
2. Set up team and iteration paths
3. Configure board columns and WIP limits
4. Create standard queries
5. Set up dashboard with key widgets
6. Configure pipeline integration

---

## Related Methodologies

- M-PMT-004: GitHub Projects
- M-PMT-005: GitLab Boards
- M-PMT-009: Cross-Tool Migration
- M-PMT-012: Reporting & Dashboards
