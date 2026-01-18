# M-PMT-004: GitHub Projects

## Metadata

| Field | Value |
|-------|-------|
| **ID** | M-PMT-004 |
| **Category** | PM Tools |
| **Difficulty** | Beginner |
| **Agent** | faion-pm-agent |
| **Skill** | faion-pm-tools-skill |

---

## Problem

Development teams using GitHub need project management that:
- Lives where their code lives
- Integrates automatically with PRs and issues
- Provides roadmap visibility without external tools
- Supports both Kanban and sprint-based workflows

## Framework

### 1. GitHub Projects V2 Architecture

**Structure:**

```
Organization/User
└── Project (board)
    ├── View 1: Board (Kanban)
    ├── View 2: Table (spreadsheet)
    ├── View 3: Roadmap (timeline)
    └── Items
        ├── Issues (from repos)
        ├── Pull Requests
        └── Draft Issues (ideas)
```

**Project types:**

| Type | Best For | Features |
|------|----------|----------|
| **Organization** | Team-wide | Cross-repo, team access |
| **User** | Personal | Private projects |
| **Repository** | Repo-specific | Limited to one repo |

### 2. Board Setup

**Default columns (Status field):**

```
No Status → Backlog → Todo → In Progress → In Review → Done
```

**Custom status options:**

```
Planning:
├── Idea
├── Researching
└── Spec Review

Development:
├── Ready
├── In Progress
├── Blocked
└── Code Review

Deployment:
├── Staging
├── Production
└── Done
```

**Board configuration:**

```yaml
# Board settings
columns:
  - name: "Backlog"
    limit: null
  - name: "Todo"
    limit: 10
  - name: "In Progress"
    limit: 5
  - name: "In Review"
    limit: 3
  - name: "Done"
    limit: null

filters:
  default: "is:open"

sorting:
  field: "Priority"
  direction: "desc"
```

### 3. Custom Fields

**Built-in fields:**

| Field | Type | Auto-populated |
|-------|------|----------------|
| Status | Single select | No |
| Assignees | People | From issue |
| Labels | Labels | From issue |
| Milestone | Milestone | From issue |
| Repository | Repository | From issue |
| Linked PRs | Number | Auto |

**Recommended custom fields:**

| Field | Type | Purpose |
|-------|------|---------|
| Priority | Single select | P0, P1, P2, P3 |
| Size | Single select | XS, S, M, L, XL |
| Sprint | Iteration | Time-boxed work |
| Estimate | Number | Story points |
| Due Date | Date | Deadline |
| Team | Single select | Team assignment |

**Priority configuration:**

```yaml
Priority:
  options:
    - name: "P0 - Critical"
      color: red
      description: "Production issue, drop everything"
    - name: "P1 - High"
      color: orange
      description: "This sprint, blocking"
    - name: "P2 - Medium"
      color: yellow
      description: "This sprint, normal"
    - name: "P3 - Low"
      color: blue
      description: "Next sprint or later"
```

### 4. Views

**Board view (Kanban):**

```
Use case: Daily work management
Group by: Status
Sort by: Priority (desc), then Created (asc)
Filters: is:open, assignee:@me
```

**Table view (Spreadsheet):**

```
Use case: Planning, bulk editing
Columns: Title, Status, Assignee, Priority, Size, Sprint
Sort by: Sprint, Priority
Filters: Sprint = current
```

**Roadmap view (Timeline):**

```
Use case: Release planning
Date field: Due Date or Sprint dates
Group by: Milestone or Release
Zoom: Months
```

**Creating views for different needs:**

| View Name | Type | Filter | Group By |
|-----------|------|--------|----------|
| My Work | Board | `assignee:@me` | Status |
| Sprint Board | Board | `Sprint:current` | Status |
| Backlog | Table | `Status:Backlog,Todo` | Priority |
| Roadmap Q1 | Roadmap | `Milestone:Q1-2026` | Milestone |
| Bugs | Board | `label:bug` | Priority |
| Team Alpha | Board | `Team:Alpha` | Status |

### 5. Automations (Built-in)

**Available automations:**

| Trigger | Action | Use Case |
|---------|--------|----------|
| Item added | Set Status | Auto-triage |
| Item reopened | Set Status to Todo | Reopen workflow |
| Item closed | Set Status to Done | Auto-close |
| PR merged | Set Status to Done | Deploy workflow |
| Code review requested | Set Status to In Review | PR workflow |

**Automation setup:**

```yaml
# When issue is added to project
- trigger: item_added
  conditions:
    - item_type: issue
  actions:
    - set_field:
        field: Status
        value: Backlog
    - set_field:
        field: Priority
        value: P2 - Medium

# When PR is merged
- trigger: pull_request.merged
  actions:
    - set_field:
        field: Status
        value: Done

# When assigned
- trigger: issue.assigned
  conditions:
    - status: Backlog
  actions:
    - set_field:
        field: Status
        value: Todo
```

### 6. GitHub CLI and API

**GitHub CLI (gh) commands:**

```bash
# List projects
gh project list --owner ORG_NAME

# View project
gh project view PROJECT_NUMBER --owner ORG_NAME

# Create project
gh project create --owner ORG_NAME --title "Q1 2026 Roadmap"

# Add issue to project
gh project item-add PROJECT_NUMBER --owner ORG_NAME --url ISSUE_URL

# Edit item field
gh project item-edit --project-id PROJECT_ID --id ITEM_ID \
  --field-id FIELD_ID --single-select-option-id OPTION_ID

# List project items
gh project item-list PROJECT_NUMBER --owner ORG_NAME --format json
```

**GraphQL API:**

```graphql
# Get project with items
query GetProject($org: String!, $number: Int!) {
  organization(login: $org) {
    projectV2(number: $number) {
      id
      title
      items(first: 100) {
        nodes {
          id
          content {
            ... on Issue {
              title
              number
              state
              assignees(first: 5) {
                nodes { login }
              }
            }
            ... on PullRequest {
              title
              number
              state
            }
          }
          fieldValues(first: 10) {
            nodes {
              ... on ProjectV2ItemFieldSingleSelectValue {
                name
                field { ... on ProjectV2SingleSelectField { name } }
              }
              ... on ProjectV2ItemFieldDateValue {
                date
                field { ... on ProjectV2Field { name } }
              }
            }
          }
        }
      }
    }
  }
}

# Add item to project
mutation AddItemToProject($projectId: ID!, $contentId: ID!) {
  addProjectV2ItemById(input: {
    projectId: $projectId
    contentId: $contentId
  }) {
    item {
      id
    }
  }
}

# Update item field
mutation UpdateItemField($projectId: ID!, $itemId: ID!,
                          $fieldId: ID!, $value: ProjectV2FieldValue!) {
  updateProjectV2ItemFieldValue(input: {
    projectId: $projectId
    itemId: $itemId
    fieldId: $fieldId
    value: $value
  }) {
    projectV2Item {
      id
    }
  }
}
```

**Python client:**

```python
import subprocess
import json

class GitHubProjectClient:
    def __init__(self, org: str, project_number: int):
        self.org = org
        self.project_number = project_number

    def _run_gh(self, args: list) -> dict:
        result = subprocess.run(
            ["gh"] + args,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise Exception(result.stderr)
        return json.loads(result.stdout) if result.stdout else {}

    def list_items(self) -> list:
        """List all project items"""
        return self._run_gh([
            "project", "item-list",
            str(self.project_number),
            "--owner", self.org,
            "--format", "json"
        ])["items"]

    def add_issue(self, issue_url: str) -> dict:
        """Add issue to project"""
        return self._run_gh([
            "project", "item-add",
            str(self.project_number),
            "--owner", self.org,
            "--url", issue_url,
            "--format", "json"
        ])

    def get_field_id(self, field_name: str) -> str:
        """Get field ID by name"""
        fields = self._run_gh([
            "project", "field-list",
            str(self.project_number),
            "--owner", self.org,
            "--format", "json"
        ])
        for field in fields["fields"]:
            if field["name"] == field_name:
                return field["id"]
        raise ValueError(f"Field '{field_name}' not found")

    def update_item_status(self, item_id: str, status: str):
        """Update item status"""
        # Get project and field IDs first
        project_id = self._get_project_id()
        field_id = self.get_field_id("Status")
        option_id = self._get_option_id(field_id, status)

        return self._run_gh([
            "project", "item-edit",
            "--project-id", project_id,
            "--id", item_id,
            "--field-id", field_id,
            "--single-select-option-id", option_id
        ])

# Usage
client = GitHubProjectClient("my-org", 1)
items = client.list_items()
client.add_issue("https://github.com/my-org/repo/issues/123")
```

### 7. GitHub Actions Integration

**Auto-add issues to project:**

```yaml
name: Add Issue to Project

on:
  issues:
    types: [opened]

jobs:
  add-to-project:
    runs-on: ubuntu-latest
    steps:
      - name: Add to project
        uses: actions/add-to-project@v0.5.0
        with:
          project-url: https://github.com/orgs/ORG/projects/1
          github-token: ${{ secrets.PROJECT_TOKEN }}
          labeled: bug, feature
          label-operator: OR
```

**Update status on PR merge:**

```yaml
name: Update Project on Merge

on:
  pull_request:
    types: [closed]

jobs:
  update-project:
    if: github.event.pull_request.merged == true
    runs-on: ubuntu-latest
    steps:
      - name: Get linked issues
        id: issues
        uses: actions/github-script@v7
        with:
          script: |
            const body = context.payload.pull_request.body || '';
            const matches = body.match(/(?:closes|fixes|resolves)\s+#(\d+)/gi);
            return matches ? matches.map(m => m.match(/\d+/)[0]) : [];

      - name: Update project items
        uses: actions/github-script@v7
        with:
          script: |
            const issues = ${{ steps.issues.outputs.result }};
            for (const issueNumber of issues) {
              // Update project item status to Done
              // Implementation depends on your project setup
            }
```

---

## Templates

### Project Setup Checklist

```markdown
## GitHub Project Setup

### Project Configuration
- [ ] Project created (org or repo level)
- [ ] Title and description set
- [ ] README added

### Fields
- [ ] Status field configured
- [ ] Priority field added
- [ ] Size/Estimate field added
- [ ] Sprint/Iteration field added
- [ ] Due Date field added

### Views
- [ ] Board view (default)
- [ ] Table view for planning
- [ ] Roadmap view for timeline
- [ ] My Work view (filtered)

### Automations
- [ ] Auto-set status on add
- [ ] Auto-move on PR merge
- [ ] Auto-assign on status change

### Integrations
- [ ] GitHub Actions workflows
- [ ] Branch protection rules
- [ ] Required reviews

### Documentation
- [ ] Project README
- [ ] Issue templates
- [ ] PR template
```

### Issue Templates

**.github/ISSUE_TEMPLATE/bug_report.yml:**

```yaml
name: Bug Report
description: Report a bug
labels: [bug, triage]
projects: ["org/1"]
body:
  - type: textarea
    id: description
    attributes:
      label: Description
      description: Clear description of the bug
    validations:
      required: true

  - type: textarea
    id: steps
    attributes:
      label: Steps to Reproduce
      value: |
        1. Go to '...'
        2. Click on '...'
        3. See error
    validations:
      required: true

  - type: dropdown
    id: severity
    attributes:
      label: Severity
      options:
        - Critical (P0)
        - High (P1)
        - Medium (P2)
        - Low (P3)
    validations:
      required: true

  - type: textarea
    id: environment
    attributes:
      label: Environment
      value: |
        - OS:
        - Browser:
        - Version:
```

**.github/ISSUE_TEMPLATE/feature_request.yml:**

```yaml
name: Feature Request
description: Suggest a new feature
labels: [enhancement, triage]
projects: ["org/1"]
body:
  - type: textarea
    id: problem
    attributes:
      label: Problem
      description: What problem does this solve?
    validations:
      required: true

  - type: textarea
    id: solution
    attributes:
      label: Proposed Solution
      description: How should it work?
    validations:
      required: true

  - type: textarea
    id: alternatives
    attributes:
      label: Alternatives Considered
      description: Other solutions you considered

  - type: dropdown
    id: priority
    attributes:
      label: Priority
      options:
        - High - Critical for business
        - Medium - Important but not urgent
        - Low - Nice to have
```

---

## Examples

### Example 1: Open Source Project

**Project:** Feature Roadmap

**Views:**
- Board: Community contributions by status
- Roadmap: Release milestones
- Table: All issues with metadata

**Fields:**
- Status: Backlog, Accepted, In Progress, Review, Done
- Priority: Critical, High, Medium, Low
- Milestone: v1.0, v1.1, v2.0
- Good First Issue: Yes/No

**Automations:**
- New issue → Status: Backlog
- Label "accepted" added → Status: Accepted
- PR merged → Status: Done

### Example 2: Product Team Sprint Board

**Project:** Sprint Q1-2026

**Views:**
- Sprint Board: Current sprint items
- Backlog: Prioritized backlog
- My Work: Assigned to me
- Bugs: Bug issues only

**Fields:**
- Status: Ready, In Progress, Review, QA, Done
- Sprint: Sprint 1, Sprint 2, Sprint 3
- Size: XS (1), S (2), M (3), L (5), XL (8)
- Team: Frontend, Backend, Mobile

**Iteration settings:**
- Duration: 2 weeks
- Start: Monday
- Capacity tracked per team

---

## Common Mistakes

| Mistake | Impact | Solution |
|---------|--------|----------|
| Too many views | Confusion | Start with 3-4 views |
| No automations | Manual overhead | Set up basic auto-status |
| Missing issue templates | Inconsistent issues | Create templates |
| No field standards | Poor filtering | Document field usage |
| Ignoring draft issues | Ideas lost | Use drafts for quick capture |

---

## Next Steps

1. Create organization-level project
2. Configure Status, Priority, and Size fields
3. Create Board, Table, and Roadmap views
4. Set up issue templates with auto-add
5. Configure basic automations
6. Add GitHub Actions for PR workflow

---

## Related Methodologies

- M-PMT-003: Linear Issue Tracking
- M-PMT-005: GitLab Boards
- M-PMT-009: Cross-Tool Migration
- M-PMT-011: Agile Ceremonies Setup
