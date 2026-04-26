# Security Testing

## Summary

Security testing identifies vulnerabilities before exploitation through static analysis (SAST), dynamic testing (DAST), dependency scanning, and OWASP Top 10 scenario tests. Core rule: assert exact HTTP status codes (401/403/400) — not just "not 500" — and assert absence of sensitive data in responses, not just "request did not crash."

## Why

LLMs and developers frequently re-introduce known vulnerability classes: SQL string concatenation, missing CSRF, weak hashing, hardcoded secrets. Shift-left automated scanning catches these before production. Without security gates in CI, the cost of detection grows exponentially — a pre-push secret scan takes seconds; a production credential rotation takes hours.

## When To Use

- Pre-deploy gate after any change touching auth, sessions, file upload, deserialization, or SQL queries
- After bumping dependencies (transitive CVEs surface via pip-audit, npm audit)
- Wiring SAST + secrets scan + dep-audit into CI before opening the project to outside contributors
- Reviewing AI-generated PRs — LLMs frequently re-introduce SQL string concatenation and missing CSRF

## When NOT To Use

- Pre-commit on every save — DAST/fuzzing is too slow; restrict to PR/CI or nightly
- As a substitute for threat modelling — testing only finds what you tell it to look for
- For business-logic flaws (price tampering, IDOR via valid-but-wrong IDs) — those need handwritten scenario tests
- Penetration testing of production without written authorization (legal exposure)

## Content

| File | What's inside |
|------|---------------|
| `content/01-owasp-tests.xml` | OWASP Top 10 test patterns: broken access control, injection, XSS, brute force, session invalidation |
| `content/02-sast-ci.xml` | SAST tooling: Bandit, Semgrep, pip-audit, gitleaks; GitHub Actions workflow; Bandit config |
| `content/03-input-validation.xml` | Input validation tests: email, password strength, file upload type/size, path traversal |
| `content/04-antipatterns.xml` | Common failure modes: security as afterthought, assert != 500, ignoring low severity |

## Templates

| File | Purpose |
|------|---------|
| `templates/security-ci.yml` | GitHub Actions workflow with Bandit, Semgrep, pip-audit, and artifact upload |
| `templates/bandit-config.yaml` | Bandit rules configuration covering the B1xx–B7xx rule set |
