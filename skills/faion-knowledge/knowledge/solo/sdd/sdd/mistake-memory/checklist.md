# Mistake Capture Checklist

## When to Capture

Capture a mistake when:
- [ ] Bug found in production
- [ ] Task took >2x estimated tokens
- [ ] Same error occurred twice
- [ ] CI/CD pipeline failed unexpectedly
- [ ] Code review found critical issue
- [ ] LLM generated incorrect/hallucinated code
- [ ] Context was lost mid-task
- [ ] Security vulnerability discovered

## Immediate Capture (Within 1 Hour)

### 1. Document the Incident

- [ ] **What happened?** (Brief description)
- [ ] **When?** (Timestamp)
- [ ] **Where?** (File, function, system)
- [ ] **Who discovered?** (Human/CI/LLM)
- [ ] **Impact?** (Users affected, data loss, downtime)

### 2. Preserve Evidence

- [ ] Save error logs
- [ ] Screenshot UI errors
- [ ] Copy LLM conversation/prompt
- [ ] Note environment details
- [ ] Git commit hash (if applicable)

### 3. Assign Severity

| Severity | Criteria |
|----------|----------|
| Critical | Production down, data loss, security breach |
| High | Major feature broken, significant user impact |
| Medium | Feature degraded, workaround exists |
| Low | Minor issue, cosmetic, edge case |

## Root Cause Analysis (Within 24 Hours)

### 4. Perform Five Whys

- [ ] Why 1: What was the immediate cause?
- [ ] Why 2: What enabled that cause?
- [ ] Why 3: What systemic factor contributed?
- [ ] Why 4: What process gap exists?
- [ ] Why 5: What is the root cause?

### 5. Categorize the Mistake

**LLM-Specific Categories:**
- [ ] Hallucination (factual, API, confident fabrication)
- [ ] Context loss (window limit, instruction drift)
- [ ] Scope creep (added unrequested features)
- [ ] Missing validation (skipped checks)

**General Categories:**
- [ ] Implementation (edge cases, error handling)
- [ ] Data handling (backup, migration, corruption)
- [ ] Security (secrets, auth, validation)
- [ ] Deployment (config, rollback, dependencies)
- [ ] Estimation (complexity underestimated)
- [ ] Communication (unclear requirements)
- [ ] Testing (insufficient coverage)
- [ ] Process (skipped steps)

### 6. Identify Contributing Factors

- [ ] Insufficient context provided to LLM
- [ ] Task too large for single prompt
- [ ] Missing documentation in context
- [ ] Time pressure led to shortcuts
- [ ] Unfamiliar technology/domain
- [ ] Unclear or changing requirements
- [ ] Missing or skipped quality gates

## Prevention Planning (Within 48 Hours)

### 7. Define Immediate Actions

- [ ] What fix is needed now?
- [ ] Who will implement?
- [ ] What testing required?
- [ ] When will it be deployed?

### 8. Define Process Changes

- [ ] What checklist item to add?
- [ ] What quality gate to implement?
- [ ] What automation to create?
- [ ] What documentation to update?

### 9. Create Prevention Rules

```markdown
## Prevention Rule Template

**Rule ID:** PREV_XXX
**Source Mistake:** MIS_XXXX_XXX
**Trigger:** [file pattern / task type / keyword]
**Action:** [warn / require_checklist / block]
**Message:** [Warning text with mistake reference]
```

### 10. Update Checklists

- [ ] Add item to relevant domain checklist
- [ ] Specify position (first, before-execution, after-completion)
- [ ] Include reference to source mistake

## Follow-Up (1 Week Later)

### 11. Verify Prevention Effectiveness

- [ ] Was the prevention triggered since implementation?
- [ ] Did it successfully prevent recurrence?
- [ ] Any false positives to address?
- [ ] Adjustments needed?

### 12. Close the Loop

- [ ] Update mistake record with prevention effectiveness
- [ ] Share learnings with team (if applicable)
- [ ] Archive incident report
- [ ] Schedule next review (30 days)

## Quick Capture Template

For fast documentation when time is limited:

```markdown
## Quick Mistake: [Title]

**Date:** YYYY-MM-DD
**Severity:** Critical / High / Medium / Low
**Category:** [hallucination / context / implementation / etc.]

**What:** [One sentence description]

**Impact:** [Time lost / users affected / data lost]

**Root Cause:** [Brief]

**Prevention:**
- [ ] [Action 1]
- [ ] [Action 2]

**Source:** TASK_XXX / INC_XXX
```

## LLM-Specific Capture Additions

When the mistake involves LLM-generated code:

### Context Analysis

- [ ] What was in the LLM context?
- [ ] What was missing from context?
- [ ] Was context window exceeded?
- [ ] Were instructions clear?

### Prompt Analysis

- [ ] Was the prompt too vague?
- [ ] Were examples provided?
- [ ] Was the task appropriately scoped?
- [ ] Was Chain-of-Thought used?

### Output Analysis

- [ ] Did LLM show uncertainty?
- [ ] Were there warning signs missed?
- [ ] Was output reviewed before use?
- [ ] Were tests run against output?

### Correction Approach

- [ ] What feedback fixed the error?
- [ ] How many iterations needed?
- [ ] What additional context helped?
- [ ] Should this be added to standard prompts?
