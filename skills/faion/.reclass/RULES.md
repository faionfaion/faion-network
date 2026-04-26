# Tier Classification Rules

Methodology = one folder with `README.md` + 4 sibling docs. Each methodology has ONE tier.

## Tier definitions

### FREE — anyone can use it
Basics, fundamentals, standard single-developer patterns. No enterprise context, no team-of-team coordination, no production-at-scale concerns, no AI.

- Hello-world / getting-started / 101 / fundamentals / intro
- Core language features (python-basics, js-async-basics, go-concurrency-101)
- Standard tooling (git-basics, unit-testing, basic-refactoring, linting)
- Terminal, IDE, git workflows
- Basic marketing copy / SEO copywriting / one-pager landing pages

### SOLO — solopreneur / small team
Builds real products alone or with a couple of collaborators. Needs craftsmanship, not enterprise rigor.

- Frontend polish (Tailwind, component libs, PWA, responsive, a11y-basics)
- API design (REST, GraphQL, OpenAPI, contract-first)
- Architecture basics (ADR, DDD-lite, clean architecture, monorepo)
- Product MVP / roadmap / single-owner backlog
- Self-hosted single-server ops (nginx, systemd, Docker Compose, Cloudflare)
- Content marketing / technical SEO / organic social
- SDD workflow, quality gates for solo projects
- Stakeholder communication / customer dev (Mom Test, discovery calls)

### PRO — enterprise / agency
Production-at-scale, multi-team coordination, compliance, paid growth, formal research.

- Scale patterns: horizontal scaling, sharding, CQRS, event sourcing, microservices
- Distributed systems, consistency, consensus, saga, outbox
- SRE / observability stacks (Prometheus, Grafana, OpenTelemetry, tracing-at-scale)
- Kubernetes, Terraform, multi-cloud, GitOps
- Enterprise backend stacks (Java/Spring, C#/.NET, PHP/Laravel, Ruby/Rails)
- Formal PM: SAFe, PMBoK, EVM, WBS, RACI, Scrum-of-Scrums
- BA modeling: BPMN, UML, data models, capability maps, requirements traceability
- Formal UX research: usability studies, JTBD frameworks, personas at scale, WCAG compliance
- Paid marketing: PPC (Google/Meta/LinkedIn), SMM at scale, growth experiments, CRO
- Market research: TAM/SAM/SOM, competitive intelligence, pricing research
- HR: hiring pipelines, onboarding, DEI

### GEEK — AI agent builder
Anything touching ML, LLM, AI agents, or AI-native workflows.

- ML engineering, model training, evals, fine-tuning
- LLM integration (OpenAI, Anthropic, Gemini APIs), prompt engineering, caching
- RAG: embeddings, vector DBs, hybrid search, re-ranking
- AI agents: LangChain, Agent SDK, MCP, tool use, orchestration
- Multimodal AI: vision, TTS/STT, video gen, image gen
- ML Ops: model deploys, drift detection, online evals
- Claude Code: skills, hooks, sub-agents, settings

## Decision procedure per methodology

1. Read first 30 lines of `README.md`.
2. Match strongest signal against tier definitions above.
3. Tie-break: if content assumes enterprise context (load balancers, distributed transactions, 10+ engineers) → PRO. If it assumes AI primitives (embeddings, LLM calls) → GEEK. If it's single-operator → SOLO. If it's "first principles" → FREE.
4. If still ambiguous after content read, keep it in its current tier (conservative).

## Name heuristics (fast-pass before content read)

| Regex signal | Strong tier |
|--------------|-------------|
| `^(ml-|ai-|llm-|rag-|agent-sdk|claude-|multimodal-|fine-tun|embedding|vector-|prompt-)` | GEEK |
| `(kubernetes|k8s|terraform|multi-cloud|sharding|cqrs|event-sourcing|microservices|sre-|observability|prometheus|grafana|distributed-)` | PRO |
| `(ppc|smm|paid-|safe-|pmbok|evm-|wbs-|bpmn|uml-|wcag|compliance|enterprise-)` | PRO |
| `(mvp|roadmap|adr|monorepo|pwa|tailwind|openapi|rest-design|graphql|content-marketing|seo-technical|sdd-|server-craft)` | SOLO |
| `(basics|fundamentals|101|hello-world|intro|getting-started|tutorial|unit-testing|git-basics)` | FREE |

## Move target rule

A methodology at `knowledge/<tier-A>/<group>/<domain>/<methodology>/` moves to `knowledge/<tier-B>/<group>/<domain>/<methodology>/` — same group and domain, new tier. Create the destination domain folder if it doesn't exist in that tier.

Never move a methodology to a different group or domain — only tier changes.
