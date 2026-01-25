# Business Analyst Skill

> **Entry Point:** Invoked via [/faion-net](../faion-net/CLAUDE.md) or directly as `/faion-business-analyst`

## When to Use

- Planning BA approach and stakeholder analysis
- Requirements elicitation (interviews, workshops, documentation review)
- Requirements lifecycle management and traceability
- Strategy analysis (current/future state, gap analysis)
- Use case modeling and user story mapping
- Business process analysis (BPMN)
- Solution evaluation and assessment

## Overview

BA orchestrator with 2 sub-skills, 28 methodologies across 6 Knowledge Areas.

**Agent:** faion-ba-agent

---

## Architecture

```
faion-business-analyst (orchestrator)
├── faion-business-analyst:core (21 methodologies)
│   └── Planning, Elicitation, Lifecycle, Strategy, Evaluation
└── faion-business-analyst:modeling (7 methodologies)
    └── Use Cases, User Stories, BPMN, ERD, Decision Tables
```

---

## Quick Decision

| If you need... | Sub-Skill | Key Methodology |
|----------------|-----------|-----------------|
| Plan BA approach | business-analyst:core | ba-planning, stakeholder-analysis |
| Gather requirements | business-analyst:core | elicitation-techniques |
| Track requirements | business-analyst:core | requirements-traceability |
| Analyze state | business-analyst:core | strategy-analysis |
| Model requirements | business-analyst:modeling | use-case-modeling, user-story-mapping |
| Evaluate solution | business-analyst:core | solution-assessment |

---

## Sub-Skills

### faion-business-analyst:core (21 methodologies)

Planning, elicitation, requirements lifecycle, strategy analysis, solution evaluation, modern practices.

**Location:** `~/.claude/skills/faion-business-analyst:core/`

### faion-business-analyst:modeling (7 methodologies)

Use cases, user stories, BPMN, ERD, decision tables, interfaces, acceptance criteria.

**Location:** `~/.claude/skills/faion-business-analyst:modeling/`

---

## 6 Knowledge Areas

| # | Knowledge Area | Focus | Sub-Skill |
|---|----------------|-------|-----------|
| 1 | BA Planning & Monitoring | Approach, stakeholders | business-analyst:core |
| 2 | Elicitation & Collaboration | Gather information | business-analyst:core |
| 3 | Requirements Lifecycle | Trace, maintain, prioritize | business-analyst:core |
| 4 | Strategy Analysis | Current/future state, gaps | business-analyst:core |
| 5 | Requirements Analysis & Design | Model, verify, validate | business-analyst:modeling |
| 6 | Solution Evaluation | Measure, assess, improve | business-analyst:core |

**Detailed overview:** [knowledge-areas-detail.md](knowledge-areas-detail.md)

---

## Files

| File | Purpose |
|------|---------|
| [SKILL.md](SKILL.md) | Main orchestrator |
| [knowledge-areas-detail.md](knowledge-areas-detail.md) | 6 KAs overview |
| [ref-CLAUDE.md](ref-CLAUDE.md) | References overview |

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [faion-net](../faion-net/CLAUDE.md) | Parent orchestrator |
| [faion-product-manager](../faion-product-manager/CLAUDE.md) | Provides product vision |
| [faion-project-manager](../faion-project-manager/CLAUDE.md) | Uses requirements for scope |
| [faion-sdd](../faion-sdd/CLAUDE.md) | Transforms requirements into specs |
| [faion-software-architect](../faion-software-architect/CLAUDE.md) | Uses requirements for architecture |

---

*BA Domain Skill v4.0 | 28 Methodologies | 2 Sub-Skills | 6 Knowledge Areas*
