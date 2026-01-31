# Faion Network Orchestrator

**Entry Point:** `/faion-net`

Universal orchestrator: 54 skills, 1297 methodologies across Development, DevOps, AI/ML, Product, Marketing, PM, BA, UX, Research.

## How It Works

```
/faion-net → Analyze intent → Skill tool → Domain skill loads → Execute
```

**CRITICAL:** Invoke domain skills using `Skill(skill-name)`. Markdown links do NOT load skills.

## Decision Tree

| Category | Intent | Invoke |
|----------|--------|--------|
| **Research** | Market, competitors, TAM | `Skill(faion-researcher)` |
| **Architecture** | System design, ADRs | `Skill(faion-software-architect)` |
| **Product** | MVP, roadmaps, OKRs | `Skill(faion-product-manager)` |
| **Python** | Django, FastAPI | `Skill(faion-python-developer)` |
| **JavaScript** | React, Node, Next.js | `Skill(faion-javascript-developer)` |
| **Backend** | Go, Rust, Java, C# | `Skill(faion-backend-systems)` or `Skill(faion-backend-enterprise)` |
| **Frontend** | Tailwind, PWA | `Skill(faion-frontend-developer)` |
| **APIs** | REST, GraphQL | `Skill(faion-api-developer)` |
| **Testing** | TDD, E2E | `Skill(faion-testing-developer)` |
| **DevOps** | Docker, K8s, CI/CD | `Skill(faion-infrastructure-engineer)` or `Skill(faion-cicd-engineer)` |
| **LLM** | OpenAI, Claude APIs | `Skill(faion-llm-integration)` |
| **RAG** | Embeddings, vectors | `Skill(faion-rag-engineer)` |
| **AI Agents** | LangChain, MCP | `Skill(faion-ai-agents)` |
| **GTM** | Launches, pricing | `Skill(faion-gtm-strategist)` |
| **Growth** | AARRR, A/B tests | `Skill(faion-growth-marketer)` |
| **SEO** | Technical, on-page | `Skill(faion-seo-manager)` |
| **PM Agile** | Scrum, Kanban | `Skill(faion-pm-agile)` |
| **BA** | Requirements, BPMN | `Skill(faion-ba-core)` |
| **UX Research** | Interviews, testing | `Skill(faion-ux-researcher)` |
| **UI Design** | Wireframes, tokens | `Skill(faion-ui-designer)` |
| **SDD** | Specs, design docs | `Skill(faion-sdd-planning)` |

## Statistics

| Metric | Count |
|--------|-------|
| Skills | 54 |
| Orchestrators | 3 |
| Leaf skills | 51 |
| Methodologies | 1297 |

## Methodology Structure

Each methodology is a folder with 5 files:
```
{methodology}/
├── README.md       # Main content
├── checklist.md    # Step-by-step checklist
├── templates.md    # Code/config templates
├── examples.md     # Practical examples
└── llm-prompts.md  # AI prompts
```

**Full decision tree:** [SKILL.md](SKILL.md)

---

*Faion Network v3.0*
