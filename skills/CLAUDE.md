# Skills Directory

Claude Code skills for the faion-network framework.

## Entry Point

**`/faion-net`** - Universal orchestrator for all software projects.

This is the **ONLY skill you need to invoke directly**. It automatically selects and coordinates all domain skills based on your task.

```
/faion-net  →  Analyzes task  →  Selects appropriate skill(s)  →  Executes
```

## Active Skills (46)

### Orchestrators

| Skill | Description | Sub-skills |
|-------|-------------|------------|
| **faion-net** | Universal orchestrator | All domain skills |
| **faion-sdd** | SDD workflow | sdd-planning, sdd-execution |
| **faion-feature-executor** | Sequential task execution | - |

### Domain Skills

| Skill | Domain | Methodologies |
|-------|--------|---------------|
| **faion-software-developer** | Development (orchestrator) | 7 sub-skills |
| **faion-software-architect** | Architecture | 33 |
| **faion-devops-engineer** | DevOps (orchestrator) | 2 sub-skills |
| **faion-ml-engineer** | ML/AI (orchestrator) | 5 sub-skills |
| **faion-marketing-manager** | Marketing (orchestrator) | 4 sub-skills |
| **faion-ux-ui-designer** | UX/UI (orchestrator) | 3 sub-skills |
| **faion-product-manager** | Product (orchestrator) | 2 sub-skills |
| **faion-project-manager** | PM (orchestrator) | 2 sub-skills |
| **faion-business-analyst** | BA (orchestrator) | 2 sub-skills |
| **faion-researcher** | Research (orchestrator) | 2 sub-skills |
| **faion-communicator** | Communication | 14 |
| **faion-hr-recruiter** | HR/Recruiting | 15 |
| **faion-claude-code** | Claude Code config | 9 |

## Task Routing

| Task Type | Domain Skill Used |
|-----------|-------------------|
| Research, market analysis, competitors | faion-researcher |
| Architecture, system design, ADRs | faion-software-architect |
| Product planning, MVP/MLP, roadmaps | faion-product-manager |
| Writing code, APIs, testing | faion-software-developer |
| Infrastructure, CI/CD, deployment | faion-devops-engineer |
| AI/ML, LLM APIs, RAG, embeddings | faion-ml-engineer |
| Marketing, GTM, SEO, ads | faion-marketing-manager |
| UX/UI, usability, accessibility | faion-ux-ui-designer |
| Project management, agile | faion-project-manager |
| Business analysis, requirements | faion-business-analyst |
| Stakeholder communication | faion-communicator |
| HR, recruiting, onboarding | faion-hr-recruiter |
| SDD workflow, specs, tasks | faion-sdd |
| Claude Code setup, skills, hooks | faion-claude-code |
| Sequential task execution | faion-feature-executor |

## Statistics

| Metric | Count |
|--------|-------|
| Total Skills | 46 |
| Orchestrators | 11 |
| Sub-skills | 31 |
| Standalone | 4 |
| Methodologies | 605+ |

## How It Works

1. **Invoke** `/faion-net` with your task
2. **faion-net** analyzes intent using decision trees
3. **Routes** to appropriate domain skill(s)
4. **Executes** with full methodology knowledge

## User-Invocable Skills

**Only `/faion-net` is user-invocable.** All other skills are marked as `user-invocable: false` in their frontmatter.

All domain skills automatically include this reference at the top:

> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

This ensures users always go through the orchestrator for optimal routing and coordination.

## Architecture

```
skills/
├── CLAUDE.md                     # This file
├── faion-net/                    # Universal orchestrator
├── faion-sdd/                    # SDD workflow (orchestrator)
│   ├── faion-sdd-planning/       # Specs, design, plans
│   └── faion-sdd-execution/      # Quality gates, review
├── faion-software-developer/     # Development (orchestrator)
│   ├── faion-python-developer/
│   ├── faion-javascript-developer/
│   ├── faion-backend-developer/
│   ├── faion-frontend-developer/
│   ├── faion-api-developer/
│   ├── faion-testing-developer/
│   └── faion-devtools-developer/
├── faion-devops-engineer/        # DevOps (orchestrator)
│   ├── faion-infrastructure-engineer/
│   └── faion-cicd-engineer/
├── faion-ml-engineer/            # ML/AI (orchestrator)
│   ├── faion-llm-integration/
│   ├── faion-rag-engineer/
│   ├── faion-ml-ops/
│   ├── faion-ai-agents/
│   └── faion-multimodal-ai/
├── faion-marketing-manager/      # Marketing (orchestrator)
│   ├── faion-gtm-strategist/
│   ├── faion-content-marketer/
│   ├── faion-growth-marketer/
│   └── faion-conversion-optimizer/
├── faion-ux-ui-designer/         # UX/UI (orchestrator)
│   ├── faion-ux-researcher/
│   ├── faion-ui-designer/
│   └── faion-accessibility-specialist/
├── faion-product-manager/        # Product (orchestrator)
├── faion-project-manager/        # PM (orchestrator)
├── faion-business-analyst/       # BA (orchestrator)
├── faion-researcher/             # Research (orchestrator)
├── faion-software-architect/     # Architecture
├── faion-communicator/           # Communication
├── faion-hr-recruiter/           # HR/Recruiting
├── faion-claude-code/            # Claude Code config
└── faion-feature-executor/       # Task executor
```

## Naming Conventions

- **Skills**: `faion-{domain}` (e.g., faion-software-developer)
- **Sub-skills**: `faion-{domain}:{sub}` or `faion-{subdomain}-{type}`
- **Methodologies**: Semantic naming `{name}.md` (e.g., gtm-strategy.md)
- **Agent**: `faion-task-YOLO-executor-opus-agent`

## Usage

Invoke skills via slash commands:
```
/faion-net                  # Universal orchestrator (recommended)
/faion-sdd                  # SDD workflow
/faion-software-developer   # Development tasks
```

## Related

- Main skill: [faion-net/CLAUDE.md](faion-net/CLAUDE.md)
- Decision trees: [faion-net/decision-trees.md](faion-net/decision-trees.md)
- Methodologies: [faion-net/methodologies-catalog.md](faion-net/methodologies-catalog.md)
- Agent: `~/.claude/agents/faion-task-YOLO-executor-opus-agent.md`
- Memory: `~/.sdd/memory/`
