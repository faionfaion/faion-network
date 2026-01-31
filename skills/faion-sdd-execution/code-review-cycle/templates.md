# Code Review Cycle Templates

## PR Template

```markdown
## Summary
<!-- Brief description of changes -->

## SDD References
| Document | Section |
|----------|---------|
| Spec | [SPEC-XXX](link) |
| Design | [DESIGN-XXX](link) |
| Task | [TASK-XXX](link) |

## Changes
- [x] Feature/fix description
- [x] Another change

## Acceptance Criteria Verification
| AC | Status | Notes |
|----|--------|-------|
| AC-1: Given X, When Y, Then Z | Verified | Screenshot/test |

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] Edge cases tested

## Checklist
- [ ] Self-review completed
- [ ] Tests pass locally
- [ ] No lint/type errors
- [ ] Documentation updated
- [ ] No secrets committed
```

## Review Comment Templates

### Required Change
```
[Required] This could cause a null pointer exception when user is undefined.
Consider adding a null check:
if (user) {
  processUser(user);
}
```

### Suggestion
```
[Suggestion] Could use early return here to reduce nesting:
if (!isValid) return;
// rest of code
```

### Question
```
[Question] I see you chose to use a Map here instead of an object.
Was this for a specific reason like preserving insertion order?
Just trying to understand the decision for future reference.
```

### Nitpick
```
[Nitpick] Could rename this to be more descriptive:
processData -> processUserRegistrationData
```

### Praise
```
[Nice] Clean separation of concerns here. The validation logic is
well isolated and reusable.
```

### FYI
```
[FYI] There's a utility for this in utils/string.ts that handles
edge cases like null/undefined.
```

## Review Checklist Template

```markdown
## Code Review Checklist

### PR: [Title]
### Reviewer: @name
### Date: YYYY-MM-DD

### Correctness
- [ ] Solves the stated problem
- [ ] Handles edge cases
- [ ] No obvious bugs
- [ ] Error handling appropriate

### Design
- [ ] Follows project patterns
- [ ] Appropriate abstraction level
- [ ] No unnecessary complexity
- [ ] Consistent with architecture

### Code Quality
- [ ] Clear naming
- [ ] Well-organized
- [ ] No code smells
- [ ] DRY (Don't Repeat Yourself)

### Testing
- [ ] Adequate test coverage
- [ ] Tests are meaningful
- [ ] Edge cases tested

### Security
- [ ] Input validation
- [ ] No hardcoded secrets
- [ ] Auth/authz correct

### Documentation
- [ ] Code is self-documenting
- [ ] Complex logic commented
- [ ] API docs updated

### SDD Compliance
- [ ] Matches design document
- [ ] Deviations justified
- [ ] Acceptance criteria met

### Verdict
- [ ] Approved
- [ ] Approved with suggestions
- [ ] Request changes

### Summary
[Overall assessment and key points]
```

## Approval Criteria Template

```yaml
merge_criteria:
  automated:
    - all_tests_pass: true
    - lint_clean: true
    - type_check_pass: true
    - coverage_threshold_met: true
    - security_scan_pass: true

  human_review:
    - required_approvals: 1  # or 2 for critical paths
    - no_unresolved_required_comments: true
    - all_discussions_resolved: true

  special_cases:
    critical_path:
      - additional_approval_from: "tech lead"
    security_sensitive:
      - additional_approval_from: "security team"
    database_changes:
      - additional_approval_from: "DBA or senior"
```

## Review Metrics Template

```yaml
review_metrics:
  efficiency:
    - time_to_first_review: "< 4 hours"
    - time_to_merge: "< 24 hours"
    - review_iterations: "< 3"

  quality:
    - bugs_found_in_review: "track"
    - bugs_escaped_to_prod: "minimize"
    - rework_rate: "< 10%"

  engagement:
    - review_participation: "all team members"
    - feedback_ratio: "constructive vs blocking"
    - knowledge_sharing: "FYI comments"
```
