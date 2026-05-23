---
slug: lint-staged-only-not-whole-tree
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Every linter / formatter wired into a pre-commit hook MUST receive ONLY the staged file set, not the whole repo tree — use lint-staged, lefthook glob filter, or pre-commit's built-in staged filter.
content_id: "2ee0fd98fd721db8"
complexity: light
produces: config
est_tokens: 2800
tags: [pre-commit, lint-staged, lefthook, hooks, staged-files]
---
# Pre-Commit Linters MUST Run on Staged Files Only

## Summary

**One-sentence:** Every linter / formatter wired into a pre-commit hook MUST receive ONLY the staged file set, not the whole repo tree — use lint-staged, lefthook glob filter, or pre-commit's built-in staged filter.

**One-paragraph:** Pre-Commit Linters MUST Run on Staged Files Only produces a config artefact for the sdlc-ai domain. It pins observable preconditions, scores candidate decisions against ≥5 testable rules, fails fast on disqualifiers, and emits a schema-validated output. The methodology routes between apply and skip-this-methodology via an explicit decision tree so downstream agents never run it on an unsuitable input.

**Ефективно для:**

- Repo with large tree where whole-tree lint takes 30+ seconds.
- Pre-commit run that blocks flow because it lints unchanged files.
- Polyglot repo where different languages need different linters per glob.
- Team migrating from heavy CI-only lint to fast pre-commit.

## Applies If (ALL must hold)

- Pre-commit framework already chosen (pre-commit, lefthook, husky).
- Repo size makes whole-tree lint > 5 s.
- Team accepts that whole-tree clean-up happens in CI scheduled job.
- Lint tools accept a list of paths as argument.

## Skip If (ANY kills it)

- Repo is tiny (whole-tree lint < 1 s).
- Lint tool can't accept path arguments (rare).
- Team wants whole-tree as a discipline floor — accept slowdown.
- Hook framework doesn't support staged filter (replace it).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Hook framework chosen | pre-commit/lefthook/husky+lint-staged | lead |
| Linter accepts paths | all linters in use | platform |
| Whole-tree CI job | scheduled or PR-CI | ci-eng |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[lint-precommit-floor]] | Upstream framework choice |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-rule + rationale + source | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns (symptom/root-cause/fix) | 700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `staged_filter_wire` | sonnet | Per-linter glob filter. |
| `ci_mirror` | haiku | Schedule whole-tree job. |

## Templates

| File | Purpose |
|------|---------|
| `templates/lefthook.yml` | Lefthook staged-files config. |
| `templates/package.json.fragment` | lint-staged config. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-staged-only-not-whole-tree.py` | Validate hook-config artefact. | pre-merge of hook config |

## Related

- [[lint-precommit-floor]]
- [[lint-ruff-and-biome-as-default]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (precondition flag, repo metric, capability flag) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on a rule that triggers the procedure or on `skip-this-methodology`.
