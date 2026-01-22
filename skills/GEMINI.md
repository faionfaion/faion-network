# Skills Directory

Claude Code skills for the faion-network framework.

## Active Skills (16)

### Orchestrators

| Skill | Description | Methodologies |
|-------|-------------|---------------|
| **faion-net** | Universal orchestrator for all software projects | 502 methodologies |
| **faion-sdd** | Specification-Driven Development workflow | 17 methodologies |
| **faion-feature-executor** | Sequential task execution with quality gates | - |

### Domain Skills

| Skill | Domain | Key Areas |
|-------|--------|-----------|
| **faion-software-architect** | Architecture | System design, ADRs, patterns, quality attributes |
| **faion-software-developer** | Development | Python, JS/TS, backend, APIs, testing, UI design |
| **faion-devops-engineer** | DevOps | Docker, K8s, Terraform, CI/CD, monitoring |
| **faion-ml-engineer** | ML/AI | LLM APIs, RAG, embeddings, vector DBs |
| **faion-business-analyst** | BA | Business Analysis Framework, requirements, stakeholder analysis |
| **faion-product-manager** | Product | MVP/MLP, roadmaps, OKRs, prioritization |
| **faion-project-manager** | PM | Project Management Framework 7/8, agile, risk management |
| **faion-marketing-manager** | Marketing | GTM, SEO, ads, content, email |
| **faion-ux-ui-designer** | UX/UI | 10 Usability Heuristics, accessibility, prototyping |
| **faion-researcher** | Research | Market research, competitors, validation |
| **faion-communicator** | Communication | Active listening, Mom Test, conflict resolution, SPIN |
| **faion-hr-recruiter** | HR/Recruiting | Talent acquisition, employer branding, interviewing, onboarding |
| **faion-claude-code** | Claude Code | Skills, agents, hooks, MCP, IDE integration |

## Subfolders

Each skill folder contains:
- `SKILL.md` - Main skill documentation
- `CLAUDE.md` - Navigation and summary
- `methodologies/` or `references/` - Methodology files (semantic names)
- `references/` - Reference materials and best practices

## Architecture

```
skills/
├── CLAUDE.md                     # This file
├── faion-net/                    # Universal orchestrator
├── faion-sdd/                    # SDD workflow
├── faion-feature-executor/       # Task executor
├── faion-software-architect/     # Architecture (NEW)
├── faion-software-developer/     # Development
├── faion-devops-engineer/        # DevOps
├── faion-ml-engineer/            # ML/AI
├── faion-business-analyst/       # Business Analysis
├── faion-product-manager/        # Product Management
├── faion-project-manager/        # Project Management
├── faion-marketing-manager/      # Marketing
├── faion-ux-ui-designer/         # UX/UI Design
├── faion-researcher/             # Research
├── faion-communicator/           # Communication & Stakeholder Dialogue
├── faion-hr-recruiter/           # HR & Recruiting
└── faion-claude-code/            # Claude Code config
```

## Naming Conventions

- **Skills**: `faion-{domain}` (e.g., faion-software-developer)
- **Methodologies**: Semantic naming `{name}.md` (e.g., gtm-strategy.md, prompt-engineering.md)
- **Agent**: `faion-task-executor-YOLO-agent`

**Note:** All skills now use semantic naming for methodologies.

## Usage

Invoke skills via slash commands:
```
/faion-net           # Universal orchestrator
/faion-sdd           # SDD workflow
/faion-software-developer  # Development tasks
```

## Related

- Agent: `~/.claude/agents/faion-task-executor-YOLO-agent.md`
- Documentation: `~/.claude/docs/`
- Memory: `~/.sdd/memory/`
