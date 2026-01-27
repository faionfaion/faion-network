# Architecture Workflows

Structured processes for architecture design, review, assessment, and documentation. This guide covers practical workflows used by architects in 2025-2026.

## Overview

Architecture workflows provide repeatable processes for:

- **System Design** - Structured approach to designing new systems
- **Architecture Review** - Evaluating existing or proposed architectures
- **ADR Creation** - Documenting and managing architectural decisions
- **Technology Evaluation** - Selecting technologies systematically
- **Architecture Assessment** - Quality attributes analysis (ATAM/CBAM)
- **Migration Planning** - Modernizing legacy systems incrementally
- **Design Document Review** - Reviewing technical designs

## Workflow Categories

### 1. System Design Workflow

End-to-end process for designing new systems, commonly used in interviews and real projects.

```
CLARIFY → ESTIMATE → DESIGN → DEEP DIVE → TRADE-OFFS → DOCUMENT
```

**Key Activities:**
- Requirements clarification (functional + non-functional)
- Scale estimation (users, data, traffic)
- High-level design (C4 diagrams, API contracts)
- Component deep dive (database, caching, queues)
- Quality attributes (scalability, reliability, security)
- Decision documentation (ADRs)

### 2. Architecture Review Workflow

Two types of reviews serve different purposes:

| Type | Purpose | Timing |
|------|---------|--------|
| **Roadmap Review** | Decide if something should be done | Early planning |
| **Design Review** | Evaluate how something will be built | Before implementation |

**Review Techniques:**
- Risk-storming (identify failure points)
- ATAM (quality attribute trade-offs)
- Design critique (peer review)
- Security review (threat modeling)

### 3. ADR Workflow

Architecture Decision Records document significant decisions using async, Git-based processes.

```
IDENTIFY → DRAFT → REVIEW → DECIDE → MAINTAIN
```

**Lifecycle States:**
- `proposed` - Under discussion
- `accepted` - Approved and active
- `deprecated` - No longer recommended
- `superseded` - Replaced by another ADR

**Best Practices (2025):**
- Treat ADRs like code (versioned, reviewed, PRs)
- Keep focused on single decision
- Use readout meetings (10-15 min reading, 30-45 min total)
- Push for timely decisions (1-3 readouts max)
- Conduct after-action reviews (30 days later)

### 4. Technology Evaluation Workflow

Structured approach to technology selection with AI acceleration.

```
DEFINE CRITERIA → RESEARCH → EVALUATE → DECIDE → DOCUMENT
```

**Evaluation Framework:**
- SWOT analysis (Strengths, Weaknesses, Opportunities, Threats)
- PEST analysis (Political, Economic, Social, Technological)
- Weighted scoring matrix
- Proof of concept validation

**2025 Enhancement:**
AI can compress research time, cluster vendors, draft evidence packs, and benchmark against standards.

### 5. Architecture Assessment Workflow (ATAM/CBAM)

Formal evaluation methods from SEI Carnegie Mellon.

**ATAM (Architecture Tradeoff Analysis Method):**
1. Present business drivers
2. Present architecture
3. Identify architectural approaches
4. Generate quality attribute utility tree
5. Analyze architectural approaches
6. Brainstorm and prioritize scenarios
7. Analyze architectural approaches (refined)
8. Present results

**CBAM (Cost Benefit Analysis Method):**
Extends ATAM with economic analysis:
- Cost estimation for each decision
- Benefit quantification
- ROI calculation
- Risk-adjusted returns

**Key Outputs:**
- Sensitivity points (decisions with significant impact)
- Trade-off points (conflicts between quality attributes)
- Risk themes (patterns of architectural risk)

### 6. Migration Planning Workflow

Strangler Fig pattern for incremental modernization.

```
IDENTIFY → ISOLATE → ROUTE → TEST → ITERATE
```

**Steps:**
1. **Identify** - Select component for migration
2. **Isolate** - Implement in new platform
3. **Route** - Use API gateway/proxy to redirect traffic
4. **Test** - Canary releases, A/B testing, monitoring
5. **Iterate** - Repeat for each component

**2025 Trends:**
- Event-Driven Strangling (Kafka CDC)
- AI-Assisted code analysis
- Feature flags for gradual rollout
- Real-time data sync during migration

### 7. Design Document Review Workflow

Sprint-integrated review process.

```
IDENTIFY → PREPARE → REVIEW → FEEDBACK → APPROVE
```

**Integration Points:**
- Sprint planning: identify architecturally significant work
- PR process: ADRs reviewed alongside code
- CI/CD gates: automated architecture validation

## Decision Trees

### When to Use Each Workflow

```
New system?
├── Yes → System Design Workflow
│         ├── Complex/large → Include ATAM
│         └── Simple → Lightweight design
└── No
    ├── Evaluating existing?
    │   ├── Yes → Architecture Review Workflow
    │   │         ├── Quality focus → ATAM
    │   │         └── Cost focus → CBAM
    │   └── No
    │       ├── Making decision?
    │       │   ├── Technology → Technology Evaluation Workflow
    │       │   └── Architecture → ADR Workflow
    │       └── Legacy modernization?
    │           └── Yes → Migration Planning Workflow
```

### Review Type Selection

```
What's the goal?
├── Should we build this? → Roadmap Review
├── Is this design good? → Design Review
├── What are the risks? → Risk-storming
├── Quality trade-offs? → ATAM
└── Cost/benefit? → CBAM
```

## LLM-Assisted Workflows

### How LLMs Enhance Architecture Work (2025-2026)

| Activity | LLM Contribution |
|----------|------------------|
| Requirements analysis | Extract and categorize requirements from stakeholder input |
| Scale estimation | Calculate capacity needs from business metrics |
| Design generation | Generate initial architecture options with trade-offs |
| ADR writing | Draft ADRs from meeting notes or decisions |
| Technology research | Summarize vendor comparisons, benchmark data |
| Risk identification | Brainstorm failure modes and edge cases |
| Diagram creation | Generate C4, sequence, and component diagrams |
| Review facilitation | Prepare questions for design reviews |

### Effective LLM Usage Patterns

**1. Structured Input**
Provide clear context: business goals, constraints, quality priorities.

**2. Iterative Refinement**
Start with high-level design, then deep dive into specific components.

**3. Trade-off Exploration**
Ask LLM to compare alternatives with explicit criteria.

**4. Documentation Generation**
Use LLM to draft ADRs, design docs, and diagrams from decisions.

**5. Review Preparation**
Generate checklists and review questions for specific architecture types.

### Current Adoption (2025 Survey)

- 37% use AI in some workflows
- 33% are exploring
- 19% haven't started yet
- Main uses: diagram generation, docs creation, design validation

## CI/CD Integration

### Quality Gates for Architecture

```yaml
# Pre-commit: Architectural patterns
- naming conventions
- file organization
- import restrictions

# PR: Static analysis
- SonarQube (code smells, anti-patterns)
- Dependency analysis
- Security scanning

# Build: Architecture validation
- ArchUnit tests
- Dependency rules
- API contract validation
```

## Common Challenges (2025 Survey)

| Challenge | Frequency |
|-----------|-----------|
| Keeping documentation up to date | #1 |
| Lack of standards | #2 |
| Finding right level of detail | #3 |
| Getting stakeholder buy-in | #4 |
| Balancing speed and rigor | #5 |

## External Resources

### Official Documentation

- [AWS ADR Process](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html)
- [Microsoft ADR Guidance](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record)
- [Azure Strangler Fig Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/strangler-fig)
- [SEI ATAM](https://resources.sei.cmu.edu/library/asset-view.cfm?assetid=629)

### Community Resources

- [ADR GitHub Organization](https://adr.github.io/)
- [Joel Parker Henderson ADR Examples](https://github.com/joelparkerhenderson/architecture-decision-record)
- [C4 Model](https://c4model.com/)
- [Structurizr](https://structurizr.com/)

### Books and Guides

- "Software Architecture: The Hard Parts" (Ford, Richards, et al.)
- "Fundamentals of Software Architecture" (Richards, Ford)
- "Design It!" (Keeling)
- "Building Evolutionary Architectures" (Ford, Parsons, Kua)

### Tools

| Category | Tools |
|----------|-------|
| ADR Management | Log4brains, dotnet-adr, adr-tools |
| Diagramming | Structurizr, PlantUML, Mermaid, C4-PlantUML |
| Documentation | Confluence, Notion, GitHub Wiki, GitBook |
| Analysis | SonarQube, ArchUnit, Dependency-Track |

## Related Files

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Step-by-step workflow checklists |
| [examples.md](examples.md) | Real workflow examples |
| [templates.md](templates.md) | Copy-paste templates |
| [llm-prompts.md](llm-prompts.md) | Effective prompts for LLM-assisted workflows |

---

*Part of faion-software-architect skill*
