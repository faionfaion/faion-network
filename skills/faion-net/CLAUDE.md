# Faion Network Orchestrator Skill

**Entry Point:** `/faion-net`

Universal orchestrator for end-to-end software project lifecycle. From idea to production, from research to marketing.

## How It Works

```
/faion-net  →  Analyzes task  →  Selects skill(s)  →  Routes  →  Executes
```

## Statistics

| Metric | Count |
|--------|-------|
| Domain Skills | 18 |
| Agents | 60+ |
| Methodologies | 605 |

## Skill Routing

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

## Execution Modes

| Mode | Agent/Skill | When to Use |
|------|-------------|-------------|
| **YOLO** (Autonomous) | faion-task-YOLO-executor-opus-agent | Clear tasks, specs exist |
| **Interactive** | faion-communicator | Vague requirements, user wants control |

## Quick Start

1. **Invoke:** `/faion-net`
2. **Describe task:** "Help me research competitors for my SaaS product"
3. **Orchestrator routes:** → faion-researcher
4. **Execution:** Full research with 32 methodologies

---

*Faion Network v2.2*
