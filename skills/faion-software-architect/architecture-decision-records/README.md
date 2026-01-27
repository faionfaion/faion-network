# Architecture Decision Records (ADRs)

Documenting significant architecture decisions with structured rationale.

## What is an ADR?

An **Architecture Decision Record (ADR)** is a short document capturing an important architecture decision:

| Element | Description |
|---------|-------------|
| **Context** | Why the decision was needed |
| **Decision** | What was decided |
| **Consequences** | Trade-offs and impacts |
| **Alternatives** | Options considered and rejected |

ADRs create an **architecture knowledge base** that preserves decision rationale for future team members, stakeholders, and auditors.

## Key Terminology

| Term | Definition |
|------|------------|
| **AD** | Architecture Decision - a single justified design choice |
| **ADR** | Architecture Decision Record - document capturing an AD |
| **ADL** | Architecture Decision Log - collection of all ADRs for a project |
| **ASR** | Architecturally Significant Requirement - requirement with measurable architecture impact |
| **AKM** | Architecture Knowledge Management - discipline of managing architecture knowledge |

## When to Write an ADR

### Triggers (Write ADR)

| Category | Examples |
|----------|----------|
| **Technology choices** | Programming language, framework, database, cloud provider |
| **Architecture style** | Monolith, microservices, serverless, event-driven |
| **Design patterns** | CQRS, Saga, Event Sourcing, API Gateway |
| **Third-party services** | Auth provider, payment gateway, monitoring tool |
| **Breaking changes** | API versioning, data migration, protocol change |
| **Security decisions** | Auth mechanism, encryption, compliance requirements |
| **Infrastructure** | Container orchestration, CI/CD pipeline, deployment strategy |
| **Integration patterns** | Sync vs async, REST vs gRPC, message broker selection |

### Skip ADR When

- Decision is **trivial** (minimal risk, self-contained, single developer)
- Already **covered elsewhere** (standards, policies, documentation)
- **Temporary** solution (workaround, PoC, experiment)
- **Not architecturally significant** (UI color, variable naming)

### Decision Rule

> "An ADR should be written whenever a decision of significant impact is made; it is up to each team to align on what defines significant impact."

## ADR Formats

### Michael Nygard Format (2011)

The original, minimalist ADR format. Best for teams starting with ADRs.

**Sections:** Title, Status, Context, Decision, Consequences

**Characteristics:**
- Simple and popular
- Fits agile environments
- Easy to adopt

### MADR 4.0 (Markdown Any Decision Records)

Extended format with structured options analysis. Best for complex decisions requiring trade-off documentation.

**Sections:** Title, Status, Context, Decision Drivers, Considered Options, Decision Outcome, Pros/Cons

**Characteristics:**
- Full and minimal templates available
- Annotated and bare variants
- Strong community support
- Default in Log4brains

### Y-Statements

Concise single-sentence format capturing decision rationale. Best for quick documentation and code annotations.

**Structure:**
```
In the context of [context],
facing [requirement],
we decided [decision]
and neglected [alternatives]
to achieve [benefits],
accepting that [drawbacks].
```

**Characteristics:**
- Extremely concise
- Good for code annotations (@YStatementJustification in Java)
- Can be verbose for complex decisions

### Comparison Matrix

| Format | Complexity | Best For | Adoption Effort |
|--------|------------|----------|-----------------|
| Nygard | Low | Simple decisions, teams starting with ADRs | Low |
| MADR | Medium | Complex decisions, options analysis | Medium |
| Y-Statement | Very Low | Quick capture, code annotations | Very Low |
| Tyree & Akerman | High | Enterprise, formal governance | High |

## ADR Lifecycle

```
Draft → Proposed → Accepted/Rejected → [Deprecated | Superseded]
                                              │
                                              └─→ Reference new ADR
```

### Status Definitions

| Status | Description | Mutability |
|--------|-------------|------------|
| **Draft** | Work in progress, not ready for review | Editable |
| **Proposed** | Ready for review and discussion | Editable |
| **Accepted** | Approved and in effect | Immutable |
| **Rejected** | Not approved, rationale preserved | Immutable |
| **Deprecated** | No longer relevant due to context change | Immutable |
| **Superseded** | Replaced by newer ADR | Immutable + Link to successor |

### Immutability Principle

After acceptance/rejection:
- **Never delete** ADRs
- **Never modify** accepted content
- **Create new ADR** to supersede
- **Add timestamps** to any clarifications

## ADR Storage

### Recommended Location

```
project/
├── docs/
│   └── adr/
│       ├── 0001-use-postgresql-for-database.md
│       ├── 0002-adopt-microservices-architecture.md
│       ├── 0003-implement-jwt-authentication.md
│       └── README.md  # ADR index
└── src/
```

### Naming Convention

```
NNNN-title-with-dashes.md
```

- **NNNN**: 4-digit sequential number (0001, 0002, ...)
- **title-with-dashes**: Lowercase, descriptive title
- **.md**: Markdown extension

### Multi-Repository Projects

For projects with multiple repositories:
1. **Main repository**: Store ADRs in primary repo
2. **Link in dependent repos**: Reference ADRs in README
3. **Consider**: Dedicated docs repository for large organizations

## ADR Tools

### CLI Tools

| Tool | Language | Key Features |
|------|----------|--------------|
| **adr-tools** | Bash | Create, list, link, supersede ADRs |
| **adr-tools-python** | Python | Python port of adr-tools |
| **pyadr** | Python | ADR management with lifecycle support |
| **ADR Manager** | Node.js | VS Code extension |

### Documentation Generators

| Tool | Features |
|------|----------|
| **Log4brains** | CLI + static site generator, hot reload, CI/CD integration |
| **adr-viewer** | Static site generator for ADRs |
| **adr-log** | Generate TOC/index of ADRs |

### Log4brains Quick Start

```bash
# Install
npm install -g log4brains

# Initialize in project
log4brains init

# Create new ADR
log4brains adr new "Use PostgreSQL for database"

# Preview locally
log4brains preview

# Build static site
log4brains build
```

### adr-tools Quick Start

```bash
# Install (macOS)
brew install adr-tools

# Initialize
adr init docs/adr

# Create new ADR
adr new "Use PostgreSQL for database"

# Supersede ADR
adr new -s 3 "Use CockroachDB instead of PostgreSQL"

# Generate TOC
adr generate toc > docs/adr/README.md
```

## Best Practices

### Writing Quality ADRs

| Practice | Description |
|----------|-------------|
| **Keep it short** | 1-2 pages maximum |
| **Write when deciding** | Not after the fact |
| **Include context** | Future readers need background |
| **Document alternatives** | Show due diligence |
| **Accept trade-offs** | No perfect solutions exist |
| **Version control** | Store in repo with code |
| **Review like code** | PR-based approval process |
| **Never delete** | Supersede instead |

### Team Adoption

1. **Start small**: Document next 3-5 decisions
2. **Create template**: Customize for your team
3. **Include in DoD**: "Is there an ADR for this?"
4. **Regular reviews**: Monthly ADR review meetings
5. **Onboarding material**: ADRs as architecture documentation

### Governance Questions

| Question | Options |
|----------|---------|
| Who can propose ADRs? | Anyone / Senior engineers / Architects only |
| Who approves ADRs? | Team lead / Architecture board / Consensus |
| What threshold? | All decisions / Only cross-team / Only significant |
| Review process? | PR review / Meeting / Async approval |

## LLM-Assisted ADR Writing

### When to Use LLM

| Task | LLM Suitability |
|------|-----------------|
| Draft initial ADR from notes | Excellent |
| Research alternatives | Good |
| Identify consequences | Good |
| Format and structure | Excellent |
| Review for completeness | Good |
| Final decision | Human only |

### LLM Tips

1. **Provide context**: Include project constraints, team skills, existing stack
2. **Specify format**: Reference Nygard/MADR template explicitly
3. **Request alternatives**: Ask for 3-5 options with pros/cons
4. **Iterate**: Refine draft through conversation
5. **Human review**: Always validate technical accuracy

### Effective Prompts

See [llm-prompts.md](llm-prompts.md) for detailed prompts.

## Integration with Development Workflow

### Git Workflow

```
1. Create branch: feature/adr-xxx-description
2. Write ADR draft (status: Proposed)
3. Open PR for review
4. Discussion in PR comments
5. Update based on feedback
6. Merge when approved (status: Accepted)
```

### CI/CD Integration

```yaml
# Example: Validate ADRs in CI
- name: Validate ADR format
  run: |
    for file in docs/adr/*.md; do
      # Check required sections exist
      grep -q "## Status" "$file" || exit 1
      grep -q "## Context" "$file" || exit 1
      grep -q "## Decision" "$file" || exit 1
    done
```

### Architecture Review Meetings

1. Review proposed ADRs
2. Discuss open questions
3. Decide: accept, reject, or request changes
4. Update ADR status
5. Communicate decision to team

## Related Resources

### Files in This Folder

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Step-by-step ADR writing checklist |
| [examples.md](examples.md) | Real-world ADR examples |
| [templates.md](templates.md) | Copy-paste ADR templates |
| [llm-prompts.md](llm-prompts.md) | Prompts for LLM-assisted ADR writing |

### External Links

| Resource | URL |
|----------|-----|
| ADR GitHub Organization | https://adr.github.io/ |
| MADR Project | https://adr.github.io/madr/ |
| Joel Parker Henderson's ADR Examples | https://github.com/joelparkerhenderson/architecture-decision-record |
| Log4brains | https://github.com/thomvaill/log4brains |
| adr-tools | https://github.com/npryce/adr-tools |
| Michael Nygard's Original Post | https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions |
| Spotify: When to Write ADR | https://engineering.spotify.com/2020/04/when-should-i-write-an-architecture-decision-record |
| AWS ADR Guidance | https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/ |
| Google Cloud ADR Overview | https://cloud.google.com/architecture/architecture-decision-records |
| Microsoft Azure ADR Guide | https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record |

### Related Methodologies

| Methodology | Relationship |
|-------------|--------------|
| [trade-off-analysis/](../trade-off-analysis/) | Evaluating options for ADR |
| [quality-attributes/](../quality-attributes/) | NFR context for decisions |
| [system-design-process/](../system-design-process/) | When ADRs are created |
| [c4-model/](../c4-model/) | Visualizing architecture in ADRs |
