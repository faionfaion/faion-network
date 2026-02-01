---
id: tool-migration-basics
name: "Cross-Tool Migration - Basics"
domain: PM
skill: faion-project-manager
category: "pm-tools"
---

# Cross-Tool Migration - Basics

## Overview

Migrating project management tools is a complex undertaking that involves data migration, process adaptation, team training, and maintaining productivity during transition. This methodology provides a structured approach to minimize disruption and maximize success.

## When to Use

- Organization switching PM tools (e.g., Jira to Linear)
- Consolidating multiple tools into one
- Scaling from simple to enterprise-grade solution
- Post-acquisition tool standardization
- Moving from legacy to modern tools

## Migration Assessment

### Pre-Migration Audit

```yaml
audit_checklist:
  data_inventory:
    - total_projects: count
    - total_issues: count
    - total_attachments: size_gb
    - custom_fields: list
    - automations: count
    - integrations: list

  usage_patterns:
    - active_users: count
    - daily_active: percentage
    - key_workflows: list
    - power_users: list
    - pain_points: list

  dependencies:
    - ci_cd_integration: [tool, criticality]
    - slack_integration: [channels, automations]
    - documentation_links: [wiki, confluence]
    - reporting_systems: [dashboards, exports]

  compliance:
    - audit_requirements: [yes/no]
    - data_retention: [policy]
    - access_controls: [requirements]
```

## Tool Mapping

### Field Mapping Template

| Source (Jira) | Target (Linear) | Transformation | Notes |
|---------------|-----------------|----------------|-------|
| Issue Type | Issue Label | Bug→bug, Story→feature | |
| Status | State | Map to closest | Review differences |
| Priority | Priority | 1:1 if available | |
| Story Points | Estimate | Direct transfer | |
| Sprint | Cycle | Match dates | |
| Epic | Project | Create projects | |
| Component | Label | Flatten hierarchy | |
| Fix Version | Milestone | Map by name | |
| Assignee | Assignee | Match by email | |
| Reporter | Creator | May lose data | API limitation |
| Comments | Comments | Preserve thread | |
| Attachments | Attachments | Upload separately | Check size limits |
| Custom Field: X | Custom Field: Y | Transform rule | |

## Field Mapping Spreadsheet

### Standard Fields

| Jira Field | Linear Field | Transformation | Validated |
|------------|--------------|----------------|-----------|
| Summary | Title | Direct copy | Yes |
| Description | Description | Markdown convert | Yes |
| Issue Type | Label | Map: Story→feature | Yes |
| Status | State | See status mapping | Yes |
| Priority | Priority | See priority mapping | Yes |
| Assignee | Assignee | Match by email | Yes |
| Reporter | - | Not migrated | N/A |
| Created | - | System generated | N/A |
| Updated | - | System generated | N/A |
| Sprint | Cycle | Match by date range | Yes |
| Epic Link | Project | Create Linear projects | Yes |
| Story Points | Estimate | Direct copy | Yes |

### Status Mapping

| Jira Status | Linear State |
|-------------|--------------|
| Open | Backlog |
| To Do | Todo |
| In Progress | In Progress |
| In Review | In Review |
| Done | Done |
| Won't Do | Canceled |

### Priority Mapping

| Jira Priority | Linear Priority |
|---------------|-----------------|
| Highest | Urgent |
| High | High |
| Medium | Medium |
| Low | Low |
| Lowest | No Priority |

## Best Practices

### Planning

1. **Involve stakeholders early** - Get buy-in before starting
2. **Document everything** - Current state, decisions, mappings
3. **Plan for parallel run** - Keep both tools temporarily
4. **Identify champions** - Power users to help others

### Data Migration

1. **Clean before migrating** - Don't migrate garbage
2. **Archive old data** - Don't migrate everything
3. **Test thoroughly** - Multiple test migrations
4. **Validate counts** - Ensure nothing lost

### Team Transition

1. **Training before cutover** - Everyone should be ready
2. **Support desk** - Dedicated help during transition
3. **Feedback loops** - Quick iteration on issues
4. **Celebrate milestones** - Acknowledge progress

### Risk Mitigation

1. **Rollback plan** - Always have exit strategy
2. **Incremental migration** - Migrate in waves
3. **Freeze period** - No changes during migration
4. **Audit trail** - Track all migration activities

## Training Program

```yaml
training_tracks:
  basic_user:
    duration: 1_hour
    topics:
      - new_tool_navigation
      - creating_issues
      - updating_status
      - finding_your_work
    format: live_demo

  power_user:
    duration: 2_hours
    topics:
      - advanced_search
      - custom_views
      - automation_basics
      - integrations
    format: workshop

  admin:
    duration: 4_hours
    topics:
      - configuration
      - permissions
      - automation_rules
      - reporting
      - troubleshooting
    format: hands_on
```

## References

- [Atlassian Migration Guide](https://support.atlassian.com/jira-cloud/docs/migrate-from-jira-server-to-jira-cloud/)
- [Linear Import](https://linear.app/docs/import)
- [Change Management (ADKAR)](https://www.prosci.com/methodology/adkar)
- [Data Migration Best Practices](https://www.oreilly.com/library/view/data-migration/9780470392164/)
## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Implement methodology | haiku | Pattern application and configuration |
| Review implementation | sonnet | Code analysis and verification |
| Design strategy | opus | Complex decision-making |

