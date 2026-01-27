# Security Testing

## Overview

Security testing identifies vulnerabilities in applications before attackers can exploit them. Modern security testing combines static analysis (SAST), dynamic testing (DAST), dependency scanning (SCA), and secret detection to provide comprehensive protection across the software development lifecycle.

**Key principle:** Shift security left - integrate testing early in development, not just before production.

---

## OWASP Top 10 2025

The OWASP Top 10 2025 represents the most critical web application security risks, based on analysis of 175,000+ CVE records.

| Rank | Category | Key Points |
|------|----------|------------|
| **A01** | Broken Access Control | #1 risk. Includes SSRF (consolidated from 2021). Test authorization at every function. |
| **A02** | Security Misconfiguration | Moved up from #5. Debug modes, default credentials, unnecessary features. |
| **A03** | Software Supply Chain Failures | **NEW**. Extends beyond dependencies to build systems, distribution infrastructure. |
| **A04** | Cryptographic Failures | Weak encryption, exposed sensitive data, improper key management. |
| **A05** | Injection | SQL, NoSQL, OS command, LDAP injection. Includes XSS. |
| **A06** | Insecure Design | Threat modeling gaps, missing security controls by design. |
| **A07** | Authentication Failures | Weak passwords, session management, credential stuffing. |
| **A08** | Software/Data Integrity Failures | CI/CD pipeline attacks, unsigned updates, deserialization. |
| **A09** | Security Logging Failures | Insufficient logging, missing alerting, no incident detection. |
| **A10** | Mishandling Exceptional Conditions | **NEW**. Improper error handling, failing open, logical errors. |

**2025 Key Shift:** Focus moves from symptoms to root causes. Testing now covers dependencies, build systems, and container images.

---

## Testing Categories

### 1. Static Application Security Testing (SAST)

Analyzes source code without executing the application.

| Tool | Language Focus | Best For |
|------|----------------|----------|
| **Semgrep** | Multi-language | Custom rules, CI/CD speed, low config |
| **Bandit** | Python only | Python-specific security patterns |
| **SonarQube** | Multi-language | Code quality + security combined |
| **CodeQL** | Multi-language | Deep dataflow analysis, GitHub native |
| **Snyk Code** | Multi-language | Developer-friendly, PR feedback |

**When to use:** Every commit, PR checks, pre-merge gates.

### 2. Dynamic Application Security Testing (DAST)

Tests running applications by simulating attacks.

| Tool | Type | Best For |
|------|------|----------|
| **OWASP ZAP** | Open source | CI/CD automation, free, scriptable |
| **Burp Suite** | Commercial | Manual pentesting, deep analysis |
| **Nuclei** | Open source | Template-based scanning, fast |
| **Nikto** | Open source | Web server misconfiguration |

**When to use:** Staging environments, pre-production, scheduled scans.

### 3. Software Composition Analysis (SCA)

Scans dependencies for known vulnerabilities.

| Tool | Features | Integration |
|------|----------|-------------|
| **Snyk** | Continuous monitoring, auto-fix PRs | IDE, CI/CD, CLI |
| **Dependabot** | GitHub native, automatic PRs | GitHub only |
| **Safety/pip-audit** | Python packages | CLI, CI/CD |
| **npm audit** | Node.js packages | npm/yarn native |
| **Trivy** | Containers, IaC, SBOM | CLI, CI/CD |

**When to use:** Every build, weekly scheduled scans, new dependency additions.

### 4. Secret Detection

Finds hardcoded credentials, API keys, tokens.

| Tool | Approach | Coverage |
|------|----------|----------|
| **TruffleHog** | Entropy + patterns, 700+ detectors | Git, S3, Docker, cloud storage |
| **Gitleaks** | Regex patterns, fast | Git history, pre-commit |
| **detect-secrets** | Baseline methodology, low FP | Pre-commit, CI/CD |
| **GitHub Secret Scanning** | Native GitHub | Public/private repos |

**When to use:** Pre-commit hooks, every PR, historical scans for new repos.

---

## Security Testing in CI/CD

### Pipeline Integration Points

```
Code Commit → SAST + Secrets → PR Review → DAST (staging) → Deploy → Runtime Monitoring
     ↓              ↓               ↓             ↓            ↓            ↓
  Bandit      TruffleHog      Code Review    OWASP ZAP    Container    WAF/RASP
  Semgrep     Gitleaks        Manual         Nuclei       Scan
```

### Recommended Pipeline

```yaml
# GitHub Actions example
stages:
  - lint-and-sast    # Semgrep, Bandit (fast, every commit)
  - secrets          # TruffleHog, Gitleaks (every commit)
  - dependencies     # Snyk, npm audit (every build)
  - dast             # OWASP ZAP (staging only, nightly)
  - container        # Trivy (on image build)
```

### Gate Criteria

| Stage | Block on | Allow with Warning |
|-------|----------|-------------------|
| SAST | Critical/High severity | Medium severity |
| Secrets | Any detected secret | None |
| Dependencies | Critical CVEs, exploited in wild | High CVEs with no fix |
| DAST | Critical/High | Medium/Low |

---

## API Security Testing

### OWASP API Security Top 10 2023

| Risk | Description | Test Approach |
|------|-------------|---------------|
| **API1** | Broken Object Level Authorization | Access other users' objects by changing IDs |
| **API2** | Broken Authentication | Token manipulation, session attacks |
| **API3** | Broken Object Property Level Authorization | Access restricted properties |
| **API4** | Unrestricted Resource Consumption | Rate limiting, payload size |
| **API5** | Broken Function Level Authorization | Admin endpoints, privilege escalation |
| **API6** | Unrestricted Access to Sensitive Business Flows | Business logic abuse |
| **API7** | Server Side Request Forgery | Internal network access via API |
| **API8** | Security Misconfiguration | CORS, headers, error messages |
| **API9** | Improper Inventory Management | Shadow APIs, undocumented endpoints |
| **API10** | Unsafe Consumption of APIs | Third-party API trust |

### API Testing Tools

- **Postman/Newman** - API testing automation
- **OWASP ZAP** - API scanning mode
- **Burp Suite** - Manual API testing
- **42Crunch** - OpenAPI security audit
- **Pynt** - API security testing platform

---

## Authentication & Authorization Testing

### Authentication Tests

| Test Case | What to Check |
|-----------|---------------|
| Credential stuffing protection | Rate limiting, CAPTCHA, account lockout |
| Password policy | Complexity, length, breach database check |
| Session management | Secure cookies, expiration, rotation |
| MFA bypass | Token reuse, backup code abuse |
| Token security | JWT validation, signature verification |

### Authorization Tests

| Test Case | What to Check |
|-----------|---------------|
| Horizontal privilege escalation | User A accessing User B's data |
| Vertical privilege escalation | User accessing admin functions |
| IDOR | Changing object IDs in requests |
| Missing function-level access control | Direct URL access to admin pages |
| Insecure direct object references | Predictable resource IDs |

---

## Input Validation Testing

### Injection Types to Test

| Type | Payloads | Detection |
|------|----------|-----------|
| SQL Injection | `' OR '1'='1`, `; DROP TABLE--` | Database errors, unexpected data |
| NoSQL Injection | `{"$gt": ""}`, `{"$ne": null}` | Query manipulation |
| Command Injection | `; ls`, `| cat /etc/passwd` | Command execution |
| XSS | `<script>alert(1)</script>` | Script execution |
| Path Traversal | `../../../etc/passwd` | File access outside webroot |
| LDAP Injection | `*)(uid=*))(|(uid=*` | Directory service manipulation |
| XML Injection | XXE payloads | External entity processing |

### Validation Best Practices

1. **Whitelist validation** - Define allowed characters/patterns
2. **Type coercion** - Enforce expected data types
3. **Length limits** - Prevent buffer overflows
4. **Encoding output** - Context-aware escaping
5. **Parameterized queries** - Never concatenate user input

---

## LLM Usage Tips for Security Testing

### Effective Prompting Patterns

1. **Generate test cases from code:**
   > "Analyze this endpoint and generate security test cases for OWASP Top 10 vulnerabilities"

2. **Review for vulnerabilities:**
   > "Review this code for security vulnerabilities. Focus on injection, authentication, and access control"

3. **Create security automation:**
   > "Write a GitHub Actions workflow that runs Semgrep, Bandit, and TruffleHog on every PR"

4. **Explain findings:**
   > "Explain this Semgrep finding and provide remediation steps: [paste finding]"

### LLM Limitations in Security Testing

- Cannot execute dynamic tests
- May miss context-specific vulnerabilities
- Training data cutoff affects CVE knowledge
- Cannot replace manual penetration testing
- May hallucinate non-existent vulnerabilities

---

## Quick Reference Commands

### SAST

```bash
# Semgrep
semgrep --config auto .
semgrep --config p/owasp-top-ten .
semgrep --config p/security-audit .

# Bandit (Python)
bandit -r src/ -f json -o bandit-report.json
bandit -r src/ -ll  # Only high severity

# SonarQube (via Docker)
docker run --rm -v "$PWD:/src" sonarsource/sonar-scanner-cli
```

### DAST

```bash
# OWASP ZAP
docker run -t zaproxy/zap-stable zap-baseline.py -t https://target.com
docker run -t zaproxy/zap-stable zap-full-scan.py -t https://target.com

# Nuclei
nuclei -u https://target.com -t cves/
nuclei -u https://target.com -t vulnerabilities/
```

### Secrets

```bash
# TruffleHog
trufflehog git file://. --only-verified
trufflehog github --org=myorg

# Gitleaks
gitleaks detect --source . --verbose
gitleaks detect --source . --report-path report.json
```

### Dependencies

```bash
# Python
pip-audit
safety check -r requirements.txt

# Node.js
npm audit
npm audit fix

# Snyk
snyk test
snyk monitor
```

---

## External Resources

### Standards & Guides
- [OWASP Top 10 2025](https://owasp.org/Top10/2025/)
- [OWASP API Security Top 10](https://owasp.org/API-Security/)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [CWE Top 25](https://cwe.mitre.org/top25/)

### Tools Documentation
- [Semgrep Registry](https://semgrep.dev/explore)
- [Bandit Documentation](https://bandit.readthedocs.io/)
- [OWASP ZAP Documentation](https://www.zaproxy.org/docs/)
- [TruffleHog GitHub](https://github.com/trufflesecurity/trufflehog)
- [Snyk Documentation](https://docs.snyk.io/)

### Learning Resources
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)
- [OWASP WebGoat](https://owasp.org/www-project-webgoat/)
- [HackTheBox](https://www.hackthebox.com/)
- [PentesterLab](https://pentesterlab.com/)

---

## Related Skills

- [faion-software-developer](../faion-software-developer/CLAUDE.md) - Secure coding practices
- [faion-devops-engineer](../faion-devops-engineer/CLAUDE.md) - Security in CI/CD
- [faion-api-developer](../faion-api-developer/CLAUDE.md) - API security
- [faion-infrastructure-engineer](../faion-infrastructure-engineer/CLAUDE.md) - Container security

---

*Based on OWASP Top 10 2025 and industry best practices. Last updated: 2026-01.*
