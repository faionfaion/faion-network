# Agent Integration — Quality Management (PMBoK)

## When to use
- Software / hardware programs with external acceptance criteria (UAT sign-off, FDA/EMA submission, ISO 9001 surveillance audits, automotive ASPICE).
- Multi-team programs where Definition of Done drift across teams creates integration defects.
- Regulated domains needing documented Quality Plan, Quality Assurance audits, and Quality Control records (medical, aerospace, finance, public sector).
- Programs with explicit SLA / SLO obligations where escape defect rates and uptime are contractual.
- Quality gates in CI/CD pipelines that block merges, releases, and deployments.
- Pair with `change-control/`, `lessons-learned/`, `risk-management/`, dev `code-quality/`, dev `testing-developer/`, ux `usability-testing/`.

## When NOT to use
- Pre-PMF startups iterating on prototypes — heavy quality plans slow learning; use `code-quality/` and basic CI checks.
- Throwaway spikes / POCs — DoD is "demo runs once".
- One-person side projects — checklist overhead exceeds defect cost.
- Pure research / scientific exploration where the deliverable is a finding, not a product.
- When the real bottleneck is requirements clarity, not quality — fix scope/requirements first (`scope-management`, BA `requirements-validation`).

## Where it fails / limitations
- Conflates Cost-of-Quality (prevention + appraisal + failure) with mere QA budget; teams under-invest in prevention because failure cost is invisible.
- Definition of Done is a checkbox cargo cult unless tied to measurable acceptance criteria and runtime evidence (test coverage, security scan, perf baseline).
- "Quality is everyone's job" → in practice no one owns it; missing named QA owner per workstream is a common failure.
- Static checklists rot; programs accumulate dozens of checklists that nobody updates.
- LLMs grading "code quality" produce confident but inconsistent verdicts; deterministic linters and SAST beat narrative review for pass/fail gates.
- Process metrics (DoD compliance) become targets and lose information value (Goodhart's law).
- Cross-team DoD harmonization is political — central enforcement breeds workarounds, decentralization breeds drift.
- UAT sign-off cannot substitute for production telemetry; defects escape UAT every release.

## Agentic workflow
Quality is encoded as a typed `quality-plan.yaml` in git: standards, metrics, thresholds, gates, owners. CI runs deterministic checks (lint, type, test, coverage, SAST, perf) and emits a machine-readable QA report. A subagent reads that report plus issue tracker data and produces the Quality Dashboard with computed RAG. A second subagent triages new defect reports — extracting steps, environment, severity, and proposing a duplicate match before assigning. Quality gate decisions (release / hold / abort) require human approval; agents emit recommendations only.

### Recommended subagents
- `faion-sdd-executor-agent` — drives quality work as SDD tasks (TASK_define_dod, TASK_quality_plan, TASK_release_gate, TASK_audit_prep).
- Custom `dod-checker-agent` (sonnet) — given a PR / story, validates against `quality-plan.yaml` checklist; outputs structured pass/fail per criterion with evidence link (CI run, test report, coverage report).
- Custom `defect-triage-agent` (sonnet) — parses incoming bug reports; normalizes to schema; runs duplicate detection (embedding similarity) against existing tickets; assigns severity by rubric.
- Custom `quality-dashboard-agent` (sonnet) — aggregates CI outputs, defect tracker, telemetry; emits Sprint Quality Report with computed metrics, no opinion-based GREEN.
- Custom `audit-prep-agent` (opus) — for ISO/SOC2/regulatory audits, walks `quality-plan.yaml` evidence requirements and produces a gap report.
- Custom `escape-analyzer-agent` (opus) — for production defects that escaped pre-release testing, identifies missing gate / weak control; emits proposed prevention update.

### Prompt pattern
```
You are dod-checker. Inputs: PR diff, quality-plan.yaml, CI run.json, test-report.xml,
coverage.xml, sast.sarif. For each DoD item, emit STRICT JSON:
{ "criterion": "...", "status": "pass|fail|n/a", "evidence_url": "...",
  "evidence_summary": "<= 1 line", "blocking": true|false }
Rules: pass requires concrete evidence (CI URL, log line, file:line).
"n/a" requires explicit rationale field. Never assume pass without evidence.
```

Defect triage prompt: `Normalize defect report to schema {id, severity, priority, summary, repro, expected, actual, env, logs, suspected_root_cause, duplicates[]}. Severity rubric in quality-plan.yaml. Run duplicate match against last 90 days of tickets.`

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ruff` / `eslint` / `golangci-lint` | Deterministic style + bug rules | language-specific |
| `mypy` / `pyright` / `tsc --noEmit` | Type checking | language-specific |
| `pytest --cov` / `jest --coverage` / `go test -cover` | Test + coverage | preinstalled |
| `sonar-scanner` | SonarQube static analysis | https://docs.sonarsource.com/sonarqube |
| `semgrep` | Custom security/quality rules; agent-friendly SARIF output | https://semgrep.dev |
| `trivy` / `grype` | SCA / container vuln scanning | https://aquasecurity.github.io/trivy |
| `bandit` (Python) / `gosec` (Go) | SAST | https://bandit.readthedocs.io |
| `k6` / `locust` | Performance gate scripts | https://k6.io |
| `playwright` / `cypress` | E2E acceptance gates | https://playwright.dev |
| `pa11y-ci` / `axe-core` | Accessibility gates | https://pa11y.org |
| `gh checks` / `glab ci` | Aggregate gate status | https://cli.github.com |
| `pre-commit` | Local enforcement of quality plan basics | https://pre-commit.com |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| GitHub Actions / GitLab CI / Jenkins / CircleCI | SaaS / OSS | REST + JSON | Quality gate runtime; mandatory for deterministic gates. |
| SonarQube / SonarCloud | OSS / SaaS | REST | Code quality with thresholds; webhook to gate. |
| Codacy / DeepSource | SaaS | REST | Lighter alternative; less configurable than Sonar. |
| Snyk / GitHub Advanced Security / Dependabot | SaaS | REST | Vuln gates; severity feeds into quality dashboard. |
| Datadog / New Relic / Grafana / Honeycomb | SaaS | REST | Production quality telemetry; SLO-based gates. |
| Sentry / Rollbar / Bugsnag | SaaS | REST | Escape defect tracking; webhook → triage agent. |
| Jira / Linear / Azure DevOps | SaaS | REST | Defect register; severity field; duplicate detection. |
| TestRail / Xray / Zephyr | SaaS | REST | Manual + automated test case repository. |
| Allure | OSS | filesystem reports | Aggregated test report artifact. |
| Drata / Vanta / Tugboat Logic | SaaS | REST | Continuous compliance; auto-evidence for ISO/SOC2 audits. |

## Templates & scripts
README provides Definition of Done, Quality Checklist, Defect Report. Inline below: a script that gates a PR by reading `quality-plan.yaml` thresholds and CI artifacts.

```python
#!/usr/bin/env python3
"""quality_gate.py — pass/fail PR against quality-plan.yaml."""
import json, sys, yaml, pathlib

def main(plan: str, ci: str) -> int:
    rules = yaml.safe_load(pathlib.Path(plan).read_text())["thresholds"]
    actual = json.loads(pathlib.Path(ci).read_text())
    fails = []
    for k, threshold in rules.items():
        v = actual.get(k)
        if v is None:
            fails.append(f"{k}: missing")
            continue
        op = threshold.get("op", ">=")
        target = threshold["value"]
        ok = (v >= target) if op == ">=" else (v <= target)
        if not ok:
            fails.append(f"{k}: {v} {op} {target} FAIL")
    if fails:
        sys.stdout.write("\n".join(fails) + "\n")
        return 1
    sys.stdout.write("Quality gate PASSED\n")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
```

Run as a CI step; non-zero exit blocks merge.

## Best practices
- Quality Plan in git (`quality-plan.yaml`): standards, metrics, thresholds, gates, owners; PR-reviewed, versioned, tagged.
- Definition of Done is per-artifact-type (story, feature, release) with measurable criteria; don't put narrative items in DoD.
- Prevention > detection — invest in linters, types, contracts, generative testing before adding more manual review.
- Cost-of-Quality tracking: log prevention, appraisal, internal-failure, external-failure costs; CoQ trend reveals true ROI.
- Escape-defect retrospective is mandatory for any production defect rated S1/S2; output is a quality plan amendment, not blame.
- Tie quality metrics to SLO/SLA, not vanity numbers; "test coverage 80%" without integration coverage is misleading.
- Centralize defect schema; one severity rubric, one priority rubric, one taxonomy across the program.
- Audit evidence is generated, not curated — every gate run produces an immutable artifact with timestamp, inputs, outputs.
- Quality owner is named per workstream (not "the team"); CODEOWNERS on `quality-plan.yaml`.
- Beware Goodhart: rotate which metrics gate vs. which inform; gating on the same metric for years invites gaming.

## AI-agent gotchas
- LLMs grade "code quality" inconsistently; never let an agent be the sole gate authority — pair with deterministic tools.
- Agents reading test reports skip the parts they cannot interpret (binary blobs, large logs); always pre-process to structured JSON before prompt.
- Defect triage agents over-merge duplicates because of surface similarity; require >0.85 embedding cosine + matching environment before auto-link.
- Severity inflation: agents rate everything S2/S3 to be "safe"; force a calibration set with examples in the prompt.
- Agents writing defect reports invent reproduction steps; ground on actual logs/traces and refuse to fabricate steps.
- Privacy: defect logs frequently leak PII (user IDs, emails, payment data); scrub before sending to a third-party model.
- Audit-prep agents producing "evidence" without traceable source create regulatory liability; every evidence claim must point to an immutable artifact.
- Auto-closing duplicates without human review erases information; agent recommends, human merges.
- Coverage hallucination: agents claim coverage that exceeds the actual report; always trust the file, not the LLM summary.
- Human-in-the-loop checkpoints (mandatory): release gate decisions, escape-defect classification, severity overrides, audit evidence approval, DoD changes.

## References
- PMI PMBOK 7e — Delivery Performance Domain (Quality).
- PMI PMBOK 6e — Project Quality Management Knowledge Area.
- ISO 9001:2015 — Quality management systems.
- ISO/IEC 25010 — Software product quality model.
- Crosby, P. — "Quality Is Free" (Cost of Quality).
- Deming, W. E. — "Out of the Crisis" (PDCA, system of profound knowledge).
- Juran, J. — "Juran's Quality Handbook".
- Beck, K. / Fowler, M. — "Refactoring" (preventive quality).
- Sibling methodologies: `change-control/`, `risk-management/`, `lessons-learned/`, dev `code-quality/`, dev `testing-developer/`, ux `usability-testing/`.
