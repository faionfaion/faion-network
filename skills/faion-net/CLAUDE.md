# Faion Network Orchestrator Skill

**Entry Point:** `/faion-net`

Universal orchestrator for end-to-end software project lifecycle. From idea to production, from research to marketing.

<<<<<<< HEAD
## Key Statistics
=======
## How It Works

```
/faion-net  →  Analyzes task  →  Selects skill(s)  →  Routes  →  Executes
```

## Statistics
>>>>>>> claude

| Metric | Count |
|--------|-------|
| Domain Skills | 18 |
| Agents | 60+ |
<<<<<<< HEAD
| Methodologies | 502 |
=======
| Methodologies | 605 |
>>>>>>> claude

## Skill Routing

<<<<<<< HEAD
```
faion-net/
├── SKILL.md                    # Main skill definition
├── CLAUDE.md                   # This file (navigation)
├── decision-trees.md           # Skill & methodology selection
├── methodologies-catalog.md    # Full 502 methodologies catalog
├── workflow.md                 # SDD workflow phases
├── directory-structure.md      # SDD folder layout
├── quality-assurance.md        # Confidence checks, reflexion
├── ref-CLAUDE.md               # Extended references (from references/)
└── *-domain.md                 # Domain-specific references (10 files)
```

## Key Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Execution modes, capabilities, domain skills list |
| `decision-trees.md` | **Decision trees for skill and methodology selection** |
| `methodologies-catalog.md` | Complete 502 methodologies by category |
| `*-domain.md` | Domain-specific agents, skills, methodologies |
=======
| User Intent | Domain Skill |
|-------------|--------------|
| Research, market, competitors | [faion-researcher](../faion-researcher/CLAUDE.md) |
| Architecture, system design | [faion-software-architect](../faion-software-architect/CLAUDE.md) |
| Product planning, roadmaps | [faion-product-manager](../faion-product-manager/CLAUDE.md) |
| Writing code, APIs | [faion-software-developer](../faion-software-developer/CLAUDE.md) |
| Infrastructure, CI/CD | [faion-devops-engineer](../faion-devops-engineer/CLAUDE.md) |
| AI/ML, LLM APIs | [faion-ml-engineer](../faion-ml-engineer/CLAUDE.md) |
| Marketing, GTM, SEO | [faion-marketing-manager](../faion-marketing-manager/CLAUDE.md) |
| UX/UI, usability | [faion-ux-ui-designer](../faion-ux-ui-designer/CLAUDE.md) |
| Project management | [faion-project-manager](../faion-project-manager/CLAUDE.md) |
| Business analysis | [faion-business-analyst](../faion-business-analyst/CLAUDE.md) |
| Communication | [faion-communicator](../faion-communicator/CLAUDE.md) |
| HR, recruiting | [faion-hr-recruiter](../faion-hr-recruiter/CLAUDE.md) |
| SDD workflow | [faion-sdd](../faion-sdd/CLAUDE.md) |
| Claude Code setup | [faion-claude-code](../faion-claude-code/CLAUDE.md) |
| Sequential execution | [faion-feature-executor](../faion-feature-executor/CLAUDE.md) |

## Files

| File | Purpose |
|------|---------|
| [SKILL.md](SKILL.md) | Decision tree + execution modes |
| [methodologies-catalog.md](methodologies-catalog.md) | All 605 methodologies overview |
| [methodologies-product.md](methodologies-product.md) | Product, research, PM, BA, UX (175) |
| [methodologies-dev.md](methodologies-dev.md) | Dev, DevOps, ML/AI, architecture (146) |
| [methodologies-marketing.md](methodologies-marketing.md) | Marketing, growth, ads (82) |
| [workflow.md](workflow.md) | SDD phases and lifecycle |
| [*-domain.md](*.md) | Domain-specific references (10 files) |
>>>>>>> claude

## Execution Modes

| Mode | Agent/Skill | When to Use |
|------|-------------|-------------|
<<<<<<< HEAD
| YOLO (Autonomous) | faion-task-YOLO-executor-opus-agent | Clear tasks, SDD specs exist |
| Interactive | faion-communicator | Vague requirements, user prefers control |

## Skill Selection (Quick)

See [Decision Trees](decision-trees.md) for full guidance.

```
User Intent                         → Skill
─────────────────────────────────────────────
Research/Discovery                  → faion-researcher
Architecture/Design                 → faion-software-architect
Product Planning                    → faion-product-manager
Writing Code                        → faion-software-developer
Infrastructure                      → faion-devops-engineer
AI/ML/LLM                          → faion-ml-engineer
Marketing                          → faion-marketing-manager
UX/UI                              → faion-ux-ui-designer
Project Management                  → faion-project-manager
Business Analysis                   → faion-business-analyst
Communication                       → faion-communicator
HR/Recruiting                       → faion-hr-recruiter
SDD Workflow                        → faion-sdd
Claude Code Setup                   → faion-claude-code
```

## Domain Skills (15)

| Skill | Purpose | Methodologies |
|-------|---------|---------------|
| faion-sdd | Specs, designs, implementation plans, task lifecycle | 17 |
| faion-feature-executor | Sequential tasks with quality gates | - |
| faion-researcher | Market research, competitors, personas | 32 |
| faion-product-manager | MVP/MLP, RICE/MoSCoW, roadmaps | 33 |
| faion-software-developer | Python, JS/TS, APIs, DevOps | 111 |
| faion-devops-engineer | Docker, K8s, Terraform, CI/CD | 26 |
| faion-ml-engineer | LLM APIs, RAG, embeddings, fine-tuning | 42 |
| faion-marketing-manager | GTM, landing pages, SEO | 86 |
| faion-project-manager | PMBok 7/8, risk, EVM | 46 |
| faion-business-analyst | BABOK, 6 Knowledge Areas | 24 |
| faion-ux-ui-designer | Nielsen's 10 Heuristics, usability | 75 |
| faion-communicator | Mom Test, conflict resolution, feedback | 10 |
| faion-hr-recruiter | Talent acquisition, employer branding | 5 |
| faion-claude-code | Skills, agents, commands, MCP servers | - |
| faion-software-architect | System design, patterns, ADRs | TBD |

## Methodology Categories

Full catalog: [methodologies-catalog.md](methodologies-catalog.md)

| Category | Count |
|----------|-------|
| Development | 68 |
| ML/AI | 30 |
| Marketing + Growth + Ads | 68 |
| UX/UI | 32 |
| PM + BA | 44 |
| Research | 14 |
| Product | 18 |
| DevOps | 20 |
| SDD | 12 |
| Communication | 10 |
| HR | 45 |

## References

- [Decision Trees](decision-trees.md) - Skill and methodology selection
- [Methodologies Catalog](methodologies-catalog.md) - All 502 methodologies
- [Workflow](workflow.md) - SDD phases
- [Quality Assurance](quality-assurance.md) - Confidence checks

---

*Faion Network v2.1*
=======
| **YOLO** (Autonomous) | faion-task-YOLO-executor-opus-agent | Clear tasks, specs exist |
| **Interactive** | faion-communicator | Vague requirements, user wants control |

## Quick Start

1. **Invoke:** `/faion-net`
2. **Describe task:** "Help me research competitors for my SaaS product"
3. **Orchestrator routes:** → faion-researcher
4. **Execution:** Full research with 32 methodologies

---

*Faion Network v2.2*
>>>>>>> claude
