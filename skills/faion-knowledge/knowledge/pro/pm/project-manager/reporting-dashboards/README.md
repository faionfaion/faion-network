---
id: dashboard-setup
name: "Dashboard Setup"
domain: PM
skill: faion-project-manager
category: "pm-tools"
---

# Dashboard Setup

## Overview

Practical guide for setting up dashboards, automated reporting, and integrations across PM tools. Includes tool-specific configurations, report templates, and automation.

## When to Use

- Implementing dashboards in PM tools
- Automating status reporting
- Setting up Slack/email notifications
- Connecting PM tools to PowerBI/analytics

## Process/Steps

### 1. Tool-Specific Dashboards

**Jira Dashboard:**
```yaml
jira_dashboard:
  gadgets:
    - name: "Sprint Burndown"
      type: "agile-burndown-chart"
      config:
        board: "Team Board"
        sprint: "current"

    - name: "Sprint Health"
      type: "sprint-health-gadget"
      config:
        board: "Team Board"

    - name: "Created vs Resolved"
      type: "two-dimensional-filter-statistics"
      config:
        filter: "project = PROJ"
        x_axis: "created"
        y_axis: "resolved"

    - name: "Pie Chart - Priority"
      type: "pie-chart"
      config:
        filter: "project = PROJ AND status != Done"
        statistic_type: "priority"

    - name: "Filter Results"
      type: "filter-results"
      config:
        filter: "My Open Issues"
        columns: ["Key", "Summary", "Status", "Priority"]
```

**Linear Dashboard Views:**
```yaml
linear_views:
  cycle_view:
    type: board
    group_by: status
    filter: "cycle:current"

  insights:
    built_in:
      - cycle_velocity
      - issue_completion
      - bug_count
      - team_workload

  roadmap:
    type: timeline
    filter: "project:*"
    group_by: project
```

**ClickUp Dashboard:**
```yaml
clickup_dashboard:
  widgets:
    - type: "Sprint Widget"
      shows: current_sprint

    - type: "Workload"
      group_by: assignee
      show_capacity: true

    - type: "Time Tracking"
      shows: logged_vs_estimated

    - type: "Custom Chart"
      chart_type: line
      x_axis: date
      y_axis: completed_tasks

    - type: "Table"
      filter: "status:in progress"
      columns: ["Name", "Assignee", "Due Date"]
```

### 2. Automated Reporting

**Scheduled Reports:**
```yaml
automated_reports:
  daily_standup:
    schedule: "09:00 weekdays"
    channel: slack_team_channel
    content:
      - in_progress_items
      - blocked_items
      - completed_yesterday

  weekly_status:
    schedule: "Friday 16:00"
    recipients: [stakeholders@company.com]
    format: email
    content:
      - sprint_progress
      - key_accomplishments
      - upcoming_work
      - risks_and_blockers
      - metrics_snapshot

  sprint_report:
    schedule: "sprint_end"
    format: pdf
    content:
      - sprint_goal_status
      - completed_items
      - incomplete_items
      - velocity
      - burndown_chart
      - retrospective_actions
```

**Slack Integration:**
```yaml
slack_reporting:
  daily_digest:
    time: "09:00"
    channel: "#team-updates"
    template: |
      *Daily Digest - {{ date }}*

      📊 *Sprint Progress:* {{ progress }}%
      ✅ *Completed Yesterday:* {{ completed_count }}
      🚧 *In Progress:* {{ in_progress_count }}
      🚫 *Blocked:* {{ blocked_count }}

      <{{ dashboard_url }}|View Dashboard>

  alert_notifications:
    - trigger: "blocked_item_created"
      channel: "#alerts"
      message: "🚨 Item blocked: {{ issue_title }}"

    - trigger: "milestone_approaching"
      channel: "#releases"
      message: "📅 Milestone {{ milestone_name }} due in 3 days"
```

### 3. Report Templates

**Weekly Status Report:**
```markdown
# Weekly Status Report
**Project:** [Project Name]
**Period:** [Start Date] - [End Date]
**Prepared by:** [Name]

## Executive Summary
[1-2 sentence summary of project health]

## Overall Status: 🟢 On Track / 🟡 At Risk / 🔴 Off Track

## Key Accomplishments
- [Accomplishment 1]
- [Accomplishment 2]
- [Accomplishment 3]

## Metrics
| Metric | Target | Actual | Trend |
|--------|--------|--------|-------|
| Sprint Velocity | 40 pts | 38 pts | → |
| Bug Count | < 5 | 3 | ↓ |
| Cycle Time | 4 days | 3.5 days | ↓ |

## Risks & Issues
| # | Description | Impact | Mitigation | Status |
|---|-------------|--------|------------|--------|
| 1 | [Risk] | High | [Action] | Open |

## Next Week's Focus
- [Priority 1]
- [Priority 2]

## Decisions Needed
- [Decision 1 - Owner - By Date]

## Appendix
- [Link to dashboard]
- [Link to detailed metrics]
```

**Sprint Report:**
```markdown
# Sprint [N] Report

## Sprint Overview
| Attribute | Value |
|-----------|-------|
| Sprint Goal | [Goal] |
| Duration | [Start] - [End] |
| Team Size | [N] |

## Goal Achievement: ✅ Met / ⚠️ Partial / ❌ Not Met

## Delivery Summary
| Metric | Committed | Completed | Delta |
|--------|-----------|-----------|-------|
| Stories | 8 | 7 | -1 |
| Points | 34 | 31 | -3 |
| Bugs Fixed | 5 | 6 | +1 |

## Burndown Chart
[Chart Image]

## Completed Items
| Key | Title | Points | Type |
|-----|-------|--------|------|
| #123 | Story A | 5 | Feature |
| #124 | Story B | 3 | Feature |

## Incomplete Items
| Key | Title | Points | Reason |
|-----|-------|--------|--------|
| #130 | Story X | 3 | Blocked by API |

## Velocity Trend
[Chart: Last 6 sprints]

## Quality Metrics
- Bugs Found: [N]
- Bugs Fixed: [N]
- Escaped Defects: [N]
- Test Coverage: [N]%

## Retrospective Highlights
**Continue:** [Item]
**Stop:** [Item]
**Start:** [Item]

## Action Items
| Action | Owner | Status |
|--------|-------|--------|
| [Action] | @name | ⏳ |
```

## Templates/Examples

### Portfolio Dashboard Config

```yaml
portfolio_dashboard:
  title: "Engineering Portfolio"
  refresh: 15_minutes

  row_1:
    - widget: status_overview
      width: 4
      config:
        projects: all
        show: health_status

    - widget: delivery_confidence
      width: 4
      config:
        metric: on_time_percentage
        target: 90

    - widget: resource_utilization
      width: 4
      config:
        show: percentage

  row_2:
    - widget: burnup_chart
      width: 8
      config:
        scope: quarterly_roadmap
        show_scope_changes: true

    - widget: risk_summary
      width: 4
      config:
        show: top_5_risks
        sort_by: impact

  row_3:
    - widget: project_table
      width: 12
      columns:
        - name
        - status
        - progress
        - owner
        - due_date
        - risk_level
```

### Jira JQL Queries for Dashboards

```sql
-- Sprint Scope (current sprint)
project = PROJ AND sprint in openSprints()

-- Completed This Sprint
project = PROJ AND sprint in openSprints() AND status = Done

-- In Progress
project = PROJ AND status = "In Progress"

-- Blocked Items
project = PROJ AND labels = blocked AND status != Done

-- Bugs by Priority (pie chart)
project = PROJ AND type = Bug AND status != Done

-- Created vs Resolved (2D filter)
project = PROJ AND created >= -30d

-- Velocity Data (custom field)
project = PROJ AND sprint in closedSprints() AND status = Done
-- Group by sprint, sum story points

-- Aging Issues
project = PROJ AND status = "In Progress" AND updated < -7d

-- Release Scope
project = PROJ AND fixVersion = "1.0.0"
```

### PowerBI Connection

```python
# Connect PM tool to PowerBI
import requests
import pandas as pd

def fetch_jira_data(jql_query):
    """Fetch Jira data for PowerBI"""
    url = f"{JIRA_URL}/rest/api/3/search"
    headers = {"Authorization": f"Bearer {JIRA_TOKEN}"}
    params = {
        "jql": jql_query,
        "fields": "summary,status,priority,customfield_10026",  # story points
        "maxResults": 1000
    }

    response = requests.get(url, headers=headers, params=params)
    issues = response.json()["issues"]

    return pd.DataFrame([{
        "key": i["key"],
        "summary": i["fields"]["summary"],
        "status": i["fields"]["status"]["name"],
        "priority": i["fields"]["priority"]["name"],
        "story_points": i["fields"].get("customfield_10026", 0)
    } for i in issues])

# Example: Velocity trend
velocity_data = fetch_jira_data(
    "project = PROJ AND sprint in closedSprints() AND status = Done"
)
```

## Best Practices

### Implementation
1. **Start simple** - Add widgets as needed
2. **Test filters** - Ensure queries return correct data
3. **Set permissions** - Control dashboard visibility
4. **Document setup** - Maintain dashboard documentation

### Automation
1. **Choose cadence carefully** - Not too frequent
2. **Format for channel** - Email vs Slack vs PDF
3. **Include context** - Links to details
4. **Handle failures** - Error notifications

### Maintenance
1. **Review regularly** - Remove unused dashboards
2. **Update queries** - Keep filters current
3. **Gather feedback** - Are reports useful?
4. **Optimize performance** - Cache expensive queries

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Analyze and assess | sonnet | Evaluation and planning |
| Execute implementation | haiku | Apply established patterns |
| Review and validate | sonnet | Quality assurance |
| Strategic decision | opus | Novel scenarios |
| Optimize and refine | haiku | Performance tuning |
| Document approach | haiku | Create documentation |

## References

- [Jira Dashboards](https://support.atlassian.com/jira-software-cloud/docs/create-and-customize-a-dashboard/)
- [Linear Insights](https://linear.app/docs/insights)
