# Decision Analysis: [Decision Topic]

**Version:** [X.X]
**Date:** [Date]
**Decision ID:** DEC-[NNN]
**Analyst:** [Name]
**Decision Maker:** [Name — must be a specific named human with authority]

## 1. Decision Context

### Decision Statement (25 words max, outcome-shaped)

[What specific decision needs to be made — outcome-shaped, not solution-shaped]

### Objectives

- [Objective 1 — outcome-shaped]
- [Objective 2 — outcome-shaped]

### Constraints

| Constraint | Source Quote | Source Document |
|------------|-------------|----------------|
| [Constraint] | "[verbatim quote]" | [doc name] |

### Background

[Context — why this decision is needed now, and what triggered it]

## 2. Options Considered

### Option 1: [Name]
- **Description:** [What this option involves]
- **Pros:** [Benefits]
- **Cons:** [Drawbacks]

### Option 2: [Name]
[Same structure]

### Option 3: Do Nothing / Status Quo
- **Description:** Maintain current state
- **Pros:** [Benefits — no change cost, no risk]
- **Cons:** [Opportunity cost, ongoing pain]

## 3. Evaluation Criteria (5-7 max)

| Criterion | Weight | Traces To | Definition | Scoring Direction | Rubric: 1 | Rubric: 3 | Rubric: 5 |
|-----------|--------|-----------|------------|------------------|-----------|-----------|-----------|
| [Criterion] | [X%] | REQ-XXX | [What it means] | higher_better | [Worst] | [Mid] | [Best] |

**Weight locked at:** [timestamp] **by:** [name]

## 4. Evaluation Matrix

| Criterion | Weight | Option 1 | Option 2 | Option 3: Do Nothing |
|-----------|--------|----------|----------|---------------------|
| [Criterion 1] | [X%] | [Score] / evidence: [URL] | [Score] / evidence: [URL] | [Score] |
| **Weighted Total** | 100% | **[X.XX]** | **[X.XX]** | **[X.XX]** |

## 5. Analysis

### Sensitivity Analysis (±20% on each criterion weight)

| Criterion Varied | Recommendation Changes? | Notes |
|-----------------|------------------------|-------|
| [Criterion] | Yes/No | [If yes, explain] |

### Risks per Option

| Option | Key Risks | Mitigation |
|--------|-----------|------------|
| [Option] | [Risks] | [Mitigation] |

## 6. Recommendation

**Recommended Option:** [Option X]

**Rationale:** [Evidence-based rationale citing weighted scores and sensitivity results]

**Requirement Traces (bi-directional):**
- Impacted requirements: REQ-XXX, REQ-YYY (update each with `decisions: [DEC-NNN]`)
- This document: `traces_to: [REQ-XXX, REQ-YYY]`

## 7. Approval

| Role | Name | Verdict (approve/reject) | Date |
|------|------|--------------------------|------|
| Decision Maker | | approve | |

**Post-Implementation Review Scheduled:** [6 months from approval date]
