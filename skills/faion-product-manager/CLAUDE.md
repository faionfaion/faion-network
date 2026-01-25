# Product Manager Skill

> **Entry Point:** Invoked via [/faion-net](../faion-net/CLAUDE.md) or directly as `/faion-product-manager`

## When to Use

- Defining MVP/MLP scope
- Feature prioritization (RICE, MoSCoW)
- Creating product roadmaps
- Backlog management and grooming
- Product discovery and validation
- OKRs and product metrics
- Product launch planning
- Lifecycle management (intro/growth/maturity/decline)

## Overview

Product management for MVP/MLP planning, feature prioritization, roadmaps, backlog management, and product lifecycle orchestration.

**Methodologies:** 33 | **Agents:** 2

## Key Capabilities

| Area | Description |
|------|-------------|
| MVP/MLP Planning | Scope MVPs, transform to MLP with delight features |
| Feature Prioritization | RICE and MoSCoW frameworks |
| Roadmap Design | Now-Next-Later, outcome-based, timeline roadmaps |
| Backlog Management | DEEP/INVEST principles, grooming |
| Product Discovery | Validate assumptions before building |
| Product Launch | Coordinated launch planning |
| Lifecycle Management | Stage-appropriate strategies |

## Workflows

### Project Bootstrap Pipeline

```
<<<<<<< HEAD
IDEA -> CONCEPT -> TECH STACK -> MVP SCOPE -> CONFIRMATION -> BACKLOG -> CONSTITUTION -> TASK_000
```

Output structure:
```
.aidocs/
  constitution.md
  roadmap.md
  features/
    backlog/{NN}-{feature}/spec.md
    00-setup/tasks/todo/TASK_000_project_setup.md
=======
IDEA → CONCEPT → TECH STACK → MVP SCOPE → CONFIRMATION → BACKLOG → CONSTITUTION → TASK_000
>>>>>>> claude
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

<<<<<<< HEAD
## File Structure

All methodologies and references are in the skill root folder (flat structure):

| Prefix | Content |
|--------|---------|
| (none) | 18 core methodology files (mvp-scoping.md, mlp-planning.md, etc.) |
| meth-* | 15 methodology files (prefixed to avoid conflicts) |
| ref-* | 15 reference files (best practices and advanced frameworks for 2026) |

## Key Files

| File | Description |
|------|-------------|
| SKILL.md | Main skill definition with agents, workflows, methodology summaries |
| mvp-scoping.md | MVP scope framework with templates |
| mlp-planning.md | MLP transformation from MVP |
| feature-prioritization-rice.md | RICE scoring framework |
| roadmap-design.md | Roadmap types and templates |
| meth-continuous-discovery.md | Continuous Discovery Habits framework |

=======
>>>>>>> claude
## Agents

| Agent | Purpose |
|-------|---------|
| faion-mvp-scope-analyzer-agent | MVP scope via competitor analysis |
| faion-mlp-agent | MLP orchestrator (analyze, find-gaps, propose, update, plan) |

## Files

| File | Purpose |
|------|---------|
| [SKILL.md](SKILL.md) | Main skill with workflows, decision tree |
| [mvp-scoping.md](mvp-scoping.md) | MVP scope framework |
| [mlp-planning.md](mlp-planning.md) | MLP transformation framework |
| [feature-prioritization-rice.md](feature-prioritization-rice.md) | RICE scoring |
| [roadmap-design.md](roadmap-design.md) | Roadmap types and templates |

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [faion-net](../faion-net/CLAUDE.md) | Parent orchestrator |
| [faion-researcher](../faion-researcher/CLAUDE.md) | Market data for decisions |
| [faion-project-manager](../faion-project-manager/CLAUDE.md) | Manages execution |
| [faion-business-analyst](../faion-business-analyst/CLAUDE.md) | Requirements analysis |
| [faion-sdd](../faion-sdd/CLAUDE.md) | Transforms decisions into specs |
| [faion-marketing-manager](../faion-marketing-manager/CLAUDE.md) | GTM for launches |
