# Execution Workflow Examples

## Example 1: Django Authentication Feature

### Input

```
/faion-feature-executor cashflow-planner 01-auth
```

### Context Loaded

```
Constitution: cashflow-planner
- Tech: Django 5.1, Python 3.11, PostgreSQL
- Testing: pytest, 80% coverage
- Build: docker-compose up
- Format: black, isort, flake8

Feature: 01-auth
- Spec: 5 FR (user model, auth service, JWT, permissions, email)
- Design: 3 AD (custom user, token refresh, email templates)
- Tasks: 4 in todo/
```

### Execution Output

```
Loading context...
- Constitution: cashflow-planner (Django 5.x, pytest, 80% coverage)
- Feature: 01-auth (4 tasks in todo/)
- Spec: 5 FR, Design: 3 AD

Executing tasks:

TASK-001-user-model ━━━━━━━━━━ EXECUTING
├─ Creating User model with email auth...
├─ Running tests... 12/12 ✅
├─ Coverage: 85%
└─ Status: SUCCESS

TASK-002-auth-service ━━━━━━━━━━ EXECUTING
├─ Creating AuthService with JWT...
├─ Running tests... 8/8 ✅
├─ Coverage: 82%
└─ Status: SUCCESS

TASK-003-permissions ━━━━━━━━━━ EXECUTING
├─ Adding permission system...
├─ Running tests... 15/15 ✅
├─ Coverage: 88%
└─ Status: SUCCESS

TASK-004-email-verification ━━━━━━━━━━ EXECUTING
├─ Email verification flow...
├─ Running tests... 10/10 ✅
├─ Coverage: 90%
└─ Status: SUCCESS

Code Review Cycle:
├─ Iteration 1: 5 issues found
│   ├─ Fixed: 3 style issues (black, isort)
│   ├─ Fixed: 2 missing docstrings
├─ Iteration 2: 0 issues ✅
└─ Status: CLEAN

Feature completed:
- Tasks: 4/4
- Coverage: 88%
- Review: PASSED
- Moved to: .aidocs/done/01-auth
```

## Example 2: React Landing Page (Resume)

### Input

```
/faion-feature-executor faion-net 02-landing-page
```

### State Found

```
Feature: 02-landing-page (in-progress)
- 1 task in in-progress/: TASK-002
- 3 tasks in todo/: TASK-003, TASK-004, TASK-005
- 1 task in done/: TASK-001
```

### Execution Output

```
Skill: Found 1 task in in-progress/, 3 in todo/
Resuming from TASK-002...

TASK-002-hero-section ━━━━━━━━━━ RESUMING
├─ Previous progress: 60% (components created)
├─ Completing implementation...
├─ Adding responsive styles...
├─ Running tests... 15/15 ✅
└─ Status: SUCCESS

TASK-003-features-section ━━━━━━━━━━ EXECUTING
├─ Creating features grid...
├─ Running tests... 8/8 ✅
└─ Status: SUCCESS

TASK-004-cta-section ━━━━━━━━━━ EXECUTING
├─ Creating CTA with form...
├─ Running tests... 12/12 ✅
└─ Status: SUCCESS

TASK-005-seo-metadata ━━━━━━━━━━ EXECUTING
├─ Adding SEO tags and Open Graph...
├─ Running tests... 5/5 ✅
└─ Status: SUCCESS

Code Review: CLEAN (1 iteration)

Feature completed:
- Tasks: 5/5
- Coverage: 92%
- Review: PASSED
```

## Example 3: Go Microservice (Build Failure)

### Input

```
/faion-feature-executor payment-service 03-webhooks
```

### Execution with Failure

```
TASK-001-webhook-receiver ━━━━━━━━━━ EXECUTING
├─ Creating webhook handler...
├─ Running tests... 10/10 ✅
└─ Status: SUCCESS

TASK-002-signature-validation ━━━━━━━━━━ EXECUTING
├─ Adding signature validation...
├─ Running tests... 8/8 ✅
├─ Build verification... ❌ FAILED
│   Error: undefined: crypto.ValidateHMAC
├─ Attempt 1: Importing crypto package...
├─ Running tests... 8/8 ✅
├─ Build verification... ✅ SUCCESS
└─ Status: SUCCESS (retry)

TASK-003-event-processing ━━━━━━━━━━ EXECUTING
├─ Event processing pipeline...
├─ Running tests... 12/12 ✅
└─ Status: SUCCESS

Code Review:
├─ Iteration 1: 3 issues
│   ├─ Security: Missing rate limiting
│   ├─ Style: gofmt needed
│   ├─ Missing: Error handling docs
├─ Fixes applied...
├─ Iteration 2: CLEAN ✅

Feature completed: 3/3 tasks
```

## Example 4: Partial Failure (Test Issues)

### Input

```
/faion-feature-executor mobile-app 04-notifications
```

### Execution with Partial Failure

```
TASK-001-fcm-setup ━━━━━━━━━━ EXECUTING
├─ Firebase Cloud Messaging setup...
├─ Running tests... 5/5 ✅
└─ Status: SUCCESS

TASK-002-notification-service ━━━━━━━━━━ EXECUTING
├─ Creating notification service...
├─ Running tests... 8/10 ❌ FAILED
│   Error: Timeout in async notification test
├─ Attempt 1: Increasing timeout...
├─ Running tests... 9/10 ❌ FAILED
├─ Attempt 2: Mocking external service...
├─ Running tests... 8/10 ❌ FAILED
├─ Attempt 3: Debugging test...
├─ Running tests... 8/10 ❌ FAILED
└─ Status: FAILED (max retries)

# Feature Execution: mobile-app/04-notifications

## Status: PARTIAL

### Summary
| Metric | Value |
|--------|-------|
| Tasks Completed | 1/4 |
| Tasks Failed | 1 |
| Blockers | 2 |

### Failed Tasks

| Task | Status | Reason | Attempts |
|------|--------|--------|----------|
| TASK-002 | FAILED | Async test timeout | 3 |
| TASK-003 | BLOCKED | Depends on TASK-002 | - |
| TASK-004 | BLOCKED | Depends on TASK-002 | - |

### Required Actions
1. Manually debug TASK-002 async notification test
2. Check Firebase mock configuration
3. Re-run feature executor after fix
```

## Example 5: Code Review Iterations

### Input

```
/faion-feature-executor blog-platform 05-editor
```

### Multiple Review Iterations

```
TASK-001-rich-text-editor ━━━━━━━━━━ SUCCESS
TASK-002-markdown-support ━━━━━━━━━━ SUCCESS
TASK-003-image-upload ━━━━━━━━━━ SUCCESS

Code Review Cycle:
├─ Iteration 1: 8 issues found
│   ├─ Style: 5 formatting issues → auto-fixed
│   ├─ Security: XSS vulnerability in markdown → manually fixed
│   ├─ Missing: 2 test cases → generated
│
├─ Iteration 2: 3 issues found
│   ├─ Style: 1 import order → auto-fixed
│   ├─ Missing: Error handling docstring → added
│   ├─ Performance: Inefficient image resize → optimized
│
├─ Iteration 3: 1 issue found
│   ├─ Missing: Integration test for upload → generated
│
├─ Iteration 4: CLEAN ✅

Final Status: PASSED (4 iterations)
```

## Example 6: Feature with Complex Dependencies

### Input

```
/faion-feature-executor ecommerce 06-checkout
```

### Task Dependency Handling

```
Context loaded:
- Tasks: 6 total
- Dependencies detected:
  - TASK-002 depends on TASK-001
  - TASK-003 depends on TASK-001
  - TASK-004 depends on TASK-002, TASK-003
  - TASK-005 depends on TASK-004
  - TASK-006 depends on TASK-005

Execution order (dependency-sorted):
1. TASK-001-cart-model
2. TASK-002-payment-integration (after 1)
3. TASK-003-shipping-calculator (after 1)
4. TASK-004-order-processing (after 2, 3)
5. TASK-005-confirmation-email (after 4)
6. TASK-006-admin-dashboard (after 5)

TASK-001-cart-model ━━━━━━━━━━ SUCCESS
TASK-002-payment-integration ━━━━━━━━━━ SUCCESS
TASK-003-shipping-calculator ━━━━━━━━━━ SUCCESS
TASK-004-order-processing ━━━━━━━━━━ SUCCESS
TASK-005-confirmation-email ━━━━━━━━━━ SUCCESS
TASK-006-admin-dashboard ━━━━━━━━━━ SUCCESS

Feature completed: 6/6 tasks (dependency-ordered)
```

## Example 7: Empty Task Queue

### Input

```
/faion-feature-executor api-service 07-analytics
```

### All Tasks Already Done

```
Loading context...
- Feature: 07-analytics (in .aidocs/done/)
- All tasks in done/ subfolder

Task Discovery:
├─ in-progress/: 0 tasks
├─ todo/: 0 tasks
├─ done/: 4 tasks
└─ Status: NO_TASKS

Result: All tasks completed. Feature already in done/.
```
