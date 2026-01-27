# Security Testing Checklist

Step-by-step checklist for comprehensive security testing.

---

## Pre-Development Checklist

### Threat Modeling

- [ ] Identify assets (data, functionality, infrastructure)
- [ ] Define trust boundaries
- [ ] Enumerate threat actors and attack vectors
- [ ] Document STRIDE threats (Spoofing, Tampering, Repudiation, Information Disclosure, DoS, Elevation of Privilege)
- [ ] Prioritize risks by impact and likelihood
- [ ] Define security requirements based on threats

### Security Requirements

- [ ] Authentication requirements defined
- [ ] Authorization model documented
- [ ] Data classification completed
- [ ] Encryption requirements specified
- [ ] Logging and audit requirements defined
- [ ] Compliance requirements identified (GDPR, SOC2, PCI-DSS)

---

## Development Phase Checklist

### Secure Coding

- [ ] Input validation on all user inputs
- [ ] Output encoding based on context (HTML, JS, SQL, URL)
- [ ] Parameterized queries for database access
- [ ] Secure password hashing (bcrypt, Argon2, PBKDF2)
- [ ] No secrets hardcoded in source code
- [ ] Secure session management
- [ ] CSRF protection implemented
- [ ] Security headers configured

### IDE/Local Security Checks

- [ ] IDE security plugin installed (Snyk, SonarLint)
- [ ] Pre-commit hooks for secret detection
- [ ] Local SAST scan passes
- [ ] Dependency audit shows no critical vulnerabilities

---

## Pull Request Checklist

### Code Review Security Focus

- [ ] Authentication changes reviewed by security team
- [ ] Authorization logic verified
- [ ] No sensitive data in logs
- [ ] Error messages don't leak information
- [ ] Crypto usage reviewed (no custom crypto)
- [ ] File upload restrictions in place
- [ ] Rate limiting implemented
- [ ] Input validation comprehensive

### Automated PR Checks

- [ ] SAST scan passes (Semgrep, Bandit)
- [ ] Secret detection passes (TruffleHog, Gitleaks)
- [ ] Dependency scan passes (Snyk, npm audit)
- [ ] Code coverage includes security-critical paths

---

## CI/CD Pipeline Checklist

### Static Analysis (SAST)

- [ ] **Semgrep configured**
  - [ ] OWASP Top 10 rules enabled
  - [ ] Custom rules for project patterns
  - [ ] Results reviewed, not just passed

- [ ] **Language-specific SAST**
  - [ ] Python: Bandit with full test suite
  - [ ] JavaScript: ESLint security plugin
  - [ ] Go: gosec
  - [ ] Java: SpotBugs with FindSecBugs

### Secret Detection

- [ ] **Pre-commit hooks**
  - [ ] detect-secrets baseline updated
  - [ ] Gitleaks pre-commit hook active

- [ ] **CI Pipeline**
  - [ ] TruffleHog scans full git history
  - [ ] Verified secrets flagged as critical
  - [ ] Build fails on detected secrets

### Dependency Scanning (SCA)

- [ ] **Python**
  - [ ] pip-audit or Safety runs on every build
  - [ ] Requirements pinned with hashes
  - [ ] Private PyPI uses trusted sources only

- [ ] **JavaScript**
  - [ ] npm audit runs on every build
  - [ ] package-lock.json committed
  - [ ] No `npm install` from arbitrary URLs

- [ ] **Container Images**
  - [ ] Base images from trusted registries
  - [ ] Trivy/Grype scans on image build
  - [ ] No critical CVEs in final image

### Infrastructure as Code

- [ ] Checkov/tfsec scans Terraform
- [ ] CloudFormation Guard for AWS
- [ ] No hardcoded credentials in IaC
- [ ] Security groups follow least privilege

---

## Dynamic Testing (DAST) Checklist

### Pre-DAST Setup

- [ ] Test environment isolated from production
- [ ] Test accounts with various privilege levels
- [ ] Authentication configured in scanner
- [ ] Scope defined (include/exclude URLs)
- [ ] Rate limiting adjusted for testing

### OWASP ZAP Checklist

- [ ] **Baseline Scan**
  - [ ] Passive scan completed
  - [ ] No high-severity passive findings

- [ ] **Active Scan**
  - [ ] SQL injection tests completed
  - [ ] XSS tests completed
  - [ ] Path traversal tests completed
  - [ ] SSRF tests completed

- [ ] **API Scan**
  - [ ] OpenAPI spec imported
  - [ ] All endpoints tested
  - [ ] Authentication tested
  - [ ] Authorization tested

### Authentication Testing

- [ ] Password brute force protected
- [ ] Account lockout implemented
- [ ] Session fixation prevented
- [ ] Session timeout configured
- [ ] Secure cookie attributes set
- [ ] JWT signature verified
- [ ] Token expiration enforced

### Authorization Testing

- [ ] Horizontal privilege escalation tested
- [ ] Vertical privilege escalation tested
- [ ] IDOR vulnerabilities checked
- [ ] Admin functions protected
- [ ] API authorization consistent with UI

---

## OWASP Top 10 2025 Checklist

### A01: Broken Access Control

- [ ] Server-side access control enforced
- [ ] Deny by default for new endpoints
- [ ] CORS configured restrictively
- [ ] Directory listing disabled
- [ ] JWT tokens validated properly
- [ ] SSRF attacks mitigated
- [ ] Rate limiting on sensitive operations

### A02: Security Misconfiguration

- [ ] Debug mode disabled in production
- [ ] Default credentials changed
- [ ] Unnecessary features disabled
- [ ] Error messages don't leak stack traces
- [ ] Security headers present (CSP, HSTS, X-Frame-Options)
- [ ] Cloud storage permissions reviewed
- [ ] Admin interfaces not publicly accessible

### A03: Software Supply Chain Failures

- [ ] Dependencies from trusted sources only
- [ ] Lockfiles committed and used
- [ ] Dependency vulnerabilities monitored
- [ ] SBOM generated for releases
- [ ] Build pipeline integrity verified
- [ ] Code signing implemented
- [ ] Third-party integrations reviewed

### A04: Cryptographic Failures

- [ ] TLS 1.2+ enforced
- [ ] Strong cipher suites only
- [ ] Passwords hashed with modern algorithms
- [ ] Sensitive data encrypted at rest
- [ ] Encryption keys rotated regularly
- [ ] No sensitive data in URLs
- [ ] PII masked in logs

### A05: Injection

- [ ] Parameterized queries used
- [ ] ORM used safely
- [ ] OS commands avoided or sanitized
- [ ] LDAP queries parameterized
- [ ] XML parsers configured safely (no XXE)
- [ ] Output encoded for context
- [ ] Content-Type headers enforced

### A06: Insecure Design

- [ ] Threat modeling completed
- [ ] Security controls in architecture
- [ ] Business logic abuse scenarios tested
- [ ] Resource limits implemented
- [ ] Fail-secure defaults
- [ ] Separation of duties enforced

### A07: Authentication Failures

- [ ] MFA available for sensitive accounts
- [ ] Password complexity enforced
- [ ] Passwords checked against breach databases
- [ ] Rate limiting on login attempts
- [ ] Secure password recovery
- [ ] Session invalidated on logout
- [ ] Remember-me tokens secure

### A08: Software/Data Integrity Failures

- [ ] CI/CD pipeline access restricted
- [ ] Code changes require approval
- [ ] Dependencies verified (checksums, signatures)
- [ ] Deserialization input validated
- [ ] Updates delivered securely
- [ ] Integrity checks on critical data

### A09: Security Logging Failures

- [ ] Authentication events logged
- [ ] Authorization failures logged
- [ ] Input validation failures logged
- [ ] Logs protected from tampering
- [ ] Alerting configured for security events
- [ ] Log retention meets compliance
- [ ] No sensitive data in logs

### A10: Mishandling Exceptional Conditions

- [ ] Errors handled gracefully
- [ ] No security bypass on exceptions
- [ ] Resource cleanup on errors
- [ ] Timeout handling implemented
- [ ] Circuit breakers for external services
- [ ] Fail-secure, not fail-open

---

## API Security Checklist (OWASP API Top 10)

### API1: Broken Object Level Authorization

- [ ] Authorization check on every object access
- [ ] UUIDs instead of sequential IDs
- [ ] Ownership verified for each request
- [ ] Tests for accessing other users' objects

### API2: Broken Authentication

- [ ] Strong token generation
- [ ] Token expiration enforced
- [ ] Refresh token rotation
- [ ] No credentials in URLs
- [ ] Authentication on all endpoints

### API3: Broken Property Level Authorization

- [ ] Response filtering by role
- [ ] Mass assignment prevention
- [ ] Sensitive properties excluded from responses

### API4: Unrestricted Resource Consumption

- [ ] Rate limiting per client
- [ ] Pagination on list endpoints
- [ ] Request payload size limits
- [ ] Timeout on expensive operations
- [ ] Query complexity limits (GraphQL)

### API5: Broken Function Level Authorization

- [ ] Admin endpoints require admin role
- [ ] Function-level checks, not just endpoint
- [ ] No admin functionality via regular endpoints

### API6: Unrestricted Access to Sensitive Flows

- [ ] Business logic abuse tested
- [ ] Transaction limits enforced
- [ ] Velocity checks on sensitive operations
- [ ] CAPTCHA on high-value flows

### API7: Server Side Request Forgery

- [ ] URL validation before fetching
- [ ] Internal IPs blocked
- [ ] Redirect following disabled/limited
- [ ] Response filtering

### API8: Security Misconfiguration

- [ ] CORS configured per-endpoint
- [ ] HTTP methods restricted
- [ ] Content-Type validation
- [ ] API versioning secure

### API9: Improper Inventory Management

- [ ] API documentation complete
- [ ] Deprecated endpoints removed
- [ ] Shadow APIs discovered and secured
- [ ] API gateway inventory accurate

### API10: Unsafe Consumption of APIs

- [ ] Third-party API responses validated
- [ ] TLS enforced for outbound calls
- [ ] Timeout and retry limits
- [ ] Input sanitization from external APIs

---

## Pre-Release Checklist

### Final Security Review

- [ ] All critical/high findings remediated
- [ ] Security test results documented
- [ ] Risk acceptance for deferred issues
- [ ] Penetration test completed (if required)
- [ ] Security sign-off obtained

### Deployment Security

- [ ] Secrets in secret manager (not env vars)
- [ ] Production config reviewed
- [ ] WAF rules updated
- [ ] Monitoring and alerting configured
- [ ] Incident response plan updated
- [ ] Rollback plan documented

---

## Post-Deployment Checklist

### Ongoing Monitoring

- [ ] Runtime security monitoring active
- [ ] Dependency vulnerability alerts configured
- [ ] Security log review scheduled
- [ ] Penetration testing scheduled (quarterly/annual)
- [ ] Bug bounty program (if applicable)

### Incident Preparedness

- [ ] Incident response runbook updated
- [ ] Contact list current
- [ ] Breach notification procedures documented
- [ ] Forensic readiness verified

---

## Quick Reference

### Severity Classification

| Severity | Response Time | Examples |
|----------|---------------|----------|
| Critical | Immediate | RCE, SQL injection, auth bypass |
| High | 24-48 hours | Stored XSS, privilege escalation |
| Medium | 1-2 weeks | Reflected XSS, CSRF |
| Low | Next sprint | Information disclosure, missing headers |

### Common False Positive Indicators

- Test/mock data flagged as secrets
- Example code in documentation
- Disabled/unreachable code paths
- Development-only configurations

### When to Engage Security Team

- Authentication/authorization changes
- Cryptography implementation
- New third-party integrations
- Compliance-relevant changes
- High-severity findings
- Security architecture decisions

---

*Use this checklist throughout the development lifecycle. Not all items apply to every project - adapt based on risk profile and compliance requirements.*
