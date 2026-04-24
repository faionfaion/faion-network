# Review Workflow

Step-by-step workflow for validating implementation and extracting learnings.

---

## Overview

The review workflow validates completed work against specifications and extracts patterns and learnings for future use.

```
VALIDATE -> CODE-REVIEW -> ACCEPTANCE -> LEARN -> UPDATE-MEMORY -> CLOSE
    |           |             |           |            |            |
  Tests     Quality        AC check    Patterns     Memory      Move to
  pass      standards      verified    extracted    updated      done/
```

---

## When to Use

| Trigger | Review Type |
|---------|-------------|
| Task completed | Task Review |
| Wave completed | Wave Review |
| Feature completed | Feature Review |
| PR submitted | Code Review |
| Post-incident | Retrospective |

---

## Phase 1: Validate

### Purpose

Verify all quality gates pass before proceeding with review.

### Entry State

```
INPUT: Completed task/wave/feature
STATE: validate
CONFIDENCE: 0%
```

### Workflow Steps

```
1. Run automated checks
   |
   +---> Linting (L1)
   +---> Type checking (L2)
   +---> Unit tests (L3)
   +---> Integration tests (L4)
   |
   v
2. Check coverage
   |
   +---> Compare to constitution threshold
   +---> Identify uncovered paths
   |
   v
3. Run security scans (if applicable)
   |
   +---> Dependency vulnerabilities
   +---> Secret detection
   |
   v
4. Aggregate results
```

### Validation Checklist

```markdown
## Validation Results

### Automated Checks
| Check | Status | Details |
|-------|--------|---------|
| Lint (L1) | Pass/Fail | [errors count] |
| Types (L2) | Pass/Fail | [errors count] |
| Unit Tests (L3) | Pass/Fail | [pass/total] |
| Integration (L4) | Pass/Fail | [pass/total] |

### Coverage
- Current: [X]%
- Required: [Y]%
- Status: [Met/Not Met]

### Security
| Scan | Status | Findings |
|------|--------|----------|
| Dependencies | Pass/Fail | [count] |
| Secrets | Pass/Fail | [count] |
```

### Exit Criteria

- [ ] All L1-L4 gates pass
- [ ] Coverage threshold met
- [ ] No critical security findings

### Exit State

```
OUTPUT: Validation report
STATE: code-review
CONFIDENCE: 30%
```

---

## Phase 2: Code Review

### Purpose

Review code quality, patterns, and adherence to standards.

### Entry State

```
INPUT: Validated code
STATE: code-review
CONFIDENCE: 30%
```

### Review Dimensions

| Dimension | Focus | Severity |
|-----------|-------|----------|
| Correctness | Does it do what spec says? | Critical |
| Security | Auth, validation, injection | Critical |
| Performance | N+1, indexes, caching | High |
| Patterns | Follows codebase conventions | Medium |
| Readability | Comments, naming, structure | Medium |
| Tests | Coverage, edge cases | Medium |

### Workflow Steps

```
1. Correctness Review
   |
   +---> Compare implementation to spec FR-XXX
   +---> Check all AC scenarios work
   +---> Verify edge cases handled
   |
   v
2. Security Review
   |
   +---> Input validation present?
   +---> Auth checks in place?
   +---> No SQL injection vectors?
   +---> No hardcoded secrets?
   |
   v
3. Performance Review
   |
   +---> N+1 query patterns?
   +---> Missing database indexes?
   +---> Resource leaks?
   +---> Caching opportunities?
   |
   v
4. Pattern Review
   |
   +---> Follows existing codebase patterns?
   +---> Naming conventions correct?
   +---> Directory structure correct?
   |
   v
5. Readability Review
   |
   +---> Code self-documenting?
   +---> Complex logic commented?
   +---> Dead code removed?
   |
   v
6. Test Review
   |
   +---> Test coverage adequate?
   +---> Edge cases tested?
   +---> Test names descriptive?
```

### Code Review Checklist

```markdown
## Code Review

### Correctness
- [ ] Implements all FR-XXX requirements
- [ ] Handles all AC scenarios
- [ ] Edge cases from spec addressed
- [ ] Error messages helpful

### Security
- [ ] All inputs validated
- [ ] Auth/authz checks present
- [ ] No injection vulnerabilities
- [ ] No secrets in code
- [ ] Sensitive data encrypted/hashed

### Performance
- [ ] No N+1 queries
- [ ] Appropriate indexes
- [ ] No resource leaks
- [ ] Pagination for lists

### Patterns
- [ ] Follows existing patterns
- [ ] Consistent naming
- [ ] Correct file locations
- [ ] DRY principle followed

### Readability
- [ ] Self-documenting code
- [ ] Complex logic explained
- [ ] No dead code
- [ ] Reasonable function length

### Tests
- [ ] Unit tests for logic
- [ ] Integration tests for flows
- [ ] Descriptive test names
- [ ] Fixtures clean and reusable
```

### Multi-Model Review Pattern

For critical code, use multiple LLM models:

```
Code to Review
      |
      +---> Model A Review (e.g., Claude)
      +---> Model B Review (e.g., GPT-4)
      +---> Model C Review (e.g., Gemini)
      |
      v
Aggregate Findings
      |
      +---> Common issues (high confidence)
      +---> Unique issues (investigate)
      +---> Contradictions (human decision)
```

### Exit Criteria

- [ ] All critical issues resolved
- [ ] High severity issues addressed
- [ ] Medium issues documented/ticketed

### Exit State

```
OUTPUT: Code review report
STATE: acceptance
CONFIDENCE: 60%
```

---

## Phase 3: Acceptance

### Purpose

Verify implementation meets all acceptance criteria from spec.

### Entry State

```
INPUT: Code review passed
STATE: acceptance
CONFIDENCE: 60%
```

### Workflow Steps

```
1. Load acceptance criteria
   |
   +---> Read all AC-XXX from spec
   |
   v
2. For each AC:
   |
   +---> Execute scenario manually or via test
   +---> Verify expected outcome
   +---> Document result
   |
   v
3. Compile acceptance report
   |
   v
4. Get stakeholder sign-off (if required)
```

### Acceptance Testing Template

```markdown
## Acceptance Testing

### AC-001: [Scenario Name]

**Scenario:** [Description]

**Given:** [Precondition]
**When:** [Action taken]
**Then:** [Expected result]

**Test Steps:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Actual Result:** [What happened]
**Status:** Pass / Fail
**Evidence:** [Screenshot/log/etc.]

---

### AC-002: [Next Scenario]
...

---

## Summary

| AC | Description | Status |
|----|-------------|--------|
| AC-001 | [Summary] | Pass |
| AC-002 | [Summary] | Pass |
| AC-003 | [Summary] | Fail |

**Overall:** [X/Y] passed
**Decision:** [Approved / Needs Work]
```

### Exit Criteria

- [ ] All AC scenarios tested
- [ ] All required AC pass
- [ ] Failures documented and addressed

### Exit State

```
OUTPUT: Acceptance report
STATE: learn
CONFIDENCE: 80%
```

---

## Phase 4: Learn (Reflexion)

### Purpose

Extract patterns from success and lessons from failures.

### Entry State

```
INPUT: Completed and accepted work
STATE: learn
CONFIDENCE: 80%
```

### PDCA Cycle

```
Plan (What we intended)
  |
  v
Do (What we did)
  |
  v
Check (Compare results)
  |
  v
Act (Improve process)
  |
  v
Store (Update memory)
```

### Workflow Steps

```
1. Analyze what worked
   |
   +---> Successful patterns
   +---> Efficient approaches
   +---> Reusable components
   |
   v
2. Analyze what didn't work
   |
   +---> Errors encountered
   +---> Root causes
   +---> Prevention strategies
   |
   v
3. Identify improvements
   |
   +---> Process improvements
   +---> Tool improvements
   +---> Documentation gaps
   |
   v
4. Prepare memory updates
```

### Pattern Extraction

```markdown
## Pattern Learned

### Context
[When this pattern applies]

### Problem
[What problem it solves]

### Solution
[The pattern/approach that worked]

### Example
```[language]
// Example code
```

### Benefits
- [Benefit 1]
- [Benefit 2]

### Trade-offs
- [Trade-off 1]

### Evidence
- Used in: [task/feature]
- Result: [outcome]
```

### Mistake Analysis

```markdown
## Mistake Recorded

### Error
[What went wrong]

### Root Cause
[Why it happened]

### Impact
[What was affected]

### Detection
[How we found it]

### Prevention
[How to avoid in future]

### Recovery
[How to fix if it happens]

### Checklist Addition
- [ ] [New check to add]
```

### Improvement Suggestions

```markdown
## Improvement Identified

### Area
[Process/Tool/Documentation]

### Current State
[How it works now]

### Problem
[What's suboptimal]

### Proposed Change
[Suggested improvement]

### Expected Benefit
[What we gain]

### Priority
[High/Medium/Low]
```

### Exit Criteria

- [ ] Successful patterns documented
- [ ] Mistakes analyzed
- [ ] Improvements identified

### Exit State

```
OUTPUT: Learnings
STATE: update-memory
CONFIDENCE: 90%
```

---

## Phase 5: Update Memory

### Purpose

Persist learnings to project memory for future use.

### Entry State

```
INPUT: Learnings
STATE: update-memory
CONFIDENCE: 90%
```

### Memory Locations

```
.aidocs/memory/
├── patterns.md      # Successful patterns
├── mistakes.md      # Errors and solutions
├── decisions.md     # Key decisions made
└── session.md       # Current session state
```

### Workflow Steps

```
1. Update patterns.md
   |
   +---> Add new patterns
   +---> Update existing patterns with new evidence
   |
   v
2. Update mistakes.md
   |
   +---> Add new mistakes
   +---> Cross-reference with patterns
   |
   v
3. Update decisions.md
   |
   +---> Add significant decisions
   +---> Link to ADRs if applicable
   |
   v
4. Update session.md
   |
   +---> Clear completed items
   +---> Update current state
```

### Pattern Memory Format

```markdown
## patterns.md

### Pattern: [Name]
- **ID:** PAT-XXX
- **Domain:** [Development/Testing/etc.]
- **Context:** [When to use]
- **Pattern:** [Description]
- **Example:** [Code or process]
- **Used in:** [Task/Feature references]
- **Last updated:** [Date]

---
```

### Mistake Memory Format

```markdown
## mistakes.md

### Mistake: [Name]
- **ID:** ERR-XXX
- **Type:** [Code/Process/Design]
- **Error:** [What happened]
- **Root cause:** [Why]
- **Prevention:** [How to avoid]
- **Recovery:** [How to fix]
- **Occurred in:** [Task/Feature]
- **Last updated:** [Date]

---
```

### Exit Criteria

- [ ] Patterns stored
- [ ] Mistakes recorded
- [ ] Session state updated

### Exit State

```
OUTPUT: Memory updated
STATE: close
CONFIDENCE: 95%
```

---

## Phase 6: Close

### Purpose

Complete the task/feature lifecycle.

### Entry State

```
INPUT: Memory updated
STATE: close
CONFIDENCE: 95%
```

### Workflow Steps

```
1. Move task/feature to done/
   |
   +---> mv tasks/in-progress/TASK_XXX.md tasks/done/
   +---> OR mv features/in-progress/feature-XXX/ features/done/
   |
   v
2. Update task status
   |
   +---> Set status: done in frontmatter
   +---> Add completion date
   |
   v
3. Generate summary
   |
   +---> What was built
   +---> Files changed
   +---> Tests added
   +---> Metrics
   |
   v
4. Notify completion
   |
   +---> Report to user
   +---> Link to evidence
```

### Completion Summary Template

```markdown
## Task/Feature Completion Summary

### Overview
- **ID:** TASK-XXX / feature-XXX
- **Title:** [Name]
- **Completed:** [Date]

### Deliverables
| Item | Status |
|------|--------|
| [Deliverable 1] | Done |
| [Deliverable 2] | Done |

### Files Changed
| Action | File | LOC |
|--------|------|-----|
| CREATE | [path] | +XXX |
| MODIFY | [path] | +XX/-YY |

### Testing
- Unit tests: [X] added
- Integration tests: [Y] added
- Coverage: [Z]%

### Acceptance
- AC passed: [X/Y]

### Metrics
- Tasks completed: [N]
- Estimated tokens: [Xk]
- Actual tokens: [Yk]

### Lessons Learned
- Pattern: [PAT-XXX] discovered
- Mistake: [ERR-XXX] prevented

### Next Steps
- [Follow-up item 1]
- [Follow-up item 2]
```

### Exit State

```
OUTPUT: Closed task/feature
STATE: complete
NEXT: None (or next task/feature)
```

---

## Review Types

### Task Review (Per Task)

Quick review for individual tasks:

```
Validate (L1-L3) -> Quick Code Check -> Mark Done -> Brief Learning
```

Duration: 5-15 minutes

### Wave Review (Per Wave)

Review for completed wave with parallel work:

```
Merge Check -> Integration Tests -> Cross-Task Review -> Checkpoint Learning
```

Duration: 15-30 minutes

### Feature Review (Per Feature)

Comprehensive review for completed feature:

```
Full Validation -> Deep Code Review -> Acceptance Testing -> Full Reflexion
```

Duration: 30-60 minutes

### PR Review (Pull Request)

Review for external contribution:

```
CI Checks -> Code Review -> Approval/Changes Requested -> Merge
```

Duration: Variable

---

## Multi-Model Review Strategy

### When to Use Multiple Models

| Scenario | Recommendation |
|----------|----------------|
| Security-critical code | Always multi-model |
| Complex algorithms | Recommended |
| Financial calculations | Always multi-model |
| Standard CRUD | Single model OK |
| Simple fixes | Single model OK |

### Multi-Model Process

```
1. Submit same code to multiple models
   |
   +---> Claude: Review for [aspect]
   +---> GPT-4: Review for [aspect]
   +---> Gemini: Review for [aspect]
   |
   v
2. Collect findings
   |
   v
3. Categorize findings:
   |
   +---> Agreement: High confidence issue
   +---> Single model: Investigate further
   +---> Contradiction: Human judgment needed
   |
   v
4. Synthesize final review
```

---

## Automated Review Integration

### CI/CD Integration

```yaml
# .github/workflows/review.yml
name: Automated Review

on: [pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Lint
        run: npm run lint
      - name: Types
        run: npm run typecheck
      - name: Test
        run: npm run test:coverage

  code-review:
    needs: validate
    runs-on: ubuntu-latest
    steps:
      - name: AI Code Review
        uses: coderabbit/ai-review@v1
        with:
          model: claude-3-sonnet
```

### Pre-Commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: lint
        name: Lint
        entry: npm run lint
        language: system
        pass_filenames: false

      - id: type-check
        name: Type Check
        entry: npm run typecheck
        language: system
        pass_filenames: false
```

---


## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Writing specification templates | haiku | Form completion, mechanical setup |
| Reviewing specifications for clarity | sonnet | Language analysis, logical consistency |
| Architecting complex system specs | opus | Holistic design, novel combinations |
## Related Workflows

| Workflow | Relationship |
|----------|--------------|
| [implementation-workflow.md](implementation-workflow.md) | Input from execution |
| [spec-workflow.md](spec-workflow.md) | AC from spec |
| [llm-prompts.md](llm-prompts.md) | Prompts for review |

---

*Review Workflow | SDD Workflows | v1.0.0*
