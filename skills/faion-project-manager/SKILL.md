---
name: faion-project-manager
user-invocable: false
description: "PM orchestrator: coordinates faion-agile-pm (Scrum, Kanban, tools, modern PM) and faion-traditional-pm (PMBoK, scope, schedule, risk, EVM). 50 total methodologies across 2 sub-skills."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(ls:*), Task, AskUserQuestion, TodoWrite
---

<<<<<<< HEAD
# PM Domain Skill

**Communication: User's language. Docs/code: English.**

## References

| Reference | Content |
|-----------|---------|
| [pm-tools.md](pm-tools.md) | Jira, ClickUp, Linear, GitHub Projects, GitLab, Azure DevOps |
| [pmbok8.md](pmbok8.md) | PMBoK 8 Focus Areas, 7 Domains, 6 Principles, AI in PM |

## Agents

| Agent | When to Use |
|-------|-------------|
| `faion-pm-agent` | Execute PMBoK 7/8 methodologies for project management |

## Purpose

Orchestrates project management activities using PMBoK 7th Edition (2021) and PMBoK 8 principles. Provides professional PM methodologies for solopreneurs and teams.
=======
# PM Domain Skill (Orchestrator)

**Communication: User's language. Docs/code: English.**

## Purpose

Orchestrates project management activities using PMBoK 7/8 framework. Coordinates two specialized sub-skills for comprehensive PM coverage.
>>>>>>> claude

## Architecture

```
faion-project-manager (orchestrator)
    |
    +-> faion-agile-pm (28 methodologies)
    |   - Scrum, Kanban, SAFe ceremonies
    |   - PM tools (Jira, Linear, ClickUp, GitHub, etc.)
    |   - Dashboards, reporting, metrics
    |   - Team development, RACI
    |   - AI in PM, hybrid delivery
    |
    +-> faion-traditional-pm (22 methodologies)
        - PMBoK knowledge areas
        - Stakeholder management
        - Planning (scope, schedule, cost, WBS)
        - Risk management
        - EVM, quality, change control
        - Project closure, lessons learned
```

## References

<<<<<<< HEAD
# Decision Tree: What PM Task?

Use this tree to select the right methodology for your PM need.

## 1. Stakeholder Management

```
Need to work with stakeholders?
    |
    +-> Identify who's involved? --> stakeholder-register.md
    |
    +-> Analyze power/interest? --> stakeholder-engagement.md
    |
    +-> Define responsibilities? --> raci-matrix.md
    |
    +-> Build team agreements? --> team-development.md
```

## 2. Planning & Scope

```
Need to plan the project?
    |
    +-> Define what to build? --> scope-management.md
    |
    +-> Break down work? --> wbs-creation.md / work-breakdown-structure.md
    |
    +-> Create timeline? --> schedule-development.md
    |
    +-> Estimate costs? --> cost-estimation.md
    |
    +-> Choose approach (agile/predictive)? --> agile-hybrid-approaches.md
```

## 3. Execution & Monitoring

```
Need to execute or track?
    |
    +-> Measure performance? --> earned-value-management.md
    |
    +-> Manage changes? --> change-control.md
    |
    +-> Handle communications? --> communications-management.md
    |
    +-> Manage quality? --> quality-management.md
    |
    +-> Track resources? --> resource-management.md
```

## 4. Risk Management

```
Need to manage risks?
    |
    +-> Identify and assess? --> risk-register.md
    |
    +-> Plan responses? --> risk-management.md
```

## 5. Project Lifecycle

```
Project lifecycle activities?
    |
    +-> Integrate all components? --> project-integration.md
    |
    +-> Handle procurement? --> procurement-management.md
    |
    +-> Close project? --> project-closure.md
    |
    +-> Capture lessons? --> lessons-learned.md
    |
    +-> Track benefits? --> benefits-realization.md
```

## 6. PM Tools Selection

```
Need PM tool guidance?
    |
    +-> Enterprise/Scaled Agile? --> jira-workflow-management.md
    |
    +-> Engineering teams? --> linear-issue-tracking.md
    |
    +-> Developer-focused? --> github-projects.md
    |
    +-> Microsoft ecosystem? --> azure-devops-boards.md
    |
    +-> All-in-one workspace? --> clickup-setup.md
    |
    +-> Simple kanban? --> trello-kanban.md
    |
    +-> Knowledge + PM? --> notion-pm.md
    |
    +-> DevOps focus? --> gitlab-boards.md
    |
    +-> Select tool? --> pm-tool-selection.md
    |
    +-> Migrate tools? --> cross-tool-migration.md
```

---

# PMBoK 7 Overview

## Performance Domains (8)

Interactive, interrelated areas that work together throughout a project.

| Domain | Focus | Key Outcome |
|--------|-------|-------------|
| **Stakeholder** | Engaging stakeholders | Agreement on objectives, support |
| **Team** | Building high-performing teams | Shared ownership, growth |
| **Development Approach** | Selecting predictive/agile/hybrid | Right approach for context |
| **Planning** | Scope, schedule, cost, resources | Realistic, achievable plans |
| **Project Work** | Executing and monitoring | Efficient delivery |
| **Delivery** | Value and outcomes | Benefits realized |
| **Measurement** | Tracking with metrics | Data-driven decisions |
| **Uncertainty** | Risks and complexity | Managed uncertainty |

## Principles (12)

| # | Principle | Core Behavior |
|---|-----------|---------------|
| P-01 | Stewardship | Act with integrity, be accountable |
| P-02 | Team | Build culture of accountability and respect |
| P-03 | Stakeholders | Engage proactively |
| P-04 | Value | Focus on outcomes, not outputs |
| P-05 | Systems Thinking | See the whole, understand interdependencies |
| P-06 | Leadership | Inspire, adapt style, enable others |
| P-07 | Tailoring | Adapt processes to context |
| P-08 | Quality | Build quality into processes |
| P-09 | Complexity | Navigate with appropriate strategies |
| P-10 | Risk | Balance risk with reward |
| P-11 | Adaptability | Embrace change, learn from experience |
| P-12 | Change | Enable envisioned future state |

---

# PMBoK 8 Updates

## Key Changes from PMBoK 7

| Aspect | PMBoK 7 | PMBoK 8 |
|--------|---------|---------|
| Principles | 12 | 6 (streamlined) |
| Performance Domains | 8 | 7 (reorganized) |
| AI Coverage | None | Dedicated appendix |
| Sustainability | Mentioned | Core principle |
| Processes | None (principle-based) | 40 non-prescriptive |

## PMBoK 8 Core Principles (6)

1. **Stewardship & Ethics** - Combined ethical responsibility
2. **Collaboration** - Team + stakeholder engagement
3. **Value Optimization** - Continuous value delivery
4. **Systems & Complexity** - Holistic thinking
5. **Adaptability** - Resilience + change management
6. **Sustainability** - NEW - Environmental and social responsibility

## AI in Project Management

| Application | Tools | Use Case |
|-------------|-------|----------|
| Schedule Prediction | Jira Rovo, ClickUp Brain | Forecast delays |
| Risk Analysis | Monday.com AI | Identify patterns |
| Resource Optimization | MS Project Copilot | Balance workloads |
| Status Reporting | Various | Auto-generate summaries |
| Decision Support | ChatGPT, Claude | Scenario analysis |
=======
| Reference | Content |
|-----------|---------|
| [ref-pmbok.md](ref-pmbok.md) | PMBoK 7/8 overview, 8 domains, 12/6 principles |
| [ref-CLAUDE.md](ref-CLAUDE.md) | External resources, tools, certifications |

## Sub-Skills

### faion-agile-pm (28 methodologies)

**Use when:**
- Planning sprints or ceremonies
- Selecting or setting up PM tools
- Building dashboards and reports
- Implementing agile/hybrid approaches
- Team development and roles

**Key methodologies:**
- Scrum/Kanban ceremonies
- Jira, Linear, ClickUp, GitHub Projects
- Dashboard setup, reporting
- Team development, RACI matrix
- AI in PM, hybrid delivery

**Location:** [faion-agile-pm/SKILL.md](faion-agile-pm/SKILL.md)

### faion-traditional-pm (22 methodologies)

**Use when:**
- Planning project scope, schedule, cost
- Managing stakeholders
- Handling risks and uncertainty
- Tracking performance with EVM
- Closing projects and capturing lessons

**Key methodologies:**
- Stakeholder register and engagement
- Scope, WBS, schedule, cost, resources
- Risk register and management
- EVM, quality, change control
- Project closure, lessons learned

**Location:** [faion-traditional-pm/SKILL.md](faion-traditional-pm/SKILL.md)

## Decision Guide

| Task Type | Sub-Skill | Examples |
|-----------|-----------|----------|
| **Agile Execution** | faion-agile-pm | Sprint planning, standups, retros |
| **Tool Selection** | faion-agile-pm | Which PM tool? How to setup? |
| **Reporting** | faion-agile-pm | Dashboards, burn charts, velocity |
| **Team Structure** | faion-agile-pm | RACI, team development |
| **Project Planning** | faion-traditional-pm | Scope, WBS, schedule, cost |
| **Stakeholders** | faion-traditional-pm | Identify, analyze, engage |
| **Risk Management** | faion-traditional-pm | Risk register, responses |
| **Performance** | faion-traditional-pm | EVM (CPI, SPI, EAC) |
| **Project Closure** | faion-traditional-pm | Close, lessons learned, benefits |

## PMBoK 8 Overview

### 8 Performance Domains

| Domain | Sub-Skill |
|--------|-----------|
| Stakeholder | faion-traditional-pm |
| Team | faion-agile-pm |
| Development Approach | faion-agile-pm |
| Planning | faion-traditional-pm |
| Project Work | faion-traditional-pm |
| Delivery | Both |
| Measurement | faion-traditional-pm (EVM) + faion-agile-pm (dashboards) |
| Uncertainty | faion-traditional-pm |

### 12 Core Principles (PMBoK 7)

Stewardship, Team, Stakeholders, Value, Systems Thinking, Leadership, Tailoring, Quality, Complexity, Risk, Adaptability, Change.

## Common Workflows

### New Project

```
1. faion-traditional-pm: stakeholder-register
2. faion-agile-pm: raci-matrix
3. faion-traditional-pm: scope-management, wbs-creation
4. faion-traditional-pm: schedule-development, cost-estimation
5. faion-traditional-pm: risk-register
6. faion-agile-pm: pm-tools-overview (select tool)
```

### Sprint/Iteration

```
1. faion-agile-pm: scrum-ceremonies (planning)
2. faion-agile-pm: dashboard-setup
3. faion-traditional-pm: earned-value-management (track)
4. faion-agile-pm: scrum-ceremonies (review, retro)
```

### Health Check

```
1. faion-traditional-pm: earned-value-management
2. faion-traditional-pm: risk-management
3. faion-traditional-pm: stakeholder-engagement
4. faion-agile-pm: reporting-basics
```
>>>>>>> claude

## Integration Points

<<<<<<< HEAD
# Quick Reference Tables

## Development Approach Selection

| Factor | Predictive | Agile |
|--------|-----------|-------|
| Requirements | Stable, well-defined | Evolving, emergent |
| Technology | Proven, familiar | New, experimental |
| Stakeholder availability | Limited | High |
| Team experience | Traditional PM | Agile methods |
| Risk tolerance | Low | High |
| Delivery frequency | Single | Continuous |

## Estimation Techniques

| Technique | Accuracy | When to Use |
|-----------|----------|-------------|
| Analogous | -50% to +100% | Early stages, ROM |
| Parametric | -10% to +25% | Historical data available |
| Bottom-up | -5% to +10% | Detailed scope defined |
| Three-point | Variable | Risk-aware estimation |

## EVM Quick Reference

| Metric | Formula | Interpretation |
|--------|---------|----------------|
| SV | EV - PV | Schedule variance (+good) |
| CV | EV - AC | Cost variance (+good) |
| SPI | EV / PV | Schedule index (>1 ahead) |
| CPI | EV / AC | Cost index (>1 under budget) |
| EAC | BAC / CPI | Estimate at completion |

## Risk Response Strategies

| For Threats | For Opportunities |
|-------------|-------------------|
| **Avoid** - Eliminate | **Exploit** - Ensure |
| **Mitigate** - Reduce P/I | **Enhance** - Increase P/I |
| **Transfer** - Shift to 3rd party | **Share** - Partner |
| **Accept** - Acknowledge | **Accept** - Take if occurs |

## RAG Status

| Color | Status | Action |
|-------|--------|--------|
| Green | On track | Continue monitoring |
| Amber | At risk | Corrective action needed |
| Red | Off track | Escalation required |

---

# Methodologies (23)

All methodologies are in `` folder.

## Core PM Methodologies

| Name | File | Domain |
|------|------|--------|
| Stakeholder Register | [stakeholder-register.md](stakeholder-register.md) | Stakeholder |
| Stakeholder Engagement | [stakeholder-engagement.md](stakeholder-engagement.md) | Stakeholder |
| Stakeholder Engagement Advanced | [stakeholder-engagement-advanced.md](stakeholder-engagement-advanced.md) | Stakeholder |
| RACI Matrix | [raci-matrix.md](raci-matrix.md) | Team |
| Team Development | [team-development.md](team-development.md) | Team |
| Agile Hybrid Approaches | [agile-hybrid-approaches.md](agile-hybrid-approaches.md) | Development |
| WBS Creation | [wbs-creation.md](wbs-creation.md) | Planning |
| Work Breakdown Structure | [work-breakdown-structure.md](work-breakdown-structure.md) | Planning |
| Schedule Development | [schedule-development.md](schedule-development.md) | Planning |
| Cost Estimation | [cost-estimation.md](cost-estimation.md) | Planning |
| Resource Management | [resource-management.md](resource-management.md) | Planning |
| Scope Management | [scope-management.md](scope-management.md) | Planning |
| Project Integration | [project-integration.md](project-integration.md) | Work |
| Communications Management | [communications-management.md](communications-management.md) | Work |
| Change Control | [change-control.md](change-control.md) | Work |
| Quality Management | [quality-management.md](quality-management.md) | Delivery |
| Earned Value Management | [earned-value-management.md](earned-value-management.md) | Measurement |
| Performance Domains Overview | [performance-domains-overview.md](performance-domains-overview.md) | Measurement |
| Risk Register | [risk-register.md](risk-register.md) | Uncertainty |
| Risk Management | [risk-management.md](risk-management.md) | Uncertainty |
| Procurement Management | [procurement-management.md](procurement-management.md) | Work |
| Lessons Learned | [lessons-learned.md](lessons-learned.md) | Closure |
| Project Closure | [project-closure.md](project-closure.md) | Closure |
| Benefits Realization | [benefits-realization.md](benefits-realization.md) | Delivery |

## PM Tools & Advanced

| Name | File | Purpose |
|------|------|---------|
| Jira Workflow Management | [jira-workflow-management.md](jira-workflow-management.md) | Enterprise agile |
| ClickUp Setup | [clickup-setup.md](clickup-setup.md) | All-in-one PM |
| Linear Issue Tracking | [linear-issue-tracking.md](linear-issue-tracking.md) | Engineering teams |
| GitHub Projects | [github-projects.md](github-projects.md) | Developer PM |
| GitLab Boards | [gitlab-boards.md](gitlab-boards.md) | DevOps PM |
| Azure DevOps Boards | [azure-devops-boards.md](azure-devops-boards.md) | Microsoft ecosystem |
| Notion PM | [notion-pm.md](notion-pm.md) | Knowledge + PM |
| Trello Kanban | [trello-kanban.md](trello-kanban.md) | Simple kanban |
| PM Tool Selection | [pm-tool-selection.md](pm-tool-selection.md) | Choosing tools |
| Cross Tool Migration | [cross-tool-migration.md](cross-tool-migration.md) | Tool migration |
| Agile Ceremonies Setup | [agile-ceremonies-setup.md](agile-ceremonies-setup.md) | Sprint rituals |
| Reporting Dashboards | [reporting-dashboards.md](reporting-dashboards.md) | Metrics, KPIs |
| Hybrid Delivery | [hybrid-delivery.md](hybrid-delivery.md) | Water-Scrum-Fall |
| AI in Project Management | [ai-in-project-management.md](ai-in-project-management.md) | AI tools |
| AI Powered PM Tools | [ai-powered-pm-tools.md](ai-powered-pm-tools.md) | Tool automation |
| Predictive Analytics PM | [predictive-analytics-pm.md](predictive-analytics-pm.md) | ML forecasting |
| Value Stream Management | [value-stream-management.md](value-stream-management.md) | DORA, flow metrics |
| PM Framework Focus Areas | [pm-framework-focus-areas.md](pm-framework-focus-areas.md) | PMBoK 8 focus |
| Seven Performance Domains | [seven-performance-domains.md](seven-performance-domains.md) | PMBoK 8 domains |
| Six Core Principles | [six-core-principles.md](six-core-principles.md) | PMBoK 8 principles |
| PM Certification Alignment 2026 | [pm-certification-alignment-2026.md](pm-certification-alignment-2026.md) | PMP exam prep |
| PM Certification Changes 2026 | [pm-certification-changes-2026.md](pm-certification-changes-2026.md) | Exam updates |

---

# Integration with Other Domain Skills

| Domain Skill | Integration Point |
|--------------|-------------------|
| faion-sdd | Task planning uses PMBoK scheduling |
| faion-business-analyst | Requirements feed into PM scope |
| faion-product-manager | Product roadmap aligns with project schedule |
| faion-marketing-manager | Campaign planning uses PM methods |

---

*PM Domain Skill v3.0 - 2026-01-21*
*Based on PMBoK 7th Edition (2021) and PMBoK 8 updates*
*8 Performance Domains | 12 Principles | 46 Methodologies*
=======
| Domain Skill | Integration |
|--------------|-------------|
| faion-sdd | Task planning uses PMBoK scheduling |
| faion-business-analyst | Requirements feed into scope |
| faion-product-manager | Roadmap aligns with schedule |
| faion-software-developer | Developer tools (GitHub, Linear) |

---

*PM Domain Skill v4.0 - Orchestrator*
*2 sub-skills | 50 methodologies | PMBoK 7/8*
>>>>>>> claude
