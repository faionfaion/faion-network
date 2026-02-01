# Key Trends Summary 2025-2026

Comprehensive overview of major trends in Specification-Driven Development and documentation practices.

**Last Updated:** 2026-01-25
**Version:** 2.0

---

## Overview

This methodology covers the evolving landscape of SDD, living documentation, ADRs, and AI-assisted development. These trends fundamentally reshape how software is specified, designed, documented, and built.

**Key Insight:** The bottleneck has shifted from implementation to specification. LLMs can generate code at scale, but quality specifications remain a human-centric skill.

---

## 1. Specification-Driven Development (SDD)

### What Changed

SDD emerged as the dominant paradigm for AI-assisted development in 2025. The core principle: **Intent is the source of truth** - specifications drive code generation, not vice versa.

### Core Workflow

```
Intent → Spec → Plan → Execute → Review
```

| Phase | Owner | Output |
|-------|-------|--------|
| Intent | Human | Problem statement, goals |
| Spec | Human + LLM | Requirements, acceptance criteria |
| Plan | LLM + Human review | Implementation steps, file changes |
| Execute | LLM | Code, tests, docs |
| Review | Human | Validation, approval |

### Key Principles

1. **Human-in-the-Loop**: LLMs draft artifacts, humans review before proceeding
2. **Spec Quality = Code Quality**: Better specs yield better generated code
3. **Context Engineering**: Refined context > raw prompts
4. **Iterative Refinement**: Specs evolve through implementation feedback

### Where SDD Works Best

| Scenario | Effectiveness |
|----------|---------------|
| Feature work in existing systems (N to N+1) | Highest |
| Greenfield with clear requirements | High |
| Legacy modernization | Medium-High |
| Exploratory/R&D work | Medium |
| Vibe coding / rapid prototypes | Low (use different approach) |

### Major Tools (2025)

| Tool | Vendor | Key Feature |
|------|--------|-------------|
| Kiro | Amazon | Full SDD workflow with hooks |
| Spec Kit | GitHub/Microsoft | Open-source toolkit |
| Tessl | Tessl | Framework and registry |
| Claude Code | Anthropic | Native SDD support |

---

## 2. Living Documentation

### Docs-as-Code

Documentation treated as first-class code: version controlled, CI/CD pipelines, automated testing.

**Core Stack:**
- **Format:** Markdown/MDX
- **Storage:** Git repository
- **Build:** Static site generators (Docusaurus, MkDocs, Mintlify)
- **CI/CD:** Automated linting, link checking, publishing

### LLM-Optimized Documentation

Documentation structured for both human and LLM consumption:

| Pattern | Benefit |
|---------|---------|
| Clear headings hierarchy | Better LLM parsing |
| Explicit context sections | Reduced hallucination |
| Code blocks with language tags | Accurate code generation |
| API contracts in specs | Type-safe integration |

### Auto-Generation Pipeline

```
Source Code
    ↓
Static Analysis + Docstrings
    ↓
OpenAPI/GraphQL Schema
    ↓
Generated Documentation
    ↓
Developer Portal (Backstage, GitBook)
```

### Developer Portals (2025-2026)

| Platform | Market Position | Best For |
|----------|-----------------|----------|
| Backstage | 89% market share | Large orgs, extensibility |
| Port | Rising | Service catalogs, workflows |
| Cortex | Growing | Service ownership, scorecards |
| Roadie | SaaS leader | Backstage without ops overhead |

**Key Insight:** Portal is not the platform. The portal is UI; the platform is the backend that provisions resources.

---

## 3. Architecture Decision Records (ADRs)

### Industry Adoption

ADRs are now standard practice across AWS, Google Cloud, Microsoft Azure, and UK Government. They're part of well-architected frameworks.

### ADR Lifecycle

```
Draft → Review → Accepted → [Superseded/Deprecated]
```

**Key Rule:** ADRs are append-only. Never edit accepted ADRs; create new ones that supersede old decisions.

### Storage Pattern

```
project/
└── docs/
    └── adr/
        ├── 0001-use-postgresql.md
        ├── 0002-adopt-event-sourcing.md
        └── template.md
```

### Best Practices (AWS 200+ ADRs Experience)

| Practice | Rationale |
|----------|-----------|
| Keep meetings 30-45 min | Focused discussions |
| One decision per ADR | Simpler review |
| Separate design from decision | Reference design docs |
| Push for timely decisions | Most are two-way doors |
| Team collaboration | All affected teams approve |

### ADR Structure

1. **Title** - Short descriptive name
2. **Status** - Proposed/Accepted/Deprecated/Superseded
3. **Context** - What forces are at play
4. **Decision** - What we decided
5. **Consequences** - What happens as a result
6. **Alternatives** - What we considered

---

## 4. LLM-First Workflows

### Adoption Metrics (2025)

- 65% of developers use AI coding tools weekly (Stack Overflow)
- 25% of Y Combinator W25 codebases are 95%+ AI-generated
- 90% of Claude Code's code is written by Claude Code itself (Anthropic)
- ~25% of Microsoft and Google code is AI-generated

### Effective Workflow Patterns

**Context Packing:**
1. Brain dump everything the model should know
2. Include high-level goals and invariants
3. Provide examples of good solutions
4. Warn about approaches to avoid

**Spec-First Workflow:**
1. Write detailed spec before any code
2. Break work into small testable chunks
3. Provide extensive codebase context
4. Review and test everything generated

### Agentic Development

Model Context Protocol (MCP) has become the standard for agent interactions:

| Component | Purpose |
|-----------|---------|
| MCP Servers | Tool providers |
| MCP Clients | AI agents |
| Resources | Context data |
| Tools | Callable functions |

**2026 Prediction:** Multi-agent workflows with parallel execution become mainstream.

### Challenges

| Challenge | Mitigation |
|-----------|------------|
| Context window limits | Chunking, RAG, better prompts |
| Hallucination | Human review gates, testing |
| Spec drift | Continuous validation |
| Non-determinism | CI/CD quality gates |

---

## 5. Platform Engineering Impact

### Market Trajectory

- 2022: 45% of large orgs have platform teams
- 2026: 80% projected (Gartner)

### Platform vs Portal

| Aspect | Platform | Portal |
|--------|----------|--------|
| What | Backend system | Frontend UI |
| Does | Provisions, deploys, orchestrates | Discovers, accesses, visualizes |
| Example | Kubernetes, Terraform | Backstage, Port |

### Developer Experience Focus

**Golden Paths:** Paved roads that make the right thing easy:

```
New Service Template → CI/CD Auto-Config → Observability Built-in
```

**Metrics that Matter:**
- Time to first commit
- Deployment frequency
- Lead time for changes
- Mean time to recovery

---

## 6. Observability-Driven Development

### OpenTelemetry Dominance

OTel is now the #2 CNCF project (after Kubernetes). It provides vendor-neutral telemetry.

### Three Pillars + Profiling

| Signal | Use Case |
|--------|----------|
| Logs | Event records |
| Metrics | Measurements over time |
| Traces | Request flow across services |
| Profiles | Resource consumption (new in 2025) |

### Shift-Left Observability

```
Dev → Test → Stage → Prod
 ↑      ↑      ↑      ↑
Observability at every stage
```

### Collector Patterns

| Pattern | When |
|---------|------|
| Agent | Per-instance, low latency |
| Gateway | Centralized, easier ops |
| Hierarchical | Agent + Gateway combined |

---

## LLM Usage Tips

### For Spec Writing

- Ask LLM to identify missing requirements
- Use LLM to generate acceptance criteria from user stories
- Have LLM critique your spec for ambiguity

### For ADR Creation

- Provide context about your system
- Ask for alternative analysis
- Request consequence mapping

### For Documentation

- Generate initial structure from code
- Ask for consistency review
- Request readability improvements

---

## External Resources

### Specification-Driven Development

- [Thoughtworks: SDD - Key 2025 Practice](https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices)
- [Martin Fowler: SDD Tools Analysis](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)
- [GitHub Blog: Spec-Driven Development Toolkit](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)
- [Microsoft: Spec Kit](https://developer.microsoft.com/blog/spec-driven-development-spec-kit)
- [JetBrains: Spec-Driven Approach](https://blog.jetbrains.com/junie/2025/10/how-to-use-a-spec-driven-approach-for-coding-with-ai/)
- [Red Hat: SDD Quality](https://developers.redhat.com/articles/2025/10/22/how-spec-driven-development-improves-ai-coding-quality)
- [Amazon Kiro: Future of SDD](https://kiro.dev/blog/kiro-and-the-future-of-software-development/)
- [Zencoder: Practical SDD Guide](https://docs.zencoder.ai/user-guides/tutorials/spec-driven-development-guide)

### Architecture Decision Records

- [AWS: ADR Best Practices](https://aws.amazon.com/blogs/architecture/master-architecture-decision-records-adrs-best-practices-for-effective-decision-making/)
- [Google Cloud: ADR Overview](https://docs.cloud.google.com/architecture/architecture-decision-records)
- [Microsoft Azure: ADR Framework](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record)
- [ADR GitHub Organization](https://adr.github.io/)
- [UK GOV: ADR Framework](https://www.gov.uk/government/publications/architectural-decision-record-framework/architectural-decision-record-framework)
- [Michael Nygard: Original ADR Post](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)

### Living Documentation

- [Squarespace: Docs-as-Code Journey](https://engineering.squarespace.com/blog/2025/making-documentation-simpler-and-practical-our-docs-as-code-journey)
- [GitBook: LLM-Ready Docs](https://gitbook.com/docs/publishing-documentation/llm-ready-docs)
- [Mintlify Documentation Platform](https://www.mintlify.com/)
- [Augment Code: Auto Documentation](https://www.augmentcode.com/learn/auto-document-your-code-tools-and-best-practices)

### LLM-First Development

- [Addy Osmani: LLM Coding Workflow 2026](https://addyosmani.com/blog/ai-coding-workflow/)
- [Simon Willison: 2025 Year in LLMs](https://simonwillison.net/2025/Dec/31/the-year-in-llms/)
- [The New Stack: Agentic Development 2026](https://thenewstack.io/5-key-trends-shaping-agentic-development-in-2026/)
- [MIT Tech Review: AI Coding Everywhere](https://www.technologyreview.com/2025/12/15/1128352/rise-of-ai-coding-developers-2026/)

### Platform Engineering

- [Roadie: Platform Engineering 2026](https://roadie.io/blog/platform-engineering-in-2026-why-diy-is-dead/)
- [Backstage vs IDPs Comparison](https://atmosly.com/knowledge/backstage-vs-internal-developer-portals-comparison-guide-2025)
- [CTO Magazine: Backstage at Scale](https://ctomagazine.com/backstage-platform-developer-experience/)
- [DX: Spotify Backstage Guide](https://getdx.com/blog/spotify-backstage/)

### Observability

- [OpenTelemetry: AI Agent Observability](https://opentelemetry.io/blog/2025/ai-agent-observability/)
- [The New Stack: OpenTelemetry in 2026](https://thenewstack.io/can-opentelemetry-save-observability-in-2026/)
- [CNCF: Observability Trends 2025](https://www.cncf.io/blog/2025/03/05/observability-trends-in-2025-whats-driving-change/)
- [Better Stack: OTel Best Practices](https://betterstack.com/community/guides/observability/opentelemetry-best-practices/)

---

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Writing specification templates | haiku | Form completion, mechanical setup |
| Reviewing specifications for clarity | sonnet | Language analysis, logical consistency |
| Architecting complex system specs | opus | Holistic design, novel combinations |

## Related Methodologies

| Methodology | Path |
|-------------|------|
| SDD Workflow Overview | [sdd-workflow-overview.md](../faion-sdd-planning/methodologies/sdd-workflow-overview.md) |
| Writing Specifications | [writing-specifications.md](../faion-sdd-planning/methodologies/writing-specifications.md) |
| Writing Design Documents | [writing-design-documents.md](../faion-sdd-planning/methodologies/writing-design-documents.md) |
| ADR Templates | [adr-template.md](../faion-software-architect/methodologies/adr-template.md) |
| Quality Gates | [quality-gates.md](../faion-sdd-execution/methodologies/quality-gates.md) |

---

*Reference Document | Key Trends Summary 2025-2026 | Version 2.0*
