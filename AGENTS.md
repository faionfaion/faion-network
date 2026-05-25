# faion-network

**Methodology base for the CLI.** The repo is the source of truth for everything the `faion` CLI ships at runtime: skills, methodologies, playbooks, workflows, and the `tier-manifest.json` that gates them.

| Item | Value |
|------|-------|
| Repo | `faionfaion/faion-network` |
| Content | 54 skills, 1300+ methodologies, 120 playbooks, 5 workflows, `tier-manifest.json` |
| Tiers | free / solo / pro / geek (cumulative; manifest is the authoritative path-to-tier map) |
| Distribution | Read by `faion-cli` at runtime; read by `faion-net-be` on disk via `KNOWLEDGE_ROOT` + `TIER_MANIFEST_PATH` settings; **not** bundled into the public `faion` plugin |
| Symlink | `~/workspace/.claude → projects/faion-net/faion-network` so Claude Code loads skills from here directly |

**Ecosystem map:** see `../AGENTS.md` for the full 5-repo stack and runtime data flow.

## Adapters

This repo is packaged for Claude Code and Codex. Shared project rules live below; runtime-specific Faion behavior lives in adapter files:

| Runtime | Adapter |
|---------|---------|
| Claude Code | `skills/faion/adapters/claude-code.md` and `skills/faion/workflows/adapters/claude-code.md` |
| Codex | `skills/faion/adapters/codex.md` and `skills/faion/workflows/adapters/codex.md` |

Claude Code-specific metadata (`CLAUDE.md`, `allowed-tools`, hooks) is kept for Claude compatibility. Codex should ignore it unless the Codex adapter says otherwise.

## Git Commits

- 50 chars title, optional body
- NO "Co-Authored-By: Claude"
- NO emojis
- Format: `type: short description`
- **CHANGELOG.md required** — pre-commit hook blocks without it. Add entry under `## [Unreleased]`

## Language

- **User:** Ukrainian
- **Docs/code:** English (saves ~30% tokens)
- **Subagent prompts:** English

## Documentation

**NO ASCII ART.** Allowed: tables, lists, arrows (`→`), directory trees.

## Documentation Convention

Every directory uses this pattern for multi-agent compatibility:

```
any-dir/
├── CLAUDE.md       # Always: @AGENTS.md (Claude Code entrypoint)
├── AGENTS.md       # Essential context for THIS dir (20-80 lines, auto-loaded)
├── .agents/        # Detailed reference docs (on-demand)
│   └── INDEX.md    # Full index of .agents/ contents
└── .aidocs/        # SDD lifecycle docs (project roots only)
    └── INDEX.md    # Full index of .aidocs/ contents
```

- `CLAUDE.md` = always `@AGENTS.md`, nothing else
- `AGENTS.md` = what this dir IS + commands + gotchas. Mentions `.agents/INDEX.md` path
- `.agents/` = architecture, API refs, decisions, deep dives
- `.product/` = per-project SDD + product docs (specs, designs, plans, roadmap)
- `.aidocs/` = workspace-level SDD (multi-repo projects like NERO)

**Per-module coverage:** `CLAUDE.md` + `AGENTS.md` required in every directory that contains source code — not just repo roots, but also subpackages, module folders, test dirs. When creating or modifying a directory, always ensure the pair exists. AGENTS.md: 20-80 lines, file table, key types. Skip only empty `__init__.py`-only dirs with no logic.

Full convention: `skills/faion-claude-code/project-docs-convention/README.md`

## Directory Structure

**Full documentation:** [docs/directory-structure.md](docs/directory-structure.md)

**SDD feature lifecycle:** `backlog/ → todo/ → in-progress/ → done/`
**Task lifecycle (inside feature):** `todo/ → in-progress/ → done/`

**SDD document types:**
- **constitution.md** - Tech decisions, standards, architecture. Declares per-project `project-spec/` location.
- **roadmap.md** - Feature timeline, releases, success metrics
- **project-spec/** - Per-project source-of-truth folder (domain, business rules, data model, deploy, invariants). See `project-spec-structure` methodology.
- **spec.md** - What to build (requirements, success criteria); delta-only when project-spec/ exists.
- **plan.md** - Merged design + implementation plan; two H2 sections: `## Design` + `## Execution Plan`. See `plan-md-structure` methodology.
- **user-flows.md** - Per-feature, REQUIRED only when user-facing flow exists. See `user-flows-template` methodology.
- **ui-ux-design.md** - Per-feature, REQUIRED only when UI is touched. See `ui-ux-design-template` methodology.
- **readiness.md** - Gate before moving feature to `done/`. See `readiness-checklist` methodology.

**CR / BUG side streams:**
- **crs/{todo,done}/CR0NN-slug.md** - Change requests; lighter than features. See `cr-bug-tracking`.
- **bugs/{todo,in-progress,done}/BUG0NN-slug.md** - Defects with repro + regression test. See `cr-bug-tracking`.

`project-spec/` location is declared per-project in each project's `constitution.md`.

## No Time Estimates

**NEVER provide time estimates** for task execution in SDD workflow:

- ❌ "This will take 2 hours"
- ❌ "Estimated duration: 3 days"
- ❌ "Should be done in 30 minutes"
- ✅ "Task complexity: High" (qualitative)
- ✅ "Est. tokens: ~50k" (resource-based)

**Why:** Time estimates are inherently unreliable and create false expectations. Use complexity levels and token estimates instead.

**In SDD documents:**
- `implementation-plan.md` — NO `estimated_duration` field
- `TASK_*.md` — NO time estimates, use token estimates only
- `roadmap.md` — Use phases/milestones, not dates when possible

## Token Efficiency

**Symbols:** `→` leads to | `⇒` transforms | `✅` done | `❌` failed | `⚠️` warning

**Abbrev:** `cfg` config | `impl` impl | `perf` perf | `sec` security | `dep` dependency

## SDD Memory

**Location:** Project-local `.aidocs/memory/` (not global)

```
.aidocs/memory/
├── patterns.md           # Learned patterns
├── mistakes.md           # Errors and solutions
├── decisions.md          # Key decisions
└── session.md            # Session state
```

**Note:** Memory updates sync to project CLAUDE.md automatically.

## Linting & Pre-Commit Rules

**Every project MUST have pre-commit hooks.** If a hook fails, fix the issue — never skip with `--no-verify`.

### Per-Project Setup

| Project | Tool | Pre-commit | What it checks |
|---------|------|------------|----------------|
| **backend** | ruff | `.pre-commit-config.yaml` | Format, lint (E/W/F/I/B/C4/UP/SIM/DJ/T20), debug statements |
| **dag** | ruff | `.pre-commit-config.yaml` | Same as backend |
| **frontend** | ESLint + Prettier | `.husky/pre-commit` | Format, Angular lint, selector prefix |
| **ddl-builder** | ESLint + Prettier + TS | `.husky/pre-commit` | Format, typecheck, RELEASE_NOTES.md |

### Agent Rules

1. **When hook fails** — read the error, fix the root cause, commit again. Never `--no-verify`.
2. **When adding new Python code** — run `ruff check --fix` before committing. No `print()` in production code (T20).
3. **When adding new TypeScript code** — run `npm run typecheck`. No `any` types.
4. **When finding a new bug pattern** — consider adding a ruff/ESLint rule for it. Document in project AGENTS.md.
5. **DDL Builder** — always update RELEASE_NOTES.md with every commit.

### ruff Quick Reference (Python)

```bash
ruff check .              # Lint
ruff check . --fix        # Lint + auto-fix
ruff format .             # Format (replaces black)
ruff check . --select T20 # Find print() statements
```

Key rule groups: `E` errors, `F` pyflakes, `I` isort, `B` bugbear, `T20` no-print, `DJ` django, `UP` pyupgrade.

## References

- [Claude Code Docs](https://docs.anthropic.com/en/docs/claude-code)
- [Skills](https://docs.anthropic.com/en/docs/claude-code/skills)
- [Sub-agents](https://docs.anthropic.com/en/docs/claude-code/sub-agents)
