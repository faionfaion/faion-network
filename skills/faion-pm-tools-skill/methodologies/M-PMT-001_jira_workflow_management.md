# M-PMT-001: Jira Workflow Management

## Metadata

| Field | Value |
|-------|-------|
| **ID** | M-PMT-001 |
| **Category** | PM Tools |
| **Difficulty** | Intermediate |
| **Agent** | faion-pm-agent |
| **Skill** | faion-pm-tools-skill |

---

## Problem

Teams struggle to configure Jira effectively, leading to:
- Inconsistent issue tracking across projects
- Complex workflows that slow down work
- JQL queries that are hard to write and maintain
- Poor integration between boards and backlogs

## Framework

### 1. Project Structure Design

**Choose the right project type:**

| Type | Best For | Key Features |
|------|----------|--------------|
| **Scrum** | Sprint-based teams | Sprints, velocity, burndown |
| **Kanban** | Continuous flow | WIP limits, cumulative flow |
| **Team-managed** | Small teams | Simplified setup, quick start |
| **Company-managed** | Enterprise | Custom workflows, schemes |

**Recommended hierarchy:**

```
Organization
└── Project (one per product)
    ├── Epic (feature group)
    │   ├── Story (user value)
    │   │   └── Subtask (work item)
    │   └── Bug (defect)
    └── Task (non-story work)
```

### 2. Workflow Configuration

**Standard workflow states:**

```
To Do → In Progress → In Review → Done
```

**Advanced workflow with validation:**

```
Backlog
  ↓ (ready for sprint)
To Do
  ↓ (start work)
In Progress
  ↓ (submit for review)
In Review
  ↓ (approved) / ↙ (rejected → In Progress)
Done
```

**Workflow rules:**
- Only assignee can transition from In Progress
- Code Review required before Done
- All subtasks must be Done before parent closes

### 3. Board Configuration

**Kanban board columns:**

| Column | WIP Limit | Description |
|--------|-----------|-------------|
| Backlog | - | Prioritized work |
| To Do | 5 | Ready to start |
| In Progress | 3 | Active work |
| In Review | 2 | Pending review |
| Done | - | Completed |

**Swimlanes:**
- By Assignee (who is working on what)
- By Epic (feature grouping)
- By Priority (urgent vs normal)

### 4. JQL Essentials

**Basic queries:**

```jql
# My open issues
assignee = currentUser() AND status != Done

# Sprint backlog
sprint in openSprints() AND status = "To Do"

# Bugs created this week
type = Bug AND created >= startOfWeek()

# Overdue issues
duedate < now() AND status != Done

# High priority unassigned
priority in (High, Highest) AND assignee is EMPTY
```

**Advanced queries:**

```jql
# Issues blocked for > 3 days
status = "In Progress" AND updated < -3d

# Stories without estimates
type = Story AND "Story Points" is EMPTY

# Issues in current sprint not started
sprint in openSprints() AND status = "To Do"
    AND created < -2d

# Recently resolved by team
resolved >= -7d AND project = PROJ
    ORDER BY resolved DESC
```

### 5. REST API Patterns

**Authentication:**

```bash
# API Token (recommended)
curl -X GET \
  -H "Authorization: Basic $(echo -n 'email@example.com:API_TOKEN' | base64)" \
  "https://your-domain.atlassian.net/rest/api/3/issue/PROJ-123"
```

**Common operations:**

```python
import requests
from requests.auth import HTTPBasicAuth

# Configuration
JIRA_URL = "https://your-domain.atlassian.net"
AUTH = HTTPBasicAuth("email@example.com", "API_TOKEN")

# Get issue
def get_issue(issue_key: str):
    response = requests.get(
        f"{JIRA_URL}/rest/api/3/issue/{issue_key}",
        auth=AUTH,
        headers={"Accept": "application/json"}
    )
    return response.json()

# Create issue
def create_issue(project_key: str, summary: str, issue_type: str = "Story"):
    payload = {
        "fields": {
            "project": {"key": project_key},
            "summary": summary,
            "issuetype": {"name": issue_type}
        }
    }
    response = requests.post(
        f"{JIRA_URL}/rest/api/3/issue",
        auth=AUTH,
        json=payload
    )
    return response.json()

# Transition issue
def transition_issue(issue_key: str, transition_id: str):
    payload = {"transition": {"id": transition_id}}
    response = requests.post(
        f"{JIRA_URL}/rest/api/3/issue/{issue_key}/transitions",
        auth=AUTH,
        json=payload
    )
    return response.status_code == 204

# Search with JQL
def search_issues(jql: str, max_results: int = 50):
    params = {
        "jql": jql,
        "maxResults": max_results,
        "fields": "summary,status,assignee,priority"
    }
    response = requests.get(
        f"{JIRA_URL}/rest/api/3/search",
        auth=AUTH,
        params=params
    )
    return response.json()["issues"]
```

**Webhook setup:**

```json
{
  "name": "Issue Created Webhook",
  "url": "https://your-app.com/jira/webhook",
  "events": [
    "jira:issue_created",
    "jira:issue_updated",
    "sprint_started",
    "sprint_closed"
  ],
  "filters": {
    "issue-related-events-section": "project = PROJ"
  }
}
```

### 6. Automation Rules

**Auto-assign on transition:**

```
WHEN: Issue transitions to "In Progress"
IF: Assignee is empty
THEN: Assign to current user
```

**Close subtasks with parent:**

```
WHEN: Issue transitions to "Done"
IF: Issue has subtasks
THEN: Transition subtasks to "Done"
```

**Sprint reminder:**

```
WHEN: Scheduled - Daily at 9 AM
IF: Issues in current sprint with status "To Do" for > 3 days
THEN: Comment "This issue has been in To Do for {{daysSinceStatusChange}} days"
AND: Notify assignee
```

---

## Templates

### Project Setup Checklist

```markdown
## Jira Project Setup

### Basic Configuration
- [ ] Project type selected (Scrum/Kanban/Team-managed)
- [ ] Project key defined (3-4 uppercase letters)
- [ ] Issue types configured (Epic, Story, Bug, Task, Subtask)
- [ ] Workflow states defined

### Board Setup
- [ ] Columns match workflow states
- [ ] WIP limits configured
- [ ] Swimlanes defined
- [ ] Quick filters created

### Fields & Screens
- [ ] Custom fields created
- [ ] Field screens configured
- [ ] Required fields set

### Automation
- [ ] Auto-assign rules
- [ ] Notification rules
- [ ] Status transition rules

### Integrations
- [ ] GitHub/GitLab connected
- [ ] Slack notifications
- [ ] CI/CD webhooks
```

### JQL Query Library

```markdown
## Common JQL Queries

### Sprint Queries
- Current sprint: `sprint in openSprints()`
- Sprint backlog: `sprint in openSprints() AND status = "To Do"`
- Spillover: `sprint in closedSprints() AND status != Done`

### Team Queries
- My work: `assignee = currentUser() AND status != Done`
- Team workload: `project = PROJ AND assignee is not EMPTY`
- Unassigned: `project = PROJ AND assignee is EMPTY`

### Progress Queries
- Blocked: `status = "In Progress" AND updated < -3d`
- Overdue: `duedate < now() AND status != Done`
- Recently done: `resolved >= -7d ORDER BY resolved DESC`

### Quality Queries
- Bugs by priority: `type = Bug ORDER BY priority DESC`
- Bug trend: `type = Bug AND created >= -30d`
- Escaped bugs: `type = Bug AND "Found In" = Production`
```

---

## Examples

### Example 1: SaaS Product Project

**Project:** SAAS (Scrum)

**Workflow:**
```
Backlog → Ready → In Progress → Code Review → QA → Done
```

**Board columns:**
| Column | WIP | Mapped Statuses |
|--------|-----|-----------------|
| Backlog | - | Backlog |
| Ready | 8 | Ready |
| Dev | 4 | In Progress |
| Review | 3 | Code Review |
| QA | 2 | QA |
| Done | - | Done |

**Sprint query:**
```jql
project = SAAS AND sprint in openSprints()
    AND type in (Story, Bug)
    ORDER BY priority DESC, rank ASC
```

### Example 2: Support Team Kanban

**Project:** SUPPORT (Kanban)

**Workflow:**
```
New → Triaged → In Progress → Waiting → Resolved
```

**SLA tracking:**
- P1 (Critical): 4 hours response
- P2 (High): 8 hours response
- P3 (Medium): 24 hours response
- P4 (Low): 72 hours response

**Dashboard JQL:**
```jql
# Breaching SLA
project = SUPPORT AND status != Resolved
    AND (
        (priority = P1 AND created < -4h) OR
        (priority = P2 AND created < -8h) OR
        (priority = P3 AND created < -24h)
    )
```

---

## Common Mistakes

| Mistake | Impact | Solution |
|---------|--------|----------|
| Too many workflow states | Confusion, bottlenecks | Keep to 4-6 states max |
| No WIP limits | Overcommitment | Set limits, enforce them |
| Generic issue types | Poor tracking | Create specific types |
| Complex JQL in filters | Slow performance | Simplify, use indexes |
| No automation | Manual overhead | Automate repetitive tasks |

---

## Next Steps

1. Set up a test project with basic workflow
2. Configure board with WIP limits
3. Create essential JQL filters
4. Add automation rules
5. Connect to development tools (GitHub/GitLab)

---

## Related Methodologies

- M-PMT-009: Cross-Tool Migration
- M-PMT-010: PM Tool Selection
- M-PMT-011: Agile Ceremonies Setup
- M-PMT-012: Reporting & Dashboards
