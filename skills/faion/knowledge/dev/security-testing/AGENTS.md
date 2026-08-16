# Security Testing

## Summary

**One-sentence:** Security-testing plan + report: SAST per language, dependency audit, DAST (ZAP) against staging, secrets scanning pre-commit, OWASP ASVS coverage matrix per release.

**One-paragraph:** Security testing fails when SAST runs once a quarter, when dependency audits ignore transitive deps, when DAST never sees auth-protected paths, when secret scanning runs only at PR (not pre-commit), and when the ASVS coverage is implicit. This methodology produces a per-release plan + report: SAST tools per language (semgrep / bandit / gosec), dependency audit via osv.dev + GitHub Advisory, ZAP authenticated scan against staging, gitleaks pre-commit + CI, and an ASVS L1 coverage matrix.

**Ефективно для:**

- Перший security pass перед production launch.
- SOC 2 / ISO 27001 готовність - треба ASVS matrix.
- Dependency hijack incident - переглянути audit pipeline.
- Secrets витекли в git - впровадити gitleaks pre-commit.
- DAST scan не покриває auth flow - налаштувати ZAP context.

## Applies If (ALL must hold)

- Service ships to production with internet exposure.
- Compliance regime (SOC 2 / ISO / GDPR) is in scope OR launch is imminent.
- Staging environment exists where DAST can run safely.
- Team can act on findings within a documented window.

## Skip If (ANY kills it)

- Project is local-only with no network surface.
- Compliance regime forbids running automated scans against this environment.
- Throwaway prototype with no production users or sensitive data.
- Security testing is delegated entirely to an external pentest firm under contract.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Language inventory | list of languages + versions | engineering |
| Dependency lockfiles | package-lock.json / poetry.lock / Cargo.lock | engineering |
| Staging URL + auth creds | test account credentials | platform |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[supply-chain-risk-checklist-spike]] | library-level supply-chain inputs feed dependency audit section. |
| [[rate-limiting]] | DAST should account for limits to avoid self-DoS during scan. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 rules: SAST on PR, dep audit with transitive, DAST authenticated, secrets pre-commit, ASVS matrix, fix window by severity, scan rate-limit aware | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step plan: SAST, dep audit, DAST, secrets, ASVS matrix | ~900 |
| `content/05-examples.xml` | essential | Worked example for a SaaS release security pass | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pick-sast` | haiku | Language → tool mapping. |
| `configure-dast-context` | sonnet | Per-app judgement on auth flow + rate limits. |
| `draft-asvs-matrix` | sonnet | Map controls to project state. |
| `triage-findings` | opus | Stakes high; severity vs exploitability judgement. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ci-security.yml` | GitHub Actions snippet wiring SAST + dep audit + secrets scan. |
| `templates/asvs-matrix.csv` | ASVS L1 coverage matrix template (markdown table). |
| `templates/bandit-config.yaml` | Bandit config: skip rules with project rationale + severity gate. |
| `templates/security-ci.yml` | Variant CI security workflow snippet (semgrep + bandit + gitleaks). |
| `templates/_smoke-test.json` | Minimum viable security report for validator smoke-test. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-security-testing.py` | Validate the artefact against `content/02-output-contract.xml` schema. | After draft, before merge; pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[supply-chain-risk-checklist-spike]]
- [[rate-limiting]]
- [[api-error-handling]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs - SAST cadence, transitive coverage, DAST auth, secrets gate - onto a rule from `content/01-core-rules.xml`. Use it before any release: it catches quarterly-SAST, direct-only deps, unauth-only DAST upstream.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/ci-security.yml`

```yaml
name: security
on: [pull_request]
jobs:
  sast:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: returntocorp/semgrep-action@v1
        with: { config: 'p/ci' }
      - run: pip install bandit && bandit -r .
  deps:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: google/osv-scanner-action@v1
  secrets:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - uses: zricethezav/gitleaks-action@v2
```

### `templates/asvs-matrix.csv`

```csv
# ASVS L1 Coverage

| Control | Status | Owner | Notes |
|---------|--------|-------|-------|
| V1.1.1  | covered | sec-team | Threat model up to date |
| V2.1.1  | covered | auth-team | bcrypt cost=12 |
| V5.1.1  | in-progress | api-team | Input validation 90% covered |
| V9.1.1  | accepted-risk | platform | TLS 1.3 only behind LB |
```

### `templates/bandit-config.yaml`

```yaml
skips: []

exclude_dirs:
  - tests
  - venv
  - .venv
  - migrations

# Core rules — do not blanket-skip without justification comment
tests:
  - B101  # assert_used
  - B102  # exec_used
  - B105  # hardcoded_password_string
  - B106  # hardcoded_password_funcarg
  - B107  # hardcoded_password_default
  - B110  # try_except_pass
  - B201  # flask_debug_true
  - B301  # pickle
  - B303  # md5
  - B307  # eval
  - B324  # hashlib_insecure_functions
  - B501  # request_with_no_cert_validation
  - B505  # weak_cryptographic_key
  - B506  # yaml_load
  - B602  # subprocess_popen_with_shell_equals_true
  - B608  # hardcoded_sql_expressions
  - B701  # jinja2_autoescape_false
  - B703  # django_mark_safe
```

### `templates/security-ci.yml`

```yaml
name: Security Scanning

on:
  push:
    branches: [main, develop]
  pull_request:
  schedule:
    - cron: '0 0 * * 0'  # Weekly

jobs:
  sast:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Bandit (Python SAST)
        run: |
          pip install bandit==1.7.7
          bandit -r src/ -f json -o bandit-report.json || true

      - name: Dependency audit (pip-audit)
        run: |
          pip install pip-audit==2.6.1
          pip-audit --format json > pip-audit-report.json || true

      - name: Semgrep (OWASP Top 10 + secrets)
        uses: returntocorp/semgrep-action@v1
        with:
          config: >-
            p/security-audit
            p/secrets
            p/owasp-top-ten

      - name: Secret scan (gitleaks)
        uses: gitleaks/gitleaks-action@v2

      - name: npm audit
        run: npm audit --json > npm-audit.json || true

      - name: Upload security reports
        uses: actions/upload-artifact@v4
        with:
          name: security-reports
          path: |
            bandit-report.json
            pip-audit-report.json
            npm-audit.json
```

### `templates/_smoke-test.json`

```json
{
  "release": "v1",
  "sast_tools": [
    "semgrep"
  ],
  "dep_audit": {
    "sources": [
      "osv.dev"
    ],
    "transitive": true
  },
  "dast": {
    "authenticated": true,
    "target": "https://staging"
  },
  "secrets_scan": {
    "pre_commit": true,
    "ci": true
  },
  "asvs_coverage": {
    "level": "L1",
    "covered_pct": 80
  },
  "fix_windows": {
    "critical_hours": 24,
    "high_days": 7,
    "medium_days": 30
  }
}
```
