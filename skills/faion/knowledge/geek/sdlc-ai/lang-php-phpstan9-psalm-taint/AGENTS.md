---
slug: lang-php-phpstan9-psalm-taint
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Run PHPStan at level 9 and Psalm with --taint-analysis on every PHP repo where AI agents author code — PHPStan for type strictness, Psalm for inter-procedural taint (SQLi, XSS, command injection).
content_id: "23531c17f120c1fe"
complexity: medium
produces: config
est_tokens: 3700
tags: [php, phpstan, psalm, static-analysis, taint]
---
# PHP Dual Gate: PHPStan Level 9 + Psalm Taint Analysis

## Summary

**One-sentence:** Run PHPStan at level 9 and Psalm with --taint-analysis on every PHP repo where AI agents author code — PHPStan for type strictness, Psalm for inter-procedural taint (SQLi, XSS, command injection).

**One-paragraph:** PHP Dual Gate: PHPStan Level 9 + Psalm Taint Analysis produces a config artefact for the sdlc-ai domain. It pins observable preconditions, scores candidate decisions against ≥5 testable rules, fails fast on disqualifiers, and emits a schema-validated output. The methodology routes between apply and skip-this-methodology via an explicit decision tree so downstream agents never run it on an unsuitable input.

**Ефективно для:**

- PHP repo where AI agents write code that touches user input.
- Legacy PHP gradually adopting strict typing.
- Library publisher that needs level-10 for downstream confidence.
- Security-sensitive PHP (auth, payments, admin) that must catch taint at CI.

## Applies If (ALL must hold)

- PHP 8.1+ runtime.
- Composer + autoloader available.
- CI can run two extra checks (PHPStan + Psalm).
- Team accepts adding type annotations to reach level 9 / 10.

## Skip If (ANY kills it)

- PHP < 7.4 — analyzer support poor.
- Codebase relies on magic methods / dynamic properties — false-positive flood.
- Throwaway prototype — gate cost exceeds value.
- Both tools already in use — verify config matches this methodology before duplicating.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| phpstan.neon | committed PHPStan config | lead |
| psalm.xml | committed Psalm config | lead |
| CI matrix | two stages in CI | ci-eng |
| Baseline files | phpstan-baseline.neon for existing violations | lead |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[lint-precommit-floor]] | Hooks can run analyzers locally |
| [[sec-codeql-autofix-on-pr]] | Sibling SAST gate |

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
| `config_draft` | sonnet | Pick level + baseline strategy. |
| `baseline_generation` | haiku | Run analyzers and snapshot baselines. |
| `ci_wire_up` | sonnet | Add the two CI jobs. |

## Templates

| File | Purpose |
|------|---------|
| `templates/phpstan.neon` | PHPStan level 9 config. |
| `templates/psalm.xml` | Psalm taint-analysis config. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-lang-php-phpstan9-psalm-taint.py` | Validate the analyzer-config artefact. | pre-merge of analyzer config |

## Related

- [[lint-precommit-floor]]
- [[sec-codeql-autofix-on-pr]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (precondition flag, repo metric, capability flag) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on a rule that triggers the procedure or on `skip-this-methodology`.
