---
slug: ai-generated-code-lint-presets
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "196be164c9feed19"
summary: A packaged set of ruff and ESLint lint presets that catch the dominant AI-code smells — unused imports, fabricated APIs, no-op tests, broad excepts, console-log left over from prototyping — so the daily PR review pass enforces them automatically.
tags: [lint, ruff, eslint, ai-codegen, presets, code-quality]
---
# AI-Generated Code Lint Presets

## Summary

**One-sentence:** A packaged set of ruff (Python) and ESLint (TS / JS) presets tuned for the dominant AI-code smells — unused imports, fabricated APIs, no-op tests, broad excepts, leftover console.log / debugger, magic literals, missing returns — so the daily PR review pass catches them without manual scanning.

**One-paragraph:** AI coding assistants emit a recognizable smell signature: imports that the model "thinks" exist; `try: ... except: pass` that hides errors; tests with `assert True` or `assert response` without checking properties; commented-out blocks left behind; magic literals where constants are required; default `console.log` / `print` debug statements never removed. This methodology ships two ready-to-use lint preset files — `ruff-ai-presets.toml` and `eslint-ai-presets.json` — that turn these smells into hard errors. The developer drops them into the project, runs them as a pre-commit hook, and the typical PR review pass cleans up 80% of AI smell before a human looks. Output: zero-friction lint that the AI itself can self-correct against on the next iteration.

## Applies If (ALL must hold)

- Repository contains code authored or substantially edited by an AI assistant.
- The repo uses ruff (Python) or ESLint (TypeScript / JavaScript) — or can adopt them.
- A pre-commit framework is installed (see `lint-precommit-floor`).
- Daily PR review pass is the active workflow (see `Daily PR review pass (own + teammates)`).

## Skip If (ANY kills it)

- Project uses a non-supported language (Go, Rust, Swift) — separate presets needed.
- Project has heavy legacy code that would fail the presets — adopt with `--add-noqa` first, fix incrementally.
- Lint discipline is already strict and AI smell is absent — overhead exceeds the win.
- Pre-commit is disabled — fix `lint-precommit-floor` first.

## Prerequisites

- ruff installed at &gt;= 0.6 (Python projects) OR ESLint installed at &gt;= 9 (TS / JS projects).
- A `.pre-commit-config.yaml` or `husky` configured.
- Branch hygiene allowing one PR per logical lint adoption.
- A baseline lint run to identify the noqa floor for the existing code.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/sdlc-ai/lint-precommit-floor` | Pre-commit must already be wired before these presets attach to it. |
| `geek/sdlc-ai/lint-ruff-and-biome-as-default` | Sibling: this methodology specialises ruff for AI-code smell. |
| `pro/dev/software-developer/code-quality` | Background on code-quality discipline. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: presets immutable, no-op-test rule, broad-except rule, magic-literal rule, debug-statement rule | ~1100 |
| `content/02-output-contract.xml` | essential | Lint report shape, baseline-noqa rule, exemption discipline | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: AI auto-noqa, preset drift, false positives, etc. | ~1000 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `lint-run-and-parse` | haiku | Mechanical: run lint, parse JSON output |
| `noqa-floor-suggest` | haiku | Mechanical: tag pre-existing violations with explicit noqa |
| `pr-comment-from-findings` | sonnet | Structured comment composition with rationale |
| `preset-tune-suggest` | sonnet | Bounded judgement on per-project tuning |

## Templates

| File | Purpose |
|------|---------|
| `templates/ruff-ai-presets.toml` | Ruff ruleset tuned for AI-code smells |
| `templates/eslint-ai-presets.json` | ESLint ruleset tuned for AI-code smells |
| `templates/pr-comment.md` | PR comment template structured per smell |

## Scripts

| System | Purpose | When to call |
|------|---------|--------------|
| `scripts/adopt.sh` | Copy presets in, add `--add-noqa` for existing violations, commit | First-time adoption |
| `scripts/lint-summary.py` | Run lint, count smells per category, emit summary | Pre-PR |

## Related

- parent skill: `pro/dev/software-developer/`
- peer methodologies: `code-quality`, `lint-precommit-floor`, `lint-ruff-and-biome-as-default`
- external: [Ruff docs](https://docs.astral.sh/ruff/) · [ESLint typescript-eslint](https://typescript-eslint.io/) · [Astral T20 (no print)](https://docs.astral.sh/ruff/rules/print/)
