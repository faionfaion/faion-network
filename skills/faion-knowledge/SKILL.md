---
name: faion-knowledge
description: "Umbrella knowledge skill: 52 domain knowledge bases, 1300+ methodologies. Content organized by pricing tier (free/solo/pro/geek)."
tier: free
user-invocable: true
---

# Faion Knowledge

**Communication: User's language.**

Single umbrella skill bundling all domain knowledge. No per-domain sub-skills — all content is markdown, loaded on demand with Read, organized into tier subtrees (`free`, `solo`, `pro`, `geek`) matching the pricing manifest.

## Structure

```
knowledge/
├── free/   8 skills   dev core (Python, JS, testing, quality, backend/devtools router, full-stack) + marketing router
├── solo/  13 skills   frontend, API, architect, automation, server-craft, SDD, product planning/ops, UI, content, SEO, comms
├── pro/   24 skills   backend systems/enterprise, DevOps/CI/CD/infra, PM, product-manager, BA, UX research, growth/GTM/PPC/SMM/CRO, research, HR
└── geek/   7 skills   ML engineer, AI agents, RAG, ML ops, multimodal AI, LLM integration, Claude Code
```

Each tier holds per-group subdirs (`dev/`, `infra/`, `marketing/`, etc.). Each skill = folder with `SKILL.md` + methodology subfolders. Each methodology = `README.md` + `checklist.md` + `templates.md` + `examples.md` + `llm-prompts.md`.

## How It Works

```
User task → Identify domain → Resolve tier → Read knowledge/<tier>/<group>/<name>/README.md → Apply
```

No `Skill(faion-X)` calls — those sub-skills no longer exist. Load domain content with `Read` or `Grep` against `knowledge/<tier>/<group>/...`. Tier gating is a directory boundary: a free-tier session should only read from `knowledge/free/`, solo from `free + solo`, pro from `free + solo + pro`, geek from all four.

## Tier Map

### Free (8) — `knowledge/free/`

Core developer skill set + marketing router. Everyone gets these.

| Need | Read |
|------|------|
| Full-stack overview | `free/dev/software-developer/` |
| Python (Django, FastAPI) | `free/dev/python-developer/` |
| JS/TS (React, Node, Next.js) | `free/dev/javascript-developer/` |
| Testing (TDD, E2E, mocking) | `free/dev/testing-developer/` |
| Code quality, DDD, refactoring | `free/dev/code-quality/` |
| Backend router | `free/dev/backend-developer/` |
| DevTools overview | `free/dev/devtools-developer/` |
| Marketing overview | `free/marketing/marketing-manager/` |

### Solo (13) — `knowledge/solo/`

Extends free with solopreneur / small-team essentials: frontend polish, API design, architecture, SDD, product planning, UI, content/SEO, comms.

| Need | Read |
|------|------|
| Frontend (Tailwind, PWA, a11y) | `solo/dev/frontend-developer/` |
| APIs (REST, GraphQL, OpenAPI) | `solo/dev/api-developer/` |
| System design, ADRs | `solo/dev/software-architect/` |
| Puppeteer, monorepo, automation | `solo/dev/automation-tooling/` |
| SSH, nginx, systemd, tuning | `solo/infra/server-craft/` |
| SDD workflow overview | `solo/sdd/sdd/` |
| Specs, design docs, impl plans | `solo/sdd/sdd-planning/` |
| MVP, roadmaps, OKRs | `solo/product/product-planning/` |
| Prioritization, backlog, analytics | `solo/product/product-operations/` |
| Wireframes, design systems | `solo/ux/ui-designer/` |
| Copy, email, social, SEO content | `solo/marketing/content-marketer/` |
| Technical + on-page SEO | `solo/marketing/seo-manager/` |
| Stakeholder dialogue, Mom Test | `solo/comms/communicator/` |

### Pro (24) — `knowledge/pro/`

Extends solo with enterprise / agency breadth: heavy backend stacks, full DevOps pipeline, PM/BA rigor, UX research, paid marketing, user research, HR.

| Need | Read |
|------|------|
| Go, Rust, DBs, caching | `pro/dev/backend-systems/` |
| Java, C#, PHP, Ruby | `pro/dev/backend-enterprise/` |
| DevOps overview | `pro/infra/devops-engineer/` |
| CI/CD, GitHub Actions, GitOps | `pro/infra/cicd-engineer/` |
| Docker, K8s, Terraform, AWS/GCP | `pro/infra/infrastructure-engineer/` |
| PM overview | `pro/pm/project-manager/` |
| Scrum, Kanban, SAFe | `pro/pm/pm-agile/` |
| PMBoK, EVM, WBS | `pro/pm/pm-traditional/` |
| Product management overview | `pro/product/product-manager/` |
| BA overview | `pro/ba/business-analyst/` |
| Requirements, elicitation, strategy | `pro/ba/ba-core/` |
| Use cases, BPMN, data models | `pro/ba/ba-modeling/` |
| UX/UI overview | `pro/ux/ux-ui-designer/` |
| User interviews, usability | `pro/ux/ux-researcher/` |
| Personas, JTBD | `pro/ux/user-researcher/` |
| WCAG, a11y | `pro/ux/accessibility-specialist/` |
| Growth, AARRR, experiments | `pro/marketing/growth-marketer/` |
| Launches, positioning, pricing | `pro/marketing/gtm-strategist/` |
| Google, Meta, LinkedIn ads | `pro/marketing/ppc-manager/` |
| Social media strategy | `pro/marketing/smm-manager/` |
| Landing pages, CRO, funnels | `pro/marketing/conversion-optimizer/` |
| TAM/SAM, competitors, pricing | `pro/research/market-researcher/` |
| Research overview | `pro/research/researcher/` |
| Hiring, onboarding, DEI | `pro/comms/hr-recruiter/` |

### Geek (7) — `knowledge/geek/`

AI agent-builder tier. Everything else plus the full AI/ML knowledge stack.

| Need | Read |
|------|------|
| ML/AI overview | `geek/ai/ml-engineer/` |
| AI agents, LangChain, MCP | `geek/ai/ai-agents/` |
| RAG, embeddings, vector DBs | `geek/ai/rag-engineer/` |
| Fine-tuning, evals, ML Ops | `geek/ai/ml-ops/` |
| Vision, image/video, TTS/STT | `geek/ai/multimodal-ai/` |
| LLM APIs (OpenAI, Claude, Gemini) | `geek/ai/llm-integration/` |
| Claude Code setup, skills, hooks | `geek/ai/claude-code/` |

## Related User-Invocable Skills

Independent skills — tools, not knowledge bases:

- `faion-brainstorm` — multi-agent diverge/converge/review (free+)
- `faion-sdd-execution` — quality gates, code review cycle (solo+)
- `faion-feature-executor` — sequential SDD task execution (solo+)
- `faion-improver` — session-based audit/improve loop (pro+)
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
| Tiers | 4 |
| Groups | 11 |

See [tier-manifest.json](../tier-manifest.json) for the authoritative tier-to-path mapping.

---

*Faion Network v4.1 — tier-partitioned knowledge umbrella*
