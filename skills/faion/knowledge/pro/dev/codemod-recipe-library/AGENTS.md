---
slug: codemod-recipe-library
tier: pro
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces tested codemod recipes (jscodeshift / ast-grep / libcst / Bowler) for the framework upgrade at hand, each with before/after fixtures and a CI smoke test.
content_id: "58d8548c6fe18775"
complexity: medium
produces: code
est_tokens: 4300
tags: [codemod, framework-upgrade, jscodeshift, ast-grep, libcst]
---
# Codemod Recipe Library

## Summary

**One-sentence:** Produces tested codemod recipes (jscodeshift / ast-grep / libcst / Bowler) for the framework upgrade at hand, each with before/after fixtures and a CI smoke test.

**One-paragraph:** Major framework upgrades (Angular X→X+1, React 17→18, Django 4→5, Rails 7→8) leak hundreds of mechanical edits into the diff. A codemod recipe library packages those edits as jscodeshift / ast-grep / Bowler / libcst transforms with paired before/after fixtures and a CI smoke test, replacing manual sed-and-pray rewrites.

**Ефективно для:**

- Major upgrade (React 17→18, Django 4→5) — hundreds of mechanical edits.
- jscodeshift / ast-grep / libcst — typed AST, не regex.
- Кожен recipe має before/after fixture + smoke test.
- PR разом із codemod source — ревьюер бачить трансформацію.

## Applies If (ALL must hold)

- Task is an instance of role-software-developer/Survive a Major Framework Upgrade OR adjacent.
- Operator has source repo + target framework version + upgrade notes.
- Output consumed by downstream PR cycle.
- Tier == pro or higher.

## Skip If (ANY kills it)

- Single-file upgrade where manual edit is faster than scripting.
- Already-merged upgrade — no codemod needed retroactively.
- Closed-source tool with no AST library.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Source repo (target file glob) | git path | team |
| Target framework upgrade notes | Markdown | framework docs |
| AST library for the language | tool | npm / pip |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[software-developer]] | Operating context for the upgrade task |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | ~900 |
| `content/04-procedure.xml` | essential | 5-step end-to-end procedure | ~800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `identify-mechanical-edits` | sonnet | Per-edit judgment from upgrade notes. |
| `author-codemod` | sonnet | Write the transform + before/after fixture. |
| `review-cross-recipe` | opus | Synthesis when recipes interact (one transform depends on another). |
| `validate-output` | haiku | Schema check via the validator script. |

## Templates

| File | Purpose |
|------|---------|
| `templates/codemod-recipe.md` | Markdown skeleton for one recipe with before/after. |
| `templates/codemod-recipes-index.json` | JSON skeleton matching the output contract. |
| `templates/smoke-test.sh` | Shell smoke test driver for every recipe. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-codemod-recipe-library.py` | Validate the output artefact against the schema in 02-output-contract.xml. | CI on each artefact change; pre-commit. |
| `scripts/validate-codemod-recipe-library.py` | Validator script. | after subagent returns, before downstream consumer reads |

## Related

- [[client-conventions-reverse-engineering]]
- [[mutation-testing-ci-gate]]

## Decision tree

See `content/06-decision-tree.xml`. Tree picks the AST tool by language + edit shape and gates recipes on fixture + smoke presence.
