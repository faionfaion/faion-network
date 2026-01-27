# Trade-off Analysis

Framework for evaluating and documenting architecture trade-offs using structured decision-making methods.

> "There are no solutions, only trade-offs." - Thomas Sowell

## Overview

Trade-off analysis is the systematic process of evaluating competing alternatives in architecture decisions. Every architecture choice involves sacrificing one quality to gain another. The goal is to make **informed** trade-offs aligned with business priorities.

## Why Trade-off Analysis Matters

| Problem | Impact |
|---------|--------|
| Decisions made without analysis | 67% of failed software implementations stem from incorrect build vs. buy decisions (Forrester 2024) |
| Undocumented trade-offs | Teams revisit settled debates ("decision amnesia") |
| Poor stakeholder communication | Misaligned expectations, resistance to change |
| Ignored quality attributes | Systems fail to meet NFRs in production |

Organizations using structured decision frameworks report **25-35% better outcomes** from software investments.

## Core Methods

### ATAM (Architecture Tradeoff Analysis Method)

Industry-standard method developed by SEI/Carnegie Mellon for evaluating architectures against quality attributes.

**Key outputs:**
- Sensitivity points (affect single quality attribute)
- Trade-off points (affect multiple quality attributes)
- Risks and non-risks
- Risk themes

**When to use:** Major architecture decisions, system redesigns, technology migrations.

**Typical duration:** 3-4 days with full stakeholder participation.

### ATRAF (Architecture Tradeoff and Risk Analysis Framework)

Published May 2025, extends ATAM for evaluating reference architectures and architectural frameworks.

**Three methods:**
- ATRAM: Enhanced risk identification for concrete systems
- RATRAM: Reference architecture evaluation
- AFTRAM: Architectural framework evaluation

### Lightweight Alternatives

| Method | Duration | Best For |
|--------|----------|----------|
| Decision Matrix | 1-2 hours | Technology selection, vendor comparison |
| Mini-ATAM | Half day | Sprint-level decisions |
| Tiny Architectural Review (TARA) | 2-4 hours | Focused quality attribute analysis |
| LAAAM | 1 day | Iterative architecture evaluation |

## Quality Attributes in Trade-offs

Quality attributes often conflict. Improving one typically degrades another.

### Common Conflicts

| Improving | Often Degrades |
|-----------|----------------|
| Performance | Maintainability, Portability |
| Security | Usability, Performance |
| Availability | Consistency, Cost |
| Flexibility | Performance, Simplicity |
| Scalability | Consistency, Cost |

### ISO 25010 Quality Model

```
Product Quality
├── Functional Suitability
├── Performance Efficiency (time, resources, capacity)
├── Compatibility (co-existence, interoperability)
├── Usability (learnability, operability, accessibility)
├── Reliability (availability, fault tolerance, recoverability)
├── Security (confidentiality, integrity, authenticity)
├── Maintainability (modularity, reusability, testability)
└── Portability (adaptability, installability, replaceability)
```

## Common Trade-off Categories

### 1. Architecture Style Trade-offs

| Decision | Get | Lose |
|----------|-----|------|
| Monolith | Simplicity, debugging ease | Independent scaling |
| Modular Monolith | Boundary clarity, simpler ops | Deployment independence |
| Microservices | Scale, team autonomy | Complexity, latency |
| Serverless | No ops, auto-scale | Cold starts, vendor lock-in |

### 2. Data Trade-offs (CAP Theorem)

| Choice | Get | Lose |
|--------|-----|------|
| CP (Consistency + Partition) | Correctness | Availability during partitions |
| AP (Availability + Partition) | Always available | Immediate consistency |
| CA (Consistency + Availability) | Both (single node only) | Partition tolerance |

### 3. Build vs Buy

| Choice | Get | Lose |
|--------|-----|------|
| Build | Customization, control, IP | Time, maintenance burden |
| Buy | Speed, proven solution | Flexibility, vendor lock-in |
| Hybrid | Best of both | Integration complexity |

**Key insight:** Organizations with proprietary core technology see ~2x stronger revenue growth (Deloitte 2025).

### 4. Technical Debt vs Speed

| Choice | Get | Lose |
|--------|-----|------|
| Ship fast (accept debt) | Time to market, feedback | Future velocity, maintenance cost |
| Build clean | Sustainable velocity | Immediate speed |
| Balanced (15-20% debt budget) | Both (moderate) | Neither maximized |

**Martin Fowler's Technical Debt Quadrant:**

```
                    Reckless              Prudent
                ┌─────────────────┬─────────────────┐
  Deliberate    │ "We don't have  │ "We must ship   │
                │ time for design"│ now, deal later"│
                ├─────────────────┼─────────────────┤
  Inadvertent   │ "What's         │ "Now we know    │
                │ layering?"      │ better approach"│
                └─────────────────┴─────────────────┘
```

### 5. Communication Pattern Trade-offs

| Pattern | Get | Lose |
|---------|-----|------|
| Synchronous | Simplicity, immediate response | Coupling, blocking |
| Asynchronous | Decoupling, resilience | Complexity, debugging |
| Event-driven | Loose coupling, extensibility | Eventual consistency |

## Decision-Making Framework

### Quick Decision Tree

```
For each option, answer:

1. What problem does it solve?
2. What new problems does it create?
3. What is the cost of being wrong?
4. Is this decision reversible?

High cost + Irreversible → Invest more in analysis
Low cost + Reversible → Decide fast, iterate
```

### Reversibility Classification

| Type | Examples | Analysis Depth |
|------|----------|----------------|
| Type 1 (Irreversible) | Database choice, cloud provider, core language | Deep analysis, ATAM |
| Type 2 (Reversible) | Library choice, API design, caching strategy | Quick analysis, iterate |

## Anti-patterns to Avoid

| Anti-pattern | Description | Mitigation |
|--------------|-------------|------------|
| Resume-Driven Development | Choosing tech for CV, not fit | Focus on problem-solution fit |
| Premature Optimization | Optimizing before proving bottleneck | Profile first, optimize proven hot spots |
| Analysis Paralysis | Over-analyzing instead of deciding | Set decision deadlines, use Type 1/2 |
| Cargo Culting | Copying big companies without context | Understand your constraints first |
| Hidden Trade-offs | Not documenting sacrifices | Explicit trade-off section in ADRs |
| Stakeholder Surprise | Trade-offs discovered in production | Early stakeholder involvement |

## Documentation Requirements

Every significant trade-off decision should be documented with:

1. **Context**: What prompted this decision?
2. **Options evaluated**: All alternatives considered
3. **Criteria and weights**: How options were scored
4. **Trade-offs identified**: What we gain/lose with chosen option
5. **Risks and mitigations**: How we address downsides
6. **Decision rationale**: Why this option despite trade-offs

## Stakeholder Communication

### By Audience

| Stakeholder | Focus On | Avoid |
|-------------|----------|-------|
| Executives | Business impact, cost, risk | Technical details |
| Product | User impact, timeline | Implementation complexity |
| Engineering | Technical trade-offs, implementation | Business justification |
| Operations | Operational impact, SLAs | Feature details |

### Communication Tactics

1. **Visual representations** for non-technical stakeholders
2. **Business terms** (cost, risk, timeline) over technical terms
3. **Decision matrices** to show objective comparison
4. **Risk heat maps** for severity communication
5. **ADR readout meetings** (10-15 min read, then discuss)

## Files in This Folder

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Step-by-step trade-off analysis process |
| [examples.md](examples.md) | Real-world trade-off analysis examples |
| [templates.md](templates.md) | Copy-paste templates for analysis |
| [llm-prompts.md](llm-prompts.md) | Effective prompts for LLM-assisted analysis |

## LLM Usage Tips

### When to Use LLM for Trade-off Analysis

| Use Case | LLM Effectiveness |
|----------|-------------------|
| Generating option alternatives | High |
| Identifying quality attribute impacts | High |
| Structuring decision matrices | High |
| Generating scenarios for ATAM | High |
| Domain-specific risk identification | Medium (needs context) |
| Stakeholder-specific communication | Medium |
| Final decision making | Low (human judgment needed) |

### Best Practices

1. **Provide full context**: Business constraints, team capabilities, existing systems
2. **Ask for trade-offs explicitly**: "What do we lose by choosing X?"
3. **Request multiple perspectives**: Technical, business, operational
4. **Validate with domain experts**: LLM suggestions need human verification
5. **Use iterative refinement**: Start broad, narrow down options

### Prompt Patterns

```
"Analyze trade-offs between [Option A] and [Option B] for [context].
Consider: performance, maintainability, cost, team expertise.
Format as decision matrix with weighted scores."
```

## Related Methodologies

| Methodology | Location |
|-------------|----------|
| Architecture Decision Records | [architecture-decision-records.md](../architecture-decision-records.md) |
| Quality Attributes | [quality-attributes/](../quality-attributes/) |
| System Design Process | [system-design-process/](../system-design-process/) |
| Database Selection | [database-selection/](../database-selection/) |

## External Resources

- [SEI ATAM Collection](https://www.sei.cmu.edu/library/architecture-tradeoff-analysis-method-collection/) - Original ATAM documentation
- [ATAM Wikipedia](https://en.wikipedia.org/wiki/Architecture_tradeoff_analysis_method) - Overview and history
- [ADR GitHub Repository](https://github.com/joelparkerhenderson/architecture-decision-record) - ADR templates and examples
- [AWS ADR Best Practices](https://aws.amazon.com/blogs/architecture/master-architecture-decision-records-adrs-best-practices-for-effective-decision-making/) - Enterprise ADR guidance
- [ISO 25010](https://iso25000.com/index.php/en/iso-25000-standards/iso-25010) - Quality model standard

## References

- Kazman, R., Klein, M., Clements, P. (2000). ATAM: Method for Architecture Evaluation. SEI.
- Fowler, M. (2009). Technical Debt Quadrant.
- Hassouna et al. (2025). ATRAF: Architecture Tradeoff and Risk Analysis Framework.
- Forrester (2024). Software Development Trends Report.
- Deloitte (2025). Technology Investment Analysis.
