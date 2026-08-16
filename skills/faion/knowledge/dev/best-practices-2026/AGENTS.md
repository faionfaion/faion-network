# Software Development Best Practices 2026

## Summary

**One-sentence:** A 2026 snapshot of stable practices across AI-assisted coding, TS5, React 19/Next 15, Python 3.12/3.13, that becomes the project's `constitution.md` source.

**One-paragraph:** Produces a versioned snapshot of current-stable best practices for the dominant 2026 stack (AI-assisted coding with Copilot/Cursor/Claude Code, TypeScript 5 strict, React 19 + Next 15, Python 3.12-3.13, AI testing) extracted into a project-local `constitution.md` so downstream agents cite a stable, project-specific contract — not this drifting reference.

**Ефективно для:** старту нового проєкту, аудиту чинного за зваженою рубрикою, або щоквартального оновлення `constitution.md`.

## Applies If (ALL must hold)

- Project is on a 2026 stable stack (TS5, React 19+/Next 15+, Python 3.12+) OR is being migrated to it.
- Team uses AI coding assistants (Copilot, Cursor, Claude Code) in daily work.
- A `constitution.md` (or ADR home) exists in the repo to receive the extracted clauses.

## Skip If (ANY kills it)

- Legacy stack pinned to older versions (Python 3.9, React 17, TS 4.x) — load the legacy-specific methodology instead.
- One-off scripts / notebooks — no constitution.md needed.
- Project already maintains a more domain-specific best-practices doc with stricter rules.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Repo's `constitution.md` (empty or partial) | Markdown | repo root or `.aidocs/` |
| Stack versions in package.json / pyproject.toml | JSON/TOML | repo root |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `free/dev/python-developer/python-typing` | Python typing baseline this snapshot enforces. |
| `solo/sdd/sdd/sdd-document-templates` | Constitution template surface. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 13 rules: AI tool matching, prompt structure, no auto-accept on auth/data, TS strict flags, React 19 patterns, Python 3.12+ baseline, ruff + mypy --strict, uv lockfile, pre-commit gate, `.aidocs/` scaffold, AI testing baseline, snapshot+drift cadence, applicability skip gate | ~1900 |
| `content/02-output-contract.xml` | essential | Schema for the constitution snapshot record (stack versions, rule citations, drift-scan date) | ~700 |
| `content/03-failure-modes.xml` | essential | 9 antipatterns: auto-accept on auth, single-tool monomania, stale snapshot, unstructured prompts, partial TS strict adoption, AI tests as oracle, raw pip in CI, no pre-commit, `strict: false` from an old template | ~1200 |
| `content/04-procedure.xml` | essential | 5-step audit: detect stack → score each rule → prioritise by weight x blast radius → one fix per PR → extract and lock the baseline | ~900 |
| `content/06-decision-tree.xml` | essential | When to extract vs cite vs deprecate a rule, plus the skip-the-methodology leaf | ~350 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Extract rules into `constitution.md` | sonnet | Mechanical extraction with templated output. |
| Drift scan vs current ecosystem | opus | Judgement: which rules aged, which are still current. |
| Wire AI-assisted-coding policy | opus | Security / policy judgement. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tsconfig-strict.json` | TypeScript 5 strict tsconfig with all recommended flags. |
| `templates/bp2026-drift.sh` | Drift scanner: compares pinned stack versions in repo vs the 2026 baseline; prints a delta. |
| `templates/rubric.json` | Weighted baseline rubric — one item per gating rule, with weight and acceptance criterion. |
| `templates/audit-report.md.j2` | Audit report skeleton: per-rule PASS/WARN/FAIL with evidence, remediation order, extraction record. |
| `templates/audit-report.md` | Audit report skeleton: per-rule PASS/WARN/FAIL with evidence, remediation order, extraction record. Generated from `templates/audit-report.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-best-practices-2026.py` | Validates the constitution-snapshot record schema. | After extraction; quarterly. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[python-typing]] — Python typing baseline.
- [[code-review]] — review pattern that enforces these rules at PR time.
- [[code-coverage]] — coverage gate that pairs with this.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` decides for each candidate rule whether to extract it into `constitution.md` (project-specific contract), cite it inline (keep this file as a reference), or deprecate it (aged out of current stack). A skip leaf (`r13-skip-gate`) is always reachable: non-TS/Python stacks, sub-100-LOC repos and frozen legacy trees exit here.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/tsconfig-strict.json`

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noImplicitOverride": true,
    "target": "ES2023",
    "lib": [
      "ES2023",
      "DOM",
      "DOM.Iterable"
    ],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "verbatimModuleSyntax": true,
    "isolatedModules": true,
    "allowImportingTsExtensions": true,
    "resolvePackageJsonExports": true,
    "resolvePackageJsonImports": true,
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,
    "skipLibCheck": true
  }
}
```

### `templates/bp2026-drift.sh`

```bash
set -euo pipefail
root="${1:-.}"
fail=0
note() { echo "- $*"; fail=1; }
if [ -f "$root/tsconfig.json" ]; then
  for k in '"strict": true' '"noUncheckedIndexedAccess": true' '"verbatimModuleSyntax": true'; do
    grep -q "$k" "$root/tsconfig.json" || note "tsconfig missing: $k"
  done
fi
if [ -f "$root/package.json" ]; then
  node -e '
    const p=require(process.argv[1]);
    const dep={...(p.dependencies||{}),...(p.devDependencies||{})};
    const want={typescript:"^5",react:"^19",next:"^15"};
    for (const [k,v] of Object.entries(want)) {
      if (k in dep && !new RegExp(v).test(dep[k]))
        console.log("- "+k+" pinned at "+dep[k]+", want "+v);
    }
  ' "$root/package.json"
fi
if [ -f "$root/pyproject.toml" ]; then
  grep -E 'python = "\\^?3\\.(12|13)' "$root/pyproject.toml" >/dev/null || note "Python <3.12"
  grep -q "ruff" "$root/pyproject.toml" || note "ruff not configured"
fi
exit $fail
```

### `templates/rubric.json`

Weighted rubric, one item per gating rule; see the file for the full body. Item ids are the rule ids
of `content/01-core-rules.xml` (`r4-ts-strict-flags`, `r9-ruff-mypy-strict`, `r10-uv-lockfile`,
`r11-pre-commit-gate`, `r12-aidocs-scaffold`, …), each with `weight` (1-5) and a `check` string.

### `templates/audit-report.md.j2`

```jinja
<!--

purpose: Markdown audit report skeleton — per-rule PASS/WARN/FAIL with evidence and remediation
consumes: scored rubric from templates/rubric.json
produces: report
depends-on: content/04-procedure.xml
token-budget-impact: ~260 tokens when loaded as context
-->


# 2026 Best-Practices Audit — {{ repo_name }}

Generated {{ date }}; baseline rubric version 2026.1; snapshot version {{ snapshot_version }}.

| Rule | Status | Weight | Evidence | Remediation |
|------|--------|--------|----------|-------------|
| r4-ts-strict-flags | PASS | 3 | tsconfig.json:12 | — |
| r5-react-19-patterns | WARN | 2 | 3 of 7 server components | wrap remaining fetches in Suspense |
| r9-ruff-mypy-strict | FAIL | 3 | mypy --strict emits 18 errors | fix, or add per-module ignores with an owner |

## Remediation order

Ordered by weight x blast radius; strictness flips first.

1. ...

## Constitution extraction

Rules extracted into `constitution.md` this pass: {{ extracted_rules }}. Next drift scan due: {{ next_scan_due }}.
```
