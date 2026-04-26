# Decision Analysis: [Decision Topic]

**Version:** 1.0
**Date:** [Date — criteria locked]
**Analyst:** [Name]
**Decision Maker:** [Name]
**Weight-setter:** [Name, timestamp] — weights locked before scoring

## 1. Decision Context

**Decision Statement:** [What specific decision needs to be made]

**Objectives:**
- [Objective 1]

**Constraints:**
- [Constraint 1]

**Background:** [Why this decision is needed now]

## 2. Options Considered

### Option 1: [Name]
- **Description:** [What this option involves]
- **Pros:** [Verifiable benefits]
- **Cons:** [Verifiable drawbacks]

### Option 2: Do Nothing / Status Quo
- **Description:** Maintain current state
- **Cons:** [What we lose by stalling]

## 3. Criteria and Weights (lock before scoring)

| Criterion | Weight | Direction | Definition | Score scale |
|-----------|--------|-----------|------------|-------------|
| [Criterion] | [X%] | higher_better/lower_better | [What it means] | [5=best for this direction] |

Total weights must sum to 100%. Max 7 criteria.

## 4. Evaluation Matrix

| Criterion | Wt | Option 1 | Option 2 | Option 3 | Evidence |
|-----------|----|----------|----------|----------|----------|
| [Crit 1] | X% | [Score] | [Score] | [Score] | [URL, fetched YYYY-MM-DD] |
| **Weighted Total** | 100% | **X.XX** | **X.XX** | **X.XX** | |

## 5. Sensitivity Analysis

Run: `python sensitivity.py matrix.json`

| Option | Robustness % | Mean | SD |
|--------|-------------|------|----|
| [Option 1] | [X%] | [X.XX] | [X.XX] |

If top option robustness < 70%: escalate to human before committing.

## 6. Recommendation

**Recommended Option:** [Option X]
**Rationale:** [At most 80 words]
**Robustness:** [X% Monte Carlo trials]
**Top Risks:**
1. [Risk] — Mitigation: [Plan]

**Pre-mortem:** Assume in 12 months this was the wrong call. Why?
- [Pre-mortem finding]

## 7. Approval

| Role | Name | Decision | Date |
|------|------|----------|------|
| Decision Maker | | Approve/Reject | |

**Final Decision:** [What was decided]
