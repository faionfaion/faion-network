# AGENTS.md Context Pyramid (CLAUDE.md → AGENTS.md → .agents/INDEX.md)

## Summary

Organize every directory's agent context as a three-tier pyramid: `CLAUDE.md` is a one-line `@AGENTS.md` hook (the only thing Claude Code auto-loads), `AGENTS.md` is a 20-80 line essential brief auto-loaded via `@`-ref AND directly readable by non-Claude-Code agents (Agent SDK, Codex, aider, Cursor), and `.agents/INDEX.md` is the on-demand catalogue of deep references. The convention is enforced per directory — every source folder gets its own `CLAUDE.md` + `AGENTS.md` pair so agents entering at any depth get a calibrated brief without bulk-loading the whole tree.

## Why

Claude Code only auto-loads `CLAUDE.md`; standalone agents (Agent SDK, OpenAI Codex, GitHub Copilot Agent) only read `AGENTS.md`. Putting context in one breaks the other. The `CLAUDE.md = @AGENTS.md` hook is the single mechanic that lets one source of truth (`AGENTS.md`) serve both. The 20-80 line cap on `AGENTS.md` is empirical: above ~5k tokens the routing brief becomes its own context-pollution problem, and below 20 lines it cannot answer "what is this dir + how do I work in it". The per-directory pair ensures an agent that lands in `src/auth/` gets auth-specific context, not the repo-wide overview.

## When To Use

- Any repo where multiple agent kinds (Claude Code + Codex + aider + custom Agent SDK) need to share project context.
- Multi-package monorepos where each subpackage has different commands, gotchas, and dependencies.
- Long-lived projects where decision history and architecture deep-dives must stay searchable but not auto-loaded.
- Migrating from a single bloated `CLAUDE.md` to a routing-friendly layout.

## When NOT To Use

- Single-file scripts or one-off notebooks — the convention's overhead exceeds the benefit.
- Generated directories (build output, vendored deps) — they get rewritten and the docs would drift.
- Trivial leaf folders with under three files and no agent-relevant logic — keep the parent's `AGENTS.md` instead.

## Content

| File | What's inside |
|------|---------------|
| `content/01-three-tier-rule.xml` | The mandatory three-tier shape, the 20-80 line cap, and the `@AGENTS.md` hook rule. |
| `content/02-per-directory-coverage.xml` | Which directories require their own pair; which may inherit from parent; what skip-criteria look like. |

## Templates

| File | Purpose |
|------|---------|
| `templates/CLAUDE.md` | The one-line hook file every directory gets verbatim. |
| `templates/AGENTS.md` | Skeleton with the six required sections (what-is, commands, state, key-paths, gotchas, links). |
| `templates/INDEX.md` | `.agents/INDEX.md` table format that lists deep-reference docs. |
