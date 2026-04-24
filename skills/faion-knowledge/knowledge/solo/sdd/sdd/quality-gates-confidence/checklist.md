# Quality Gate Checklists

Phase-specific checklists for quality gate validation.

---

## L1: Syntax & Format Gate

### Automated Checks

| Check | Command | Pass Criteria |
|-------|---------|---------------|
| Syntax | `npm run build` / `python -m py_compile` | Exit code 0 |
| Linter | `npm run lint` / `pylint` | 0 errors |
| Types | `tsc --noEmit` / `mypy` | 0 errors |
| Format | `prettier --check` / `black --check` | No changes needed |

### Checklist

```markdown
## L1 Gate: Syntax & Format

**File/PR:** [identifier]
**Date:** YYYY-MM-DD

### Automated Results

| Check | Status | Output |
|-------|--------|--------|
| Build | [ ] PASS / [ ] FAIL | |
| Lint | [ ] PASS / [ ] FAIL | errors: X |
| Types | [ ] PASS / [ ] FAIL | errors: X |
| Format | [ ] PASS / [ ] FAIL | files: X |

### Gate Decision

- [ ] PASS - Proceed to L2
- [ ] FAIL - Fix syntax/format issues

**Confidence Score:** X%
```

---

## L2: Unit Test Gate

### Automated Checks

| Check | Command | Pass Criteria |
|-------|---------|---------------|
| Tests run | `npm test` / `pytest` | All tests execute |
| Tests pass | Test report | 100% pass rate |
| Coverage | `jest --coverage` / `pytest --cov` | >= 80% |
| New code covered | Coverage diff | New code >= 90% |

### Checklist

```markdown
## L2 Gate: Unit Tests

**File/PR:** [identifier]
**Date:** YYYY-MM-DD

### Test Results

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Tests run | X | - | |
| Tests passed | X | 100% | [ ] PASS / [ ] FAIL |
| Tests failed | X | 0 | |
| Coverage | X% | 80% | [ ] PASS / [ ] FAIL |
| New code coverage | X% | 90% | [ ] PASS / [ ] FAIL |

### Failed Tests (if any)

| Test | Error | Fix Status |
|------|-------|------------|
| | | [ ] Fixed |

### Gate Decision

- [ ] PASS - Proceed to L3
- [ ] FAIL - Fix failing tests / add coverage

**Confidence Score:** X%
```

---

## L3: Integration Test Gate

### Automated Checks

| Check | Command | Pass Criteria |
|-------|---------|---------------|
| Integration tests | `npm run test:integration` | All pass |
| API contract tests | `dredd` / `schemathesis` | Contract valid |
| E2E tests | `playwright test` / `cypress run` | Core flows pass |
| DB migrations | `migrate --check` | No pending |

### Checklist

```markdown
## L3 Gate: Integration Tests

**File/PR:** [identifier]
**Date:** YYYY-MM-DD

### Integration Test Results

| Suite | Passed | Failed | Skipped |
|-------|--------|--------|---------|
| API | | | |
| Database | | | |
| External Services | | | |
| E2E | | | |

### API Contract Validation

| Endpoint | Method | Status |
|----------|--------|--------|
| | | [ ] Valid |

### Failed Tests (if any)

| Test | Error | Root Cause | Fix Status |
|------|-------|------------|------------|
| | | | [ ] Fixed |

### Gate Decision

- [ ] PASS - Proceed to L4
- [ ] FAIL - Fix integration issues

**Confidence Score:** X%
```

---

## L4: Code Review Gate

### Manual Review Areas

| Area | Reviewer Focus |
|------|---------------|
| Logic | Algorithm correctness, edge cases |
| Security | Input validation, auth, data handling |
| Performance | N+1 queries, memory leaks, complexity |
| Maintainability | Readability, documentation, patterns |
| Architecture | Design alignment, coupling, cohesion |

### Checklist

```markdown
## L4 Gate: Code Review

**PR:** [#number]
**Author:** [name]
**Reviewer:** [name]
**Date:** YYYY-MM-DD

### Automated Checks

| Check | Status |
|-------|--------|
| Security scan (SAST) | [ ] PASS / [ ] FAIL |
| Dependency audit | [ ] PASS / [ ] FAIL |
| Complexity analysis | [ ] PASS / [ ] FAIL |

### Manual Review

| Criterion | Status | Notes |
|-----------|--------|-------|
| Logic correctness | [ ] OK / [ ] ISSUE | |
| Security practices | [ ] OK / [ ] ISSUE | |
| Performance | [ ] OK / [ ] ISSUE | |
| Error handling | [ ] OK / [ ] ISSUE | |
| Code readability | [ ] OK / [ ] ISSUE | |
| Documentation | [ ] OK / [ ] ISSUE | |
| Test quality | [ ] OK / [ ] ISSUE | |
| Pattern adherence | [ ] OK / [ ] ISSUE | |

### Security Checklist

- [ ] Input validation present
- [ ] No SQL injection vectors
- [ ] No XSS vulnerabilities
- [ ] Auth/authz correct
- [ ] Secrets not hardcoded
- [ ] Sensitive data encrypted
- [ ] Logging safe (no secrets)

### Issues Found

| ID | Severity | Description | Status |
|----|----------|-------------|--------|
| | High/Med/Low | | [ ] Resolved |

### Gate Decision

- [ ] APPROVE - Proceed to L5
- [ ] REQUEST CHANGES - Address issues
- [ ] REJECT - Fundamental issues

**Confidence Score:** X%
```

---

## L5: Staging Validation Gate

### Staging Checks

| Check | Method | Pass Criteria |
|-------|--------|---------------|
| Deployment | CI/CD | Deploys successfully |
| Health check | /health endpoint | Returns 200 |
| Smoke tests | Automated suite | All pass |
| Load test | k6/Locust | Meets SLOs |
| Security scan | DAST | No critical issues |

### Checklist

```markdown
## L5 Gate: Staging Validation

**Release:** [version]
**Environment:** staging
**Date:** YYYY-MM-DD

### Deployment

| Step | Status | Duration |
|------|--------|----------|
| Build | [ ] PASS / [ ] FAIL | |
| Deploy | [ ] PASS / [ ] FAIL | |
| Migration | [ ] PASS / [ ] FAIL | |
| Health check | [ ] PASS / [ ] FAIL | |

### Automated Validation

| Test Suite | Passed | Failed | Duration |
|------------|--------|--------|----------|
| Smoke tests | | | |
| Regression | | | |
| Performance | | | |

### Performance Results

| Metric | Actual | SLO | Status |
|--------|--------|-----|--------|
| P50 latency | ms | ms | [ ] PASS |
| P99 latency | ms | ms | [ ] PASS |
| Error rate | % | % | [ ] PASS |
| Throughput | rps | rps | [ ] PASS |

### Security Scan (DAST)

| Severity | Count | Action |
|----------|-------|--------|
| Critical | | Must fix |
| High | | Must fix |
| Medium | | Should fix |
| Low | | Track |

### Manual QA (if applicable)

| Feature | Status | Tester |
|---------|--------|--------|
| | [ ] OK / [ ] ISSUE | |

### Gate Decision

- [ ] PASS - Ready for production
- [ ] FAIL - Fix staging issues

**Confidence Score:** X%
```

---

## L6: Production Gate

### Pre-Production Checks

| Check | Owner | Status |
|-------|-------|--------|
| CAB approval | Change manager | Required |
| Rollback tested | DevOps | Required |
| Monitoring ready | SRE | Required |
| Documentation updated | Tech writer | Required |
| Stakeholder sign-off | Product owner | Required |

### Checklist

```markdown
## L6 Gate: Production Release

**Release:** [version]
**Date:** YYYY-MM-DD
**Release Manager:** [name]

### Pre-Flight Checks

| Check | Status | Owner |
|-------|--------|-------|
| All L1-L5 gates passed | [ ] | CI/CD |
| Staging validation complete | [ ] | QA |
| Change request approved | [ ] | CAB |
| Rollback plan documented | [ ] | DevOps |
| Rollback tested | [ ] | DevOps |
| Monitoring dashboards ready | [ ] | SRE |
| Alerts configured | [ ] | SRE |
| Feature flags configured | [ ] | Dev |
| Documentation updated | [ ] | Tech writer |
| Release notes prepared | [ ] | PM |

### Approvals

| Role | Name | Approved | Date |
|------|------|----------|------|
| Tech Lead | | [ ] | |
| QA Lead | | [ ] | |
| Product Owner | | [ ] | |
| Release Manager | | [ ] | |

### Rollback Criteria

| Condition | Action |
|-----------|--------|
| Error rate > X% | Immediate rollback |
| P99 latency > Xms | Investigate, possible rollback |
| Core flow failure | Immediate rollback |

### Gate Decision

- [ ] GO - Deploy to production
- [ ] NO-GO - Reason: [...]

**Confidence Score:** X%
```

---

## Specification Review Gate

### Checklist

```markdown
## Gate: Specification Review

**Spec:** [path/to/spec.md]
**Author:** [name]
**Reviewer:** [name]
**Date:** YYYY-MM-DD

### Completeness

| Criterion | Status | Notes |
|-----------|--------|-------|
| Problem statement clear | [ ] OK / [ ] ISSUE | |
| User personas defined | [ ] OK / [ ] ISSUE | |
| All FRs have unique IDs | [ ] OK / [ ] ISSUE | |
| Each FR is testable | [ ] OK / [ ] ISSUE | |
| NFRs defined (perf, sec) | [ ] OK / [ ] ISSUE | |
| AC uses Given-When-Then | [ ] OK / [ ] ISSUE | |
| Out of scope listed | [ ] OK / [ ] ISSUE | |
| Dependencies documented | [ ] OK / [ ] ISSUE | |
| No conflicting requirements | [ ] OK / [ ] ISSUE | |

### Review Questions

1. Can a developer understand WHAT to build? [ ] Yes / [ ] No
2. Can QA write tests from ACs? [ ] Yes / [ ] No
3. Are edge cases considered? [ ] Yes / [ ] No
4. Is scope realistic? [ ] Yes / [ ] No

### Gate Decision

- [ ] APPROVE - Ready for design
- [ ] REQUEST CHANGES - Issues to address
- [ ] REJECT - Major gaps

**Confidence Score:** X%
```

---

## Design Review Gate

### Checklist

```markdown
## Gate: Design Review

**Design:** [path/to/design.md]
**Spec:** [path/to/spec.md]
**Author:** [name]
**Reviewer:** [name]
**Date:** YYYY-MM-DD

### Requirement Coverage

| Requirement ID | Covered | Design Section |
|----------------|---------|----------------|
| FR-001 | [ ] | |
| FR-002 | [ ] | |

### Design Quality

| Criterion | Status | Notes |
|-----------|--------|-------|
| All FRs addressed | [ ] OK / [ ] ISSUE | |
| ADRs documented | [ ] OK / [ ] ISSUE | |
| File structure specified | [ ] OK / [ ] ISSUE | |
| Data models defined | [ ] OK / [ ] ISSUE | |
| API contracts specified | [ ] OK / [ ] ISSUE | |
| Dependencies versioned | [ ] OK / [ ] ISSUE | |
| Security documented | [ ] OK / [ ] ISSUE | |
| Testing strategy defined | [ ] OK / [ ] ISSUE | |
| No unjustified tech choices | [ ] OK / [ ] ISSUE | |

### Review Questions

1. Can a developer implement from this alone? [ ] Yes / [ ] No
2. Any obvious scalability issues? [ ] Yes / [ ] No
3. Security best practices followed? [ ] Yes / [ ] No
4. Will this handle NFRs? [ ] Yes / [ ] No

### Gate Decision

- [ ] APPROVE - Ready for implementation
- [ ] REQUEST CHANGES - Issues to address
- [ ] REJECT - Major gaps

**Confidence Score:** X%
```

---

## Quick Reference

### Gate Thresholds

| Gate | Min Confidence | Action if Fail |
|------|----------------|----------------|
| L1 | 95% | Block, fix immediately |
| L2 | 90% | Block, add tests |
| L3 | 85% | Block, fix integrations |
| L4 | 80% | Conditional proceed |
| L5 | 85% | Block, fix staging |
| L6 | 90% | No production |

### Severity Definitions

| Severity | Definition | SLA |
|----------|------------|-----|
| Critical | Blocks release, security breach | Immediate |
| High | Major functionality broken | Before merge |
| Medium | Feature degraded | Before release |
| Low | Minor issue, cosmetic | Next sprint |

---

*Quality Gate Checklists | SDD Execution | Version 2.0*
