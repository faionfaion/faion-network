# Linting and Pre-Commit Rules

Every project MUST have pre-commit hooks. If a hook fails, fix the issue — never skip with `--no-verify`.

## This repo's own hooks

Installed by `scripts/install-hooks.sh`, which points `core.hooksPath` at the tracked `.githooks/`. It is idempotent and runs automatically from `init.sh`, `scripts/check-validators.sh` and `scripts/f066-validate-all.sh`, so a fresh clone is hooked the first time any of them is used. To install by hand:

```bash
./scripts/install-hooks.sh
```

`commit-msg` enforces the repo rule: `type: short description`, 50-character title, no trailing period, no `Co-Authored-By`, no emojis. Merge, revert and fixup titles are exempt.

`pre-commit` runs three gates:

| Gate | Cost | Scope |
|------|------|-------|
| `## [Unreleased]` CHANGELOG entry | instant | Diffs that **section** against HEAD — touching a released section does not satisfy the rule |
| `AGENTS.md` 20-80 line budget | instant | Staged files only; methodology and playbook envelopes exempt (their shape is the corpus spec, not the docs convention) |
| Corpus validators | ~15 s | Nine whole-corpus validators, plus `validate-methodology-v2.py` scoped to the slugs the commit touched |

### Why that validator split

`scripts/f066-validate-all.sh` takes about four minutes, and ~205 s of that is validator 3 alone: it spawns one python per slug across 2,639 slugs. The other nine sweep the whole corpus in ~6 s of CPU between them, so they run in full on every commit and validator 3 runs only against the touched slugs. The full sweep is manual, before a release:

```bash
scripts/check-validators.sh --check-all      # fast set + the full v2 sweep, diffed vs baseline
scripts/check-validators.sh --write-baseline # after fixing corpus content
```

`validate-playbook-v3.py` runs in neither. It fails **455/455** because the validator demands YAML frontmatter no playbook `AGENTS.md` has ever carried — that is a broken validator, not broken content, and a gate that is always red trains people to ignore gates.

### The baseline, not the count

The corpus carries known, pre-existing failures (9 decision-tree, 6 methodology-v2, 2 templates). The hook gates on the failure **set** in `scripts/validator-baseline.txt`, normalised to `<validator-id>\t<repo-relative-path>`. A line present now and absent from the baseline blocks; a baseline line that no longer reproduces is reported as a fix and never blocks, so repairing content does not also require curating a file to land. Gating on counts instead would wave through a swap — one failure fixed, one introduced.

Not covered, and still manual: `skills/tier-manifest.json` is generated, and nothing checks that a staged `meta.json` change was followed by `python3 scripts/regen-tier-manifest.py`.

## Per-project setup

The table below describes the application projects agents work on from here.

| Project | Tool | Pre-commit | What it checks |
|---------|------|------------|----------------|
| **backend** | ruff | `.pre-commit-config.yaml` | Format, lint (E/W/F/I/B/C4/UP/SIM/DJ/T20), debug statements |
| **dag** | ruff | `.pre-commit-config.yaml` | Same as backend |
| **frontend** | ESLint + Prettier | `.husky/pre-commit` | Format, Angular lint, selector prefix |
| **ddl-builder** | ESLint + Prettier + TS | `.husky/pre-commit` | Format, typecheck, RELEASE_NOTES.md |

## Agent rules

1. **When a hook fails** — read the error, fix the root cause, commit again. Never `--no-verify`.
2. **When adding Python code** — run `ruff check --fix` before committing. No `print()` in production code (T20).
3. **When adding TypeScript code** — run `npm run typecheck`. No `any` types.
4. **When finding a new bug pattern** — consider adding a ruff / ESLint rule for it, and document it in that project's `AGENTS.md`.
5. **DDL Builder** — always update `RELEASE_NOTES.md` with every commit.

## ruff quick reference

```bash
ruff check .              # Lint
ruff check . --fix        # Lint + auto-fix
ruff format .             # Format (replaces black)
ruff check . --select T20 # Find print() statements
```

Key rule groups: `E` errors, `F` pyflakes, `I` isort, `B` bugbear, `T20` no-print, `DJ` django, `UP` pyupgrade.
