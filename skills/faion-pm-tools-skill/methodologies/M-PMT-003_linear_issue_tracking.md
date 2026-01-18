# M-PMT-003: Linear Issue Tracking

## Metadata

| Field | Value |
|-------|-------|
| **ID** | M-PMT-003 |
| **Category** | PM Tools |
| **Difficulty** | Beginner |
| **Agent** | faion-pm-agent |
| **Skill** | faion-pm-tools-skill |

---

## Problem

Product teams need a fast, keyboard-driven issue tracker that:
- Minimizes friction in daily workflow
- Provides clear visibility into roadmaps
- Integrates seamlessly with development tools
- Scales without becoming cluttered

## Framework

### 1. Workspace Organization

**Linear hierarchy:**

```
Workspace (company)
├── Team (department)
│   └── Project (initiative)
│       └── Issue (work item)
│           └── Sub-issue (subtask)
└── Cycle (time-boxed sprint)
```

**Team structure recommendations:**

| Company Size | Teams | Projects per Team |
|--------------|-------|-------------------|
| Startup (1-10) | 1-2 | 2-4 |
| Small (10-50) | 3-5 | 3-6 |
| Medium (50-200) | 5-15 | 5-10 |
| Enterprise (200+) | Team-based | Initiative-based |

**Example setup:**

```
Workspace: Acme
├── Team: Product
│   ├── Project: Mobile App v2
│   ├── Project: Web Dashboard
│   └── Project: API v3
├── Team: Engineering
│   ├── Project: Infrastructure
│   ├── Project: Security
│   └── Project: Performance
└── Team: Design
    ├── Project: Design System
    └── Project: User Research
```

### 2. Issue Workflow

**Default workflow states:**

```
Backlog → Todo → In Progress → In Review → Done → Canceled
```

**State definitions:**

| State | Description | Actions |
|-------|-------------|---------|
| **Backlog** | Idea, not prioritized | Triage, estimate |
| **Todo** | Ready for work | Assign, schedule |
| **In Progress** | Actively being worked on | Code, design |
| **In Review** | PR submitted, awaiting review | Review, test |
| **Done** | Shipped to production | Close, archive |
| **Canceled** | Will not be done | Document reason |

**Custom workflows by team:**

```
Engineering: Backlog → Todo → In Progress → Code Review → QA → Done
Design: Backlog → Research → Designing → Review → Done
Marketing: Ideas → Planning → In Progress → Published
```

### 3. Cycles and Roadmaps

**Cycle planning:**

| Duration | Best For | Ceremony |
|----------|----------|----------|
| 1 week | Bug fixes, support | Weekly standup |
| 2 weeks | Feature sprints | Sprint planning, retro |
| 4 weeks | Large initiatives | Monthly planning |

**Cycle setup:**

```
Cycle: Sprint 14 (Jan 15-28)
├── Goal: "Ship user authentication"
├── Issues: 15 total
│   ├── 8 In Progress
│   ├── 5 Todo
│   └── 2 Done
└── Progress: 42%
```

**Roadmap structure:**

```
Roadmap
├── Q1 2026
│   ├── Project: Auth System (Jan-Feb)
│   ├── Project: Dashboard v2 (Feb-Mar)
│   └── Project: Mobile App (Mar)
└── Q2 2026
    ├── Project: API v3 (Apr-May)
    └── Project: Integrations (May-Jun)
```

### 4. Issue Management

**Issue fields:**

| Field | Purpose | Required |
|-------|---------|----------|
| Title | Brief description | Yes |
| Description | Details, context | No |
| Assignee | Owner | No |
| Priority | Urgency (P0-P4) | Yes |
| Estimate | Story points (0-8) | No |
| Project | Initiative grouping | No |
| Cycle | Sprint assignment | No |
| Labels | Categorization | No |
| Due date | Deadline | No |

**Priority levels:**

| Priority | Label | SLA | Example |
|----------|-------|-----|---------|
| **P0** | Urgent | < 24h | Production down |
| **P1** | High | < 3 days | Major bug, blocking |
| **P2** | Medium | Current cycle | Normal features |
| **P3** | Low | Next cycle | Nice to have |
| **P4** | Backlog | Later | Ideas, research |

**Estimate scale (Fibonacci):**

| Points | Effort | Example |
|--------|--------|---------|
| 0 | Trivial | Typo fix |
| 1 | Small | Config change |
| 2 | Medium | Simple feature |
| 3 | Large | Complex feature |
| 5 | XL | Multi-day task |
| 8 | Epic | Break it down |

### 5. GraphQL API

**Authentication:**

```bash
# API Key header
curl -X POST \
  -H "Authorization: Bearer lin_api_XXXXX" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ viewer { id name } }"}' \
  https://api.linear.app/graphql
```

**Common queries:**

```graphql
# Get current user's issues
query MyIssues {
  viewer {
    assignedIssues(first: 50, filter: {
      state: { type: { nin: ["completed", "canceled"] } }
    }) {
      nodes {
        id
        identifier
        title
        state { name }
        priority
        estimate
        project { name }
        cycle { name number }
      }
    }
  }
}

# Get team issues
query TeamIssues($teamId: String!) {
  team(id: $teamId) {
    issues(first: 100) {
      nodes {
        id
        identifier
        title
        state { name }
        assignee { name }
        priority
      }
    }
  }
}

# Get cycle progress
query CycleProgress($cycleId: String!) {
  cycle(id: $cycleId) {
    name
    number
    startsAt
    endsAt
    progress
    issues {
      nodes {
        id
        title
        state { name }
      }
    }
  }
}
```

**Mutations:**

```graphql
# Create issue
mutation CreateIssue($input: IssueCreateInput!) {
  issueCreate(input: $input) {
    success
    issue {
      id
      identifier
      title
    }
  }
}

# Variables
{
  "input": {
    "teamId": "team_id",
    "title": "Implement user authentication",
    "description": "Add OAuth2 login flow",
    "priority": 2,
    "estimate": 3,
    "projectId": "project_id",
    "cycleId": "cycle_id"
  }
}

# Update issue
mutation UpdateIssue($id: String!, $input: IssueUpdateInput!) {
  issueUpdate(id: $id, input: $input) {
    success
    issue {
      id
      state { name }
    }
  }
}

# Assign issue
{
  "id": "issue_id",
  "input": {
    "assigneeId": "user_id",
    "stateId": "state_id_in_progress"
  }
}
```

**Python client:**

```python
import requests

class LinearClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.url = "https://api.linear.app/graphql"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def query(self, query: str, variables: dict = None):
        payload = {"query": query}
        if variables:
            payload["variables"] = variables
        response = requests.post(
            self.url,
            headers=self.headers,
            json=payload
        )
        return response.json()

    def get_my_issues(self):
        query = """
        query {
          viewer {
            assignedIssues(first: 50) {
              nodes {
                id
                identifier
                title
                state { name }
                priority
              }
            }
          }
        }
        """
        return self.query(query)["data"]["viewer"]["assignedIssues"]["nodes"]

    def create_issue(self, team_id: str, title: str, **kwargs):
        mutation = """
        mutation CreateIssue($input: IssueCreateInput!) {
          issueCreate(input: $input) {
            success
            issue { id identifier title }
          }
        }
        """
        variables = {
            "input": {
                "teamId": team_id,
                "title": title,
                **kwargs
            }
        }
        result = self.query(mutation, variables)
        return result["data"]["issueCreate"]["issue"]

    def update_issue(self, issue_id: str, **updates):
        mutation = """
        mutation UpdateIssue($id: String!, $input: IssueUpdateInput!) {
          issueUpdate(id: $id, input: $input) {
            success
            issue { id state { name } }
          }
        }
        """
        variables = {"id": issue_id, "input": updates}
        return self.query(mutation, variables)

# Usage
client = LinearClient("lin_api_XXXXX")
issues = client.get_my_issues()
new_issue = client.create_issue(
    team_id="team_123",
    title="Add dark mode",
    description="User requested feature",
    priority=3,
    estimate=2
)
```

### 6. Integrations

**GitHub integration:**

```
When PR opened → Link to Linear issue (via branch name)
When PR merged → Move issue to "Done"
When commit pushed → Add comment to issue
```

**Branch naming convention:**

```
{username}/{issue-id}-{short-description}
john/PROJ-123-add-dark-mode
```

**Slack integration:**

```
Notifications:
├── New high-priority issues → #engineering
├── Issues assigned to me → DM
├── Cycle completed → #team-updates
└── Comments mentioning me → DM
```

**Webhook events:**

```json
{
  "action": "update",
  "type": "Issue",
  "data": {
    "id": "issue_id",
    "identifier": "PROJ-123",
    "title": "Add dark mode",
    "state": { "name": "In Progress" },
    "assignee": { "name": "John" }
  }
}
```

---

## Templates

### Issue Templates

**Bug report:**

```markdown
## Bug Report

**Environment:** [Production/Staging/Development]
**Browser/Device:** [Chrome 120, macOS 14]

### Description
[Brief description of the bug]

### Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. Scroll to '...'
4. See error

### Expected Behavior
[What should happen]

### Actual Behavior
[What actually happens]

### Screenshots
[If applicable]
```

**Feature request:**

```markdown
## Feature Request

### Problem
[What problem does this solve?]

### Proposed Solution
[How should it work?]

### User Stories
- As a [user], I want [feature] so that [benefit]

### Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

### Out of Scope
[What this does NOT include]
```

### Cycle Planning Template

```markdown
## Cycle [N] Planning

**Duration:** [Start] - [End]
**Goal:** [One sentence describing the main objective]

### Priorities
1. [P0/P1 items - must complete]
2. [P2 items - should complete]
3. [P3 items - nice to have]

### Capacity
| Team Member | Available | Focus |
|-------------|-----------|-------|
| Alice | 100% | Auth feature |
| Bob | 80% | Bug fixes |
| Carol | 50% | Support + design |

### Risks
- [Potential blockers]
- [Dependencies]

### Success Metrics
- [ ] Ship [feature] to production
- [ ] Close [N] bugs
- [ ] [Specific measurable outcome]
```

---

## Examples

### Example 1: Startup Product Team

**Setup:**

```
Workspace: StartupCo
├── Team: Product (6 people)
│   ├── Project: Core Platform
│   ├── Project: Mobile App
│   └── Project: Integrations
└── Cycles: 2-week sprints
```

**Labels:**
- `frontend`, `backend`, `mobile`
- `bug`, `feature`, `tech-debt`
- `customer-request`, `internal`

**Workflow:**
```
Backlog → Prioritized → In Progress → Review → Done
```

### Example 2: Enterprise Engineering

**Setup:**

```
Workspace: Enterprise Corp
├── Team: Platform
├── Team: Mobile
├── Team: Infrastructure
├── Team: Security
└── Team: Data
```

**Cross-team projects:**
- Project: "Q1 Performance Initiative" (Platform + Infra)
- Project: "SOC2 Compliance" (Security + all teams)

**Reporting:**
- Weekly: Cycle burndown per team
- Monthly: Roadmap progress
- Quarterly: OKR alignment

---

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Create issue | `C` |
| Search | `Cmd/Ctrl + K` |
| My issues | `G` then `M` |
| Active cycle | `G` then `A` |
| Board view | `G` then `B` |
| Assign to me | `I` |
| Set priority | `1-4` |
| Set estimate | `E` |
| Add label | `L` |
| Archive | `A` |

---

## Common Mistakes

| Mistake | Impact | Solution |
|---------|--------|----------|
| No cycle goals | Scattered work | Define clear sprint goal |
| Skipping estimates | Poor planning | Use simple 0-5 scale |
| Too many labels | Confusion | Keep to 10-15 labels |
| Ignoring backlog | Issue pile-up | Weekly triage session |
| No project grouping | Lost context | Group by initiative |

---

## Next Steps

1. Create workspace and first team
2. Set up cycle duration (start with 2 weeks)
3. Import or create initial backlog
4. Connect GitHub integration
5. Run first cycle planning session

---

## Related Methodologies

- M-PMT-001: Jira Workflow Management
- M-PMT-004: GitHub Projects
- M-PMT-009: Cross-Tool Migration
- M-PMT-011: Agile Ceremonies Setup
