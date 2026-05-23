---
slug: lint-shellcheck-hadolint-iac-floor
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Every repo with shell / Dockerfile / Compose / GH Actions / Kubernetes / Terraform / YAML MUST run a per-format IaC linter at the same hook tier as code linters — shellcheck, hadolint, yamllint, actionlint, tflint.
content_id: "ae357ecc943a92a0"
complexity: medium
produces: config
est_tokens: 3500
tags: [shellcheck, hadolint, iac, linting, infrastructure]
---
# Infrastructure-as-Code Lint Floor (shellcheck, hadolint, yamllint, actionlint, tflint)

## Summary

**One-sentence:** Every repo with shell / Dockerfile / Compose / GH Actions / Kubernetes / Terraform / YAML MUST run a per-format IaC linter at the same hook tier as code linters — shellcheck, hadolint, yamllint, actionlint, tflint.

**One-paragraph:** Infrastructure-as-Code Lint Floor (shellcheck, hadolint, yamllint, actionlint, tflint) produces a config artefact for the sdlc-ai domain. It pins observable preconditions, scores candidate decisions against ≥5 testable rules, fails fast on disqualifiers, and emits a schema-validated output. The methodology routes between apply and skip-this-methodology via an explicit decision tree so downstream agents never run it on an unsuitable input.

**Ефективно для:**

- Any repo with mixed bash + Dockerfile + YAML + Terraform.
- Production deploy where one bad bash quoting bites repeatedly.
- CI-heavy repo where a broken actionlint blows the next run.
- Compliance-driven team needing IaC governance evidence.

## Applies If (ALL must hold)

- Repo has any of: bash, Dockerfile, GH Actions, k8s manifests, Terraform.
- CI can run multiple linters in parallel.
- Pre-commit framework already in place.
- Team accepts adding the right linter per file type.

## Skip If (ANY kills it)

- Pure-Python / pure-Go repo with no IaC.
- Team has IaC validation via Terraform Cloud / Atlantis that overlaps.
- Bash scripts are trivial and never run in prod.
- Team won't fix shellcheck warnings — gate becomes noise.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Linter binaries | shellcheck / hadolint / yamllint / actionlint / tflint | dev-env |
| Pre-commit hook set | per-tool entries | platform |
| CI mirror | same checks in CI | ci-eng |
| Exclusions list | .shellcheckrc / .hadolint.yaml / .yamllint | lead |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[lint-precommit-floor]] | Hook framework hosts IaC linters |
| [[lint-megalinter-polyglot]] | MegaLinter alternative for ≥ 3 languages |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-rule + rationale + source | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns (symptom/root-cause/fix) | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with decision gates | 700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `linter_pick_per_format` | sonnet | Map file glob → linter. |
| `config_draft` | sonnet | Per-tool rc files. |
| `ci_wire_up` | haiku | Add per-linter CI step. |

## Templates

| File | Purpose |
|------|---------|
| `templates/.shellcheckrc` | ShellCheck config. |
| `templates/.hadolint.yaml` | Hadolint config. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-shellcheck-hadolint-iac-floor.py` | Validate the IaC-lint-config artefact. | pre-merge of IaC lint config |

## Related

- [[lint-precommit-floor]]
- [[lint-megalinter-polyglot]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (precondition flag, repo metric, capability flag) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on a rule that triggers the procedure or on `skip-this-methodology`.
