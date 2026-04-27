# Security Testing

## Summary

Layered security testing using SAST (static code analysis), DAST (dynamic attack simulation), SCA (dependency vulnerability scanning), and secret detection — integrated at every stage of the CI/CD pipeline. Every PR must pass SAST and secrets checks; DAST runs nightly on staging; container scans run on image build.

## Why

Attackers exploit known vulnerability patterns (OWASP Top 10, API Security Top 10) that automated tools can detect before deployment. Shift-left integration (SAST on every commit, secrets pre-commit) reduces fix cost by orders of magnitude compared to post-production discovery. Tools do not replace threat modeling or manual penetration testing — they triage known patterns so humans focus on logic flaws.

## When To Use

- Every change to auth, authorization, input handling, file upload, deserialization, crypto, or session code
- Pre-launch on new services before internet exposure
- Continuous: SAST + secret scanning on every PR, SCA on every build, DAST nightly on staging
- New dependency adoption (SCA before merge)
- Incident response to confirm scope and regression-test the fix
- Compliance audits (SOC 2, ISO 27001, PCI)

## When NOT To Use

- As a substitute for threat modeling — tools find known patterns; design flaws hide from scanners
- DAST against any environment with real user data, real billing, or real downstream effects
- Replacing manual review for critical-path code (auth, crypto, payment)
- Auto-merging security patches without human review

## Content

| File | What's inside |
|------|---------------|
| `content/01-pipeline-and-rules.xml` | CI/CD integration points, gate criteria, shift-left rules |
| `content/02-tool-categories.xml` | SAST/DAST/SCA/secrets tool table with usage context |
| `content/03-owasp-and-api-security.xml` | OWASP Top 10 2025, API Security Top 10 2023, auth/authz test cases |
| `content/04-gotchas.xml` | AI-agent gotchas, limitations, best practices |

## Templates

| File | Purpose |
|------|---------|
| `templates/security-pipeline.yml` | GitHub Actions security workflow (SAST + secrets + SCA + container) |
| `templates/prompt-triage-findings.txt` | Agent prompt: triage scanner JSON by reachability, open fix PR |
| `templates/prompt-api-audit.txt` | Agent prompt: audit routes for OWASP API Top 10 issues |
