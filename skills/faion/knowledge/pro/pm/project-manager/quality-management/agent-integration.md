# Agent Integration — Quality Management

## When to use
- Setting Definition of Done across a multi-team/multi-repo product
- Defect-escape rate climbing or production incidents recurring on the same surfaces
- Codebase has no quality dashboard and PM/PO cannot answer "is the trend better?"
- Pre-release hardening: agent-driven quality audit before a major launch
- Compliance kickoff (SOC2, ISO 9001) where evidence trail must be reproducible

## When NOT to use
- One-person prototype before product-market fit — quality gates slow validation loops
- Spike/research code marked throwaway — formal QC inflates effort 2-3x
- When team rejects DoD as "ceremony" — fix the trust issue first, then introduce gates
- For aesthetic taste (UX polish) — use design review, not quality management

## Where it fails / limitations
- Coverage % becomes Goodhart target (developers write trivial tests to hit 80%)
- DoD checklists ossify; teams check the box without reading
- "Zero critical bugs" hides triage bias — severity gets downgraded under pressure
- Quality gates without trend analysis flag noise; root-cause loops are missing
- Inspection-only QA finds defects but cannot prevent them — too late, too costly

## Agentic workflow
A quality-auditor subagent reads the changed files in a PR, applies the DoD checklist, runs static analysis (ruff, eslint, sonar), and posts a structured review. A second metric-collector agent aggregates coverage, defect rate, escape rate, MTTR into a weekly dashboard. Human-in-loop is required for severity classification and for any waiver decision — the agent flags, the human decides. Pair with `code-review` skill for the actual review pass.

### Recommended subagents
- `dod-validator` — checks PR against DoD line items, posts pass/fail per item
- `quality-metric-collector` — pulls coverage, lint, defect counts, MTTR; emits dashboard JSON
- `defect-triager` — drafts severity + priority, references similar past issues, asks human to confirm
- `quality-trend-analyst` — weekly run, identifies regressions in any metric, opens incident if SPC limits breached

### Prompt pattern
```
You are a dod-validator subagent. Apply DoD {dod.yaml} to PR diff {diff}.
For each item return: {item_id, status: pass|fail|n/a, evidence_link}.
Block merge if any "must" item fails. Do not invent evidence.
```

```
You are a defect-triager. Given bug report {report}, draft severity (Critical|
High|Medium|Low) with one-sentence rationale citing user impact, frequency,
workaround. Output JSON {severity, priority, rationale, similar_issue_ids}.
Wait for human confirm before assigning.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `sonar-scanner` | Static analysis, code smells, coverage | https://docs.sonarsource.com/sonarqube/latest/analyzing-source-code/scanners/sonarscanner/ |
| `ruff` | Python lint + format (replaces black + flake8) | `pip install ruff` |
| `eslint` | JS/TS lint | `npm i -D eslint` |
| `pytest --cov` | Python coverage | `pip install pytest-cov` |
| `c8` / `nyc` | JS/TS coverage | `npm i -D c8` |
| `gh pr checks` | Read CI quality gate status | https://cli.github.com |
| `gitleaks` | Secret scanning, security gate | https://github.com/gitleaks/gitleaks |
| `semgrep` | Pattern-based static analysis | https://semgrep.dev |
| `trivy` | Container/SBOM vulnerability scan | https://aquasecurity.github.io/trivy |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| SonarQube/SonarCloud | OSS / SaaS | Yes | Web API for issues, quality gates, coverage |
| Codacy | SaaS | Yes | REST API, multi-language analysis |
| Code Climate | SaaS | Yes | Maintainability + test coverage, GitHub native |
| Codecov | SaaS | Yes | Coverage trend API, PR comments |
| Sentry | SaaS/OSS | Yes | Defect-in-prod telemetry, API for events |
| BugSnag | SaaS | Yes | Stability score API |
| TestRail | SaaS | Partial | Test case management, REST API but seat-priced |
| Zephyr | SaaS | Partial | Jira-coupled QA, API exists |
| BrowserStack | SaaS | Yes | Cross-browser test runs via API |

## Templates & scripts
See templates.md for DoD, defect report, quality checklist. Inline DoD-validator stub:

```python
# dod_validator.py — minimal PR DoD gate
import sys, json, subprocess
DOD = [
    ("tests_pass", lambda: run("pytest -q") == 0),
    ("coverage_80", lambda: coverage_pct() >= 80),
    ("lint_clean", lambda: run("ruff check .") == 0),
    ("no_secrets", lambda: run("gitleaks detect --no-banner") == 0),
]
def run(cmd): return subprocess.call(cmd, shell=True)
def coverage_pct():
    r = subprocess.run(["coverage", "report", "--format=total"], capture_output=True, text=True)
    return float(r.stdout.strip() or 0)
results = [{"item": n, "pass": bool(fn())} for n, fn in DOD]
print(json.dumps(results, indent=2))
sys.exit(0 if all(r["pass"] for r in results) else 1)
```

## Best practices
- Lock DoD per repo in `quality/dod.yaml` and version it — agents read the file, not human prose
- Track defect escape rate (bugs found in prod / total bugs) as a leading indicator; SPC chart it
- Separate "must" from "should" in DoD; only "must" blocks merge, "should" opens a follow-up
- Run quality gate twice: pre-commit (fast) and pre-merge (full) — do not duplicate slow checks
- For agent-written code, raise the bar: 90%+ coverage, mutation testing on critical modules, no warning suppressions without comment
- Quality cost is U-shaped: too little = rework, too much = lost velocity. Re-tune gates quarterly using lead-time data

## AI-agent gotchas
- Coverage tools can be gamed by agents writing assertion-free tests — also gate on mutation score (mutmut, stryker)
- LLMs invent test cases that compile but assert tautologies — require at least one failing-then-passing red/green log per generated test
- Severity classification drifts toward "Medium" because it is the safest answer — calibrate with rubric examples and force evidence
- Static analyzers report thousands of legacy issues on first run; agents will try to fix all in one PR — chunk by file/module
- Sentry/BugSnag rate-limits can drop events in incident spikes; do not trust raw counts for SLO breaches
- DoD validators that auto-skip "n/a" items get exploited; require human approval for any "n/a" tag

## References
- ISO 9001:2015 (quality management systems)
- PMBoK 7th: Delivery Performance Domain
- W.E. Deming, *Out of the Crisis* (1986) — prevention over inspection
- Capers Jones, *Software Quality in 2024* — defect economics
- Google SRE Workbook, ch. 4 (SLOs and quality)
