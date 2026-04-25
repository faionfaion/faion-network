# Agent Integration — Security Testing

## When to use
- Pre-deploy gate after any change touching auth, sessions, file upload, deserialization, templating, or external HTTP/SQL queries.
- After bumping dependencies (transitive vulns surface via CVE feeds).
- Generating OWASP-Top-10 fuzz suites for an existing API once the contract is stable.
- Wiring SAST + secrets + dep-audit into CI before opening the project to outside contributors.
- Reviewing a third-party AI-generated PR — LLMs frequently re-introduce SQL string concatenation, `eval`, `subprocess shell=True`, missing CSRF, weak hashing.

## When NOT to use
- Pre-commit on every save: fuzzing/DAST is too slow; restrict to PR/CI or nightly.
- As a substitute for threat modelling — testing only finds what you tell it to look for.
- For business-logic flaws (price tampering, IDOR via valid-but-wrong IDs) — those need handwritten scenario tests, not scanners.
- Penetration testing of production without written authorization (legal exposure).

## Where it fails / limitations
- SAST (Bandit, Semgrep) drowns in false positives on Django ORM and dynamic Python; tune the ruleset or you’ll desensitize reviewers.
- `safety`/`pip-audit` only catch known CVEs — zero-days and supply-chain attacks (typosquatting, malicious post-install) are invisible.
- DAST tools cannot reach endpoints that need a logged-in admin + multi-step state without a tuned auth recorder.
- LLM-generated security tests often assert `status_code != 500` instead of `== 403/401/400` — they confirm "no crash" not "correctly denied".
- Hardcoded test credentials in the suite become real secrets the moment the repo goes public.

## Agentic workflow
Run the agent over a clean checkout to seed a baseline (`semgrep --config p/owasp-top-ten`, `bandit -r src/`, `pip-audit`, `gitleaks detect`). Save findings as JSON, feed each finding back to a sonnet/opus agent with the file context and ask for a minimal patch + a regression test. Triage layer: another agent labels each finding `true-positive | false-positive | accepted-risk` with justification, and only TPs become PRs. Always require a human sign-off before merging anything in the auth, crypto, or session-handling path.

### Recommended subagents
- `security-review` (built-in slash skill) — runs against the current branch; use it as the first pass before custom pipelines.
- `password-scrubber-agent` (in `agents/`) — sweeps the diff for committed credentials before push.
- `faion-sdd-executor-agent` — to drive the fix-and-regression-test loop one finding at a time with quality gates.

### Prompt pattern
```
Given this Semgrep finding (rule: <id>, file: <path>, line: <n>),
1. Confirm exploitability with a concrete attack payload.
2. Propose the minimal patch (no refactor).
3. Write a pytest that fails on the unpatched code and passes on the patched code.
Output JSON: {verdict, patch, test, justification}.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Semgrep | Multi-lang SAST, rule packs `p/owasp-top-ten`, `p/secrets`, `p/django` | `pip install semgrep` · semgrep.dev |
| Bandit | Python SAST | `pip install bandit` · bandit.readthedocs.io |
| pip-audit | Python dep CVE scan (PyPI Advisory DB) | `pip install pip-audit` · pypa/pip-audit |
| safety | Python dep CVE scan (Safety DB) | `pip install safety` |
| npm audit / pnpm audit | JS/TS dep scan | bundled with package manager |
| osv-scanner | Multi-lang OSV.dev CVE scan | google/osv-scanner |
| trivy | Container + IaC + dep scan | aquasec/trivy |
| gitleaks | Pre-commit + repo secret scan | gitleaks/gitleaks |
| trufflehog | Verified-secret scan with provider checks | trufflesecurity/trufflehog |
| ZAP / zaproxy | DAST proxy + automation framework | zaproxy.org |
| nuclei | Template-driven vuln scanner for known CVEs | projectdiscovery/nuclei |
| sqlmap | SQLi exploitation (test envs only) | sqlmap.org |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Advanced Security (CodeQL, Dependabot, secret scan) | SaaS | Yes — REST + GraphQL API | Best out-of-the-box flow if already on GitHub. |
| Snyk | SaaS | Yes — `snyk` CLI + REST API | Strong dep + IaC + container coverage; license noise on OSS plans. |
| Socket.dev | SaaS | Partial — webhooks + API | Behaviour-based supply-chain (post-install scripts, telemetry). |
| StackHawk / Bright | SaaS | Yes — CLI for CI | Authenticated DAST, easier than self-hosting ZAP. |
| OWASP ZAP | OSS | Yes — daemon mode + API | Can be driven by an agent via the REST API or `zap-cli`. |
| Trivy / Grype | OSS | Yes — JSON output | Stick to one to avoid noise; trivy covers more file types. |
| HashiCorp Vault | OSS / SaaS | Yes — CLI + API | Move secrets out of `.env` so leak blast radius drops. |
| 1Password CLI (`op`) | SaaS | Yes — CLI | Used by this workspace; agents should fetch creds via `op` not env files. |

## Templates & scripts
See `templates.md` and `examples.md` for OWASP suite, Bandit config, GitHub Actions `security.yml`. Minimal triage helper:

```python
# scripts/triage_semgrep.py
import json, sys, pathlib
findings = json.loads(pathlib.Path(sys.argv[1]).read_text())["results"]
buckets = {"high": [], "medium": [], "low": []}
for f in findings:
    sev = f["extra"]["severity"].lower()
    buckets.setdefault(sev, []).append({
        "rule": f["check_id"],
        "path": f["path"],
        "line": f["start"]["line"],
        "msg": f["extra"]["message"][:120],
    })
for level, items in buckets.items():
    print(f"## {level.upper()} ({len(items)})")
    for i in items:
        print(f"- {i['path']}:{i['line']} [{i['rule']}] {i['msg']}")
```

## Best practices
- Pin scanner versions in CI; auto-bumps silently change rule sets and break builds.
- Maintain a `.semgrepignore` / `.banditignore` with rationale per entry — never blanket-ignore a rule.
- Treat secrets in git history as compromised: rotate first, scrub second; `git-filter-repo` does not recover the leaked credential.
- Run dependency audit on the lockfile, not `requirements.txt`/`package.json`, to catch transitive vulns.
- Add per-PR quality gate: fail build only on new high/critical findings vs. baseline; total-count gates lock you out of legacy code forever.
- For auth tests, assert exact status codes (`401`/`403`) and absence of leaked headers (`Server`, `X-Powered-By`), not just non-500.

## AI-agent gotchas
- LLMs love `assert response.status_code != 500` — that passes on a 200 OK that returned the victim's data. Always require explicit allow-listed status codes.
- An agent told to "fix the SQL injection" may rewrite the query with `f"... {sanitize(user_input)} ..."` and a homemade sanitizer; force parameterised queries (`?` / `%s` / `$1`) in the prompt.
- Agents will happily commit `.env.example` with real-looking values that turn out to be real; route every diff through `gitleaks` or `password-scrubber-agent` before push.
- DAST runs at full tilt will trip your own rate-limiter / WAF and get the agent IP-banned — scope to a staging URL with elevated limits.
- Fuzz suites generated by LLMs frequently hit `/api/admin` while authenticated as admin and "prove" the endpoint is unreachable. Use a low-privilege fixture user.
- Human-in-loop checkpoint: any patch in `auth/`, `crypto/`, `session/`, `webhook signature` must require explicit human approval; never auto-merge.

## References
- OWASP Top 10 — https://owasp.org/Top10/
- OWASP Web Security Testing Guide — https://owasp.org/www-project-web-security-testing-guide/
- OWASP ASVS — https://owasp.org/www-project-application-security-verification-standard/
- Semgrep registry — https://semgrep.dev/explore
- OSV.dev — https://osv.dev/
- NIST SSDF (SP 800-218) — https://csrc.nist.gov/Projects/ssdf
