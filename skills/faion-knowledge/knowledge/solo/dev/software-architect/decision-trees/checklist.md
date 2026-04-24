# Architecture Decision Checklist

Step-by-step checklist for making architecture decisions systematically. Use this checklist for any significant architecture choice.

## Quick Reference

**Decision Complexity Levels:**
| Level | Time | Stakeholders | Documentation |
|-------|------|--------------|---------------|
| Low | 1-2 hours | 1-2 people | Lightweight ADR |
| Medium | 1-2 days | 3-5 people | Standard ADR |
| High | 1-2 weeks | 5+ people | Full ADR + POC |

---

## Phase 1: Problem Definition

### 1.1 Identify the Decision

- [ ] **State the decision clearly**
  - What exactly needs to be decided?
  - What triggers this decision? (new feature, scaling issue, tech debt)
  - Is this reversible or irreversible?

- [ ] **Define scope boundaries**
  - What is in scope for this decision?
  - What is explicitly out of scope?
  - What dependencies exist?

- [ ] **Determine decision urgency**
  - When must the decision be made?
  - What happens if delayed?
  - Can it be staged/incremental?

### 1.2 Gather Context

- [ ] **Business context**
  - What business problem does this solve?
  - Who are the stakeholders?
  - What is the budget/timeline?

- [ ] **Technical context**
  - Current architecture state
  - Existing constraints (legacy systems, contracts)
  - Team skills and capacity

- [ ] **Requirements context**
  - Functional requirements affected
  - Non-functional requirements (performance, security, scalability)
  - Compliance/regulatory requirements

---

## Phase 2: Options Generation

### 2.1 Identify Options

- [ ] **Brainstorm all viable options**
  - Include "do nothing" as an option
  - Include unconventional approaches
  - Don't filter prematurely

- [ ] **Research each option**
  - Industry adoption and maturity
  - Vendor/community support
  - Known limitations

- [ ] **Eliminate clearly unsuitable options**
  - Document why eliminated
  - Keep 2-5 viable options for analysis

### 2.2 Option Documentation

For each remaining option, document:

- [ ] **Description** - What is this option?
- [ ] **Pros** - Benefits and advantages
- [ ] **Cons** - Drawbacks and risks
- [ ] **Fit** - How well it meets requirements
- [ ] **Cost** - Initial and ongoing (TCO)
- [ ] **Complexity** - Implementation difficulty

---

## Phase 3: Trade-off Analysis

### 3.1 Define Evaluation Criteria

- [ ] **List all criteria relevant to the decision**

  Common criteria:
  - [ ] Performance (latency, throughput)
  - [ ] Scalability (horizontal, vertical)
  - [ ] Reliability (uptime, fault tolerance)
  - [ ] Security (compliance, data protection)
  - [ ] Maintainability (complexity, documentation)
  - [ ] Cost (initial, operational, migration)
  - [ ] Time to implement
  - [ ] Team expertise
  - [ ] Vendor lock-in risk
  - [ ] Integration with existing systems

- [ ] **Assign weights to criteria**
  - Total should equal 100%
  - Involve stakeholders in weighting
  - Document rationale for weights

### 3.2 Score Options

- [ ] **Create decision matrix**

  | Criteria | Weight | Option A | Option B | Option C |
  |----------|--------|----------|----------|----------|
  | Performance | 20% | 4 | 3 | 5 |
  | Cost | 25% | 3 | 5 | 2 |
  | ... | ... | ... | ... | ... |
  | **Weighted Total** | 100% | **3.4** | **3.8** | **3.1** |

- [ ] **Validate scores**
  - Are scores evidence-based?
  - Did multiple people review?
  - Are edge cases considered?

### 3.3 Analyze Trade-offs

- [ ] **Identify conflicts**
  - Which criteria conflict? (e.g., cost vs performance)
  - What compromises are acceptable?

- [ ] **Consider risks**
  - What could go wrong with each option?
  - What is the mitigation strategy?
  - What is the rollback plan?

- [ ] **Evaluate long-term implications**
  - How does this affect future architecture?
  - Does this create technical debt?
  - Is this a one-way door or two-way door decision?

---

## Phase 4: Validation

### 4.1 Technical Validation

- [ ] **Proof of Concept (for high-impact decisions)**
  - Define POC scope and success criteria
  - Time-box the POC (typically 1-2 weeks)
  - Test critical integration points
  - Measure actual performance

- [ ] **Architecture review**
  - Does this align with architecture principles?
  - Does this introduce new patterns?
  - Are there security implications?

### 4.2 Stakeholder Validation

- [ ] **Present to stakeholders**
  - Explain the decision and rationale
  - Show the trade-offs considered
  - Address concerns

- [ ] **Gather feedback**
  - Are there perspectives missed?
  - Are there additional constraints?
  - Is there consensus?

- [ ] **Address objections**
  - Document all objections
  - Explain how addressed or why not
  - Update decision if needed

---

## Phase 5: Documentation

### 5.1 Create ADR

- [ ] **Title** - Short, descriptive title
- [ ] **Status** - Proposed, Accepted, Deprecated, Superseded
- [ ] **Context** - Why is this decision needed?
- [ ] **Decision** - What was decided?
- [ ] **Consequences** - What are the implications?
- [ ] **Alternatives** - What options were considered?

See [templates.md](templates.md) for ADR templates.

### 5.2 Communicate Decision

- [ ] **Notify affected teams**
- [ ] **Update architecture diagrams**
- [ ] **Create implementation tickets**
- [ ] **Schedule knowledge sharing**

---

## Phase 6: Implementation Planning

### 6.1 Migration Strategy (if applicable)

- [ ] **Choose migration approach**
  - Big bang vs incremental
  - Strangler fig pattern
  - Feature flags

- [ ] **Define rollback plan**
  - At what point do we rollback?
  - How do we rollback?
  - What data migration is needed?

### 6.2 Success Criteria

- [ ] **Define measurable outcomes**
  - Performance targets
  - Cost targets
  - Timeline milestones

- [ ] **Plan for monitoring**
  - What metrics to track?
  - What alerts to set?
  - When to review?

---

## Quick Checklists by Decision Type

### Architecture Style Decision

- [ ] Assessed team size and structure
- [ ] Evaluated DevOps maturity
- [ ] Considered deployment frequency needs
- [ ] Analyzed data consistency requirements
- [ ] Reviewed scaling requirements
- [ ] Checked bounded context clarity

### Technology/Framework Selection

- [ ] Matched to team expertise
- [ ] Verified ecosystem maturity
- [ ] Checked license compatibility
- [ ] Evaluated community support
- [ ] Tested performance requirements
- [ ] Assessed learning curve

### Database Selection

- [ ] Identified primary access patterns
- [ ] Determined consistency requirements (CAP)
- [ ] Estimated data volume and growth
- [ ] Checked query complexity needs
- [ ] Evaluated operational complexity
- [ ] Considered backup/recovery requirements

### Cloud Provider Selection

- [ ] Assessed existing technology investments
- [ ] Evaluated regional availability needs
- [ ] Compared pricing models
- [ ] Checked compliance certifications
- [ ] Reviewed hybrid cloud requirements
- [ ] Analyzed vendor lock-in risks

### Build vs Buy Decision

- [ ] Determined strategic importance
- [ ] Calculated total cost of ownership (3-5 years)
- [ ] Evaluated time to value
- [ ] Assessed integration complexity
- [ ] Reviewed team capability
- [ ] Considered vendor dependency risks

---

## Decision Review Schedule

| Decision Impact | Review Frequency |
|-----------------|------------------|
| High (architecture style, cloud provider) | Annually |
| Medium (frameworks, databases) | 18 months |
| Low (libraries, tools) | As needed |

### Review Checklist

- [ ] Is the original context still valid?
- [ ] Have requirements changed?
- [ ] Have better options emerged?
- [ ] Is the decision delivering expected outcomes?
- [ ] Should this decision be revisited?

---

## Anti-Patterns to Avoid

### Decision Anti-Patterns

- [ ] **Analysis Paralysis** - Taking too long to decide
  - Set decision deadlines
  - Accept "good enough" for reversible decisions

- [ ] **Highest Paid Person's Opinion (HiPPO)** - Deferring to authority
  - Use data and criteria, not hierarchy
  - Document dissenting opinions

- [ ] **Resume-Driven Development** - Choosing for personal benefit
  - Focus on business needs
  - Document why technology fits the problem

- [ ] **Cargo Culting** - Copying without understanding
  - Understand why others chose this
  - Validate it fits your context

- [ ] **Shiny Object Syndrome** - Chasing new technology
  - Evaluate maturity and stability
  - Consider long-term support

### Process Anti-Patterns

- [ ] **Undocumented Decisions** - Losing institutional knowledge
  - Always write an ADR
  - Store in version control

- [ ] **Premature Optimization** - Solving problems you don't have
  - Start simple
  - Optimize when data supports it

- [ ] **One-Size-Fits-All** - Applying same solution everywhere
  - Evaluate each case individually
  - Different contexts need different solutions

---

## Checklist Template

Copy this for each decision:

```markdown
## Decision: [Title]

**Date:** YYYY-MM-DD
**Status:** In Progress / Complete
**Impact:** Low / Medium / High

### Phase 1: Problem Definition
- [ ] Decision stated clearly
- [ ] Scope defined
- [ ] Context gathered

### Phase 2: Options
- [ ] Options identified
- [ ] Options researched
- [ ] Options documented

### Phase 3: Analysis
- [ ] Criteria defined and weighted
- [ ] Options scored
- [ ] Trade-offs analyzed

### Phase 4: Validation
- [ ] Technical validation (POC if needed)
- [ ] Stakeholder review
- [ ] Objections addressed

### Phase 5: Documentation
- [ ] ADR created
- [ ] Decision communicated
- [ ] Implementation planned

### Notes
[Any additional notes]
```

---

*Architecture Decision Checklist v2.0 - Updated January 2026*
