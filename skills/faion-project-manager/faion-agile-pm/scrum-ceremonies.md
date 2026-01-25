---
id: scrum-ceremonies
name: "Scrum Ceremonies"
domain: PM
skill: faion-project-manager
category: "pm-tools"
---

# Scrum Ceremonies

## Overview

Scrum ceremonies (events) provide the rhythm and structure for iterative development. This methodology covers the setup, facilitation, and optimization of core Scrum events: Sprint Planning, Daily Standup, Sprint Review, Retrospective, and Backlog Refinement.

## When to Use

- Starting a new Scrum team
- Transitioning from waterfall to agile
- Optimizing existing ceremony effectiveness
- Remote/hybrid team ceremony adaptation

## Process/Steps

### 1. Scrum Events Overview

```
Sprint Timeline (2 weeks):
Day 1: Sprint Planning (2-4 hrs)
├── Daily Standup (15 min) × 10 days
├── Backlog Refinement (1-2 hrs) mid-sprint
└── Day 10:
    ├── Sprint Review (1-2 hrs)
    └── Sprint Retrospective (1-2 hrs)
```

**Time Boxing:**
| Event | 1-Week Sprint | 2-Week Sprint | 4-Week Sprint |
|-------|---------------|---------------|---------------|
| Sprint Planning | 2 hours | 4 hours | 8 hours |
| Daily Standup | 15 minutes | 15 minutes | 15 minutes |
| Sprint Review | 1 hour | 2 hours | 4 hours |
| Retrospective | 45 minutes | 1.5 hours | 3 hours |
| Refinement | 1-2 hours | 2-4 hours | 4-8 hours |

### 2. Sprint Planning

**Setup in PM Tool:**
```yaml
sprint_planning:
  preparation:
    - product_backlog_refined: true
    - sprint_goal_drafted: true
    - team_capacity_calculated: true
    - previous_velocity_reviewed: true

  agenda:
    - part_1_what: 60_minutes
      - review_sprint_goal
      - review_top_backlog_items
      - clarify_acceptance_criteria
      - team_asks_questions

    - part_2_how: 60_minutes
      - break_down_stories_to_tasks
      - estimate_tasks
      - identify_dependencies
      - commit_to_sprint_backlog

  outputs:
    - sprint_goal: documented
    - sprint_backlog: in_tool
    - capacity: recorded
```

**Tool Configuration:**

**Jira:**
```yaml
jira_sprint_planning:
  views:
    - backlog_view: enabled
    - sprint_planning_mode: enabled

  filters:
    - refined_stories: "status = 'Ready' AND sprint IS EMPTY"

  fields_shown:
    - story_points
    - acceptance_criteria
    - priority
    - components

  capacity_planning:
    - team_members: list
    - days_off: calendar
    - velocity_chart: displayed
```

**Linear:**
```yaml
linear_sprint_planning:
  cycle_setup:
    - create_new_cycle: true
    - set_dates: start_end
    - set_scope: true

  views:
    - backlog_filter: "state:backlog"
    - priority_sort: true

  fields:
    - estimate
    - project
    - label
```

### 3. Daily Standup

**Format Options:**

**Classic Three Questions:**
```
1. What did I do yesterday?
2. What will I do today?
3. Any blockers?
```

**Walk-the-Board:**
```
1. Start from rightmost column (closest to done)
2. Discuss each item's status
3. Focus on flow, not individuals
4. Identify blocked items
```

**Async Standup (Remote):**
```yaml
async_standup:
  tool: slack  # or standup bot
  time: "09:00 team timezone"

  template: |
    **Yesterday:** [completed items]
    **Today:** [planned items]
    **Blockers:** [any impediments]
    **FYI:** [optional updates]

  rules:
    - post_by: "09:30"
    - thread_for_discussion: true
    - emoji_reactions_for_ack: true
```

**Tool Integration:**
```yaml
standup_automation:
  jira:
    - quick_filter: "My In Progress"
    - board_view: sprint_board
    - update_during_standup: real_time

  slack_bot:
    - geekbot: scheduled
    - standuply: scheduled
    - daily_bot: scheduled

  video:
    - zoom: 15_min_room
    - meet: recurring
    - teams: channel_meeting
```

### 4. Sprint Review (Demo)

**Setup:**
```yaml
sprint_review:
  preparation:
    - demo_environment_ready: staging
    - demo_script_prepared: true
    - stakeholders_invited: true
    - metrics_gathered: true

  agenda:
    - welcome: 5_minutes
    - sprint_goal_recap: 5_minutes
    - demonstrations: 45_minutes
    - feedback_collection: 15_minutes
    - backlog_discussion: 15_minutes
    - next_sprint_preview: 5_minutes

  demo_format:
    per_story:
      - context: "User story and why"
      - demo: "Live demonstration"
      - acceptance: "Criteria met"
      - feedback: "Questions and input"
```

**PM Tool Reporting:**
```yaml
review_metrics:
  display:
    - sprint_goal_achieved: yes_no
    - stories_completed: count
    - story_points_completed: sum
    - bugs_fixed: count
    - velocity_trend: chart

  jira_dashboard:
    widgets:
      - sprint_burndown
      - velocity_chart
      - control_chart
      - cumulative_flow

  linear_view:
    - cycle_summary
    - completed_issues
    - team_metrics
```

### 5. Sprint Retrospective

**Formats:**

**Start-Stop-Continue:**
```
| Start | Stop | Continue |
|-------|------|----------|
| [What should we begin doing?] | [What should we stop?] | [What works well?] |
```

**4Ls:**
```
| Liked | Learned | Lacked | Longed For |
|-------|---------|--------|------------|
| [Positive experiences] | [New insights] | [What was missing] | [Wishes] |
```

**Sailboat:**
```
         Star (Goal)
              |
         Boat (Team)
        /   \
    Wind     Anchor
  (Helps)   (Holds back)

Rocks (Risks ahead)
```

**Mad-Sad-Glad:**
```
| Mad | Sad | Glad |
|--------|--------|---------|
| [Frustrations] | [Disappointments] | [Celebrations] |
```

**Tool Setup:**
```yaml
retro_tools:
  dedicated:
    - retrium: full_features
    - easyretro: simple
    - parabol: integrated_standups
    - miro: visual_boards

  in_pm_tool:
    jira:
      - confluence_page: template
      - sprint_report: link

    notion:
      - retro_database: create
      - template: apply

    linear:
      - project_doc: create
```

### 6. Backlog Refinement

**Setup:**
```yaml
refinement_session:
  frequency: once_per_sprint
  duration: 1_to_2_hours
  participants:
    - product_owner: required
    - dev_team: required
    - scrum_master: facilitates

  agenda:
    - review_upcoming_items: 20_minutes
    - clarify_requirements: 30_minutes
    - break_down_large_items: 20_minutes
    - estimate_items: 20_minutes
    - prioritize: 10_minutes

  definition_of_ready:
    - acceptance_criteria_defined: true
    - dependencies_identified: true
    - estimate_provided: true
    - small_enough: true  # fits in sprint
    - testable: true
```

**Estimation Techniques:**

**Planning Poker:**
```yaml
planning_poker:
  scale: [1, 2, 3, 5, 8, 13, 21, "?", "coffee"]
  tools:
    - planningpoker.com
    - scrumpoker-online.org
    - integrated_in_jira

  process:
    1. PO presents story
    2. Team asks questions
    3. Everyone votes secretly
    4. Reveal simultaneously
    5. Discuss outliers
    6. Re-vote if needed
    7. Consensus recorded
```

**T-Shirt Sizing:**
```
| Size | Relative Effort | Story Points |
|------|-----------------|--------------|
| XS | Very small, few hours | 1 |
| S | Small, ~1 day | 2-3 |
| M | Medium, 2-3 days | 5 |
| L | Large, ~1 week | 8 |
| XL | Very large, needs split | 13+ |
```

## Best Practices

### General Principles
1. **Time-box strictly** - End on time, always
2. **Prepare in advance** - Agendas, data, environment
3. **Focus on outcomes** - Not just going through motions
4. **Rotate facilitation** - Build team capability

### Remote Ceremonies
1. **Cameras on** - Increases engagement
2. **Async prep** - Share materials beforehand
3. **Interactive tools** - Miro, FigJam, digital boards
4. **Shorter sessions** - Zoom fatigue is real
5. **Record for absent** - Respect time zones

### Tool Integration
1. **Single source of truth** - Use PM tool during ceremonies
2. **Real-time updates** - Update board during standup
3. **Automated reporting** - Dashboards for reviews
4. **Action item tracking** - Retro actions in backlog

### Continuous Improvement
1. **Measure effectiveness** - Ceremony health surveys
2. **Experiment** - Try new formats
3. **Adapt to team** - No one-size-fits-all
4. **Regular meta-retros** - Retrospective on retrospectives

## Templates/Examples

### Sprint Planning Template

```markdown
# Sprint [N] Planning

## Sprint Info
| Item | Value |
|------|-------|
| Duration | [Start Date] - [End Date] |
| Working Days | [N] |
| Team Capacity | [N] person-days |

## Sprint Goal
> [One sentence describing what we're trying to achieve]

## Team Capacity
| Member | Days Available | Focus Area | Notes |
|--------|----------------|------------|-------|
| @dev1 | 10 | Backend | |
| @dev2 | 8 | Frontend | PTO Friday |
| @dev3 | 10 | Full-stack | |

**Total Capacity:** [N] person-days

## Sprint Backlog

### Committed
| ID | Title | Points | Assignee |
|----|-------|--------|----------|
| #123 | Story A | 5 | @dev1 |
| #124 | Story B | 3 | @dev2 |

**Total Points:** [N]
**Velocity (3-sprint avg):** [N]

### Stretch Goals
| ID | Title | Points |
|----|-------|--------|
| #130 | Nice to have | 2 |

## Risks & Dependencies
- [ ] Risk 1: [description] - Mitigation: [action]
- [ ] Dependency: Story B depends on API from Team X

## Action Items
- [ ] @dev1: Set up test environment by Day 2
- [ ] @PO: Provide design assets by Day 1
```

### Retrospective Template

```markdown
# Sprint [N] Retrospective

**Date:** [Date]
**Facilitator:** [Name]
**Attendees:** [List]

## Sprint Metrics
| Metric | Value | Trend |
|--------|-------|-------|
| Velocity | [N] pts | up/down/same |
| Commitment | [N]% | up/down/same |
| Bugs Escaped | [N] | up/down/same |

## What Went Well
- [Item 1]
- [Item 2]
- [Item 3]

## What Could Improve
- [Item 1]
- [Item 2]
- [Item 3]

## Action Items
| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|
| [Action 1] | @name | [Date] | Pending |
| [Action 2] | @name | [Date] | Pending |

## Previous Action Items Review
| Action | Owner | Status |
|--------|-------|--------|
| [Previous action] | @name | Done/Not Done |

## Team Health Check
| Dimension | Score (1-5) |
|-----------|-------------|
| Team morale | 4 |
| Process clarity | 3 |
| Technical health | 4 |
```

### Standup Bot Configuration

```yaml
# Geekbot Configuration
standup:
  name: "Daily Standup"
  channel: "#team-standups"
  time: "09:00"
  timezone: "Europe/Kyiv"
  days: ["monday", "tuesday", "wednesday", "thursday", "friday"]

  questions:
    - text: "What did you accomplish yesterday?"
      required: true

    - text: "What are you working on today?"
      required: true

    - text: "Any blockers or help needed?"
      required: true

    - text: "How are you feeling? (optional)"
      required: false

  settings:
    send_to_channel: true
    allow_edits: true
    remind_after: 30_minutes
    skip_on_absence: true
```

## References

- [Scrum Framework](https://scrumguides.org/)
- [Agile Retrospectives (Derby & Larsen)](https://pragprog.com/titles/dlret/agile-retrospectives/)
- [Retromat - Retro Ideas](https://retromat.org/)
