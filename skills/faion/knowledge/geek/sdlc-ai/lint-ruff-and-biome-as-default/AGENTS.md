---
slug: lint-ruff-and-biome-as-default
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: For new Python projects, ruff is the SOLE linter + formatter (replaces black/flake8/isort/pyupgrade/autoflake/pydocstyle). For JS/TS, biome is the SOLE formatter + linter where prettier+eslint is over-engineered.
content_id: "37188d9687132c77"
complexity: medium
produces: config
est_tokens: 3500
tags: [ruff, biome, linting, formatting, python]
---
# Ruff for Python and Biome for JS/TS as the Sole Linter+Formatter

## Summary

**One-sentence:** For new Python projects, ruff is the SOLE linter + formatter (replaces black/flake8/isort/pyupgrade/autoflake/pydocstyle). For JS/TS, biome is the SOLE formatter + linter where prettier+eslint is over-engineered.

**One-paragraph:** Ruff for Python and Biome for JS/TS as the Sole Linter+Formatter produces a config artefact for the sdlc-ai domain. It pins observable preconditions, scores candidate decisions against ≥5 testable rules, fails fast on disqualifiers, and emits a schema-validated output. The methodology routes between apply and skip-this-methodology via an explicit decision tree so downstream agents never run it on an unsuitable input.

**Ефективно для:**

- New Python project (no legacy black/flake8 baggage).
- Python repo migrating off the multi-tool chain.
- New JS/TS project where prettier+eslint is overkill.
- Pre-commit hook needs millisecond-fast lint to keep flow.

## Applies If (ALL must hold)

- Python ≥ 3.9 (ruff supports all current versions).
- JS/TS project where prettier+eslint isn't already entrenched.
- Team accepts a single tool decision per language.
- Custom rules limited (or expressible in ruff/biome).

## Skip If (ANY kills it)

- Legacy project with heavy eslint custom rules — migration cost.
- Project depends on a plugin not in ruff/biome (e.g. eslint-plugin-vue specifics).
- Team explicitly wants prettier formatting style different from biome.
- Tooling pinned by external mandate.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| pyproject.toml ruff section | committed config | py lead |
| biome.json | committed config | frontend lead |
| Pre-commit hook entries | ruff + biome hooks | platform |
| CI gate | `ruff check` + `biome ci` | ci-eng |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[lint-precommit-floor]] | Hook framework hosts ruff/biome |

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
| `rule_pick` | sonnet | Choose ruff rule selection per project. |
| `biome_config_draft` | sonnet | Biome config + ignore set. |
| `ci_wire_up` | haiku | Add CI steps. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pyproject.toml.fragment` | ruff section. |
| `templates/biome.json` | Biome config. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ruff-and-biome-as-default.py` | Validate the linter-config artefact. | pre-merge of lint config |

## Related

- [[lint-precommit-floor]]
- [[lint-staged-only-not-whole-tree]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (precondition flag, repo metric, capability flag) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on a rule that triggers the procedure or on `skip-this-methodology`.
