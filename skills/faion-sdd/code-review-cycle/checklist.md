# Code Review Checklists

## Self-Review Checklist

Run before creating a PR. Use AI assistance for automated checks.

### Code Quality

```yaml
code_quality:
  automated: # AI can verify
    - "Follows project style guide (linter passes)"
    - "No commented-out code"
    - "No debug statements (console.log, print, debugger)"
    - "No hardcoded values (use constants/config)"
    - "No unused imports or variables"
    - "No TODO/FIXME without issue reference"

  manual: # Human judgment needed
    - "Error handling is appropriate for context"
    - "Abstraction level is consistent"
    - "No premature optimization"
```

### Functionality

```yaml
functionality:
  automated:
    - "All acceptance criteria addressed"
    - "Tests cover new code paths"
    - "Tests pass locally"

  manual:
    - "Edge cases are handled"
    - "No regression in existing functionality"
    - "Changes work as expected locally"
    - "Error messages are helpful"
```

### Testing

```yaml
testing:
  automated:
    - "Unit tests added for new functions"
    - "Coverage threshold met"
    - "No skipped/disabled tests"

  manual:
    - "Tests are meaningful, not just coverage"
    - "Tests cover edge cases"
    - "Integration tests updated if needed"
    - "Test names describe behavior"
```

### Documentation

```yaml
documentation:
  automated:
    - "Public functions have docstrings"
    - "API docs generated without errors"

  manual:
    - "Code is self-documenting with clear names"
    - "Complex logic has comments explaining why"
    - "README updated if setup changed"
    - "CHANGELOG updated if user-facing"
```

### SDD Compliance

```yaml
sdd_compliance:
  - "Implementation matches design document"
  - "Deviations are documented and justified"
  - "Traceability links are correct"
  - "All acceptance criteria verifiable"
```

### Security

```yaml
security:
  automated:
    - "No secrets in code"
    - "Dependencies have no known vulnerabilities"
    - "SAST scan passes"

  manual:
    - "Input validation is sufficient"
    - "Auth/authz implemented correctly"
    - "Sensitive data handled properly"
```

---

## Peer Review Checklist

For the reviewer to complete during review.

### Quick Template

```markdown
## Review: [PR Title]
Reviewer: @name | Date: YYYY-MM-DD

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
- [ ] Input validated
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

### AI Review Notes
- [ ] AI suggestions addressed or dismissed with reason
- [ ] No critical AI-flagged issues ignored

### Verdict
- [ ] Approved
- [ ] Approved with suggestions
- [ ] Request changes

### Summary
[Overall assessment]
```

### Detailed Review Dimensions

```yaml
review_dimensions:
  correctness:
    questions:
      - "Does it solve the stated problem?"
      - "Does it handle edge cases?"
      - "Could it cause data corruption?"
      - "Are there race conditions?"
      - "What happens on failure?"
    ai_assist: "Ask AI to identify potential failure modes"

  design:
    questions:
      - "Does it follow architectural patterns?"
      - "Is it consistent with existing code?"
      - "Is it extensible for future needs?"
      - "Is there unnecessary complexity?"
      - "Are responsibilities well-separated?"
    ai_assist: "Ask AI to compare with similar code in repo"

  readability:
    questions:
      - "Can I understand without author explanation?"
      - "Are names clear and consistent?"
      - "Is the code well-organized?"
      - "Are comments helpful, not redundant?"
    ai_assist: "AI excels at readability suggestions"

  performance:
    questions:
      - "Are there N+1 queries?"
      - "Is caching used appropriately?"
      - "Are there memory leaks?"
      - "Is it efficient at scale?"
      - "Are there unnecessary allocations?"
    ai_assist: "Ask AI to identify O(n^2) or worse patterns"

  security:
    questions:
      - "Is input validated?"
      - "Are there injection risks?"
      - "Is authentication/authorization correct?"
      - "Are secrets handled properly?"
      - "Is data encrypted when needed?"
    ai_assist: "Run security-focused AI scan"

  testing:
    questions:
      - "Are tests meaningful?"
      - "Do tests cover edge cases?"
      - "Are mocks used appropriately?"
      - "Would tests catch regressions?"
      - "Are tests readable/maintainable?"
    ai_assist: "Ask AI to suggest missing test cases"
```

---

## Security Review Checklist

For security-sensitive code paths.

```yaml
security_review:
  authentication:
    - "Auth tokens validated correctly"
    - "Session management secure"
    - "Password handling follows best practices"
    - "MFA implemented where required"

  authorization:
    - "Permission checks at all entry points"
    - "No privilege escalation paths"
    - "Resource ownership verified"
    - "Admin actions properly restricted"

  input_validation:
    - "All user input validated"
    - "SQL injection prevented (parameterized queries)"
    - "XSS prevented (output encoding)"
    - "Path traversal prevented"
    - "File upload restrictions enforced"

  data_protection:
    - "Sensitive data encrypted at rest"
    - "TLS for data in transit"
    - "PII handled per regulations"
    - "Audit logging for sensitive operations"

  dependencies:
    - "No known vulnerabilities (Dependabot/Snyk)"
    - "Dependencies from trusted sources"
    - "Dependency versions pinned"

  secrets:
    - "No secrets in code"
    - "Secrets in environment/vault"
    - "No secrets in logs"
    - "API keys properly scoped"

  error_handling:
    - "No sensitive data in error messages"
    - "Stack traces not exposed to users"
    - "Errors logged appropriately"
```

---

## Architectural Review Checklist

For significant changes to system architecture.

```yaml
architectural_review:
  design_alignment:
    - "Aligns with system architecture docs"
    - "Follows established patterns"
    - "Deviations documented in ADR"

  scalability:
    - "Handles expected load"
    - "No single points of failure"
    - "Can scale horizontally if needed"

  maintainability:
    - "Clear separation of concerns"
    - "Dependencies well-managed"
    - "Configuration externalized"

  observability:
    - "Logging sufficient for debugging"
    - "Metrics for key operations"
    - "Tracing for distributed calls"

  backwards_compatibility:
    - "API changes are backwards compatible"
    - "Database migrations are reversible"
    - "Feature flags for gradual rollout"

  integration:
    - "External dependencies documented"
    - "Fallback behavior defined"
    - "Circuit breakers where appropriate"
```

---

## Database Change Checklist

For PRs with database migrations.

```yaml
database_review:
  migration:
    - "Migration is reversible"
    - "Down migration tested"
    - "No data loss possible"
    - "Handles empty/full tables"

  performance:
    - "New indexes documented"
    - "Query plans verified"
    - "No table locks during migration"
    - "Batch operations for large data"

  data_integrity:
    - "Foreign keys maintained"
    - "Constraints appropriate"
    - "Default values sensible"
    - "Nullable fields intentional"

  deployment:
    - "Can deploy without downtime"
    - "Rollback procedure documented"
    - "Data backfill strategy clear"
```

---

## AI-Flagged Issues Triage

How to handle AI review feedback.

```yaml
ai_feedback_triage:
  critical: # Must address
    - "Security vulnerabilities"
    - "Potential data corruption"
    - "Known anti-patterns that cause bugs"

  high: # Should address
    - "Missing error handling"
    - "Performance issues"
    - "Test coverage gaps"

  medium: # Consider
    - "Readability improvements"
    - "Refactoring suggestions"
    - "Documentation gaps"

  low: # Optional
    - "Style preferences"
    - "Alternative approaches"
    - "Minor optimizations"

  dismiss_if:
    - "False positive (explain why)"
    - "Intentional design decision (reference ADR)"
    - "Out of scope for this PR (create follow-up)"
```
