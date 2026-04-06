# Claude Code Instructions

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
- **constitution.md** - Tech decisions, standards, architecture
- **roadmap.md** - Feature timeline, releases, success metrics
- **spec.md** - What to build (requirements, success criteria)
- **design.md** - How to build (architecture, API contracts)
- **test-plan.md** - How to verify (test cases per AC, required at feature level)
- **implementation-plan.md** - Task breakdown, dependencies, token estimates

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

## References

- [Claude Code Docs](https://docs.anthropic.com/en/docs/claude-code)
- [Skills](https://docs.anthropic.com/en/docs/claude-code/skills)
- [Sub-agents](https://docs.anthropic.com/en/docs/claude-code/sub-agents)
