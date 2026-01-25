---
id: strategy-basics
name: "BA Strategy Basics: Current/Future State & Risk"
domain: BA
skill: faion-business-analyst
category: "business-analysis"
knowledge_area: "KA-4 Strategy"
---

# BA Strategy Basics: Current/Future State & Risk

Current state analysis, future state definition, risk analysis, and change strategy planning.

---

## 1. Current State Analysis

### Problem
How to understand the existing environment and identify needs?

### Framework

1. **Business Context**
   - Organizational structure
   - Business processes
   - Strategic goals

2. **Capability Assessment**
   - Current capabilities
   - Capability gaps
   - Maturity levels

3. **Technology Landscape**
   - Current systems
   - Integration points
   - Technical debt

4. **Stakeholder Landscape**
   - Key players
   - Pain points
   - Success metrics

5. **SWOT Analysis**
   - Strengths
   - Weaknesses
   - Opportunities
   - Threats

### Template

```markdown
## Current State Assessment

### Business Context
- Organization: {description}
- Core processes: {list}
- Strategic alignment: {goals}

### Capability Assessment
| Capability | Current State | Target State | Gap |
|------------|--------------|--------------|-----|
| {cap} | {level 1-5} | {level 1-5} | {delta} |

### Pain Points
1. {pain point 1}
2. {pain point 2}

### SWOT
| Strengths | Weaknesses |
|-----------|------------|
| {s1} | {w1} |

| Opportunities | Threats |
|---------------|---------|
| {o1} | {t1} |
```

---

## 2. Future State Definition

### Problem
How to define the desired future state?

### Framework

1. **Vision Statement**
   - Clear, compelling description
   - Stakeholder-aligned
   - Measurable outcomes

2. **Goals and Objectives**
   - SMART criteria
   - Aligned with strategy
   - Prioritized

3. **New Capabilities**
   - Required capabilities
   - Capability improvements
   - Capability retirements

4. **Success Metrics**
   - KPIs definition
   - Baseline vs target
   - Measurement approach

5. **Constraints and Assumptions**
   - Budget limitations
   - Timeline constraints
   - Technical constraints
   - Assumptions to validate

### Template

```markdown
## Future State Vision

### Vision Statement
{compelling description of future state}

### Goals and Objectives
| Goal | Objective | Metric | Target |
|------|-----------|--------|--------|
| {G1} | {O1} | {KPI} | {value} |

### Capability Roadmap
| Capability | Current | Future | Timeline |
|------------|---------|--------|----------|
| {cap} | Level 2 | Level 4 | Q3 2026 |

### Constraints
- Budget: {amount}
- Timeline: {deadline}
- Technology: {constraints}

### Assumptions
1. {assumption 1} - Validated: Yes/No
2. {assumption 2} - Validated: Yes/No
```

---

## 3. Risk Analysis

### Problem
How to identify and assess risks to the change initiative?

### Framework

1. **Risk Identification**
   - Technical risks
   - Business risks
   - Organizational risks
   - External risks

2. **Risk Assessment**
   - Probability (1-5)
   - Impact (1-5)
   - Risk score = P x I

3. **Risk Response**
   - Avoid, Mitigate, Transfer, Accept
   - Response owner
   - Contingency plan

4. **Risk Monitoring**
   - Triggers
   - Status tracking
   - Escalation criteria

### Template

```markdown
## Risk Register

| ID | Risk | Category | P | I | Score | Response | Owner |
|----|------|----------|---|---|-------|----------|-------|
| R-001 | {description} | Technical | 4 | 5 | 20 | Mitigate | {name} |
| R-002 | {description} | Business | 2 | 3 | 6 | Accept | {name} |

## Risk Matrix

High Impact
    |
    | Accept    |  Mitigate/
    | with      |  Avoid
    | Reserve   |
    |-----------|----------
    | Accept    |  Monitor
    |           |  Closely
Low Impact --- Low Prob --- High Prob
```

---

## 4. Change Strategy Planning

### Problem
How to develop the optimal approach for achieving the future state?

### Framework

1. **Gap Analysis**
   - Current vs future state delta
   - Capability gaps
   - Process gaps
   - Technology gaps

2. **Solution Options**
   - Build vs buy vs partner
   - Phased vs big bang
   - Scope variations

3. **Transition Planning**
   - Milestones and phases
   - Dependencies
   - Resource requirements

4. **Readiness Assessment**
   - Organizational readiness
   - Technical readiness
   - Stakeholder readiness

5. **Business Case**
   - Expected benefits
   - Total cost of ownership
   - ROI calculation

### Template

```markdown
## Change Strategy

### Gap Analysis
| Dimension | Current | Future | Gap | Priority |
|-----------|---------|--------|-----|----------|
| Process | {state} | {state} | {gap} | H/M/L |
| Technology | {state} | {state} | {gap} | H/M/L |

### Solution Options
| Option | Description | Pros | Cons | Est. Cost |
|--------|-------------|------|------|-----------|
| A | Build in-house | Control | Time | $500K |
| B | Buy COTS | Speed | Fit | $300K |

### Recommendation
Option {X} because {rationale}

### Transition Roadmap
Phase 1 (Q1): {scope}
Phase 2 (Q2): {scope}
Phase 3 (Q3): {scope}
```

---

*BA Strategy Basics*
*Knowledge Area: KA-4 Strategy*
