# M-PMT-011: Agile Ceremonies Setup

## Metadata

| Field | Value |
|-------|-------|
| **ID** | M-PMT-011 |
| **Category** | PM Tools |
| **Difficulty** | Beginner |
| **Agent** | faion-pm-agent |
| **Skill** | faion-pm-tools-skill |

---

## Problem

Teams adopting Agile struggle with:
- Which ceremonies to implement
- How long each ceremony should take
- What to discuss in each meeting
- How to keep ceremonies effective over time
- Configuring PM tools to support ceremonies

---

## Framework

### 1. Ceremony Overview

**Core Scrum ceremonies:**

| Ceremony | Purpose | Duration | Frequency | Attendees |
|----------|---------|----------|-----------|-----------|
| Sprint Planning | Plan upcoming sprint | 2-4 hours | Start of sprint | Team + PO |
| Daily Standup | Sync and unblock | 15 min | Daily | Team |
| Sprint Review | Demo completed work | 1-2 hours | End of sprint | Team + Stakeholders |
| Sprint Retrospective | Improve process | 1-1.5 hours | End of sprint | Team |
| Backlog Refinement | Prepare future work | 1-2 hours | Weekly or bi-weekly | Team + PO |

**Kanban ceremonies:**

| Ceremony | Purpose | Duration | Frequency |
|----------|---------|----------|-----------|
| Daily Standup | Sync and unblock | 15 min | Daily |
| Replenishment | Add items to board | 30 min | As needed |
| Flow Review | Analyze metrics | 30-60 min | Weekly |
| Service Delivery Review | Customer feedback | 60 min | Bi-weekly |
| Retrospective | Improve process | 1 hour | Monthly |

### 2. Daily Standup

**Format:**

```markdown
## Daily Standup Format

**Time:** 15 minutes max
**When:** Same time daily (recommend morning)
**Where:** Same location/channel
**Who:** Dev team (PO optional, SM facilitates)

### Classic Three Questions
1. What did I complete yesterday?
2. What will I work on today?
3. Any blockers or impediments?

### Alternative: Walk the Board
- Start from rightmost column (closest to Done)
- Discuss each card: "What's needed to move this forward?"
- More focus on work items, less on individuals

### Anti-patterns to Avoid
- Status reports to manager
- Problem-solving (take offline)
- Going over 15 minutes
- Only talking to Scrum Master
- Skipping when "nothing changed"
```

**PM tool setup:**

```yaml
# Jira: Sprint board as visual aid
Board View: Active sprint
Columns: To Do | In Progress | In Review | Done
Filter: Current sprint only

# Linear: Current cycle view
Cycle View: Active cycle
Group by: Status
Show: Assignee badges

# ClickUp: Board view with WIP limits
View: Board
Group by: Status
WIP Limits: In Progress (3 per person)

# Trello: Sprint board
Lists: Backlog | In Progress | Review | Done
Card Aging: Enable to spot stale items
```

**Standup bot automation:**

```python
# Slack standup bot example
import schedule
from datetime import datetime, time

class StandupBot:
    def __init__(self, slack_client, channel: str, team: list):
        self.slack = slack_client
        self.channel = channel
        self.team = team
        self.responses = {}

    def send_prompt(self):
        """Send standup prompt to team"""
        message = """
:sunrise: *Daily Standup* - {date}

Please share your update:
1. What did you complete yesterday?
2. What will you work on today?
3. Any blockers?

Reply in thread below!
        """.format(date=datetime.now().strftime("%A, %B %d"))

        self.slack.chat_postMessage(channel=self.channel, text=message)

    def collect_responses(self, timeout_minutes=30):
        """Collect responses from thread"""
        # Collect for 30 minutes, then post summary
        pass

    def post_summary(self):
        """Post summary of standup responses"""
        summary = "*Standup Summary*\n\n"
        for member, update in self.responses.items():
            summary += f"*{member}:*\n{update}\n\n"

        missing = set(self.team) - set(self.responses.keys())
        if missing:
            summary += f"\n:warning: No update from: {', '.join(missing)}"

        self.slack.chat_postMessage(channel=self.channel, text=summary)


# Schedule standup
schedule.every().day.at("09:00").do(standup_bot.send_prompt)
```

### 3. Sprint Planning

**Agenda:**

```markdown
## Sprint Planning Agenda

**Duration:** 2 hours (1-week sprint) / 4 hours (2-week sprint)
**Attendees:** Dev team, Product Owner, Scrum Master

### Part 1: What (1 hour)
1. **Sprint Goal** (10 min)
   - PO proposes sprint goal
   - Team discusses and commits

2. **Backlog Review** (30 min)
   - PO presents prioritized items
   - Team asks clarifying questions
   - Confirm acceptance criteria

3. **Capacity Planning** (20 min)
   - Calculate available hours
   - Account for PTO, meetings, other work
   - Determine sprint capacity

### Part 2: How (1 hour)
4. **Task Breakdown** (40 min)
   - Break user stories into tasks
   - Estimate tasks (hours or points)
   - Identify dependencies

5. **Commitment** (15 min)
   - Team commits to sprint backlog
   - Verify it fits capacity
   - Final sprint goal confirmation

6. **Logistics** (5 min)
   - Daily standup time
   - Any schedule conflicts
   - Sprint review/retro scheduling
```

**Capacity calculation:**

```markdown
## Sprint Capacity Calculator

### Team Availability
| Member | Days | Hours/Day | Available | PTO | Other | Capacity |
|--------|------|-----------|-----------|-----|-------|----------|
| Alice | 10 | 6 | 60 | 8 | 4 | 48 |
| Bob | 10 | 6 | 60 | 0 | 8 | 52 |
| Carol | 10 | 6 | 60 | 16 | 4 | 40 |
| **Total** | | | 180 | 24 | 16 | **140** |

### Velocity Check
- Last sprint: 42 points
- Average (3 sprints): 45 points
- Planned this sprint: 44 points

### Capacity vs Commitment
- Total capacity: 140 hours
- Estimated work: 132 hours
- Buffer (6%): OK
```

**PM tool configuration:**

```yaml
# Jira: Sprint creation
1. Backlog → Create Sprint
2. Set sprint goal
3. Drag stories into sprint
4. View sprint report

# Linear: Cycle creation
1. Cycles → New Cycle
2. Set dates and goal
3. Add issues to cycle
4. Set cycle targets

# ClickUp: Sprint folder
1. Create Sprint folder (Sprint 14)
2. Move tasks from Backlog list
3. Set sprint duration via custom fields
4. Use Sprint dashboard

# GitHub Projects: Iteration
1. Settings → Iterations
2. Create new iteration
3. Assign issues to iteration
4. Filter board by iteration
```

### 4. Sprint Review (Demo)

**Agenda:**

```markdown
## Sprint Review Agenda

**Duration:** 1-2 hours
**Attendees:** Team, PO, Stakeholders

### Structure
1. **Opening** (5 min)
   - Sprint goal reminder
   - Agenda overview

2. **Demo** (45-60 min)
   - Each completed item demonstrated
   - Team member who built it demos
   - Live environment (not slides)
   - Answer stakeholder questions

3. **Metrics Review** (10 min)
   - What was planned vs completed
   - Burndown chart
   - Any items moved to next sprint

4. **Stakeholder Feedback** (15-20 min)
   - What they liked
   - What could be improved
   - New ideas or priorities
   - Market/customer updates

5. **Backlog Update** (10 min)
   - PO adjusts priorities based on feedback
   - Preview of next sprint
   - Any scope changes

6. **Closing** (5 min)
   - Thank attendees
   - Next review date
```

**Demo checklist:**

```markdown
## Sprint Demo Checklist

### Before Demo
- [ ] All demo items tested
- [ ] Demo environment stable
- [ ] Demo script prepared
- [ ] Screen sharing tested
- [ ] Stakeholders invited
- [ ] Meeting room/link ready

### Demo Items
| Story | Demo By | Environment | Notes |
|-------|---------|-------------|-------|
| USER-123 | Alice | Staging | Show happy + error path |
| USER-124 | Bob | Staging | Use test account |
| USER-125 | Carol | Production | Read-only demo |

### After Demo
- [ ] Feedback documented
- [ ] Action items captured
- [ ] Recording shared (if applicable)
- [ ] Backlog updated
```

### 5. Sprint Retrospective

**Formats:**

```markdown
## Retrospective Formats

### 1. Start/Stop/Continue
- **Start:** What should we start doing?
- **Stop:** What should we stop doing?
- **Continue:** What's working that we should keep?

### 2. What Went Well / What Didn't / Ideas
- **Went Well:** Celebrate successes
- **Didn't Go Well:** Problems encountered
- **Ideas:** Improvements to try

### 3. 4Ls (Liked, Learned, Lacked, Longed For)
- **Liked:** What did you enjoy?
- **Learned:** What did you learn?
- **Lacked:** What was missing?
- **Longed For:** What do you wish we had?

### 4. Sailboat
- **Wind:** What pushed us forward?
- **Anchor:** What held us back?
- **Rocks:** What risks do we see?
- **Island:** Where do we want to be?

### 5. Mad/Sad/Glad
- **Mad:** What frustrated you?
- **Sad:** What disappointed you?
- **Glad:** What made you happy?
```

**Retrospective agenda:**

```markdown
## Retrospective Agenda

**Duration:** 1-1.5 hours
**Attendees:** Dev team, Scrum Master (PO optional)

### Structure
1. **Set the Stage** (5 min)
   - Check-in (one word for the sprint)
   - Review retro agreement (Vegas rule)
   - Explain format

2. **Gather Data** (15 min)
   - Silent brainstorming (sticky notes)
   - Add items to board
   - Read and cluster similar items

3. **Generate Insights** (20 min)
   - Vote on top items to discuss
   - Discuss each item (5 min each)
   - Identify root causes

4. **Decide Actions** (15 min)
   - What will we try next sprint?
   - Who owns each action?
   - How will we track?

5. **Close** (5 min)
   - Review action items
   - Appreciation moment
   - Retro on the retro (optional)

### Action Item Tracking
| Action | Owner | Due | Status |
|--------|-------|-----|--------|
| Reduce meeting time | SM | Next sprint | |
| Add more tests | Team | Ongoing | |
```

**Retro tools:**

| Tool | Features | Best For |
|------|----------|----------|
| Miro/FigJam | Visual boards, voting, timer | Remote teams |
| EasyRetro | Structured templates, anonymous | Quick setup |
| Parabol | Guided facilitation, actions | Consistent retros |
| Notion/ClickUp | Built-in, track actions | Keeping in one tool |

### 6. Backlog Refinement

**Agenda:**

```markdown
## Backlog Refinement Agenda

**Duration:** 1-2 hours
**Frequency:** Weekly or bi-weekly
**Attendees:** Team, PO

### Structure
1. **Review Upcoming Work** (10 min)
   - PO presents next priority items
   - Any items from stakeholders

2. **Clarify Requirements** (30-45 min)
   - Discuss acceptance criteria
   - Ask questions
   - Identify unknowns
   - Break down large items

3. **Estimate** (20-30 min)
   - Planning poker or t-shirt sizing
   - Relative estimation
   - Note any outliers for discussion

4. **Prioritize** (10 min)
   - PO confirms priority order
   - Dependencies identified
   - Technical debt items scheduled

5. **Definition of Ready Check** (10 min)
   - Items meet DoR?
   - What's needed before sprint planning?

### Definition of Ready
- [ ] Clear acceptance criteria
- [ ] Estimated
- [ ] Dependencies identified
- [ ] Design complete (if needed)
- [ ] Small enough for 1 sprint
- [ ] Testable
```

**Estimation techniques:**

```markdown
## Estimation Methods

### Planning Poker
- Each person has cards: 1, 2, 3, 5, 8, 13, 21, ?
- Everyone reveals simultaneously
- Discuss outliers, re-estimate
- Tools: Jira, Linear (built-in), PlanITPoker.com

### T-Shirt Sizing
- XS, S, M, L, XL
- Quick relative sizing
- Convert to points if needed:
  - XS = 1, S = 2, M = 3, L = 5, XL = 8

### Bucket System
For large backlogs:
1. Create buckets: 1, 2, 3, 5, 8, 13, 20, 40, 100
2. Place first item in middle
3. Relative placement of rest
4. Quick pass in silence
5. Discuss disagreements

### Fibonacci Points
| Points | Meaning |
|--------|---------|
| 1 | Trivial (< 2 hours) |
| 2 | Small (half day) |
| 3 | Medium (1 day) |
| 5 | Large (2-3 days) |
| 8 | Very large (1 week) |
| 13 | Epic (needs breakdown) |
```

### 7. Tool Configuration

**Jira setup for ceremonies:**

```yaml
# Sprint Planning
Board Settings:
  - Estimation: Story Points
  - Sprint: 2 weeks
  - Columns: To Do | In Progress | Review | Done

Sprint Planning Meeting:
  - View: Backlog
  - Filter: Stories ready for sprint
  - Action: Create sprint, drag items

# Standup
Board View:
  - Active sprint only
  - Quick filters: My Issues, Blocked
  - Swimlanes by assignee (optional)

# Review
Reports:
  - Sprint Report
  - Burndown Chart
  - Velocity Chart

# Retrospective
External tool or:
  - Create "Retro" issue type
  - Custom fields: What Went Well, Improve, Actions
```

**Linear setup:**

```yaml
# Cycles (Sprints)
Settings → Cycles:
  - Duration: 2 weeks
  - Start day: Monday
  - Auto-archive: After 1 week

# Standup
View: Active Cycle
Group by: Status
Filter: My Issues

# Triage (Backlog Refinement)
Inbox → Triage:
  - Review new issues
  - Assign to project/cycle
  - Set priority and estimate

# Retrospective
Create "Retro" project or use:
  - Labels: retro-action
  - Track actions as issues
```

**ClickUp setup:**

```yaml
# Sprint Structure
Space: [Project]
├── Folder: Sprint 14
│   ├── List: Sprint Backlog
│   ├── List: In Progress
│   ├── List: Done
│   └── List: Retro Actions
├── Folder: Sprint 15
└── List: Product Backlog

# Custom Fields
- Sprint Points (number)
- Story Type (dropdown)
- Sprint Goal (text)

# Views
- Board: Standup view
- Timeline: Sprint planning
- Table: Backlog refinement
- Dashboard: Review metrics

# Automations
When status = Done:
  - Notify #team-channel
  - Add timestamp to "Completed" field
```

---

## Templates

### Ceremony Calendar Template

```markdown
## Sprint Ceremony Calendar

**Sprint:** [Number]
**Duration:** [Start Date] - [End Date]

### Week 1

| Day | Time | Ceremony | Duration | Attendees |
|-----|------|----------|----------|-----------|
| Mon | 10:00 | Sprint Planning | 2 hours | Team + PO |
| Mon-Fri | 09:15 | Daily Standup | 15 min | Team |
| Wed | 14:00 | Backlog Refinement | 1 hour | Team + PO |

### Week 2

| Day | Time | Ceremony | Duration | Attendees |
|-----|------|----------|----------|-----------|
| Mon-Thu | 09:15 | Daily Standup | 15 min | Team |
| Fri | 10:00 | Sprint Review | 1 hour | Team + Stakeholders |
| Fri | 14:00 | Retrospective | 1.5 hours | Team |

### Recurring Calendar Invites
- [ ] Daily Standup (Mon-Fri, 09:15)
- [ ] Sprint Planning (Every other Monday, 10:00)
- [ ] Backlog Refinement (Every Wednesday, 14:00)
- [ ] Sprint Review (Every other Friday, 10:00)
- [ ] Retrospective (Every other Friday, 14:00)
```

### Ceremony Effectiveness Tracker

```markdown
## Ceremony Health Check

**Sprint:** [Number]
**Date:** [Date]

### Rate Each Ceremony (1-5)

| Ceremony | Value | Efficiency | Participation | Score |
|----------|-------|------------|---------------|-------|
| Sprint Planning | | | | |
| Daily Standup | | | | |
| Sprint Review | | | | |
| Retrospective | | | | |
| Backlog Refinement | | | | |

### Feedback
**What's working:**
-

**What needs improvement:**
-

### Action Items
1. [Action]
2. [Action]
```

---

## Examples

### Example 1: Remote Team Setup

**Context:** 6-person distributed team across 3 time zones

**Ceremonies:**

```yaml
Daily Standup:
  Type: Async (Slack bot)
  Time: Post by 10am local time
  Format: Written responses in thread
  Sync call: Tuesday & Thursday only

Sprint Planning:
  Duration: 3 hours (with break)
  Format: Video call + Miro board
  Recording: Yes, for absent team members

Sprint Review:
  Duration: 1 hour
  Format: Video call with screen share
  Recording: Shared with stakeholders

Retrospective:
  Tool: Parabol (async + sync hybrid)
  Async: Gather data (24 hours)
  Sync: Discuss and decide (1 hour)
```

### Example 2: Small Startup (5 people)

**Context:** Early-stage startup, moving fast

**Simplified ceremonies:**

```yaml
Daily Standup:
  Format: Walk the Kanban board
  Duration: 10 minutes
  Focus: Unblocking, not status

Weekly Planning:
  Combined: Planning + Refinement
  Duration: 1.5 hours Monday morning
  Output: Week's priorities clear

Bi-weekly Review:
  Informal demo to stakeholders
  Duration: 30 minutes
  Focus: Feedback, not ceremony

Monthly Retrospective:
  Duration: 1 hour
  Format: Simple Start/Stop/Continue
  Focus: 1-2 actionable improvements
```

---

## Common Mistakes

| Mistake | Impact | Solution |
|---------|--------|----------|
| Standups too long | Time waste, disengagement | Strict 15 min, parking lot |
| No sprint goal | Unclear focus | Always define goal in planning |
| Skipping retros | No improvement | Retros are non-negotiable |
| Demo on slides | No real feedback | Always demo live |
| No action follow-up | Retros feel pointless | Track and review actions |
| Over-ceremonial | Agile theater | Adapt ceremonies to team |
| Under-prepared PO | Wasted planning time | Refinement before planning |

---

## Next Steps

1. Schedule all ceremonies in calendar
2. Configure PM tool views for each ceremony
3. Create ceremony checklists
4. Train team on formats
5. Run first sprint cycle
6. Review and adjust in retrospective

---

## Related Methodologies

- M-PMT-012: Reporting & Dashboards
- M-PMT-001: Jira Workflow Management
- M-PMT-003: Linear Issue Tracking
- M-PMT-010: PM Tool Selection
