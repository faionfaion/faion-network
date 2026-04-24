---
name: faion-knowledge
description: "Umbrella knowledge skill: 52 domain knowledge bases across dev, AI, infra, product, PM, BA, UX, marketing, research. 1300+ methodologies."
tier: free
user-invocable: true
---

# Faion Knowledge

**Communication: User's language.**

Single umbrella skill bundling all domain knowledge. No per-domain sub-skills to invoke — all knowledge lives here as markdown, loaded on demand with Read.

## Structure

```
knowledge/
├── dev/           13 skills   Python, JS, Go, Rust, Java, C#, backend, frontend, API, testing, arch, automation, code quality
├── ai/             7 skills   ML engineer, AI agents, RAG, ML ops, multimodal, LLM integration, Claude Code
├── infra/          4 skills   DevOps, CI/CD, infrastructure, server craft
├── product/        3 skills   PM, product planning, product operations
├── pm/             3 skills   Project manager, Agile PM, Traditional PM
├── ba/             3 skills   BA, BA core, BA modeling
├── ux/             5 skills   UX/UI, UI designer, UX researcher, user researcher, accessibility
├── marketing/      8 skills   Marketing, GTM, content, growth, CRO, SEO, PPC, SMM
├── research/       2 skills   Researcher, market researcher
├── comms/          2 skills   Communicator, HR recruiter
└── sdd/            2 skills   SDD, SDD planning
```

Each skill = folder with `SKILL.md` + methodology subfolders. Each methodology = `README.md` + `checklist.md` + `templates.md` + `examples.md` + `llm-prompts.md`.

## How It Works

```
User task → Identify domain → Read knowledge/<group>/<name>/README.md → Apply
```

No `Skill(faion-X)` calls — those sub-skills no longer exist. Load domain content with `Read` or `Grep` against `knowledge/<group>/...`.

## Domain Routing

### Development (`knowledge/dev/`)

| Need | Read |
|------|------|
| Full-stack overview | `dev/software-developer/` |
| System design, ADRs | `dev/software-architect/` |
| Python (Django, FastAPI) | `dev/python-developer/` |
| JS/TS (React, Node, Next.js) | `dev/javascript-developer/` |
| Frontend (Tailwind, PWA, a11y) | `dev/frontend-developer/` |
| APIs (REST, GraphQL, OpenAPI) | `dev/api-developer/` |
| Backend router | `dev/backend-developer/` |
| Go, Rust, DBs, caching | `dev/backend-systems/` |
| Java, C#, PHP, Ruby | `dev/backend-enterprise/` |
| Testing (TDD, E2E, mocking) | `dev/testing-developer/` |
| Code quality, DDD, refactoring | `dev/code-quality/` |
| Puppeteer, monorepo, automation | `dev/automation-tooling/` |
| DevTools overview | `dev/devtools-developer/` |

### AI / ML (`knowledge/ai/`)

| Need | Read |
|------|------|
| ML/AI overview | `ai/ml-engineer/` |
| LLM APIs (OpenAI, Claude, Gemini) | `ai/llm-integration/` |
| RAG, embeddings, vector DBs | `ai/rag-engineer/` |
| Fine-tuning, evals, ML Ops | `ai/ml-ops/` |
| AI agents, LangChain, MCP | `ai/ai-agents/` |
| Vision, image/video, TTS/STT | `ai/multimodal-ai/` |
| Claude Code setup, skills, hooks | `ai/claude-code/` |

### Infrastructure (`knowledge/infra/`)

| Need | Read |
|------|------|
| DevOps overview | `infra/devops-engineer/` |
| Docker, K8s, Terraform, AWS/GCP | `infra/infrastructure-engineer/` |
| CI/CD, GitHub Actions, GitOps | `infra/cicd-engineer/` |
| SSH, nginx, systemd, tuning | `infra/server-craft/` |

### Product (`knowledge/product/`)

| Need | Read |
|------|------|
| Product management overview | `product/product-manager/` |
| MVP, roadmaps, OKRs | `product/product-planning/` |
| Prioritization, backlog, analytics | `product/product-operations/` |

### Project Management (`knowledge/pm/`)

| Need | Read |
|------|------|
| PM overview | `pm/project-manager/` |
| Scrum, Kanban, SAFe | `pm/pm-agile/` |
| PMBoK, EVM, WBS | `pm/pm-traditional/` |

### Business Analysis (`knowledge/ba/`)

| Need | Read |
|------|------|
| BA overview | `ba/business-analyst/` |
| Requirements, elicitation, strategy | `ba/ba-core/` |
| Use cases, BPMN, data models | `ba/ba-modeling/` |

### UX / UI (`knowledge/ux/`)

| Need | Read |
|------|------|
| UX/UI overview | `ux/ux-ui-designer/` |
| Wireframes, design systems | `ux/ui-designer/` |
| User interviews, usability | `ux/ux-researcher/` |
| Personas, JTBD | `ux/user-researcher/` |
| WCAG, a11y | `ux/accessibility-specialist/` |

### Marketing (`knowledge/marketing/`)

| Need | Read |
|------|------|
| Marketing overview | `marketing/marketing-manager/` |
| Launches, positioning, pricing | `marketing/gtm-strategist/` |
| Copy, email, social, SEO content | `marketing/content-marketer/` |
| Growth, AARRR, experiments | `marketing/growth-marketer/` |
| Landing pages, CRO, funnels | `marketing/conversion-optimizer/` |
| Technical + on-page SEO | `marketing/seo-manager/` |
| Google, Meta, LinkedIn ads | `marketing/ppc-manager/` |
| Social media strategy | `marketing/smm-manager/` |

### Research (`knowledge/research/`)

| Need | Read |
|------|------|
| Research overview | `research/researcher/` |
| TAM/SAM, competitors, pricing | `research/market-researcher/` |

### Communication & HR (`knowledge/comms/`)

| Need | Read |
|------|------|
| Stakeholder dialogue, Mom Test | `comms/communicator/` |
| Hiring, onboarding, DEI | `comms/hr-recruiter/` |

### SDD (`knowledge/sdd/`)

| Need | Read |
|------|------|
| SDD workflow overview | `sdd/sdd/` |
| Specs, design docs, impl plans | `sdd/sdd-planning/` |

Execution tooling lives outside this skill — see `faion-sdd-execution` and `faion-feature-executor`.

## Related User-Invocable Skills

Independent skills — tools, not knowledge bases:

- `faion-brainstorm` — multi-agent diverge/converge/review
- `faion-sdd-execution` — quality gates, code review cycle
- `faion-feature-executor` — sequential SDD task execution
- `faion-improver` — session-based audit/improve loop
- `faion-media-ops` — media pipeline templates

## Methodology File Structure

```
{methodology}/
├── README.md       # Main content
├── checklist.md    # Step-by-step checklist
├── templates.md    # Code/config templates
├── examples.md     # Practical examples
└── llm-prompts.md  # AI prompts
```

Read `README.md` first; pull the others on demand.

## Statistics

| Metric | Count |
|--------|-------|
| Knowledge skills | 52 |
| Methodologies | 1300+ |
| Groups | 11 |

---

*Faion Network v4.0 — unified knowledge umbrella*
