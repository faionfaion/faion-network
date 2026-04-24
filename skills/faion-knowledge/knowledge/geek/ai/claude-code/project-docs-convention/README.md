# Project Documentation Convention

Convention for organizing documentation in Claude Code projects so that both Claude Code and standalone agents can discover and use the same context.

## Problem

Claude Code auto-loads `CLAUDE.md` files. Standalone agents (Agent SDK, subagents, autoheal) don't — they read files directly. Putting all context in `CLAUDE.md` makes it invisible to non-Claude-Code agents. Putting it elsewhere makes Claude Code unaware.

## Solution: AGENTS.md + @-ref Pattern

```
any-dir/
├── CLAUDE.md       # Always: @AGENTS.md (Claude Code hook, nothing else)
├── AGENTS.md       # Essential context for THIS dir (auto-loaded via @-ref)
├── .agents/        # Detailed reference docs
│   ├── INDEX.md    # Full index of .agents/ contents
│   └── topic/      # Subdirs with own CLAUDE.md + AGENTS.md
└── .product/       # SDD + product docs (per-project)
    └── INDEX.md    # Full index of .product/ contents
```

### How It Works

1. **Claude Code** reads `CLAUDE.md` → follows `@AGENTS.md` → gets essential context
2. **Standalone agents** read `AGENTS.md` directly → same essential context
3. **Either agent** reads `.agents/INDEX.md` when they need details
4. **SDD agents** read `.product/INDEX.md` for specs, designs, plans

### File Roles

| File | Role | Size target | Auto-loaded? |
|------|------|------------|-------------|
| `CLAUDE.md` | Hook — always `@AGENTS.md` | 1 line | By Claude Code |
| `AGENTS.md` | Essential context for this directory | 20-80 lines | Via @-ref |
| `.agents/INDEX.md` | Comprehensive doc index | Unlimited | On demand |
| `.product/INDEX.md` | Product/SDD doc index | Unlimited | On demand |

### What Goes Where

| In AGENTS.md (auto-loaded, keep small) | In .agents/ (on-demand reference) |
|----------------------------------------|-----------------------------------|
| What this directory IS | Architecture deep dives |
| Build / test / deploy commands | API reference, endpoint docs |
| Current state, active gotchas | Historical decisions (ADRs) |
| Key subdirectory listing | Dependency analysis |
| Links to INDEX.md files | Migration guides, troubleshooting |
| Status / health checks | Infrastructure details, port maps |

| In .product/ (per-project SDD + product) | NOT in any of these |
|-----------------------------|---------------------|
| constitution.md (tech stack, standards) | Code files (stay in src/) |
| roadmap.md (features, milestones) | Test files (stay in tests/) |
| spec.md, design.md, implementation-plan.md | Config files (.env, docker-compose) |
| Feature dirs (backlog → todo → in-progress → done) | Git history (use git log) |
| product_docs/, content/, improvements/ | |

## Rules

1. **CLAUDE.md** — ALWAYS contains only `@AGENTS.md`. No exceptions.
2. **AGENTS.md** — Self-contained. No @-refs. Mentions `.agents/INDEX.md` and `.aidocs/INDEX.md` by path (not @-ref) so agents know where to look.
3. **INDEX.md** — Table format: `| File/Dir | Description |`. One line per entry.
4. **.agents/ subdirs** — Each has `CLAUDE.md` (@AGENTS.md) + `AGENTS.md` for recursive discovery.
5. **Don't create .agents/** for trivial dirs (< 3 files, no docs needed).
6. **Don't move code** into .agents/. Only documentation and reference material.

## Compatibility with Faion-network

This convention extends (not replaces) the faion-network directory structure:

| Faion-network concept | Convention mapping |
|----------------------|-------------------|
| `CLAUDE.md` with content | → `CLAUDE.md` = `@AGENTS.md`, content → `AGENTS.md` |
| `.aidocs/` (workspace-level SDD) | Stays as `.aidocs/` at workspace root. Add `INDEX.md`. |
| `.aidocs/` (per-project SDD) | Renamed to `.product/`. Add `INDEX.md`. |
| `.aidocs/product_docs/` | → `.product/product_docs/` (per-project) |
| `.aidocs/improvements/` | → `.product/improvements/` (per-project) |
| `.aidocs/memory/` | → `.product/memory/` (per-project) |
| `.claude/skills/` | Unchanged. Skills use own SKILL.md. |
| `docs/` in repos | Move to `.agents/` or keep if git-tracked public docs. |
| No equivalent | `.agents/` — new, for operational/reference docs |

## INDEX.md Format

```markdown
# Index

## Directories

| Directory | Description |
|-----------|-------------|
| `architecture/` | System design, component diagrams |
| `api/` | REST/WS endpoint reference |

## Files

| File | Description |
|------|-------------|
| `infrastructure.md` | Server topology, ports, domains |
| `decisions.md` | Key architectural decisions |
```

## Audit

```bash
# Check all CLAUDE.md files are @-ref
bash ~/workspace/scripts/audit-claude-md.sh ~

# Agent prompt for full directory audit
cat ~/workspace/scripts/agent-docs-audit.md
```
