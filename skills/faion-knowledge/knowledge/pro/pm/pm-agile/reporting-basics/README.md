---
id: reporting-basics
name: "Reporting Basics"
domain: PM
skill: faion-project-manager
category: "pm-tools"
---

# Reporting Basics

## Overview

Effective reporting transforms raw project data into actionable insights. This methodology covers metrics framework, dashboard types, and key performance indicators for project visibility.

## When to Use

- Setting up new project visibility systems
- Improving existing reporting capabilities
- Creating stakeholder-specific dashboards
- Selecting key metrics and KPIs

## Process/Steps

### 1. Metrics Framework

**Metric Categories:**
```yaml
metrics:
  delivery_metrics:
    - velocity: "Story points completed per sprint"
    - throughput: "Issues completed per time period"
    - cycle_time: "Time from start to completion"
    - lead_time: "Time from request to delivery"
    - burndown: "Work remaining in sprint"
    - burnup: "Work completed over time"

  quality_metrics:
    - escaped_defects: "Bugs found in production"
    - defect_density: "Bugs per story point"
    - rework_rate: "Reopened issues percentage"
    - test_coverage: "Code coverage percentage"

  flow_metrics:
    - wip: "Work in progress count"
    - flow_efficiency: "Active time / total time"
    - cumulative_flow: "Status distribution over time"
    - aging_wip: "Time items spend in each state"

  team_metrics:
    - capacity_utilization: "Actual vs planned hours"
    - focus_factor: "Productive time ratio"
    - team_happiness: "Satisfaction score"
    - predictability: "Commitment vs delivery"
```

### 2. Dashboard Types

**Team Dashboard:**
```yaml
team_dashboard:
  purpose: "Daily team visibility"
  audience: ["developers", "scrum master"]
  refresh: real_time

  widgets:
    - sprint_burndown:
        type: chart
        shows: remaining_work_by_day

    - sprint_board:
        type: kanban
        shows: current_sprint_items

    - blocker_list:
        type: list
        filter: "label:blocked"

    - team_workload:
        type: bar_chart
        shows: issues_per_assignee

    - recent_activity:
        type: feed
        shows: last_24h_updates
```

**Management Dashboard:**
```yaml
management_dashboard:
  purpose: "Sprint/release status"
  audience: ["product owner", "managers"]
  refresh: hourly

  widgets:
    - sprint_progress:
        type: gauge
        shows: percent_complete

    - velocity_trend:
        type: line_chart
        shows: last_6_sprints

    - release_burnup:
        type: chart
        shows: scope_vs_completed

    - risk_register:
        type: list
        shows: open_risks

    - milestone_timeline:
        type: timeline
        shows: upcoming_milestones

    - blockers_summary:
        type: count
        shows: blocked_items_count
```

**Executive Dashboard:**
```yaml
executive_dashboard:
  purpose: "Portfolio health"
  audience: ["executives", "stakeholders"]
  refresh: daily

  widgets:
    - portfolio_status:
        type: status_grid
        shows: all_projects_health

    - delivery_confidence:
        type: gauge
        shows: on_track_percentage

    - resource_allocation:
        type: pie_chart
        shows: team_distribution

    - budget_vs_actual:
        type: bar_chart
        shows: cost_tracking

    - key_milestones:
        type: timeline
        shows: next_90_days

    - risk_heatmap:
        type: matrix
        shows: impact_vs_probability
```

### 3. Key Performance Indicators

**Scrum KPIs:**
```yaml
scrum_kpis:
  velocity:
    formula: "SUM(story_points) WHERE sprint = X AND status = Done"
    target: "Trending up or stable"
    display: line_chart_last_10_sprints

  sprint_commitment:
    formula: "completed_points / committed_points * 100"
    target: ">= 85%"
    display: gauge

  sprint_goal_achieved:
    formula: "Count where sprint_goal = met"
    target: "100%"
    display: binary_indicator

  escaped_defects:
    formula: "bugs_in_production per sprint"
    target: "< 2"
    display: number_with_trend
```

**Kanban KPIs:**
```yaml
kanban_kpis:
  throughput:
    formula: "COUNT(issues) WHERE completed_date in period"
    target: "Trending up"
    display: bar_chart_weekly

  cycle_time:
    formula: "AVG(completed_date - started_date)"
    target: "< 5 days"
    display: histogram

  wip_compliance:
    formula: "COUNT(issues in_progress) <= WIP_limit"
    target: "100%"
    display: percentage

  flow_efficiency:
    formula: "active_time / (active_time + wait_time) * 100"
    target: "> 40%"
    display: gauge
```

### 4. Dashboard Design Principles

**Information Hierarchy:**
```
Level 1: Overall Health (traffic light)
├── Level 2: Key Metrics (numbers)
│   ├── Level 3: Trend Charts (graphs)
│   │   └── Level 4: Detailed Data (tables)
```

**Color Coding:**
```yaml
status_colors:
  green: "On track, no issues"
  yellow: "At risk, needs attention"
  red: "Off track, requires escalation"
  blue: "Information, neutral"
  gray: "Not started, N/A"
```

**Widget Layout:**
```
+------------------+------------------+
|   Main Metric    |  Secondary       |
|   (Large)        |  Metric          |
+------------------+------------------+
|                                     |
|   Primary Chart                     |
|   (Wide, important trend)           |
|                                     |
+------------------+------------------+
| Quick Stats | Quick Stats | Quick   |
| (Small)     | (Small)     | Stats   |
+------------------+------------------+
|                                     |
|   Detailed Table (scrollable)       |
|                                     |
+-------------------------------------+
```

## Best Practices

### Dashboard Design
1. **Less is more** - Focus on actionable metrics
2. **Context matters** - Include targets and trends
3. **Update automatically** - Real-time when possible
4. **Mobile-friendly** - Accessible anywhere
5. **Consistent layout** - Familiar patterns

### Metric Selection
1. **Align with goals** - Measure what matters
2. **Balance lagging/leading** - Past and predictive
3. **Avoid vanity metrics** - Must drive decisions
4. **Limit to 5-7 key metrics** - Prevent overload

### Reporting
1. **Know your audience** - Tailor detail level
2. **Lead with insights** - Not just data
3. **Include actions** - What to do next
4. **Regular cadence** - Build trust through consistency

### Continuous Improvement
1. **Review effectiveness** - Are dashboards used?
2. **Gather feedback** - Ask stakeholders
3. **Iterate design** - Improve based on usage
4. **Archive old dashboards** - Keep system clean

## References

- [Scrum Metrics](https://www.scrum.org/resources/blog/agile-metrics)
- [Kanban Metrics](https://www.kanbanize.com/kanban-resources/kanban-analytics)
- [Information Dashboard Design (Stephen Few)](https://www.perceptualedge.com/library.php)
## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Implement methodology | haiku | Pattern application and configuration |
| Review implementation | sonnet | Code analysis and verification |
| Design strategy | opus | Complex decision-making |

