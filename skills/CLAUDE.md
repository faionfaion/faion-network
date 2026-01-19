# Skills Directory

Claude Code skills for the faion-network framework.

## Active Skills (14)

### Orchestrators

| Skill | Description | Methodologies |
|-------|-------------|---------------|
| **faion-net** | Universal orchestrator for all software projects | 60+ agents, 40+ skills |
| **faion-sdd** | Specification-Driven Development workflow | M-SDD-001 to M-SDD-017 |
| **faion-feature-executor** | Sequential task execution with quality gates | Uses faion-task-executor-agent |

### Domain Skills

| Skill | Domain | Key Areas |
|-------|--------|-----------|
| **faion-software-developer** | Development | Python, JS/TS, backend, APIs, testing, UI design |
| **faion-devops-engineer** | DevOps | Docker, K8s, Terraform, CI/CD, monitoring |
| **faion-ml-engineer** | ML/AI | LLM APIs, RAG, embeddings, vector DBs |
| **faion-business-analyst** | BA | BABOK v3, requirements, stakeholder analysis |
| **faion-product-manager** | Product | MVP/MLP, roadmaps, OKRs, prioritization |
| **faion-project-manager** | PM | PMBOK 7/8, agile, risk management |
| **faion-marketing-manager** | Marketing | GTM, SEO, ads, content, email |
| **faion-ux-ui-designer** | UX/UI | Nielsen heuristics, accessibility, prototyping |
| **faion-researcher** | Research | Market research, competitors, validation |
| **faion-communicator** | Communication | Active listening, Mom Test, conflict resolution, SPIN |
| **faion-claude-code** | Claude Code | Skills, agents, hooks, MCP, IDE integration |

## Subfolders

### Active Skill Folders
Each active skill folder contains:
- `SKILL.md` - Main skill documentation
- `CLAUDE.md` - Navigation and summary
- `methodologies/` - Methodology files (M-XXX-NNN)
- `references/` - Reference materials and best practices

### Archive Folders
| Folder | Description |
|--------|-------------|
| `_archived/` | 50 legacy skills consolidated into domain orchestrators |
| `archive/` | 5 older development skills |

## Architecture

```
skills/
├── CLAUDE.md                     # This file
├── faion-net/                    # Universal orchestrator
├── faion-sdd/                    # SDD workflow
├── faion-feature-executor/       # Task executor
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
├── faion-claude-code/            # Claude Code config
├── _archived/                    # 50 legacy skills
└── archive/                      # 5 older skills
```

## Naming Conventions

- **Skills**: `faion-{domain}` (e.g., faion-software-developer)
- **Methodologies**: `M-{DOMAIN}-{NNN}` (e.g., M-DEV-001)
- **Agents**: `faion-{function}-agent` (e.g., faion-task-executor-agent)

## Usage

Invoke skills via slash commands:
```
/faion-net           # Universal orchestrator
/faion-sdd           # SDD workflow
/faion-software-developer  # Development tasks
```

## Related

- Agents: `~/.claude/agents/`
- Documentation: `~/.claude/docs/`
- Memory: `~/.sdd/memory/`
