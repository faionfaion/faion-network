# Skills Directory

Claude Code skills for the faion-network framework.

## Active Skills (15)

### Orchestrators

| Skill | Description | Methodologies |
|-------|-------------|---------------|
| **faion-net** | Universal orchestrator for all software projects | 501 methodologies |
| **faion-sdd** | Specification-Driven Development workflow | M-SDD-001 to M-SDD-017 |
| **faion-feature-executor** | Sequential task execution with quality gates | Uses faion-task-executor-YOLO-agent |

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
| **faion-hr-recruiter** | HR/Recruiting | Talent acquisition, employer branding, interviewing, onboarding |
| **faion-claude-code** | Claude Code | Skills, agents, hooks, MCP, IDE integration |

## Subfolders

Each skill folder contains:
- `SKILL.md` - Main skill documentation
- `CLAUDE.md` - Navigation and summary
- `methodologies/` - Methodology files (M-XXX-NNN)
- `references/` - Reference materials and best practices

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
├── faion-hr-recruiter/           # HR & Recruiting
└── faion-claude-code/            # Claude Code config
```

## Naming Conventions

- **Skills**: `faion-{domain}` (e.g., faion-software-developer)
- **Methodologies**:
  - Legacy: `M-{DOMAIN}-{NNN}` (e.g., M-DEV-001)
  - Semantic: `{name}.md` with id `{name}` (e.g., gtm-strategy.md)
- **Agent**: `faion-task-executor-YOLO-agent`

**Note:** faion-marketing-manager and faion-hr-recruiter use semantic naming (77 and 45 methodologies respectively).

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
