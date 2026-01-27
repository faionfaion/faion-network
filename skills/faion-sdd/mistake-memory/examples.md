# Mistake Examples

Real-world examples of mistakes, their analysis, and prevention strategies.

## LLM-Specific Mistakes

### MIS_2024_001: API Hallucination

**Category:** Hallucination - API
**Severity:** Medium

**What Happened:**
LLM generated code using `response.getData()` method that doesn't exist in the axios library. Code passed syntax check but failed at runtime.

**Timeline:**
- 10:00 - Requested LLM to write API client
- 10:05 - LLM generated code with confident-looking API calls
- 10:10 - Code failed with "getData is not a function"
- 10:15 - Manual review found hallucinated method

**Root Cause Analysis:**
1. Why did code fail? → Used non-existent method
2. Why was it generated? → LLM pattern-matched from similar APIs
3. Why wasn't it caught? → No type checking, no tests before integration
4. Why no verification? → Trusted LLM output too much
5. Root cause: Missing verification step for LLM-generated API calls

**Prevention:**
```yaml
rule:
  id: PREV_001
  trigger: task_contains
  keywords: ["API", "client", "axios", "fetch"]
  action: require_checklist
  checklist: api-implementation
  message: "Verify all API methods against official documentation"
```

**Checklist Addition:**
- [ ] Verify every method call against library documentation
- [ ] Run TypeScript compilation before integration
- [ ] Write at least one test that exercises the API call

---

### MIS_2024_002: Context Window Loss

**Category:** Context - Window Limit
**Severity:** High

**What Happened:**
During a large refactoring task, the LLM "forgot" the coding standards from the beginning of the conversation. Generated code used different naming conventions, missing error handling patterns that were specified earlier.

**Timeline:**
- Started with 2000-line file refactoring
- First 500 lines followed standards perfectly
- By line 1500, naming conventions drifted
- Error handling patterns were inconsistent
- Review caught 47 style violations

**Root Cause Analysis:**
1. Why inconsistent? → LLM lost earlier context
2. Why lost? → Context window exceeded
3. Why exceeded? → Single large task without chunking
4. Why not chunked? → Assumed LLM could handle full file
5. Root cause: Task too large for context window

**Prevention:**
```yaml
rule:
  id: PREV_002
  trigger: file_size
  threshold: 500_lines
  action: warn
  message: "Large file detected. Break into chunks of 200-300 lines. See MIS_2024_002."
```

**Process Change:**
- Max 300 lines per LLM request
- Include coding standards summary with each chunk
- Verify consistency across chunks before merging

---

### MIS_2024_003: Confident Fabrication

**Category:** Hallucination - Factual
**Severity:** Medium

**What Happened:**
LLM confidently stated that React 19 had a `useAsyncState` hook built-in. Developer implemented code using this non-existent hook, wasting 2 hours debugging.

**Timeline:**
- Asked LLM about best practices for async state
- LLM recommended "React 19's built-in useAsyncState hook"
- Developer trusted recommendation
- 2 hours spent debugging import errors
- Finally discovered hook doesn't exist

**Root Cause Analysis:**
1. Why debugging? → Hook doesn't exist
2. Why recommended? → LLM hallucinated based on patterns
3. Why trusted? → LLM was confident, no citation
4. Why no verification? → Assumed LLM knew React 19
5. Root cause: Trusted LLM for factual claims without verification

**Prevention:**
```yaml
rule:
  id: PREV_003
  trigger: mentions_new_feature
  patterns: ["new in", "introduced in", "React 19", "latest version"]
  action: warn
  message: "LLM may hallucinate new features. Verify against official docs."
```

**Behavioral Change:**
- Always verify new API/feature claims against official documentation
- Ask LLM for documentation links (even if hallucinated, reveals uncertainty)
- Use multi-model verification for factual claims

---

## Traditional Development Mistakes

### MIS_2024_010: Database Migration Without Backup

**Category:** Data Handling
**Severity:** Critical

**What Happened:**
Ran destructive migration (`DROP COLUMN`) on production without backup. Lost 2 weeks of data in dropped column.

**Timeline:**
- 10:00 - Started migration script
- 10:02 - Migration completed successfully
- 10:30 - User report: missing data
- 11:00 - Confirmed data loss
- 14:00 - Restored from nightly backup (lost 12 hours)

**Impact:**
- 12 hours of data lost
- 4 hours downtime
- 50 users affected
- 16 developer hours for recovery

**Root Cause Analysis:**
1. Why data lost? → Column was dropped
2. Why no backup? → No pre-migration backup procedure
3. Why no procedure? → Migration process never formalized
4. Why not formalized? → Team grew fast, process didn't scale
5. Root cause: Missing process for destructive database operations

**Prevention:**
```yaml
rule:
  id: PREV_010
  trigger: file_pattern
  pattern: "DROP (TABLE|COLUMN)"
  file_types: ["*.sql", "migrations/*"]
  action: block
  message: "Destructive migration detected. Backup required. See MIS_2024_010."
```

**Checklist Addition (database-migration):**
- [ ] Take full backup before any schema change (FIRST ITEM)
- [ ] Verify rollback procedure exists and tested
- [ ] Run migration on staging first
- [ ] Have recovery plan documented

---

### MIS_2024_015: Hardcoded API Key in Commit

**Category:** Security
**Severity:** Critical

**What Happened:**
Developer committed AWS credentials to public repository. Credentials were harvested by bot within 15 minutes, resulting in $2,400 cloud bill.

**Timeline:**
- 14:00 - Committed code with hardcoded AWS_SECRET_KEY
- 14:15 - Bot harvested credentials from GitHub
- 14:30 - Crypto mining instances spawned
- 16:00 - AWS billing alert received
- 16:30 - Credentials rotated, instances terminated

**Impact:**
- $2,400 unauthorized charges
- 2.5 hours incident response
- Full credential rotation required
- Security audit triggered

**Root Cause Analysis:**
1. Why charges? → Unauthorized resource usage
2. Why unauthorized? → Credentials compromised
3. Why compromised? → Committed to public repo
4. Why committed? → No pre-commit secret scanning
5. Root cause: Missing secret detection in development workflow

**Prevention:**
```yaml
rule:
  id: PREV_015
  trigger: file_pattern
  patterns:
    - "AWS_SECRET"
    - "api_key.*=.*['\"][a-zA-Z0-9]{20,}"
    - "password.*=.*['\"]"
  action: block
  message: "Potential secret detected. Use environment variables. See MIS_2024_015."
```

**Process Changes:**
- Install pre-commit hook with secret scanning
- Use git-secrets or gitleaks in CI
- Store all secrets in environment variables
- Regular credential rotation

---

### MIS_2024_020: Missing Error Handling in Payment Flow

**Category:** Implementation
**Severity:** High

**What Happened:**
Payment processing code lacked proper error handling. Network timeout caused silent failure, user was charged but order wasn't created.

**Timeline:**
- User initiated payment
- Payment processed successfully
- Network timeout during order creation
- Exception not caught, silently failed
- User charged, no order, no notification
- Discovered 3 days later from support ticket

**Impact:**
- 12 users affected over 3 days
- $1,800 in refunds processed
- Trust damage, negative reviews
- 8 hours to identify and fix

**Root Cause Analysis:**
1. Why no order? → Order creation failed
2. Why silent? → Exception not caught
3. Why not caught? → Missing try/catch in async flow
4. Why missing? → Code review didn't catch it
5. Root cause: Insufficient error handling review for payment flows

**Prevention:**
```yaml
rule:
  id: PREV_020
  trigger: file_path
  patterns: ["payment", "checkout", "billing", "subscription"]
  action: require_checklist
  checklist: payment-implementation
  message: "Payment code detected. Full error handling review required."
```

**Checklist Addition (payment-implementation):**
- [ ] Every async operation has try/catch
- [ ] All failure paths logged with context
- [ ] User notified of any failure
- [ ] Idempotency implemented (safe to retry)
- [ ] Transaction rollback on partial failure

---

## Estimation Mistakes

### MIS_2024_025: Third-Party Integration Underestimated

**Category:** Estimation
**Severity:** Medium

**What Happened:**
Estimated 2 days for Stripe integration. Actual time was 8 days due to undocumented edge cases, webhook reliability issues, and testing complexity.

**Factors Missed:**
- Webhook retry logic and idempotency
- Test mode vs production differences
- Error handling for all decline codes
- Subscription lifecycle complexity
- PCI compliance requirements

**Root Cause Analysis:**
1. Why 4x overrun? → Many unknown unknowns
2. Why unknown? → First time integrating payments
3. Why not anticipated? → Optimistic estimation
4. Why optimistic? → Based on documentation, not experience
5. Root cause: Third-party integrations have hidden complexity

**Prevention:**
```yaml
rule:
  id: PREV_025
  trigger: task_keywords
  keywords: ["integration", "third-party", "API", "payment", "auth provider"]
  action: suggest
  message: "Consider spike first. Past integrations took 2-4x estimated. See MIS_2024_025."
```

**Estimation Adjustment:**
- Add 2x multiplier for any third-party integration
- Require spike/POC for unfamiliar services
- Include webhook handling in estimates
- Account for testing complexity

---

## Pattern Summary

| Category | Common Root Causes | Prevention Theme |
|----------|-------------------|------------------|
| Hallucination | Missing context, overconfidence in LLM | Verification, documentation in context |
| Context Loss | Large tasks, long conversations | Chunking, context refresh |
| Data Handling | Missing procedures, shortcuts | Checklists, automation |
| Security | No automated checks, time pressure | Pre-commit hooks, CI scanning |
| Implementation | Insufficient review, edge cases | Comprehensive checklists, testing |
| Estimation | Optimism, unfamiliarity | Multipliers, spikes, historical data |
