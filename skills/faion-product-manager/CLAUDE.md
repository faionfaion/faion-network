# Product Manager Skill

## Overview

Product management domain skill for MVP/MLP planning, feature prioritization, roadmaps, backlog management, and product lifecycle orchestration. Combines MLP planning and project bootstrap capabilities into a comprehensive product development framework.

**Skill ID:** faion-product-manager
**Methodologies:** 18 core + 15 best practices (33 total)
**Agents:** 2 (faion-mvp-scope-analyzer-agent, faion-mlp-agent)

## Key Capabilities

| Area | Description |
|------|-------------|
| MVP/MLP Planning | Scope MVPs, transform to MLP with delight features |
| Feature Prioritization | RICE and MoSCoW frameworks for objective decisions |
| Roadmap Design | Now-Next-Later, outcome-based, timeline roadmaps |
| Backlog Management | DEEP/INVEST principles, grooming, health checks |
| Product Discovery | Validate assumptions before building |
| Product Launch | Coordinated launch planning and execution |
| Lifecycle Management | Stage-appropriate strategies (intro/growth/maturity/decline) |

## Workflows

### Project Bootstrap Pipeline

```
IDEA -> CONCEPT -> TECH STACK -> MVP SCOPE -> CONFIRMATION -> BACKLOG -> CONSTITUTION -> TASK_000
```

Output structure:
```
aidocs/sdd/{project}/
  constitution.md
  roadmap.md
  features/
    backlog/{NN}-{feature}/spec.md
    00-setup/tasks/todo/TASK_000_project_setup.md
```

### MLP Transformation

```
1. Analyze MVP scope (competitors)
2. Extract current state from specs
3. Find MLP gaps
4. Propose WOW features
5. Update specs with MLP requirements
6. Create implementation order
```

## Folder Structure

| Folder | Content |
|--------|---------|
| [methodologies/](methodologies/) | 18 detailed methodology files (M-PRD-001 to M-PRD-018) |
| [references/](references/) | Best practices and advanced frameworks for 2026 |

## Key Files

| File | Description |
|------|-------------|
| SKILL.md | Main skill definition with agents, workflows, methodology summaries |
| methodologies/M-PRD-001_mvp_scoping.md | MVP scope framework with templates |
| methodologies/M-PRD-002_mlp_planning.md | MLP transformation from MVP |
| methodologies/M-PRD-003_feature_prioritization_rice.md | RICE scoring framework |
| methodologies/M-PRD-005_roadmap_design.md | Roadmap types and templates |
| references/best-practices-2026.md | 15 advanced methodologies (M-PRD-019 to M-PRD-033) |

## Agents

| Agent | Purpose |
|-------|---------|
| faion-mvp-scope-analyzer-agent | MVP scope via competitor analysis |
| faion-mlp-agent | MLP orchestrator with modes: analyze, find-gaps, propose, update, plan |

## Numbering Convention

| Type | Pattern | Example |
|------|---------|---------|
| Features | `{NN}-{name}` | `01-auth`, `02-payments` |
| Tasks | `TASK_{NNN}_*` | `TASK_001_setup` |
| Requirements | `FR-{NN}.{N}` | `FR-01.1` |
| Acceptance | `AC-{NN}.{N}` | `AC-01.1` |

## Related Skills

| Skill | Relationship |
|-------|-------------|
| faion-research-domain-skill | Provides market data for product decisions |
| faion-pm-domain-skill | Provides project management standards |
| faion-ba-domain-skill | Provides business analysis standards |
| faion-sdd-domain-skill | Uses product decisions for specifications |
