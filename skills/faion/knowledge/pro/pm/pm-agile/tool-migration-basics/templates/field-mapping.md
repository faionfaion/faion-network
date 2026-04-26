# Field Mapping Table — [Source Tool] to [Target Tool]

**Migration:** [Source] → [Target]  
**Date:** [YYYY-MM-DD]  
**Status:** Draft / Approved / Final

## Standard Fields

| Source Field | Target Field | Transformation | Ambiguity | Won't Migrate | Notes |
|-------------|--------------|----------------|-----------|---------------|-------|
| Summary | Title | Direct copy | No | No | |
| Description | Description | MD to HTML/target format | No | No | Check format conversion |
| Issue Type | Label/Type | Bug→bug, Story→feature | No | No | Verify all types mapped |
| Status | State | See status mapping below | No | No | |
| Priority | Priority | See priority mapping below | No | No | |
| Assignee | Assignee | Match by email | No | No | Pre-resolve user mapping |
| Reporter | — | System-managed in target | No | Yes | Log source reporter in comment |
| Sprint | Cycle/Iteration | Match by date range | Yes | No | Check date boundary behavior |
| Epic Link | Project/Epic | Create target equivalents | Yes | No | Hierarchy may differ |
| Story Points | Estimate | Direct if same scale | No | No | |
| Components | Labels | Flatten hierarchy | Yes | No | Multiple components → multiple labels |
| Fix Version | Milestone | Match by name | Yes | No | Create milestones in advance |
| Custom Field X | — | No equivalent | No | Yes | Archive in source |

## Status Mapping

| Source Status | Target Status | Notes |
|--------------|---------------|-------|
| Open | Backlog | |
| To Do | Todo | |
| In Progress | In Progress | |
| In Review | In Review | |
| Done | Done | |
| Won't Do | Canceled | |
| Reopened | Backlog | Reset to start |

## Priority Mapping

| Source Priority | Target Priority | Notes |
|----------------|-----------------|-------|
| Highest / Critical | Urgent | |
| High | High | |
| Medium | Medium | |
| Low | Low | |
| Lowest | No Priority | |

## Won't Migrate — Decision Log

| Field / Feature | Reason | Alternative |
|-----------------|--------|-------------|
| Reporter field | System-managed in target | Add source reporter to first comment |
| Plugin X data | No target equivalent | Export to CSV and archive |
| Time tracking logs | Target tracks differently | Export to spreadsheet before cutover |

## User ID Mapping

| Source Username | Target Email | Resolved |
|-----------------|--------------|---------|
| jsmith | john.smith@company.com | Yes |
| [unresolved] | [unknown] | No — will drop @mention |

## Validation Checklist

- [ ] All source fields either mapped or explicitly marked "won't migrate"
- [ ] Status mapping covers all statuses in source (query: SELECT DISTINCT status FROM source)
- [ ] Priority mapping covers all priorities
- [ ] User mapping covers all active assignees (query for last 90 days)
- [ ] legacy_id custom field created in target before migration run
- [ ] Field mapping approved by PM lead before dry-run
