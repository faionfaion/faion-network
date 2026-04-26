# PHP Dual Gate: PHPStan Level 9 + Psalm Taint Analysis

## Summary

Run two static analyzers in CI for every PHP project where AI agents author code: PHPStan at level 9 (or 10 for libraries) for type strictness, and Psalm with `--taint-analysis` for inter-procedural data-flow checks (SQLi, XSS, command injection). Both must report green before merge. PHPStan level 9 forbids `mixed` types — exactly the type LLMs love to emit — and Psalm uniquely tracks tainted user input across method boundaries, catching injection patterns PHPStan does not model.

## Why

PHPStan and Psalm are complementary, not redundant: PHPStan is a strict type system, Psalm is a dataflow / taint engine. As of PHPStan 2.1.34 (early 2026), level 9 reflection-cache analysis is 25-40% faster, making the gate affordable on every PR. The combined floor encodes the "deploy LLM only where these two tools are silent" pattern referenced in 2026 PHP+AI literature: any LLM-suggested code that introduces `mixed`, untyped properties, or untracked-input → SQL/exec sinks fails before review. The result: agents produce smaller, more correct diffs because their iteration loop terminates only when both tools accept the change.

## When To Use

- Symfony, Laravel, Drupal, or vanilla PHP services with agent contributors.
- Projects with web-facing controllers, ORM query builders, file uploads, shell command construction.
- Codebases ratcheting up type strictness (start L5, increment per release; pin L9 once green).
- Library packages targeting Packagist — level 10 is feasible because there is no framework noise.

## When NOT To Use

- Greenfield prototypes under ~1 KLOC where the bootstrap cost dominates value.
- Pure CLI scripts with no external input — Psalm's taint pass produces no signal.
- Legacy codebases where setting L9 day one would mark thousands of files as failing — phase from L5 → L7 → L9 with the baseline file.

## Content

| File | What's inside |
|------|---------------|
| `content/01-phpstan-level9.xml` | Level 9 rule, baseline strategy, `mixed` ban, CI invocation. |
| `content/02-psalm-taint.xml` | Taint analysis rule, source/sink declarations, suppression discipline. |

## Templates

| File | Purpose |
|------|---------|
| `templates/phpstan.neon` | Level 9 config with parallel runner and reflection cache enabled. |
| `templates/psalm.xml` | Psalm config with `--taint-analysis` defaults and standard plugin set. |
