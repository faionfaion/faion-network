# Linting and Pre-Commit Rules

Every project MUST have pre-commit hooks. If a hook fails, fix the issue — never skip with `--no-verify`.

Note: this repo (`faion-network`) is content, not application code, and installs no git hook of its own. The table below describes the application projects agents work on from here.

## Per-project setup

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
