# Static Application Security Testing (SAST) in CI/CD

## Summary

**One-sentence:** Produces a SAST CI config (Semgrep / CodeQL / etc.) with PR-gate on CRITICAL+HIGH only, MEDIUM+LOW informational, baseline for legacy code, and pinned scanner version.

**One-paragraph:** SAST is the cheapest security feedback loop — runs on the PR diff, finds vulnerabilities before merge. The non-negotiable: block on CRITICAL+HIGH only at start (MEDIUM/LOW informational), pin scanner image + rule pack (no `@master`), baseline existing findings on first integration so legacy code doesn't drown new work, and emit SARIF to GitHub Code Scanning. Tool choice: CodeQL for GitHub-native + semantic analysis; Semgrep for custom rules + multi-platform; Snyk Code for AI-driven autofix; SonarQube for code-quality + security combined.

**Ефективно для:**

- Будь-який проект, що ships код у prod — SAST = мінімальний security gate.
- PR-level feedback: developer бачить finding до merge.
- Custom rules для domain-specific patterns (hardcoded secrets, SQL interpolation).
- Wiring SARIF у GitHub Code Scanning / GitLab Code Quality.

## Applies If (ALL must hold)

- Project ships code to production (not throwaway scripts).
- CI is in place AND can run a scanner step on PRs.
- Severity policy can be agreed (start with block on CRITICAL+HIGH).

## Skip If (ANY kills it)

- Replacing DAST — SAST cannot see runtime issues (auth bypass, SSRF, business logic).
- Greenfield exploration with fluid requirements — FP volume will drown the team before rules are tuned.
- One-off scripts / scratch repos — overhead exceeds value.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Language list | list of primary languages in the repo | repo analysis |
| Severity policy | block list (start CRITICAL+HIGH) | security team |
| Baseline strategy | ignore-existing OR fail-on-existing | security team |
| Custom rules (optional) | list of project-specific patterns | security team |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[security-container-scanning]] | SAST + image scan complement each other |
| [[security-dast]] | SAST is shift-left; DAST is shift-right |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: block-critical-high-only, pin-scanner-and-rules, baseline-existing-findings, sarif-uploaded, skip-this-methodology | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for SAST CI config + valid/invalid + forbidden | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: block-on-every-finding, floating-rule-pack, no-baseline, sarif-skipped | 800 |
| `content/04-procedure.xml` | essential | 5 steps: pick tool → pin → baseline → PR gate → SARIF upload | 800 |
| `content/06-decision-tree.xml` | essential | Decision tree on stack + hosting → tool | 800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pick-tool` | haiku | Deterministic on hosting (GitHub / GitLab / self) + stack. |
| `compose-workflow` | sonnet | Assemble the CI YAML with correct permissions + baseline. |
| `triage-findings` | sonnet | Reduce FP rate; author exemptions with rationale + expiry. |

## Templates

| File | Purpose |
|------|---------|
| `templates/semgrep.yml` | GitHub Actions workflow: Semgrep CI with SARIF upload |
| `templates/codeql.yml` | GitHub Actions workflow: CodeQL with weekly schedule + matrix per language |
| `templates/.semgrep/no-hardcoded-secrets.yaml` | Custom Semgrep rule: hardcoded passwords + API keys |
| `templates/_smoke-test.json` | Minimum SAST CI config artefact used by validate-security-sast.py --self-test |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-security-sast.py` | Validate the config artefact against the schema in `content/02-output-contract.xml` | CI on every artefact change + pre-commit hook |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[security-container-scanning]]
- [[security-dast]]
- [[secrets-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals on the input to a conclusion that points back to a rule from `01-core-rules.xml`. Use it when wiring SAST into a new repo or auditing an existing PR-gate.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/semgrep.yml`

```yaml
name: semgrep
on:
  pull_request: {}
  push:
    branches: [main, master]

permissions:
  contents: read
  security-events: write

jobs:
  semgrep:
    runs-on: ubuntu-latest
    container:
      image: semgrep/semgrep:1.65.0
    steps:
      - uses: actions/checkout@v4
      - name: Run Semgrep
        run: semgrep ci --sarif --output semgrep.sarif --severity ERROR --severity WARNING
        env:
          SEMGREP_APP_TOKEN: ${{ secrets.SEMGREP_APP_TOKEN }}
      - uses: github/codeql-action/upload-sarif@v3
        if: always()
        with: { sarif_file: semgrep.sarif }
```

### `templates/codeql.yml`

```yaml
name: codeql
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: "0 6 * * 1"

permissions:
  security-events: write
  actions: read
  contents: read

jobs:
  analyze:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        language: [javascript, python]
    steps:
      - uses: actions/checkout@v4
      - uses: github/codeql-action/init@v3
        with:
          languages: ${{ matrix.language }}
          queries: +security-extended,security-and-quality
      - uses: github/codeql-action/autobuild@v3
      - uses: github/codeql-action/analyze@v3
        with:
          category: "/language:${{ matrix.language }}"
```

### `templates/.semgrep/no-hardcoded-secrets.yaml`

```yaml
rules:
  - id: hardcoded-password
    patterns:
      - pattern-either:
          - pattern: password = "..."
          - pattern: PASSWORD = "..."
          - pattern: passwd = "..."
    message: "Hardcoded password — move to a secret manager."
    languages: [python, javascript, typescript]
    severity: ERROR
  - id: hardcoded-api-key
    pattern-regex: '(?i)(api[_-]?key|apikey)\s*[=:]\s*["''][a-zA-Z0-9]{20,}["'']'
    message: "Possible hardcoded API key — move to a secret manager."
    languages: [generic]
    severity: WARNING
```

### `templates/_smoke-test.json`

```json
{
  "tool": "semgrep",
  "tool_version": "1.65.0",
  "severity_block": [
    "ERROR"
  ],
  "severity_inform": [
    "WARNING",
    "INFO"
  ],
  "baseline_strategy": "ignore-existing",
  "sarif_uploaded": true,
  "pr_gate": true
}
```
