# Code Quality Trends

## Summary

**One-sentence:** Audits a stack against current best-practice quality standards (lint, type-safety, tests, perf budgets, security) and emits a per-gap remediation report.

**One-paragraph:** Code-quality 'best practices' drift faster than most repos update — strict mode flags rotate, type-only imports become standard, perf budgets get tighter. This methodology runs a quarterly audit per stack (TypeScript / Python / React), emits a report listing each gap (current vs. recommended), and ships ready-to-paste config diffs. The cadence is the point: a stale audit is worse than none — it gives false confidence. Mechanism: typed audit driver → detector per category → per-gap diff. Source list updates with each refresh.

**Ефективно для:**

- Квартальний health-check на legacy-репо: 'що в нас застаріло за квартал'.
- Onboarding для нового tech-lead: дає 'state of the art' baseline за один прогон.
- AI-агенти можуть автоматично PR-ити config-diff без участі рев'юера тривіальних апгрейдів.
- Team з нульовою time для standards-update: автопаці rule-set дрейф у фоновому режимі.

## Applies If (ALL must hold)

- Stack is one of: TypeScript, Python, React, or a clear combination.
- Repo has existing lint + test infra (audit is incremental, not green-field).
- Owner has authority to merge config-level changes (not blocked by enterprise sign-off).

## Skip If (ANY kills it)

- Repo is end-of-life — no future value in modernising.
- Standards locked by an external compliance regime (ISO 25010 etc).
- Audit was run within last 60 days — refresh is overkill.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Stack detection | JSON | package.json / pyproject.toml inspection |
| Current lint config | JSON / YAML | repo root |
| Type-checker config | tsconfig.json / mypy.ini | repo root |
| Perf budget (if any) | lighthouse-budget.json | repo or 'none' |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | Standalone — no upstream artefacts required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: refresh-quarterly, typed-strict-mode, diff-not-overwrite, perf-budget-required, security-baseline | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for audit report | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns: stale-audit, copy-paste-config, flag-cargo-cult | 700 |
| `content/04-procedure.xml` | essential | 5-step audit procedure | 700 |
| `content/05-examples.xml` | reference | Worked TypeScript audit | 500 |
| `content/06-decision-tree.xml` | essential | Stack → category → strict-or-relaxed tree | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `detect_stack` | haiku | File-pattern detection — deterministic. |
| `run_category_detectors` | haiku | Per-category check; mostly deterministic. |
| `draft_remediation` | sonnet | Per-gap diff generation; needs context. |
| `synthesise_report` | sonnet | Cross-category report drafting. |

## Templates

| File | Purpose |
|------|---------|
| `templates/audit-prompt.txt` | LLM prompt to drive the per-category audit |
| `templates/detect-stack.sh` | Shell script for stack detection |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-code-quality-trends.py` | Validate an audit report against schema | After draft, before circulating |

## Related

- - [[code-review-process]] — the audit becomes input for review-standard updates.
- - [[refactoring-patterns]] — gaps that need code changes route here.

## Decision tree

See `content/06-decision-tree.xml`. The tree branches on detected stack → per-category lookup (lint / types / tests / perf / sec). Strict-mode default unless legacy escape-hatch is named in the manifest.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/audit-prompt.txt`

```text
Audit this repo against the 2026 Code Quality Checklist for stack={{STACK}}.

Output a JSON array of objects. Each object:
{
  "item": "<checklist item text>",
  "status": "pass | fail | na",
  "evidence": "<file:line or command output that proves status>",
  "fix_command": "<shell command to fix, or null if manual>"
}

Rules:
- Cap output at 30 items; pick the highest-leverage from the matched stack checklist.
- Do not invent configs that do not exist; mark missing tools as "fail" and propose installation.
- Do not cite benchmarks or statistics from memory; use only the attached checklist.
- Mark "na" for items that do not apply to this stack.
- Every "fail" must have a non-null fix_command or a clear manual instruction.
- Use only the attached 2026 Code Quality Checklist as source of truth.
```

### `templates/detect-stack.sh`

```bash
#!/usr/bin/env bash
# detect-stack.sh — coarse stack classifier for the audit agent.
# Reads manifest files and emits lang/framework/version tags.
# Usage: detect-stack.sh [directory]
set -euo pipefail

ROOT="${1:-.}"
cd "$ROOT"

[ -f tsconfig.json ] && echo "lang:ts" || { [ -f package.json ] && echo "lang:js"; }
{ [ -f pyproject.toml ] || [ -f requirements.txt ] || [ -f setup.py ]; } && echo "lang:py"
[ -f go.mod ] && echo "lang:go"
[ -f Cargo.toml ] && echo "lang:rust"

[ -f next.config.js ] || [ -f next.config.mjs ] && echo "fw:next"
[ -f remix.config.js ] && echo "fw:remix"
[ -f svelte.config.js ] && echo "fw:svelte"
[ -f manage.py ] && echo "fw:django"
[ -f main.go ] && grep -q "gin" go.mod 2>/dev/null && echo "fw:gin"

[ -f package.json ] && grep -q '"react"' package.json 2>/dev/null && echo "lib:react"
[ -f package.json ] && grep -q '"vue"' package.json 2>/dev/null && echo "lib:vue"

[ -f pyproject.toml ] && grep -m1 'requires-python' pyproject.toml | sed 's/.*= */python:/'
[ -f package.json ] && jq -r '.engines.node // empty' package.json 2>/dev/null | sed 's/^/node:/'
```
