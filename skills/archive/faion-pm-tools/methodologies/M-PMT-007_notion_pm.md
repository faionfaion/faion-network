# M-PMT-007: Notion PM

## Metadata

| Field | Value |
|-------|-------|
| **ID** | M-PMT-007 |
| **Category** | PM Tools |
| **Difficulty** | Beginner |
| **Agent** | faion-pm-agent |
| **Skill** | faion-pm-tools-skill |

---

## Problem

Teams want flexible project management that:
- Combines documentation with task tracking
- Adapts to any workflow without rigid structure
- Provides multiple views of the same data
- Enables collaboration on docs and tasks together

## Framework

### 1. Workspace Architecture

**Notion hierarchy:**

```
Workspace (team)
├── Teamspace (department)
│   ├── Page (document/hub)
│   │   ├── Database (tasks/projects)
│   │   ├── Subpage (documentation)
│   │   └── Linked database (view)
```

**Recommended structure:**

```
Workspace: Acme Inc
├── Teamspace: Product
│   ├── Page: Product Hub
│   │   ├── Database: Roadmap
│   │   ├── Database: Tasks
│   │   └── Page: Documentation
│   ├── Page: Sprints
│   └── Page: Meetings
├── Teamspace: Engineering
│   ├── Page: Tech Specs
│   └── Page: Architecture
└── Teamspace: Operations
    ├── Page: Processes
    └── Page: Resources
```

### 2. Database Design

**Core databases:**

| Database | Purpose | Key Properties |
|----------|---------|----------------|
| Projects | Initiatives | Status, Owner, Timeline, Priority |
| Tasks | Work items | Status, Assignee, Sprint, Project |
| Sprints | Iterations | Dates, Goals, Capacity |
| Bugs | Defects | Severity, Reporter, Environment |

**Task database properties:**

```yaml
Properties:
  - name: Name
    type: title

  - name: Status
    type: select
    options:
      - name: Backlog
        color: gray
      - name: To Do
        color: blue
      - name: In Progress
        color: yellow
      - name: In Review
        color: purple
      - name: Done
        color: green

  - name: Assignee
    type: person

  - name: Priority
    type: select
    options:
      - name: P0 - Critical
        color: red
      - name: P1 - High
        color: orange
      - name: P2 - Medium
        color: yellow
      - name: P3 - Low
        color: gray

  - name: Sprint
    type: relation
    database: Sprints

  - name: Project
    type: relation
    database: Projects

  - name: Estimate
    type: number
    format: number

  - name: Due Date
    type: date

  - name: Tags
    type: multi_select
    options:
      - frontend
      - backend
      - design
      - bug
      - feature

  - name: Created
    type: created_time

  - name: Completed
    type: date
```

**Relations and rollups:**

```yaml
# In Projects database
Properties:
  - name: Tasks
    type: relation
    database: Tasks
    bidirectional: true

  - name: Total Tasks
    type: rollup
    relation: Tasks
    property: Name
    calculation: count

  - name: Completed Tasks
    type: rollup
    relation: Tasks
    property: Status
    calculation: count
    filter: "Status = Done"

  - name: Progress
    type: formula
    formula: "round(prop(\"Completed Tasks\") / prop(\"Total Tasks\") * 100)"
```

### 3. Views

**Essential views per database:**

| View | Type | Purpose | Filter/Sort |
|------|------|---------|-------------|
| Board | Kanban | Daily work | Group by Status |
| Table | List | Planning | Sort by Priority |
| Calendar | Timeline | Deadlines | By Due Date |
| Timeline | Gantt | Roadmap | By Date range |
| Gallery | Cards | Visual overview | None |

**Board view configuration:**

```yaml
View: Sprint Board
Type: Board
Group by: Status
Sub-group: None
Filter:
  - Sprint = Current Sprint
Sort:
  - Priority: Ascending
Properties shown:
  - Assignee
  - Priority
  - Estimate
  - Due Date
```

**Table view for planning:**

```yaml
View: Backlog Planning
Type: Table
Filter:
  - Status != Done
Sort:
  - Priority: Ascending
  - Created: Descending
Columns:
  - Name
  - Status
  - Priority
  - Assignee
  - Estimate
  - Sprint
  - Project
```

**Timeline view for roadmap:**

```yaml
View: Roadmap
Type: Timeline
Show by: Date range (Start Date → Due Date)
Table properties:
  - Name
  - Status
  - Owner
Filter:
  - Type = Project OR Type = Epic
Group by: Quarter
```

### 4. Templates

**Task template:**

```markdown
## Description
<!-- What needs to be done -->

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Technical Notes
<!-- Implementation details -->

## Resources
- Link 1
- Link 2

---
**Updates**
<!-- Add progress updates here -->
```

**Sprint template:**

```markdown
## Sprint [Number]

**Duration:** [Start] - [End]
**Goal:** [One sentence]

### Priorities
1. [ ] Priority 1
2. [ ] Priority 2
3. [ ] Priority 3

### Capacity
| Team Member | Available | Focus |
|-------------|-----------|-------|
| @Alice | 100% | Feature A |
| @Bob | 80% | Bug fixes |

### Metrics
- Planned: [X] points
- Completed: [Y] points
- Velocity: [Z] points/sprint

### Retro Notes
**What went well:**
-

**What to improve:**
-

**Action items:**
- [ ] Action 1
```

**Meeting notes template:**

```markdown
## [Meeting Type] - [Date]

**Attendees:** @person1, @person2
**Duration:** X minutes

### Agenda
1. Topic 1
2. Topic 2

### Discussion Notes
#### Topic 1
- Point 1
- Point 2

### Decisions
- Decision 1: [description]

### Action Items
- [ ] @person - Task 1 (due: date)
- [ ] @person - Task 2 (due: date)

### Next Meeting
[Date/Time]
```

### 5. Automations

**Button automations:**

```yaml
# Create task from template
Button: "New Task"
Actions:
  - Add page to: Tasks database
  - Set property: Status = "To Do"
  - Set property: Created = now()
  - Open page

# Complete task
Button: "Mark Done"
Actions:
  - Set property: Status = "Done"
  - Set property: Completed = now()
```

**Database automations (Notion AI):**

```yaml
# Auto-assign on status change
Trigger: Property changed (Status = "In Progress")
Condition: Assignee is empty
Action: Assign to last editor

# Due date reminder
Trigger: Due date is today
Action: Send notification to Assignee

# Move to done sprint
Trigger: Status changed to "Done"
Action: Set Completed Sprint = Current Sprint
```

### 6. Notion API

**Authentication:**

```bash
# Internal integration token
curl -X POST 'https://api.notion.com/v1/databases/DATABASE_ID/query' \
  -H 'Authorization: Bearer secret_xxx' \
  -H 'Notion-Version: 2022-06-28' \
  -H 'Content-Type: application/json'
```

**Python client:**

```python
from notion_client import Client

class NotionPM:
    def __init__(self, token: str):
        self.client = Client(auth=token)

    def get_database(self, database_id: str):
        """Get database schema"""
        return self.client.databases.retrieve(database_id)

    def query_database(self, database_id: str, filter: dict = None,
                       sorts: list = None):
        """Query database with optional filter and sort"""
        params = {"database_id": database_id}
        if filter:
            params["filter"] = filter
        if sorts:
            params["sorts"] = sorts
        return self.client.databases.query(**params)

    def create_page(self, database_id: str, properties: dict,
                    content: list = None):
        """Create page in database"""
        params = {
            "parent": {"database_id": database_id},
            "properties": properties
        }
        if content:
            params["children"] = content
        return self.client.pages.create(**params)

    def update_page(self, page_id: str, properties: dict):
        """Update page properties"""
        return self.client.pages.update(
            page_id=page_id,
            properties=properties
        )

    # PM-specific methods
    def get_sprint_tasks(self, tasks_db: str, sprint_id: str):
        """Get all tasks in a sprint"""
        return self.query_database(
            tasks_db,
            filter={
                "property": "Sprint",
                "relation": {"contains": sprint_id}
            },
            sorts=[{"property": "Priority", "direction": "ascending"}]
        )

    def get_my_tasks(self, tasks_db: str, user_id: str):
        """Get tasks assigned to user"""
        return self.query_database(
            tasks_db,
            filter={
                "and": [
                    {"property": "Assignee", "people": {"contains": user_id}},
                    {"property": "Status", "select": {"does_not_equal": "Done"}}
                ]
            }
        )

    def create_task(self, tasks_db: str, title: str, **kwargs):
        """Create new task"""
        properties = {
            "Name": {"title": [{"text": {"content": title}}]},
            "Status": {"select": {"name": kwargs.get("status", "To Do")}},
        }
        if kwargs.get("priority"):
            properties["Priority"] = {"select": {"name": kwargs["priority"]}}
        if kwargs.get("assignee"):
            properties["Assignee"] = {"people": [{"id": kwargs["assignee"]}]}
        if kwargs.get("due_date"):
            properties["Due Date"] = {"date": {"start": kwargs["due_date"]}}
        if kwargs.get("sprint_id"):
            properties["Sprint"] = {"relation": [{"id": kwargs["sprint_id"]}]}

        return self.create_page(tasks_db, properties)

    def complete_task(self, page_id: str):
        """Mark task as done"""
        return self.update_page(page_id, {
            "Status": {"select": {"name": "Done"}},
            "Completed": {"date": {"start": datetime.now().isoformat()}}
        })


# Usage
from datetime import datetime

notion = NotionPM("secret_xxx")

# Query tasks
tasks = notion.get_sprint_tasks(
    tasks_db="database_id",
    sprint_id="sprint_page_id"
)

# Create task
new_task = notion.create_task(
    tasks_db="database_id",
    title="Implement OAuth login",
    priority="P1 - High",
    assignee="user_id",
    due_date="2026-01-28",
    sprint_id="sprint_page_id"
)

# Complete task
notion.complete_task("task_page_id")
```

**Filter examples:**

```python
# Tasks due this week
filter = {
    "and": [
        {"property": "Due Date", "date": {"on_or_after": "2026-01-20"}},
        {"property": "Due Date", "date": {"on_or_before": "2026-01-26"}},
        {"property": "Status", "select": {"does_not_equal": "Done"}}
    ]
}

# High priority bugs
filter = {
    "and": [
        {"property": "Tags", "multi_select": {"contains": "bug"}},
        {"property": "Priority", "select": {"equals": "P0 - Critical"}}
    ]
}

# Overdue tasks
filter = {
    "and": [
        {"property": "Due Date", "date": {"before": datetime.now().isoformat()}},
        {"property": "Status", "select": {"does_not_equal": "Done"}}
    ]
}
```

### 7. Integrations

**Slack integration:**

```
/notion [command]
├── /notion create task [title]
├── /notion show sprint
└── /notion my tasks
```

**GitHub integration:**

```
Notion → GitHub:
├── Create issue from Notion task
├── Sync status bidirectionally
└── Link PRs to Notion pages

GitHub → Notion:
├── Auto-create Notion task on issue
├── Update Notion on PR merge
└── Add commit links to Notion
```

**Zapier/Make automations:**

```yaml
# GitHub Issue → Notion Task
Trigger: New GitHub Issue
Action: Create Notion page
Mapping:
  - Title → Name
  - Body → Description
  - Labels → Tags
  - Assignee → Assignee
```

---

## Templates

### Workspace Setup Checklist

```markdown
## Notion PM Setup

### Structure
- [ ] Teamspaces created
- [ ] Main hub pages created
- [ ] Navigation sidebar organized

### Databases
- [ ] Tasks database with all properties
- [ ] Projects database
- [ ] Sprints database
- [ ] Relations configured between databases

### Views
- [ ] Board view (daily work)
- [ ] Table view (planning)
- [ ] Calendar view (deadlines)
- [ ] Timeline view (roadmap)
- [ ] Filtered views (My Tasks, By Project)

### Templates
- [ ] Task template
- [ ] Sprint template
- [ ] Meeting notes template
- [ ] Project brief template

### Automations
- [ ] Button automations
- [ ] Database automations
- [ ] External integrations (Slack, GitHub)

### Team
- [ ] Team members invited
- [ ] Permissions configured
- [ ] Onboarding documentation
```

---

## Examples

### Example 1: Startup Product Team

**Structure:**

```
Workspace: StartupCo
├── Teamspace: Product
│   ├── Roadmap (Timeline view)
│   ├── Sprint Board (Kanban)
│   ├── Backlog (Table)
│   └── Documentation
│       ├── PRDs
│       └── Specs
```

**Databases:**
- Tasks (linked to Sprints, Projects)
- Sprints (2-week iterations)
- Projects (quarterly initiatives)

**Views:**
- Sprint Board: Current sprint tasks
- My Tasks: Assigned to me, not done
- Roadmap: Projects on timeline

### Example 2: Freelancer/Solopreneur

**Structure:**

```
Workspace: Personal
├── Page: Project Hub
│   ├── Database: Clients
│   ├── Database: Projects
│   └── Database: Tasks
├── Page: Weekly Planning
└── Page: Resources
```

**Simple task statuses:**
- Inbox, Next, Doing, Done

**Weekly review template:**
- Review completed tasks
- Plan next week
- Update project status

---

## Common Mistakes

| Mistake | Impact | Solution |
|---------|--------|----------|
| Too many databases | Confusion | Start with 2-3 core databases |
| Complex relations | Slow performance | Keep relations simple |
| No templates | Inconsistent data | Create templates early |
| Too many views | Hard to navigate | 3-5 views per database |
| Ignoring rollups | Manual counting | Use rollups for metrics |

---

## Next Steps

1. Create Tasks and Projects databases
2. Set up essential properties and relations
3. Create Board, Table, and Timeline views
4. Build task and sprint templates
5. Configure basic automations
6. Connect to Slack or other tools

---

## Related Methodologies

- M-PMT-002: ClickUp Setup
- M-PMT-008: Trello Kanban
- M-PMT-010: PM Tool Selection
- M-PMT-012: Reporting & Dashboards
