# PM Domain Skill

Project Manager domain skill based on PMBOK 7th Edition (2021) and PMBOK 8 (2026). Provides professional project management methodologies for solopreneurs and teams.

## Overview

- **Name:** faion-project-manager
- **Type:** Domain Skill (orchestrator)
- **Agent:** faion-pm-agent
- **Methodologies:** 24 (M-PM-001 to M-PM-020, plus M-PM-021 to M-PM-030 in references)

## Core Framework

### PMBOK 7 Performance Domains (8)

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

### PMBOK 7 Principles (12)

Stewardship, Team, Stakeholders, Value, Systems Thinking, Leadership, Tailoring, Quality, Complexity, Risk, Adaptability, Change.

### PMBOK 8 Updates (2026)

- 6 streamlined principles (down from 12)
- 7 updated performance domains
- 5 Focus Areas (process groups reframed)
- AI in PM appendix
- Value Stream Management integration

## Directory Structure

```
faion-project-manager/
├── CLAUDE.md              # This file
├── SKILL.md               # Full skill definition with inline methodologies
├── methodologies/         # Individual methodology files (M-PM-001 to M-PM-020)
│   └── CLAUDE.md          # Methodologies index
└── references/            # Extended references
    ├── CLAUDE.md          # References index
    ├── pm-tools.md        # Jira, ClickUp, Linear, GitHub Projects, etc.
    └── pmbok8.md          # PMBOK 8 updates, AI in PM, VSM
```

## Subfolders

| Folder | Content |
|--------|---------|
| [methodologies/](methodologies/) | 24 individual PMBOK methodology files covering stakeholders, planning, execution, risk, quality, and closure |
| [references/](references/) | Extended reference guides for PM tools and PMBOK 8 updates |

## Key Files

| File | Description |
|------|-------------|
| SKILL.md | Complete skill definition with 8 Performance Domains, 12 Principles, 20 inline methodologies |
| methodologies/M-PM-001_stakeholder_engagement.md | Stakeholder identification and Power/Interest grid |
| methodologies/M-PM-006_risk_management.md | Risk identification, assessment, and response strategies |
| methodologies/M-PM-007_earned_value_management.md | EVM metrics (PV, EV, AC, SPI, CPI, EAC) |
| methodologies/M-PM-012_agile_hybrid_approaches.md | Choosing predictive, agile, or hybrid approaches |
| references/pm-tools.md | Comprehensive guide to Jira, ClickUp, Linear, GitHub Projects, Azure DevOps |
| references/pmbok8.md | PMBOK 8 Focus Areas, AI in PM, Value Stream Management |

## Integration

| Domain Skill | Integration Point |
|--------------|-------------------|
| faion-sdd | Task planning uses PMBOK scheduling |
| faion-business-analyst | Requirements feed into PMBOK scope |
| faion-product-manager | Product roadmap aligns with project schedule |
| faion-marketing-manager | Campaign planning uses PMBOK methods |

## Usage

Execute methodologies via faion-pm-agent:

```
Call faion-pm-agent with:
  methodology: "M-PM-001" (Stakeholder Register)
  methodology: "M-PM-007" (Earned Value Management)
  methodology: "M-PM-016" (Risk Register)
```

---

*PM Domain Skill v2.0 - 2026-01-18*
*Based on PMBOK 7th Edition (2021) and PMBOK 8 (2026)*
