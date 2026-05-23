---
slug: lint-megalinter-polyglot
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: For polyglot repos (≥3 languages), wire MegaLinter as one CI job that runs the right per-language linters with SARIF output instead of N hand-rolled jobs.
content_id: "9ed9f393ac539279"
complexity: medium
produces: config
est_tokens: 3500
tags: [lint, megalinter, ci, polyglot, sarif]
---
# MegaLinter as the Polyglot Quality Umbrella in CI

## Summary

**One-sentence:** For polyglot repos (≥3 languages), wire MegaLinter as one CI job that runs the right per-language linters with SARIF output instead of N hand-rolled jobs.

**One-paragraph:** MegaLinter as the Polyglot Quality Umbrella in CI produces a config artefact for the sdlc-ai domain. It pins observable preconditions, scores candidate decisions against ≥5 testable rules, fails fast on disqualifiers, and emits a schema-validated output. The methodology routes between apply and skip-this-methodology via an explicit decision tree so downstream agents never run it on an unsuitable input.

**Ефективно для:**

- Repo with ≥ 3 languages (Python + JS + Go + YAML + Docker etc).
- CI maintenance burden: 6+ linter jobs that drift.
- Need SARIF output for GitHub code-scanning.
- Want a single place to declare per-language exclusions.

## Applies If (ALL must hold)

- Repo has ≥ 3 file types needing lint coverage.
- CI can mount the MegaLinter Docker image.
- Team accepts MegaLinter's curated linter set per language.
- GitHub Advanced Security (or equivalent SARIF consumer) available.

## Skip If (ANY kills it)

- Single-language repo — direct linter is simpler.
- Air-gapped CI — MegaLinter image pull blocked.
- Custom linter pipeline already tuned and trusted.
- Repo too small to justify the image-pull overhead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| .mega-linter.yml | committed MegaLinter config | platform |
| CI job | GH Actions / GitLab CI / Azure step | ci-eng |
| SARIF upload step | code-scanning / artifact upload | ci-eng |
| Per-language exclusions | documented list | lang owners |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[lint-precommit-floor]] | Local hooks are the per-language local floor |
| [[lint-staged-only-not-whole-tree]] | Local discipline complements full-tree CI |

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
| `config_draft` | sonnet | Pick which flavours / disable list. |
| `ci_workflow_draft` | haiku | Wire MegaLinter step. |
| `sarif_consumer_wire` | sonnet | Upload + dashboard hookup. |

## Templates

| File | Purpose |
|------|---------|
| `templates/.mega-linter.yml` | Committed MegaLinter config. |
| `templates/megalinter-workflow.yml` | GH Actions job. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-megalinter-polyglot.py` | Validate the MegaLinter config artefact. | pre-merge of lint config |

## Related

- [[lint-precommit-floor]]
- [[lint-shellcheck-hadolint-iac-floor]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (precondition flag, repo metric, capability flag) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on a rule that triggers the procedure or on `skip-this-methodology`.
