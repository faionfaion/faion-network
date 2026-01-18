# M-DO-021: Security Scanning

## Metadata
- **Category:** Development/DevOps
- **Difficulty:** Intermediate
- **Tags:** #devops, #security, #scanning, #sast, #dast, #methodology
- **Agent:** faion-devops-agent

---

## Problem

Vulnerabilities in code and dependencies go undetected. Security is treated as an afterthought. Breaches occur after deployment when fixes are expensive.

## Promise

After this methodology, you will shift security left with automated scanning. Vulnerabilities will be detected in CI before they reach production.

## Overview

Security scanning includes SAST (static analysis), DAST (dynamic testing), SCA (dependency scanning), and secret detection. Integrate into CI/CD.

---

## Framework

### Step 1: Dependency Scanning (SCA)

```bash
# npm audit
npm audit
npm audit --production
npm audit fix

# Snyk
npm install -g snyk
snyk auth
snyk test
snyk monitor

# OWASP Dependency-Check
dependency-check --scan . --format HTML --out report.html

# pip-audit (Python)
pip install pip-audit
pip-audit

# Trivy for dependencies
trivy fs --security-checks vuln .
```

```yaml
# GitHub Actions - Dependabot
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10

  - package-ecosystem: "docker"
    directory: "/"
    schedule:
      interval: "weekly"

  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

### Step 2: Static Analysis (SAST)

```yaml
# GitHub Actions - CodeQL
name: CodeQL

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 0 * * 0'

jobs:
  analyze:
    runs-on: ubuntu-latest
    permissions:
      security-events: write

    strategy:
      matrix:
        language: ['javascript', 'python']

    steps:
      - uses: actions/checkout@v4

      - name: Initialize CodeQL
        uses: github/codeql-action/init@v2
        with:
          languages: ${{ matrix.language }}

      - name: Autobuild
        uses: github/codeql-action/autobuild@v2

      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v2
```

```bash
# Semgrep
pip install semgrep
semgrep --config=auto .
semgrep --config=p/security-audit .
semgrep --config=p/owasp-top-ten .

# ESLint security plugin
npm install eslint-plugin-security
# .eslintrc.json
{
  "plugins": ["security"],
  "extends": ["plugin:security/recommended"]
}

# Bandit (Python)
pip install bandit
bandit -r ./src
```

### Step 3: Secret Detection

```bash
# GitLeaks
gitleaks detect --source . --verbose
gitleaks detect --source . --report-path gitleaks-report.json

# TruffleHog
trufflehog git file://. --only-verified

# detect-secrets
pip install detect-secrets
detect-secrets scan > .secrets.baseline
detect-secrets audit .secrets.baseline
```

```yaml
# Pre-commit hook
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks

  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
```

```yaml
# GitHub Actions - Secret scanning
name: Secret Scan

on: [push, pull_request]

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: GitLeaks
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Step 4: Container Scanning

```bash
# Trivy
trivy image myapp:latest
trivy image --severity HIGH,CRITICAL myapp:latest
trivy image --exit-code 1 --severity CRITICAL myapp:latest

# Grype
grype myapp:latest
grype myapp:latest --fail-on high

# Docker Scout
docker scout cves myapp:latest
docker scout recommendations myapp:latest
```

```yaml
# GitHub Actions - Container scanning
- name: Build image
  run: docker build -t myapp:${{ github.sha }} .

- name: Scan image
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: myapp:${{ github.sha }}
    format: 'sarif'
    output: 'trivy-results.sarif'
    severity: 'HIGH,CRITICAL'
    exit-code: '1'

- name: Upload scan results
  uses: github/codeql-action/upload-sarif@v2
  if: always()
  with:
    sarif_file: 'trivy-results.sarif'
```

### Step 5: Infrastructure Scanning

```bash
# Checkov (Terraform, CloudFormation, Kubernetes)
pip install checkov
checkov -d . --framework terraform
checkov -f deployment.yaml --framework kubernetes

# tfsec (Terraform)
tfsec .
tfsec . --minimum-severity HIGH

# kube-bench (Kubernetes CIS)
docker run --rm -v /etc:/etc:ro aquasec/kube-bench:latest

# Terrascan
terrascan scan -t aws
```

```yaml
# GitHub Actions - IaC scanning
- name: Checkov
  uses: bridgecrewio/checkov-action@v12
  with:
    directory: ./terraform
    framework: terraform
    soft_fail: false

- name: tfsec
  uses: aquasecurity/tfsec-action@v1.0.0
  with:
    soft_fail: false
```

### Step 6: Dynamic Analysis (DAST)

```bash
# OWASP ZAP
docker run -t owasp/zap2docker-stable zap-baseline.py -t https://app.example.com

# Nikto
nikto -h https://app.example.com

# nuclei
nuclei -u https://app.example.com -t cves/
```

```yaml
# GitHub Actions - ZAP scan
- name: ZAP Scan
  uses: zaproxy/action-baseline@v0.9.0
  with:
    target: 'https://staging.example.com'
    rules_file_name: '.zap/rules.tsv'
    cmd_options: '-a'
```

---

## Templates

### Complete Security Pipeline

```yaml
name: Security

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  secrets:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  sast:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: github/codeql-action/init@v2
        with:
          languages: javascript
      - uses: github/codeql-action/autobuild@v2
      - uses: github/codeql-action/analyze@v2

  dependencies:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm audit --audit-level=high

  containers:
    runs-on: ubuntu-latest
    needs: [secrets, sast, dependencies]
    steps:
      - uses: actions/checkout@v4
      - run: docker build -t app:${{ github.sha }} .
      - uses: aquasecurity/trivy-action@master
        with:
          image-ref: app:${{ github.sha }}
          exit-code: '1'
          severity: 'CRITICAL'

  infrastructure:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: bridgecrewio/checkov-action@v12
        with:
          directory: ./terraform
```

### Security Policy

```markdown
# SECURITY.md

## Reporting a Vulnerability

Please report security vulnerabilities to security@example.com.

Do NOT create public GitHub issues for security vulnerabilities.

## Response Timeline

- Acknowledgment: Within 24 hours
- Initial assessment: Within 72 hours
- Fix deployment: Within 30 days for critical issues

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 2.x     | :white_check_mark: |
| 1.x     | :x:                |
```

---

## Common Mistakes

1. **Ignoring scan results** - Fix or document exceptions
2. **No baseline** - Creates alert fatigue
3. **Only scanning main** - Scan PRs too
4. **Missing dependencies** - Scan transitive deps
5. **No enforcement** - Scans must block merge

---

## Checklist

- [ ] Dependency scanning (npm audit, Snyk)
- [ ] Static analysis (CodeQL, Semgrep)
- [ ] Secret detection (GitLeaks)
- [ ] Container scanning (Trivy)
- [ ] IaC scanning (Checkov, tfsec)
- [ ] Pre-commit hooks
- [ ] CI/CD integration
- [ ] Security policy documented

---

## Next Steps

- M-DO-014: Secrets Management
- M-DO-020: Container Registry
- M-DO-001: GitHub Actions

---

*Methodology M-DO-021 v1.0*
