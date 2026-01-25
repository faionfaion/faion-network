# Skills Directory

Claude Code skills for the faion-network framework.

## Entry Point

**`/faion-net`** - Universal orchestrator for all software projects.

This is the **ONLY skill you need to invoke directly**. It automatically selects and coordinates all domain skills based on your task.

```
/faion-net  →  Analyzes task  →  Selects appropriate skill(s)  →  Executes
```

## Active Skills (54)

### Core Orchestrators

| Skill | Description |
|-------|-------------|
| **faion-net** | Universal orchestrator |
| **faion-sdd** | SDD workflow |
| **faion-feature-executor** | Sequential task execution |

### Development

| Skill | Methodologies | Focus |
|-------|---------------|-------|
| faion-software-developer | - | Development routing |
| faion-software-architect | 33 | System design, ADRs |
| faion-python-developer | 29 | Django, FastAPI |
| faion-javascript-developer | 25 | React, Node.js, Next.js |
| faion-backend-developer | - | Backend routing |
| faion-backend-systems | 22 | Go, Rust, databases |
| faion-backend-enterprise | 25 | Java, C#, PHP, Ruby |
| faion-frontend-developer | 30 | Tailwind, UI, PWA |
| faion-api-developer | 22 | REST, GraphQL |
| faion-testing-developer | 25 | TDD, mocking |
| faion-devtools-developer | - | DevTools routing |
| faion-code-quality | 23 | Code review, DDD |
| faion-automation-tooling | 23 | Puppeteer, CI/CD |

### DevOps & Infrastructure

| Skill | Methodologies | Focus |
|-------|---------------|-------|
| faion-devops-engineer | - | DevOps routing |
| faion-infrastructure-engineer | 23 | Docker, K8s, Terraform |
| faion-cicd-engineer | 18 | GitHub Actions, GitOps |

### ML/AI

| Skill | Methodologies | Focus |
|-------|---------------|-------|
| faion-ml-engineer | - | ML routing |
| faion-llm-integration | 20 | OpenAI, Claude, Gemini |
| faion-rag-engineer | 18 | Embeddings, vector DBs |
| faion-ml-ops | 15 | Fine-tuning, evaluation |
| faion-ai-agents | 15 | LangChain, MCP |
| faion-multimodal-ai | 12 | Vision, speech, voice |

### Marketing

| Skill | Methodologies | Focus |
|-------|---------------|-------|
| faion-marketing-manager | - | Marketing routing |
| faion-gtm-strategist | 28 | Launches, positioning |
| faion-content-marketer | 16 | SEO, email, social |
| faion-growth-marketer | 32 | Experiments, AARRR |
| faion-conversion-optimizer | 13 | CRO, funnels, PLG |
| faion-seo-manager | 15 | On-page, technical SEO |
| faion-ppc-manager | 12 | Google, Meta ads |
| faion-smm-manager | 10 | Social media |

### Product & Project

| Skill | Methodologies | Focus |
|-------|---------------|-------|
| faion-product-manager | - | Product routing |
| faion-product-planning | 17 | MVP, roadmaps, OKRs |
| faion-product-operations | 16 | Prioritization, backlog |
| faion-project-manager | - | PM routing |
| faion-pm-agile | 28 | Scrum, Kanban, tools |
| faion-pm-traditional | 22 | PMBoK, EVM, WBS |

### Business Analysis

| Skill | Methodologies | Focus |
|-------|---------------|-------|
| faion-business-analyst | - | BA routing |
| faion-ba-core | 21 | Requirements, strategy |
| faion-ba-modeling | 7 | Use cases, BPMN |

### UX/UI Design

| Skill | Methodologies | Focus |
|-------|---------------|-------|
| faion-ux-ui-designer | - | UX/UI routing |
| faion-ux-researcher | 30 | User interviews, testing |
| faion-ui-designer | 30 | Wireframes, tokens |
| faion-accessibility-specialist | 15 | WCAG, a11y |
| faion-user-researcher | 12 | Personas, JTBD |

### Research & Communication

| Skill | Methodologies | Focus |
|-------|---------------|-------|
| faion-researcher | - | Research routing |
| faion-market-researcher | 18 | TAM, competitors |
| faion-communicator | 14 | Stakeholder dialogue |
| faion-hr-recruiter | 15 | Talent, onboarding |
| faion-claude-code | 9 | Claude Code config |

## Task Routing

| Task Type | Domain Skill |
|-----------|--------------|
| Research, market analysis | faion-researcher |
| Architecture, system design | faion-software-architect |
| Product planning, MVP/MLP | faion-product-manager |
| Writing code, APIs | faion-software-developer |
| Infrastructure, CI/CD | faion-devops-engineer |
| AI/ML, LLM APIs, RAG | faion-ml-engineer |
| Marketing, GTM, SEO | faion-marketing-manager |
| UX/UI, usability | faion-ux-ui-designer |
| Project management | faion-project-manager |
| Business analysis | faion-business-analyst |
| Communication | faion-communicator |
| HR, recruiting | faion-hr-recruiter |
| SDD workflow | faion-sdd |
| Claude Code setup | faion-claude-code |

## Statistics

| Metric | Count |
|--------|-------|
| Total Skills | 54 |
| Routing Skills | 12 |
| Methodologies | 605+ |

## User-Invocable Skills

**Only `/faion-net` is user-invocable.** All other skills are marked as `user-invocable: false` in their frontmatter.

All domain skills include this reference:

> **Entry point:** `/faion-net` — invoke for automatic routing.

## Naming Conventions

- **Skills**: `faion-{domain}` (e.g., faion-software-developer)
- **Methodologies**: Semantic naming `{name}.md` (e.g., gtm-strategy.md)
- **Agent**: `faion-task-YOLO-executor-opus-agent`

## Related

- Main skill: [faion-net/CLAUDE.md](faion-net/CLAUDE.md)
- Decision trees: [faion-net/decision-trees.md](faion-net/decision-trees.md)
- Methodologies: [faion-net/methodologies-catalog.md](faion-net/methodologies-catalog.md)
- Agent: `~/.claude/agents/faion-task-YOLO-executor-opus-agent.md`
