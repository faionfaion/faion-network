# CLAUDE.md Creation

## Summary

CLAUDE.md is a project-specific instruction file that gives Claude Code the context it needs: commands, structure, conventions, and gotchas. A well-crafted CLAUDE.md (under 150 lines) eliminates the back-and-forth of Claude asking basic questions about the project setup.

## Why

Claude Code reads CLAUDE.md at session start. Without it, the agent must infer project structure, commands, and conventions from code — a slow, error-prone process that consumes context budget. A 300+ line CLAUDE.md itself wastes context. The sweet spot: concise, structured, focused on what Claude cannot infer from code alone (commands, env vars, gotchas, naming conventions).

## When To Use

- Starting a new project where Claude Code will be the primary AI assistant.
- Inheriting a codebase and needing to orient Claude to existing conventions before making changes.
- After a major dependency upgrade or framework migration that invalidates existing instructions.
- Setting up per-module CLAUDE.md files in a monorepo where modules have different stacks.

## When NOT To Use

- Throwaway scripts or single-file utilities with no ongoing AI-assisted development.
- Projects where team policy prohibits AI coding tools entirely.
- When an accurate CLAUDE.md already exists — update specific sections rather than recreating.

## Content

| File | What's inside |
|------|---------------|
| `content/01-structure-rules.xml` | Required sections, anti-patterns (stale content, duplicate docs, wall of text), length budget. |
| `content/02-conventions.xml` | Content rules for Commands, Structure, Conventions, Key Files sections; monorepo delegation pattern. |

## Templates

| File | Purpose |
|------|---------|
| `templates/claude-md-minimal.md` | Minimal CLAUDE.md (~30 lines) for simple single-stack projects. |
| `templates/claude-md-standard.md` | Standard CLAUDE.md (~100 lines) for FastAPI/Django backends. |
| `templates/claude-md-monorepo.md` | Monorepo root CLAUDE.md that delegates to per-app files. |
| `templates/extract-commands.sh` | Bash script to dump npm scripts and Makefile targets into CLAUDE.md-ready format. |
