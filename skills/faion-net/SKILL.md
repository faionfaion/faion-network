---
name: faion-net
description: "Universal orchestrator for software projects: SDD workflow, research, product planning, development, marketing, project/business analysis, UX, HR/recruiting. 60+ agents, 15 skills, 502 methodologies."
user-invocable: true
---

# Faion Network Orchestrator

**Communication: User's language.**

Universal skill for end-to-end software project lifecycle. From idea to production, from research to marketing.

---

## Step 1: Knowledge Freshness Check

**At session start, calculate:** `gap = current_date - model_cutoff` (from system prompt)

**Output:** `Knowledge gap: ~{months} months. WebSearch needed for: {areas}`

**Fast-changing areas (use WebSearch):**
- Package versions (npm, pip, cargo, go)
- Framework APIs (React, Next.js, Django, FastAPI)
- Cloud pricing (AWS, GCP, Azure)
- AI models (new releases, pricing, limits)
- Security (CVEs, vulnerabilities)

---

## Step 2: Execution Mode Selection

**Ask user at session start:**

```python
AskUserQuestion([
    {
        "question": "How should I work on tasks?",
        "header": "Mode",
        "options": [
            {"label": "YOLO Mode (Recommended)", "description": "Maximum autonomy. Execute tasks completely without interruptions. Uses faion-task-executor-YOLO-agent."},
            {"label": "Interactive Mode", "description": "Collaborative dialogue. Ask questions, clarify requirements, validate decisions. Stakeholder interview style."}
        ]
    }
])
```

---

### YOLO Mode (Autonomous)

**Agent:** `faion-task-executor-YOLO-agent`

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
    subagent_type="faion-task-executor-YOLO-agent"
)
```

---

### Interactive Mode (Dialogue)

**Skill:** `faion-communicator` (9 methodologies)

**Behavior:**
- Execute directly in main conversation flow
- Ask clarifying questions before proceeding
- Validate understanding at each step
- Use communication techniques:
  - **Interview:** Gather requirements with probing questions
  - **Brainstorm:** Generate options collaboratively
  - **Clarification:** Resolve ambiguity
  - **Validation:** Confirm before implementing
  - **Socratic:** Deep exploration through questions

**When to use:**
- Vague or incomplete requirements
- User wants to learn/understand
- Complex decisions needing input
- User prefers control over speed

**Communication Protocol:**

```markdown
## For new feature requests → Interview
"I'd like to understand your requirements:
1. What problem are you solving?
2. Who are the users?
3. What's the success criteria?
4. Any constraints?"

## For design decisions → Brainstorm + Validate
"Let's explore options:
- Option A: [pros/cons]
- Option B: [pros/cons]
Which direction feels right?"

## For ambiguous requirements → Clarification
"When you say 'fast', do you mean:
a) Response time < 100ms?
b) Quick to implement?
c) Fast user experience?"

## Before implementation → Validation
"Here's my understanding: [summary]
Is this correct? Shall I proceed?"
```

**Execution:**
- Use tools directly in conversation
- Ask questions via AskUserQuestion or text
- Provide step-by-step visibility
- Confirm before significant changes

---

## Capabilities

**Idea → Validation:**
- Generate startup/product ideas (7 frameworks)
- Research pain points via Reddit, forums, reviews
- Validate problems with evidence (frequency, severity, willingness to pay)
- Evaluate niche viability (market size, competition, barriers)
- Generate product names, check domain availability

**Research → Strategy:**
- Market research (TAM/SAM/SOM, trends, growth drivers)
- Competitor analysis (features, pricing, positioning)
- User personas from real feedback
- Pricing strategies and models
- Problem validation with evidence

**Product Planning:**
- MVP scope from competitor analysis
- MLP planning (gap analysis, WOW moments)
- Feature prioritization (RICE, MoSCoW)
- Roadmap design, release planning
- User story mapping, OKRs

**SDD Workflow:**
- Project bootstrap (constitution, roadmap)
- Specification writing with acceptance criteria
- Technical design documents
- Implementation plans with task parallelization
- Task execution with quality gates
- Reflexion learning (patterns, mistakes)

**Development:**
- Code generation (Python, JS/TS, Go, Ruby, PHP, Java, C#, Rust)
- Code review and refactoring
- Testing (unit, integration, E2E, TDD)
- API design (REST, GraphQL, OpenAPI)
- DevOps (CI/CD, Docker, K8s, Terraform, AWS)
- Browser automation (Puppeteer, Playwright)

**AI/LLM:**
- RAG pipelines (document Q&A, knowledge bases)
- Embeddings (generation, indexing, search)
- Fine-tuning (LoRA, QLoRA, PEFT)
- Prompt engineering and optimization
- Multimodal (image, video, audio generation)
- Voice agents (STT, TTS, real-time)
- Autonomous agents (LangGraph, ReAct)

**Marketing:**
- GTM strategy and execution
- Landing pages with high conversion
- Content marketing and SEO
- Paid ads (Meta, Google)
- Email campaigns and automation
- Social media strategy

**Project Management (Project Management Framework 7/8):**
- Stakeholder management
- Risk management
- Earned Value Management (EVM)
- Change control
- Agile, Waterfall, Hybrid delivery

**Business Analysis (Business Analysis Framework):**
- Requirements elicitation
- Traceability matrices
- Solution assessment
- 6 Knowledge Areas, 30 tasks

**UX:**
- User research (interviews, surveys, contextual inquiry)
- Usability testing (moderated, unmoderated)
- Heuristic evaluation (10 Usability Heuristics)
- Personas, journey mapping
- Wireframing, prototyping

---

## Domain Skills (14)

| Skill | Purpose |
|-------|---------|
| `faion-sdd` | SDD orchestrator: specs, designs, implementation plans, constitutions, task lifecycle, quality gates, reflexion |
| `faion-feature-executor` | SDD feature executor: sequential tasks with quality gates, tests/coverage, code review |
| `faion-researcher` | Idea generation (SCAMPER), market research, competitors, personas, pricing, validation. 20 methodologies |
| `faion-product-manager` | MVP/MLP planning, RICE/MoSCoW prioritization, roadmaps, backlog, user stories, OKRs. 18 methodologies |
| `faion-software-developer` | Python, JS/TS, Django, FastAPI, React, APIs, testing, DevOps, UI design. 68 methodologies |
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

## All Methodologies (494)

### Research
| Name | File |
|------|------|
| idea-generation | SCAMPER Ideation |
| mind-mapping | Mind Mapping |
| reverse-engineering-ideas | Reverse Engineering Ideas |
| problem-first-discovery | Problem-First Discovery |
| trend-surfing | Trend Surfing |
| skill-stack-analysis | Skill-Stack Analysis |
| market-research-tam-sam-som | Market Gap Analysis |
| pain-point-research | Pain Point Research |
| competitor-analysis | Competitor Feature Matrix |
| pricing-research | Pricing Strategy Analysis |
| persona-building | Persona Building |
| niche-evaluation | Niche Evaluation |
| problem-validation | Problem Validation |
| project-naming | Project Naming |

### Product
| Name | Description |
|------|-------------|
| mvp-scoping | MVP Scoping |
| mlp-planning | MLP Planning |
| feature-prioritization-rice | RICE Prioritization |
| feature-prioritization-moscow | MoSCoW Prioritization |
| roadmap-design | Roadmap Design |
| user-story-mapping | User Story Mapping |
| okr-setting | OKR Setting |
| problem-validation | Problem Validation |
| assumption-mapping | Assumption Mapping |
| lean-canvas | Lean Canvas |
| jobs-to-be-done | Jobs To Be Done |
| opportunity-scoring | Opportunity Scoring |
| value-proposition-canvas | Value Proposition Canvas |
| sprint-planning | Sprint Planning |
| release-planning | Release Planning |
| backlog-refinement | Backlog Refinement |
| five-whys-analysis | Five Whys Analysis |
| impact-mapping | Impact Mapping |

### Development
| Name | Description |
|------|-------------|
| python-django-standards | Django Coding Standards |
| python-django-decision-tree | Django Code Decision Tree |
| python-django-base-model | Django Base Model Pattern |
| python-django-testing-pytest | Django Testing with pytest |
| python-fastapi-standards | FastAPI Standards |
| python-async-patterns | Python Async Patterns |
| python-type-hints | Python Type Hints |
| python-poetry-setup | Poetry Project Setup |
| react-component-architecture | React Component Architecture |
| typescript-strict-mode | TypeScript Strict Mode |
| react-hooks-best-practices | React Hooks Best Practices |
| nextjs-app-router | Next.js App Router |
| nodejs-service-layer | Node.js Service Layer |
| express-fastify-patterns | Express/Fastify Patterns |
| bun-runtime | Bun Runtime |
| package-management-pnpm | Package Management (pnpm) |
| monorepo-turborepo | Monorepo Setup (Turborepo) |
| go-project-structure | Go Project Structure |
| go-error-handling | Go Error Handling |
| go-concurrency-patterns | Go Concurrency Patterns |
| rust-ownership-model | Rust Ownership Model |
| rust-error-handling | Rust Error Handling |
| ruby-rails-patterns | Ruby on Rails Patterns |
| php-laravel-patterns | PHP Laravel Patterns |
| java-spring-boot | Java Spring Boot |
| csharp-dotnet-patterns | C# .NET Patterns |
| clean-architecture | Clean Architecture |
| domain-driven-design | Domain-Driven Design |
| cqrs-pattern | CQRS Pattern |
| event-sourcing | Event Sourcing |
| microservices-design | Microservices Design |
| api-rest-design | API Design (REST) |
| api-graphql-design | API Design (GraphQL) |
| api-openapi-specification | OpenAPI Specification |
| database-design | Database Design |
| database-sql-optimization | SQL Optimization |
| database-nosql-patterns | NoSQL Patterns |
| caching-strategy | Caching Strategy |
| message-queues | Message Queues |
| websocket-design | WebSocket Design |
| testing-unit | Unit Testing |
| testing-integration | Integration Testing |
| testing-e2e | E2E Testing |
| testing-tdd-workflow | TDD Workflow |
| testing-fixtures | Test Fixtures |
| testing-mocking | Mocking Strategies |
| testing-coverage | Code Coverage |
| testing-security | Security Testing |
| testing-performance | Performance Testing |
| documentation | Documentation |
| claude-md-creation | CLAUDE.md Creation |
| code-review | Code Review |
| refactoring-patterns | Refactoring Patterns |
| technical-debt | Technical Debt |
| error-handling | Error Handling |
| logging-patterns | Logging Patterns |
| feature-flags | Feature Flags |
| ab-testing | A/B Testing |
| internationalization | Internationalization |
| accessibility | Accessibility |
| seo-spa | SEO for SPAs |
| pwa-development | PWA Development |
| mobile-responsive | Mobile Responsive |
| ui-component-library | UI Component Library |
| storybook-setup | Storybook Setup |
| design-tokens | Design Tokens |
| css-in-js | CSS-in-JS |
| tailwind-patterns | Tailwind Patterns |

### DevOps
| Name | Description |
|------|-------------|
| docker-containerization | Docker Containerization |
| docker-compose | Docker Compose |
| kubernetes-deployment | Kubernetes Deployment |
| kubernetes-helm-charts | Helm Charts |
| terraform-iac | Terraform IaC |
| aws-architecture | AWS Architecture |
| gcp-architecture | GCP Architecture |
| azure-architecture | Azure Architecture |
| cicd-github-actions | GitHub Actions CI/CD |
| cicd-gitlab | GitLab CI/CD |
| cicd-jenkins | Jenkins Pipelines |
| gitops-argocd | ArgoCD GitOps |
| monitoring-prometheus | Prometheus Monitoring |
| monitoring-grafana | Grafana Dashboards |
| logging-elk-stack | ELK Stack Logging |
| nginx-configuration | Nginx Configuration |
| load-balancing | Load Balancing |
| ssl-tls-setup | SSL/TLS Setup |
| secrets-management | Secrets Management |
| backup-strategies | Backup Strategies |

### ML/AI
| Name | Description |
|------|-------------|
| llm-openai-api | OpenAI API Integration |
| llm-claude-api | Claude API Integration |
| llm-gemini-api | Gemini API Integration |
| llm-local-ollama | Local LLM (Ollama) |
| embedding-generation | Embedding Generation |
| vector-database-setup | Vector Database Setup |
| rag-pipeline-design | RAG Pipeline Design |
| rag-evaluation | RAG Evaluation |
| hybrid-search | Hybrid Search |
| reranking | Reranking |
| chunking-strategies | Chunking Strategies |
| fine-tuning-openai | Fine-tuning (OpenAI) |
| fine-tuning-lora | Fine-tuning (LoRA) |
| prompt-engineering | Prompt Engineering |
| chain-of-thought | Chain-of-Thought |
| function-calling | Tool Use / Function Calling |
| structured-output | Structured Output |
| guardrails | Guardrails |
| llm-cost-optimization | Cost Optimization |
| model-evaluation | Model Evaluation |
| langchain-patterns | LangChain Patterns |
| llamaindex-patterns | LlamaIndex Patterns |
| autonomous-agents | Autonomous Agents |
| multi-agent-systems | Multi-Agent Systems |
| image-generation | Image Generation (DALL-E, Midjourney) |
| image-analysis-vision | Image Analysis (Vision) |
| speech-to-text | Speech-to-Text |
| text-to-speech | Text-to-Speech |
| voice-agents | Voice Agents |
| video-generation | Video Generation |

### Marketing
| Name | Description |
|------|-------------|
| gtm-strategy | GTM Strategy |
| icp-definition | ICP Definition |
| value-proposition-design | Value Proposition |
| positioning-statement | Positioning Statement |
| messaging-framework | Messaging Framework |
| landing-page-design | Landing Page Design |
| above-the-fold-design | Hero Section |
| social-proof-strategy | Social Proof |
| cta-optimization | CTA Optimization |
| ab-testing-framework | A/B Testing |
| copywriting-fundamentals | Copywriting Formulas |
| aida-framework | AIDA Framework |
| pas-framework | PAS Framework |
| feature-benefit-mapping | Feature-Benefit Mapping |
| seo-on-page-optimization | SEO On-Page |
| seo-fundamentals | SEO Technical |
| keyword-research | Keyword Research |
| content-marketing | Content Strategy |
| blog-post-template | Blog Writing |
| link-building-strategy | Guest Posting |
| seo-link-building | Link Building |
| google-ads-structure | Google Ads |
| meta-ads-structure | Meta Ads |
| linkedin-strategy | LinkedIn Ads |
| retargeting-strategy | Retargeting |
| welcome-sequence | Email Welcome Sequence |
| newsletter-strategy | Newsletter |
| nurture-sequence | Drip Campaigns |
| email-deliverability | Email Deliverability |
| social-media-strategy | Social Media Strategy |
| twitter-x-strategy | Twitter/X Growth |
| linkedin-content-strategy | LinkedIn Growth |
| community-building | Community Building |
| influencer-partnership | Influencer Marketing |
| product-hunt-launch | Product Hunt Launch |
| press-coverage | Press Release |
| marketing-analytics-stack | Analytics Setup |
| conversion-tracking | Conversion Tracking |
| funnel-optimization | Funnel Analysis |
| customer-lifecycle-marketing | Customer Journey |

### Growth
| Name | Description |
|------|-------------|
| aarrr-pirate-metrics | AARRR Pirate Metrics |
| north-star-metric | North Star Metric |
| growth-loops | Growth Loops |
| ab-testing-framework | A/B Testing Framework |
| multivariate-testing | Multivariate Testing |
| statistical-significance | Statistical Significance |
| cohort-analysis | Cohort Analysis |
| funnel-optimization | Funnel Optimization |
| viral-coefficient | Viral Coefficient |
| product-led-growth | Product-Led Growth |
| activation-rate | Activation Rate |
| retention-loops | Retention Loops |

### Advertising
| Name | Description |
|------|-------------|
| meta-campaign-setup | Meta Campaign Setup |
| meta-targeting | Meta Targeting |
| meta-creative | Meta Creative |
| meta-reporting | Meta Reporting |
| google-campaign-setup | Google Campaign Setup |
| google-keywords | Google Keywords |
| google-creative | Google Creative |
| google-reporting | Google Reporting |
| linkedin-ads | LinkedIn Ads |
| twitter-ads | Twitter Ads |
| analytics-setup | Analytics Setup |
| conversion-tracking | Conversion Tracking |
| attribution-models | Attribution Models |
| budget-optimization | Budget Optimization |
| ab-testing-ads | A/B Testing Ads |
| retargeting | Retargeting |

### Business Operations
| Name | Description |
|------|-------------|
| pricing-strategy | Pricing Strategy |
| subscription-models | Subscription Models |
| customer-support | Customer Support |
| churn-prevention | Churn Prevention |
| upselling-cross-selling | Upselling & Cross-selling |
| partnership-strategy | Partnership Strategy |
| financial-planning | Financial Planning |
| legal-compliance | Legal Compliance |
| tax-considerations | Tax Considerations |
| hiring-contractors | Hiring Contractors |
| automation-workflow | Automation Workflow |
| customer-success | Customer Success |
| metrics-dashboards | Metrics Dashboards |
| annual-planning | Annual Planning |

### Project Management
| Name | Description |
|------|-------------|
| stakeholder-register | Stakeholder Register |
| stakeholder-analysis-matrix | Stakeholder Analysis Matrix |
| raci-matrix | RACI Matrix |
| team-charter | Team Charter |
| development-approach-selection | Development Approach Selection |
| project-life-cycle-design | Project Life Cycle Design |
| wbs-creation | WBS Creation |
| schedule-development | Schedule Development |
| cost-estimation | Cost Estimation |
| communication-management-plan | Communication Management Plan |
| change-management-process | Change Management Process |
| quality-management-plan | Quality Management Plan |
| acceptance-criteria-definition | Acceptance Criteria Definition |
| earned-value-management | Earned Value Management |
| project-dashboard-design | Project Dashboard Design |
| risk-register | Risk Register |
| risk-response-planning | Risk Response Planning |
| lessons-learned | Lessons Learned |
| project-closure-checklist | Project Closure Checklist |
| project-status-report | Project Status Report |

### PM Tools
| Name | Description |
|------|-------------|
| jira-workflow | Jira Workflow Management |
| clickup-setup | ClickUp Setup |
| linear-issue-tracking | Linear Issue Tracking |
| github-projects | GitHub Projects |
| gitlab-boards | GitLab Boards |
| azure-devops-boards | Azure DevOps Boards |
| notion-pm | Notion PM |
| trello-kanban | Trello Kanban |
| cross-tool-migration | Cross-Tool Migration |
| pm-tool-selection | PM Tool Selection |
| agile-ceremonies-setup | Agile Ceremonies Setup |
| reporting-dashboards | Reporting & Dashboards |

### Business Analysis
| Name | Description |
|------|-------------|
| ba-planning | Business Case Development |
| stakeholder-analysis | Stakeholder Analysis |
| elicitation-techniques | Requirements Elicitation |
| use-case-modeling | Use Case Modeling |
| user-story-mapping | User Story Writing |
| acceptance-criteria | Acceptance Criteria |
| requirements-traceability | Traceability Matrix |
| strategy-analysis | Gap Analysis |
| business-process-analysis | Process Modeling (BPMN) |
| data-analysis | Data Modeling |
| solution-assessment | Solution Assessment |
| requirements-validation | Feasibility Study |

### UX/UI
| Name | Description |
|------|-------------|
| user-interviews | User Interviews |
| surveys | Surveys |
| contextual-inquiry | Contextual Inquiry |
| competitive-analysis | Competitive Analysis |
| personas | Persona Development |
| empathy-mapping | Empathy Mapping |
| journey-mapping | Journey Mapping |
| service-blueprint | Service Blueprint |
| information-architecture | Information Architecture |
| card-sorting | Card Sorting |
| wireframing | Wireframing |
| prototyping | Prototyping |
| usability-testing | Usability Testing |
| heuristic-evaluation | Heuristic Evaluation |
| ab-testing | A/B Testing |
| accessibility-evaluation | Accessibility Audit |
| design-tokens-fundamentals | Design System |
| component-library | Component Library |
| typography-system | Typography System |
| color-system | Color System |
| spacing-system | Spacing System |
| icon-system | Icon System |
| motion-design | Motion Design |
| micro-interactions | Micro-interactions |
| form-design | Form Design |
| navigation-patterns | Navigation Patterns |
| search-ux | Search UX |
| error-states | Error States |
| empty-states | Empty States |
| loading-states | Loading States |
| onboarding | Onboarding |
| dark-mode | Dark Mode |

### SDD
| Name | Description |
|------|-------------|
| sdd-workflow-overview | Constitution Creation |
| writing-specifications | Roadmap Planning |
| writing-technical-design | Feature Specification |
| creating-implementation-plans | Technical Design |
| task-creation-parallelization | Implementation Plan |
| executing-single-task | Task Breakdown |
| constitution-guidelines | Task Execution |
| quality-gates-review-cycle | Quality Gate |
| reflexion-learning | Code Review Cycle |
| pattern-memory | Reflexion Learning |
| mistake-memory | Pattern Memory |
| agentic-sdd-integration | Mistake Memory |

### Communication
| Name | Description |
|------|-------------|
| active-listening | Active Listening (RASA, Empathic, Reflective) |
| mom-test | The Mom Test (Customer Validation) |
| stakeholder-communication | Stakeholder Communication (Interview, Brainstorm, Clarify, Validate, Socratic) |
| conflict-resolution | Conflict Resolution (Thomas-Kilmann, NVC) |
| giving-receiving-feedback | Giving & Receiving Feedback (SBI, Radical Candor, EEC) |
| selling-ideas | Selling Ideas (SPIN Selling, Challenger Sale, Elevator Pitch) |
| business-storytelling | Business Storytelling (Pyramid Principle, SCQA, Pixar) |
| negotiation-persuasion | Negotiation & Persuasion (BATNA, Cialdini's 6) |
| difficult-conversations | Difficult Conversations (Crucial Conversations, DESC) |
| brainstorming-ideation | Brainstorming & Ideation (SCAMPER, Mind Mapping, 6-3-5) |

---

## References

**Workflow:**
- [SDD Workflow](references/workflow.md) - Phases, project/feature selection
- [Directory Structure](references/directory-structure.md) - SDD folder layout
- [Quality Assurance](references/quality-assurance.md) - Confidence checks, reflexion

**Domains (Reference → Skill):**

| Domain | Reference | Skill to Invoke |
|--------|-----------|-----------------|
| SDD | [sdd-domain.md](references/sdd-domain.md) | `faion-sdd` |
| Research | [research-domain.md](references/research-domain.md) | `faion-researcher` |
| Product | [product-domain.md](references/product-domain.md) | `faion-product-manager` |
| Development | [development-domain.md](references/development-domain.md) | `faion-software-developer` |
| DevOps | [development-domain.md](references/development-domain.md) | `faion-devops-engineer` |
| Marketing | [marketing-domain.md](references/marketing-domain.md) | `faion-marketing-manager` |
| Project Management | [pm-domain.md](references/pm-domain.md) | `faion-project-manager` |
| Business Analysis | [ba-domain.md](references/ba-domain.md) | `faion-business-analyst` |
| UX/UI | [ux-domain.md](references/ux-domain.md) | `faion-ux-ui-designer` |
| AI/LLM | [ai-llm-domain.md](references/ai-llm-domain.md) | `faion-ml-engineer` |
| Communication | [faion-communicator](~/.claude/skills/faion-communicator/SKILL.md) | `faion-communicator` |
| Claude Code | - | `faion-claude-code` |

---

*Faion Network v2.0*
*14 Domain Skills | 494 Methodologies | 60+ Agents*
