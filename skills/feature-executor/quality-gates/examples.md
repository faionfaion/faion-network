# Quality Gates Examples

## Example 1: Successful Post-Task Validation

### Task

```
TASK-001-user-authentication
```

### Validation Steps

```
Post-Task Validation: TASK-001-user-authentication

1. Running tests...
   Command: pytest -v --cov=app.auth --cov-report=term-missing
   Result: 12/12 passed ✅
   Duration: 2.3s

2. Checking coverage...
   Coverage: 85%
   Threshold: 80%
   Status: PASS ✅

3. Verifying build...
   Command: python -m py_compile app/auth/*.py
   Result: SUCCESS ✅

4. Running project...
   Command: python manage.py check
   Result: System check identified no issues ✅

5. Hallucination check...
   Agent: faion-hallucination-checker-agent
   Status: VERIFIED ✅

Post-Task Validation: SUCCESS
```

## Example 2: Test Failure with Retry

### Task

```
TASK-002-payment-integration
```

### Validation with Failures

```
Post-Task Validation: TASK-002-payment-integration

1. Running tests... (Attempt 1)
   Command: npm test -- --coverage
   Result: 8/10 passed ❌
   Failures:
   - test_charge_declined: AssertionError
   - test_refund_flow: Timeout

   Analyzing failures...
   Fix: Updated mock responses for declined charges
   Fix: Increased timeout for async refund test

2. Running tests... (Attempt 2)
   Command: npm test -- --coverage
   Result: 9/10 passed ❌
   Failures:
   - test_refund_flow: Still timing out

   Analyzing failures...
   Fix: Changed to proper async/await pattern

3. Running tests... (Attempt 3)
   Command: npm test -- --coverage
   Result: 10/10 passed ✅

2. Checking coverage...
   Coverage: 82%
   Threshold: 80%
   Status: PASS ✅

Post-Task Validation: SUCCESS (after 3 attempts)
```

## Example 3: Coverage Below Threshold

### Task

```
TASK-003-notification-service
```

### Coverage Warning

```
Post-Task Validation: TASK-003-notification-service

1. Running tests...
   Command: go test -v -cover ./...
   Result: 15/15 passed ✅

2. Checking coverage...
   Coverage: 72%
   Threshold: 80%
   Status: WARNING ⚠️

   Uncovered lines:
   - notification/service.go:45-52 (error handling)
   - notification/templates.go:23-28 (template parsing)

   Action: Generating missing tests...

   Running tests again...
   Command: go test -v -cover ./...
   Result: 20/20 passed ✅
   Coverage: 83%
   Status: PASS ✅

Post-Task Validation: SUCCESS (coverage improved)
```

## Example 4: Build Failure

### Task

```
TASK-004-api-endpoints
```

### Build Error Recovery

```
Post-Task Validation: TASK-004-api-endpoints

1. Running tests...
   Result: 25/25 passed ✅

2. Checking coverage...
   Coverage: 88%
   Status: PASS ✅

3. Verifying build... (Attempt 1)
   Command: npm run build
   Result: FAILED ❌
   Error: TS2304: Cannot find name 'UserDto'

   Analyzing error...
   Fix: Added missing import for UserDto

4. Verifying build... (Attempt 2)
   Command: npm run build
   Result: SUCCESS ✅

5. Running project...
   Command: npm run start:dev
   Result: Server listening on port 3000 ✅

Post-Task Validation: SUCCESS (after build fix)
```

## Example 5: Code Review Cycle - Clean

### Feature

```
feature-001-user-management
```

### Review Iteration

```
Code Review Cycle: Iteration 1

Running code review...
Agent: faion-code-agent
Files: 8 changed

Review Results:
├─ Style issues: 3
│   ├─ app/models/user.py:12 - Unused import 'datetime'
│   ├─ app/services/user.py:45 - Line too long (89 > 79)
│   └─ app/views/user.py:23 - Missing blank line
│
├─ Documentation: 2
│   ├─ app/services/user.py:15 - Missing docstring
│   └─ app/services/user.py:67 - Missing docstring

Auto-fixing issues...
├─ Removed unused import ✅
├─ Reformatted long line ✅
├─ Added blank line ✅
├─ Added docstring for create_user() ✅
├─ Added docstring for delete_user() ✅

Re-running tests...
Result: 12/12 passed ✅

Code Review Cycle: Iteration 2

Running code review...
Agent: faion-code-agent

Review Results: CLEAN ✅

Final Status: PASSED (2 iterations, 5 issues fixed)
```

## Example 6: Code Review Cycle - Multiple Iterations

### Feature

```
feature-002-checkout-flow
```

### Multiple Review Cycles

```
Code Review Cycle: Iteration 1

Review Results: 8 issues found
├─ Style: 5 (auto-fixed)
├─ Security: 1 (XSS in payment form)
├─ Missing: 2 (test cases)

Fixes applied:
├─ Style issues auto-fixed ✅
├─ Security: Sanitized user input ✅
├─ Generated tests for edge cases ✅

Code Review Cycle: Iteration 2

Review Results: 3 issues found
├─ Style: 1 (import order)
├─ Performance: 1 (N+1 query)
├─ Missing: 1 (error handling docs)

Fixes applied:
├─ Import order fixed ✅
├─ Optimized with select_related() ✅
├─ Added error handling docstring ✅

Code Review Cycle: Iteration 3

Review Results: 1 issue found
├─ Missing: Integration test for full checkout

Fixes applied:
├─ Generated integration test ✅

Code Review Cycle: Iteration 4

Review Results: CLEAN ✅

Final Status: PASSED (4 iterations, 12 issues fixed)
```

## Example 7: Review Cycle Max Iterations

### Feature

```
feature-003-analytics-dashboard
```

### Max Iterations Reached

```
Code Review Cycle: Iterations 1-4

[... multiple iterations with fixes ...]

Code Review Cycle: Iteration 5

Review Results: 2 issues found
├─ Performance: Complex query optimization needed
├─ Missing: Comprehensive integration tests

Note: Maximum iterations (5) reached

Final Status: INCOMPLETE
Remaining Issues:
1. Optimize analytics query (manual review needed)
2. Add integration tests for dashboard widgets

Action Required: Manual review and fixes
```

## Example 8: Hallucination Check - Verified

### Task

```
TASK-005-email-templates
```

### Verification Process

```
Hallucination Check: TASK-005-email-templates

CLAIMED: SUCCESS
- Created: app/templates/email/welcome.html
- Created: app/templates/email/reset_password.html
- Created: app/services/email.py
- Tests: 8/8 passed
- Coverage: 90%

VERIFICATION:
1. File existence...
   ✅ app/templates/email/welcome.html exists (142 lines)
   ✅ app/templates/email/reset_password.html exists (156 lines)
   ✅ app/services/email.py exists (215 lines)

2. Tests verification...
   Running: pytest tests/test_email.py -v
   ✅ 8/8 tests passed

3. Coverage verification...
   Running: pytest --cov=app.services.email
   ✅ Coverage: 90% (matches claim)

4. Build verification...
   Running: python -m py_compile app/services/email.py
   ✅ No syntax errors

5. Acceptance criteria...
   ✅ AC-1: Welcome email template created
   ✅ AC-2: Password reset template created
   ✅ AC-3: EmailService with send methods
   ✅ AC-4: Tests for all email types

Status: VERIFIED
All claims accurate with evidence.
```

## Example 9: Hallucination Check - Partial

### Task

```
TASK-006-user-dashboard
```

### Partial Verification

```
Hallucination Check: TASK-006-user-dashboard

CLAIMED: SUCCESS
- Created: frontend/pages/dashboard.tsx
- Modified: frontend/components/Header.tsx
- Tests: 15/15 passed
- Coverage: 85%

VERIFICATION:
1. File existence...
   ✅ frontend/pages/dashboard.tsx exists (320 lines)
   ❌ frontend/components/Header.tsx not modified (last change: 2 days ago)

2. Tests verification...
   Running: npm test dashboard
   ⚠️ 12/15 tests passed (not 15/15)

3. Coverage verification...
   Running: npm test -- --coverage
   ⚠️ Coverage: 78% (not 85%)

Status: PARTIAL
Discrepancies:
1. Header.tsx was not actually modified
2. Only 12/15 tests pass (not 15/15)
3. Coverage is 78% (not 85%)

Action: Re-run task validation
```

## Example 10: Configuration Defaults

### Project Without Constitution Settings

```
Loading configuration...

constitution.md: No testing section found
Using defaults:

Testing:
  Framework: pytest (detected from requirements.txt)
  Command: pytest -v --cov
  Coverage threshold: 80% (default)

Build:
  Command: python -m py_compile (default for Python)
  Run command: python manage.py runserver

Quality:
  Max review iterations: 5 (default)
  Max task retries: 3 (default)

Configuration loaded successfully with defaults.
```
