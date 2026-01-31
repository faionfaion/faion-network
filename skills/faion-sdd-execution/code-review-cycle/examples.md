# Code Review Cycle Examples

## Example 1: Good PR with Self-Review

### PR Description
```markdown
## Summary
Add user authentication with JWT tokens

## SDD References
| Document | Section |
|----------|---------|
| Spec | [SPEC-024](../spec.md#authentication) |
| Design | [DESIGN-024](../design.md#jwt-implementation) |
| Task | [TASK-024-03](../tasks/TASK-024-03.md) |

## Changes
- [x] Created User model with password hashing (bcrypt)
- [x] Created AuthService with login/logout
- [x] Created JWT utilities (sign/verify)
- [x] Added auth middleware for protected routes
- [x] Comprehensive test coverage (95%)

## Acceptance Criteria Verification
| AC | Status | Notes |
|----|--------|-------|
| AC-1: User can register with email/password | Verified | Unit + E2E tests |
| AC-2: User can login and receive JWT | Verified | Token expires in 24h |
| AC-3: Protected routes require valid JWT | Verified | Returns 401 if invalid |

## Testing
- [x] Unit tests added (auth.service.test.ts, jwt.test.ts)
- [x] Integration tests pass
- [x] E2E tests for login/register flow
- [x] Edge cases tested (expired token, invalid credentials)

## Checklist
- [x] Self-review completed
- [x] Tests pass locally (95% coverage)
- [x] No lint/type errors
- [x] API docs updated
- [x] No secrets committed (using env vars)
```

### Review Comment (Constructive)
```
[Nice] Good use of bcrypt for password hashing with proper salt rounds.

[Suggestion] Consider adding rate limiting to login endpoint to prevent
brute force attacks. We have a rate-limiter utility in utils/rate-limit.ts

[Question] Why is token expiry set to 24h? Most apps use 1h for access
tokens and longer-lived refresh tokens. Was this a product decision?

Approved ✅
```

### Author Response
```
Thanks for the review!

Rate limiting - Great catch! I'll add it in a follow-up PR (TASK-024-04)
to keep this PR focused. Created ticket.

Token expiry - Product decision from spec.md. We're keeping it simple
for MVP, no refresh tokens yet. Will add refresh tokens in phase 2.
```

## Example 2: PR with Required Changes

### Initial PR (Issues Found)
```javascript
// auth.service.ts
class AuthService {
  login(email, password) {
    const user = db.query("SELECT * FROM users WHERE email = '" + email + "'");
    if (user.password === password) {
      return { token: jwt.sign({ id: user.id }) };
    }
    return null;
  }
}
```

### Review Comments
```
[Required] SQL injection vulnerability on line 3.
Use parameterized queries:
const user = db.query('SELECT * FROM users WHERE email = ?', [email]);

[Required] Password comparison on line 4 is not secure.
Should use bcrypt.compare() as specified in design.md:
if (await bcrypt.compare(password, user.password_hash))

[Required] No error handling. What if db.query fails?
Add try-catch and proper error responses.

[Suggestion] Return structure is inconsistent. When login fails,
return null vs success returns object. Consider:
{ success: false, error: 'Invalid credentials' } for failures.

Request Changes ❌
```

### Fixed Version
```javascript
// auth.service.ts
class AuthService {
  async login(email: string, password: string): Promise<AuthResult> {
    try {
      const user = await db.query(
        'SELECT * FROM users WHERE email = ?',
        [email]
      );

      if (!user) {
        return { success: false, error: 'Invalid credentials' };
      }

      const isValid = await bcrypt.compare(password, user.password_hash);
      if (!isValid) {
        return { success: false, error: 'Invalid credentials' };
      }

      const token = jwt.sign({ id: user.id }, process.env.JWT_SECRET, {
        expiresIn: '24h'
      });

      return { success: true, token };
    } catch (error) {
      logger.error('Login error', error);
      return { success: false, error: 'Internal server error' };
    }
  }
}
```

### Follow-up Review
```
[Nice] All security issues addressed! SQL injection fixed,
password comparison using bcrypt, proper error handling.

[Nice] Consistent return structure makes error handling much cleaner.

Approved ✅
```

## Example 3: Review Metrics

### Team Weekly Review Metrics
```yaml
week_of: 2024-01-15
team: Backend Team

efficiency:
  time_to_first_review:
    average: "3.2 hours"
    target: "< 4 hours"
    status: "✅ on track"

  time_to_merge:
    average: "18 hours"
    target: "< 24 hours"
    status: "✅ on track"

  review_iterations:
    average: 2.1
    target: "< 3"
    status: "✅ on track"

quality:
  bugs_found_in_review: 12
  bugs_escaped_to_prod: 1
  prevention_rate: "92%"

  issues_by_type:
    security: 3
    logic_bugs: 5
    code_quality: 4

engagement:
  prs_reviewed: 24
  reviewers_participating: 5
  avg_comments_per_pr: 4.2

  feedback_distribution:
    required: 18
    suggestions: 42
    questions: 15
    praise: 31
    nitpicks: 8

trends:
  - "Security issues down 40% since adding pre-commit hooks"
  - "Review time improved 25% with smaller PRs"
  - "Team engagement up - all members reviewing regularly"

action_items:
  - "Continue encouraging small PRs (< 400 LOC)"
  - "Add automated security scanning to CI"
  - "Share knowledge from [FYI] comments in team wiki"
```

## Example 4: Post-Merge Reflexion

### Feature: User Authentication (Complete)

```yaml
feature: "User Authentication"
tasks_completed: 5
duration: "2 weeks"
total_prs: 8

what_worked_well:
  patterns:
    - "Small, focused PRs (avg 200 LOC) reviewed faster"
    - "Self-review checklist caught issues before peer review"
    - "Security checklist prevented 3 vulnerabilities"

  process:
    - "Daily review time (10am) kept reviews moving"
    - "Constructive feedback culture - lots of [Nice] comments"
    - "Pre-commit hooks caught secrets/lint early"

what_could_be_better:
  improvements:
    - "Initial design missed rate limiting - added later"
    - "Tests for edge cases came late - should be in plan"
    - "Token refresh strategy not in MVP - tech debt"

  lessons:
    - "Always include rate limiting in auth design"
    - "Security review before implementation, not after"
    - "Consider token refresh in initial design"

memory_updates:
  patterns_learned:
    - pattern: "Auth requires rate limiting from start"
      context: "authentication, security"
      file: "patterns_learned.jsonl"

  mistakes_avoided:
    - mistake: "SQL injection via string concatenation"
      prevention: "Code review caught it"
      source: "MIS_2024_042"

next_feature_improvements:
  - "Add security checklist to design review"
  - "Include rate limiting in all API designs"
  - "Test edge cases during implementation, not after"
