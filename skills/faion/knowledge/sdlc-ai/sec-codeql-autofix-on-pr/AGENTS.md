# CodeQL + Copilot Autofix as the PR-time SAST Gate

## Summary

**One-sentence:** Enable GitHub Code Scanning with CodeQL on push + pull_request; block merge on new CodeQL alerts; let Copilot Autofix post AI-generated patches as PR suggestions (never auto-merge).

**One-paragraph:** GitHub Code Scanning + CodeQL gives every PR a SAST run; Copilot Autofix layers AI-generated patches on top for high-confidence alerts. This methodology produces a CodeQL workflow file plus branch-protection settings making the CodeQL check required; AI-suggested patches arrive as PR review comments a human accepts/edits/rejects but never auto-merges. Coverage extends to Bash, Dockerfile, Terraform/HCL, PHP via the AI-powered detections lane.

**Ефективно для:**

- GitHub-hosted repo з executable code (OSS — free; private — GHAS).
- Repo з HTTP / auth / deserialization / SQL / template-render surface.
- Polyglot repo, де shell / Docker / Terraform / PHP теж потребують SAST.
- Agent-driven feature work — agent читає SARIF через `gh api`.

## Applies If (ALL must hold)

- Repo hosted on GitHub.
- Repo has executable code (not docs / notebooks / asset-only).
- GitHub Advanced Security OR public OSS license (Code Scanning free for public OSS).
- Team accepts "block merge on new CodeQL alert" policy.

## Skip If (ANY kills it)

- Repo not hosted on GitHub — use Semgrep / SonarQube instead.
- Documentation-, asset-, or notebook-only repo with no executable surface.
- Throwaway experimental branches that will never merge.
- Mass-renaming refactor that legitimately churns thousands of lines (schedule one-shot baseline reset).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| GitHub workflow | .github/workflows/codeql.yml | platform |
| Branch protection | required check = codeql-analyze | platform |
| GHAS license OR OSS license | repo settings | platform |
| Language matrix | list of CodeQL-supported languages | maintainer |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[sec-secrets-defense-in-depth]] | Complementary secret-scan layer. |
| [[sec-trivy-pinned-supply-chain-scan]] | Complementary supply-chain layer. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-rule + rationale + source | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns (symptom/root-cause/fix) | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with decision gates | 500 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `workflow_draft` | haiku | Boilerplate YAML. |
| `branch_protection_set` | haiku | Mechanical. |
| `autofix_review_policy` | sonnet | Light judgement on accept/edit/reject. |

## Templates

| File | Purpose |
|------|---------|
| `templates/codeql-workflow.yml` | CodeQL Code Scanning workflow with matrix. |
| `templates/branch-protection.json` | Branch-protection settings making codeql-analyze a required check. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-sec-codeql-autofix-on-pr.py` | Validate workflow + branch-protection config against schema. | Pre-merge of workflow file |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[sec-secrets-defense-in-depth]]
- [[sec-trivy-pinned-supply-chain-scan]]
- [[mr-renovate-ai-handoff]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from observable signals (host == GitHub? GHAS or OSS? executable surface?) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether to enable the CodeQL gate — the tree terminates either on the active rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/codeql-workflow.yml`

```yaml
# Pin codeql-action by major and review release notes for any compromised tags before bumping.
name: CodeQL

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '17 3 * * 1'  # weekly baseline scan

permissions:
  contents: read
  security-events: write
  actions: read

jobs:
  analyze:
    name: Analyze (${{ matrix.language }})
    runs-on: ubuntu-latest
    timeout-minutes: 30
    strategy:
      fail-fast: false
      matrix:
        language: [javascript-typescript, python]
    steps:
      - uses: actions/checkout@v4
      - name: Init CodeQL
        uses: github/codeql-action/init@v3
        with:
          languages: ${{ matrix.language }}
          queries: security-and-quality
      - name: Autobuild
        uses: github/codeql-action/autobuild@v3
      - name: Analyze
        uses: github/codeql-action/analyze@v3
        with:
          category: '/language:${{ matrix.language }}'
```

### `templates/branch-protection.json`

```json
{
  "_usage": "gh api -X PUT repos/$OWNER/$REPO/branches/main/protection -H 'Accept: application/vnd.github+json' --input templates/branch-protection.json",
  "required_status_checks": {
    "strict": true,
    "contexts": [
      "CodeQL / Analyze (javascript-typescript)",
      "CodeQL / Analyze (python)"
    ]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": true,
    "required_approving_review_count": 1
  },
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false,
  "required_linear_history": true,
  "required_conversation_resolution": true
}
```
