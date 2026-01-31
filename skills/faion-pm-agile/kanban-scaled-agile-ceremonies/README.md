---
id: kanban-scaled-agile-ceremonies
name: "Kanban and Scaled Agile Ceremonies"
domain: PM
skill: faion-project-manager
category: "pm-tools"
---

# Kanban and Scaled Agile Ceremonies

## Overview

Alternative agile cadences for teams using Kanban methodology or scaling agile across multiple teams. Covers Kanban service delivery cadences and Enterprise Agile Framework (SAFe) ceremonies.

## When to Use

- Teams using Kanban instead of Scrum
- Continuous flow projects without sprints
- Scaling agile for multiple teams
- Enterprise agile implementations
- Hybrid Kanban/Scrum approaches

## Process/Steps

### 1. Kanban Cadences

**Kanban Alternative Events:**
```yaml
kanban_cadences:
  daily:
    - standup: 15_minutes
      focus: flow_and_blockers

  weekly:
    - replenishment: 30_minutes
      purpose: fill_ready_column
      participants: [PO, team]

    - service_delivery_review: 30_minutes
      purpose: metrics_review
      participants: [team, stakeholders]

  bi_weekly:
    - retrospective: 60_minutes
      purpose: process_improvement

  monthly:
    - strategy_review: 60_minutes
      purpose: align_with_goals
```

**Kanban Standup:**
```yaml
kanban_standup:
  format: walk_the_board
  direction: right_to_left  # start with "Done" column

  agenda:
    1. Review blocked items (highest priority)
    2. Review items close to completion
    3. Review WIP items
    4. Pull new items if capacity available

  focus:
    - flow_efficiency
    - cycle_time
    - blockers
    - wip_limits
```

**Replenishment Meeting:**
```yaml
replenishment:
  frequency: weekly
  duration: 30_minutes
  participants:
    - product_owner: required
    - team_leads: required
    - stakeholders: optional

  agenda:
    - review_ready_queue: 10_minutes
    - prioritize_new_items: 10_minutes
    - estimate_size: 5_minutes
    - commit_to_queue: 5_minutes

  outputs:
    - ready_queue_filled: true
    - priorities_clear: true
    - team_capacity_considered: true
```

**Service Delivery Review:**
```yaml
service_delivery_review:
  frequency: weekly
  duration: 30_minutes
  participants:
    - team: required
    - stakeholders: required
    - customers: optional

  metrics_reviewed:
    - throughput: items_per_week
    - cycle_time: average_days
    - lead_time: average_days
    - wip: current_vs_limits
    - blocked_items: count
    - sla_performance: percentage

  format:
    - metrics_presentation: 10_minutes
    - trend_analysis: 10_minutes
    - improvement_discussion: 10_minutes
```

**Kanban Retrospective:**
```yaml
kanban_retrospective:
  frequency: bi_weekly
  duration: 60_minutes

  focus_areas:
    - process_policies
    - wip_limits_effectiveness
    - flow_efficiency
    - blocker_patterns
    - team_collaboration

  outcomes:
    - policy_changes: documented
    - wip_limit_adjustments: implemented
    - experiments: defined
```

### 2. Scaled Agile Events

**Enterprise Agile Framework Events:**
```yaml
safe_events:
  team_level:
    - iteration_planning
    - daily_standup
    - iteration_review
    - iteration_retrospective

  program_level:
    - pi_planning: 2_days
      participants: all_teams
      outputs: [pi_objectives, program_board]

    - scrum_of_scrums: 15_minutes
      frequency: daily_or_every_other_day
      participants: scrum_masters

    - po_sync: 30_minutes
      frequency: weekly
      participants: product_owners

    - inspect_and_adapt: 3_hours
      frequency: end_of_pi
      purpose: retrospective_at_scale
```

**PI Planning (Program Increment Planning):**
```yaml
pi_planning:
  duration: 2_days
  frequency: every_8_12_weeks
  participants:
    - all_agile_teams
    - product_management
    - system_architects
    - business_owners

  day_1_agenda:
    - business_context: 30_minutes
    - product_vision: 30_minutes
    - architecture_vision: 30_minutes
    - planning_context: 30_minutes
    - team_breakouts: 4_hours
    - draft_plan_review: 1_hour

  day_2_agenda:
    - planning_adjustments: 1_hour
    - team_breakouts: 2_hours
    - final_plan_review: 2_hours
    - confidence_vote: 15_minutes
    - plan_rework_if_needed: 1_hour
    - planning_retrospective: 30_minutes

  outputs:
    - committed_pi_objectives: per_team
    - program_board: dependencies_visible
    - risks_identified: documented
    - confidence_vote: recorded
```

**Scrum of Scrums:**
```yaml
scrum_of_scrums:
  frequency: daily_or_every_other_day
  duration: 15_minutes
  participants:
    - scrum_master_from_each_team
    - release_train_engineer: facilitator

  questions:
    - what_did_your_team_accomplish: since_last
    - what_will_your_team_do: before_next
    - what_impediments: team_facing
    - what_dependencies: with_other_teams

  focus:
    - cross_team_dependencies
    - integration_issues
    - shared_impediments
```

**PO Sync:**
```yaml
po_sync:
  frequency: weekly
  duration: 30_minutes
  participants:
    - product_owners: all_teams
    - product_manager: facilitator

  agenda:
    - feature_priorities: 10_minutes
    - dependency_coordination: 10_minutes
    - upcoming_work: 5_minutes
    - impediments: 5_minutes

  outputs:
    - aligned_priorities: true
    - dependencies_managed: true
    - roadmap_updates: communicated
```

**Inspect and Adapt (I&A):**
```yaml
inspect_and_adapt:
  frequency: end_of_pi
  duration: 3_hours
  participants:
    - all_teams
    - stakeholders
    - leadership

  agenda:
    - pi_system_demo: 45_minutes
      - demonstrate_integrated_work
      - get_stakeholder_feedback

    - quantitative_measurement: 30_minutes
      - review_metrics
      - velocity
      - quality
      - predictability

    - retrospective_workshop: 90_minutes
      - identify_problems
      - root_cause_analysis
      - improvement_backlog

    - action_planning: 15_minutes
      - select_improvements
      - assign_owners
      - track_in_next_pi
```

### 3. Hybrid Approaches

**ScrumBan (Scrum + Kanban):**
```yaml
scrumban_ceremonies:
  from_scrum:
    - sprint_planning: optional_or_simplified
    - daily_standup: walk_the_board
    - retrospective: bi_weekly

  from_kanban:
    - replenishment: weekly
    - wip_limits: enforced
    - continuous_flow: true

  adaptations:
    - timeboxing: flexible
    - commitment: to_wip_not_sprint
    - metrics: cycle_time_and_velocity
```

## Best Practices

### Kanban Ceremonies
1. **Focus on flow** - Optimize for throughput, not utilization
2. **Visualize everything** - Make work and policies visible
3. **Limit WIP** - Enforce work-in-progress limits
4. **Measure and improve** - Use metrics to drive decisions
5. **Evolve policies** - Continuously refine process

### Scaled Agile
1. **Align on cadence** - Synchronize team iterations
2. **Face-to-face PI Planning** - Critical for alignment (or high-quality remote)
3. **Manage dependencies** - Make them visible early
4. **Servant leadership** - RTE and management support teams
5. **Continuous integration** - Integrate frequently across teams

### Remote Ceremonies
1. **Virtual collaboration tools** - Miro, Mural for PI Planning boards
2. **Breakout rooms** - For team planning sessions
3. **Async components** - Pre-work and follow-up in tools
4. **Time zones** - Schedule fairly or rotate inconvenience
5. **Recording** - Capture sessions for review

## Templates/Examples

### Kanban Metrics Dashboard

```markdown
# Kanban Metrics - Week [N]

## Flow Metrics
| Metric | This Week | Last Week | Trend |
|--------|-----------|-----------|-------|
| Throughput | 12 items | 10 items | up |
| Avg Cycle Time | 4.5 days | 5.2 days | improving |
| Avg Lead Time | 8.3 days | 9.1 days | improving |
| Current WIP | 15 items | 14 items | stable |

## WIP Analysis
| Column | Current | Limit | Status |
|--------|---------|-------|--------|
| Ready | 8 | 10 | OK |
| In Progress | 5 | 5 | At Limit |
| Review | 2 | 3 | OK |
| Done (this week) | 12 | - | - |

## Blockers
| Item | Days Blocked | Reason | Owner |
|------|--------------|--------|-------|
| #456 | 3 | API dependency | @dev1 |
| #789 | 1 | Design review | @designer |

## Aging Items
| Item | Days in WIP | Column | Risk |
|------|-------------|--------|------|
| #123 | 8 | In Progress | High |
| #234 | 6 | Review | Medium |
```

### PI Planning Board Template

```markdown
# PI [N] Planning Board

## Program Objectives
1. [Objective 1] - Business Value: [H/M/L]
2. [Objective 2] - Business Value: [H/M/L]
3. [Objective 3] - Business Value: [H/M/L]

## Team Commitments

### Team A
| Iteration | Features | Dependencies |
|-----------|----------|--------------|
| Iteration 1 | Feature A1, A2 | None |
| Iteration 2 | Feature A3 | Team B Feature B1 |
| Iteration 3 | Feature A4 | External API |

### Team B
| Iteration | Features | Dependencies |
|-----------|----------|--------------|
| Iteration 1 | Feature B1 | None |
| Iteration 2 | Feature B2 | Team A Feature A1 |
| Iteration 3 | Feature B3 | None |

## Program Board (Dependencies)
```
Iteration 1:  Team A [A1, A2]
              Team B [B1]

Iteration 2:  Team A [A3] <---- depends on B1
              Team B [B2] <---- depends on A1

Iteration 3:  Team A [A4] <---- External API
              Team B [B3]
```

## Risks
| Risk | Impact | Mitigation | Owner |
|------|--------|-----------|-------|
| External API delay | High | Build stub/mock | @architect |
| Resource conflict | Medium | Cross-train team members | @scrum-master |

## Confidence Vote
Team A: 4/5
Team B: 5/5
Overall: 4.5/5
```

### Scrum of Scrums Template

```markdown
# Scrum of Scrums - [Date]

**Facilitator:** [RTE Name]
**Teams:** [Team A, Team B, Team C]

## Team A (@scrum-master-a)
**Yesterday:** Completed Feature X integration
**Today:** Starting Feature Y
**Blockers:** None
**Dependencies:** Need Team B's API endpoint by EOW

## Team B (@scrum-master-b)
**Yesterday:** Fixed critical bug in payment module
**Today:** Finalizing API for Team A
**Blockers:** Waiting on design review
**Dependencies:** None

## Team C (@scrum-master-c)
**Yesterday:** Deployed to staging environment
**Today:** Performance testing
**Blockers:** Test environment unstable
**Dependencies:** None

## Action Items
- [ ] @team-b: Deliver API endpoint by Friday
- [ ] @devops: Investigate staging environment issues
- [ ] @design: Review Team B mockups by tomorrow
```

## References

- [Kanban Guide](https://www.kanban.university/kanban-guide/)
- [Enterprise Agile Framework Framework](https://scaledagileframework.com/)
- [Kanban Metrics](https://www.atlassian.com/agile/kanban/metrics)
- [PI Planning Guide](https://scaledagileframework.com/pi-planning/)
