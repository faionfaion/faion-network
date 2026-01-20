# PM Domain Skill

Project Manager domain skill providing professional project management methodologies for solopreneurs and teams.

## Overview

- **Name:** faion-project-manager
- **Type:** Domain Skill (orchestrator)
- **Agent:** faion-pm-agent
- **Methodologies:** 46

## Core Framework

### Performance Domains (8)

| Domain | Focus |
|--------|-------|
| Stakeholder | Engaging stakeholders effectively |
| Team | Building high-performing teams |
| Development Approach | Selecting predictive/agile/hybrid |
| Planning | Scope, schedule, cost, resources |
| Project Work | Executing and monitoring activities |
| Delivery | Delivering value and outcomes |
| Measurement | Tracking with EVM, metrics, dashboards |
| Uncertainty | Managing risks and complexity |

### Core Principles (12)

Stewardship, Team, Stakeholders, Value, Systems Thinking, Leadership, Tailoring, Quality, Complexity, Risk, Adaptability, Change.

## Directory Structure

```
faion-project-manager/
├── CLAUDE.md              # This file
├── SKILL.md               # Full skill definition
└── references/            # 46 methodology files + tool guides
    ├── stakeholder-engagement.md
    ├── risk-management.md
    ├── earned-value-management.md
    ├── ... (43 more files)
    └── pm-tools.md
```

## Key Methodologies

| File | Description |
|------|-------------|
| stakeholder-engagement.md | Stakeholder identification and Power/Interest grid |
| risk-management.md | Risk identification, assessment, response strategies |
| earned-value-management.md | EVM metrics (PV, EV, AC, SPI, CPI, EAC) |
| agile-hybrid-approaches.md | Choosing predictive, agile, or hybrid approaches |
| scope-management.md | Scope definition and control |
| schedule-development.md | Timeline planning and tracking |
| quality-management.md | Quality assurance and control |

## PM Tools

| File | Tool |
|------|------|
| jira-workflow-management.md | Jira workflows, JQL, Scrum/Kanban |
| clickup-setup.md | ClickUp views, automation |
| linear-issue-tracking.md | Linear for engineering teams |
| github-projects.md | GitHub Projects for developers |
| azure-devops-boards.md | Azure DevOps enterprise |
| notion-pm.md | Notion databases |
| trello-kanban.md | Trello kanban boards |

## Integration

| Domain Skill | Integration Point |
|--------------|-------------------|
| faion-sdd | Task planning uses PM scheduling |
| faion-business-analyst | Requirements feed into PM scope |
| faion-product-manager | Product roadmap aligns with project schedule |
| faion-marketing-manager | Campaign planning uses PM methods |

## Usage

Execute methodologies via faion-pm-agent:

```
# Called from faion-net or faion-sdd orchestrators
```

---

*PM Domain Skill v2.0*
