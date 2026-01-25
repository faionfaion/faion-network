# PM Domain Skill

> **Entry Point:** Invoked via [/faion-net](../faion-net/CLAUDE.md) or directly as `/faion-project-manager`

## When to Use

- Planning projects (scope, schedule, cost, resources)
- Stakeholder management and engagement
- Risk management and uncertainty handling
- Team development and RACI matrices
- Progress tracking with EVM and metrics
- PM tools (Jira, Linear, ClickUp, GitHub Projects)
- Agile ceremonies and hybrid delivery
- Project closure and lessons learned

## Overview

Project Manager domain skill providing professional PM methodologies for solopreneurs and teams.

**Methodologies:** 50 | **Agent:** faion-pm-agent

## Core Framework

### Performance Domains (8)

| Domain | Focus |
|--------|-------|
| Stakeholder | Engaging stakeholders |
| Team | High-performing teams |
| Development Approach | Predictive/agile/hybrid |
| Planning | Scope, schedule, cost, resources |
| Project Work | Executing and monitoring |
| Delivery | Value and outcomes |
| Measurement | EVM, metrics, dashboards |
| Uncertainty | Risks and complexity |

### Core Principles (12)

Stewardship, Team, Stakeholders, Value, Systems Thinking, Leadership, Tailoring, Quality, Complexity, Risk, Adaptability, Change.

## Architecture

```
faion-project-manager (orchestrator)
├── faion-project-manager:agile (28 methodologies)
│   └── Scrum, Kanban, SAFe, PM tools, dashboards
└── faion-project-manager:traditional (22 methodologies)
    └── PMBoK knowledge areas, EVM, WBS, closure
```

## Sub-Skills

### faion-project-manager:agile (28 methodologies)

Scrum, Kanban, SAFe ceremonies, PM tools (Jira, Linear, ClickUp, GitHub, Azure DevOps), dashboards, reporting, team development, AI in PM, hybrid delivery.

**Location:** `~/.claude/skills/faion-project-manager:agile/`

### faion-project-manager:traditional (22 methodologies)

PMBoK knowledge areas, stakeholder management, planning (scope, schedule, cost, WBS), risk management, EVM, quality, change control, project closure, lessons learned.

**Location:** `~/.claude/skills/faion-project-manager:traditional/`

## Files

| File | Purpose |
|------|---------|
| [SKILL.md](SKILL.md) | Quick methodology selector, PMBoK overview, index |
| [ref-pmbok.md](ref-pmbok.md) | PMBoK 7/8 reference |
| [ref-CLAUDE.md](ref-CLAUDE.md) | External resources, tools, certifications |

## PM Tools

| Tool | Best For |
|------|----------|
| Jira | Enterprise, scaled agile |
| ClickUp | All-in-one workspace |
| Linear | Engineering teams |
| GitHub Projects | Developers |
| Azure DevOps | Microsoft ecosystem |
| Notion | Knowledge + PM |
| Trello | Simple kanban |

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [faion-net](../faion-net/CLAUDE.md) | Parent orchestrator |
| [faion-sdd](../faion-sdd/CLAUDE.md) | Task planning uses PMBoK |
| [faion-business-analyst](../faion-business-analyst/CLAUDE.md) | Requirements feed into scope |
| [faion-product-manager](../faion-product-manager/CLAUDE.md) | Product roadmap aligns with schedule |
| [faion-marketing-manager](../faion-marketing-manager/CLAUDE.md) | Campaign planning |

---

*PM Domain Skill v4.0 - 2 sub-skills | 50 methodologies | PMBoK 7/8*
