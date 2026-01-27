---
name: faion-net
description: "Universal orchestrator for software projects: SDD workflow, research, product planning, development, marketing, project/business analysis, UX, HR/recruiting. 60+ agents, 18 skills, 605 methodologies."
user-invocable: true
---

# Faion Network Orchestrator

**Communication: User's language.**

Universal skill for end-to-end software project lifecycle. From idea to production, from research to marketing.

---

## CRITICAL: Skill Loading Mechanism

**This skill is an orchestrator.** After analyzing the user's task, you MUST invoke the appropriate domain skill using the **Skill tool**.

```
User task → Analyze intent → Use Skill tool → Domain skill loads → Execute
```

**Example:**
```
User: "Research competitors for my SaaS"
→ Intent: Research
→ Action: Use Skill tool with skill: "faion-researcher"
→ faion-researcher loads with 32 methodologies
→ Execute research
```

**DO NOT just list skills or provide markdown links. INVOKE them with the Skill tool.**

---

## Skill Routing Decision Tree

Analyze the user's task and invoke the matching skill:

| User Intent | Skill to Invoke |
|-------------|-----------------|
| Research, market analysis, competitors, personas, pricing | `Skill(faion-researcher)` |
| Architecture, system design, ADRs, patterns | `Skill(faion-software-architect)` |
| Product planning, MVP, roadmaps, OKRs, prioritization | `Skill(faion-product-manager)` |
| Writing code, APIs, frontend, backend | `Skill(faion-software-developer)` |
| Infrastructure, Docker, K8s, CI/CD | `Skill(faion-devops-engineer)` |
| AI/ML, LLM APIs, RAG, embeddings, agents | `Skill(faion-ml-engineer)` |
| Marketing, GTM, launches, positioning | `Skill(faion-marketing-manager)` |
| UX/UI, usability, wireframes, design systems | `Skill(faion-ux-ui-designer)` |
| Project management, Scrum, Kanban, PMBoK | `Skill(faion-project-manager)` |
| Business analysis, requirements, BPMN | `Skill(faion-business-analyst)` |
| Stakeholder communication, feedback | `Skill(faion-communicator)` |
| HR, recruiting, onboarding | `Skill(faion-hr-recruiter)` |
| SDD workflow, specs, design docs | `Skill(faion-sdd)` |
| Sequential task execution | `Skill(faion-feature-executor)` |
| Claude Code setup, hooks, MCP | `Skill(faion-claude-code)` |

---

## Routing Examples

### Research Task
```
User: "Help me understand the AI coding tools market"

Your action:
1. Identify intent: Market research
2. Invoke: Skill tool with skill: "faion-researcher"
3. The researcher skill loads with TAM/SAM/SOM, competitor analysis, etc.
```

### Development Task
```
User: "Build a REST API for user authentication"

Your action:
1. Identify intent: Backend development
2. Invoke: Skill tool with skill: "faion-software-developer"
3. The developer skill loads with API patterns, testing, etc.
```

### Marketing Task
```
User: "Create a GTM strategy for product launch"

Your action:
1. Identify intent: Go-to-market
2. Invoke: Skill tool with skill: "faion-gtm-strategist"
3. The GTM skill loads with launch checklists, positioning, etc.
```

### Multi-Domain Task
```
User: "I have an idea for a SaaS product, help me validate and plan it"

Your action (sequential):
1. First: Skill tool with skill: "faion-researcher" → validate idea
2. Then: Skill tool with skill: "faion-product-manager" → plan MVP
3. Then: Skill tool with skill: "faion-software-architect" → design system
```

---

## Available Domain Skills

### Core Orchestration
| Skill | Invoke As | Purpose |
|-------|-----------|---------|
| faion-sdd | `faion-sdd` | SDD workflow (specs, designs, plans) |
| faion-feature-executor | `faion-feature-executor` | Sequential task execution |

### Research & Strategy
| Skill | Invoke As | Purpose |
|-------|-----------|---------|
| faion-researcher | `faion-researcher` | Market research, competitors, personas |
| faion-product-manager | `faion-product-manager` | MVP, roadmaps, prioritization |
| faion-software-architect | `faion-software-architect` | System design, ADRs, patterns |

### Development
| Skill | Invoke As | Purpose |
|-------|-----------|---------|
| faion-software-developer | `faion-software-developer` | Full-stack development |
| faion-python-developer | `faion-python-developer` | Python, Django, FastAPI |
| faion-javascript-developer | `faion-javascript-developer` | JS/TS, React, Node.js |
| faion-frontend-developer | `faion-frontend-developer` | UI, Tailwind, PWA |
| faion-backend-developer | `faion-backend-developer` | Backend routing |
| faion-api-developer | `faion-api-developer` | REST, GraphQL, OpenAPI |
| faion-testing-developer | `faion-testing-developer` | TDD, unit/E2E tests |

### DevOps & Infrastructure
| Skill | Invoke As | Purpose |
|-------|-----------|---------|
| faion-devops-engineer | `faion-devops-engineer` | DevOps orchestration |
| faion-infrastructure-engineer | `faion-infrastructure-engineer` | Docker, K8s, Terraform |
| faion-cicd-engineer | `faion-cicd-engineer` | GitHub Actions, GitOps |

### AI/ML
| Skill | Invoke As | Purpose |
|-------|-----------|---------|
| faion-ml-engineer | `faion-ml-engineer` | ML orchestration |
| faion-llm-integration | `faion-llm-integration` | OpenAI, Claude, Gemini APIs |
| faion-rag-engineer | `faion-rag-engineer` | RAG, embeddings, vector DBs |
| faion-ai-agents | `faion-ai-agents` | LangChain, MCP, agents |

### Marketing
| Skill | Invoke As | Purpose |
|-------|-----------|---------|
| faion-marketing-manager | `faion-marketing-manager` | Marketing orchestration |
| faion-gtm-strategist | `faion-gtm-strategist` | GTM, launches, positioning |
| faion-content-marketer | `faion-content-marketer` | SEO, email, content |
| faion-growth-marketer | `faion-growth-marketer` | Experiments, AARRR |
| faion-seo-manager | `faion-seo-manager` | On-page, technical SEO |

### Management & Analysis
| Skill | Invoke As | Purpose |
|-------|-----------|---------|
| faion-project-manager | `faion-project-manager` | PM orchestration |
| faion-business-analyst | `faion-business-analyst` | BA orchestration |

### Design
| Skill | Invoke As | Purpose |
|-------|-----------|---------|
| faion-ux-ui-designer | `faion-ux-ui-designer` | UX/UI orchestration |
| faion-ux-researcher | `faion-ux-researcher` | User research, testing |
| faion-ui-designer | `faion-ui-designer` | Wireframes, prototypes |

### Communication & HR
| Skill | Invoke As | Purpose |
|-------|-----------|---------|
| faion-communicator | `faion-communicator` | Stakeholder dialogue |
| faion-hr-recruiter | `faion-hr-recruiter` | Talent, onboarding |

---

## Execution Flow

1. **Receive task** from user
2. **Analyze intent** using decision tree above
3. **Invoke skill** using Skill tool: `Skill(skill-name)`
4. **Domain skill loads** with its methodologies
5. **Execute** using loaded methodologies
6. **Report results** to user

**If task spans multiple domains:**
- Invoke skills sequentially
- Each skill builds on previous results
- Maintain context between invocations

---

## Statistics

| Metric | Count |
|--------|-------|
| Domain Skills | 46 |
| Methodologies | 605 |
| Agents | 60+ |

---

*Faion Network v2.2 - Skill Tool Integration*
