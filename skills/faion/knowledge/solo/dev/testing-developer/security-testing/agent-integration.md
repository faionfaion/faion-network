# Agent Integration — Security Testing

## When to use
- Every change to authentication, authorization, input handling, file upload, deserialization, crypto, or session code.
- Pre-launch on new services, before exposing to the internet.
- Continuous: SAST + secret scanning on every PR, SCA on every build, DAST nightly on staging, container scan on image build.
- Adoption of new dependencies — SCA before merge, license scan in parallel.
- Incident response: confirm scope, find lateral movement, regression-test the fix.
- Compliance audits (SOC 2, ISO 27001, PCI) — auditors expect tooling + evidence.

## When NOT to use
- As a substitute for threat modeling. Tools find known patterns; design flaws hide from scanners.
- 100% scanner-driven security. The CVSS-9 a scanner finds is rarely the bug that breaches you.
- Pen-testing in production without explicit written approval and a rollback plan.
- DAST against any environment with real user data, real billing, or real downstream effects.
- Replacing manual review for critical-path code (auth, crypto, payment) — agents triage, humans decide.

## Where it fails / limitations
- High false-positive rates (especially DAST + SCA) erode trust. Triage process is mandatory.
- SAST cannot reason about runtime context — taint flows it can't see.
- DAST without authentication coverage misses 80% of the surface (the authenticated app).
- SCA flags transitive vulnerabilities that are unreachable in your code → noise.
- Scanners do not understand business logic (BOLA / IDOR are the #1 OWASP API risk and need humans).
- Container scans on every layer multiply findings; pin a base image and dedupe.
- Reachability analysis is the differentiator (Snyk Code, Semgrep Pro) but expensive.
- Secrets that have already been pushed are leaked forever — rotate, do not just remove from git.

## Agentic workflow
Agents triage scanner output, propose fixes, and write regression tests; they do NOT auto-merge security patches without human review. Pipeline: SAST + secrets on every commit (fast feedback), SCA on every build, DAST + container scan nightly. The agent reads scanner JSON, deduplicates against a baseline (`.semgrepignore`, `.snyk`, allowlist), classifies by reachability, and opens a triaged PR with the proposed fix and a test that fails on the unpatched code.

### Recommended subagents
- `security-review` (built-in Claude Code) — runs on every PR, summarizes risk, lists owasp categories.
- `faion-sdd-execution` — quality gate: SAST/secrets/SCA must pass; DAST baseline on staging before deploy.
- A `triage-bot` agent (Sonnet) — reduces scanner output to "exploitable + fixable now" subset, opens issues.
- A `fix-and-test` agent (Opus) — for high-confidence findings, writes the patch + the regression test in one PR.
- `nero-tools` — pages Telegram on Critical findings via `tg-send`.

### Prompt pattern
```
Read reports/semgrep.json and reports/trufflehog.json from this PR.
For each finding:
  1. Decide reachability (function called from a user-facing path? → critical;
     test code only → suppress with rationale).
  2. If reachable + High/Critical: open a fix proposal with a regression
     test that fails before the fix and passes after.
  3. If suppressed: add to .semgrepignore with a one-line reason and a
     review-by date.
Output: PR description draft + diff(s). Do not push.
```

```
Audit auth/middleware.py and routes/*.py for OWASP API Top 10 issues.
Focus on API1 (BOLA), API3 (BOPLA), API5 (BFLA). For each finding,
provide: file:line, risk, exploit sketch (curl), proposed fix.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `semgrep` | SAST, multi-language, fast, custom rules | `pip install semgrep` |
| `bandit` | Python SAST | `pip install bandit` |
| `gosec` | Go SAST | `go install github.com/securego/gosec/v2/cmd/gosec@latest` |
| `eslint-plugin-security` / `eslint-plugin-no-unsanitized` | JS/TS SAST | npm |
| `codeql` | Deep dataflow SAST | `gh extension install github/gh-codeql` |
| `trufflehog` | Secret scanning, 700+ detectors, verified | `brew install trufflehog` |
| `gitleaks` | Secret scan + pre-commit hook | `brew install gitleaks` |
| `detect-secrets` | Baseline-based secret scan | `pip install detect-secrets` |
| `trivy` | Containers, IaC, SBOM, deps | `brew install trivy` |
| `grype` + `syft` | Vuln scan + SBOM gen | `brew install grype syft` |
| `snyk` | SCA + Code + container | `npm i -g snyk` |
| `pip-audit` / `safety` | Python dependency vuln | `pip install pip-audit` |
| `npm audit` / `yarn npm audit` | Node deps | bundled |
| `cargo audit` / `cargo deny` | Rust deps | `cargo install cargo-audit cargo-deny` |
| `nuclei` | Template-based DAST | `brew install nuclei` |
| `zap-cli` / `zaproxy` | OWASP ZAP CLI + automation | docker `zaproxy/zap-stable` |
| `nikto` | Web server misconfig | `apt install nikto` |
| `sslyze` / `testssl.sh` | TLS configuration audit | brew/apt |
| `kube-bench` / `kube-hunter` | k8s CIS + scan | brew |
| `tfsec` / `checkov` | Terraform / IaC scan | `brew install tfsec checkov` |
| `osv-scanner` | Google OSV vuln DB | `brew install osv-scanner` |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Snyk | SaaS | Yes — `snyk` CLI, REST API | Code + Open Source + Container + IaC; PR fix bots |
| GitHub Advanced Security (CodeQL + Dependabot + Secret Scanning) | SaaS | Yes — gh API | Native to GitHub repos |
| Semgrep Cloud | SaaS + OSS | Yes — CLI + REST API | Custom rule engine, free tier |
| Sonatype Nexus / Lifecycle | SaaS | Yes — REST | SCA + license + policy |
| JFrog Xray | SaaS | Yes — REST | Artifact + container scanning |
| OWASP ZAP | OSS | Yes — Docker + REST API | DAST workhorse |
| Burp Suite Pro | Commercial | Partial — Burp REST API | Manual pentesting |
| StackHawk | SaaS | Yes — `hawk` CLI + IaC | DAST in CI |
| Wiz / Lacework / Aqua | SaaS | Yes — REST | CSPM + container security |
| HackerOne / Bugcrowd | SaaS | Manual | Bounty programs, agents triage incoming reports |
| Trivy + Harbor (registry) | OSS | Yes | Self-hosted container scan + registry |
| GitGuardian | SaaS | Yes — REST | Secret scanning + history monitoring |

## Templates & scripts
See `templates.md` for GitHub Actions security pipeline and `examples.md` for ZAP + Nuclei recipes.

Pre-merge security gate (drop into `.github/workflows/security.yml`):

```yaml
name: security
on: [pull_request]
jobs:
  sast-and-secrets:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - name: Semgrep
        uses: semgrep/semgrep-action@v1
        with: { config: 'p/owasp-top-ten p/security-audit' }
      - name: TruffleHog
        uses: trufflesecurity/trufflehog@main
        with: { extra_args: '--only-verified' }
      - name: Trivy fs
        run: trivy fs --severity HIGH,CRITICAL --exit-code 1 --ignore-unfixed .
      - name: Gitleaks
        uses: gitleaks/gitleaks-action@v2
```

## Best practices
- Shift left, but shift right too: SAST + DAST + RASP is a layered defense, no single tool is sufficient.
- Define a baseline. Pre-existing findings get a triage decision once; only new findings block PRs.
- Reachability over CVSS. A CVSS-10 in unreachable code is lower priority than a CVSS-6 in a public endpoint.
- Treat secrets in git history as compromised forever — rotate first, scrub later.
- Auth-cover DAST: provide ZAP / Burp / StackHawk a logged-in session via a custom auth script.
- Threat-model new features before tools touch them. Tools find what they know; threat modeling finds what you didn't think to build.
- Patch transitive deps via `npm overrides` / `poetry [tool.poetry.dependencies]` / `cargo [patch]`.
- Sign artifacts (cosign / sigstore), pin base images by digest, generate SBOM (`syft`), scan SBOM (`grype`).
- Human-in-loop on every Critical finding; agents may auto-PR Low/Medium with regression tests.
- Track time-to-remediate as a leading indicator of security posture.
- Penetration testing once a year + after major architectural changes — scanners do not replace pentesters.

## AI-agent gotchas
- Agents will "fix" findings by widening allowlists or suppressing rules. Lock `.semgrepignore` / `.snyk` behind a separate review path with a mandatory rationale + review-by date.
- LLM-generated regex for input validation is famously bypassable. Use battle-tested libraries (`bleach`, `defusedxml`, `validators`, `email-validator`, `urllib`) and pin them.
- Agents asked to "make tests pass" may delete failing security tests. Mark security tests in CI to fail the suite if they are skipped or removed.
- Auto-merging Dependabot/Snyk PRs without integration tests breaks prod weekly. Require green build + at least one passing integration test class on the changed dep.
- Agents can hallucinate CVE IDs and remediation steps. Always cross-check against NVD or osv.dev.
- Generated DAST scripts that mutate prod data leak into prod by mistake. Restrict DAST automation to non-prod URLs in policy + by ACL.
- Secret rotation requires coordinated changes (key in vault, app config, dependent services). An agent doing only one of three creates an outage. Stage rotation in a runbook the agent follows step-by-step.
- LLM-suggested crypto ("here's a custom AES-GCM wrapper") is the bug class to most fear. Force `cryptography.fernet`, libsodium, or KMS-managed keys; reject ad-hoc primitives.
- Agents suppressing CodeQL/Semgrep with `// nosec` need to write a one-line reason. CI lints commits for naked suppressions.
- An agent reading a vulnerability report and writing the fix needs the issue body, not just the code. Otherwise the patch is cosmetic. Wire the issue/PR body into the agent's context for any security task.

## References
- https://owasp.org/Top10/2025/
- https://owasp.org/API-Security/
- https://owasp.org/www-project-web-security-testing-guide/
- https://owasp.org/www-project-application-security-verification-standard/
- https://cheatsheetseries.owasp.org/
- https://semgrep.dev/explore
- https://docs.snyk.io/
- https://www.zaproxy.org/docs/
- https://github.com/trufflesecurity/trufflehog
- https://www.first.org/cvss/v3-1/specification-document
- https://slsa.dev/
- https://www.sigstore.dev/
- https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- https://www.nist.gov/cyberframework
