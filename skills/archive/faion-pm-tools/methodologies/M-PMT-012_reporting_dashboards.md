# M-PMT-012: Reporting & Dashboards

## Metadata

| Field | Value |
|-------|-------|
| **ID** | M-PMT-012 |
| **Category** | PM Tools |
| **Difficulty** | Intermediate |
| **Agent** | faion-pm-agent |
| **Skill** | faion-pm-tools-skill |

---

## Problem

Teams lack visibility into project health because:
- Data scattered across multiple tools
- Manual reporting wastes time
- Stakeholders ask same questions repeatedly
- Metrics don't drive decisions
- Dashboards built but never used

---

## Framework

### 1. Essential Metrics

**Agile/Scrum metrics:**

| Metric | What It Measures | Formula | Good Signal |
|--------|------------------|---------|-------------|
| **Velocity** | Work completed per sprint | Sum of completed story points | Consistent (+/- 20%) |
| **Burndown** | Sprint progress | Remaining work over time | Linear descent |
| **Burnup** | Scope + completion | Work done vs total scope | Parallel lines |
| **Cycle Time** | Time to complete item | Done date - Start date | Decreasing |
| **Lead Time** | Idea to delivery | Done date - Created date | Predictable |
| **Throughput** | Items completed | Count of Done items | Stable/increasing |
| **WIP** | Work in progress | Count of In Progress items | Within limits |
| **Escape Rate** | Bugs in production | Bugs found post-release | Decreasing |

**Flow metrics (Kanban):**

| Metric | What It Measures | Why It Matters |
|--------|------------------|----------------|
| **Throughput** | Items completed/week | Delivery capacity |
| **Cycle Time** | Time in active work | Efficiency |
| **WIP** | Current active items | System load |
| **Flow Efficiency** | Active / Total time | Value-add ratio |
| **Aging WIP** | Items stuck too long | Identify blockers |
| **Blocked Time** | Time items blocked | Process problems |

**Health indicators:**

```yaml
Sprint Health:
  green:
    - Burndown on track
    - WIP within limits
    - No items blocked > 2 days
    - Sprint goal achievable

  yellow:
    - Burndown slightly behind
    - WIP at limit
    - 1-2 items blocked
    - Sprint goal at risk

  red:
    - Burndown significantly behind
    - WIP over limit
    - Multiple blocked items
    - Sprint goal not achievable
```

### 2. Dashboard Design Principles

**SMART dashboard criteria:**

```markdown
## Dashboard Checklist

- [ ] **Specific:** Shows exactly what user needs
- [ ] **Measurable:** Quantified, not qualitative
- [ ] **Actionable:** Insights lead to action
- [ ] **Relevant:** Answers user's actual questions
- [ ] **Timely:** Data is current, updates automated

## Design Principles

1. **One screen:** Key info visible without scrolling
2. **Hierarchy:** Most important metrics prominent
3. **Context:** Show trend, not just current value
4. **Comparison:** Benchmark against target/past
5. **Color coding:** Green/yellow/red for quick scan
6. **Drill-down:** Click for details
```

**Dashboard types by audience:**

| Audience | Focus | Key Metrics | Update Frequency |
|----------|-------|-------------|------------------|
| **Developers** | Daily work | WIP, blockers, my tasks | Real-time |
| **Team Lead** | Sprint health | Burndown, velocity, blockers | Daily |
| **PM/PO** | Delivery | Roadmap progress, lead time | Weekly |
| **Stakeholders** | Business outcomes | Completion %, milestones | Bi-weekly |
| **Executives** | Portfolio | Budget, schedule, risks | Monthly |

### 3. Tool-Specific Dashboards

**Jira Dashboards:**

```yaml
# Team Dashboard
Name: "Sprint Dashboard"
Layout: 2 columns

Gadgets:
  Row 1:
    - Sprint Burndown Chart
      Description: Shows remaining work
      Size: Wide

  Row 2:
    - Sprint Health Gadget
      Description: Quick status
    - Filter Results: Blocked Issues
      JQL: "sprint in openSprints() AND labels = blocked"

  Row 3:
    - Two Dimensional Filter Statistics
      Filter: Sprint issues
      X-axis: Assignee
      Y-axis: Status

  Row 4:
    - Created vs Resolved Chart
      Filter: Last 30 days
    - Velocity Chart
      Board: Team board

# Setup Steps:
1. Dashboards → Create Dashboard
2. Add Gadgets → Select from list
3. Configure each gadget with JQL filters
4. Share with team
```

**Jira JQL queries for dashboards:**

```sql
-- Current sprint items
sprint in openSprints()

-- My blocked items
assignee = currentUser() AND labels = blocked

-- Overdue items
due < now() AND status != Done

-- Recently completed
status changed to Done after -7d

-- Items without estimates
"Story Points" is EMPTY AND issuetype = Story

-- High priority bugs
issuetype = Bug AND priority in (Highest, High) AND status != Done

-- Sprint scope change
sprint = "Sprint 14" AND createdDate > "2026-01-13"

-- Velocity calculation (custom)
project = PROJ AND status = Done AND sprint in closedSprints()
```

**Linear Insights:**

```yaml
# Team Dashboard (built-in)
Insights Tab:
  - Cycle progress
  - Team workload
  - Issue distribution
  - SLA tracking

# Custom Views
View: Cycle Report
Metrics:
  - Scope changes
  - Completed vs planned
  - Bugs introduced
  - Estimate accuracy

# API for Custom Dashboards
Query:
  query CycleMetrics($cycleId: String!) {
    cycle(id: $cycleId) {
      name
      startsAt
      endsAt
      progress
      issues {
        nodes {
          state { name }
          estimate
          completedAt
        }
      }
    }
  }
```

**ClickUp Dashboards:**

```yaml
# Dashboard Setup
1. Home → Dashboards → New Dashboard
2. Add Widgets:

Widgets:
  - Sprint Burndown
    Type: Line chart
    Data: Time vs Remaining points
    Filter: Current sprint

  - Status Distribution
    Type: Pie chart
    Data: Tasks by status

  - Team Workload
    Type: Bar chart
    Data: Tasks by assignee
    Breakdown: Status

  - Time Tracking
    Type: Table
    Data: Logged vs estimated time

  - Goals Progress
    Type: Progress bars
    Data: Sprint goals completion

  - Activity Feed
    Type: List
    Data: Recent comments, completions

# Sharing
- Share link for stakeholders
- Embed in Notion/Confluence
- Schedule email reports
```

**GitHub Projects Insights:**

```yaml
# Built-in Charts
Project Settings → Insights:
  - Burnup chart
  - Items by status
  - Items by iteration

# Custom Charts (via GraphQL API)
query ProjectMetrics($projectId: ID!) {
  node(id: $projectId) {
    ... on ProjectV2 {
      items(first: 100) {
        nodes {
          fieldValues(first: 10) {
            nodes {
              ... on ProjectV2ItemFieldIterationValue {
                iterationId
              }
              ... on ProjectV2ItemFieldSingleSelectValue {
                name  # Status
              }
            }
          }
        }
      }
    }
  }
}

# Third-party: ZenHub, LinearB, Sleuth
- Advanced metrics
- PR analytics
- Deployment tracking
```

**Notion Dashboards:**

```yaml
# Dashboard Page Structure
Page: Team Dashboard
├── Header: Sprint 14 Status
├── Database Views:
│   ├── Linked Database: Tasks (Board view, current sprint)
│   ├── Linked Database: Tasks (Table view, assigned to me)
│   └── Linked Database: Bugs (Gallery view, critical)
├── Callout: Sprint Goal
├── Rollup Metrics:
│   ├── Total Tasks: rollup(count)
│   ├── Completed: rollup(count where status=Done)
│   ├── Progress: formula(Completed/Total * 100)
└── Embeds:
    ├── Google Sheets chart (if needed)
    └── External dashboard link

# Formula Examples
Progress %:
  round(prop("Completed") / prop("Total") * 100)

Days until due:
  dateBetween(prop("Due Date"), now(), "days")

Status emoji:
  if(prop("Progress") >= 80, "🟢",
    if(prop("Progress") >= 50, "🟡", "🔴"))
```

### 4. Custom Reporting

**Report types:**

| Report | Audience | Content | Frequency |
|--------|----------|---------|-----------|
| Sprint Report | Team + PO | Burndown, completed, carryover | End of sprint |
| Weekly Status | Stakeholders | Progress, blockers, next week | Weekly |
| Release Notes | Customers | Features, fixes, improvements | Per release |
| Quarterly Review | Leadership | OKRs, metrics, roadmap | Quarterly |
| Retrospective Summary | Team | Actions, trends | Per sprint |

**Sprint report template:**

```markdown
# Sprint [Number] Report

**Duration:** [Start] - [End]
**Team:** [Team Name]

## Sprint Goal
[Goal statement]

**Achievement:** [Met / Partially Met / Not Met]

## Summary

| Metric | Planned | Actual | Delta |
|--------|---------|--------|-------|
| Story Points | 40 | 38 | -2 |
| Stories | 8 | 7 | -1 |
| Bugs Fixed | 5 | 6 | +1 |
| Velocity | 42 | 38 | -10% |

## Completed Items

| ID | Title | Points | Type |
|----|-------|--------|------|
| PROJ-101 | User login | 5 | Feature |
| PROJ-102 | Dashboard redesign | 8 | Feature |
| PROJ-103 | Fix payment bug | 3 | Bug |

## Carryover Items

| ID | Title | Points | Reason |
|----|-------|--------|--------|
| PROJ-104 | Export feature | 5 | Blocked by API |

## Burndown
[Chart or link to chart]

## Retrospective Actions
1. [Action 1] - Owner: @name
2. [Action 2] - Owner: @name

## Next Sprint Preview
- [Item 1]
- [Item 2]
- [Item 3]
```

**Weekly status email template:**

```markdown
Subject: [Project] Weekly Status - Week of [Date]

## TL;DR
[One sentence summary]

## Progress (Green/Yellow/Red)
Overall Status: 🟢 On Track

| Milestone | Progress | Due | Status |
|-----------|----------|-----|--------|
| MVP | 75% | Feb 15 | 🟢 |
| Beta | 30% | Mar 1 | 🟡 |

## This Week
- Completed user authentication
- Fixed 3 critical bugs
- Deployed v0.3 to staging

## Next Week
- Start payment integration
- Complete API documentation
- User testing prep

## Blockers
- [None] OR
- Waiting on [X] from [Team/Person]

## Risks
- [Risk description] - Mitigation: [Plan]

## Metrics
- Velocity: 42 points (target: 45)
- Bug count: 12 open (down from 18)

---
Dashboard: [Link]
Questions? Reply to this email.
```

### 5. Automation

**Automated report generation:**

```python
import requests
from datetime import datetime, timedelta
from jinja2 import Template

class SprintReporter:
    def __init__(self, pm_tool_client, slack_client):
        self.pm = pm_tool_client
        self.slack = slack_client

    def generate_sprint_report(self, sprint_id: str) -> dict:
        """Generate sprint metrics and report"""
        # Fetch sprint data
        sprint = self.pm.get_sprint(sprint_id)
        issues = self.pm.get_sprint_issues(sprint_id)

        # Calculate metrics
        completed = [i for i in issues if i['status'] == 'Done']
        carryover = [i for i in issues if i['status'] != 'Done']

        planned_points = sum(i.get('story_points', 0) for i in issues)
        completed_points = sum(i.get('story_points', 0) for i in completed)

        return {
            'sprint_name': sprint['name'],
            'start_date': sprint['start_date'],
            'end_date': sprint['end_date'],
            'planned_points': planned_points,
            'completed_points': completed_points,
            'velocity': completed_points,
            'completion_rate': completed_points / planned_points if planned_points else 0,
            'completed_items': completed,
            'carryover_items': carryover,
            'story_count': len([i for i in completed if i['type'] == 'Story']),
            'bug_count': len([i for i in completed if i['type'] == 'Bug'])
        }

    def format_report(self, data: dict) -> str:
        """Format report as markdown"""
        template = Template("""
# Sprint Report: {{ sprint_name }}

**Period:** {{ start_date }} - {{ end_date }}

## Summary
| Metric | Value |
|--------|-------|
| Planned Points | {{ planned_points }} |
| Completed Points | {{ completed_points }} |
| Velocity | {{ velocity }} |
| Completion Rate | {{ (completion_rate * 100)|round }}% |

## Completed ({{ completed_items|length }} items)
{% for item in completed_items %}
- [{{ item.key }}] {{ item.title }} ({{ item.story_points }} pts)
{% endfor %}

## Carryover ({{ carryover_items|length }} items)
{% for item in carryover_items %}
- [{{ item.key }}] {{ item.title }} - {{ item.status }}
{% endfor %}
        """)
        return template.render(**data)

    def send_to_slack(self, channel: str, report: str):
        """Post report to Slack"""
        self.slack.chat_postMessage(
            channel=channel,
            text=f"*Sprint Report*\n```{report}```"
        )

    def schedule_weekly_digest(self):
        """Schedule automated weekly report"""
        import schedule

        def send_digest():
            active_sprint = self.pm.get_active_sprint()
            if active_sprint:
                data = self.generate_sprint_report(active_sprint['id'])
                report = self.format_report(data)
                self.send_to_slack("#team-updates", report)

        schedule.every().friday.at("17:00").do(send_digest)
```

**Slack bot for on-demand reports:**

```python
from slack_bolt import App

app = App(token="xoxb-...")

@app.command("/sprint-status")
def sprint_status(ack, respond, command):
    ack()

    reporter = SprintReporter(pm_client, slack_client)
    sprint = pm_client.get_active_sprint()

    if not sprint:
        respond("No active sprint found.")
        return

    data = reporter.generate_sprint_report(sprint['id'])

    blocks = [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": f"Sprint: {data['sprint_name']}"}
        },
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"*Planned:* {data['planned_points']} pts"},
                {"type": "mrkdwn", "text": f"*Completed:* {data['completed_points']} pts"},
                {"type": "mrkdwn", "text": f"*Velocity:* {data['velocity']}"},
                {"type": "mrkdwn", "text": f"*Progress:* {int(data['completion_rate']*100)}%"}
            ]
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f":white_check_mark: {len(data['completed_items'])} done | :hourglass: {len(data['carryover_items'])} remaining"
            }
        }
    ]

    respond(blocks=blocks)

@app.command("/team-workload")
def team_workload(ack, respond, command):
    ack()

    workload = pm_client.get_team_workload()

    text = "*Team Workload*\n"
    for member in workload:
        bar = "█" * member['tasks'] + "░" * (10 - member['tasks'])
        text += f"• {member['name']}: {bar} ({member['tasks']} tasks)\n"

    respond(text)
```

### 6. Dashboard Templates

**Executive dashboard structure:**

```yaml
Executive Dashboard:
  Header:
    - Portfolio status (pie chart)
    - Budget vs actual (bar chart)
    - Schedule variance (gauge)

  Row 1: Project Health
    - Project cards with RAG status
    - Key milestones timeline

  Row 2: Resources
    - Team allocation heatmap
    - Contractor spend

  Row 3: Risks & Issues
    - Top 5 risks table
    - Escalated issues count

  Footer:
    - Last updated timestamp
    - Link to detailed reports
```

**Team dashboard structure:**

```yaml
Team Dashboard:
  Header:
    - Sprint name and goal
    - Days remaining countdown
    - Sprint health indicator

  Row 1: Sprint Progress
    - Burndown chart (large)
    - Velocity trend (small)

  Row 2: Work Distribution
    - Tasks by status (pie)
    - Tasks by assignee (bar)

  Row 3: Blockers & Alerts
    - Blocked items list
    - Approaching due dates
    - WIP limit warnings

  Row 4: Activity
    - Recent completions
    - Recent comments
    - PR activity (if integrated)
```

**Personal dashboard:**

```yaml
Personal Dashboard:
  Header:
    - "Good morning, [Name]"
    - Today's focus item

  Row 1: My Work
    - My tasks by status (board view)
    - Overdue items alert

  Row 2: Upcoming
    - Due this week calendar
    - Sprint commitments

  Row 3: Activity
    - Mentioned in comments
    - PRs awaiting my review
    - Blocked items I own
```

---

## Templates

### Dashboard Requirements Template

```markdown
## Dashboard Requirements

### Purpose
[What decisions will this dashboard inform?]

### Target Audience
- Primary: [Role]
- Secondary: [Role]

### Key Questions to Answer
1. [Question 1]
2. [Question 2]
3. [Question 3]

### Required Metrics
| Metric | Source | Update Frequency | Visualization |
|--------|--------|------------------|---------------|
| | | | |

### Access & Permissions
- View: [Who]
- Edit: [Who]
- Admin: [Who]

### Technical Requirements
- Tool: [PM tool name]
- Integrations needed: [List]
- Update frequency: [Real-time / Daily / Weekly]
```

### Report Automation Checklist

```markdown
## Report Automation Setup

### Data Sources
- [ ] PM tool API access configured
- [ ] Custom fields defined
- [ ] Filters/JQL queries tested
- [ ] Historical data available

### Automation
- [ ] Report generation script written
- [ ] Schedule configured (cron/scheduler)
- [ ] Error handling and alerts
- [ ] Test run successful

### Distribution
- [ ] Recipients identified
- [ ] Slack/Email channels configured
- [ ] Permissions set
- [ ] Opt-out mechanism (if needed)

### Maintenance
- [ ] Documentation written
- [ ] Owner assigned
- [ ] Review schedule set
- [ ] Feedback collection method
```

---

## Examples

### Example 1: Startup Weekly Dashboard

**Setup:**

```yaml
Tool: Notion
Audience: 10-person startup

Dashboard Contents:
  1. Sprint Progress
     - Linked database: Tasks, Board view
     - Filter: Current sprint

  2. Metrics Block
     - Total tasks: Rollup count
     - Completed: Rollup count (status=Done)
     - Progress bar: Formula

  3. Burn Chart
     - Embed: Google Sheets chart
     - Updated: Daily via script

  4. Blockers
     - Linked database: Tasks, Table view
     - Filter: Status = Blocked

  5. Team Focus
     - Callout blocks per person
     - "This week I'm focused on..."
```

### Example 2: Engineering Team Jira Dashboard

**Configuration:**

```yaml
Dashboard: Engineering Sprint Dashboard

Gadgets:
  - Sprint Burndown Chart
    Board: ENG Board
    Sprint: Active

  - Two Dimensional Filter Statistics
    Filter: Sprint issues
    X: Assignee
    Y: Status
    Stat: Issue Count

  - Filter Results: Blocked
    JQL: project = ENG AND labels = blocked AND sprint in openSprints()
    Columns: Key, Summary, Assignee, Labels

  - Pie Chart: By Type
    Filter: project = ENG AND sprint in openSprints()
    Statistic: Issue Type

  - Created vs Resolved
    Filter: project = ENG
    Period: Last 30 days

  - Velocity Chart
    Board: ENG Board
    Sprints: Last 5

Sharing:
  - Public to team
  - Favorite for quick access
```

---

## Common Mistakes

| Mistake | Impact | Solution |
|---------|--------|----------|
| Too many metrics | Analysis paralysis | Focus on 5-7 key metrics |
| No benchmarks | Can't interpret data | Add targets and trends |
| Manual updates | Outdated data, wasted time | Automate everything |
| One dashboard for all | Irrelevant to most | Create role-specific views |
| Vanity metrics | False confidence | Focus on actionable metrics |
| No action from data | Wasted effort | Link metrics to decisions |
| Complex charts | Misinterpretation | Keep visualizations simple |

---

## Next Steps

1. Identify key metrics for your team
2. Choose dashboard tool/approach
3. Create team dashboard with essentials
4. Add automation for reports
5. Collect feedback and iterate
6. Expand to stakeholder dashboards

---

## Related Methodologies

- M-PMT-011: Agile Ceremonies Setup
- M-PMT-001: Jira Workflow Management
- M-PMT-003: Linear Issue Tracking
- M-PMT-004: GitHub Projects
- M-PMT-007: Notion PM
