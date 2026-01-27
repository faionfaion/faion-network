# Quality Gate Examples

Real-world examples of gate pass/fail scenarios with analysis.

---

## L1 Gate Examples

### Example 1: L1 PASS - Clean Code

**Scenario:** New utility function added

```markdown
## L1 Gate: Syntax & Format

**PR:** #142 - Add date formatting utility
**Date:** 2026-01-25

### Automated Results

| Check | Status | Output |
|-------|--------|--------|
| Build | [x] PASS | Compiled successfully |
| Lint | [x] PASS | 0 errors, 0 warnings |
| Types | [x] PASS | No type errors |
| Format | [x] PASS | Already formatted |

### Gate Decision

- [x] PASS - Proceed to L2
- [ ] FAIL

**Confidence Score:** 100%
```

---

### Example 2: L1 FAIL - Type Errors

**Scenario:** LLM generated code with type mismatches

```markdown
## L1 Gate: Syntax & Format

**PR:** #143 - Add user profile API
**Date:** 2026-01-25

### Automated Results

| Check | Status | Output |
|-------|--------|--------|
| Build | [x] PASS | Compiled successfully |
| Lint | [x] PASS | 0 errors |
| Types | [ ] FAIL | 3 errors found |
| Format | [x] PASS | Already formatted |

### Type Errors

```
src/api/profile.ts:24:5 - error TS2322:
  Type 'string' is not assignable to type 'number'

src/api/profile.ts:31:10 - error TS2345:
  Argument of type 'undefined' is not assignable to parameter of type 'User'

src/api/profile.ts:45:3 - error TS2739:
  Type '{ name: string; }' is missing property 'email'
```

### Analysis

LLM hallucinated incorrect types. The `User` interface requires `email` but generated code only provided `name`.

### Fix Required

1. Add missing `email` property to user object
2. Fix type annotation on line 24
3. Add null check before passing to function on line 31

### Gate Decision

- [ ] PASS
- [x] FAIL - Fix type errors before proceeding

**Confidence Score:** 75% (blocked)
```

---

## L2 Gate Examples

### Example 3: L2 PASS - Good Coverage

**Scenario:** Feature with comprehensive tests

```markdown
## L2 Gate: Unit Tests

**PR:** #144 - Add password validation
**Date:** 2026-01-25

### Test Results

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Tests run | 12 | - | |
| Tests passed | 12 | 100% | [x] PASS |
| Tests failed | 0 | 0 | |
| Coverage | 94% | 80% | [x] PASS |
| New code coverage | 100% | 90% | [x] PASS |

### Test Summary

```
PASS src/validators/password.test.ts
  Password Validation
    ✓ accepts valid password with all requirements (2ms)
    ✓ rejects password shorter than 8 characters (1ms)
    ✓ rejects password without uppercase (1ms)
    ✓ rejects password without lowercase (1ms)
    ✓ rejects password without number (1ms)
    ✓ rejects password without special character (1ms)
    ✓ rejects password with spaces (1ms)
    ✓ accepts password at exactly 8 characters (1ms)
    ✓ accepts password with unicode characters (1ms)
    ✓ handles empty string (1ms)
    ✓ handles null input (1ms)
    ✓ handles undefined input (1ms)
```

### Gate Decision

- [x] PASS - Proceed to L3
- [ ] FAIL

**Confidence Score:** 97%
```

---

### Example 4: L2 FAIL - Failing Tests

**Scenario:** LLM code doesn't match test expectations

```markdown
## L2 Gate: Unit Tests

**PR:** #145 - Add email duplicate check
**Date:** 2026-01-25

### Test Results

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Tests run | 8 | - | |
| Tests passed | 6 | 100% | [ ] FAIL |
| Tests failed | 2 | 0 | |
| Coverage | 82% | 80% | [x] PASS |
| New code coverage | 75% | 90% | [ ] FAIL |

### Failed Tests

| Test | Error | Fix Status |
|------|-------|------------|
| should find duplicate with different case | Expected true, got false | [ ] Fixed |
| should handle concurrent checks | Timeout after 5000ms | [ ] Fixed |

### Analysis

1. **Case sensitivity bug:** LLM used strict equality (`===`) instead of case-insensitive comparison for email lookup
2. **Race condition:** LLM didn't implement proper locking for concurrent duplicate checks

### Root Cause

LLM training data likely contained simple examples without edge cases. The specification mentioned "case-insensitive" but LLM didn't implement it.

### Fix Required

1. Convert emails to lowercase before comparison
2. Add database-level unique constraint with case-insensitive collation
3. Implement optimistic locking or transaction isolation

### Gate Decision

- [ ] PASS
- [x] FAIL - Fix failing tests before proceeding

**Confidence Score:** 65% (blocked)
```

---

## L3 Gate Examples

### Example 5: L3 PASS - Integration Works

**Scenario:** API endpoint with database integration

```markdown
## L3 Gate: Integration Tests

**PR:** #146 - User registration endpoint
**Date:** 2026-01-25

### Integration Test Results

| Suite | Passed | Failed | Skipped |
|-------|--------|--------|---------|
| API | 5 | 0 | 0 |
| Database | 3 | 0 | 0 |
| External Services | 2 | 0 | 0 |

### API Contract Validation

| Endpoint | Method | Status |
|----------|--------|--------|
| POST /api/users | POST | [x] Valid |
| GET /api/users/:id | GET | [x] Valid |

### E2E Flow Test

```
✓ Register user flow
  ✓ POST /api/users creates user in database
  ✓ Password is hashed before storage
  ✓ Confirmation email is sent
  ✓ User can login with new credentials
  ✓ Duplicate email returns 409 Conflict
```

### Gate Decision

- [x] PASS - Proceed to L4
- [ ] FAIL

**Confidence Score:** 92%
```

---

### Example 6: L3 FAIL - API Contract Mismatch

**Scenario:** Frontend expects different response format

```markdown
## L3 Gate: Integration Tests

**PR:** #147 - Update product listing API
**Date:** 2026-01-25

### Integration Test Results

| Suite | Passed | Failed | Skipped |
|-------|--------|--------|---------|
| API | 3 | 2 | 0 |
| Database | 2 | 0 | 0 |

### API Contract Validation

| Endpoint | Method | Status |
|----------|--------|--------|
| GET /api/products | GET | [ ] Invalid |
| GET /api/products/:id | GET | [x] Valid |

### Contract Mismatch

**Expected (from spec):**
```json
{
  "data": [
    { "id": 1, "name": "Product", "price": 9.99 }
  ],
  "pagination": {
    "page": 1,
    "total": 100
  }
}
```

**Actual (from LLM):**
```json
{
  "products": [
    { "id": 1, "name": "Product", "price": "9.99" }
  ],
  "page": 1,
  "totalCount": 100
}
```

### Issues

| Issue | Severity | Description |
|-------|----------|-------------|
| 1 | High | Response wrapper uses `products` not `data` |
| 2 | High | `price` is string not number |
| 3 | Medium | `pagination` object missing, fields at root |
| 4 | Low | `totalCount` vs `total` naming |

### Analysis

LLM deviated from the specification. The design.md clearly showed the expected format, but LLM used a different convention (possibly from training data patterns).

### Fix Required

1. Rename `products` to `data`
2. Parse price as float, not string
3. Nest pagination fields in `pagination` object
4. Rename `totalCount` to `total`

### Gate Decision

- [ ] PASS
- [x] FAIL - Fix API contract violations

**Confidence Score:** 55% (blocked)
```

---

## L4 Gate Examples

### Example 7: L4 PASS with Minor Issues

**Scenario:** Code review finds minor improvements

```markdown
## L4 Gate: Code Review

**PR:** #148 - Add shopping cart service
**Author:** Claude
**Reviewer:** Human
**Date:** 2026-01-25

### Automated Checks

| Check | Status |
|-------|--------|
| Security scan (SAST) | [x] PASS |
| Dependency audit | [x] PASS |
| Complexity analysis | [x] PASS |

### Manual Review

| Criterion | Status | Notes |
|-----------|--------|-------|
| Logic correctness | [x] OK | |
| Security practices | [x] OK | |
| Performance | [x] OK | Used efficient data structures |
| Error handling | [x] OK | All paths covered |
| Code readability | [ ] ISSUE | Some magic numbers |
| Documentation | [ ] ISSUE | Missing JSDoc on public methods |
| Test quality | [x] OK | |
| Pattern adherence | [x] OK | Follows service pattern |

### Issues Found

| ID | Severity | Description | Status |
|----|----------|-------------|--------|
| 1 | Low | Magic number 30 for cart expiry | [x] Resolved |
| 2 | Low | Missing JSDoc on 3 public methods | [x] Resolved |

### Feedback

**Positive:**
- Clean separation of concerns
- Good error handling with custom exceptions
- Efficient cart calculation algorithm

**Improvements made:**
- Added `CART_EXPIRY_DAYS = 30` constant
- Added JSDoc documentation

### Gate Decision

- [x] APPROVE - Proceed to L5
- [ ] REQUEST CHANGES
- [ ] REJECT

**Confidence Score:** 88%
```

---

### Example 8: L4 FAIL - Security Issues

**Scenario:** Code review finds security vulnerabilities

```markdown
## L4 Gate: Code Review

**PR:** #149 - Add file upload feature
**Author:** Claude
**Reviewer:** Human
**Date:** 2026-01-25

### Automated Checks

| Check | Status |
|-------|--------|
| Security scan (SAST) | [ ] FAIL |
| Dependency audit | [x] PASS |
| Complexity analysis | [x] PASS |

### SAST Findings

```
HIGH: Path Traversal in file upload
  Location: src/upload/handler.ts:45
  Issue: User-controlled filename used directly in path construction
  CWE: CWE-22

HIGH: Unrestricted File Upload
  Location: src/upload/handler.ts:52
  Issue: No file type validation
  CWE: CWE-434
```

### Manual Review

| Criterion | Status | Notes |
|-----------|--------|-------|
| Logic correctness | [x] OK | |
| Security practices | [ ] ISSUE | Critical vulnerabilities |
| Performance | [ ] ISSUE | No file size limit |
| Error handling | [x] OK | |

### Security Checklist

- [ ] Input validation present - MISSING filename sanitization
- [x] No SQL injection vectors
- [x] No XSS vulnerabilities
- [x] Auth/authz correct
- [x] Secrets not hardcoded
- [ ] File type validation - MISSING

### Issues Found

| ID | Severity | Description | Status |
|----|----------|-------------|--------|
| 1 | Critical | Path traversal via filename | [ ] Open |
| 2 | Critical | No file type whitelist | [ ] Open |
| 3 | High | No file size limit | [ ] Open |
| 4 | Medium | No virus scanning | [ ] Open |

### Analysis

LLM generated a naive file upload implementation. Common security controls were not included:
- No sanitization of user-provided filename
- No validation of file extension/MIME type
- No file size limits
- Direct path construction from user input

### Required Fixes

1. Sanitize filename: strip path separators, limit characters
2. Use UUID for stored filename, keep original in metadata
3. Implement file type whitelist (check extension AND magic bytes)
4. Add file size limit (configurable, default 10MB)
5. Store files outside web root
6. Consider virus scanning for production

### Gate Decision

- [ ] APPROVE
- [x] REQUEST CHANGES - Security issues must be fixed
- [ ] REJECT

**Confidence Score:** 35% (blocked)
```

---

## L5 Gate Examples

### Example 9: L5 PASS - Staging Verified

**Scenario:** Feature successfully deployed to staging

```markdown
## L5 Gate: Staging Validation

**Release:** v2.3.0
**Environment:** staging
**Date:** 2026-01-25

### Deployment

| Step | Status | Duration |
|------|--------|----------|
| Build | [x] PASS | 2m 15s |
| Deploy | [x] PASS | 1m 30s |
| Migration | [x] PASS | 0m 45s |
| Health check | [x] PASS | 0m 05s |

### Automated Validation

| Test Suite | Passed | Failed | Duration |
|------------|--------|--------|----------|
| Smoke tests | 25 | 0 | 3m |
| Regression | 142 | 0 | 12m |
| Performance | 8 | 0 | 5m |

### Performance Results

| Metric | Actual | SLO | Status |
|--------|--------|-----|--------|
| P50 latency | 45ms | 100ms | [x] PASS |
| P99 latency | 180ms | 500ms | [x] PASS |
| Error rate | 0.02% | 0.1% | [x] PASS |
| Throughput | 850rps | 500rps | [x] PASS |

### Security Scan (DAST)

| Severity | Count | Action |
|----------|-------|--------|
| Critical | 0 | - |
| High | 0 | - |
| Medium | 1 | Tracked for next sprint |
| Low | 3 | Accepted risk |

### Manual QA

| Feature | Status | Tester |
|---------|--------|--------|
| User registration | [x] OK | QA Team |
| Shopping cart | [x] OK | QA Team |
| Checkout flow | [x] OK | QA Team |
| Payment processing | [x] OK | QA Team |

### Gate Decision

- [x] PASS - Ready for production
- [ ] FAIL

**Confidence Score:** 94%
```

---

### Example 10: L5 FAIL - Performance Regression

**Scenario:** New feature causes performance degradation

```markdown
## L5 Gate: Staging Validation

**Release:** v2.4.0
**Environment:** staging
**Date:** 2026-01-25

### Deployment

| Step | Status | Duration |
|------|--------|----------|
| Build | [x] PASS | 2m 30s |
| Deploy | [x] PASS | 1m 45s |
| Migration | [x] PASS | 3m 20s |
| Health check | [x] PASS | 0m 08s |

### Performance Results

| Metric | Actual | SLO | Status |
|--------|--------|-----|--------|
| P50 latency | 320ms | 100ms | [ ] FAIL |
| P99 latency | 2400ms | 500ms | [ ] FAIL |
| Error rate | 0.5% | 0.1% | [ ] FAIL |
| Throughput | 180rps | 500rps | [ ] FAIL |

### Analysis

Performance severely degraded after v2.4.0 deployment.

**Root Cause Investigation:**
```sql
-- New query added in product search (from LLM)
SELECT * FROM products
WHERE name LIKE '%search_term%'
ORDER BY created_at DESC;

-- EXPLAIN ANALYZE shows:
-- Seq Scan on products: 2.3s
-- No index usage, full table scan on 500k rows
```

**Issues Identified:**

| Issue | Impact | Fix |
|-------|--------|-----|
| N+1 query in search | High latency | Add eager loading |
| Missing index on search | Full table scan | Add GIN/trigram index |
| Unbounded result set | Memory pressure | Add pagination |
| No query caching | Repeated work | Add Redis cache |

### LLM Code Analysis

The LLM generated a naive database query without:
- Proper indexing consideration
- Pagination
- Caching strategy
- Query optimization

This is a common LLM pattern - generating "working" code that doesn't scale.

### Required Fixes

1. Add GIN index for text search:
   ```sql
   CREATE INDEX idx_products_name_gin ON products
   USING gin(name gin_trgm_ops);
   ```
2. Implement pagination (limit 20, offset-based)
3. Add Redis caching with 5-minute TTL
4. Use prepared statements
5. Consider full-text search (Elasticsearch) for scale

### Gate Decision

- [ ] PASS
- [x] FAIL - Performance regression must be fixed

**Confidence Score:** 40% (blocked)
```

---

## Confidence Score Examples

### High Confidence (Proceed)

```
Automated Checks: 100% pass  (0.40)
Coverage: 95% requirements   (0.19)
Risk: All mitigated          (0.20)
Traceability: 100%           (0.20)
-----------------------------------
Total Confidence: 99%

Decision: PROCEED
```

### Borderline (Review Required)

```
Automated Checks: 95% pass   (0.38)
Coverage: 80% requirements   (0.16)
Risk: 70% mitigated          (0.14)
Traceability: 90%            (0.18)
-----------------------------------
Total Confidence: 86%

Decision: CONDITIONAL PROCEED
- Review remaining 5% automated failures
- Document missing coverage
- Accept remaining risk with sign-off
```

### Low Confidence (Block)

```
Automated Checks: 70% pass   (0.28)
Coverage: 60% requirements   (0.12)
Risk: 40% mitigated          (0.08)
Traceability: 50%            (0.10)
-----------------------------------
Total Confidence: 58%

Decision: BLOCKED
- Fix failing automated checks
- Add missing test coverage
- Complete risk assessment
- Improve traceability matrix
```

---

## Lessons from Examples

### Common LLM Gate Failures

| Pattern | Detection | Prevention |
|---------|-----------|------------|
| Type mismatches | L1 typecheck | Provide type definitions in prompt |
| Missing edge cases | L2 unit tests | Include edge cases in spec |
| API contract deviation | L3 contract tests | Provide exact schema in prompt |
| Security naivety | L4 SAST + review | Security requirements in spec |
| Performance ignorance | L5 load tests | NFRs with specific targets |

### Gate Improvement Suggestions

1. **Feed failures back to LLM** - Use gate failure info in re-prompts
2. **Pattern library** - Show LLM correct patterns for common issues
3. **Early validation** - Run L1 checks during generation, not after
4. **Specification clarity** - Ambiguous specs lead to gate failures

---

*Quality Gate Examples | SDD Execution | Version 2.0*
