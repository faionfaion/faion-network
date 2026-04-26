# CLAUDE.md / AGENTS.md Documentation

## Summary

Convention for writing AI-readable directory context files: `CLAUDE.md` (single line: `@AGENTS.md`) and `AGENTS.md` (20-80 lines covering purpose, file table, key types, commands, gotchas). Required in every directory with source code — not just repo roots but also subpackages, module folders, test dirs.

## Why

Without per-directory context, agents load the whole repo tree or hallucinate structure. The `CLAUDE.md = @AGENTS.md` pattern bridges Claude Code with other tools (Cursor, Cline, Codex). Capping AGENTS.md at 80 lines enforces routing-first: agents narrow the search per level, never bulk-load. The "Gotchas" section is the highest-value content — it corrects training-data assumptions unique to this specific codebase.

## When To Use

- Creating a new directory with code: add `CLAUDE.md` + `AGENTS.md` before any other file.
- Onboarding an agent to an unfamiliar module — agent reads AGENTS.md to route, then loads specific files.
- After a significant refactor: regenerate AGENTS.md so future context loads stay accurate.
- Multi-agent workspaces where each tool reads a different filename.
- Repos with many sub-packages where loading the whole tree blows context budget.

## When NOT To Use

- Tiny one-file scripts — a README is sufficient.
- Generated / vendored code (`node_modules/`, `dist/`) — never document these.
- Highly volatile prototypes where structure changes daily — document after dust settles.
- Directories that are pure data (assets, fixtures) without logic.

## Content

| File | What's inside |
|------|---------------|
| `content/01-convention.xml` | CLAUDE.md one-liner rule, AGENTS.md strict shape, line-cap enforcement, gotchas section requirement. |
| `content/02-templates-by-type.xml` | Backend, frontend, infra, library AGENTS.md templates with required sections per type. |
| `content/03-antipatterns.xml` | Over-documentation, hallucinated commands, missing gotchas, drift from source, secrets in docs. |

## Templates

| File | Purpose |
|------|---------|
| `templates/AGENTS-universal.md` | Universal AGENTS.md template with all required sections. |
| `templates/audit-agents-md.sh` | Drift detector: flags dirs where source files are newer than AGENTS.md by more than 14 days. |
