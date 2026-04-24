# Code Review Templates

Templates for PRs, review comments, and AI configuration.

## PR Templates

### Standard PR Template

```markdown
## Summary

<!-- Brief description: what changed and why -->

## SDD References

| Document | Link |
|----------|------|
| Spec | [SPEC-XXX](link) |
| Design | [DESIGN-XXX](link) |
| Task | [TASK-XXX](link) |

## Changes

- [ ] Change 1 description
- [ ] Change 2 description

## Acceptance Criteria Verification

| AC | Status | Evidence |
|----|--------|----------|
| AC-1: Given X, When Y, Then Z | Verified | [Screenshot/test] |
| AC-2: ... | Verified | |

## Testing

- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] Edge cases tested

## Screenshots (if UI changes)

| Before | After |
|--------|-------|
| [image] | [image] |

## Checklist

- [ ] Self-review completed
- [ ] AI review addressed (CodeRabbit/Copilot)
- [ ] Tests pass locally
- [ ] No lint/type errors
- [ ] Documentation updated
- [ ] No secrets committed

## Notes for Reviewer

<!-- Any context that helps review -->

---
AI Review Summary: <!-- Paste AI review summary here -->
```

### Security-Sensitive PR Template

```markdown
## Summary

<!-- Description of security-related change -->

## Security Context

**Type of Change:**
- [ ] Authentication
- [ ] Authorization
- [ ] Data encryption
- [ ] Input validation
- [ ] Dependency update
- [ ] Security fix
- [ ] Other: ___

**Risk Assessment:**
- [ ] Low - Cosmetic/non-functional
- [ ] Medium - Functional but limited exposure
- [ ] High - Auth/data handling/external inputs

## SDD References

| Document | Link |
|----------|------|
| Spec | [SPEC-XXX](link) |
| Design | [DESIGN-XXX](link) |
| Security Review | [SECURITY-XXX](link) |

## Security Checklist

- [ ] No hardcoded secrets
- [ ] Input validation implemented
- [ ] Output encoding for XSS prevention
- [ ] SQL injection prevented (parameterized queries)
- [ ] Auth/authz checks at all entry points
- [ ] Sensitive data encrypted
- [ ] Security scan passed (SAST/DAST)
- [ ] Dependencies scanned for vulnerabilities

## Threat Model Considerations

<!-- What threats does this change address or introduce? -->

## Testing

- [ ] Security-focused unit tests
- [ ] Penetration testing (if applicable)
- [ ] Fuzz testing (if applicable)

## Rollback Plan

<!-- How to quickly rollback if issues discovered -->

## Required Approvals

- [ ] Security team review
- [ ] Tech lead review
```

### Database Migration PR Template

```markdown
## Summary

<!-- Description of database change -->

## Migration Details

**Type:**
- [ ] Schema change (add/modify table)
- [ ] Data migration
- [ ] Index addition
- [ ] Performance optimization
- [ ] Cleanup/removal

**Scope:**
- Tables affected:
- Estimated rows:
- Estimated execution time:

## SDD References

| Document | Link |
|----------|------|
| Design | [DESIGN-XXX](link) |
| Task | [TASK-XXX](link) |

## Migration Checklist

### Safety
- [ ] Migration is reversible (down migration tested)
- [ ] No data loss possible
- [ ] Handles empty and full tables
- [ ] No table-level locks (or acceptable downtime window)

### Performance
- [ ] Query plans reviewed for new queries
- [ ] New indexes documented and justified
- [ ] Batch operations for large data changes
- [ ] Tested on production-sized data

### Deployment
- [ ] Can deploy without downtime
- [ ] Rollback procedure documented
- [ ] Data backfill strategy documented
- [ ] Blue-green compatible

## Test Results

| Environment | Data Size | Execution Time | Result |
|-------------|-----------|----------------|--------|
| Local | 1k rows | Xs | Pass |
| Staging | 100k rows | Xs | Pass |

## Rollback Script

```sql
-- Paste rollback script here
```

## Required Approvals

- [ ] DBA review
- [ ] Tech lead review
```

### Hotfix PR Template

```markdown
## HOTFIX

**Severity:** Critical / High / Medium
**Production Impact:** <!-- Currently affecting X users/requests -->

## Problem

<!-- Brief description of the production issue -->

## Root Cause

<!-- What caused this issue -->

## Fix

<!-- What this PR does to fix it -->

## Verification

- [ ] Fix tested locally
- [ ] Fix verified in staging
- [ ] Regression tests added
- [ ] No other code affected

## Monitoring

<!-- How will we verify the fix works in production? -->
- [ ] Error rate should decrease
- [ ] Metric X should normalize
- [ ] Alerts should clear

## Post-Mortem

- [ ] Incident documented
- [ ] Post-mortem scheduled

## Fast-Track Approval

Due to production impact, requesting fast-track review.

- [ ] Primary reviewer: @name
- [ ] Secondary reviewer: @name (async)
```

---

## Review Comment Templates

### Required Change

```markdown
[Required] **Issue:** Brief description of problem

**Current code:**
<!-- Paste problematic code -->

**Problem:** Explain why this is an issue

**Suggested fix:**
<!-- Paste suggested fix -->

**Reference:** Link to documentation/standard
```

### Suggestion

```markdown
[Suggestion] **Improvement opportunity**

**Current approach:**
<!-- Brief description -->

**Alternative:**
<!-- Suggested approach -->

**Benefits:**
- Benefit 1
- Benefit 2

This is optional - the current approach works.
```

### Security Concern

```markdown
[Security] **Potential vulnerability: [Type]**

**Risk:** Brief description of what could go wrong

**Current code:**
<!-- Problematic code -->

**Recommended fix:**
<!-- Secure version -->

**Severity:** Critical / High / Medium / Low

**References:**
- OWASP link
- CWE number
```

### Performance Concern

```markdown
[Performance] **Potential performance issue**

**Concern:** Brief description

**Code location:** Lines X-Y

**Impact:** Could affect [specific scenario]

**Suggested improvement:**
<!-- Alternative approach -->

**Estimated impact:** O(n) -> O(1) / ~X% improvement

Note: [Blocking / Non-blocking] - [context]
```

### Question

```markdown
[Question] **Seeking clarification**

I see [observation about the code].

Questions:
1. Is this intentional because [hypothesis]?
2. [Follow-up question]

If intentional, could you add a comment explaining the reasoning?
```

### Praise

```markdown
[Nice] **Good pattern**

Great use of [pattern/technique] here.

This [specific benefit]. I'll reference this as an example
for the team.
```

### FYI/Educational

```markdown
[FYI] **For your awareness**

[Educational information or tip]

This doesn't require any changes - just thought you might
find it useful.

Reference: [Link to docs/article]
```

---

## AI Review Configuration

### CodeRabbit Configuration (.coderabbit.yaml)

```yaml
language: en
tone_instructions: >
  Be direct but constructive. Use conventional comment prefixes:
  [Required], [Suggestion], [Question], [Nitpick].
  Focus on logic, security, and architecture over style.

early_access: false

reviews:
  profile: chill # Options: chill, default, assertive
  request_changes_workflow: false
  high_level_summary: true
  high_level_summary_placeholder: "@coderabbitai summary"
  poem: false
  review_status: true
  collapse_walkthrough: true
  path_instructions:
    - path: "**/*.ts"
      instructions: "Ensure TypeScript strict mode compliance"
    - path: "**/api/**"
      instructions: "Check for input validation and auth"
    - path: "**/migrations/**"
      instructions: "Verify reversibility and performance"

chat:
  auto_reply: true

knowledge_base:
  learnings:
    scope: local # local or global
```

### GitHub Copilot Review Settings

Configure via repository settings or in PR:

```markdown
@copilot review this PR focusing on:
- Security vulnerabilities
- Error handling gaps
- Test coverage
- Performance implications

Ignore:
- Formatting (handled by linter)
- Import ordering
```

### Custom AI Rules File (.ai-review-rules.md)

```markdown
# Project AI Review Rules

## Must Flag
- SQL queries without parameterization
- Missing authentication checks on endpoints
- Hardcoded credentials or API keys
- Console.log in production code
- Empty catch blocks
- TODO without issue reference

## Ignore
- Line length (handled by linter)
- Import order (handled by linter)
- Trailing whitespace (handled by linter)

## Patterns to Suggest
- Use Result<T, E> instead of throwing
- Prefer const over let
- Use early returns over nested if
- Destructure props in function signature

## Project-Specific
- All API endpoints must use ApiResponse wrapper
- Database queries must use Repository pattern
- Dates must use DateService, not new Date()
```

---

## Review Summary Templates

### Approval

```markdown
## Review Summary: Approved

**Reviewer:** @name
**Date:** YYYY-MM-DD

### Assessment
- Correctness: Good
- Design: Follows patterns
- Testing: Adequate coverage
- Security: No concerns

### Highlights
- [Nice] Good use of [pattern] in [file]
- Clean separation of concerns

### Minor Suggestions (optional)
- [Suggestion] Consider X in future iterations

Approved for merge.
```

### Request Changes

```markdown
## Review Summary: Changes Requested

**Reviewer:** @name
**Date:** YYYY-MM-DD

### Blocking Issues (must fix)
1. [Required] Security issue in auth.ts:45
2. [Required] Missing error handling in api.ts:23

### Suggestions (consider)
1. [Suggestion] Performance improvement in query
2. [Suggestion] Add integration test

### Questions (need answers)
1. [Question] Why custom implementation instead of library?

Please address blocking issues. Happy to re-review once updated.
```

### AI Review Summary

```markdown
## AI Review Summary

**Tool:** CodeRabbit / Copilot / Claude
**Date:** YYYY-MM-DD

### Automated Findings
| Category | Count | Status |
|----------|-------|--------|
| Security | 2 | Addressed |
| Performance | 1 | Dismissed (see note) |
| Style | 5 | Addressed |
| Tests | 1 | Addressed |

### Dismissed with Reason
- **Performance #1:** AI suggested caching, but data changes frequently.
  Not appropriate for this use case.

### Changes Made from AI Feedback
- Fixed SQL injection (security #1, #2)
- Added missing null check (style #3)
- Added edge case test (tests #1)
```
