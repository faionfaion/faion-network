# M-PMT-010: PM Tool Selection

## Metadata

| Field | Value |
|-------|-------|
| **ID** | M-PMT-010 |
| **Category** | PM Tools |
| **Difficulty** | Beginner |
| **Agent** | faion-pm-agent |
| **Skill** | faion-pm-tools-skill |

---

## Problem

Teams struggle to choose the right PM tool because:
- Too many options with overlapping features
- Different team members have different preferences
- Costs scale unpredictably
- Wrong choice leads to low adoption or re-migration
- Features needed today differ from future needs

---

## Framework

### 1. Requirements Assessment

**Team profile questionnaire:**

```markdown
## PM Tool Requirements Assessment

### Team Size & Structure
- [ ] Solo / 1 person
- [ ] Small team / 2-10 people
- [ ] Medium team / 11-50 people
- [ ] Large team / 51-200 people
- [ ] Enterprise / 200+ people

### Team Distribution
- [ ] Co-located (same office)
- [ ] Hybrid (office + remote)
- [ ] Fully remote
- [ ] Multiple time zones

### Primary Work Type
- [ ] Software development
- [ ] Marketing/Creative
- [ ] Operations
- [ ] Sales
- [ ] Mixed/Cross-functional

### Methodology
- [ ] Scrum (sprints, ceremonies)
- [ ] Kanban (continuous flow)
- [ ] Waterfall (phases)
- [ ] Hybrid/Custom
- [ ] None/Flexible

### Must-Have Features
- [ ] Kanban boards
- [ ] Sprint planning
- [ ] Time tracking
- [ ] Resource management
- [ ] Gantt charts
- [ ] Custom workflows
- [ ] Automations
- [ ] API access
- [ ] Reporting/Analytics
- [ ] Mobile app

### Integration Requirements
- [ ] GitHub/GitLab/Bitbucket
- [ ] Slack/Teams
- [ ] Google Workspace
- [ ] Salesforce
- [ ] Zendesk
- [ ] Other: ___________

### Budget
- [ ] Free only
- [ ] < $10/user/month
- [ ] $10-20/user/month
- [ ] $20-50/user/month
- [ ] Enterprise (custom pricing)
```

### 2. Tool Comparison Matrix

**Feature comparison:**

| Feature | Jira | Linear | ClickUp | Asana | Monday | Notion | Trello | GitHub |
|---------|------|--------|---------|-------|--------|--------|--------|--------|
| **Kanban** | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| **Sprints** | Yes | Yes | Yes | Yes | Yes | DIY | Power-Up | Yes |
| **Roadmap** | Yes | Yes | Yes | Yes | Yes | Yes | Power-Up | Yes |
| **Time Track** | Plugin | No | Yes | Yes | Yes | No | Power-Up | No |
| **Automations** | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| **Custom Fields** | Yes | Yes | Yes | Yes | Yes | Yes | Power-Up | No |
| **API** | REST | GraphQL | REST | REST | REST | REST | REST | REST/GQL |
| **Mobile** | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |

**Team size fit:**

| Tool | Solo | Small (2-10) | Medium (11-50) | Large (51-200) | Enterprise |
|------|------|--------------|----------------|----------------|------------|
| Trello | *** | ** | * | - | - |
| Notion | *** | *** | ** | * | - |
| Linear | ** | *** | *** | ** | * |
| GitHub Projects | ** | *** | ** | ** | * |
| ClickUp | ** | *** | *** | ** | * |
| Asana | ** | *** | *** | *** | ** |
| Monday | ** | *** | *** | *** | ** |
| Jira | * | ** | *** | *** | *** |
| Azure DevOps | - | * | ** | *** | *** |

Legend: *** Best fit | ** Good fit | * Possible | - Not recommended

**Methodology fit:**

| Tool | Scrum | Kanban | Waterfall | Hybrid |
|------|-------|--------|-----------|--------|
| Jira | *** | ** | * | ** |
| Linear | *** | *** | - | ** |
| ClickUp | ** | *** | ** | *** |
| Asana | ** | *** | ** | *** |
| Monday | ** | *** | ** | *** |
| Notion | * | ** | * | *** |
| Trello | * | *** | - | ** |
| GitHub Projects | ** | *** | - | ** |

### 3. Pricing Analysis

**2026 pricing comparison (per user/month, billed annually):**

| Tool | Free | Starter | Pro | Business | Enterprise |
|------|------|---------|-----|----------|------------|
| **Trello** | $0 (10 boards) | $5 | $10 | $17.50 | Custom |
| **Notion** | $0 (personal) | $10 | $15 | $18 | Custom |
| **Linear** | $0 (small team) | - | $10 | - | Custom |
| **GitHub** | $0 (public) | $4 | $21 | - | Custom |
| **ClickUp** | $0 (limited) | $7 | $12 | $19 | Custom |
| **Asana** | $0 (15 users) | $10.99 | $24.99 | $30.49 | Custom |
| **Monday** | $0 (2 users) | $9 | $12 | $19 | Custom |
| **Jira** | $0 (10 users) | $8.15 | - | - | Custom |
| **Azure DevOps** | $0 (5 users) | $6 | - | - | Custom |

**Total cost calculation:**

```markdown
## Cost Calculator

**Team:** [X] users
**Plan:** [Plan name]
**Per user/month:** $[Y]
**Billing:** Annual / Monthly

### Annual Cost
- Users: [X]
- Monthly per user: $[Y]
- Annual per user: $[Y] x 12 = $[Z]
- Total annual: [X] x $[Z] = $[Total]

### Growth Projection
| Year | Users | Monthly Cost | Annual Cost |
|------|-------|--------------|-------------|
| Y1 | 10 | $100 | $1,200 |
| Y2 | 25 | $250 | $3,000 |
| Y3 | 50 | $500 | $6,000 |

### Hidden Costs
- Add-ons/Power-Ups: $[Amount]/month
- Training: $[Amount] one-time
- Migration: $[Amount] one-time
- Integrations: $[Amount]/month
```

### 4. Use Case Recommendations

**By team type:**

```yaml
Software Development Team:
  Small (< 10):
    primary: Linear
    alternative: GitHub Projects
    why: "Developer-focused, fast, clean UI"

  Medium (10-50):
    primary: Linear
    alternative: Jira
    why: "Scales well, good integrations"

  Large (50+):
    primary: Jira
    alternative: Azure DevOps
    why: "Enterprise features, compliance"

Marketing Team:
  Small (< 10):
    primary: Notion
    alternative: Trello
    why: "Flexible, combines docs + tasks"

  Medium (10-50):
    primary: Monday
    alternative: Asana
    why: "Visual, good for campaigns"

  Large (50+):
    primary: Asana
    alternative: Monday
    why: "Workload management, reporting"

Operations Team:
  Small (< 10):
    primary: ClickUp
    alternative: Notion
    why: "All-in-one, good free tier"

  Medium (10-50):
    primary: ClickUp
    alternative: Monday
    why: "Flexible views, automations"

  Large (50+):
    primary: Monday
    alternative: Asana
    why: "Cross-department visibility"

Startup (Mixed Team):
  Small (< 10):
    primary: Notion
    alternative: Linear + Notion
    why: "Wiki + PM in one, free tier"

  Medium (10-50):
    primary: Linear + Notion
    alternative: ClickUp
    why: "Best of both worlds"

Freelancer/Solopreneur:
  primary: Notion
  alternative: Trello
  why: "Free, flexible, personal + client projects"
```

### 5. Evaluation Process

**Trial checklist:**

```markdown
## Tool Trial Evaluation

**Tool:** [Name]
**Trial Period:** [Dates]
**Evaluators:** [Team members]

### Setup (Day 1)
- [ ] Created account
- [ ] Invited test users
- [ ] Imported sample data
- [ ] Configured basic workflow

### Core Workflow (Days 2-5)
- [ ] Created project/board
- [ ] Added tasks with all needed fields
- [ ] Tested status transitions
- [ ] Set up views (board, list, calendar)
- [ ] Tested assignments and notifications

### Collaboration (Days 6-10)
- [ ] Comments and mentions work
- [ ] File attachments work
- [ ] Real-time updates visible
- [ ] Permissions work correctly
- [ ] Mobile app usable

### Integrations (Days 11-12)
- [ ] Connected to Git provider
- [ ] Connected to Slack/Teams
- [ ] Tested webhooks/API
- [ ] Automations work

### Team Feedback (Days 13-14)
- [ ] Collected feedback from testers
- [ ] Identified pain points
- [ ] Noted feature gaps
- [ ] Scored usability (1-10)

### Scoring

| Criteria | Weight | Score (1-10) | Weighted |
|----------|--------|--------------|----------|
| Ease of use | 20% | | |
| Features | 25% | | |
| Integrations | 15% | | |
| Performance | 10% | | |
| Pricing | 15% | | |
| Support/Docs | 10% | | |
| Mobile app | 5% | | |
| **TOTAL** | 100% | | |

### Verdict
- [ ] ADOPT: Meets all requirements
- [ ] CONSIDER: Minor gaps to address
- [ ] REJECT: Does not meet needs
```

**Scoring rubric:**

```yaml
Scoring Guide:
  Ease of Use:
    9-10: Intuitive, minimal training needed
    7-8: Easy with brief learning curve
    5-6: Moderate complexity
    3-4: Significant training required
    1-2: Confusing, poor UX

  Features:
    9-10: All must-haves + nice-to-haves
    7-8: All must-haves
    5-6: Most must-haves
    3-4: Missing key features
    1-2: Fundamentally lacking

  Integrations:
    9-10: All required integrations work well
    7-8: Most integrations available
    5-6: Basic integrations only
    3-4: Limited integration options
    1-2: No useful integrations

  Performance:
    9-10: Fast, no lag
    7-8: Occasionally slow
    5-6: Noticeable delays
    3-4: Frequently slow
    1-2: Unusable performance

  Pricing:
    9-10: Within budget with room to grow
    7-8: Within budget
    5-6: At budget limit
    3-4: Slightly over budget
    1-2: Significantly over budget
```

### 6. Decision Matrix

**Weighted decision matrix template:**

```markdown
## PM Tool Decision Matrix

**Date:** [Date]
**Evaluators:** [Names]
**Finalists:** [Tool A, Tool B, Tool C]

### Criteria Weights
| Criteria | Weight | Rationale |
|----------|--------|-----------|
| Features | 25% | Core functionality critical |
| Ease of Use | 20% | Adoption depends on UX |
| Price | 15% | Budget constraints |
| Integrations | 15% | Workflow automation |
| Scalability | 15% | Future growth |
| Support | 10% | Help when needed |

### Scoring (1-10)

| Criteria | Weight | Tool A | Tool B | Tool C |
|----------|--------|--------|--------|--------|
| Features | 25% | 8 | 9 | 7 |
| Ease of Use | 20% | 9 | 7 | 8 |
| Price | 15% | 7 | 6 | 9 |
| Integrations | 15% | 8 | 9 | 6 |
| Scalability | 15% | 7 | 9 | 6 |
| Support | 10% | 8 | 8 | 7 |

### Weighted Scores

| Criteria | Weight | Tool A | Tool B | Tool C |
|----------|--------|--------|--------|--------|
| Features | 25% | 2.00 | 2.25 | 1.75 |
| Ease of Use | 20% | 1.80 | 1.40 | 1.60 |
| Price | 15% | 1.05 | 0.90 | 1.35 |
| Integrations | 15% | 1.20 | 1.35 | 0.90 |
| Scalability | 15% | 1.05 | 1.35 | 0.90 |
| Support | 10% | 0.80 | 0.80 | 0.70 |
| **TOTAL** | 100% | **7.90** | **8.05** | **7.20** |

### Recommendation
**Winner:** Tool B
**Runner-up:** Tool A

**Rationale:**
Tool B scores highest overall due to superior features and scalability,
despite slightly higher cost. Best fit for our growing engineering team
with strong Git integration needs.
```

### 7. Quick Selection Guide

**Flowchart decision tree:**

```
START: What's your primary need?

├── Software Development
│   ├── Small team (< 15)?
│   │   ├── Want simplicity? → Linear
│   │   └── Want free + GitHub? → GitHub Projects
│   └── Large team (15+)?
│       ├── Enterprise needs? → Jira
│       └── Modern UX preferred? → Linear
│
├── Marketing/Creative
│   ├── Small team?
│   │   ├── Need docs too? → Notion
│   │   └── Visual boards only? → Trello
│   └── Large team?
│       ├── Complex workflows? → Asana
│       └── Visual reports? → Monday
│
├── Operations/General
│   ├── Small team?
│   │   ├── All-in-one? → ClickUp
│   │   └── Simple tasks? → Todoist
│   └── Large team?
│       └── Cross-functional? → Monday or Asana
│
└── Solo/Freelancer
    ├── Client work + personal? → Notion
    ├── Just task boards? → Trello
    └── Dev + tasks? → GitHub Projects
```

**One-liner recommendations:**

| Scenario | Tool | Why |
|----------|------|-----|
| Dev team wanting Jira alternative | Linear | Modern, fast, keyboard-driven |
| Startup needing docs + PM | Notion | All-in-one, great free tier |
| Marketing team visual boards | Monday | Beautiful, easy dashboards |
| Solo dev with multiple projects | GitHub Projects | Free, integrated with code |
| Agency managing client work | ClickUp | Spaces per client, rich features |
| Enterprise software team | Jira | Scalable, compliance, ecosystem |
| Simple personal Kanban | Trello | Easy, free, minimal |

---

## Templates

### Requirements Document Template

```markdown
# PM Tool Requirements

## Overview
- **Team:** [Name/Department]
- **Size:** [X] current, [Y] projected (12 months)
- **Budget:** $[X]/month or $[Y]/year
- **Timeline:** Select by [Date], implement by [Date]

## Must-Have Features
1. [Feature 1]: [Why needed]
2. [Feature 2]: [Why needed]
3. [Feature 3]: [Why needed]

## Nice-to-Have Features
1. [Feature 1]: [Benefit]
2. [Feature 2]: [Benefit]

## Required Integrations
1. [Integration 1]: [Current usage]
2. [Integration 2]: [Current usage]

## Workflow Requirements
- Primary methodology: [Scrum/Kanban/etc.]
- Key workflows:
  - [Workflow 1]
  - [Workflow 2]

## Evaluation Criteria (Weighted)
| Criteria | Weight | Notes |
|----------|--------|-------|
| [Criterion 1] | [X]% | |
| [Criterion 2] | [Y]% | |

## Stakeholders
- Decision maker: [Name]
- Evaluators: [Names]
- End users: [Count/Roles]
```

### Tool Comparison Report Template

```markdown
# PM Tool Comparison Report

**Prepared by:** [Name]
**Date:** [Date]
**Tools Evaluated:** [List]

## Executive Summary
[2-3 sentence recommendation]

## Evaluation Results

### Tool 1: [Name]
**Score:** [X]/10
**Pricing:** $[X]/user/month

**Pros:**
- Pro 1
- Pro 2

**Cons:**
- Con 1
- Con 2

**Best for:** [Use case]

### Tool 2: [Name]
[Same structure]

## Recommendation
**Primary:** [Tool name]
**Alternative:** [Tool name]

## Implementation Plan
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Appendix
- Trial feedback
- Detailed scoring
- Pricing breakdown
```

---

## Examples

### Example 1: Startup Selecting First Tool

**Context:** 8-person startup, 5 devs + 3 non-technical

**Requirements:**
- Free or cheap (< $10/user)
- Dev-friendly with GitHub integration
- Non-technical team can use easily
- Docs and wiki needed

**Evaluation:**

| Tool | Dev UX | Non-dev UX | GitHub | Wiki | Price | Score |
|------|--------|------------|--------|------|-------|-------|
| Linear | 10 | 6 | 9 | No | Free | 7.5 |
| Notion | 7 | 9 | 3 | Yes | Free | 7.0 |
| ClickUp | 7 | 7 | 7 | Yes | Free | 7.2 |
| GitHub | 10 | 4 | 10 | No | Free | 6.5 |

**Decision:** Linear for dev team + Notion for docs/wiki
**Rationale:** Best dev experience, Notion fills docs gap

### Example 2: Agency Migrating from Spreadsheets

**Context:** 15-person marketing agency, managing 20+ clients

**Requirements:**
- Client workspaces/separation
- Time tracking
- Client portal/sharing
- Reporting for clients

**Evaluation:**

| Tool | Workspaces | Time | Portal | Reports | Price/user |
|------|------------|------|--------|---------|------------|
| ClickUp | Spaces | Built-in | Yes | Good | $12 |
| Monday | Workspaces | Add-on | Yes | Great | $19 |
| Asana | Portfolios | Add-on | Limited | Good | $24.99 |

**Decision:** ClickUp
**Rationale:** Best value with all features included, workspaces per client

---

## Common Mistakes

| Mistake | Impact | Solution |
|---------|--------|----------|
| Choosing for features alone | Low adoption | Prioritize UX and team fit |
| Not testing with real work | Surprise issues | Do 2-week trial with real projects |
| Ignoring integration needs | Broken workflows | List integrations upfront |
| Underestimating growth | Re-migration later | Plan for 2x current team |
| Letting one person decide | Team resentment | Involve key users in trial |
| Not considering training | Slow adoption | Budget time for onboarding |

---

## Next Steps

1. Complete requirements assessment
2. Shortlist 2-3 tools based on matrix
3. Run 2-week trial with real projects
4. Collect and score team feedback
5. Make final decision with stakeholders
6. Plan implementation and migration

---

## Related Methodologies

- M-PMT-009: Cross-Tool Migration
- M-PMT-001: Jira Workflow Management
- M-PMT-002: ClickUp Setup
- M-PMT-003: Linear Issue Tracking
- M-PMT-007: Notion PM
- M-PMT-008: Trello Kanban
