# M-PMT-002: ClickUp Setup

## Metadata

| Field | Value |
|-------|-------|
| **ID** | M-PMT-002 |
| **Category** | PM Tools |
| **Difficulty** | Beginner |
| **Agent** | faion-pm-agent |
| **Skill** | faion-pm-tools-skill |

---

## Problem

Teams adopting ClickUp face challenges:
- Overwhelming number of features without clear guidance
- Inefficient workspace structure that does not scale
- Underutilization of automations and integrations
- Inconsistent task management across teams

## Framework

### 1. Workspace Hierarchy Design

**ClickUp hierarchy:**

```
Workspace (company)
└── Space (department/team)
    └── Folder (project group)
        └── List (project/sprint)
            └── Task (work item)
                └── Subtask (sub-item)
```

**Recommended structure by company size:**

| Size | Spaces | Folders per Space | Lists per Folder |
|------|--------|-------------------|------------------|
| Solo (1) | 1-2 | 2-3 | 3-5 |
| Small (2-10) | 2-4 | 3-5 | 5-10 |
| Medium (11-50) | 4-8 | 5-10 | 10-20 |
| Large (50+) | 8+ | Team-based | Project-based |

**Example: SaaS Startup**

```
Workspace: Acme Inc
├── Space: Product
│   ├── Folder: Q1 2026 Roadmap
│   │   ├── List: Sprint 1
│   │   ├── List: Sprint 2
│   │   └── List: Backlog
│   └── Folder: Bugs
│       ├── List: Critical
│       └── List: Normal
├── Space: Marketing
│   ├── Folder: Campaigns
│   └── Folder: Content
└── Space: Operations
    ├── Folder: HR
    └── Folder: Finance
```

### 2. Custom Statuses

**Basic workflow:**

```
To Do → In Progress → Review → Done
```

**Development workflow:**

```
Backlog
  ↓
Ready for Dev
  ↓
In Progress
  ↓
Code Review
  ↓
QA Testing
  ↓
Deployed
  ↓
Done
```

**Status groups:**
- **Active statuses** (colored): To Do, In Progress, Review
- **Done statuses** (gray): Complete, Deployed
- **Closed statuses** (hidden): Archived, Cancelled

### 3. Custom Fields

**Essential fields:**

| Field | Type | Purpose |
|-------|------|---------|
| Priority | Dropdown | Urgency level |
| Story Points | Number | Effort estimate |
| Sprint | Dropdown | Sprint assignment |
| Due Date | Date | Deadline |
| Assignee | People | Owner |
| Department | Dropdown | Team filter |

**Advanced fields:**

| Field | Type | Use Case |
|-------|------|----------|
| Progress | Progress | Manual % completion |
| Dependencies | Relationship | Task blocking |
| Customer | Relationship | Client tracking |
| Revenue Impact | Currency | Business value |
| Risk Level | Dropdown | Risk assessment |

### 4. Views Configuration

**Essential views per list:**

| View | Type | Purpose |
|------|------|---------|
| Board | Kanban | Sprint work |
| List | Table | Detailed planning |
| Calendar | Timeline | Deadlines |
| Gantt | Timeline | Dependencies |
| Workload | Resource | Team capacity |

**View settings:**

```
Board View Settings:
├── Group by: Status
├── Sort: Priority (High to Low)
├── Subtasks: Show as separate cards
├── Columns: Show WIP limits
└── Card layout: Compact with assignee
```

### 5. Automations

**Built-in automation templates:**

**Auto-assign on status change:**
```
WHEN: Status changes to "In Progress"
THEN: Set assignee to triggered by
```

**Move completed tasks:**
```
WHEN: Status changes to "Done"
THEN: Move to "Archive" list
THEN: Add comment "Completed on {{date}}"
```

**Due date reminders:**
```
WHEN: Due date arrives
IF: Status is not "Done"
THEN: Send notification to assignee
THEN: Add comment "Due today!"
```

**Sprint automation:**
```
WHEN: Custom date arrives (Sprint end)
IF: Status is not "Done"
THEN: Change status to "Backlog"
THEN: Clear Sprint field
```

**Create from template:**
```
WHEN: Task is created
IF: Task name contains "[RELEASE]"
THEN: Apply template "Release Checklist"
```

### 6. API Integration

**Authentication:**

```bash
# Personal API Token
curl -X GET \
  -H "Authorization: pk_123456_ABCDEF" \
  "https://api.clickup.com/api/v2/team"
```

**Common operations:**

```python
import requests

API_TOKEN = "pk_123456_ABCDEF"
HEADERS = {"Authorization": API_TOKEN}
BASE_URL = "https://api.clickup.com/api/v2"

# Get workspaces
def get_workspaces():
    response = requests.get(f"{BASE_URL}/team", headers=HEADERS)
    return response.json()["teams"]

# Get lists in folder
def get_lists(folder_id: str):
    response = requests.get(
        f"{BASE_URL}/folder/{folder_id}/list",
        headers=HEADERS
    )
    return response.json()["lists"]

# Create task
def create_task(list_id: str, name: str, description: str = "",
                priority: int = 3, assignees: list = None):
    payload = {
        "name": name,
        "description": description,
        "priority": priority,  # 1=Urgent, 2=High, 3=Normal, 4=Low
        "assignees": assignees or [],
        "notify_all": True
    }
    response = requests.post(
        f"{BASE_URL}/list/{list_id}/task",
        headers=HEADERS,
        json=payload
    )
    return response.json()

# Update task
def update_task(task_id: str, updates: dict):
    response = requests.put(
        f"{BASE_URL}/task/{task_id}",
        headers=HEADERS,
        json=updates
    )
    return response.json()

# Get tasks with filters
def get_tasks(list_id: str, statuses: list = None,
              assignees: list = None, include_closed: bool = False):
    params = {
        "include_closed": str(include_closed).lower(),
        "subtasks": "true"
    }
    if statuses:
        params["statuses[]"] = statuses
    if assignees:
        params["assignees[]"] = assignees

    response = requests.get(
        f"{BASE_URL}/list/{list_id}/task",
        headers=HEADERS,
        params=params
    )
    return response.json()["tasks"]

# Add comment
def add_comment(task_id: str, comment_text: str):
    payload = {"comment_text": comment_text}
    response = requests.post(
        f"{BASE_URL}/task/{task_id}/comment",
        headers=HEADERS,
        json=payload
    )
    return response.json()
```

**Webhook setup:**

```python
def create_webhook(team_id: str, endpoint: str, events: list):
    payload = {
        "endpoint": endpoint,
        "events": events  # ["taskCreated", "taskUpdated", "taskDeleted"]
    }
    response = requests.post(
        f"{BASE_URL}/team/{team_id}/webhook",
        headers=HEADERS,
        json=payload
    )
    return response.json()
```

### 7. Templates

**Task templates:**

```
Template: Bug Report
├── Priority: High
├── Status: To Do
├── Custom Fields:
│   ├── Bug Type: [dropdown]
│   ├── Environment: [dropdown]
│   ├── Steps to Reproduce: [text]
│   └── Expected vs Actual: [text]
└── Checklist:
    ├── [ ] Reproduce issue
    ├── [ ] Identify root cause
    ├── [ ] Implement fix
    ├── [ ] Write tests
    └── [ ] Deploy to staging
```

**List templates:**

```
Template: Sprint
├── Statuses: Backlog → To Do → In Progress → Review → Done
├── Views: Board, List, Gantt
├── Custom Fields: Story Points, Sprint Goal
├── Automations:
│   ├── Auto-assign on progress
│   └── Notify on completion
└── Default tasks:
    ├── Sprint Planning
    ├── Daily Standup (recurring)
    └── Sprint Review
```

---

## Templates

### Workspace Setup Checklist

```markdown
## ClickUp Workspace Setup

### Structure
- [ ] Spaces created for each team/department
- [ ] Folders organized by project or category
- [ ] Lists created for active work
- [ ] Archive space/folder for completed work

### Configuration
- [ ] Custom statuses defined per space
- [ ] Custom fields created and applied
- [ ] Task templates created
- [ ] List templates created

### Views
- [ ] Board view for daily work
- [ ] List view for planning
- [ ] Calendar view for deadlines
- [ ] Workload view for capacity

### Automations
- [ ] Status change automations
- [ ] Due date reminders
- [ ] Assignment automations
- [ ] Integration webhooks

### Integrations
- [ ] GitHub/GitLab connected
- [ ] Slack notifications
- [ ] Calendar sync (Google/Outlook)
- [ ] Time tracking enabled
```

### Permission Structure Template

```markdown
## ClickUp Permissions

### Roles
| Role | Access Level | Use Case |
|------|--------------|----------|
| Owner | Full | Workspace admins |
| Admin | Full (space) | Team leads |
| Member | Edit | Team members |
| Guest | View/Comment | Clients, contractors |

### Space Permissions
| Space | Owner | Admin | Member | Guest |
|-------|-------|-------|--------|-------|
| Product | Full | Full | Edit | - |
| Marketing | Full | Full | Edit | View |
| Finance | Full | Full | - | - |
| Client Portal | Full | Full | View | Comment |
```

---

## Examples

### Example 1: Marketing Agency

**Structure:**

```
Workspace: Agency
├── Space: Client Projects
│   ├── Folder: Acme Corp
│   │   ├── List: Website Redesign
│   │   ├── List: SEO Campaign
│   │   └── List: Social Media
│   └── Folder: Beta Inc
│       └── List: Brand Identity
├── Space: Internal
│   ├── Folder: Operations
│   └── Folder: Team
└── Space: Templates
    ├── List: Project Templates
    └── List: Task Templates
```

**Custom fields:**
- Client (Relationship)
- Project Type (Dropdown)
- Budget (Currency)
- Deadline Type (Dropdown: Hard/Soft)

### Example 2: Software Development Team

**Structure:**

```
Workspace: TechCo
├── Space: Product - App
│   ├── Folder: Releases
│   │   ├── List: v2.0 (current)
│   │   └── List: v2.1 (planning)
│   ├── Folder: Sprints
│   │   ├── List: Sprint 14
│   │   └── List: Backlog
│   └── Folder: Bugs
├── Space: Infrastructure
│   └── Folder: DevOps
└── Space: Documentation
```

**Automations:**
1. When PR merged (webhook), move task to "QA Testing"
2. When all subtasks done, change status to "Review"
3. Every Friday, notify unfinished sprint tasks

---

## Common Mistakes

| Mistake | Impact | Solution |
|---------|--------|----------|
| Too many spaces | Navigation overhead | Consolidate related work |
| No templates | Inconsistent tasks | Create task/list templates |
| Ignoring automations | Manual overhead | Start with 3-5 automations |
| Complex hierarchies | Lost items | Keep hierarchy flat (3-4 levels) |
| No archive strategy | Cluttered lists | Weekly archive routine |

---

## Next Steps

1. Create workspace with 2-3 spaces
2. Set up custom statuses per space
3. Add essential custom fields
4. Create board and list views
5. Build 5 automation rules
6. Connect integrations (Slack, GitHub)

---

## Related Methodologies

- M-PMT-001: Jira Workflow Management
- M-PMT-009: Cross-Tool Migration
- M-PMT-010: PM Tool Selection
- M-PMT-012: Reporting & Dashboards
