# Trade-off Analysis

Framework for evaluating architecture trade-offs.

## Core Principle

> "There are no solutions, only trade-offs." - Thomas Sowell

Every architecture decision involves trade-offs. The goal is to make **informed** trade-offs aligned with business priorities.

## Trade-off Analysis Process

```
1. IDENTIFY OPTIONS
   └─ List viable alternatives

2. DEFINE CRITERIA
   └─ Quality attributes, constraints, costs

3. EVALUATE OPTIONS
   └─ Score each option against criteria

4. ANALYZE TRADE-OFFS
   └─ What do we gain/lose with each option

5. DECIDE & DOCUMENT
   └─ Choose option, write ADR
```

## Common Architecture Trade-offs

### Consistency vs Availability (CAP)

| Choice | Get | Lose |
|--------|-----|------|
| Strong consistency | Correctness | Availability during partitions |
| Eventual consistency | Availability | Immediate accuracy |

**When to choose:**
- Banking: Strong consistency
- Social media: Eventual consistency

### Performance vs Maintainability

| Choice | Get | Lose |
|--------|-----|------|
| Optimized code | Speed | Readability |
| Clean code | Maintainability | Some performance |

**Guideline:** Start clean, optimize bottlenecks.

### Monolith vs Microservices

| Choice | Get | Lose |
|--------|-----|------|
| Monolith | Simplicity, easy debugging | Independent scaling |
| Microservices | Scalability, team autonomy | Complexity, latency |

**When to choose:**
- Small team, MVP: Monolith
- Large team, clear domains: Microservices

### Build vs Buy

| Choice | Get | Lose |
|--------|-----|------|
| Build | Customization, control | Time, maintenance burden |
| Buy | Speed, proven solution | Flexibility, vendor lock-in |

### SQL vs NoSQL

| Choice | Get | Lose |
|--------|-----|------|
| SQL | ACID, joins, mature | Horizontal scaling complexity |
| NoSQL | Scale, flexibility | Consistency, query power |

### Sync vs Async

| Choice | Get | Lose |
|--------|-----|------|
| Synchronous | Simplicity, immediate response | Coupling, blocking |
| Asynchronous | Decoupling, resilience | Complexity, debugging difficulty |

## Decision Matrix

Template for comparing options:

| Criteria | Weight | Option A | Option B | Option C |
|----------|--------|----------|----------|----------|
| Performance | 5 | 4 (20) | 3 (15) | 5 (25) |
| Cost | 4 | 3 (12) | 5 (20) | 2 (8) |
| Maintainability | 3 | 5 (15) | 3 (9) | 4 (12) |
| Time to market | 4 | 2 (8) | 5 (20) | 3 (12) |
| **Total** | | **55** | **64** | **57** |

**Scoring:** 1-5 (1=poor, 5=excellent)
**Weighted Score:** Score × Weight

## ATAM (Architecture Trade-off Analysis Method)

Structured approach for evaluating architectures:

1. **Present Architecture**
   - Business drivers
   - Architecture approach

2. **Identify Scenarios**
   - Use case scenarios
   - Growth scenarios
   - Failure scenarios

3. **Analyze Against Scenarios**
   - How does architecture handle each?

4. **Identify Sensitivity Points**
   - What affects multiple attributes?

5. **Identify Trade-offs**
   - Where does improving one hurt another?

6. **Document Risks**
   - What could go wrong?

## Quick Decision Framework

```
For each option, answer:

1. What problem does it solve?
2. What new problems does it create?
3. What is the cost of being wrong?
4. Is this reversible?

If high cost of being wrong + irreversible → Invest more in analysis
If low cost + reversible → Decide fast, iterate
```

## Anti-patterns

### Resume-Driven Development
Choosing tech because it looks good on resume, not because it fits.

### Premature Optimization
Optimizing before proving it's a bottleneck.

### Analysis Paralysis
Over-analyzing instead of deciding.

### Cargo Culting
Copying what big companies do without understanding context.

## Documentation Template

```markdown
## Trade-off Analysis: [Decision]

### Options
1. Option A: [description]
2. Option B: [description]

### Criteria
- Criterion 1 (weight: X)
- Criterion 2 (weight: Y)

### Evaluation
[Decision matrix]

### Trade-offs
| Choosing Option A means... |
|----------------------------|
| ✅ We gain: [benefit] |
| ❌ We lose: [sacrifice] |

### Recommendation
[Chosen option with justification]

### Risks & Mitigations
| Risk | Mitigation |
|------|------------|
| [risk] | [mitigation] |
```

## Related

- [architecture-decision-records.md](architecture-decision-records.md) - Document decisions
- [quality-attributes-analysis.md](quality-attributes-analysis.md) - Criteria context
