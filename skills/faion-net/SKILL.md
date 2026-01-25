---
name: faion-net
description: "Universal orchestrator for software projects: SDD workflow, research, product planning, development, marketing, project/business analysis, UX, HR/recruiting. 60+ agents, 18 skills, 605 methodologies."
user-invocable: true
---

# Faion Network Orchestrator

**Communication: User's language.**

Universal skill for end-to-end software project lifecycle. From idea to production, from research to marketing.

---

## Quick Start

**Auto-Flow Protocol:**
1. Knowledge freshness check (model cutoff vs current date)
2. Context discovery (project status + activity type)
3. Skill routing (automatic based on answers)
4. Execution mode selection (YOLO vs Interactive)

**Full protocol:** [session-start-protocol.md](session-start-protocol.md)

---

## Core Components

<<<<<<< HEAD
**Ask user at session start:**

```python
AskUserQuestion([
    {
        "question": "How should I work on tasks?",
        "header": "Mode",
        "options": [
            {"label": "YOLO Mode (Recommended)", "description": "Maximum autonomy. Execute tasks completely without interruptions. Uses faion-task-YOLO-executor-opus-agent."},
            {"label": "Interactive Mode", "description": "Collaborative dialogue. Ask questions, clarify requirements, validate decisions. Stakeholder interview style."}
        ]
    }
])
```
=======
| Component | File | Purpose |
|-----------|------|---------|
| **Session Protocol** | [session-start-protocol.md](session-start-protocol.md) | Auto-flow at session start |
| **Execution Modes** | [execution-modes.md](execution-modes.md) | YOLO (autonomous) vs Interactive |
| **Capabilities** | [capabilities.md](capabilities.md) | Full lifecycle capabilities |
| **Domain Skills** | [domain-skills.md](domain-skills.md) | 18 specialized skills |
| **Skill Selection** | [decision-tree-skills.md](decision-tree-skills.md) | Skill routing logic |
| **Methodologies** | [decision-tree-methodologies.md](decision-tree-methodologies.md) | 605 methodologies selection |
>>>>>>> claude

---

## Execution Modes

<<<<<<< HEAD
**Agent:** `faion-task-YOLO-executor-opus-agent`

**Behavior:**
- Execute tasks completely without asking questions
- Make decisions autonomously using best practices
- Use appropriate methodologies from 494 available
- Document assumptions in code/comments
- Complete tasks or report blockers with details

**When to use:**
- Clear, well-defined tasks
- Tasks with SDD documentation (spec, design)
- User trusts AI judgment
- User wants speed over control

**Execution:**
```python
Task(
    prompt="Execute task: {task_description}",
    subagent_type="faion-task-YOLO-executor-opus-agent"
)
```
=======
| Mode | Agent/Skill | When to Use | Details |
|------|-------------|-------------|---------|
| **YOLO** | faion-task-YOLO-executor-opus-agent | Clear tasks, specs exist | [execution-modes.md](execution-modes.md) |
| **Interactive** | faion-communicator | Vague requirements, user wants control | [execution-modes.md](execution-modes.md) |
>>>>>>> claude

---

## Domain Skills (18)

| Category | Skills | Count |
|----------|--------|-------|
| **Core** | faion-sdd, faion-feature-executor | 2 |
| **Research** | faion-researcher, faion-product-manager, faion-software-architect | 3 |
| **Development** | faion-software-developer, faion-devops-engineer, faion-ml-engineer | 3 |
| **Marketing** | faion-marketing-manager, faion-seo-manager, faion-smm-manager, faion-ppc-manager | 4 |
| **Management** | faion-project-manager, faion-business-analyst | 2 |
| **Design** | faion-ux-ui-designer | 1 |
| **Communication** | faion-communicator, faion-hr-recruiter | 2 |
| **Tools** | faion-claude-code, faion-net | 2 |

**Full catalog:** [domain-skills.md](domain-skills.md)

---

## Capabilities Highlights

| Phase | Capabilities |
|-------|--------------|
| **Idea → Validation** | Idea generation (7 frameworks), pain point research, problem validation, niche evaluation |
| **Research → Strategy** | Market research (TAM/SAM/SOM), competitor analysis, personas, pricing strategies |
| **Product Planning** | MVP/MLP, feature prioritization (RICE, MoSCoW), roadmaps, user story mapping, OKRs |
| **SDD Workflow** | Constitution, specs, design docs, implementation plans, task parallelization, quality gates |
| **Development** | Code gen (8 languages), testing (unit/integration/E2E), API design, DevOps (CI/CD, K8s) |
| **AI/LLM** | RAG pipelines, embeddings, fine-tuning, prompt engineering, multimodal, voice agents |
| **Marketing** | GTM strategy, landing pages, SEO/SEM, paid ads, email campaigns, social media |

**Full list:** [capabilities.md](capabilities.md)

---

## Methodologies Catalog

<<<<<<< HEAD
| Skill | Purpose |
|-------|---------|
| `faion-sdd` | SDD orchestrator: specs, designs, implementation plans, constitutions, task lifecycle, quality gates, reflexion |
| `faion-feature-executor` | SDD feature executor: sequential tasks with quality gates, tests/coverage, code review |
| `faion-researcher` | Idea generation (SCAMPER), market research, competitors, personas, pricing, validation. 20 methodologies |
| `faion-product-manager` | MVP/MLP planning, RICE/MoSCoW prioritization, roadmaps, backlog, user stories, OKRs. 18 methodologies |
| `faion-software-developer` | Python, JS/TS, Django, FastAPI, React, APIs, testing, DevOps, UI design. 111 methodologies |
| `faion-devops-engineer` | Docker, K8s, Terraform, AWS/GCP/Azure, CI/CD, monitoring, IaC, nginx. 20 methodologies |
| `faion-ml-engineer` | LLM APIs, RAG, embeddings, fine-tuning, LangChain, vector DBs, prompt engineering. 30 methodologies |
| `faion-marketing-manager` | GTM, landing pages, SEO/SEM, content, ads, email, social media. 74 methodologies |
| `faion-project-manager` | Project Management Framework 7/8 (8 Domains, 12 Principles), PM tools, risk, EVM, agile. 36 methodologies |
| `faion-business-analyst` | Business Analysis Framework: 6 Knowledge Areas, requirements, stakeholders, process modeling. 30 tasks |
| `faion-ux-ui-designer` | 10 Usability Heuristics, UX research, usability testing, personas, journey mapping. 32 methodologies |
| `faion-communicator` | Stakeholder dialogue, Mom Test, conflict resolution, feedback, selling ideas, storytelling, negotiation. 10 methodologies |
| `faion-claude-code` | Claude Code config: skills, agents, commands, hooks, MCP servers, IDE integrations |
| `faion-net` | This orchestrator (recursive for complex multi-domain tasks) |

---

## Step 3: Skill Selection

Use the [Decision Trees](decision-trees.md) to select the appropriate skill.

### Quick Decision Flowchart

```
User Intent                         → Skill to Invoke
─────────────────────────────────────────────────────
Research/Discovery                  → faion-researcher
Architecture/Design Patterns        → faion-software-architect
Product Planning (MVP, roadmap)     → faion-product-manager
Writing Code                        → faion-software-developer
Infrastructure/Deployment           → faion-devops-engineer
AI/ML/LLM                          → faion-ml-engineer
Marketing/GTM                       → faion-marketing-manager
UX/UI Design                        → faion-ux-ui-designer
Project Management                  → faion-project-manager
Business Analysis                   → faion-business-analyst
Communication/Stakeholders          → faion-communicator
Hiring/HR                          → faion-hr-recruiter
SDD Workflow                        → faion-sdd
Claude Code Setup                   → faion-claude-code
```

### Multi-Skill Orchestration

For complex tasks spanning multiple domains, use orchestration patterns:

| Pattern | When to Use | Example |
|---------|-------------|---------|
| **Sequential** | Tasks have dependencies | Research → Product → Dev → Deploy |
| **Parallel** | Independent tasks | Dev + Marketing + DevOps (launch prep) |
| **Iterative** | Feedback cycles | UX ↔ Dev (design-dev loop) |

See [Decision Trees](decision-trees.md) for detailed guidance.

---

## Methodologies Catalog

**502 methodologies** organized by domain. Full catalog: [methodologies-catalog.md](methodologies-catalog.md)

| Category | Count | Domain Skill |
|----------|-------|--------------|
| Research | 14 | faion-researcher |
| Product | 18 | faion-product-manager |
| Development | 68 | faion-software-developer |
| DevOps | 20 | faion-devops-engineer |
| ML/AI | 30 | faion-ml-engineer |
| Marketing | 40 | faion-marketing-manager |
| Growth | 12 | faion-marketing-manager |
| Advertising | 16 | faion-marketing-manager |
| Business Operations | 14 | faion-marketing-manager |
| Project Management | 32 | faion-project-manager |
| Business Analysis | 12 | faion-business-analyst |
| UX/UI | 32 | faion-ux-ui-designer |
| SDD | 12 | faion-sdd |
| Communication | 10 | faion-communicator |
| HR/Recruiting | 45 | faion-hr-recruiter |
=======
**605 methodologies** organized by domain.

| Category | Count | Domain Skill |
|----------|-------|--------------|
| Development | 135 | faion-software-developer |
| UX/UI | 76 | faion-ux-ui-designer |
| Marketing | 62 | faion-marketing-manager |
| ML/AI | 57 | faion-ml-engineer |
| Project Management | 46 | faion-project-manager |
| Research | 36 | faion-researcher |
| Product | 33 | faion-product-manager |
| DevOps | 32 | faion-devops-engineer |
| Architecture | 28 | faion-software-architect |
| Business Analysis | 26 | faion-business-analyst |
| SDD | 21 | faion-sdd |
| PPC | 19 | faion-ppc-manager |
| Communication | 11 | faion-communicator |
| SEO | 7 | faion-seo-manager |
| SMM | 6 | faion-smm-manager |
| HR/Recruiting | 5 | faion-hr-recruiter |
| Claude Code | 5 | faion-claude-code |

**Full catalog:** [methodologies-catalog.md](methodologies-catalog.md)

---

## Decision Tree: Skill Routing

| If you need... | Use Skill | Key File |
|----------------|-----------|----------|
| Idea generation, market research, competitors, validation | faion-researcher | [research-domain.md](research-domain.md) |
| MVP/MLP scope, roadmap, feature prioritization (RICE/MoSCoW) | faion-product-manager | [product-domain.md](product-domain.md) |
| System design, architecture patterns, ADRs, quality attributes | faion-software-architect | [development-domain.md](development-domain.md) |
| Write code (Python, JS/TS, Go), tests, APIs, refactoring | faion-software-developer | [development-domain.md](development-domain.md) |
| CI/CD, Docker, K8s, Terraform, AWS/GCP/Azure, monitoring | faion-devops-engineer | [development-domain.md](development-domain.md) |
| LLM APIs (OpenAI/Claude/Gemini), RAG, embeddings, fine-tuning | faion-ml-engineer | [ai-llm-domain.md](ai-llm-domain.md) |
| GTM strategy, landing pages, SEO, ads (Google/Meta), email | faion-marketing-manager | [marketing-domain.md](marketing-domain.md) |
| SEO optimization (on-page, off-page, technical) | faion-seo-manager | [marketing-domain.md](marketing-domain.md) |
| Social media management, content strategy, organic growth | faion-smm-manager | [marketing-domain.md](marketing-domain.md) |
| PPC campaigns (Google/Meta), optimization, reporting | faion-ppc-manager | [marketing-domain.md](marketing-domain.md) |
| User research, wireframes, prototypes, usability testing, WCAG | faion-ux-ui-designer | [ux-domain.md](ux-domain.md) |
| PMBOK 7/8, agile, WBS, risk/schedule/cost mgmt, EVM, RACI | faion-project-manager | [pm-domain.md](pm-domain.md) |
| BABOK, requirements (use cases/user stories), process modeling | faion-business-analyst | [ba-domain.md](ba-domain.md) |
| Stakeholder interviews, Mom Test, conflict resolution, feedback | faion-communicator | [pm-domain.md](pm-domain.md) |
| Talent acquisition, interviews (STAR), onboarding, EVP, DEI | faion-hr-recruiter | [pm-domain.md](pm-domain.md) |
| SDD specs, design docs, implementation plans, quality gates | faion-sdd | [sdd-domain.md](sdd-domain.md) |
| Sequential task execution with quality gates, test validation | faion-feature-executor | [sdd-domain.md](sdd-domain.md) |
| Skills, agents, hooks, commands, MCP servers, IDE integration | faion-claude-code | [CLAUDE.md](CLAUDE.md) |

### Multi-Skill Workflows

| Workflow | Sequence | Use Case |
|----------|----------|----------|
| **Full Product Launch** | researcher → product-manager → software-architect → sdd → software-developer → devops-engineer → marketing-manager | New product from idea to market |
| **New Feature (SDD)** | sdd (spec) → sdd (design) → sdd (plan) → feature-executor (tasks) | Structured feature development |
| **Landing Page** | marketing-manager (strategy) + ux-ui-designer (design) → software-developer (impl) | Marketing page creation |
| **AI Feature** | ml-engineer (architecture) → software-developer (integration) → devops-engineer (deploy) | LLM/RAG implementation |
>>>>>>> claude

---

## References

**Core:**
<<<<<<< HEAD
- [Decision Trees](decision-trees.md) - Skill and methodology selection
- [Methodologies Catalog](methodologies-catalog.md) - Full 502 methodologies

**SDD Workflow:**
- [Workflow](workflow.md) - Phases, project/feature selection
- [Directory Structure](directory-structure.md) - SDD folder layout
- [Quality Assurance](quality-assurance.md) - Confidence checks, reflexion

**Domains:**

| Domain | Reference | Skill |
|--------|-----------|-------|
| SDD | [sdd-domain.md](sdd-domain.md) | faion-sdd |
| Research | [research-domain.md](research-domain.md) | faion-researcher |
| Product | [product-domain.md](product-domain.md) | faion-product-manager |
| Development | [development-domain.md](development-domain.md) | faion-software-developer |
| DevOps | [development-domain.md](development-domain.md) | faion-devops-engineer |
| Marketing | [marketing-domain.md](marketing-domain.md) | faion-marketing-manager |
| PM | [pm-domain.md](pm-domain.md) | faion-project-manager |
| BA | [ba-domain.md](ba-domain.md) | faion-business-analyst |
| UX/UI | [ux-domain.md](ux-domain.md) | faion-ux-ui-designer |
| AI/LLM | [ai-llm-domain.md](ai-llm-domain.md) | faion-ml-engineer |
=======
- [CLAUDE.md](CLAUDE.md) - Navigation hub
- [session-start-protocol.md](session-start-protocol.md) - Session auto-flow
- [execution-modes.md](execution-modes.md) - YOLO vs Interactive
- [capabilities.md](capabilities.md) - Full capabilities list
- [domain-skills.md](domain-skills.md) - 18 domain skills catalog

**Methodologies:**
- [methodologies-catalog.md](methodologies-catalog.md) - 605 methodologies overview

**SDD Workflow:**
- [workflow.md](workflow.md) - Phases, project/feature selection
- [directory-structure.md](directory-structure.md) - SDD folder layout
- [quality-assurance.md](quality-assurance.md) - Confidence checks, reflexion

**Domain References:**
- [sdd-domain.md](sdd-domain.md), [research-domain.md](research-domain.md), [product-domain.md](product-domain.md)
- [development-domain.md](development-domain.md), [ba-domain.md](ba-domain.md), [pm-domain.md](pm-domain.md)
- [ux-domain.md](ux-domain.md), [ai-llm-domain.md](ai-llm-domain.md), [marketing-domain.md](marketing-domain.md)
>>>>>>> claude

---

*Faion Network v2.1*
<<<<<<< HEAD
*15 Domain Skills | 502 Methodologies | 60+ Agents*
=======
*18 Domain Skills | 605 Methodologies | 60+ Agents*
>>>>>>> claude
