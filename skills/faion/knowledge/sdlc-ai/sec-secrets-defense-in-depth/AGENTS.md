# Two-Layer Secret Scanning: Gitleaks + Verified TruffleHog

## Summary

**One-sentence:** Two-layer secret scanning — gitleaks pre-commit (regex, sub-second, blocks commit) + TruffleHog --results=verified in CI (provider-verified, treats live tokens as P0 incidents).

**One-paragraph:** Single-layer secret scanning either blocks too aggressively (developers disable it) or misses verified live tokens (regex false negatives). This methodology produces a two-layer config: gitleaks runs sub-second pre-commit on the developer or agent machine and blocks the commit before any secret enters local git history; TruffleHog runs in CI with `--results=verified` to actively call providers (AWS STS, GitHub, Stripe, Slack, OpenAI, Anthropic) confirming the token is live. Verified findings trigger immediate rotation + revert.

**Ефективно для:**

- Будь-який repo (single-dev або team) — leaked AWS/OpenAI key коштує більше за project.
- Repo, де AI agents коммітять від імені людей — verified scan відрізняє sk-ant-... від example в docstring.
- Monorepo з mixed languages (JWT/.pem/dotenv/tfvars) — pattern matchers пропускають.
- Migration з legacy git history — `detect-secrets` baseline + ratchet.

## Applies If (ALL must hold)

- Repo exists in any form (single-dev prototype counts — leaked key is the same cost).
- Repo has any code, config, or commit (not pure binary asset mirror).
- CI runner has outbound network egress (TruffleHog verification calls providers).
- Team accepts blocking commits on regex match + blocking PRs on verified findings.

## Skip If (ANY kills it)

- Air-gapped CI without network egress — substitute provider-specific offline format checks.
- Generated-code drops where every blob is regenerated from a private template store — scan the template store instead.
- Vendored read-only mirror with no commit pipeline.
- Pre-prod prototype where speed of iteration matters more than risk (rare; revisit weekly).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Pre-commit framework | pre-commit / lefthook / husky | lead |
| Gitleaks binary | installed locally + in CI | platform |
| TruffleHog action | aquasecurity-style GH action | platform |
| Outbound network | egress from CI | sec |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[lint-precommit-floor]] | The pre-commit framework that gitleaks lives in. |
| [[sec-codeql-autofix-on-pr]] | Complementary SAST layer. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-rule + rationale + source | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns (symptom/root-cause/fix) | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with decision gates | 500 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `precommit_wire` | haiku | Boilerplate hook config. |
| `ci_wire` | haiku | Boilerplate GitHub Actions. |
| `incident_response` | sonnet | Verified-finding triage requires judgement (rotate vs revert vs both). |

## Templates

| File | Purpose |
|------|---------|
| `templates/precommit-secrets.yaml` | pre-commit framework hooks section for gitleaks. |
| `templates/trufflehog-action.yml` | GitHub Actions workflow with --results=verified. |
| `templates/gitleaks.toml` | gitleaks config with org-specific allowlist. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-sec-secrets-defense-in-depth.py` | Validate produced two-layer config artefact. | Pre-merge of pre-commit + workflow |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[lint-precommit-floor]]
- [[sec-codeql-autofix-on-pr]]
- [[sec-trivy-pinned-supply-chain-scan]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from observable signals (CI egress available? pre-commit installed?) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure how many layers to ship — the tree terminates either on the active rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/precommit-secrets.yaml`

```yaml
# Pin every hook by tag and review release notes before bumps.
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.21.0
    hooks:
      - id: gitleaks
        name: gitleaks (staged-only secret scan)
        args: ['protect', '--staged', '--redact', '--config', '.gitleaks.toml']
```

### `templates/trufflehog-action.yml`

```yaml
name: Secrets Verify
on:
  pull_request:
    branches: [main]

permissions:
  contents: read
  pull-requests: read

jobs:
  trufflehog:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: TruffleHog (verified only)
        uses: trufflesecurity/trufflehog@main
        with:
          base: ${{ github.event.pull_request.base.sha }}
          head: ${{ github.event.pull_request.head.sha }}
          extra_args: --results=verified --fail
```

### `templates/gitleaks.toml`

```toml
# Keep allowlist tight; broad regexes mask real findings.
[extend]
useDefault = true

[allowlist]
description = "Test fixtures and documentation samples"
paths = [
  '''(?i)(^|/)tests?(/|$)''',
  '''(?i)(^|/)fixtures(/|$)''',
  '''(?i)(^|/)docs(/|$)''',
  '''(?i)\.example$''',
]
regexes = [
  # Known-invalidated demo tokens used in API docs
  '''sk-(test|demo)-[A-Za-z0-9]{20,}''',
  '''AKIAIOSFODNN7EXAMPLE''',
]

[[rules]]
id = "ai-provider-tokens"
description = "OpenAI, Anthropic, Google AI keys"
regex = '''(?i)\b(sk-(ant|proj|svcacct|test)-[A-Za-z0-9_-]{20,}|AIza[0-9A-Za-z_-]{30,})\b'''
tags = ["key", "ai"]
```
