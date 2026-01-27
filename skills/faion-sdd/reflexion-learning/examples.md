# Learning from Mistakes - Examples

Real-world examples of Reflexion in action for SDD workflows.

## Example 1: Database Migration Failure

### Initial Task

```markdown
# TASK-055: Add user preferences table

Add a new `user_preferences` table with default values migration.
```

### First Attempt (Failed)

**Action:** Created migration, ran in staging.

**Result:** Migration timed out after 30 minutes.

**Feedback:**
```
Error: Lock wait timeout exceeded; statement killed
Affected rows: 0 of 2,847,392
```

### Reflection

```markdown
## Reflection: TASK-055 Attempt 1

**Outcome:** Failure
**Duration:** 45 minutes wasted

**What went wrong:**
Migration locked the users table while trying to add default values
for 2.8M rows in a single transaction.

**5 Whys:**
1. Why did migration timeout? Transaction too large
2. Why was transaction large? Default values for all rows
3. Why all rows at once? Single ALTER statement
4. Why single statement? Didn't consider data volume
5. Why not consider volume? No pre-check in workflow

**Root cause:** No data volume assessment before migration planning

**Prevention:**
1. Always run SELECT COUNT(*) on affected tables
2. For >100k rows, use batched updates
3. Add NOT NULL with default in two steps:
   - First: Add column as nullable
   - Second: Batch update, then set NOT NULL
```

### Second Attempt (Success)

**Loaded from reflection:**
- Use batched approach for large tables
- Check row count first

**Action:**
```sql
-- Step 1: Add nullable column
ALTER TABLE users ADD COLUMN preferences JSONB;

-- Step 2: Batch update (100k rows per batch)
DO $$
DECLARE
  batch_size INT := 100000;
  affected INT;
BEGIN
  LOOP
    UPDATE users
    SET preferences = '{}'::jsonb
    WHERE id IN (
      SELECT id FROM users
      WHERE preferences IS NULL
      LIMIT batch_size
    );
    GET DIAGNOSTICS affected = ROW_COUNT;
    EXIT WHEN affected = 0;
    COMMIT;
  END LOOP;
END $$;

-- Step 3: Add constraint
ALTER TABLE users ALTER COLUMN preferences SET NOT NULL;
```

**Result:** Completed in 8 minutes with zero downtime.

### Memory Update

**Pattern added:**

```markdown
## PAT-2024-015: Large Table Migration

**Context:** Database migrations on tables with >100k rows
**Problem:** Single-transaction migrations timeout or lock tables
**Solution:**
1. Check row count: SELECT COUNT(*)
2. If >100k: Use batched approach
3. Split ALTER into: add nullable -> batch update -> add constraint
**Confidence:** 0.5 (new pattern)
**Source:** TASK-055
```

**Mistake added:**

```markdown
## MIS-2024-008: Migration Without Data Assessment

**Severity:** High
**Context:** Any migration touching existing data
**What happened:** 45-minute timeout, blocked deployment
**Root cause:** No pre-migration data volume check
**Prevention:** Always run COUNT(*) before planning migration
**Occurrence:** 1
```

## Example 2: API Integration Error

### Initial Task

```markdown
# TASK-078: Integrate payment provider API

Connect to Stripe API for subscription billing.
```

### First Attempt (Partial)

**Action:** Implemented Stripe integration following their docs.

**Result:** Works for new subscriptions, fails on webhook handling.

**Feedback:**
```
TypeError: Cannot read property 'id' of undefined
at processWebhook (stripe.ts:142)
```

### Reflection

```markdown
## Reflection: TASK-078 Attempt 1

**Outcome:** Partial
**Worked:** Subscription creation
**Failed:** Webhook processing

**What went wrong:**
Assumed webhook payload always has `data.object.id` but some
events have different structures.

**Analysis:**
- `customer.subscription.created` has `data.object.id`
- `payment_intent.succeeded` has `data.object.payment_method`
- Some events are nested differently

**Root cause:** Assumed consistent API response structure

**Prevention:**
1. Always validate webhook payload structure
2. Use Stripe SDK types for type safety
3. Test all webhook event types, not just happy path
```

### Second Attempt (Success)

**Loaded from reflection:**
- Validate payload structure
- Test all event types

**Action:**
```typescript
function processWebhook(event: Stripe.Event) {
  // Type-safe event handling
  switch (event.type) {
    case 'customer.subscription.created':
      const subscription = event.data.object as Stripe.Subscription;
      handleSubscription(subscription.id, subscription.status);
      break;

    case 'payment_intent.succeeded':
      const intent = event.data.object as Stripe.PaymentIntent;
      handlePayment(intent.id, intent.amount);
      break;

    default:
      console.log(`Unhandled event type: ${event.type}`);
  }
}
```

**Result:** All webhook events handled correctly.

### Memory Update

**Pattern added:**

```markdown
## PAT-2024-022: API Response Validation

**Context:** Third-party API integrations
**Problem:** Responses vary by endpoint/event type
**Solution:**
1. Use SDK types when available
2. Implement discriminated unions for event handling
3. Add explicit handling for each event type
4. Log unhandled cases for discovery
**Confidence:** 0.6
**Source:** TASK-078
```

## Example 3: Test Coverage Gap

### Initial Task

```markdown
# TASK-091: Add email validation to signup form

Validate email format and check for existing accounts.
```

### First Attempt (Passed Review, Failed Prod)

**Action:** Added validation with unit tests.

**Result:** Passed code review, passed CI. Failed in production.

**Production feedback:**
```
Bug report: "I can't sign up with my email: user+tag@example.com"
```

### Reflection

```markdown
## Reflection: TASK-091 Post-Mortem

**Outcome:** Failure (escaped to production)
**Detection:** User bug report

**What went wrong:**
Email regex rejected valid emails with + character.
Regex used: /^[\w.-]+@[\w.-]+\.\w+$/
Failed on: user+tag@example.com

**Why tests didn't catch it:**
- Only tested happy path: test@example.com
- Only tested obvious invalid: "not-an-email"
- Didn't test edge cases: +, unicode, subdomains

**Root cause:** Insufficient test coverage for edge cases

**Prevention:**
1. Use established email validation library (not custom regex)
2. Test edge cases: +, multiple dots, subdomains, unicode
3. Add test case for RFC 5321 compliance
```

### Fix Applied

**Loaded from reflection:**
- Use library, not custom regex
- Test edge cases

**Action:**
```typescript
import { isEmail } from 'validator';

// Instead of custom regex
function validateEmail(email: string): boolean {
  return isEmail(email);
}

// Expanded tests
describe('validateEmail', () => {
  const validEmails = [
    'simple@example.com',
    'user+tag@example.com',
    'user.name@example.com',
    'user@sub.example.com',
    'user@example.co.uk',
  ];

  const invalidEmails = [
    'not-an-email',
    '@example.com',
    'user@',
    'user@.com',
  ];

  validEmails.forEach(email => {
    it(`accepts valid email: ${email}`, () => {
      expect(validateEmail(email)).toBe(true);
    });
  });

  invalidEmails.forEach(email => {
    it(`rejects invalid email: ${email}`, () => {
      expect(validateEmail(email)).toBe(false);
    });
  });
});
```

### Memory Update

**Pattern added:**

```markdown
## PAT-2024-031: Email Validation

**Context:** Form validation for email fields
**Problem:** Custom regex often fails edge cases
**Solution:**
1. Use established library (validator.js, email-validator)
2. Test: plus addressing, subdomains, TLD variations
3. Consider: unicode, quoted strings (rare but valid)
**Trade-offs:** Library adds dependency
**Confidence:** 0.7
**Source:** TASK-091
```

**Mistake added:**

```markdown
## MIS-2024-015: Custom Regex for Standards

**Severity:** Medium
**Context:** Validation of standardized formats (email, URL, UUID)
**What happened:** Custom regex rejected valid emails in production
**Root cause:** Email RFC is complex, regex is deceptively simple
**Prevention:** Use battle-tested libraries for standard formats
**Detection:** Add edge case tests for any validation
**Occurrence:** 1
```

## Example 4: Performance Regression

### Initial Task

```markdown
# TASK-102: Add user activity dashboard

Display user's recent activity with charts.
```

### First Attempt (Worked, Slow)

**Action:** Implemented dashboard with real-time data loading.

**Result:** Functional but page loads in 8 seconds.

**Feedback:** Performance monitoring alert: P95 latency > 5s

### Reflection

```markdown
## Reflection: TASK-102 Performance

**Outcome:** Partial (functional, not performant)
**P95 Latency:** 8.2 seconds (target: <2s)

**What went wrong:**
1. N+1 queries: Fetching activities, then user for each
2. No pagination: Loading all 1000+ activities
3. No caching: Recalculating aggregates on each load

**Analysis:**
- Query count: 1 + N (N = activities count)
- For user with 500 activities: 501 queries
- Each query: ~15ms
- Total: ~7.5s just in DB

**Root cause:** Didn't consider data scale during implementation

**Prevention:**
1. Always eager-load relationships
2. Implement pagination from start
3. Cache expensive aggregations
4. Add performance test for realistic data volumes
```

### Second Attempt (Optimized)

**Loaded from reflection:**
- Eager load relationships
- Paginate from start
- Cache aggregations

**Action:**
```python
# Before: N+1 queries
activities = Activity.objects.filter(user=user)
for activity in activities:
    print(activity.user.name)  # Extra query each time

# After: Single query with eager loading
activities = (
    Activity.objects
    .filter(user=user)
    .select_related('user')
    .order_by('-created_at')[:50]  # Pagination
)

# Cache aggregations
@cache_for(minutes=5)
def get_activity_summary(user_id):
    return Activity.objects.filter(user_id=user_id).aggregate(
        total=Count('id'),
        this_week=Count('id', filter=Q(created_at__gte=week_ago))
    )
```

**Result:** P95 latency: 180ms

### Memory Update

**Pattern added:**

```markdown
## PAT-2024-038: Query Optimization Checklist

**Context:** Any database-backed feature
**Problem:** N+1 queries and missing pagination cause slowdowns
**Solution:**
1. Use select_related/prefetch_related (Django) or equivalent
2. Always paginate collections (default: 50 items)
3. Cache aggregations (TTL: 5 minutes for dashboards)
4. Add performance test with realistic data volume
**Confidence:** 0.8
**Source:** TASK-102
```

## Example 5: Deployment Configuration

### Initial Task

```markdown
# TASK-115: Deploy feature flags service

Set up LaunchDarkly integration for feature flags.
```

### First Attempt (Failed)

**Action:** Added LaunchDarkly SDK, deployed to staging.

**Result:** Service crashes on startup.

**Feedback:**
```
Error: LaunchDarkly SDK key not found
Environment variable LD_SDK_KEY is undefined
```

### Reflection

```markdown
## Reflection: TASK-115 Deployment Failure

**Outcome:** Failure
**Stage:** Staging deployment

**What went wrong:**
Added code that requires LD_SDK_KEY but didn't:
1. Add to .env.example
2. Add to CI/CD secrets
3. Add to Kubernetes secrets
4. Document in deployment guide

**Root cause:** Incomplete environment variable lifecycle

**Prevention:**
For any new env var:
1. Add to .env.example with description
2. Add to CI/CD secrets (GitHub, GitLab)
3. Add to K8s secrets manifest
4. Update deployment documentation
5. Add validation on startup
```

### Second Attempt (Success)

**Loaded from reflection:**
- Complete env var lifecycle

**Action:**

```bash
# .env.example
LD_SDK_KEY=sdk-xxx-xxx  # LaunchDarkly SDK key (get from dashboard)

# kubernetes/secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
data:
  LD_SDK_KEY: <base64-encoded-value>

# startup validation
def validate_env():
    required = ['LD_SDK_KEY', 'DATABASE_URL', ...]
    missing = [var for var in required if not os.getenv(var)]
    if missing:
        raise EnvironmentError(f"Missing: {', '.join(missing)}")
```

**Result:** Deployed successfully to staging and production.

### Memory Update

**Pattern added:**

```markdown
## PAT-2024-045: Environment Variable Lifecycle

**Context:** Adding new configuration via environment variables
**Problem:** Forgetting to add env vars to all environments
**Solution:**
Checklist for each new env var:
1. [ ] .env.example with description
2. [ ] .env.local (or .env.development)
3. [ ] CI/CD secrets (GitHub/GitLab)
4. [ ] K8s secrets or ConfigMap
5. [ ] Deployment documentation
6. [ ] Startup validation code
**Confidence:** 0.85
**Source:** TASK-115
```

## Synthesized Insights

### Common Failure Patterns

| Pattern | Frequency | Root Cause |
|---------|-----------|------------|
| Data scale ignorance | 30% | Not checking production data volumes |
| Happy path only | 25% | Testing only expected inputs |
| Env var lifecycle | 15% | Incomplete configuration management |
| API assumptions | 15% | Trusting documentation blindly |
| Query performance | 15% | N+1, missing indexes, no pagination |

### Prevention Hierarchy

1. **Pre-flight checks** - Validate assumptions before coding
2. **Defensive coding** - Handle edge cases, validate inputs
3. **Comprehensive testing** - Edge cases, realistic volumes
4. **Monitoring** - Catch what tests miss
5. **Feedback loops** - Learn from production incidents

### Memory Loading Priority

When loading patterns/mistakes for a task:

| Task Type | Priority Patterns | Priority Mistakes |
|-----------|-------------------|-------------------|
| Database | Query optimization, migrations | Data scale, N+1 |
| API | Response validation, auth | Format assumptions |
| Forms | Input validation, accessibility | Edge case testing |
| Deploy | Env var lifecycle, rollback | Config incomplete |
| Performance | Caching, pagination | Query complexity |
